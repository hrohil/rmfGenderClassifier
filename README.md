# Rate My Professor Gender Classifier 

This project looks to explore how the writing and wording of comments (with pronouns removed) on ratemyprofessor.com (RMP) can be used to determine the professor's gender. This project consists of the following programs and data files:
### Programs for acquiring data, processing, and classification ###
* a webcrawler that crawls RMP pages for 21 universities and outputs to one file
    * commentCrawler.py
* a text-parser that converts the raw data file into data files of comments for individual professors
    * parseDataIntoFiles.py
    * produces allData
* a text processer that tokenizes, removes stopwords, and stems the files in allData and produces prerocessedData
    * preprocessAllFiles.py
* a program used to predict the gender of professors using Naive Bayes. Uses the 'leave one out' strategy, and trains on the remaining preprocessed data files
    * naiveBayes.py
    
### Data and Output Files ###
* Data file containing all the raw text from commentCrawler.py
    * commentCrawler.output
* Folder of data files containing comments on each professor's RMP page parsed from parseDataIntoFiles.py without preprocessing
    * allData
* Folder of data files from allData that have been preprocessed by preprocessAllFiles.py
    * preprocessedData
* Folder of data files of additional male professors (removed to balance the number of male and female professors)
    * extraMaleData
* Results of classifications using Naive Bayes from preprocessedData
    * naivebayes.output


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

A computer with python 3.7 and the following packages installed:
* pip
* nltk
* selenium
* BeautifulSoup
* Python 3 Virtual Environment (optional)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Porter Stemmer [https://tartarus.org/martin/PorterStemmer/]
