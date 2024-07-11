import statistics


def analyse_taxonomy(model_data, model_statistics, model_summary, strategy):
    # the first part is the row, the second part is the column

    # the classes within the taxonomy with their extracted class information
    elements = analyse_summary(model_summary)
    elements_data = analyse_data(model_data)
    elements_statistics = analyse_statistics(model_statistics, elements)
    elements, elements_statistics, elements_data = enforce_strategy_on_elements(strategy, elements, elements_statistics,
                                                                                elements_data)
    return taxonomy_mean(elements, elements_statistics)


def analyse_combined_taxonomy(model_data, model_statistics, model_summary, position, sortality, rigidity):
    elements = analyse_summary(model_summary)
    elements_data = analyse_data(model_data)
    elements_statistics = analyse_statistics(model_statistics, elements)
    elements, elements_statistics, elements_data = enforce_strategy_on_elements(position, elements, elements_statistics,
                                                                                elements_data)
    elements, elements_statistics, elements_data = enforce_strategy_on_elements(sortality, elements,
                                                                                elements_statistics,
                                                                                elements_data)
    elements, elements_statistics, elements_data = enforce_strategy_on_elements(rigidity, elements, elements_statistics,
                                                                                elements_data)
    return taxonomy_mean(elements, elements_statistics)


def analyse_summary(model_summary):
    elements = dict()
    for i in range(len(model_summary)):
        elements[model_summary.loc[i, 'execution_number']] = model_summary.loc[i, 'input_class_name']
    return elements


def analyse_data(model_data):
    elements_data = dict()
    for i in range(0, len(model_data)):
        # add all the necessary information about an element to the dictionary with the element name as the key
        element_data = dict()

        # adding each field of importance from the table to a dictionary
        element_data['gufo_classification'] = model_data.loc[i, 'gufo_classification']
        element_data['is_root'] = model_data.loc[i, 'is_root']
        element_data['is_leaf'] = model_data.loc[i, 'is_leaf']
        element_data['is_intermediate'] = model_data.loc[i, 'is_intermediate']
        element_data['number_superclasses'] = model_data.loc[i, 'number_superclasses']
        element_data['number_subclasses'] = model_data.loc[i, 'number_subclasses']

        # adding the element dictionary into a dictionary of elements_data
        elements_data[model_data.loc[i, 'class_name']] = element_data
    return elements_data


def analyse_statistics(model_statistics, elements):
    # generates a dictionary of elements -> dictionary of statistics(stat->value)
    elements_statistics = dict()
    i = 0
    for key in elements.keys():
        stats = dict()
        stats['diff_pk_classes_types_p'] = model_statistics.loc[i, 'diff_pk_classes_types_p']
        stats['diff_tk_classes_types_p'] = model_statistics.loc[i, 'diff_tk_classes_types_p']
        stats['diff_known_classif_types_p'] = model_statistics.loc[i, 'diff_known_classif_types_p']
        elements_statistics[elements[key]] = stats
        i = i + 1
    return elements_statistics


def enforce_strategy_on_elements(strategy, elements, elements_statistics, elements_data):
    # removes the elements that do not belong to the strategy of the run
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


def taxonomy_mean(elements, elements_statistics):
    taxonomy_diff_pk = []
    taxonomy_diff_tk = []
    taxonomy_classif_diff = []
    for element in elements_statistics:
        taxonomy_diff_pk.append(elements_statistics[element]['diff_pk_classes_types_p'])
        taxonomy_diff_tk.append(elements_statistics[element]['diff_tk_classes_types_p'])
        taxonomy_classif_diff.append(elements_statistics[element]['diff_known_classif_types_p'])

    return statistics.mean(taxonomy_diff_pk), statistics.mean(taxonomy_diff_tk), statistics.mean(taxonomy_classif_diff)
