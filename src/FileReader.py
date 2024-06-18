import os
import pandas as pd

# TODO LATER PROBLY SHOULD MAKE IT SO THAT THE CATALOG PATH COMES IN FROM THE ENV FILE
# start from the catalog directory
directory_path = os.path.realpath(r"C:\Users\ttuga\Desktop\Research_Project\Software\sciorDataAnalysis\catalog")
# TODO LATER MAKE SURE TO GET THE COMPLETENESS AS AN ARGUMENT
check_complete = True


def read_taxonomy(path, number_of_taxonomies, model_name):
    for tax_num in range(1, number_of_taxonomies):
        # read data_modelName_txnumber.csv
        read_file(os.path.join(path, "data_" + model_name + "_tx" + '{:03}'.format(tax_num) + ".csv"))

        # go into the tt001_ac for complete and tt001_an for incomplete
        if check_complete:
            test_path = os.path.join(path, "tt001_ac")

            # read statistics_modelName_tt001_ac_txNumber.csv
            read_file(
                os.path.join(test_path, "statistics_" + model_name + "_tt001_ac_tx" + '{:03}'.format(tax_num) + ".csv"))
        else:
            test_path = os.path.join(path, "tt001_an")

            # read statistics_modelName_tt001_an_txNumber.csv
            read_file(
                os.path.join(test_path, "statistics_" + model_name + "_tt001_aN_tx" + '{:03}'.format(tax_num) + ".csv"))

        # store or use the read data probly with pandas


def read_file(file_path):
    df = pd.read_csv(file_path)
    print(df)


def read_directory():
    models = os.listdir(directory_path)
    # pick one model
    for model in models:
        # go into the model directory
        path = os.path.join(directory_path, model)
        number_of_taxonomies = find_number_of_taxonomies(path)
        if os.path.isdir(os.path.join(path, "tt001_ac")) and os.path.isdir(os.path.join(path, "tt001_an")):
            read_taxonomy(path, number_of_taxonomies, model)
        else:
            continue


def is_ttl_file(file_path):
    root, ext = os.path.splitext(file_path)
    return ext == ".ttl"


def find_number_of_taxonomies(model_path):
    # a way to only get the number of taxonomies and not files in the model directory
    entries = os.listdir(model_path)
    turtles = [entry for entry in entries if is_ttl_file(os.path.join(model_path, entry))]
    return len(turtles)


if __name__ == "__main__":
    read_directory()
