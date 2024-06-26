import os
import statistics

import pandas as pd
from TaxonomyAnalyzer import analyse_taxonomy, analyse_combined_taxonomy
from Grapher import make_strategy_graph, make_combined_strategy_graph

# TODO LATER PROBLY SHOULD MAKE IT SO THAT THE CATALOG PATH COMES IN FROM THE ENV FILE
# start from the catalog directory
directory_path = os.path.realpath(r"C:\Users\ttuga\Desktop\Research_Project\Software\sciorDataAnalysis\catalog")

# TODO LATER MAKE SURE TO GET THE COMPLETENESS AS AN ARGUMENT
#  OR PUT THE WHOLE THING IN A FOR LOOP TO RUN THEM BOTH AT THE SAME TIME

# can change whether to run CWA or OWA from this variable
# False for OWA, True for CWA
check_complete = True

# true for only the combined graph, false for only the regular graph, none for both
# TODO MAKE THE PART OF BEING ABLE TO RUN BOTH AT THE SAME TIME
combined_graph = True


def read_taxonomy(path, number_of_taxonomies, model_name, strategy, sub_super_strategy, min_max_strategy):
    model_diff_pks = []
    model_diff_tks = []
    model_classif_diffs = []
    for tax_num in range(1, number_of_taxonomies + 1):
        taxonomy_name = model_name + "_tx" + '{:03}'.format(tax_num)
        # print(taxonomy_name)
        # print(model_name)
        # checks if the taxonomy is within the exception list
        # if TAXONOMY_EXCEPTION_DICT.keys().__contains__(model_name):
        #     if tax_num in TAXONOMY_EXCEPTION_DICT[model_name]:
        #         continue
        #     if 0 in TAXONOMY_EXCEPTION_DICT[model_name]:
        #         continue

        # read data_modelName_txnumber.csv, if the file doesn't exist, just move to the next taxonomy
        try:
            model_data = read_file(os.path.join(path, "data_" + model_name + "_tx" + '{:03}'.format(tax_num) + ".csv"))
        except FileNotFoundError:
            # TODO MIGHT BE ABLE TO ADD THE MODEL AND THE TAXONOMY TO THE EXCEPTION LIST FROM HERE
            # THAT WAY WE WOULD HAVE A CONCRETE VIEW OF THE SKIPPED TAXONOMIES
            # print(taxonomy_name)
            continue

        # go into the tt001_ac for complete and tt001_an for incomplete
        if check_complete:
            test_path = os.path.join(path, "tt001_ac")

            # read statistics_modelName_tt001_ac_txNumber.csv, if the file doesn't exist, just move to the next taxonomy
            try:
                model_statistics = read_file(
                    os.path.join(test_path,
                                 "statistics_" + model_name + "_tt001_ac_tx" + '{:03}'.format(tax_num) + ".csv"))
                # skipping taxonomies that have less than 5 classes in them
                # normally this should have been done with the model data, however,
                # due to inconsistencies between data and statistics files I have to do it here
                if len(model_statistics) < 5:
                    # print(taxonomy_name)
                    continue
                # print(len(model_statistics))
                # reading the summary file to be able to match the execution number with the element name
                model_summary = read_file(os.path.join(test_path,
                                                       "summary_" + model_name + "_tt001_ac_tx" + '{:03}'.format(
                                                           tax_num) + ".csv"))
            except FileNotFoundError:
                # TODO MIGHT BE ABLE TO ADD THE MODEL AND THE TAXONOMY TO THE EXCEPTION LIST FROM HERE
                # THAT WAY WE WOULD HAVE A CONCRETE VIEW OF THE SKIPPED TAXONOMIES
                # print(taxonomy_name)
                continue
        else:
            test_path = os.path.join(path, "tt001_an")

            # read statistics_modelName_tt001_an_txNumber.csv, if the file doesn't exist, just move to the next taxonomy
            try:
                model_statistics = read_file(
                    os.path.join(test_path,
                                 "statistics_" + model_name + "_tt001_an_tx" + '{:03}'.format(tax_num) + ".csv"))

                # skipping taxonomies that have less than 5 classes in them
                # normally this should have been done with the model data, however,
                # due to inconsistencies between data and statistics files I have to do it here
                if len(model_statistics) < 5:
                    # print(taxonomy_name)
                    continue
                # reading the summary file to be able to match the execution number with the element name
                model_summary = read_file(os.path.join(test_path,
                                                       "summary_" + model_name + "_tt001_an_tx" + '{:03}'.format(
                                                           tax_num) + ".csv"))
                # print(len(model_statistics))
            except FileNotFoundError:
                # TODO MIGHT BE ABLE TO ADD THE MODEL AND THE TAXONOMY TO THE EXCEPTION LIST FROM HERE
                # THAT WAY WE WOULD HAVE A CONCRETE VIEW OF THE SKIPPED TAXONOMIES
                # print(taxonomy_name)
                continue

        # store or use the read data probly with pandas
        # if we get statistics error, that is because this taxonomy doesn't have any classes
        # that conform to the strategy we are using, thus we skip the taxonomy
        try:
            taxonomy_diff_pk_mean, taxonomy_diff_tk_mean, taxonomy_classif_diff_mean = analyse_taxonomy(model_data,
                                                                                                        model_statistics,
                                                                                                        model_summary,
                                                                                                        taxonomy_name,
                                                                                                        strategy,
                                                                                                        sub_super_strategy,
                                                                                                        min_max_strategy)
            model_diff_pks.append(taxonomy_diff_pk_mean)
            model_diff_tks.append(taxonomy_diff_tk_mean)
            model_classif_diffs.append(taxonomy_classif_diff_mean)
        except statistics.StatisticsError:
            continue
    return model_diff_pks, model_diff_tks, model_classif_diffs


def read_file(file_path):
    df = pd.read_csv(file_path)
    return df


def read_directory():
    models = os.listdir(directory_path)
    # for sub_super_strategy in SUB_SUPER_STRATEGIES:
    #     iteration_count = 0
    #     # print(iteration_count, sub_super_strategy)
    #     for min_max_strategy in MIN_MAX_STRATEGIES:
    #         # we skip the rest of the iterations for NONE since there should only be one graph of means of strategies
    #         if sub_super_strategy == "NONE" and iteration_count > 0:
    #             continue
    #
    #         # pick one model
    #         strategy_statistics = dict()
    #         for strategy in STRATEGIES:
    #             catalog_diff_pks = []
    #             catalog_diff_tks = []
    #             catalog_classif_diffs = []
    #             for model in models:
    #                 # if not (model == 'abel2015petroleum-system'):
    #                 #     continue
    #                 # skipping the files that are not model directories
    #                 if not os.path.isdir(os.path.join(directory_path, model)):
    #                     continue
    #
    #                 # go into the model directory
    #                 path = os.path.join(directory_path, model)
    #                 number_of_taxonomies = find_number_of_taxonomies(path)
    #
    #                 # checking if the model has been tested for test1
    #                 if os.path.isdir(os.path.join(path, "tt001_ac")) and os.path.isdir(os.path.join(path, "tt001_an")):
    #                     # trying to read the necessary files
    #                     try:
    #                         # adds the means of the taxonomies of the models into the graph list for the said attribute
    #                         model_diff_pk, model_diff_tk, model_classif_diff = (
    #                             read_taxonomy(path, number_of_taxonomies, model, strategy, sub_super_strategy,
    #                                           min_max_strategy))
    #                         # adding all the taxonomy means from that model to the list of means for the entire catalog
    #                         for i in range(len(model_diff_pk)):
    #                             catalog_diff_pks.append(model_diff_pk[i])
    #                             catalog_diff_tks.append(model_diff_tk[i])
    #                             catalog_classif_diffs.append(model_classif_diff[i])
    #                     # except KeyError:
    #                     #     # TODO: THIS IS THE MODEL EXCEPTION LIST, DONT FORGET TO REMOVE/DOCUMENT IT
    #                     #     # skips a model that has inconsistency in its data and statistics files in one of its taxonomies
    #                     #     continue
    #                     except statistics.StatisticsError:
    #                         # if we get this, it is because the model doesn't have a single class in any of its taxonomies
    #                         # that conform to the strategy we are using, thus we skip the model
    #                         continue
    #                 else:
    #                     # TODO SHOW THE SKIPPED TAXONOMIES FROM HERE AS WELL
    #                     continue
    #             try:
    #                 strategy_statistics[strategy] = [statistics.mean(catalog_diff_pks),
    #                                                  statistics.mean(catalog_diff_tks),
    #                                                  statistics.mean(catalog_classif_diffs)]
    #             except statistics.StatisticsError:
    #                 # if we get this, it is because the model doesn't have a single class in any of its taxonomies
    #                 # that conform to the strategy we are using, thus we skip the model
    #                 continue
    #         make_strategy_graph(strategy_statistics, sub_super_strategy, min_max_strategy, check_complete)
    #         iteration_count = iteration_count + 1

    combined_statistics = dict()
    for position in POSITIONAL_STRATEGIES:
        for sortality in SORTALITY_STRATEGIES:
            for rigidity in RIGIDITY_STRATEGIES:
                catalog_diff_pks = []
                catalog_diff_tks = []
                catalog_classif_diffs = []
                for model in models:
                    # if not (model == 'abel2015petroleum-system'):
                    #     continue
                    # skipping the files that are not model directories
                    if not os.path.isdir(os.path.join(directory_path, model)):
                        continue

                    # go into the model directory
                    path = os.path.join(directory_path, model)
                    number_of_taxonomies = find_number_of_taxonomies(path)

                    # checking if the model has been tested for test1
                    if os.path.isdir(os.path.join(path, "tt001_ac")) and os.path.isdir(os.path.join(path, "tt001_an")):
                        # trying to read the necessary files
                        try:
                            # adds the means of the taxonomies of the models into the graph list for the said attribute
                            model_diff_pk, model_diff_tk, model_classif_diff = (
                                read_combined_taxonomies(path, number_of_taxonomies, model, position, sortality,
                                                         rigidity))
                            # adding all the taxonomy means from that model to the list of means for the entire catalog
                            for i in range(len(model_diff_pk)):
                                catalog_diff_pks.append(model_diff_pk[i])
                                catalog_diff_tks.append(model_diff_tk[i])
                                catalog_classif_diffs.append(model_classif_diff[i])
                        # except KeyError:
                        #     # TODO: THIS IS THE MODEL EXCEPTION LIST, DONT FORGET TO REMOVE/DOCUMENT IT
                        #     # skips a model that has inconsistency in its data and statistics files in one of its taxonomies
                        #     continue
                        except statistics.StatisticsError:
                            # if we get this, it is because the model doesn't have a single class in any of its taxonomies
                            # that conform to the strategy we are using, thus we skip the model
                            continue
                    else:
                        # TODO SHOW THE SKIPPED TAXONOMIES FROM HERE AS WELL
                        continue
                try:
                    combined_statistics[get_combined_strategy_name(position, sortality, rigidity)] = [
                        statistics.mean(catalog_diff_pks),
                        statistics.mean(catalog_diff_tks),
                        statistics.mean(catalog_classif_diffs)]
                except statistics.StatisticsError:
                    print(get_combined_strategy_name(position, sortality, rigidity))
                    # if we get this, it is because the model doesn't have a single class in any of its taxonomies
                    # that conform to the strategy we are using, thus we skip the model
                    continue
    make_combined_strategy_graph(combined_statistics, check_complete)


def read_combined_taxonomies(path, number_of_taxonomies, model_name, position, sortality, rigidity):
    model_diff_pks = []
    model_diff_tks = []
    model_classif_diffs = []
    for tax_num in range(1, number_of_taxonomies + 1):
        taxonomy_name = model_name + "_tx" + '{:03}'.format(tax_num)
        # print(taxonomy_name)
        # print(model_name)
        # checks if the taxonomy is within the exception list
        # if TAXONOMY_EXCEPTION_DICT.keys().__contains__(model_name):
        #     if tax_num in TAXONOMY_EXCEPTION_DICT[model_name]:
        #         continue
        #     if 0 in TAXONOMY_EXCEPTION_DICT[model_name]:
        #         continue

        # read data_modelName_txnumber.csv, if the file doesn't exist, just move to the next taxonomy
        try:
            model_data = read_file(os.path.join(path, "data_" + model_name + "_tx" + '{:03}'.format(tax_num) + ".csv"))
        except FileNotFoundError:
            # TODO MIGHT BE ABLE TO ADD THE MODEL AND THE TAXONOMY TO THE EXCEPTION LIST FROM HERE
            # THAT WAY WE WOULD HAVE A CONCRETE VIEW OF THE SKIPPED TAXONOMIES
            # print(taxonomy_name)
            continue

        # go into the tt001_ac for complete and tt001_an for incomplete
        if check_complete:
            test_path = os.path.join(path, "tt001_ac")

            # read statistics_modelName_tt001_ac_txNumber.csv, if the file doesn't exist, just move to the next taxonomy
            try:
                model_statistics = read_file(
                    os.path.join(test_path,
                                 "statistics_" + model_name + "_tt001_ac_tx" + '{:03}'.format(tax_num) + ".csv"))
                # skipping taxonomies that have less than 5 classes in them
                # normally this should have been done with the model data, however,
                # due to inconsistencies between data and statistics files I have to do it here
                if len(model_statistics) < 5:
                    # print(taxonomy_name)
                    continue
                # print(len(model_statistics))
                # reading the summary file to be able to match the execution number with the element name
                model_summary = read_file(os.path.join(test_path,
                                                       "summary_" + model_name + "_tt001_ac_tx" + '{:03}'.format(
                                                           tax_num) + ".csv"))
            except FileNotFoundError:
                # TODO MIGHT BE ABLE TO ADD THE MODEL AND THE TAXONOMY TO THE EXCEPTION LIST FROM HERE
                # THAT WAY WE WOULD HAVE A CONCRETE VIEW OF THE SKIPPED TAXONOMIES
                # print(taxonomy_name)
                continue
        else:
            test_path = os.path.join(path, "tt001_an")

            # read statistics_modelName_tt001_an_txNumber.csv, if the file doesn't exist, just move to the next taxonomy
            try:
                model_statistics = read_file(
                    os.path.join(test_path,
                                 "statistics_" + model_name + "_tt001_an_tx" + '{:03}'.format(tax_num) + ".csv"))

                # skipping taxonomies that have less than 5 classes in them
                # normally this should have been done with the model data, however,
                # due to inconsistencies between data and statistics files I have to do it here
                if len(model_statistics) < 5:
                    # print(taxonomy_name)
                    continue
                # reading the summary file to be able to match the execution number with the element name
                model_summary = read_file(os.path.join(test_path,
                                                       "summary_" + model_name + "_tt001_an_tx" + '{:03}'.format(
                                                           tax_num) + ".csv"))
                # print(len(model_statistics))
            except FileNotFoundError:
                # TODO MIGHT BE ABLE TO ADD THE MODEL AND THE TAXONOMY TO THE EXCEPTION LIST FROM HERE
                # THAT WAY WE WOULD HAVE A CONCRETE VIEW OF THE SKIPPED TAXONOMIES
                # print(taxonomy_name)
                continue

        # store or use the read data probly with pandas
        # if we get statistics error, that is because this taxonomy doesn't have any classes
        # that conform to the strategy we are using, thus we skip the taxonomy
        try:
            taxonomy_diff_pk_mean, taxonomy_diff_tk_mean, taxonomy_classif_diff_mean = analyse_combined_taxonomy(
                model_data,
                model_statistics,
                model_summary,
                position,
                sortality,
                rigidity)
            model_diff_pks.append(taxonomy_diff_pk_mean)
            model_diff_tks.append(taxonomy_diff_tk_mean)
            model_classif_diffs.append(taxonomy_classif_diff_mean)
        except statistics.StatisticsError:
            continue
    return model_diff_pks, model_diff_tks, model_classif_diffs


def is_ttl_file(file_path):
    root, ext = os.path.splitext(file_path)
    return ext == ".ttl"


def find_number_of_taxonomies(model_path):
    # a way to only get the number of taxonomies and not files in the model directory
    entries = os.listdir(model_path)
    turtles = [entry for entry in entries if is_ttl_file(os.path.join(model_path, entry))]
    return len(turtles)


def get_combined_strategy_name(position, sortality, rigidity):
    match position:
        case 'ROOT':
            return 'R_' + get_combined_strategy_sortality_name(sortality, rigidity)
        case 'LEAF':
            return 'L_' + get_combined_strategy_sortality_name(sortality, rigidity)
        case 'INTERMEDIATE':
            return 'I_' + get_combined_strategy_sortality_name(sortality, rigidity)


def get_combined_strategy_sortality_name(sortality, rigidity):
    match sortality:
        case 'SORTAL':
            return 'S_' + get_combined_strategy_rigidity_name(rigidity)
        case 'NON_SORTAL':
            return 'NS_' + get_combined_strategy_rigidity_name(rigidity)


def get_combined_strategy_rigidity_name(rigidity):
    match rigidity:
        case 'RIGID':
            return 'RG'
        case 'ANTI_RIGID':
            return 'ARG'
        case 'SEMI_RIGID':
            return 'SRG'


STRATEGIES = [
    'ROOT',
    'LEAF',
    'INTERMEDIATE',
    'SORTAL',
    'NON_SORTAL',
    'RIGID',
    'ANTI_RIGID',
    'SEMI_RIGID'
]

SUB_SUPER_STRATEGIES = [
    'NONE',
    'SUPERCLASS',
    'SUBCLASS'
]

MIN_MAX_STRATEGIES = [
    'MAX',
    'MIN'
]

POSITIONAL_STRATEGIES = [
    'ROOT',
    'LEAF',
    'INTERMEDIATE'
]

SORTALITY_STRATEGIES = [
    'SORTAL',
    'NON_SORTAL'
]

RIGIDITY_STRATEGIES = [
    'RIGID',
    'ANTI_RIGID',
    'SEMI_RIGID'
]



# """A dictionary that holds all the taxonomies that should be skipped while evaluating the dataset. The reason for
# skipping these taxonomies is that the dataset lacks one of the documents required for this evaluation on this taxonomy
# Key: the name of the model
# Value: an array that holds the numbers of the taxonomies that should be skipped
# """
# TAXONOMY_EXCEPTION_DICT = {
#     "albuquerque2011ontobio": [7],
#     "amaral2020game-theory": [2, 3],
#     # ^ think 4 should also give an error, but it's not doing that, maybe check it manually
#     "aristotle-ontology2019": [13],
#     "bernasconi2021ontovcm": [7],
#     "cmpo2017": [3],
#     "derave2019dpo": [6, 8, 18],
#     "dpo2017": [3, 4],
#     "ferreira2015ontoemergeplan": [2, 3, 5, 7, 9, 10, 15, 16],
#     "gi2mo": [2, 3],
#     "guizzardi2020decision-making": [1],
#     "guizzardi2022ufo": [9]
# }

# EXCEPTION_LIST = [
#     'alpinebits2022',
#     'dpo2017'
# ]

if __name__ == "__main__":
    read_directory()
