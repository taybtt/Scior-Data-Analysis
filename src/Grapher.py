import os

import numpy as np
from matplotlib import pyplot as plt

plots_directory = r"C:\Users\ttuga\Desktop\Research_Project\Software\sciorDataAnalysis\plots"
graphs_directory = r"C:\Users\ttuga\Desktop\Research_Project\Software\sciorDataAnalysis\graphs"


def make_strategy_graph(strategy_statistics, sub_super_strategy, min_max_strategy):
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
        # print(strategy_statistics)
    x = np.arange(len(strategy_statistics.keys()))
    width = 0.35

    fig, ax = plt.subplots()
    bars1 = ax.bar(x - width / 2, strategy_diff_pk, width, bottom=strategy_diff_tk, label='diff_pk')
    bars2 = ax.bar(x - width / 2, strategy_diff_tk, width, label='diff_tk')
    bars3 = ax.bar(x + width / 2, strategy_classif_diff, width, label='classif_diff')

    ax.set_xlabel('Execution of the Element as Initial Seeding')
    ax.set_ylabel('Mean of Information Gained Percentage')
    ax.set_title(generate_graph_name(sub_super_strategy, min_max_strategy))

    ax.set_ylim(0, 100)
    ax.set_xticks(x)

    # TODO SHOULD BE STRATEGY NAMES
    # TODO THE LABELS REQUIRE EVERY STRATEGY TO BE PRESENT, NEED TO FIX THE PART
    #  WHERE IF ONE STRATEGY HAS NO ELEMENTS TO USE FOR THE INITIAL SEEDING,
    #  IT SHOULD NOT GIVE AN ERROR BUT FIGURE IT OUT SOMEHOW
    ax.set_xticklabels(['R', 'L', 'I', 'S', 'NS', 'RG', 'ARG', 'SRG'])
    ax.legend()

    plot_name = generate_graph_file_name(sub_super_strategy, min_max_strategy)
    plt.savefig(os.path.join(plots_directory, plot_name))

    plt.show()


def generate_graph_name(sub_super_strategy, min_max_strategy):
    match sub_super_strategy:
        case 'NONE':
            return 'Mean of Percentage Information Gained Comparison of Different Strategies'
        case 'SUPERCLASS':
            if min_max_strategy == 'MAX':
                return 'Mean of Percentage Information Gained Comparison of Different Strategies from Max Superclass Elements'
            else:
                return 'Mean of Percentage Information Gained Comparison of Different Strategies from Min Superclass Elements'
        case 'SUBCLASS':
            if min_max_strategy == 'MAX':
                return 'Mean of Percentage Information Gained Comparison of Different Strategies from Max Subclass Elements'
            else:
                return 'Mean of Percentage Information Gained Comparison of Different Strategies from Min Subclass Elements'


def generate_graph_file_name(sub_super_strategy, min_max_strategy):
    match sub_super_strategy:
        case 'NONE':
            return 'strategy_comparison_graph.png'
        case 'SUPERCLASS':
            if min_max_strategy == 'MAX':
                return 'strategy_comparison_graph_max_superclass.png'
            else:
                return 'strategy_comparison_graph_min_superclass.png'
        case 'SUBCLASS':
            if min_max_strategy == 'MAX':
                return 'strategy_comparison_graph_max_subclass.png'
            else:
                return 'strategy_comparison_graph_min_subclass.png'
