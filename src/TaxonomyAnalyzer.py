import statistics


def analyse_taxonomy(taxonomy_data, taxonomy_statistics, taxonomy_summary, strategy):
    """
    This function oversees the analysis of the taxonomy with the rest of the functions on this file. This function
    analyses a taxonomy for a strategy comparison graph.
    :param taxonomy_data: data of the elements from the taxonomy
    :param taxonomy_statistics: statistics of the elements from the taxonomy
    :param taxonomy_summary: summary of the elements from the taxonomy
    :param strategy: strategy the analysis is performed for
    :return: the means of the taxonomy statistics
    """
    elements = analyse_summary(taxonomy_summary)
    elements_data = analyse_data(taxonomy_data)
    elements_statistics = analyse_statistics(taxonomy_statistics, elements)
    elements, elements_statistics, elements_data = enforce_strategy_on_elements(strategy, elements, elements_statistics,
                                                                                elements_data)
    return taxonomy_mean(elements_statistics)


def analyse_combined_taxonomy(taxonomy_data, taxonomy_statistics, taxonomy_summary, position, sortality, rigidity):
    """
    This function oversees the analysis of the taxonomy with the rest of the functions on this file. This function
    analyses a taxonomy for a strategy combination graph.
    :param taxonomy_data: data of the elements from the taxonomy
    :param taxonomy_statistics: statistics of the elements from the taxonomy
    :param taxonomy_summary: summary of the elements from the taxonomy
    :param position: position strategy the analysis is performed for
    :param sortality: sortality strategy the analysis is performed for
    :param rigidity: rigidity strategy the analysis is performed for
    :return: the means of the taxonomy statistics
    """
    elements = analyse_summary(taxonomy_summary)
    elements_data = analyse_data(taxonomy_data)
    elements_statistics = analyse_statistics(taxonomy_statistics, elements)
    elements, elements_statistics, elements_data = enforce_strategy_on_elements(position, elements, elements_statistics,
                                                                                elements_data)
    elements, elements_statistics, elements_data = enforce_strategy_on_elements(sortality, elements,
                                                                                elements_statistics,
                                                                                elements_data)
    elements, elements_statistics, elements_data = enforce_strategy_on_elements(rigidity, elements, elements_statistics,
                                                                                elements_data)
    return taxonomy_mean(elements_statistics)


def analyse_summary(taxonomy_summary):
    """
    This function analyses the summary of the elements of the taxonomy and creates a dictionary that holds the name of
    each element.
    elements dictionary:
        key: execution number of the element
        value: name of the element executed as the initial seeding
    :param taxonomy_summary: summary of the taxonomy elements
    :return: the elements dictionary of the taxonomy
    """
    elements = dict()
    for i in range(len(taxonomy_summary)):
        elements[taxonomy_summary.loc[i, 'execution_number']] = taxonomy_summary.loc[i, 'input_class_name']
    return elements


def analyse_data(taxonomy_data):
    """
    This function analyses the data of the taxonomy elements and creates a dictionary that holds a dictionary of
    data.
    elements_data dictionary:
        key: element
        value: element_data dictionary
            key: data name
            value: data value
    :param taxonomy_data: data of the taxonomy elements.
    :return: returns the nested dictionary structure of elements_data dictionary
    """
    elements_data = dict()
    for i in range(0, len(taxonomy_data)):
        # add all the necessary information about an element to the dictionary with the element name as the key
        element_data = dict()

        # adding each field of importance from the table to a dictionary
        element_data['gufo_classification'] = taxonomy_data.loc[i, 'gufo_classification']
        element_data['is_root'] = taxonomy_data.loc[i, 'is_root']
        element_data['is_leaf'] = taxonomy_data.loc[i, 'is_leaf']
        element_data['is_intermediate'] = taxonomy_data.loc[i, 'is_intermediate']
        element_data['number_superclasses'] = taxonomy_data.loc[i, 'number_superclasses']
        element_data['number_subclasses'] = taxonomy_data.loc[i, 'number_subclasses']

        # adding the element dictionary into a dictionary of elements_data
        elements_data[taxonomy_data.loc[i, 'class_name']] = element_data
    return elements_data


def analyse_statistics(taxonomy_statistics, elements):
    """
    This function analyses the statistics of the taxonomy elements and creates a dictionary that holds a dictionary of
    statistics.
    element_statistics dictionary:
        key: element
        value: stats dictionary
            key: statistics name
            value: statistics value
    :param taxonomy_statistics: statistics of the taxonomy elements.
    :param elements: elements of the taxonomy
    :return: returns the nested dictionary structure elements_statistics dictionary
    """
    elements_statistics = dict()
    i = 0
    for key in elements.keys():
        stats = dict()
        stats['diff_pk_classes_types_p'] = taxonomy_statistics.loc[i, 'diff_pk_classes_types_p']
        stats['diff_tk_classes_types_p'] = taxonomy_statistics.loc[i, 'diff_tk_classes_types_p']
        stats['diff_known_classif_types_p'] = taxonomy_statistics.loc[i, 'diff_known_classif_types_p']
        elements_statistics[elements[key]] = stats
        i = i + 1
    return elements_statistics


def enforce_strategy_on_elements(strategy, elements, elements_statistics, elements_data):
    """
    This function enforces the given strategy to the information about the elements of the taxonomy.
    This enforcing is done by removing all the elements that do not belong to the given strategy along with the information that belongs to them.
    :param strategy: strategy to enforce on the taxonomy elements.
    :param elements: elements of the taxonomy
    :param elements_statistics: statistics of the elements of the taxonomy
    :param elements_data: data of the elements of the taxonomy
    :return: the elements, the element statistics, and the element data after the enforcement of the strategy
    """
    match strategy:
        case "ROOT":
            elements_to_be_removed = []
            executions_to_be_removed = []
            for execution in elements.keys():
                if not elements_data[elements[execution]]['is_root']:
                    executions_to_be_removed.append(execution)
                    elements_to_be_removed.append(elements[execution])
            for element in elements_to_be_removed:
                del elements_statistics[element]
                del elements_data[element]
            for execution in executions_to_be_removed:
                del elements[execution]
        case "LEAF":
            elements_to_be_removed = []
            executions_to_be_removed = []
            for execution in elements.keys():
                if not elements_data[elements[execution]]['is_leaf']:
                    executions_to_be_removed.append(execution)
                    elements_to_be_removed.append(elements[execution])
            for element in elements_to_be_removed:
                del elements_statistics[element]
                del elements_data[element]
            for execution in executions_to_be_removed:
                del elements[execution]
        case 'INTERMEDIATE':
            elements_to_be_removed = []
            executions_to_be_removed = []
            for execution in elements.keys():
                if not elements_data[elements[execution]]['is_intermediate']:
                    executions_to_be_removed.append(execution)
                    elements_to_be_removed.append(elements[execution])
            for element in elements_to_be_removed:
                del elements_statistics[element]
                del elements_data[element]
            for execution in executions_to_be_removed:
                del elements[execution]
        case "SORTAL":
            elements_to_be_removed = []
            executions_to_be_removed = []
            for execution in elements.keys():
                gufo_class = elements_data[elements[execution]]['gufo_classification']
                if not (gufo_class == 'kind' or gufo_class == 'subkind' or gufo_class == 'phase' or
                        gufo_class == 'role'):
                    executions_to_be_removed.append(execution)
                    elements_to_be_removed.append(elements[execution])
            for element in elements_to_be_removed:
                del elements_statistics[element]
                del elements_data[element]
            for execution in executions_to_be_removed:
                del elements[execution]
        case "NON_SORTAL":
            elements_to_be_removed = []
            executions_to_be_removed = []
            for execution in elements.keys():
                gufo_class = elements_data[elements[execution]]['gufo_classification']
                if gufo_class == 'kind' or gufo_class == 'subkind' or gufo_class == 'phase' or gufo_class == 'role':
                    executions_to_be_removed.append(execution)
                    elements_to_be_removed.append(elements[execution])
            for element in elements_to_be_removed:
                del elements_statistics[element]
                del elements_data[element]
            for execution in executions_to_be_removed:
                del elements[execution]
        case "RIGID":
            elements_to_be_removed = []
            executions_to_be_removed = []
            for execution in elements.keys():
                gufo_class = elements_data[elements[execution]]['gufo_classification']
                if not (gufo_class == 'kind' or gufo_class == 'subkind' or gufo_class == 'category'):
                    executions_to_be_removed.append(execution)
                    elements_to_be_removed.append(elements[execution])
            for element in elements_to_be_removed:
                del elements_statistics[element]
                del elements_data[element]
            for execution in executions_to_be_removed:
                del elements[execution]
        case "ANTI_RIGID":
            elements_to_be_removed = []
            executions_to_be_removed = []
            for execution in elements.keys():
                gufo_class = elements_data[elements[execution]]['gufo_classification']
                if not (gufo_class == 'phase' or gufo_class == 'role' or gufo_class == 'phasemixin' or
                        gufo_class == 'rolemixin'):
                    executions_to_be_removed.append(execution)
                    elements_to_be_removed.append(elements[execution])
            for element in elements_to_be_removed:
                del elements_statistics[element]
                del elements_data[element]
            for execution in executions_to_be_removed:
                del elements[execution]
        case "SEMI-RIGID":
            elements_to_be_removed = []
            executions_to_be_removed = []
            for execution in elements.keys():
                gufo_class = elements_data[elements[execution]]['gufo_classification']
                if not (gufo_class == 'mixin'):
                    executions_to_be_removed.append(execution)
                    elements_to_be_removed.append(elements[execution])
            for element in elements_to_be_removed:
                del elements_statistics[element]
                del elements_data[element]
            for execution in executions_to_be_removed:
                del elements[execution]
        case _:
            return elements, elements_statistics, elements_data

    return elements, elements_statistics, elements_data


def taxonomy_mean(elements_statistics):
    """
    This function calculates the mean of the statistics of the taxonomy
    :param elements_statistics: the statistics of the taxonomy
    :return: the means for the statistics of partially known classes, totally known classes, and classifications known
    """
    taxonomy_diff_pk = []
    taxonomy_diff_tk = []
    taxonomy_classif_diff = []
    for element in elements_statistics:
        taxonomy_diff_pk.append(elements_statistics[element]['diff_pk_classes_types_p'])
        taxonomy_diff_tk.append(elements_statistics[element]['diff_tk_classes_types_p'])
        taxonomy_classif_diff.append(elements_statistics[element]['diff_known_classif_types_p'])

    return statistics.mean(taxonomy_diff_pk), statistics.mean(taxonomy_diff_tk), statistics.mean(taxonomy_classif_diff)
