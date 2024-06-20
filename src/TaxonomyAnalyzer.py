import os
import matplotlib.pyplot as plt
import numpy as np
from TaxonomyStatistics import taxonomy_mean

plots_directory = r"C:\Users\ttuga\Desktop\Research_Project\Software\sciorDataAnalysis\plots"


def analyse_taxonomy(model_data, model_statistics, taxonomy_name, strategy):
    # the first part is the row, the second part is the column
    # print(model_data.loc[0, 'class_name'])

    # the classes within the taxonomy with their extracted class information
    elements = analyse_data(model_data)
    elements_statistics = analyse_statistics(model_statistics, elements)
    elements, elements_statistics = enforce_strategy_on_elements(strategy, elements, elements_statistics)
    # print(elements)
    # print(elements_statistics)



    # make_class_graph(elements_statistics, taxonomy_name)

    # make_classification_graph(elements_statistics, taxonomy_name)

    # make_graph(elements_statistics, taxonomy_name)
    return taxonomy_mean(elements, elements_statistics)


def analyse_data(model_data):
    elements = dict()
    for i in range(0, len(model_data)):
        # add all the necessary information about an element to the dictionary with the element name as the key
        element_data = dict()

        # adding each field of importance from the table to a dictionary
        element_data['gufo_classification'] = model_data.loc[i, 'gufo_classification']
        element_data['is_root'] = model_data.loc[i, 'is_root']
        element_data['is_leaf'] = model_data.loc[i, 'is_leaf']
        element_data['number_superclasses'] = model_data.loc[i, 'number_superclasses']
        element_data['number_subclasses'] = model_data.loc[i, 'number_subclasses']

        # adding the element dictionary into a dictionary of elements
        elements[model_data.loc[i, 'class_name']] = element_data
    return elements


def enforce_strategy_on_elements(strategy, elements, elements_statistics):
    # TODO IF YOU HAVE THE TIME, ADD THE HIGHEST/LOWEST SUPERCLASS/SUBCLASS COUNTS INTO THE MIX
    # removes the elements that do not belong to the strategy of the run
    match strategy:
        case "ROOT":
            elements_to_be_removed = []
            for element in elements.keys():
                if not elements[element]['is_root']:
                    elements_to_be_removed.append(element)
            for element in elements_to_be_removed:
                del elements[element]
                del elements_statistics[element]
        case "LEAF":
            elements_to_be_removed = []
            for element in elements.keys():
                if not elements[element]['is_leaf']:
                    elements_to_be_removed.append(element)
            for element in elements_to_be_removed:
                del elements[element]
                del elements_statistics[element]
        case "SORTAL":
            elements_to_be_removed = []
            for element in elements.keys():
                gufo_class = elements[element]['gufo_classification']
                if not (gufo_class == 'kind' or gufo_class == 'subkind' or gufo_class == 'phase' or
                        gufo_class == 'role'):
                    elements_to_be_removed.append(element)
            for element in elements_to_be_removed:
                del elements[element]
                del elements_statistics[element]
        case "NON_SORTAL":
            elements_to_be_removed = []
            for element in elements.keys():
                gufo_class = elements[element]['gufo_classification']
                if gufo_class == 'kind' or gufo_class == 'subkind' or gufo_class == 'phase' or gufo_class == 'role':
                    elements_to_be_removed.append(element)
            for element in elements_to_be_removed:
                del elements[element]
                del elements_statistics[element]
        case "RIGID":
            elements_to_be_removed = []
            for element in elements.keys():
                gufo_class = elements[element]['gufo_classification']
                if not (gufo_class == 'kind' or gufo_class == 'subkind' or gufo_class == 'category'):
                    elements_to_be_removed.append(element)
            for element in elements_to_be_removed:
                del elements[element]
                del elements_statistics[element]
        case "ANTI_RIGID":
            elements_to_be_removed = []
            for element in elements.keys():
                gufo_class = elements[element]['gufo_classification']
                if not (gufo_class == 'phase' or gufo_class == 'role' or gufo_class == 'phasemixin' or
                        gufo_class == 'rolemixin'):
                    elements_to_be_removed.append(element)
            for element in elements_to_be_removed:
                del elements[element]
                del elements_statistics[element]
        case "SEMI-RIGID":
            elements_to_be_removed = []
            for element in elements.keys():
                gufo_class = elements[element]['gufo_classification']
                if not (gufo_class == 'mixin'):
                    elements_to_be_removed.append(element)
            for element in elements_to_be_removed:
                del elements[element]
                del elements_statistics[element]
        case _:
            return elements, elements_statistics

    return elements, elements_statistics


def analyse_statistics(model_statistics, elements):
    elements_statistics = dict()
    # print(elements.keys())
    i = 0
    for key in elements.keys():
        stats = dict()
        stats['diff_pk_classes_types_p'] = model_statistics.loc[i, 'diff_pk_classes_types_p']
        stats['diff_tk_classes_types_p'] = model_statistics.loc[i, 'diff_tk_classes_types_p']
        stats['diff_known_classif_types_p'] = model_statistics.loc[i, 'diff_known_classif_types_p']
        elements_statistics[key] = stats
        # elements_statistics[key] = [model_statistics.loc[i, 'diff_pk_classes_types_p'],
        #                             model_statistics.loc[i, 'diff_tk_classes_types_p'],
        #                             model_statistics.loc[i, 'diff_unknown_classif_types_p']]
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
        diff_pk.append(elements_statistics[element]['diff_pk_classes_types_p'])
        diff_tk.append(elements_statistics[element]['diff_tk_classes_types_p'])

    # print(diff_pk)
    # print(diff_tk)
    x = np.arange(len(element_names))

    fig, ax = plt.subplots()
    bars1 = ax.bar(x, diff_pk, bottom=diff_tk, label='diff_pk')
    bars2 = ax.bar(x, diff_tk, label='diff_tk')

    ax.set_xlabel('Execution of the Element')
    ax.set_ylabel('Class Information Gained')
    ax.set_title('Percentage Class Information Gained Compared from Different Elements')

    ax.set_ylim(0, 100)
    ax.set_xticks(x)
    ax.set_xticklabels(element_names)
    ax.legend()

    plot_name = taxonomy_name + '_class_graph.png'
    plt.savefig(os.path.join(plots_directory, plot_name))

    plt.show()


def make_classification_graph(elements_statistics, taxonomy_name):
    # adding the values into the graph axis
    element_names = []
    classif_diff = []
    for element in elements_statistics.keys():
        element_names.append(element)
        classif_diff.append(elements_statistics[element]['diff_known_classif_types_p'])

    x = np.arange(len(element_names))

    fig, ax = plt.subplots()
    bars = ax.bar(x, classif_diff, label='classif_diff')

    ax.set_xlabel('Execution of the Element')
    ax.set_ylabel('Classification Information Gained')
    ax.set_title('Percentage Classification Information Gained Compared from Different Elements')

    ax.set_ylim(0, 100)
    ax.set_xticks(x)
    ax.set_xticklabels(element_names)
    ax.legend()

    plot_name = taxonomy_name + '_classification_graph.png'
    plt.savefig(os.path.join(plots_directory, plot_name))

    plt.show()


def make_graph(elements_statistics, taxonomy_name):
    # plt.style.use('seaborn-whitegrid')
    # adding the values into the graph axis
    element_names = []
    diff_pk = []
    diff_tk = []
    classif_diff = []
    for element in elements_statistics.keys():
        element_names.append(element)
        diff_pk.append(elements_statistics[element]['diff_pk_classes_types_p'])
        diff_tk.append(elements_statistics[element]['diff_tk_classes_types_p'])
        classif_diff.append(elements_statistics[element]['diff_known_classif_types_p'])

    x = np.arange(len(element_names))

    width = 0.35

    fig, ax = plt.subplots()
    bars1 = ax.bar(x - width / 2, diff_pk, width, bottom=diff_tk, label='diff_pk')
    bars2 = ax.bar(x - width / 2, diff_tk, width, label='diff_tk')
    bars3 = ax.bar(x + width / 2, classif_diff, width, label='classif_diff')

    ax.set_xlabel('Execution of the Element')
    ax.set_ylabel('Information Gained')
    ax.set_title('Percentage Information Gained Compared from Different Elements')

    ax.set_ylim(0, 100)
    ax.set_xticks(x)
    ax.set_xticklabels(element_names)
    ax.legend()

    plot_name = taxonomy_name + '_graph.png'
    plt.savefig(os.path.join(plots_directory, plot_name))

    plt.show()
