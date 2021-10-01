import csv
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

from .plotter import COL_CYCLONE, COL_FAST, FONT_HUGE, titles_labels_ylog_reverse, FONT_TINY, FONT_SMALL
from .resulter import test_results
from .collector import data as data_collector

rmw_labels_cols = {
    'cyclone': ('Cyclone DDS', COL_CYCLONE),
    'fast': ('other', COL_FAST)
}

rmw_names = {
    'cyclone': 'rmw_cyclonedds_cpp',
    'fast': 'rmw_fastrtps_cpp',
}


def do_scale_plot(directory, variable_name, range_min, range_max, range_step, topics, log):
    title, axlabel, ylog , reverse_win = titles_labels_ylog_reverse[variable_name]

    fig = plt.figure(figsize=(12, 8), constrained_layout=True)
    gs = GridSpec(8, 12, figure=fig)
    lhist = plt.subplot(gs.new_subplotspec((0, 0), colspan=12, rowspan=8))

    sets = 'topics' if topics else 'nodes'

    for rmw in ['fast', 'cyclone']:
        result = []
        for i in range(range_min, range_max, range_step):
            data = []
            success = True
            for j in range(i):
                fname = f"sub_node_{j}_{rmw_names[rmw]}_{i}.csv"

                try:
                    with open(os.path.join(directory, fname)) as f:
                        source = list(f.readlines())
                        entry = {}
                        header, values = data_collector(source)
                        for h in header:
                            entry[h] = [row[h] for row in values]
                        node_data = test_results(entry, 'scaling', 1)
                        if not node_data:
                            success = False
                            break
                        else:
                            data.append(node_data[variable_name])
                except:
                    success = False
                    break

            if success:
                result.append((i, np.mean(data), np.std(data)))

        lhist.plot([r[0] for r in result], [r[1] for r in result],
                label=rmw_labels_cols[rmw][0],
                color=rmw_labels_cols[rmw][1],
                linewidth=3
        )
        lhist.errorbar([r[0] for r in result], [r[1] for r in result],
                yerr=[r[2] for r in result],
                color=rmw_labels_cols[rmw][1],
                linewidth=1.5, capsize=2
        )

    fig.suptitle(f"scaling {sets} - {title}", fontsize=FONT_HUGE)

    if log:
        lhist.set_yscale('log')

    legend_properties = {'weight':'bold', 'size': FONT_SMALL}
    handles, labels = lhist.get_legend_handles_labels()
    l = lhist.legend(handles[::-1], labels[::-1], frameon=False, prop=legend_properties)
    l.get_texts()[0].set_color(COL_CYCLONE)
    l.get_texts()[1].set_color(COL_FAST)
    lhist.tick_params(axis='both', which='major', labelsize=FONT_TINY)

    if variable_name == "ram_usage":
        lims = lhist.get_ylim()
        minv = int(lims[0] / 5) * 5
        maxv = int(lims[1] / 5) * 5 + 5
        lhist.set_ylim(minv, maxv)
        lhist.set_yticks(list(range(minv, maxv, 5)))
        lhist.set_yticklabels([str(v) for v in range(minv, maxv, 5)], fontsize=FONT_TINY)
    else:
        lims = lhist.get_ylim()
        lhist.set_ylim(max(lims[0], 0), lims[1])

    lhist.spines['right'].set_visible(False)
    lhist.spines['top'].set_visible(False)

    lhist.set_ylabel(axlabel, fontsize=FONT_SMALL)
    lhist.set_xlabel("number of topics" if topics else "number of nodes", fontsize=FONT_SMALL)
    fig.savefig(f"plots/scaling_{variable_name}_{sets}.png")

