import os
import matplotlib.pyplot as plt
import numpy as np

plots_directory = r"C:\Users\ttuga\Desktop\Research_Project\Software\sciorDataAnalysis\plots"


def analyse_taxonomy(model_data, model_statistics, taxonomy_name):
    # the first part is the row, the second part is the column
    # print(model_data.loc[0, 'class_name'])

    # the classes within the taxonomy with their extracted class information
    elements = analyse_data(model_data)
    # print(elements)
    elements_statistics = analyse_statistics(model_statistics, elements)
    # print(elements_statistics)
    make_class_graph(elements_statistics, taxonomy_name)


def analyse_data(model_data):
    elements = dict()
    for i in range(0, len(model_data)):
        # add all the necessary information about an element to the dictionary with the element name as the key
        elements[model_data.loc[i, 'class_name']] = [model_data.loc[i, 'is_root'],
                                                     model_data.loc[i, 'is_leaf'],
                                                     model_data.loc[i, 'number_superclasses'],
                                                     model_data.loc[i, 'number_subclasses']]
    return elements


def analyse_statistics(model_statistics, elements):
    elements_statistics = dict()
    i = 0
    for key in elements.keys():
        elements_statistics[key] = [model_statistics.loc[i, 'diff_pk_classes_types_p'],
                                    model_statistics.loc[i, 'diff_tk_classes_types_p'],
                                    model_statistics.loc[i, 'diff_unknown_classif_types_p']]
        i = i + 1
    return elements_statistics


def make_class_graph(elements_statistics, taxonomy_name):
    # plt.style.use('seaborn-whitegrid')
    # adding the values into the graph axis
    element_names = []
    diff_pk = []
    diff_tk = []
    for element in elements_statistics.keys():
        element_names.append(element)
        diff_pk.append(elements_statistics.get(element)[0])
        diff_tk.append(elements_statistics.get(element)[1])

    # print(diff_pk)
    # print(diff_tk)
    x = np.arange(len(element_names))

    width = 0.35

    fig, ax = plt.subplots()
    bars1 = ax.bar(x - width / 2, diff_pk, width, label='diff_pk')
    bars2 = ax.bar(x + width / 2, diff_tk, width, label='diff_tk')

    ax.set_xlabel('Execution of the Element')
    ax.set_ylabel('Class Information Gains')
    ax.set_title('Information Gains Compared from Different Elements')
    ax.set_xticks(x)
    ax.set_xticklabels(element_names)
    ax.legend()

    plot_name = taxonomy_name + '_class_graph.png'
    plt.savefig(os.path.join(plots_directory, plot_name))

    plt.show()
