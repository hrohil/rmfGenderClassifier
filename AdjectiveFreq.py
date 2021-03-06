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

    maleDict = {}
    femaleDict = {}
    male_female_diff_dict = {}
    female_male_diff_dict = {}

    femaleRatings = []
    maleRatings = []

    for file in os.listdir("commentCrawlerOutputPreprocessed"):
        text = word_tokenize(
            open("commentCrawlerOutputPreprocessed/" + file).read())
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

                        append(word, femaleDict)
                        # Add to female ratings array
                        femaleRatings.append(rating)

                    else:
                        avgMaleRating += float(rating)
                        totalMales += 1
                        if(float(file[0:2]) <= 2.5):
                            append(word, maleLowDic)
                        else:
                            append(word, maleHighDic)

                        append(word, maleDict)
                        # Add to male ratings array
                        maleRatings.append(rating)

    maleDict = normalizeDict(maleDict)
    normMaleHighDict = normalizeDict(maleHighDic)
    normMaleLowDict = normalizeDict(maleLowDic)
    femaleDict = normalizeDict(femaleDict)
    normFemaleHighDict = normalizeDict(femaleHighDic)
    normFemaleLowDict = normalizeDict(femaleLowDic)

    # Make data from these dicts
    male_female_diff_dict = populateDifferenceDict(maleDict, femaleDict)
    female_male_diff_dict = populateDifferenceDict(femaleDict, maleDict)
    low_male_low_female_diff_dict = populateDifferenceDict(
        normMaleLowDict, normFemaleLowDict)
    low_female_low_male_diff_dict = populateDifferenceDict(
        normFemaleLowDict, normMaleLowDict)
    high_male_high_female_diff_dict = populateDifferenceDict(
        normMaleHighDict, normFemaleHighDict)
    high_female_high_male_diff_dict = populateDifferenceDict(
        normFemaleHighDict, normMaleHighDict)

    print('\n')
    print("Words used to describe males more than females\n")
    printDescendingDict(male_female_diff_dict)
    print("\nWords used to describe females more than males\n")
    printDescendingDict(female_male_diff_dict)
    print("\nWords used to describe low rated females more than low rated males\n")
    printDescendingDict(low_female_low_male_diff_dict)
    print("\nWords used to describe low rated males more than low rated females\n")
    printDescendingDict(low_male_low_female_diff_dict)
    print("\nWords used to describe high rated females more than high rated males\n")
    printDescendingDict(high_female_high_male_diff_dict)
    print("\nWords used to describe high rated males more than high rated females\n")
    printDescendingDict(high_male_high_female_diff_dict)

    print("\nLow rated F\n")
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


def normalizeDict(a):
    new_dict = a.copy()
    max_freq = 0
    for key, value in new_dict.items():
        if value > max_freq:
            max_freq = value

    for key, value in new_dict.items():
        new_dict[key] = value / max_freq

    return new_dict


def populateDifferenceDict(a, b):
    difference_dict = {}

    for key in a:
        to_subtract = 0
        if key in b:
            to_subtract = b[key]

        difference_dict[key] = a[key] - to_subtract

    return difference_dict


def append(word, Dict):
    if word in Dict:
        Dict[word] += 1
    else:
        Dict[word] = 1


def printDescendingDict(Dict, top=10):
    count = 0
    for item in sorted(Dict, key=Dict.get, reverse=True):
        print(str(item) + " " + str(Dict[item]))
        count += 1
        if count == top:
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
        ratings_writer = csv.writer(
            ratings_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        ratings_writer.writerow(['Male Prof Rating', 'Female Prof Rating'])

        print('Male arr length' + str(len(male_arr)))
        print('Female arr length' + str(len(female_arr)))
        for i in range(len(male_arr)):
            ratings_writer.writerow([male_arr[i], female_arr[i]])


def write_weighted_ratings_to_CSV(male_dict, female_dict):
    sorted_male_dict = sorted(male_dict, key=Dict.get, reverse=True)
    sorted_female_dict = sorted(female_dict, key=Dict.get, reverse=True)

if __name__ == "__main__":
    main()
