import nltk
nltk.download('wordnet')
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize
import os

def main():
    stopwordsList = createStopwordsList()

    maleLowDic = {}
    maleHighDic = {}
    femaleLowDic = {}
    femaleHighDic = {}

    for file in os.listdir("commentCrawlerOutput"):
        text = word_tokenize(open("commentCrawlerOutput/" +  file).read())
        text = removeStopWords(text, stopwordsList)

        for word in text:
            if len(wn.synsets(word)) > 0:
                if 'a' is wn.synsets(word)[0].pos() or 'v' is wn.synsets(word)[0].pos():
                    if "F" in file:
                        if(float(file[0:2]) <= 2.5):
                            append(word, femaleLowDic)
                        else:
                            append(word, femaleHighDic)
                    else:
                        if(float(file[0:2]) <= 2.5):
                            append(word, maleLowDic)
                        else:
                            append(word, maleHighDic)
    print("Low rated F\n")
    printDescendingDict(femaleLowDic)
    print("\nHigh rated F\n")
    printDescendingDict(femaleHighDic)
    print("\nLow rated M\n")
    printDescendingDict(maleLowDic)
    print("\nHigh rated M\n")
    printDescendingDict(maleHighDic)
    
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

if __name__ == "__main__":
    main()
