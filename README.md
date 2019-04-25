# Rate My Professor Gender Classifier 

This project looks to explore how the writing and wording of comments (with pronouns removed) on ratemyprofessor.com (RMP) can be used to determine the professor's gender. The classification algorithms used are Naive Bayes, Rocchio Algorithm, and K-Nearest Neighbor.

 This project consists of the following programs and data files:
### Programs for acquiring data, processing, and classification ###
* a webcrawler that crawls RMP pages for 21 universities and outputs to one file
    * [commentCrawler.py](https://github.com/hrohil/rmfGenderClassifier/tree/master/commentCrawler.py)
* a text-parser that converts the raw data file into data files of comments for individual professors
    * [parseDataIntoFiles.py](https://github.com/hrohil/rmfGenderClassifier/tree/master/parseDataIntoFiles.py)
    * produces [allData](https://github.com/hrohil/rmfGenderClassifier/tree/master/allData)
* a text processer that tokenizes, removes stopwords, and stems the files in allData and produces prerocessedData
    * [preprocessAllFiles.py](https://github.com/hrohil/rmfGenderClassifier/tree/master/preprocessAllFiles.py)
* a program used to predict the gender of professors using Naive Bayes. Uses the 'leave one out' strategy, and trains on the remaining preprocessed data files
    * [naiveBayes.py](https://github.com/hrohil/rmfGenderClassifier/tree/master/naiveBayes.py)
* a program used to predict the gender of professors using Rocchio. Uses the 'leave one out' strategy, and trains on the remaining preprocessed data files
    * [rocchio.py](https://github.com/hrohil/rmfGenderClassifier/tree/master/rocchio.py)
* a program used to extract top adjectives used by students to describe male and female professors
    * [AdjectiveFreq.py](https://github.com/hrohil/rmfGenderClassifier/tree/master/AdjectiveFreq.py)
* a program used to preprocess comment crawler data for new format, to include regional CS professors
    * [preprocessCommentCrawler.py](https://github.com/hrohil/rmfGenderClassifier/tree/master/preprocessCommentCrawler.py)

    
### Data and Output Files ###
* Data file containing all the raw text from commentCrawler.py
    * [commentCrawler.output](https://github.com/hrohil/rmfGenderClassifier/tree/master/commentCrawler.output)
* Folder of data files containing comments on each professor's RMP page parsed from parseDataIntoFiles.py without preprocessing
    * [allData](https://github.com/hrohil/rmfGenderClassifier/tree/master/allData)
* Folder of data files from allData that have been preprocessed by preprocessAllFiles.py
    * [preprocessedData](https://github.com/hrohil/rmfGenderClassifier/tree/master/preprocessedData)
* Folder of data files of additional male professors (removed to balance the number of male and female professors)
    * [extraMaleData](https://github.com/hrohil/rmfGenderClassifier/tree/master/extraMaleData)
* Folder of data files of data from CS professors across NESW regions before processing
    * [commentCrawlerOutput](https://github.com/hrohil/rmfGenderClassifier/tree/master/commentCrawlerOutput)
* Folder of data files of data from CS professors across NESW regions before processing
    * [commentCrawlerOutputPreprocessed](https://github.com/hrohil/rmfGenderClassifier/tree/master/commentCrawlerOutputPreprocessed)
* Results of classifications using Naive Bayes from preprocessedData
    * [naivebayes.output](https://github.com/hrohil/rmfGenderClassifier/tree/master/naivebayes.output)
* Results of different words used for each professor group
    * [difference_analysis](https://github.com/hrohil/rmfGenderClassifier/tree/master/difference_analysis)
* Results of nearest neighbor after boosting word frequencies
    * [nearestNeighbour.boosted.output](https://github.com/hrohil/rmfGenderClassifier/tree/master/nearestNeighbour.boosted.output)
* Results of nearest neighbor after boosting word frequencies in Excel
    * [nearestNeighbour.boosted.output.excel](https://github.com/hrohil/rmfGenderClassifier/tree/master/nearestNeighbour.boosted.output)
* Results of nearest neighbor without boosting word frequencies in Excel (additional)
    * [nearestNeighbour.output.excel](https://github.com/hrohil/rmfGenderClassifier/tree/master/nearestNeighbour.output.excel)
* Results of professor ratings from CS departements across NESW regions (for two-sample t-test)
    * [prof_ratings.csv](https://github.com/hrohil/rmfGenderClassifier/tree/master/prof_ratings.csv)



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

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details

## Acknowledgments

* [Porter Stemmer](https://tartarus.org/martin/PorterStemmer/)
