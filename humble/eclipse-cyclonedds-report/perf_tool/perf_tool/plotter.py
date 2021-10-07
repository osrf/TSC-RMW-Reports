from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from dataclasses import dataclass, field
from typing import DefaultDict, List
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

import numpy as np
import json

from .resulter import Status, make_comparison, boolify


def data_select(database, variable_name, filter_host=None, filter_rate_limited=False, filter_rate_unlimited=False):
    tests = database["processed"]
    n_tests = 0
    n_win = 0
    n_lost = 0
    n_both = 0

    if variable_name == 'roundtrip':
        variable_name = 'latency_mean'

    cyclone_values, fast_values, ratios, point_type = [], [], [], []
    cyclone_fail_fast_values, cyclone_fail_point_type = [], []
    fast_fail_cyclone_values, fast_fail_point_type = [], []

    for test in tests:
        if filter_host is not None and test['host'] != filter_host:
            continue

        if filter_rate_limited and test['rate'] == 0:
            continue

        if filter_rate_unlimited and test['rate'] != 0:
            continue

        cyclone = test["cyclonedds"]
        fast = test["fastrtps"]
        comparison = test["comparison"]

        n_tests += 1

        if comparison[variable_name] == Status.CYCLONEDDS_WIN.value:
            ratios.append(- comparison[variable_name + "_diff"] + 1)
            cyclone_values.append(cyclone[variable_name])
            fast_values.append(fast[variable_name])
            point_type.append((test['host'], test['topic']))
            n_both += 1
            n_win += 1
        elif comparison[variable_name] == Status.FASTRTPS_WIN.value:
            ratios.append(comparison[variable_name + "_diff"] - 1)
            cyclone_values.append(cyclone[variable_name])
            fast_values.append(fast[variable_name])
            point_type.append((test['host'], test['topic']))
            n_both += 1
            n_lost += 1
        elif comparison[variable_name] == Status.FASTRTPS_FAIL.value:
            fast_fail_cyclone_values.append(cyclone[variable_name])
            fast_fail_point_type.append((test['host'], test['topic']))
            n_win += 1
        elif comparison[variable_name] == Status.CYCLONEDDS_FAIL.value:
            cyclone_fail_fast_values.append(fast[variable_name])
            cyclone_fail_point_type.append((test['host'], test['topic']))
            n_lost += 1

    return {
        'N': n_tests,
        'Nwin': n_win,
        'Nlost': n_lost,
        'Nboth': n_both,
        'cyclone_values': cyclone_values,
        'fast_values': fast_values,
        'ratios': ratios,
        'point_type': point_type,
        'cyclone_fail_fast_values': cyclone_fail_fast_values,
        'cyclone_fail_point_type': cyclone_fail_point_type,
        'fast_fail_cyclone_values': fast_fail_cyclone_values,
        'fast_fail_point_type': fast_fail_point_type
    }


host_colours = {
    "Ubuntu": "#E95420",
    "Windows": "#00A4EF",
    "RPi4B": "#6CC04A",
    "macOS M1": "#A2AAAD"
}

topic_colours = {
    "Array16k": "#72e5ef",
    "Array2m": "#fa557a",
    "Struct32k": "#1fa198",
    "Struct16": "#d3776f",
    "PointCloud1m": "#4397d7",
    "PointCloud4m": "#f6932e",
    "PointCloud8m": "#f6602e"
}

titles_labels_ylog_reverse = {
    'cpu_usage': ('CPU usage', 'CPU usage (%)', False, False),
    'rel_cpu_usage': ('relative CPU usage per message', 'CPU usage (%/msg)', False, False),
    'ram_usage': ('RAM usage', 'RAM usage (MB)', True, False),
    'latency_mean': ('mean latency', 'mean latency (ms)', True, False),
    'jitter': ('jitter', 'jitter (ms)', True, False),
    'throughput': ('throughput', 'throughput (MB/s/subscriber)', False, True),
    'roundtrip': ('roundtrip', 'roundtrip (ms)', False, False)
}

COL_CYCLONE = "#D0343A"
COL_FAST = "#999999"
COL_FAST_TEXT="#777777"
COL_ICEORYX = "#af1c21"
FONT_TINY = 15
FONT_SMALL = 19
FONT_BIG = 22
FONT_HUGE = 30


def do_plot(database, variable_name, filter_host=None, filter_rate_limited=False, filter_rate_unlimited=False):
    # Label plot by host if we do not filter to single host
    label_index = 0 if filter_host is None else 1
    label_colours = host_colours if filter_host is None else topic_colours

    dataset = data_select(database, variable_name, filter_host, filter_rate_limited, filter_rate_unlimited)
    title, axlabel, ylog, reverse_win = titles_labels_ylog_reverse[variable_name]

    fig = plt.figure(figsize=(20, 8), constrained_layout=True)
    gs = GridSpec(8, 20, figure=fig)
    lhist = plt.subplot(gs.new_subplotspec((0, 0), colspan=12, rowspan=8))

    rplot = plt.subplot(gs.new_subplotspec((1, 12), colspan=7, rowspan=7))
    topb = plt.subplot(gs.new_subplotspec((0, 12), colspan=7, rowspan=1))
    rightb = plt.subplot(gs.new_subplotspec((1, 19), colspan=1, rowspan=7))

    if ylog:
        if dataset['Nboth'] > 0:
            rplot.set_yscale('log')
            rplot.set_xscale('log')

        if len(dataset['cyclone_fail_fast_values']):
            rightb.set_yscale('log')

        if len(dataset['fast_fail_cyclone_values']):
            topb.set_xscale('log')

    toplot = DefaultDict(list)

    for i in range(dataset['Nboth']):
        toplot[dataset['point_type'][i][label_index]].append((
            dataset['cyclone_values'][i],
            dataset['fast_values'][i]
        ))

    for label, data in toplot.items():
        amount = len(data) + \
                 len([d[label_index] == label for d in dataset['fast_fail_point_type']]) + \
                 len([d[label_index] == label for d in dataset['cyclone_fail_point_type']])

        rplot.scatter(
            [d[1 if reverse_win else 0] for d in data],
            [d[0 if reverse_win else 1] for d in data],
            label=f"{label} ({amount})", c=label_colours.get(label), s=65, edgecolor='black', linewidth=1)

    if reverse_win:
        topb.scatter(
            dataset['cyclone_fail_fast_values'],
            [0.0] * len(dataset['cyclone_fail_fast_values']),
            c=[label_colours.get(k[label_index]) or 'black'
            for k in dataset['cyclone_fail_point_type']],
            s=65, edgecolor='black', linewidth=1
        )
        rightb.scatter(
            [0.0] * len(dataset['fast_fail_cyclone_values']),
            dataset['fast_fail_cyclone_values'],
            facecolor=[label_colours.get(k[label_index]) or 'black'
            for k in dataset['fast_fail_point_type']],
            s=65, edgecolor='black', linewidth=1
        )
    else:
        topb.scatter(
            dataset['fast_fail_cyclone_values'],
            [0.0] * len(dataset['fast_fail_cyclone_values']),
            c=[label_colours.get(k[label_index]) or 'black'
            for k in dataset['fast_fail_point_type']],
            s=65, edgecolor='black', linewidth=1
        )
        rightb.scatter(
            [0.0] * len(dataset['cyclone_fail_fast_values']),
            dataset['cyclone_fail_fast_values'],
            facecolor=[label_colours.get(k[label_index]) or 'black'
            for k in dataset['cyclone_fail_point_type']],
            s=65, edgecolor='black', linewidth=1
        )

    hdata = np.array(dataset['ratios']).clip(-3, 3)
    lhist.hist(hdata, range=(-3, 0), bins=12, histtype='step', linewidth=2, facecolor=COL_CYCLONE, fill=True, edgecolor='black',
        label=f"Cyclone DDS wins {dataset['Nwin']} tests")
    lhist.hist([-3.26] * len(dataset['fast_fail_cyclone_values']), range=(-3.5,-3.25), bins=1, histtype='step',
               linewidth=2, facecolor=COL_CYCLONE, fill=True, edgecolor='black', hatch='///',
               label=f"other fails {len(dataset['fast_fail_cyclone_values'])} tests")
    lhist.hist(hdata, range=(0, 3), bins=12, histtype='step', linewidth=2, facecolor=COL_FAST, fill=True, edgecolor='black',
        label=f"other wins {dataset['Nlost']} tests")
    lhist.hist([3.26] * len(dataset['cyclone_fail_fast_values']), range=(3.25,3.5), bins=1, histtype='step',
               linewidth=2, facecolor=COL_FAST, fill=True, edgecolor='black', hatch='///',
               label=f"Cyclone DDS failed {len(dataset['cyclone_fail_fast_values'])} tests")

    ylims = lhist.get_ylim()
    lhist.set_ylim(0, ylims[1] * 1.2)

    l = lhist.legend(frameon=False, fontsize=FONT_SMALL)
    l.get_texts()[0].set_color(COL_CYCLONE)
    l.get_texts()[1].set_color(COL_CYCLONE)
    l.get_texts()[2].set_color(COL_FAST_TEXT)
    l.get_texts()[3].set_color(COL_FAST_TEXT)

    if reverse_win:
        l = rplot.set_ylabel(f"Cyclone DDS {axlabel}", fontsize=FONT_SMALL)
        l.set_color(COL_CYCLONE)
        l = rplot.set_xlabel(f"other {axlabel}", fontsize=FONT_SMALL)
        l.set_color(COL_FAST_TEXT)
    else:
        l = rplot.set_xlabel(f"Cyclone DDS {axlabel}", fontsize=FONT_SMALL)
        l.set_color(COL_CYCLONE)
        l = rplot.set_ylabel(f"other {axlabel}", fontsize=FONT_SMALL)
        l.set_color(COL_FAST_TEXT)

    minl = min(rplot.get_xlim()[0], rplot.get_ylim()[0])
    maxl = max(rplot.get_xlim()[1], rplot.get_ylim()[1])

    if ylog:
        maxl *= 10
    else:
        maxl += 0.25 * (maxl - minl)

    rplot.plot([minl, maxl], [minl, maxl], 'k-')
    rplot.set_xlim(minl, maxl)
    rplot.set_ylim(minl, maxl)
    topb.set_xlim(minl, maxl)
    rightb.set_ylim(minl, maxl)

    rplot.spines['right'].set_visible(False)
    rplot.spines['top'].set_visible(False)
    lhist.spines['right'].set_visible(False)
    lhist.spines['top'].set_visible(False)
    topb.spines['right'].set_visible(False)
    topb.spines['top'].set_visible(False)
    topb.spines['bottom'].set_visible(False)
    rightb.spines['right'].set_visible(False)
    rightb.spines['top'].set_visible(False)
    rightb.spines['left'].set_visible(False)

    rightb.tick_params(axis='y', which='both', left=False, right=False, labelleft=False)
    topb.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    rplot.tick_params(axis='both', which='major', labelsize=FONT_TINY)


    if reverse_win:
        topb.tick_params(axis='x', which='both', left=False, right=False, labelleft=False)
        rightb.tick_params(axis='y', which='both', bottom=False, top=False, labelbottom=False)
        topb.set_yticks([0])
        topb.set_yticklabels([f"Cyclone\nfailed {len(dataset['cyclone_fail_fast_values'])}"], color=COL_FAST_TEXT, fontsize=FONT_TINY)
        rightb.set_xticks([0])
        rightb.set_xticklabels([f"other\nfailed {len(dataset['fast_fail_cyclone_values'])}"], color=COL_FAST_TEXT, fontsize=FONT_TINY)
    else:
        rightb.tick_params(axis='y', which='both', left=False, right=False, labelleft=False)
        topb.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
        rightb.set_xticks([0])
        rightb.set_xticklabels([f"Cyclone\nfailed {len(dataset['cyclone_fail_fast_values'])}"], color=COL_FAST_TEXT, fontsize=FONT_TINY)
        topb.set_yticks([0])
        topb.set_yticklabels([f"other\nfailed {len(dataset['fast_fail_cyclone_values'])}"], color=COL_FAST_TEXT, fontsize=FONT_TINY)

    lhist.set_xlabel("    ← Cyclone DDS advantage", loc="left", fontsize=FONT_SMALL, color=COL_CYCLONE)
    lhist.set_ylabel("#tests", fontsize=FONT_SMALL)
    lhist.set_xticks([-3, -2, -1, 0, 1, 2, 3])
    lhist.set_xticklabels(["4x", "3x", '2x', '1x', '2x', '3x', '4x'], fontsize=FONT_TINY)

    if variable_name == "rel_cpu_usage" and filter_host == "macOS M1":
        rplot.set_xticks([0, 0.01, 0.02])
        rplot.set_xticklabels(["0.00", "0.01", "0.02"])
        rplot.set_yticks([0, 0.01, 0.02])
        rplot.set_yticklabels(["0.00", "0.01", "0.02"])

    rplot.text(0.95, 0.99, 'Cyclone DDS wins',
        verticalalignment='top', horizontalalignment='right',
        transform=rplot.transAxes,
        color=COL_CYCLONE, fontsize=FONT_TINY)
    rplot.text(0.99, 0.95, 'other wins',
        verticalalignment='top', horizontalalignment='right',
        rotation=-90,
        transform=rplot.transAxes,
        color=COL_FAST_TEXT, fontsize=FONT_TINY)


    loc = 0
    if variable_name in ["latency_mean", "jitter"] and filter_host == "Ubuntu":
        loc = 2
    if variable_name == "jitter" and filter_host is None:
        loc = 4

    l = rplot.legend(frameon=False, loc=loc, fontsize=FONT_SMALL * 0.9)

    for i in range(len(l.legendHandles)):
        l.legendHandles[i]._sizes = [100]

    host_title = f" on {filter_host}" if filter_host is not None else ""
    rate_title = "" if not filter_rate_limited and not filter_rate_unlimited else (
        " with limited rate" if filter_rate_limited else " with unlimited rate"
    )
    fig.suptitle(f"{title}{host_title} for {dataset['N']} tests{rate_title}", fontsize=FONT_HUGE)

    pre_f = filter_host or "combined"

    fig.savefig(f"plots/{pre_f}_{variable_name}.png".replace(" ", "-"))


def linedata_select(database, variable_name, plotvars):
    tests = database["processed"]
    vars = ['host', 'mode', 'topic', 'rate', 'subs', 'zero_copy', 'reliable', 'transient']

    for constraint_name, constraint_value in plotvars['constraints'].items():
        vars.remove(constraint_name)
    vars.remove(plotvars['var'])

    data = {}

    for test in tests:
        use = True
        for constraint_name, constraint_value in plotvars['constraints'].items():
            if test[constraint_name] != constraint_value:
                use = False
                break

        if not use:
            continue

        cyclone = test["cyclonedds"]
        fast = test["fastrtps"]
        comparison = test["comparison"]

        subdata = data
        for var in vars:
            if test[var] not in subdata:
                subdata[test[var]] = {}
            subdata = subdata[test[var]]

        if 'cyclonedds' not in subdata:
            subdata['cyclonedds'] = {}
        if 'fastrtps' not in subdata:
            subdata['fastrtps'] = {}

        if comparison[variable_name] in [Status.CYCLONEDDS_WIN.value, Status.FASTRTPS_WIN.value]:
            subdata['cyclonedds'][test[plotvars['var']]] = cyclone[variable_name]
            subdata['fastrtps'][test[plotvars['var']]] = fast[variable_name]

        elif comparison[variable_name] == Status.FASTRTPS_FAIL.value:
            subdata['cyclonedds'][test[plotvars['var']]] = cyclone[variable_name]

        elif comparison[variable_name] == Status.CYCLONEDDS_FAIL.value:
            subdata['fastrtps'][test[plotvars['var']]] = fast[variable_name]

    return vars, data


line_plot_xtypes = {
    'rate': {'var': 'rate', 'columns': (('20/s', 20, ), ('100/s', 100), ('500/s', 500, ), ('unlimited', 0)), 'xlabel': "Publishing rate (#msg/s)"},
    'subs': {'var': 'subs', 'columns': (('1', 1), ('3', 3), ('5', 5)), 'xlabel': '#Subscribers'},
    'topic_size': {'var': 'topic', 'xlabel': 'Topic', 'columns':
        (('16B struct', 'Struct16'), ('16kb array', 'Array16k'), ('32kb struct', 'Struct32k'),
         ('1MB pointcloud', 'PointCloud1m'), ('2MB array', 'Array2m'), ('4MB pointcloud', 'PointCloud4m')),
    },
    'host': {'var': 'host', 'columns': (('RPi4B', 'RPi4B'), ('Windows', 'Windows'), ('Ubuntu', 'Ubuntu'), ('macOS M1', 'macOS M1')),
        'xlabel': 'Platform'}
}

rmw_names = {
    'cyclonedds': 'Cyclone DDS',
    'fastrtps': 'other',
    'cyclone': 'Cyclone DDS',
    'fast': 'other'
}

def get_cmap(n, name='hsv'):
    '''Returns a function that maps each index in 0, 1, ..., n-1 to a distinct 
    RGB color; the keyword argument name must be a standard mpl colormap name.'''
    return plt.cm.get_cmap(name, n)


def do_line_plot(database, variable_name, xtype, constraints, ylog):
    if 'subs' in constraints:
        constraints['subs'] = int(constraints['subs'])

    if 'rate' in constraints:
        constraints['rate'] = int(constraints['rate'])

    if 'reliable' in constraints:
        constraints['reliable'] = boolify(constraints['reliable'])

    if 'reliable' in constraints:
        constraints['transient'] = boolify(constraints['transient'])

    if 'zero_copy' in constraints:
        constraints['zero_copy'] = boolify(constraints['zero_copy'])


    plotvars = line_plot_xtypes[xtype]
    plotvars['constraints'] = constraints
    path, dataset = linedata_select(database, variable_name, plotvars)

    fig = plt.figure(figsize=(13, 8), constrained_layout=True)
    gs = GridSpec(8, 13, figure=fig)
    lineplot = plt.subplot(gs.new_subplotspec((0, 0), colspan=10, rowspan=8))
    textplot = plt.subplot(gs.new_subplotspec((0, 10), colspan=3, rowspan=8))
    textplot.set_axis_off()

    textplot.text(0.01, 0.97, "Constraints:",
        verticalalignment='top', horizontalalignment='left',
        transform=textplot.transAxes,
        color='black', fontsize=FONT_SMALL)

    textplot.text(0.01, 0.94, "\n".join(f"{key}: {value}" for key, value in constraints.items()),
        verticalalignment='top', horizontalalignment='left',
        transform=textplot.transAxes,
        color='black', fontsize=FONT_TINY)

    legend_items = []
    legend_names = []
    coli = 0
    colm = 0
    fail_notes = []

    def count_for(data, key, *vars):
        if vars:
            var = vars[0]
            for name, subdata in data.items():
                count_for(subdata, f"{key} {var}:{name}", *vars[1:])
        else:
            nonlocal colm
            colm += 1

    count_for(dataset, "", *path)
    cmap = get_cmap(colm, 'YlGnBu')

    def plot_for(data, key, *vars):
        if vars:
            var = vars[0]
            for name, subdata in data.items():
                plot_for(subdata, f"{key} {var}:{name}", *vars[1:])
        else:
            nonlocal coli
            c = cmap(coli)
            coli += 1

            for rmw, rmwdata in data.items():
                plot_data = []
                for i, (colname, colvar) in enumerate(plotvars['columns']):
                    if colvar not in rmwdata:
                        fail_notes.append(f"{rmw_names[rmw]} failed {colname}{key}")
                    else:
                        plot_data.append((i, rmwdata[colvar]))

                x = [d[0] for d in plot_data]
                y = [d[1] for d in plot_data]

                line, = lineplot.plot(x, y, linewidth=3, color=c)
                dotted_line = Line2D(x, y, linewidth=3, linestyle="--", color=COL_CYCLONE if rmw == "cyclonedds" else COL_FAST)
                lineplot.add_artist(dotted_line)

                legend_items.append((line, dotted_line))
                legend_names.append(f"{rmw_names[rmw]}{key}")

    plot_for(dataset, "", *path)

    if fail_notes:
        size = FONT_TINY if len(fail_notes) < 15 else FONT_TINY * 0.66

        textplot.text(0.01, 0.70, "Failures:",
            verticalalignment='top', horizontalalignment='left',
            transform=textplot.transAxes,
            color='black', fontsize=FONT_SMALL)

        textplot.text(0.01, 0.67, "\n".join(fail_notes),
            verticalalignment='top', horizontalalignment='left',
            transform=textplot.transAxes,
            color='black', fontsize=size)

    if ylog:
        lineplot.set_yscale('log')

    lineplot.tick_params(axis='both', which='major', labelsize=FONT_TINY)
    textplot.legend(legend_items, legend_names, loc=8, handlelength=4, frameon=False)
    lineplot.set_xticks(list(range(len(plotvars['columns']))))
    lineplot.set_xticklabels([c[0] for c in plotvars['columns']], fontsize=FONT_TINY)
    lineplot.set_xlabel(plotvars['xlabel'], fontsize=FONT_SMALL)
    lineplot.set_ylabel(titles_labels_ylog_reverse[variable_name][1], fontsize=FONT_SMALL)
    fig.suptitle(f"{titles_labels_ylog_reverse[variable_name][0]}", fontsize=FONT_HUGE)

    fig.savefig(f'plots/line_{variable_name}_{xtype}.png')




def data_select_zero_copy(database, variable_name, filter_host=None, filter_rate_limited=False, filter_rate_unlimited=False):
    tests = database["processed"]
    n_tests = 0
    n_win = 0
    n_both = 0
    n_lost = 0

    cyclone_values, zerocopy_values, ratios, point_type = [], [], [], []
    cyclone_fail_zerocopy_values, cyclone_fail_point_type = [], []
    zerocopy_fail_cyclone_values, zerocopy_fail_point_type = [], []

    for test in tests:
        if not test['zero_copy']:
            continue

        if test['cyclonedds'] is None:
            continue

        if filter_host is not None and test['host'] != filter_host:
            continue

        if filter_rate_limited and test['rate'] == 0:
            continue

        if filter_rate_unlimited and test['rate'] != 0:
            continue

        for ctest in tests:
            if ctest['zero_copy']:
                continue

            # test['host'] != ctest['host'] or test['mode'] != ctest['mode'] or test['reliable'] != ctest['reliable'] or
            if test['topic'] != ctest['topic'] or \
                test['rate'] != ctest['rate'] or test['subs'] != ctest['subs'] or \
                test['transient'] != ctest['transient']:
                continue

            if ctest['cyclonedds'] is None:
                continue

            cyclone = ctest["cyclonedds"]
            zerocopy = test["cyclonedds"]
            comparison = make_comparison(cyclone, zerocopy)

            n_tests += 1

            if comparison[variable_name] == Status.CYCLONEDDS_WIN.value:
                ratios.append(comparison[variable_name + "_diff"] - 1)
                cyclone_values.append(cyclone[variable_name])
                zerocopy_values.append(zerocopy[variable_name])
                point_type.append((test['host'], test['topic']))
                n_both += 1
                n_win += 1
            elif comparison[variable_name] == Status.FASTRTPS_WIN.value:
                ratios.append(- comparison[variable_name + "_diff"] + 1)
                cyclone_values.append(cyclone[variable_name])
                zerocopy_values.append(zerocopy[variable_name])
                point_type.append((test['host'], test['topic']))
                n_both += 1
                n_lost += 1
            elif comparison[variable_name] == Status.FASTRTPS_FAIL.value:
                zerocopy_fail_cyclone_values.append(cyclone[variable_name])
                zerocopy_fail_point_type.append((test['host'], test['topic']))
                n_win += 1
            elif comparison[variable_name] == Status.CYCLONEDDS_FAIL.value:
                cyclone_fail_zerocopy_values.append(zerocopy[variable_name])
                cyclone_fail_point_type.append((test['host'], test['topic']))
                n_lost += 1

            break

    return {
        'N': n_tests,
        'Nwin': n_win,
        'Nlost': n_lost,
        'Nboth': n_both,
        'cyclone_values': cyclone_values,
        'zerocopy_values': zerocopy_values,
        'ratios': ratios,
        'point_type': point_type,
        'cyclone_fail_zerocopy_values': cyclone_fail_zerocopy_values,
        'cyclone_fail_point_type': cyclone_fail_point_type,
        'zerocopy_fail_cyclone_values': zerocopy_fail_cyclone_values,
        'zerocopy_fail_point_type': zerocopy_fail_point_type
    }



def do_plot_zero_copy(database, variable_name, filter_host=None, filter_rate_limited=False, filter_rate_unlimited=False):
    # Label plot by host if we do not filter to single host
    label_index = 0 if filter_host is None else 1
    label_colours = host_colours if filter_host is None else topic_colours

    dataset = data_select_zero_copy(database, variable_name, filter_host, filter_rate_limited, filter_rate_unlimited)
    title, axlabel, ylog, reverse_win = titles_labels_ylog_reverse[variable_name]

    fig = plt.figure(figsize=(20, 8), constrained_layout=True)
    gs = GridSpec(8, 20, figure=fig)
    lhist = plt.subplot(gs.new_subplotspec((0, 0), colspan=12, rowspan=8))
    rplot = plt.subplot(gs.new_subplotspec((1, 12), colspan=7, rowspan=7))
    topb = plt.subplot(gs.new_subplotspec((0, 12), colspan=7, rowspan=1))
    rightb = plt.subplot(gs.new_subplotspec((1, 19), colspan=1, rowspan=7))

    if ylog:
        if dataset['Nboth'] > 0:
            rplot.set_yscale('log')
            rplot.set_xscale('log')

        if len(dataset['cyclone_fail_zerocopy_values']):
            rightb.set_yscale('log')

        if len(dataset['zerocopy_fail_cyclone_values']):
            topb.set_xscale('log')

    toplot = DefaultDict(list)

    for i in range(dataset['Nboth']):
        toplot[dataset['point_type'][i][label_index]].append((
            dataset['cyclone_values'][i],
            dataset['zerocopy_values'][i]
        ))

    for label, data in toplot.items():
        amount = len(data) + \
                 len([d[label_index] == label for d in dataset['zerocopy_fail_point_type']]) + \
                 len([d[label_index] == label for d in dataset['cyclone_fail_point_type']])

        rplot.scatter([d[1] for d in data], [d[0] for d in data], label=f"{label} ({amount})",
                      c=label_colours.get(label), s=65, edgecolor='black', linewidth=1)

    topb.scatter(
        dataset['zerocopy_fail_cyclone_values'],
        [0.0] * len(dataset['zerocopy_fail_cyclone_values']),
        c=[label_colours.get(k[label_index]) or 'black'
           for k in dataset['zerocopy_fail_point_type']],
        s=65, edgecolor='black', linewidth=1
    )
    rightb.scatter(
        [0.0] * len(dataset['cyclone_fail_zerocopy_values']),
        dataset['cyclone_fail_zerocopy_values'],
        facecolor=[label_colours.get(k[label_index]) or 'black'
           for k in dataset['cyclone_fail_point_type']],
        s=65, edgecolor='black', linewidth=1
    )

    hdata = np.array(dataset['ratios']).clip(-3, 3)
    lhist.hist(hdata, range=(-3, 0), bins=12, histtype='step', linewidth=2, facecolor=COL_ICEORYX, fill=True, edgecolor='black',
        label=f"Cyclone DDS + iceoryx wins {dataset['Nlost']} tests")
    lhist.hist([-3.26] * len(dataset['cyclone_fail_zerocopy_values']), range=(-3.5,-3.25), bins=1, histtype='step',
               linewidth=2, facecolor=COL_ICEORYX, fill=True, edgecolor='black', hatch='///',
               label=f"Cyclone DDS failed {len(dataset['cyclone_fail_zerocopy_values'])} tests")
    lhist.hist(hdata, range=(0, 3), bins=12, histtype='step', linewidth=2, facecolor=COL_FAST, fill=True, edgecolor='black',
        label=f"Cyclone DDS wins {dataset['Nwin']} tests")
    lhist.hist([3.26] * len(dataset['zerocopy_fail_cyclone_values']), range=(3.25,3.5), bins=1, histtype='step',
               linewidth=2, facecolor=COL_FAST, fill=True, edgecolor='black', hatch='///',
               label=f"Cyclone DDS + iceoryx fails {len(dataset['zerocopy_fail_cyclone_values'])} tests")

    ylims = lhist.get_ylim()
    lhist.set_ylim(0, ylims[1] * 1.3)

    l = lhist.legend(frameon=False, loc=2, fontsize=FONT_SMALL)
    l.get_texts()[0].set_color(COL_ICEORYX)
    l.get_texts()[1].set_color(COL_ICEORYX)
    l.get_texts()[2].set_color(COL_FAST_TEXT)
    l.get_texts()[3].set_color(COL_FAST_TEXT)

    l = rplot.set_ylabel(f"Cyclone DDS {axlabel}", fontsize=FONT_SMALL)
    l.set_color(COL_FAST_TEXT)
    l = rplot.set_xlabel(f"Cyclone DDS + iceoryx {axlabel}", fontsize=FONT_SMALL)
    l.set_color(COL_ICEORYX)

    minl = min(rplot.get_xlim()[0], rplot.get_ylim()[0])
    maxl = max(rplot.get_xlim()[1], rplot.get_ylim()[1])
    maxl += 0.2 * (maxl - minl)

    rplot.plot([minl, maxl], [minl, maxl], 'k-')
    rplot.set_xlim(minl, maxl)
    rplot.set_ylim(minl, maxl)
    topb.set_xlim(minl, maxl)
    rightb.set_ylim(minl, maxl)

    rplot.legend(frameon=False, fontsize=FONT_SMALL)
    rplot.spines['right'].set_visible(False)
    rplot.spines['top'].set_visible(False)
    lhist.spines['right'].set_visible(False)
    lhist.spines['top'].set_visible(False)
    topb.spines['right'].set_visible(False)
    topb.spines['top'].set_visible(False)
    topb.spines['bottom'].set_visible(False)
    rightb.spines['right'].set_visible(False)
    rightb.spines['top'].set_visible(False)
    rightb.spines['left'].set_visible(False)

    rightb.tick_params(axis='y', which='both', left=False, right=False, labelleft=False)
    topb.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    rplot.tick_params(axis='both', which='major', labelsize=FONT_TINY)

    rightb.set_xticks([0])
    rightb.set_xticklabels([f"Cyclone\nfailed {len(dataset['cyclone_fail_zerocopy_values'])}"], color=COL_FAST, fontsize=FONT_TINY)
    topb.set_yticks([0])
    topb.set_yticklabels([f"Cyclone DDS + iceoryx\nfailed {len(dataset['zerocopy_fail_cyclone_values'])}"], color=COL_FAST, fontsize=FONT_TINY)

    lhist.set_xlabel("    ← Cyclone DDS + iceoryx advantage", loc="left", fontsize=FONT_SMALL, color=COL_ICEORYX)
    lhist.set_ylabel("#tests", fontsize=FONT_SMALL)
    lhist.set_xticks([-3, -2, -1, 0, 1, 2, 3])
    lhist.set_xticklabels(["4x", "3x", '2x', '1x', '2x', '3x', '4x'], fontsize=FONT_TINY)

    rplot.text(0.95, 0.99, 'Cyclone DDS wins' if reverse_win else 'Cyclone DDS + iceoryx wins',
        verticalalignment='top', horizontalalignment='right',
        transform=rplot.transAxes,
        color=COL_CYCLONE, fontsize=FONT_TINY)
    rplot.text(0.99, 0.95, 'Cyclone DDS + iceoryx wins' if reverse_win else 'Cyclone DDS wins',
        verticalalignment='top', horizontalalignment='right',
        rotation=-90,
        transform=rplot.transAxes,
        color=COL_FAST_TEXT, fontsize=FONT_TINY)


    host_title = f" on {filter_host}" if filter_host is not None else ""
    rate_title = "" if not filter_rate_limited and not filter_rate_unlimited else (
        " with limited rate" if filter_rate_limited else " with unlimited rate"
    )
    fig.suptitle(f"{title}{host_title} for {dataset['N']} tests{rate_title}", fontsize=FONT_HUGE)

    pre_f = filter_host or "combined"

    fig.savefig(f"plots/{pre_f}_{variable_name}_zerocopy.png")



def data_select_raw(database, variable_name, filter_host=None, filter_rate_limited=False, filter_rate_unlimited=False):
    tests = database["processed"]
    n_tests = 0
    n_win = 0
    n_lost = 0
    n_both = 0

    cyclone_values, raw_values, ratios, point_type = [], [], [], []
    cyclone_fail_raw_values, cyclone_fail_point_type = [], []
    raw_fail_cyclone_values, raw_fail_point_type = [], []

    for test in tests:
        if filter_host is not None and test['host'] != filter_host:
            continue

        if filter_rate_limited and test['rate'] == 0:
            continue

        if filter_rate_unlimited and test['rate'] != 0:
            continue

        cyclone = test["cyclonedds"]
        raw = test["raw"]
        comparison = make_comparison(cyclone, raw)

        n_tests += 1

        if comparison[variable_name] == Status.CYCLONEDDS_WIN.value:
            ratios.append(comparison[variable_name + "_diff"] - 1)
            cyclone_values.append(cyclone[variable_name])
            raw_values.append(raw[variable_name])
            point_type.append((test['host'], test['topic']))
            n_both += 1
            n_win += 1
        elif comparison[variable_name] == Status.FASTRTPS_WIN.value:
            ratios.append(-comparison[variable_name + "_diff"] + 1)
            cyclone_values.append(cyclone[variable_name])
            raw_values.append(raw[variable_name])
            point_type.append((test['host'], test['topic']))
            n_both += 1
            n_lost += 1
        elif comparison[variable_name] == Status.FASTRTPS_FAIL.value:
            raw_fail_cyclone_values.append(cyclone[variable_name])
            raw_fail_point_type.append((test['host'], test['topic']))
            n_win += 1
        elif comparison[variable_name] == Status.CYCLONEDDS_FAIL.value:
            cyclone_fail_raw_values.append(raw[variable_name])
            cyclone_fail_point_type.append((test['host'], test['topic']))
            n_lost += 1

    return {
        'N': n_tests,
        'Nwin': n_win,
        'Nlost': n_lost,
        'Nboth': n_both,
        'cyclone_values': cyclone_values,
        'raw_values': raw_values,
        'ratios': ratios,
        'point_type': point_type,
        'cyclone_fail_raw_values': cyclone_fail_raw_values,
        'cyclone_fail_point_type': cyclone_fail_point_type,
        'raw_fail_cyclone_values': raw_fail_cyclone_values,
        'raw_fail_point_type': raw_fail_point_type
    }


def do_raw_plot(database, variable_name, filter_host=None, filter_rate_limited=False, filter_rate_unlimited=False):
    COL_RCLCPP = "#1B2A49"
    # Label plot by host if we do not filter to single host
    label_index = 0 if filter_host is None else 1
    label_colours = host_colours if filter_host is None else topic_colours

    dataset = data_select_raw(database, variable_name, filter_host, filter_rate_limited, filter_rate_unlimited)
    title, axlabel, ylog, reverse_win = titles_labels_ylog_reverse[variable_name]

    fig = plt.figure(figsize=(20, 8), constrained_layout=True)
    gs = GridSpec(8, 20, figure=fig)
    lhist = plt.subplot(gs.new_subplotspec((0, 0), colspan=12, rowspan=8))
    rplot = plt.subplot(gs.new_subplotspec((1, 12), colspan=7, rowspan=7))
    topb = plt.subplot(gs.new_subplotspec((0, 12), colspan=7, rowspan=1))
    rightb = plt.subplot(gs.new_subplotspec((1, 19), colspan=1, rowspan=7))

    if ylog:
        if dataset['Nboth'] > 0:
            rplot.set_yscale('log')
            rplot.set_xscale('log')

        if len(dataset['cyclone_fail_raw_values']):
            rightb.set_yscale('log')

        if len(dataset['raw_fail_cyclone_values']):
            topb.set_xscale('log')

    toplot = DefaultDict(list)

    for i in range(dataset['Nboth']):
        toplot[dataset['point_type'][i][label_index]].append((
            dataset['cyclone_values'][i],
            dataset['raw_values'][i]
        ))

    for label, data in toplot.items():
        amount = len(data) + \
                 len([d[label_index] == label for d in dataset['raw_fail_point_type']]) + \
                 len([d[label_index] == label for d in dataset['cyclone_fail_point_type']])

        rplot.scatter([d[1] for d in data], [d[0] for d in data], label=f"{label} ({amount})",
                      c=label_colours.get(label), s=65, edgecolor='black', linewidth=1)

    topb.scatter(
        dataset['raw_fail_cyclone_values'],
        [0.0] * len(dataset['raw_fail_cyclone_values']),
        c=[label_colours.get(k[label_index]) or 'black'
           for k in dataset['raw_fail_point_type']],
        s=65, edgecolor='black', linewidth=1
    )
    rightb.scatter(
        [0.0] * len(dataset['cyclone_fail_raw_values']),
        dataset['cyclone_fail_raw_values'],
        facecolor=[label_colours.get(k[label_index]) or 'black'
           for k in dataset['cyclone_fail_point_type']],
        s=65, edgecolor='black', linewidth=1
    )

    hdata = np.array(dataset['ratios']).clip(-3, 3)
    lhist.hist(hdata, range=(-3, 0), bins=12, histtype='step', linewidth=2, facecolor=COL_CYCLONE, fill=True, edgecolor='black',
        label=f"Cyclone DDS Direct wins {dataset['Nlost']} tests")
    lhist.hist([-3.26] * len(dataset['cyclone_fail_raw_values']), range=(-3.5,-3.25), bins=1, histtype='step',
               linewidth=2, facecolor=COL_CYCLONE, fill=True, edgecolor='black', hatch='///',
               label=f"RCLPP Cyclone DDS failed {len(dataset['cyclone_fail_raw_values'])} tests")
    lhist.hist(hdata, range=(0, 3), bins=12, histtype='step', linewidth=2, facecolor=COL_RCLCPP, fill=True, edgecolor='black',
        label=f"RCLPP Cyclone DDS wins {dataset['Nwin']} tests")
    lhist.hist([3.26] * len(dataset['raw_fail_cyclone_values']), range=(3.25,3.5), bins=1, histtype='step',
               linewidth=2, facecolor=COL_RCLCPP, fill=True, edgecolor='black', hatch='///',
               label=f"Cyclone DDS Direct fails {len(dataset['raw_fail_cyclone_values'])} tests")

    ylims = lhist.get_ylim()
    lhist.set_ylim(0, ylims[1] * 1.2)

    l = lhist.legend(frameon=False, loc=2, fontsize=FONT_SMALL)
    l.get_texts()[0].set_color(COL_CYCLONE)
    l.get_texts()[1].set_color(COL_CYCLONE)
    l.get_texts()[2].set_color(COL_RCLCPP)
    l.get_texts()[3].set_color(COL_RCLCPP)

    l = rplot.set_ylabel(f"Cyclone DDS {axlabel}", fontsize=FONT_SMALL)
    l.set_color(COL_RCLCPP)
    l = rplot.set_xlabel(f"Cyclone DDS + iceoryx {axlabel}", fontsize=FONT_SMALL)
    l.set_color(COL_CYCLONE)

    minl = min(rplot.get_xlim()[0], rplot.get_ylim()[0])
    maxl = max(rplot.get_xlim()[1], rplot.get_ylim()[1])
    maxl += 0.2 * (maxl - minl)

    rplot.plot([minl, maxl], [minl, maxl], 'k-')
    rplot.set_xlim(minl, maxl)
    rplot.set_ylim(minl, maxl)
    topb.set_xlim(minl, maxl)
    rightb.set_ylim(minl, maxl)

    rplot.legend(frameon=False, fontsize=FONT_SMALL)
    rplot.spines['right'].set_visible(False)
    rplot.spines['top'].set_visible(False)
    lhist.spines['right'].set_visible(False)
    lhist.spines['top'].set_visible(False)
    topb.spines['right'].set_visible(False)
    topb.spines['top'].set_visible(False)
    topb.spines['bottom'].set_visible(False)
    rightb.spines['right'].set_visible(False)
    rightb.spines['top'].set_visible(False)
    rightb.spines['left'].set_visible(False)

    rightb.tick_params(axis='y', which='both', left=False, right=False, labelleft=False)
    topb.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    rplot.tick_params(axis='both', which='major', labelsize=FONT_TINY)

    rightb.set_xticks([0])
    rightb.set_xticklabels([f"RCLCPP Cyclone\nfailed {len(dataset['cyclone_fail_raw_values'])}"], color=COL_FAST, fontsize=FONT_TINY)
    topb.set_yticks([0])
    topb.set_yticklabels([f"Direct Cyclone DDS\nfailed {len(dataset['raw_fail_cyclone_values'])}"], color=COL_FAST, fontsize=FONT_TINY)

    lhist.set_xlabel("    ← Direct Cyclone DDS advantage", loc="left", fontsize=FONT_SMALL, color=COL_CYCLONE)
    lhist.set_ylabel("#tests", fontsize=FONT_SMALL)
    lhist.set_xticks([-3, -2, -1, 0, 1, 2, 3])
    lhist.set_xticklabels(["4x", "3x", '2x', '1x', '2x', '3x', '4x'], fontsize=FONT_TINY)

    rplot.text(0.95, 0.99, f'Direct Cyclone DDS wins',
        verticalalignment='top', horizontalalignment='right',
        transform=rplot.transAxes,
        color=COL_CYCLONE, fontsize=FONT_TINY)
    rplot.text(0.99, 0.95, f'RCLCPP Cyclone DDS wins',
        verticalalignment='top', horizontalalignment='right',
        rotation=-90,
        transform=rplot.transAxes,
        color=COL_FAST, fontsize=FONT_TINY)

    host_title = f" on {filter_host}" if filter_host is not None else ""
    rate_title = "" if not filter_rate_limited and not filter_rate_unlimited else (
        " with limited rate" if filter_rate_limited else " with unlimited rate"
    )
    fig.suptitle(f"{title}{host_title} for {dataset['N']} tests{rate_title}", fontsize=FONT_HUGE)

    pre_f = filter_host or "combined"

    fig.savefig(f"plots/{pre_f}_{variable_name}_raw.png")



def histcat_select(database, variable_name, constraints):
    tests = database["processed"]
    vars = ['host', 'mode', 'topic', 'rate', 'subs', 'zero_copy', 'reliable', 'transient']

    for constraint_name, constraint_value in constraints.items():
        vars.remove(constraint_name)

    data = {}

    for test in tests:
        use = True
        for constraint_name, constraint_value in constraints.items():
            if test[constraint_name] != constraint_value:
                use = False
                break

        if not use:
            continue

        cyclone = test["cyclonedds"]
        fast = test["fastrtps"]
        comparison = test["comparison"]

        subdata = data
        for var in vars:
            if test[var] not in subdata:
                subdata[test[var]] = {}
            subdata = subdata[test[var]]

        if 'cyclonedds' not in subdata:
            subdata['cyclonedds'] = None
        if 'fastrtps' not in subdata:
            subdata['fastrtps'] = None

        if comparison[variable_name] in [Status.CYCLONEDDS_WIN.value, Status.FASTRTPS_WIN.value]:
            subdata['cyclonedds'] = cyclone[variable_name]
            subdata['fastrtps'] = fast[variable_name]

        elif comparison[variable_name] == Status.FASTRTPS_FAIL.value:
            subdata['cyclonedds'] = cyclone[variable_name]

        elif comparison[variable_name] == Status.CYCLONEDDS_FAIL.value:
            subdata['fastrtps'] = fast[variable_name]

    return vars, data


def do_histcat_plot(database, variable_name, constraints, ylog, onlycyclone, roundtrip, filename):
    if roundtrip:
        onlycyclone = True

    if 'subs' in constraints:
        constraints['subs'] = int(constraints['subs'])

    if 'rate' in constraints:
        constraints['rate'] = int(constraints['rate'])

    if 'reliable' in constraints:
        constraints['reliable'] = boolify(constraints['reliable'])

    if 'transient' in constraints:
        constraints['transient'] = boolify(constraints['transient'])

    if 'zero_copy' in constraints:
        constraints['zero_copy'] = boolify(constraints['zero_copy'])

    unit = {
        "cpu_usage": ("%", 2),
        "ram_usage": (" MB", 0),
        "latency_mean": ("ms", 1),
        "jitter": ("ms", 0),
        "throughput": ("", 1)
    }[variable_name]

    path, dataset = histcat_select(database, variable_name, constraints)

    fig = plt.figure(figsize=(13, 8), constrained_layout=True)
    gs = GridSpec(8, 13, figure=fig)
    lineplot = plt.subplot(gs.new_subplotspec((0, 0), colspan=10, rowspan=8))
    textplot = plt.subplot(gs.new_subplotspec((0, 10), colspan=3, rowspan=8))
    textplot.set_axis_off()

    textplot.text(0.01, 0.97, "Constraints:",
        verticalalignment='top', horizontalalignment='left',
        transform=textplot.transAxes,
        color='black', fontsize=FONT_SMALL)

    constraints_labels = []
    for key, value in constraints.items():
        if key == 'rate':
            constraints_labels.append(f"rate: {value}Hz")
        elif key == 'subs':
            constraints_labels.append(f"#subscribers: {value}")
        else:
            constraints_labels.append(f"{key}: {value}")

    textplot.text(0.01, 0.91, "\n".join(constraints_labels),
        verticalalignment='top', horizontalalignment='left',
        transform=textplot.transAxes,
        color='black', fontsize=FONT_TINY)

    legend_items = []
    legend_names = []
    coli = 0
    colm = 0

    def count_for(data, key, *vars):
        if vars:
            var = vars[0]
            for name, subdata in data.items():
                count_for(subdata, f"{key} {var}:{name}", *vars[1:])
        else:
            nonlocal colm
            colm += 1

    count_for(dataset, "", *path)
    cmap = get_cmap(colm, 'YlGnBu')
    ticks = []

    def plot_for(data, key, *vars):
        nonlocal unit
        if vars:
            var = vars[0]
            datap = True
            for name, subdata in data.items():
                addhz = "Hz" if var == 'rate' else ""
                if datap:
                    plot_for(subdata, f"{var}:{name}{addhz}\n{key}", *vars[1:])
                    datap = False
                else:
                    plot_for(subdata, f"{var}:{name}{addhz}", *vars[1:])
        else:
            nonlocal coli
            c = cmap(coli)

            if not onlycyclone:
                if data["cyclonedds"] is not None:

                    if variable_name in ["jitter"] and not roundtrip:
                        # blame Joe for this ugly hack!
                        data["cyclonedds"] *= 1000
                        unit = ("µs", 1)

                    lineplot.hist([coli-0.20], weights=[data["cyclonedds"]],
                        range=(coli-0.35, coli-0.05), bins=1,
                        histtype='step', linewidth=2, facecolor=COL_CYCLONE, fill=True, edgecolor='black',
                    )
                    if unit[1] > 0:
                        c = round(data['cyclonedds'], unit[1])
                    else:
                        c = int(round(data['cyclonedds'], unit[1]))
                    lineplot.text(coli - 0.20, data["cyclonedds"], f"{c}{unit[0]}",
                        verticalalignment='bottom', horizontalalignment='center',
                        color=COL_CYCLONE, fontsize=FONT_TINY * 1.3)
                else:
                    lineplot.text(coli - 0.20, data["fastrtps"] / 10, "FAIL",
                        verticalalignment='bottom', horizontalalignment='center',
                        color='black', fontsize=FONT_SMALL * 1.3)
                if data["fastrtps"] is not None:
                    if variable_name in ["jitter"] and not roundtrip:
                        # blame joe for this ugly hack!
                        data["fastrtps"] *= 1000
                        unit = ("µs", 1)

                    lineplot.hist([coli+0.25], weights=[data["fastrtps"]],
                        range=(coli+0.05, coli+0.35), bins=1,
                        histtype='step', linewidth=2, facecolor=COL_FAST, fill=True, edgecolor='black',
                        label="other"
                    )
                    if unit[1] > 0:
                        c = round(data['fastrtps'], unit[1])
                    else:
                        c = int(round(data['fastrtps'], unit[1]))
                    lineplot.text(coli + 0.20, data["fastrtps"], f"{c}{unit[0]}",
                        verticalalignment='bottom', horizontalalignment='center',
                        color=COL_FAST, fontsize=FONT_TINY * 1.3)
                else:
                    lineplot.text(coli + 0.20, data["cyclonedds"] / 10, "FAIL",
                        verticalalignment='bottom', horizontalalignment='center',
                        color='black', fontsize=FONT_SMALL*1.3)
            else:
                if data["cyclonedds"] is not None:
                    if variable_name in ["jitter", "latency_mean"] and not roundtrip:
                        # blame joe for this ugly hack!
                        data["cyclonedds"] *= 1000
                        unit = ("µs", 1 if variable_name == "jitter" else 0)

                    lineplot.hist([coli], weights=[data["cyclonedds"]],
                        range=(coli-0.4, coli+0.4), bins=1,
                        histtype='step', linewidth=2, facecolor=COL_ICEORYX, fill=True, edgecolor='black',
                    )
                    if unit[1] > 0:
                        c = round(data['cyclonedds'], unit[1])
                    else:
                        c = int(round(data['cyclonedds'], unit[1]))
                    lineplot.text(coli, data["cyclonedds"], f"{c}{unit[0]}",
                        verticalalignment='bottom', horizontalalignment='center',
                        color='black', fontsize=FONT_TINY * 1.3)
                else:
                    lineplot.text(coli, 0.01 if ylog else 0, "FAIL",
                        verticalalignment='bottom', horizontalalignment='center',
                        color='black', fontsize=FONT_SMALL*1.3)

            coli += 1
            ticks.append(key)

    plot_for(dataset, "", *path)

    if ylog:
        lineplot.set_yscale('log')

    ylims = lineplot.get_ylim()
    lineplot.set_ylim(ylims[0], ylims[1] * 1.2)
    lineplot.set_xlim(-0.5, len(ticks)-0.5)

    lineplot.tick_params(axis='both', which='major', labelsize=FONT_TINY)

    if not onlycyclone:
        legend_items = [
            Patch(linewidth=2, facecolor=COL_CYCLONE, edgecolor='black', label='Cyclone DDS'),
            Patch(linewidth=2, facecolor=COL_FAST, edgecolor='black', label='other')
        ]

        l = lineplot.legend(handles=legend_items, frameon=False, fontsize=FONT_SMALL)
        l.get_texts()[0].set_color(COL_CYCLONE)
        l.get_texts()[1].set_color(COL_FAST_TEXT)

    lineplot.set_xticks(list(range(len(ticks))))
    lineplot.set_xticklabels(ticks, fontsize=FONT_TINY)

    if variable_name == "jitter" and not roundtrip:
        lineplot.set_ylabel("jitter ($\mu s$)", fontsize=FONT_SMALL)
    elif variable_name == "latency_mean" and onlycyclone:
        if roundtrip:
            lineplot.set_ylabel("mean roundtrip ($ms$)", fontsize=FONT_SMALL)
        else:
            lineplot.set_ylabel("mean latency ($\mu s$)", fontsize=FONT_SMALL)
    else:
        lineplot.set_ylabel(titles_labels_ylog_reverse[variable_name][1], fontsize=FONT_SMALL)

    if roundtrip:
        if variable_name == "latency_mean":
            fig.suptitle(f"Cyclone DDS interhost roundtrip", fontsize=FONT_HUGE)
        else:
            fig.suptitle(f"Cyclone DDS interhost {titles_labels_ylog_reverse[variable_name][0]}", fontsize=FONT_HUGE)
    elif onlycyclone:
        fig.suptitle(f"Cyclone DDS + iceoryx {titles_labels_ylog_reverse[variable_name][0]}", fontsize=FONT_HUGE)
    else:
        fig.suptitle(f"{titles_labels_ylog_reverse[variable_name][0]}", fontsize=FONT_HUGE)

    fig.savefig(filename or f'plots/cathist_{variable_name}.png')
