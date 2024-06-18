def analyse_taxonomy(model_data, model_statistics):
    # the first part is the row, the second part is the column
    # print(model_data.loc[0, 'class_name'])

    # the classes within the taxonomy with their extracted information
    elements = analyse_data(model_data)
    print(elements)


def analyse_data(model_data):
    elements = dict()
    for i in range(0, len(model_data)):
        # add all the necessary information about an element to the dictionary with the element name as the key
        elements[model_data.loc[i, 'class_name']] = [model_data.loc[i, 'is_root'], model_data.loc[i, 'is_leaf'],
                                                     model_data.loc[i, 'number_superclasses'],
                                                     model_data.loc[i, 'number_subclasses']]
    return elements
