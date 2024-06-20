import os

import numpy as np
from matplotlib import pyplot as plt

plots_directory = r"C:\Users\ttuga\Desktop\Research_Project\Software\sciorDataAnalysis\plots"


def make_strategy_graph(strategy_statistics):
    strategy_names = []
    strategy_diff_pk = []
    strategy_diff_tk = []
    strategy_classif_diff = []
    for strategy in strategy_statistics.keys():
        # TODO MIGHT WANT TO CHANGE STRATEGY TO A DICTIONARY IN A DICTIONARY LIKE THE OTHERS
        strategy_names.append(strategy)
        strategy_diff_pk.append(strategy_statistics[strategy][0])
        strategy_diff_tk.append(strategy_statistics[strategy][1])
        strategy_classif_diff.append(strategy_statistics[strategy][2])
    x = np.arange(len(strategy_statistics.keys()))
    width = 0.35

    fig, ax = plt.subplots()
    bars1 = ax.bar(x - width / 2, strategy_diff_pk, width, bottom=strategy_diff_tk, label='diff_pk')
    bars2 = ax.bar(x - width / 2, strategy_diff_tk, width, label='diff_tk')
    bars3 = ax.bar(x + width / 2, strategy_classif_diff, width, label='classif_diff')

    ax.set_xlabel('Execution of the Element as Initial Seeding')
    ax.set_ylabel('Information Gained Percentage')
    ax.set_title('Percentage Information Gained Comparison of Different Strategies')

    ax.set_ylim(0, 100)
    ax.set_xticks(x)

    # TODO SHOULD BE STRATEGY NAMES
    ax.set_xticklabels(['R', 'L', 'S', 'NS', 'RG', 'ARG', 'SRG'])
    ax.legend()

    plot_name = 'strategy_comparison_graph.png'
    plt.savefig(os.path.join(plots_directory, plot_name))

    plt.show()
