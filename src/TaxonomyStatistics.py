import statistics


def taxonomy_mean(elements, elements_statistics):
    taxonomy_diff_pk = []
    taxonomy_diff_tk = []
    taxonomy_classif_diff = []
    for element in elements_statistics:
        taxonomy_diff_pk.append(elements_statistics[element]['diff_pk_classes_types_p'])
        taxonomy_diff_tk.append(elements_statistics[element]['diff_tk_classes_types_p'])
        taxonomy_classif_diff.append(elements_statistics[element]['diff_known_classif_types_p'])

    return statistics.mean(taxonomy_diff_pk), statistics.mean(taxonomy_diff_tk), statistics.mean(taxonomy_classif_diff)
