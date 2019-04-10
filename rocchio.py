import os
import math

def indexDoc(doc):
    termFreq = {}
    maxFreq = -1
    #calulate term frequencies and keep a count on max_freq
    for token in doc:
        if token in termFreq:
            termFreq[token] += 1.
            if maxFreq < termFreq[token]:
                maxFreq = termFreq[token]
        else:
            termFreq[token] = 1.
            if maxFreq < termFreq[token]:
                maxFreq = termFreq[token]

    #normalize all term frequencies given max frequencies
    return termFreq, maxFreq

def finalVector(tdf, docWeights):
    finalVector = {}
    for doc in docWeights:
        for word in doc:
            if word in tdf:
                if word in finalVector:
                    finalVector[word] += doc[word] * math.log(291./tdf[word])
                else:
                    finalVector[word] = doc[word] * math.log(291./tdf[word])
    return finalVector

def cosineSimilarty(vector1, vector2):
    numWeight = 0.
    demLength1 = 0.
    demLength2 = 0.
    for term in vector1:
        if term in vector2:
            numWeight += vector1[term]*vector2[term]
        demLength1 = vector1[term]*vector1[term]
    demLength1 = math.sqrt(demLength1)
    for term in vector2:
        demLength2 = vector2[term]*vector2[term]
    demLength2 = math.sqrt(demLength2)
    return (numWeight)/(demLength1*demLength2)

def main():
    #get a list of files in dataset
    fileList = []
    for file in os.listdir("preprocessedData"):
        fileList.append("preprocessedData/" + file)

    accuracy = 0
    female_acc = 0
    male_acc = 0
    count = 0
    #train and test over 292 files
    while count < 292:
        #test file
        testFile = fileList[count]
        #lists for training files
        trainList = []
        #for each file in list
        for i in range(len(fileList)):
            #if file is not testFile append to training file list
            if testFile != fileList[i]:
                trainList.append(fileList[i])
        #dictionary that stores term - document freq
        tdf = {}
        #list of dictionaries representing male document term weights
        maleDocumentWeights = []
        #list of dictionaries representing female document term weights
        femaleDocumentWeights = []

        for file in trainList:
            termFreq, maxFreq = indexDoc(open(file).read())
            for term in termFreq:
                termFreq[term] = termFreq[term]/maxFreq
                if term in tdf:
                    tdf[term] += 1.
                else:
                    tdf[term] = 1.
            if "female" in file:
                femaleDocumentWeights.append(termFreq)
            else:
                maleDocumentWeights.append(termFreq)

        maleFinalVector = finalVector(tdf, maleDocumentWeights)
        femaleFinalVector = finalVector(tdf, femaleDocumentWeights)

        testFreq, maxFreq = indexDoc(testFile)
        for term in termFreq:
            termFreq[term] = termFreq[term]/maxFreq
            if term in tdf:
                tdf[term] += 1.
            else:
                tdf[term] = 1.

        testList = []
        testList.append(testFreq)
        testVector = finalVector(tdf, testList)

        maleSim = cosineSimilarty(testVector, maleFinalVector)
        femaleSim = cosineSimilarty(testVector, femaleFinalVector)

        
        if femaleSim >= maleSim and "female" in testFile:
            accuracy += 1.
            female_acc += 1
        if maleSim > femaleSim and "female" not in testFile: 
            accuracy += 1.
            male_acc += 1



        count += 1
    print(accuracy/292)
    print(str(female_acc) + " " + str(male_acc))





if __name__ == "__main__":
    main()