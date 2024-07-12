# Scior-Data-Analysis
This repository contains the data analysis environment created to analyze the best initial seeding strategy for running Scior. The paper describing this process, Data Analysis on Effective Strategies to Enhance the Semantics of OWL Ontologies:

> OWL has been created to support the development of the Semantic Web, a prime initiative that aims to make the Web more machine-readable and actionable. Many believe that the ontologies created with OWL can be further improved, especially in regards to the interoperability and reusability aspects of the FAIR principles. To this end, gUFO, a lightweight implementation of UFO, can better support the semantics of the OWL ontologies to ensure the FAIR principles are incorporated into the generated models, reducing the possibility of having interoperability problems such as the false agreement problem. This work aimed to contribute to enhancing the semantics of OWL ontologies in the most effective and automated way by analyzing the usage of OWL meta-properties in Scior. Scior is a software that infers the ontological categories of OWL classes through gUFO. The objective of this work was to look for better practices for this process to identify the best initial seeding. Throughout the data analysis, 8 strategies related to the position, sortality, and rigidity of the initial seeding have been examined. The results and the subsequent discussion of them suggest that there are indeed better strategies to adopt while enhancing the semantics of OWL ontologies with Scior. 

### Specifications
The data analysis environment has been created in Python 3.12 and the libraries used can be found in the paper.

### Installation Requirements
There is no installation requirement other than having Python 3.12 in your environment.

### Execution Guidelines
The main of FileReader can be run to start the data analysis. 

Each run generates two graphs for either CWA or OWA models. This can be changed by changing the check_complete variable on line 14 of FileReader. If the variable is True, the run will be done for CWA models and if it is False, then the run will be done for OWA models.

### Results
As mentioned in the Execution Guidelines, each run will generate two graphs for either CWA or OWA models. One of the graphs is a strategy comparison graph which compares the 8 strategies against each other. The second graph, however, is a strategy combination graph. This graph combines all 3 categories of strategies to have 18 combined strategies. The resulting graph compares these 18 combined strategies against each other.

The graphs can be distinguished by their file names or different figure sizes, as the titles of the graphs have been falsely duplicated for both the strategy comparison and strategy combination graphs.

If a given strategy has no instance in the data provided, then the strategy will not appear in the resulting graph. Currently, the R_S_ARG strategy for the CWA combined strategy graph has no instances and does not appear on the graph. On the other hand, some strategies result in 0 in all the measurements. This is the case when Scior cannot learn anything about the taxonomy from the instances of this strategy.

Lastly, there have been other graphs created throughout the project. These graphs were either generated to test individual functionality or deemed out of scope. These graphs can be found in the out of scope graphs directory under the graphs directory.

### Skipped Taxonomies
There have been an assortment of taxonomies that were skipped due to various reasons. A list of these taxonomies that were skipped can be found in the documentation directory. More information on why the taxonomies were skipped can be found in the paper. Moreover, there are commented print statements throughout the code. These can be uncommented to show which taxonomies were skipped for what reasons.

## Relevant Repositories:
[Scior](https://github.com/unibz-core/Scior) is a best-paper-award-winning software that outputs the gUFO meta-properties of the classes within a taxonomy after an initial seeding is provided. Scior is the tool evaluated with this data analysis environment. More information on Scior can be found in its repository and the paper provided above.

[Scior Dataset](https://github.com/unibz-core/Scior-Dataset) contains the data generated when Scior was tested for its original paper. This dataset has provided the data that was analyzed within this environment. This repository's catalog and documentation directories have been taken from the Scior Dataset. The catalog directory stores the data analyzed and the documentation directory holds documentation about the catalog provided. Out of the data present in the catalog directory, this environment only analyzes the Test 1 results, as Test 2 results are not relevant to the data analysis conducted.

## Contributors
* [Tibet Tugay](https://orcid.org/0009-0007-8315-9760) [[Github]](https://github.com/taybtt) [[Github]](https://github.com/ttugay) [[LinkedIn]](https://www.linkedin.com/in/tibet-tugay-084583281/)
* [Pedro Paulo F. Barcelos](https://orcid.org/0000-0003-2736-7817) [[Github]](https://github.com/pedropaulofb) [[LinkedIn]](https://www.linkedin.com/in/pedro-paulo-favato-barcelos/)
