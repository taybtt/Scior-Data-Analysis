import os
import statistics

import pandas as pd
from TaxonomyAnalyzer import analyse_taxonomy

"""
This file is to be used for testing the data analysis for a single model
"""
# TODO LATER PROBLY SHOULD MAKE IT SO THAT THE CATALOG PATH COMES IN FROM THE ENV FILE
# start from the catalog directory
directory_path = os.path.realpath(r"C:\Users\ttuga\Desktop\Research_Project\Software\sciorDataAnalysis\catalog")
# TODO LATER MAKE SURE TO GET THE COMPLETENESS AS AN ARGUMENT
check_complete = True


def read_taxonomy(path, number_of_taxonomies, model_name):
    diff_pk = []
    diff_tk = []
    classif_diff = []
    for tax_num in range(1, number_of_taxonomies+1):
        taxonomy_name = model_name + "_tx" + '{:03}'.format(tax_num)
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
            continue

        # go into the tt001_ac for complete and tt001_an for incomplete
        if check_complete:
            test_path = os.path.join(path, "tt001_ac")

            # read statistics_modelName_tt001_ac_txNumber.csv, if the file doesn't exist, just move to the next taxonomy
            try:
                model_statistics = read_file(
                    os.path.join(test_path, "statistics_" + model_name + "_tt001_ac_tx" + '{:03}'.format(tax_num) + ".csv"))
            except FileNotFoundError:
                # TODO MIGHT BE ABLE TO ADD THE MODEL AND THE TAXONOMY TO THE EXCEPTION LIST FROM HERE
                # THAT WAY WE WOULD HAVE A CONCRETE VIEW OF THE SKIPPED TAXONOMIES
                continue
        else:
            test_path = os.path.join(path, "tt001_an")

            # read statistics_modelName_tt001_an_txNumber.csv, if the file doesn't exist, just move to the next taxonomy
            try:
                model_statistics = read_file(
                    os.path.join(test_path, "statistics_" + model_name + "_tt001_aN_tx" + '{:03}'.format(tax_num) + ".csv"))
            except FileNotFoundError:
                # TODO MIGHT BE ABLE TO ADD THE MODEL AND THE TAXONOMY TO THE EXCEPTION LIST FROM HERE
                # THAT WAY WE WOULD HAVE A CONCRETE VIEW OF THE SKIPPED TAXONOMIES
                continue

        # store or use the read data probly with pandas
        diff_pk_mean, diff_tk_mean, classif_diff_mean = analyse_taxonomy(model_data, model_statistics, taxonomy_name)
        diff_pk.append(diff_pk_mean)
        diff_tk.append(diff_tk_mean)
        classif_diff.append(classif_diff_mean)
    return statistics.mean(diff_pk), statistics.mean(diff_tk), statistics.mean(classif_diff)


def read_file(file_path):
    df = pd.read_csv(file_path)
    # print(df)
    return df


def read_directory():
    models = os.listdir(directory_path)
    # pick one model
    # TODO UNCOMMENT THIS
    # for model in models:
    model = models[0]
    # skipping the files that are not model directories
    # if not os.path.isdir(os.path.join(directory_path, model)):
    #     continue

    # go into the model directory
    path = os.path.join(directory_path, model)
    number_of_taxonomies = find_number_of_taxonomies(path)

    # checking if the model has been tested for test1
    # if os.path.isdir(os.path.join(path, "tt001_ac")) and os.path.isdir(os.path.join(path, "tt001_an")):
        # trying to read the necessary files
    read_taxonomy(path, number_of_taxonomies, model)
    # else:
    #     continue


def is_ttl_file(file_path):
    root, ext = os.path.splitext(file_path)
    return ext == ".ttl"


def find_number_of_taxonomies(model_path):
    # a way to only get the number of taxonomies and not files in the model directory
    entries = os.listdir(model_path)
    turtles = [entry for entry in entries if is_ttl_file(os.path.join(model_path, entry))]
    return len(turtles)


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

if __name__ == "__main__":
    read_directory()
