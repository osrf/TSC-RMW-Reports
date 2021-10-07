import collections.abc
import argparse
import json
import csv
import sys
import os

from .tabulator import headers, tabulate_database
from .resulter import process_results
from .collector import collect_csv
from .runner import test_suite_run
from .confgen import confgen
from .plotter import do_plot, do_plot_zero_copy, do_line_plot, do_raw_plot, do_histcat_plot
from .scaleplotter import do_scale_plot


def parse_arguments(args) -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog='perf_tool')
    subparsers = parser.add_subparsers(help='This tool has several modes.', dest="subtool")

    config_parser = subparsers.add_parser("confgen", help="Generate a run config file with all options for you to edit")
    config_parser.add_argument("-o", "--output", type=str, default="conf.json", help="Config file to write")

    run_parser = subparsers.add_parser('run', help='Run the performance testsuite')
    run_parser.add_argument("config", type=str, help="Config file with the test setup")
    run_parser.add_argument("-o", "--output-directory", type=str, default=".", help="Output directory that stores generated csv files")
    run_parser.add_argument("-c", "--clean", action="store_true", default=False, help="Clean output directory of csv files before use.")

    collect_parser = subparsers.add_parser('collect', help='Collect data from csv files')
    collect_parser.add_argument("-d", "--database", type=str, default="database.json", help="Database file to store collected results")
    collect_parser.add_argument("-c", "--clean", action="store_true", default=False, help="Clear database file before storing results")
    collect_parser.add_argument("host", help="Name of host that generated the csv files")
    collect_parser.add_argument("mode", help="Name of mode used to generate the csv files (usually SingleProcess or MultiProcess)")
    collect_parser.add_argument('files', nargs='+', help="CSV files to use as input")

    tabulate_parser = subparsers.add_parser('tabulate', help='Turn database file(s) into CSV results')
    tabulate_parser.add_argument("-d", "--database", type=str, default="database.json", help="Database file to use as input")
    tabulate_parser.add_argument("-o", "--csv", type=str, default="data.csv", help="CSV file to write")
    tabulate_parser.add_argument("-f", "--host-filter", type=str, help="Limit which host to include in the output.")
    group = tabulate_parser.add_mutually_exclusive_group()
    group.add_argument('--rate-unlimited', action='store_true', default=False, help="Only include results where rate==0 (=infinite)")
    group.add_argument('--rate-limited', action='store_true', default=False, help="Only include results where rate>0")

    plot_parser = subparsers.add_parser('plot', help='Turn database file(s) into plots')
    plot_parser.add_argument("-d", "--database", type=str, default="database.json", help="Database file to use as input")
    plot_parser.add_argument("variable", type=str, help="Which variable to plot")
    plot_parser.add_argument("-f", "--host-filter", type=str, help="Limit which host to include in the output.")
    group = plot_parser.add_mutually_exclusive_group()
    group.add_argument('--rate-unlimited', action='store_true', default=False, help="Only include results where rate==0 (=infinite)")
    group.add_argument('--rate-limited', action='store_true', default=False, help="Only include results where rate>0")
    group2 = plot_parser.add_mutually_exclusive_group()
    group2.add_argument("-z", "--zero-copy", action='store_true', help="Plot cyclonedds against zero-copy cyclonedds")
    group2.add_argument("-r", "--rclcpp", action='store_true', help="Plot rclcpp cyclonedds against raw cyclonedds")

    lineplot_parser = subparsers.add_parser('lineplot', help='Turn database file(s) into line plots')
    lineplot_parser.add_argument("-d", "--database", type=str, default="database.json", help="Database file to use as input")
    lineplot_parser.add_argument("variable", type=str, help="Which variable to plot")
    lineplot_parser.add_argument("xtype", type=str, help="What to put on the xaxis.")
    lineplot_parser.add_argument("-c", "--constraint", action='append', nargs=2, help="Constrain a variable to a value")
    lineplot_parser.add_argument("-l", "--log", action='store_true', default=False, help="Use logarithmic y-axis")

    histcatplot_parser = subparsers.add_parser('histcatplot', help='Turn database file(s) into line plots')
    histcatplot_parser.add_argument("-d", "--database", type=str, default="database.json", help="Database file to use as input")
    histcatplot_parser.add_argument("variable", type=str, help="Which variable to plot")
    histcatplot_parser.add_argument("-c", "--constraint", action='append', nargs=2, help="Constrain a variable to a value")
    histcatplot_parser.add_argument("-l", "--log", action='store_true', default=False, help="Use logarithmic y-axis")
    histcatplot_parser.add_argument("-y", "--onlycyclone", action='store_true', default=False, help="Use only cyclone")
    histcatplot_parser.add_argument("-r", "--roundtrip", action='store_true', default=False, help="Use roundtrip mode")
    histcatplot_parser.add_argument("-f", "--filename", type=str, default=None, help="Output filename for plot")

    scaleplot_parser = subparsers.add_parser('scaleplot', help='Turn scaling data into plots')
    scaleplot_parser.add_argument("directory", type=str, help="Source directory for scaling data")
    scaleplot_parser.add_argument("variable", type=str, help="Which variable to plot")
    scaleplot_parser.add_argument("range_min", type=int, help="Start of scaling")
    scaleplot_parser.add_argument("range_max", type=int, help="Stop of scaling")
    scaleplot_parser.add_argument("range_step", type=int, help="Step of scaling")
    scaleplot_parser.add_argument("-t", "--topics", action='store_true', default=False, help="Plot topic scaling not nodes")
    scaleplot_parser.add_argument("-l", "--log", action='store_true', default=False, help="Use logarithmic y-axis")
    scaleplot_parser.add_argument("-f", "--filename", type=str, default=None, help="Output filename for plot")

    return parser, parser.parse_args(args)


def update(d, u):
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = update(d.get(k, {}), v)
        else:
            d[k] = v
    return d


def command(args):
    parser, arguments = parse_arguments(args)
    if not arguments:
        parser.print_help()
        return 1

    if arguments.subtool == "confgen":
        with open(arguments.output, 'w') as f:
            json.dump(confgen(), f, indent=4)

    elif arguments.subtool == "run":
        with open(arguments.config) as f:
            configuration = json.load(f)

        test_suite_run(configuration, arguments.output_directory, arguments.clean)

    elif arguments.subtool == "collect":
        fname_db = arguments.database
        database = {'raw': {}}

        if not arguments.clean:
            try:
                with open(fname_db) as dbf:
                    update(database, json.load(dbf))
            except FileNotFoundError:
                pass

        for fname in arguments.files:
            with open(fname) as f:
                collect_csv(f, database['raw'], arguments.host, arguments.mode)

        process_results(database)

        with open(fname_db, 'w') as dbf:
            json.dump(database, dbf)

    elif arguments.subtool == "tabulate":
        fname_db = arguments.database
        fname_csv = arguments.csv
        host = arguments.host_filter
        rate_limited = arguments.rate_limited
        rate_unlimited = arguments.rate_unlimited

        with open(fname_db) as dbf:
            db = json.load(dbf)

        with open(fname_csv, 'w', newline='') as tbf:
            wr = csv.writer(tbf)
            wr.writerow(headers)

            for row in tabulate_database(db, filter_host=host, filter_rate_limited=rate_limited, filter_rate_unlimited=rate_unlimited):
                wr.writerow(row)

    elif arguments.subtool == "plot":
        fname_db = arguments.database
        host = arguments.host_filter
        rate_limited = arguments.rate_limited
        rate_unlimited = arguments.rate_unlimited

        with open(fname_db) as dbf:
            db = json.load(dbf)

        if arguments.zero_copy:
            do_plot_zero_copy(db, arguments.variable, host, rate_limited, rate_unlimited)
        elif arguments.rclcpp:
            do_raw_plot(db, arguments.variable, host, rate_limited, rate_unlimited)
        else:
            do_plot(db, arguments.variable, host, rate_limited, rate_unlimited)

    elif arguments.subtool == "lineplot":
        fname_db = arguments.database

        with open(fname_db) as dbf:
            db = json.load(dbf)

        do_line_plot(db, arguments.variable, arguments.xtype, {k:v for k,v in arguments.constraint}, arguments.log)

    elif arguments.subtool == "histcatplot":
        fname_db = arguments.database

        with open(fname_db) as dbf:
            db = json.load(dbf)

        do_histcat_plot(db, arguments.variable, {k:v for k,v in arguments.constraint}, arguments.log,
                        arguments.onlycyclone, arguments.roundtrip, arguments.filename)

    elif arguments.subtool == "scaleplot":
        do_scale_plot(arguments.directory, arguments.variable, arguments.range_min, arguments.range_max,
                      arguments.range_step, arguments.topics, arguments.log)



def main():
    return command(sys.argv[1:])