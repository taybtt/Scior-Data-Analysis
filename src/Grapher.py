import os

import numpy as np
from matplotlib import pyplot as plt

plots_directory = r"C:\Users\ttuga\Desktop\Research_Project\Software\sciorDataAnalysis\plots"
graphs_directory = r"C:\Users\ttuga\Desktop\Research_Project\Software\sciorDataAnalysis\graphs"


def make_strategy_graph(strategy_statistics, sub_super_strategy, min_max_strategy, check_complete):
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
    ax.set_title(generate_graph_name(sub_super_strategy, min_max_strategy, check_complete))
    generate_value_text(ax, bars1, bars2, bars3)

    ax.set_ylim(0, 100)
    ax.set_xticks(x)

    # TODO SHOULD BE STRATEGY NAMES
    # TODO THE LABELS REQUIRE EVERY STRATEGY TO BE PRESENT, NEED TO FIX THE PART
    #  WHERE IF ONE STRATEGY HAS NO ELEMENTS TO USE FOR THE INITIAL SEEDING,
    #  IT SHOULD NOT GIVE AN ERROR BUT FIGURE IT OUT SOMEHOW
    ax.set_xticklabels(['R', 'L', 'I', 'S', 'NS', 'RG', 'ARG', 'SRG'])
    ax.legend()

    plot_name = generate_graph_file_name(sub_super_strategy, min_max_strategy, check_complete)
    plt.savefig(os.path.join(graphs_directory, plot_name))

    plt.show()


def generate_value_text(ax, bars1, bars2, bars3):
    for bar in bars3:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height, f'{round(height)}', ha='center', va='bottom', rotation=90)

    for i in range(0, len(bars1)):
        bar1 = bars1[i]
        bar2 = bars2[i]
        height1 = bar1.get_height()
        height2 = bar2.get_height()
        ax.text(bar1.get_x() + bar1.get_width()/2, height1+height2, f'{round(height2)}' + '+' + f'{round(height1)}', ha='center',
                va='bottom', rotation=90)


def generate_graph_name(sub_super_strategy, min_max_strategy, check_complete):
    graph_name = ''
    match sub_super_strategy:
        case 'NONE':
            graph_name = 'Mean of Percentage Information Gained Comparison\nof Different Strategies'
        case 'SUPERCLASS':
            if min_max_strategy == 'MAX':
                graph_name = 'Mean of Percentage Information Gained Comparison\nof Different Strategies from Max Superclass Elements'
            else:
                graph_name = 'Mean of Percentage Information Gained Comparison\nof Different Strategies from Min Superclass Elements'
        case 'SUBCLASS':
            if min_max_strategy == 'MAX':
                graph_name = 'Mean of Percentage Information Gained Comparison\nof Different Strategies from Max Subclass Elements'
            else:
                graph_name = 'Mean of Percentage Information Gained Comparison\nof Different Strategies from Min Subclass Elements'
    if check_complete:
        graph_name = 'CWA ' + graph_name
    else:
        graph_name = 'OWA ' + graph_name
    return graph_name


def generate_graph_file_name(sub_super_strategy, min_max_strategy, check_complete):
    file_name = ''
    match sub_super_strategy:
        case 'NONE':
            file_name = 'strategy_comparison_graph.png'
        case 'SUPERCLASS':
            if min_max_strategy == 'MAX':
                file_name = 'strategy_comparison_graph_max_superclass.png'
            else:
                file_name = 'strategy_comparison_graph_min_superclass.png'
        case 'SUBCLASS':
            if min_max_strategy == 'MAX':
                file_name = 'strategy_comparison_graph_max_subclass.png'
            else:
                file_name = 'strategy_comparison_graph_min_subclass.png'
    if check_complete:
        file_name = 'CWA_' + file_name
    else:
        file_name = 'OWA_' + file_name
    return file_name
