import os
import numpy as np
from dotenv import load_dotenv
from matplotlib import pyplot as plt

load_dotenv()
# gets the output directory to put the graphs in from the .env file
graphs_directory = os.getenv('OUTPUT_DIRECTORY')


def make_strategy_graph(strategy_statistics, check_complete, strategies_to_skip):
    """
    This function generates a strategy comparison graph
    :param strategy_statistics: the statistics for each strategy included in the graph
    :param check_complete: whether the graph is created for CWA or OWA
    :param strategies_to_skip: the strategies that needed to be skipped in the reading
    """
    ax = make_graph_skeleton(strategy_statistics, check_complete, check_combined=False)

    # deleting the strategies skipped from the graph
    for strategy in strategies_to_skip:
        del STRATEGIES[STRATEGIES.index(strategy)]
    ax.set_xticklabels(STRATEGIES)
    ax.legend()

    if check_complete:
        plot_name = 'CWA_strategy_comparison_graph.png'
    else:
        plot_name = 'OWA_strategy_comparison_graph.png'
    plt.savefig(os.path.join(graphs_directory, plot_name))

    plt.show()


def make_combined_strategy_graph(strategy_statistics, check_complete, strategies_to_skip):
    """
    This function generates a strategy combination graph
    :param strategy_statistics: the statistics for each strategy included in the graph
    :param check_complete: whether the graph is created for CWA or OWA
    :param strategies_to_skip: the strategies that needed to be skipped in the reading
    """
    ax = make_graph_skeleton(strategy_statistics, check_complete, check_combined=True)

    # deleting the strategies skipped from the graph
    for strategy in strategies_to_skip:
        del COMBINED_STRATEGIES[COMBINED_STRATEGIES.index(strategy)]
    ax.set_xticklabels(COMBINED_STRATEGIES, rotation=45, fontsize=10)
    ax.legend()

    if check_complete:
        plot_name = 'CWA_combined_strategy_comparison_graph.png'
    else:
        plot_name = 'OWA_combined_strategy_comparison_graph.png'
    plt.savefig(os.path.join(graphs_directory, plot_name))

    plt.show()


def make_graph_skeleton(strategy_statistics, check_complete, check_combined):
    """
    This function generates the skeleton of a graph
    :param strategy_statistics: the statistics for each strategy included in the graph
    :param check_complete: whether the graph is created for CWA or OWA
    :param check_combined: whether the created skeleton is for a strategy comparison or combination graph
    :return: the elements of the subplot of the graph
    """

    strategy_names = []

    # creating lists of the values for all the strategies
    strategy_diff_pk = []
    strategy_diff_tk = []
    strategy_classif_diff = []
    for strategy in strategy_statistics.keys():
        strategy_names.append(strategy)
        strategy_diff_pk.append(strategy_statistics[strategy][0])
        strategy_diff_tk.append(strategy_statistics[strategy][1])
        strategy_classif_diff.append(strategy_statistics[strategy][2])
    x = np.arange(len(strategy_statistics.keys()))
    width = 0.35

    # the combination graph has different figure size
    if check_combined:
        fig, ax = plt.subplots(figsize=(10, 10))
    else:
        fig, ax = plt.subplots()

    # plotting the values for all the strategies
    bars1 = ax.bar(x - width / 2, strategy_diff_pk, width, bottom=strategy_diff_tk, label='diff_pk')
    bars2 = ax.bar(x - width / 2, strategy_diff_tk, width, label='diff_tk')
    bars3 = ax.bar(x + width / 2, strategy_classif_diff, width, label='classif_diff')

    ax.set_xlabel('Execution of the Element as Initial Seeding')
    ax.set_ylabel('Mean of Information Gained Percentage')
    if check_complete:
        title = 'CWA Mean of Percentage Information Gained Comparison\nof Different Strategies'
    else:
        title = 'OWA Mean of Percentage Information Gained Comparison\nof Different Strategies'
    ax.set_title(title)
    generate_value_text(ax, bars1, bars2, bars3)

    ax.set_ylim(0, 100)
    ax.set_xticks(x)

    return ax


def generate_value_text(ax, bars1, bars2, bars3):
    """
    This function generates the value of each bar on top of the bar itself
    :param ax: the elements of the subplot of the graph
    :param bars1: the list of bars for partially known classes
    :param bars2: the list of bars for totally known classes
    :param bars3: the list of bars for classifications known
    :return:
    """
    for bar in bars3:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height, f'{round(height)}', ha='center', va='bottom', rotation=90)

    for i in range(0, len(bars1)):
        bar1 = bars1[i]
        bar2 = bars2[i]
        height1 = bar1.get_height()
        height2 = bar2.get_height()
        ax.text(bar1.get_x() + bar1.get_width() / 2, height1 + height2, f'{round(height2)}' + '+' + f'{round(height1)}',
                ha='center',
                va='bottom', rotation=90)


"""
Holds the shorthand notation for the strategies
"""
STRATEGIES = [
    'R',
    'L',
    'I',
    'S',
    'NS',
    'RG',
    'ARG',
    'SRG'
]

"""
Holds the shorthand notation for the combined strategies
"""
COMBINED_STRATEGIES = [
    'R_S_RG',
    'R_S_ARG',
    'R_S_SRG',
    'R_NS_RG',
    'R_NS_ARG',
    'R_NS_SRG',
    'L_S_RG',
    'L_S_ARG',
    'L_S_SRG',
    'L_NS_RG',
    'L_NS_ARG',
    'L_NS_SRG',
    'I_S_RG',
    'I_S_ARG',
    'I_S_SRG',
    'I_NS_RG',
    'I_NS_ARG',
    'I_NS_SRG'
]
