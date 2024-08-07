import os
import statistics
import pandas as pd
from TaxonomyAnalyzer import analyse_taxonomy, analyse_combined_taxonomy
from Grapher import make_strategy_graph, make_combined_strategy_graph
from dotenv import load_dotenv

load_dotenv()
# gets the directory of the Scior Dataset Catalog from the .env file
directory_path = os.getenv('INPUT_DIRECTORY')

# can change whether to run CWA or OWA from this variable
# False for OWA, True for CWA
check_complete = False


def read_directory():
    """
    This is the general function that reads the input directory and generates the strategy comparison and combined
    strategy graphs in the output directory.
    """
    models = os.listdir(directory_path)
    strategies_to_skip = []

    # STRATEGY COMPARISON GRAPH CREATION
    strategy_statistics = dict()
    for strategy in STRATEGIES:
        catalog_diff_pks, catalog_diff_tks, catalog_classif_diffs = extract_statistics_from_directory(models, False,
                                                                                                      strategy=strategy)
        try:
            strategy_statistics[strategy] = [statistics.mean(catalog_diff_pks),
                                             statistics.mean(catalog_diff_tks),
                                             statistics.mean(catalog_classif_diffs)]
        except statistics.StatisticsError:
            # if we get this, it is because the models do not have a single class in any of its taxonomies
            # that conform to the strategy we are using, thus we skip the strategy.
            # the strategy also gets added to the skipped strategies so that it is removed from the corresponding graph
            # print(strategy)
            strategies_to_skip.append(strategy)
            continue
    make_strategy_graph(strategy_statistics, check_complete, strategies_to_skip)

    # COMBINED STRATEGIES GRAPH CREATION
    strategies_to_skip.clear()
    combined_statistics = dict()
    for position in POSITIONAL_STRATEGIES:
        for sortality in SORTALITY_STRATEGIES:
            for rigidity in RIGIDITY_STRATEGIES:
                catalog_diff_pks, catalog_diff_tks, catalog_classif_diffs = extract_statistics_from_directory(
                    models,
                    True,
                    position=position,
                    sortality=sortality,
                    rigidity=rigidity)
                try:
                    combined_statistics[get_combined_strategy_name(position, sortality, rigidity)] = [
                        statistics.mean(catalog_diff_pks),
                        statistics.mean(catalog_diff_tks),
                        statistics.mean(catalog_classif_diffs)]
                except statistics.StatisticsError:
                    # if we get this, it is because the models do not have a single class in any of its taxonomies
                    # that conform to the strategy we are using, thus we skip and possibly print the strategy. the
                    # strategy also gets added to the skipped strategies so that it is removed from the corresponding
                    # graph
                    # print(get_combined_strategy_name(position, sortality, rigidity))
                    strategies_to_skip.append(get_combined_strategy_name(position, sortality, rigidity))
                    continue
    make_combined_strategy_graph(combined_statistics, check_complete, strategies_to_skip)


def extract_statistics_from_directory(models, check_combined, strategy=None, position=None, sortality=None,
                                      rigidity=None):
    """
    This function extracts statistics from the entire input directory for one for the strategies (either a single
    strategy or a combined one) and returns the statistics regarding the whole dataset catalog
    :param models: the models in the dataset catalog
    :param check_combined: whether the extraction of the statistics are done for a combined graph or comparison graph
    :param strategy: if it is done for a comparison graph, which strategy the extraction is for
    :param position: if it is done for a combined graph, which position strategy the extraction is for
    :param sortality: if it is done for a combined graph, which sortality strategy the extraction is for
    :param rigidity: if it is done for a combined graph, which rigidity strategy the extraction is for
    :return: the difference in partially known class percentages for the whole catalog, the difference in totally known
    class percentages for the whole catalog, and the difference in classifications known percentages for the whole
    catalog
    """
    catalog_diff_pks = []
    catalog_diff_tks = []
    catalog_classif_diffs = []
    for model in models:
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
                if check_combined:
                    model_diff_pk, model_diff_tk, model_classif_diff = (read_combined_taxonomies(path,
                                                                                                 number_of_taxonomies,
                                                                                                 model, position,
                                                                                                 sortality, rigidity))
                else:
                    model_diff_pk, model_diff_tk, model_classif_diff = (read_taxonomy(path, number_of_taxonomies, model,
                                                                                      strategy))
                # adding all the taxonomy means of a model to the list of means for the entire catalog
                for i in range(len(model_diff_pk)):
                    catalog_diff_pks.append(model_diff_pk[i])
                    catalog_diff_tks.append(model_diff_tk[i])
                    catalog_classif_diffs.append(model_classif_diff[i])
            except statistics.StatisticsError:
                # if we get this, it is because the model doesn't have a single class in any of its taxonomies
                # that conform to the strategy we are using, thus we skip the model
                # print(model)
                continue
        else:
            continue
    return catalog_diff_pks, catalog_diff_tks, catalog_classif_diffs


def read_file(file_path):
    """
    Reads the file of the given path and puts it in a dataframe
    :param file_path: the path of the file to read
    :return: the dataframe containing the contents of the file
    """
    df = pd.read_csv(file_path)
    return df


def read_taxonomy(path, number_of_taxonomies, model_name, strategy):
    """
    This function reads all the taxonomies within a model for a strategy comparison graph
    :param path: path of the model
    :param number_of_taxonomies: number of taxonomies within the model
    :param model_name: name of the model
    :param strategy: strategy used for the initial seeding
    :return: a list of the difference in partially known class percentages for each taxonomy of the model, a list of the
     difference in totally known class percentages for each taxonomy of the model, and a list of the diffrence in
     classifications known percentages for each taxonomy of the model
    """
    model_diff_pks = []
    model_diff_tks = []
    model_classif_diffs = []
    for tax_num in range(1, number_of_taxonomies + 1):
        break_loop, taxonomy_data, taxonomy_statistics, taxonomy_summary, taxonomy_name = extract_taxonomy_information(
            path,
            model_name,
            tax_num)

        if break_loop:
            # continue in the case of finding an exception
            continue

        try:
            taxonomy_diff_pk_mean, taxonomy_diff_tk_mean, taxonomy_classif_diff_mean = analyse_taxonomy(
                taxonomy_data,
                taxonomy_statistics,
                taxonomy_summary,
                strategy)
            model_diff_pks.append(taxonomy_diff_pk_mean)
            model_diff_tks.append(taxonomy_diff_tk_mean)
            model_classif_diffs.append(taxonomy_classif_diff_mean)
        except statistics.StatisticsError:
            # if we get statistics error, that is because this taxonomy doesn't have any classes
            # that conform to the strategy we are using, thus we skip the taxonomy
            # print(taxonomy_name)
            continue
    return model_diff_pks, model_diff_tks, model_classif_diffs


def read_combined_taxonomies(path, number_of_taxonomies, model_name, position, sortality, rigidity):
    """
    This function reads all the taxonomies within a model for a strategy combination graph
    :param path: path of the model
    :param number_of_taxonomies: number of taxonomies within the model
    :param model_name: name of the model
    :param position: position strategy used for the initial seeding
    :param sortality: sortality strategy used for the initial seeding
    :param rigidity: rigidity strategy used for the initial seeding
    :return: a list of the difference in partially known class percentages for each taxonomy of the model, a list of the
     difference in totally known class percentages for each taxonomy of the model, and a list of the diffrence in
     classifications known percentages for each taxonomy of the model
    """
    model_diff_pks = []
    model_diff_tks = []
    model_classif_diffs = []
    for tax_num in range(1, number_of_taxonomies + 1):
        break_loop, taxonomy_data, taxonomy_statistics, taxonomy_summary, taxonomy_name = extract_taxonomy_information(
            path,
            model_name,
            tax_num)

        if break_loop:
            # continue in the case of finding an exception
            continue

        try:
            taxonomy_diff_pk_mean, taxonomy_diff_tk_mean, taxonomy_classif_diff_mean = analyse_combined_taxonomy(
                taxonomy_data,
                taxonomy_statistics,
                taxonomy_summary,
                position,
                sortality,
                rigidity)
            model_diff_pks.append(taxonomy_diff_pk_mean)
            model_diff_tks.append(taxonomy_diff_tk_mean)
            model_classif_diffs.append(taxonomy_classif_diff_mean)

        except statistics.StatisticsError:
            # if we get statistics error, that is because this taxonomy doesn't have any classes
            # that conform to the strategy we are using, thus we skip the taxonomy
            # print(taxonomy_name)
            continue
    return model_diff_pks, model_diff_tks, model_classif_diffs


def extract_taxonomy_information(path, model_name, tax_num):
    """
    This function extracts the information about a taxonomy stored within various files
    :param path: path of the model the taxonomy belongs to
    :param model_name: name of the model the taxonomy belongs to
    :param tax_num: number of the taxonomy within the model the taxonomy belongs to
    :return: whether the taxonomy needs to be skipped, information about the taxonomy from the data file,
    information about the taxonomy from the statistics file, information about the taxonomy from the summary file,
    and the name of the taxonomy
    """
    taxonomy_name = model_name + "_tx" + '{:03}'.format(tax_num)
    # read data_modelName_txnumber.csv, if the file doesn't exist, just move to the next taxonomy
    try:
        taxonomy_data = read_file(os.path.join(path, "data_" + model_name + "_tx" + '{:03}'.format(tax_num) + ".csv"))
    except FileNotFoundError:
        # if the data file is not present, we skip the taxonomy
        # print(taxonomy_name)
        return True, [], [], [], None

    # go into the tt001_ac for complete and tt001_an for incomplete
    if check_complete:
        test_path = os.path.join(path, "tt001_ac")

        # read statistics_modelName_tt001_ac_txNumber.csv, if the file doesn't exist, just move to the next taxonomy
        try:
            taxonomy_statistics = read_file(
                os.path.join(test_path,
                             "statistics_" + model_name + "_tt001_ac_tx" + '{:03}'.format(tax_num) + ".csv"))

            # skipping taxonomies that have less than 5 classes in them
            # normally this should have been done with the model data, however,
            # due to inconsistencies between data and statistics files we have to do it here
            if len(taxonomy_statistics) < 5:
                # print(taxonomy_name)
                return True, [], [], [], None

            # reading the summary file to be able to match the execution number with the element name
            taxonomy_summary = read_file(os.path.join(test_path,
                                                      "summary_" + model_name + "_tt001_ac_tx" + '{:03}'.format(
                                                          tax_num) + ".csv"))
        except FileNotFoundError:
            # if the statistics or the summary file is not present, we skip the taxonomy
            # print(taxonomy_name)
            return True, [], [], [], None
    else:
        test_path = os.path.join(path, "tt001_an")

        # read statistics_modelName_tt001_an_txNumber.csv, if the file doesn't exist, just move to the next taxonomy
        try:
            taxonomy_statistics = read_file(
                os.path.join(test_path,
                             "statistics_" + model_name + "_tt001_an_tx" + '{:03}'.format(tax_num) + ".csv"))

            # skipping taxonomies that have less than 5 classes in them
            # normally this should have been done with the model data, however,
            # due to inconsistencies between data and statistics files I have to do it here
            if len(taxonomy_statistics) < 5:
                # print(taxonomy_name)
                return True, [], [], [], None

            # reading the summary file to be able to match the execution number with the element name
            taxonomy_summary = read_file(os.path.join(test_path,
                                                      "summary_" + model_name + "_tt001_an_tx" + '{:03}'.format(
                                                          tax_num) + ".csv"))
        except FileNotFoundError:
            # if the statistics or the summary file is not present, we skip the taxonomy
            # print(taxonomy_name)
            return True, [], [], [], None
    return False, taxonomy_data, taxonomy_statistics, taxonomy_summary, taxonomy_name


def is_ttl_file(file_path):
    """
    This function checks if the file is a turtle file
    :param file_path: the path of the file to read
    :return: whether the file is a turtle file
    """
    root, ext = os.path.splitext(file_path)
    return ext == ".ttl"


def find_number_of_taxonomies(model_path):
    """
    This function finds the number of taxonomies in the model directory
    :param model_path: path of the model that requires to have its taxonomies counted
    :return: the number of taxonomies the model has
    """
    entries = os.listdir(model_path)
    turtles = [entry for entry in entries if is_ttl_file(os.path.join(model_path, entry))]
    return len(turtles)


def get_combined_strategy_name(position, sortality, rigidity):
    """
    This function is used to generate a name for a combined strategy
    :param position: position of the combined strategy
    :param sortality: sortality of the combined strategy
    :param rigidity: rigidity of the combined strategy
    :return: the string used to represent a combined strategy
    """
    match position:
        case 'ROOT':
            return 'R_' + get_combined_strategy_sortality_name(sortality, rigidity)
        case 'LEAF':
            return 'L_' + get_combined_strategy_sortality_name(sortality, rigidity)
        case 'INTERMEDIATE':
            return 'I_' + get_combined_strategy_sortality_name(sortality, rigidity)


def get_combined_strategy_sortality_name(sortality, rigidity):
    """
    This function is used to generate a half complete name for a combined strategy
    :param sortality: sortality of the combined strategy
    :param rigidity: rigidity of the combined strategy
    :return: the string used to represent a combined strategy without its position
    """
    match sortality:
        case 'SORTAL':
            return 'S_' + get_combined_strategy_rigidity_name(rigidity)
        case 'NON_SORTAL':
            return 'NS_' + get_combined_strategy_rigidity_name(rigidity)


def get_combined_strategy_rigidity_name(rigidity):
    """
        This function is used to generate an incomplete name for a combined strategy
        :param rigidity: rigidity of the combined strategy
        :return: the string used to represent a combined strategy without its position or sortality
        """
    match rigidity:
        case 'RIGID':
            return 'RG'
        case 'ANTI_RIGID':
            return 'ARG'
        case 'SEMI_RIGID':
            return 'SRG'


"""
Holds the full names of the strategies
"""
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

"""
Holds the full names of the position strategies
"""
POSITIONAL_STRATEGIES = [
    'ROOT',
    'LEAF',
    'INTERMEDIATE'
]

"""
Holds the full names of the sortality strategies
"""
SORTALITY_STRATEGIES = [
    'SORTAL',
    'NON_SORTAL'
]

"""
Holds the full names of the rigidity strategies
"""
RIGIDITY_STRATEGIES = [
    'RIGID',
    'ANTI_RIGID',
    'SEMI_RIGID'
]

if __name__ == "__main__":
    read_directory()
