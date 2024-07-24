import logging
import shutil
from signal import SIGTERM, SIGINT, SIGTSTP
import signal
from sys import executable, exit
import sys
from warnings import catch_warnings
from argparse import ArgumentParser
from concurrent.futures import ProcessPoolExecutor, as_completed
from contextlib import ExitStack
import polars as pl
import psutil
from polars.exceptions import ChronoFormatWarning
from rich.console import Console
from rich.panel import Panel
from rich.pretty import Pretty
from rich.table import Table, box
from rich.status import Status
from rich import print as richprint
from rich_argparse_plus import RichHelpFormatterPlus
from ctdfjorder.ctdplot import plot_depth_vs, plot_map, plot_secchi_chla
from ctdfjorder.CTDExceptions.CTDExceptions import CTDError
from ctdfjorder.CTD import CTD
from ctdfjorder.utils import save_to_csv
from ctdfjorder.constants import *
from ctdfjorder.Mastersheet import Mastersheet
from os import path, listdir, remove, mkdir, getcwd
from os.path import isfile
console = Console(color_system='windows')


def process_ctd_file(
        file,
        plot: bool = False,
        cached_master_sheet: Mastersheet = None,
        master_sheet_path: str = None,
        verbosity: int = 0,
        plots_folder: str = None,
        filters: zip = None
):
    logger = setup_logging(verbosity)
    steps = [
        (
            "Load File",
            lambda: CTD(
                file,
                plot=plot,
                cached_master_sheet=cached_master_sheet,
                master_sheet_path=master_sheet_path,
            ),
        ),
        ("Filter", lambda data: data.filter_columns_by_range(filters=filters)),
        ("Remove Upcasts", lambda data: data.remove_upcasts()),
        ("Remove Negative", lambda data: data.remove_non_positive_samples()),
        (
            "Remove Invalid Salinity Values",
            lambda data: data.remove_invalid_salinity_values(),
        ),
        ("Clean Salinity AI", lambda data: data.clean("clean_salinity_ai")),
        (
            "Add Surface Measurements",
            lambda data: data.add_surface_salinity_temp_meltwater(),
        ),
        ("Add Absolute Salinity", lambda data: data.add_absolute_salinity()),
        ("Add Density", lambda data: data.add_density()),
        ("Add Potential Density", lambda data: data.add_potential_density()),
        ("Add MLD", lambda data: data.add_mld(20, "potential_density_avg")),
        ("Add BF Squared", lambda data: data.add_bf_squared()),
        ("Plot", lambda data: plot_data(data)),
        ("Exit", lambda data: data.get_df()),
    ]

    def plot_data(my_data):
        plot_depth_vs(
            my_data.get_df(), POTENTIAL_DENSITY_LABEL, plot_folder=plots_folder
        )
        plot_depth_vs(my_data.get_df(), SALINITY_LABEL, plot_folder=plots_folder)

    status = []
    data = None
    with catch_warnings(record=True, action="once") as warning_list:
        warning_list_length = len(warning_list)
        for step_name, step_function in steps:
            try:
                if step_name == "Load File":
                    data = step_function()
                elif step_name == "Exit":
                    return step_function(data), status + ["green"]
                else:
                    step_function(data)
                if (
                        len(warning_list) > warning_list_length
                        and warning_list[-1].category != RuntimeWarning
                        and warning_list[-1].category != ChronoFormatWarning
                ):
                    warning_list_length = len(warning_list)
                    logger.warning(warning_list[-1].message)
                    status.append("yellow")
                else:
                    status.append("green")
            except CTDError as error:
                logger.error(error)
                status.extend(["red"] * (len(steps) - len(status)))
                return None, status
            except Exception as e:
                print(e)
                logger.exception(e)
                status.extend(["red"] * (len(steps) - len(status)))
                return None, status


def generate_status_table(status_table):
    steps = [
        "Load File",
        "Filter",
        "Remove Upcasts",
        "Remove Negative Values",
        "Remove Invalid Salinity Values",
        "Clean Salinity Data",
        "Add Surface Measurements",
        "Add Absolute Salinity",
        "Add Density",
        "Add Potential Density",
        "Add MLD",
        "Add BF Squared",
        "Plot",
        "Exit",
    ]
    table = Table(box=box.SQUARE)
    table.add_column("File", width=30)
    for step in steps:
        table.add_column(step)
    for file, status in status_table:
        table.add_row(file, *[f"[{color}]•[/{color}]" for color in status])
    return table


def run_default(
        plot=False,
        master_sheet_path=None,
        max_workers=1,
        verbosity=0,
        output_file=None,
        debug_run=False,
        status_show=False,
        mapbox_access_token=None,
        filters=None
):
    plots_folder = path.join(get_cwd(), "ctdplots")
    files = get_ctd_filenames_in_dir(get_cwd(), [".rsk", ".csv"])[
            : 20 if debug_run else None
            ]
    total_files = len(files)
    remaining_files = total_files
    if master_sheet_path in files:
        total_files -= 1
        files.remove(master_sheet_path)
    if not files:
        raise CTDError(message="No '.rsk' or '.csv' found in this folder", filename="")
    cached_master_sheet = Mastersheet(master_sheet_path) if master_sheet_path else None
    status_table, results = [], []
    if not status_show:
        Console(quiet=True)
    #live = Live(
        #generate_status_table(status_table),
        #auto_refresh=False,
        #console=live_console,
        #vertical_overflow="ellipsis",
        #transient=True
    #)
    executor = ProcessPoolExecutor(max_workers=max_workers)
    status_spinner_processing = Status(f"Processing {files} files", spinner="earth", console=console)
    status_spinner_combining = Status("Combining CTD profiles", spinner="earth", console=console)
    status_spinner_cleaning_up = Status("Cleaning up", spinner="earth", console=console)
    status_spinner_map_view = Status(
        "Running interactive map view. To shutdown press CTRL+Z.", spinner="earth", console=console
    )
    error_count = 0
    success_count = 0
    with ExitStack() as stack:
        stack.enter_context(status_spinner_processing)
        status_spinner_processing.start()
        status_spinner_processing.update(status=f"Processing {total_files} files. Press CTRL+Z to shutdown.")
        try:
            stack.enter_context(executor)
            futures = {
                executor.submit(
                    process_ctd_file,
                    file,
                    plot,
                    cached_master_sheet,
                    master_sheet_path,
                    verbosity,
                    plots_folder,
                    filters
                ): file
                for file in files
            }
            for future in as_completed(futures):
                file = futures[future]
                result, status = future.result()
                if isinstance(result, pl.DataFrame):
                    results.append(result)
                    success_count += 1
                    remaining_files -= 1
                else:
                    remaining_files -= 1
                    error_count += 1
                if status_show:
                    status_table.append((path.basename(file), status))
                    status_spinner_processing.update(status=f"Processing {remaining_files} files")
            status_spinner_processing.stop()
        except KeyboardInterrupt:
            status_spinner_processing.stop()
            with Status(
                    "Shutdown message received, terminating open profile pipelines",
                    spinner_style="red",
            ) as status_spinner:
                status_spinner.start()
                executor.shutdown(wait=True, cancel_futures=True)
                status_spinner.stop()
                for proc in psutil.process_iter():
                    if proc.name == 'Python':
                        proc.kill()

        finally:
            if status_show:
                console.print(generate_status_table(status_table))
            with console.screen():
                status_spinner_cleaning_up.start()
                executor.shutdown(wait=True, cancel_futures=True)
                status_spinner_cleaning_up.stop()
                status_spinner_combining.start()
                df = pl.concat(results, how="diagonal")
                panel = Panel(
                    Pretty(df.select("pressure", "salinity", "temperature").describe()),
                    title="Overall stats",
                    subtitle=f"Errors/Total: {error_count}/{total_files}",
                )
                pl.Config.set_tbl_rows(-1)
                df_test = df.unique("filename", keep="first").select(
                    pl.col("filename"), pl.col("unique_id")
                )
                df_test.filter(~pl.col("unique_id").is_unique()).write_csv(
                    path.join(get_cwd(), "ISUNIQUE.csv")
                )
                richprint(panel)
                df_exported = save_to_csv(df, output_file)
                status_spinner_combining.stop()
                if plot:
                    if CHLOROPHYLL_LABEL in df.collect_schema():
                        plot_secchi_chla(df, plots_folder)
                    status_spinner_map_view.start()
                    if mapbox_access_token:
                        try:
                            plot_map(df_exported, mapbox_access_token)
                        except KeyboardInterrupt:
                            status_spinner_map_view.stop()
                            for proc in psutil.process_iter():
                                if proc.name == 'Python':
                                    proc.kill()



def get_ctd_filenames_in_dir(directory, types):
    return [
        path.join(directory, f)
        for f in listdir(directory)
        if any(f.endswith(t) for t in types)
    ]


def get_cwd():
    return path.dirname(executable) if getattr(sys, "frozen", False) else getcwd()


def _reset_file_environment():
    cwd = get_cwd()
    for filename in ["output.csv", "ctdfjorder.log"]:
        file_path = path.join(cwd, filename)
        if isfile(file_path):
            remove(file_path)
    if path.isdir("ctdplots"):
        shutil.rmtree("ctdplots")
    mkdir("ctdplots")


def setup_logging(verbosity):
    level = max(30 - (verbosity * 10), 10)
    signal.signal(SIGTERM, handler)
    signal.signal(SIGINT, handler)
    signal.signal(SIGTSTP, handler)
    for logger_name in [
        "tensorflow",
        "matplotlib",
        "sklearn",
        "werkzeug",
        "dash",
        "flask",
    ]:
        logging.getLogger(logger_name).setLevel(logging.ERROR)
    logger = logging.getLogger("ctdfjorder")
    logger.handlers.clear()
    file_log = logging.FileHandler(path.join(get_cwd(), "ctdfjorder.log"))
    logging.basicConfig(level=level)
    file_log.setLevel(level)
    logger.addHandler(file_log)
    return logger


def handler(signal_received, frame):
    if signal_received == SIGINT:
        return
    raise KeyboardInterrupt


def build_parser():
    parser = ArgumentParser(
        description="Default Pipeline", formatter_class=RichHelpFormatterPlus
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    parser_default = subparsers.add_parser(
        "default",
        help="Run the default processing pipeline", formatter_class=RichHelpFormatterPlus
    )
    parser_default.add_argument(
        "-p", "--plot", action="store_true", help="Generate plots"
    )
    parser_default.add_argument(
        "-v",
        "--verbose",
        action="count",
        dest="verbosity",
        default=0,
        help="Verbose logger output to ctdfjorder.log (repeat for increased verbosity)",
    )
    parser_default.add_argument(
        "-q",
        "--quiet",
        action="store_const",
        const=-1,
        default=0,
        dest="verbosity",
        help="Quiet output (show errors only)",
    )
    parser_default.add_argument(
        "-r", "--reset", action="store_true", help="Reset file environment"
    )
    parser_default.add_argument(
        "-s", "--show-status", action="store_true", help="Show processing status and pipeline status"
    )
    parser_default.add_argument(
        "-d", "--debug-run", action="store_true", help="Run 20 files for testing"
    )
    parser_default.add_argument(
        "-m", "--mastersheet", type=str, help="Path to mastersheet"
    )
    parser_default.add_argument(
        "-w", "--workers", type=int, nargs="?", const=1, help="Max workers"
    )
    parser_default.add_argument(
        "--token",
        type=str,
        default=None,
        help="MapBox token to enable interactive map plot",
    )
    parser_default.add_argument(
        "-o", "--output", type=str, default="output.csv", help="Output file path"
    )
    # Assuming columns are passed as a list of strings
    parser_default.add_argument("--filtercolumns", nargs='*', type=str, required=False, default=None, help='List of columns to filter', choices=LIST_LABELS)

    # Upper bounds
    parser_default.add_argument("--filterupper", nargs='*', type=float, required=False, default=None, help='Upper bounds for the filtered columns')

    # Lower bounds
    parser_default.add_argument("--filterlower", nargs='*', type=float, required=False, default=None, help='Lower bounds for the filtered columns')

    return parser


def build_parser_docs():
    RichHelpFormatterPlus.choose_theme('black_and_white')
    parser = ArgumentParser(
        description="Default Pipeline"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    parser_default = subparsers.add_parser(
        "default",
        help="Run the default processing pipeline"
    )
    parser_default.add_argument(
        "-p", "--plot", action="store_true", help="Generate plots"
    )
    parser_default.add_argument(
        "-v",
        "--verbose",
        action="count",
        dest="verbosity",
        default=0,
        help="Verbose logger output to ctdfjorder.log (repeat for increased verbosity)",
    )
    parser_default.add_argument(
        "-q",
        "--quiet",
        action="store_const",
        const=-1,
        default=0,
        dest="verbosity",
        help="Quiet output (show errors only)",
    )
    parser_default.add_argument(
        "-r", "--reset", action="store_true", help="Reset file environment"
    )
    parser_default.add_argument(
        "-s", "--show-status", action="store_true", help="Show processing status and pipeline status"
    )
    parser_default.add_argument(
        "-d", "--debug-run", action="store_true", help="Run 20 files for testing"
    )
    parser_default.add_argument(
        "-m", "--mastersheet", type=str, help="Path to mastersheet"
    )
    parser_default.add_argument(
        "-w", "--workers", type=int, nargs="?", const=1, help="Max workers"
    )
    parser_default.add_argument(
        "-o", "--output", type=str, default="output.csv", help="Output file path"
    )
    # Assuming columns are passed as a list of strings
    parser_default.add_argument("--filtercolumns", nargs='*', type=str, required=False, default=None, help='List of columns to filter',
                                choices=LIST_LABELS)

    # Upper bounds
    parser_default.add_argument("--filterupper", nargs='*', type=float, required=False, default=None, help='Upper bounds for the filtered columns')

    # Lower bounds
    parser_default.add_argument("--filterlower", nargs='*', type=float, required=False, default=None, help='Lower bounds for the filtered columns')

    parser_default.add_argument(
        "--token",
        type=str,
        default=None,
        help="MapBox token to enable interactive map plot",
    )
    return parser


def main():
    signal.signal(SIGINT, handler)
    signal.signal(SIGTSTP, handler)
    signal.signal(SIGTERM, handler)
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "default":
        if type(args.filtercolumns) is not type(None) and type(args.filterupper) is not type(None) and type(args.filterlower) is not type(None):
            columns = args.filtercolumns
            upper_bounds = args.filterupper
            lower_bounds = args.filterlower
            filters = zip(columns, upper_bounds, lower_bounds)
        else:
            filters = None
        if args.reset:
            _reset_file_environment()

        table = Table(title="Processing Pipeline Config")
        table.add_column("Argument", style="cyan", no_wrap=True)
        table.add_column("Value", style="magenta")
        for arg in vars(args):
            table.add_row(arg.replace("_", " ").title(), str(getattr(args, arg)))
        console.print(table)

        run_default(
            plot=args.plot,
            master_sheet_path=args.mastersheet,
            max_workers=args.workers,
            verbosity=args.verbosity,
            output_file=args.output,
            debug_run=args.debug_run,
            status_show=args.show_status,
            mapbox_access_token=args.token,
            filters=filters,
        )
        exit()


if __name__ == '__main__':
    main()
