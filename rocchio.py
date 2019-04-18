import os
import math

def indexDoc(doc):
    termFreq = {}
    maxFreq = -1
    #calulate term frequencies and keep a count on max_freq
    for token in doc:
        if token in termFreq:
            termFreq[token] += 7.
            if maxFreq < termFreq[token]:
                maxFreq = termFreq[token]
        else:
            termFreq[token] = 7.
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
        demLength1 += vector1[term]*vector1[term]
    demLength1 += math.sqrt(demLength1)
    for term in vector2:
        demLength2 += vector2[term]*vector2[term]
    demLength2 += math.sqrt(demLength2)
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
            if i is not count:
                trainList.append(fileList[i])
        #dictionary that stores term - document freq
        tdf = {}
        #list of dictionaries representing male document term weights
        maleDocumentWeights = []
        #list of dictionaries representing female document term weights
        femaleDocumentWeights = []

        #for each training file, calculate its term weights as well update tdf
        for file in trainList:
            termFreq, maxFreq = indexDoc(open(file).read())
            for term in termFreq:
                termFreq[term] = termFreq[term]/maxFreq
                if term in tdf:
                    tdf[term] += 1.
                else:
                    tdf[term] = 1.
            #add male and female doc weights into separate lists
            if "female" in file:
                femaleDocumentWeights.append(termFreq)
            else:
                maleDocumentWeights.append(termFreq)
        
        #calculate final vectors for male and female given all male doc weights and female doc weights
        maleFinalVector = finalVector(tdf, maleDocumentWeights)
        femaleFinalVector = finalVector(tdf, femaleDocumentWeights)

        #calculate term weights for test file and update tdf
        testFreq, maxFreq = indexDoc(testFile)
        for term in termFreq:
            termFreq[term] = termFreq[term]/maxFreq
            if term in tdf:
                tdf[term] += 1.
            else:
                tdf[term] = 1.

        #calculate the final vector for test file
        testList = []
        testList.append(testFreq)
        testVector = finalVector(tdf, testList)

        #calculate cosine similarity given male and female vector
        maleSim = cosineSimilarty(testVector, maleFinalVector)
        femaleSim = cosineSimilarty(testVector, femaleFinalVector)
        
        #calculate total accuracy as well as categorical accuracy
        if femaleSim >= maleSim and "female" in testFile:
            accuracy += 1.
            female_acc += 1
        if maleSim > femaleSim and "female" not in testFile: 
            accuracy += 1.
            male_acc += 1



        count += 1
    print("Accuracy: "  + str(accuracy/292))
    print("Female accuracy: " + str(female_acc/146.) + " Male accuracy: " + str(male_acc/146.))





if __name__ == "__main__":
    main()