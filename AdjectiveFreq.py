import nltk
nltk.download('wordnet')
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize
import os
import csv


def main():
    stopwordsList = createStopwordsList()

    maleLowDic = {}
    maleHighDic = {}
    femaleLowDic = {}
    femaleHighDic = {}
    avgFemaleRating = 0.0
    avgMaleRating = 0.0
    totalFemales = 0
    totalMales = 0

    femaleRatings = []
    maleRatings = []

    for file in os.listdir("preprocessedData"):
        text = word_tokenize(open("preprocessedData/" +  file).read())
        text = removeStopWords(text, stopwordsList)

        for word in text:
            if len(wn.synsets(word)) > 0:
                if 'a' is wn.synsets(word)[0].pos():
                    rating = file[0:2]
                    if "F" in file:
                        avgFemaleRating += float(rating)
                        totalFemales += 1
                        if(float(rating) <= 2.5):
                            append(word, femaleLowDic)
                        else:
                            append(word, femaleHighDic)
                        # Add to female ratings array
                        femaleRatings.append(rating)

                    else:
                        avgMaleRating += float(rating)
                        totalMales += 1
                        if(float(file[0:2]) <= 2.5):
                            append(word, maleLowDic)
                        else:
                            append(word, maleHighDic)
                        # Add to male ratings array
                        maleRatings.append(rating)
    print("Low rated F\n")
    printDescendingDict(femaleLowDic)
    print("\nHigh rated F\n")
    printDescendingDict(femaleHighDic)
    print("\nLow rated M\n")
    printDescendingDict(maleLowDic)
    print("\nHigh rated M\n")
    printDescendingDict(maleHighDic)
    avgFemaleRating = avgFemaleRating / float(totalFemales)
    avgMaleRating = avgMaleRating / float(totalMales)
    print("\nAverage female rating " + str(avgFemaleRating))
    print("\nAverage male rating " + str(avgMaleRating))
    
    # Write ratings to CSV for calculating paired t-test
    write_ratings_to_CSV(maleRatings, femaleRatings)
    
def append(word, Dict):
    if word in Dict:
        Dict[word] += 1
    else:
        Dict[word] = 1


def printDescendingDict(Dict):
    count = 0
    for item in sorted(Dict, key=Dict.get, reverse=True):
        print(str(item) + " " + str(Dict[item]))
        count +=1
        if count is 10:
            return

def removeStopWords(tokenList, stopWordDict):
    newTokenList = []
    for token in tokenList:
        token = token.lower()
        if token not in stopWordDict and token != "":
            newTokenList.append(token)
    return newTokenList


def createStopwordsList():
    """Function to create stopwords list."""
    stopwordsList = {}
    stopwordsFile = open('stopwords', 'r')
    for word in stopwordsFile:
        word = word.rstrip()
        stopwordsList[word] = 1
    return stopwordsList

def write_ratings_to_CSV(male_arr, female_arr):

    if os.path.exists("prof_ratings.csv"):
        os.remove("prof_ratings.csv")

    with open('prof_ratings.csv', mode='w') as ratings_file:
        ratings_writer = csv.writer(ratings_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        ratings_writer.writerow(['Male Prof Rating', 'Female Prof Rating'])
        
        print('Male arr length' + str(len(male_arr)))
        print('Female arr length' + str(len(female_arr)))
        for i in range(len(male_arr)):
            ratings_writer.writerow([male_arr[i], female_arr[i]])

if __name__ == "__main__":
    main()
