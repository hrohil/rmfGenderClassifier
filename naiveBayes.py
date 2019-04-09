import sys
import os
import math


def main():
	filesFolder = sys.argv[1]
	allFiles = {}
	allFiles = createFileStructures(filesFolder)
	accurateResult = 0
	averageWordProbsFemale = {}
	averageWordProbsMale= {}
	o = open("naivebayes.output", "w")
	for i in range(0, 146):
		curTestFile = 'female' + str(i) + '.txt'
		curClassProbs = {}
		curWordProbs = {}
		curClassProbs, curWordProbs, totalUniqueVocab, femaleCounter, maleCounter = trainNaiveBayes(allFiles, curTestFile)
		result = testNaiveBayes(allFiles, curTestFile, curClassProbs, curWordProbs, totalUniqueVocab, femaleCounter, maleCounter)
		for word in curWordProbs[0]:
			if word in averageWordProbsFemale:
				averageWordProbsFemale[word] += float(curWordProbs[0][word])
			else:
				averageWordProbsFemale[word] = float(curWordProbs[0][word])
		for word in curWordProbs[1]:
			if word in averageWordProbsMale:
				averageWordProbsMale[word] += float(curWordProbs[1][word])
			else:
				averageWordProbsMale[word] = float(curWordProbs[1][word])
		o.write(str(curTestFile) + " " + result + '\n')
		if result == "female":
			accurateResult += 1

	for i in range(0, 146):
		curTestFile = 'male' + str(i) + '.txt'
		curClassProbs = {}
		curWordProbs = {}
		curClassProbs, curWordProbs, totalUniqueVocab, femaleCounter, maleCounter = trainNaiveBayes(allFiles, curTestFile)
		result = testNaiveBayes(allFiles, curTestFile, curClassProbs, curWordProbs, totalUniqueVocab, femaleCounter, maleCounter)
		for word in curWordProbs[0]:
			if word in averageWordProbsFemale:
				averageWordProbsFemale[word] += float(curWordProbs[0][word])
			else:
				averageWordProbsFemale[word] = float(curWordProbs[0][word])
		for word in curWordProbs[1]:
			if word in averageWordProbsMale:
				averageWordProbsMale[word] += float(curWordProbs[1][word])
			else:
				averageWordProbsMale[word] = float(curWordProbs[1][word])
		o.write(str(curTestFile) + " " + result + '\n')
		if result == "male":
			accurateResult += 1

	#I have calculated the average top 10 words across all training sets
	for word in averageWordProbsFemale:
		averageWordProbsFemale[word] = float(averageWordProbsFemale[word]) / float(292)
	for word in averageWordProbsMale:
		averageWordProbsMale[word] = float(averageWordProbsMale[word]) / float(292)
	
	print("Female Class Top 10 Words")
	find10TopWords(averageWordProbsFemale)
	print("Male Class Top 10 Words")
	find10TopWords(averageWordProbsMale)

	accuracy = float(accurateResult) / float(292)
	print("Accuracy: " + str(accuracy))



def createFileStructures(folder):
	"""Input name of folder. Output dictionary of all files' content."""
	allFiles = {}
	for filename in os.listdir(folder):
		with open(os.path.join(folder, filename)) as content:
			allFiles.update( {filename : content.read()} )
		#print allFiles
	return allFiles


def trainNaiveBayes(allFiles, omitFile):
	classProbabilities = {}
	wordProbabilities = []

	# Create class probabilities depending on the file you're omitting
	if 'female' in omitFile:
		classProbabilities['female'] = math.log(float(145)/float(292), 10)
		classProbabilities['male'] = math.log(float(146)/float(292), 10)
	else:
		classProbabilities['female'] = math.log(float(146)/float(292), 10)
		classProbabilities['male'] = math.log(float(145)/float(292), 10)

	# Create word probabilities for each class
	femaleWords = {}
	maleWords = {}
	wordProbabilities.append(femaleWords)
	wordProbabilities.append(maleWords)

	# Create all word probabilities for each class
	femaleCounter = 0
	maleCounter = 0
	totalUniqueVocab = 0
	for file in allFiles:
		if file != omitFile:
			currentContent = allFiles[file]
			if 'female' in file:
				for word in currentContent.split():
					femaleCounter += 1
					if word in wordProbabilities[0]:
						wordProbabilities[0][word] += 1
					else:
						wordProbabilities[0][word] = 1
						if word not in wordProbabilities[1]:
							totalUniqueVocab += 1
			else:
				for word in currentContent.split():
					maleCounter += 1
					if word in wordProbabilities[1]:
						wordProbabilities[1][word] += 1
					else:
						wordProbabilities[1][word] = 1
						if word not in wordProbabilities[0]:
							totalUniqueVocab += 1

	# Calculate lie probabilities
	for word in wordProbabilities[0]:
		occurrence = wordProbabilities[0][word]
		prob = float(float(occurrence + 1) / float(femaleCounter + totalUniqueVocab))
		wordProbabilities[0][word] = math.log(prob, 10)

	# Calculate truth probabilities
	for word in wordProbabilities[1]:
		occurrence = wordProbabilities[1][word]
		prob = float(float(occurrence + 1) / float(maleCounter + totalUniqueVocab))
		wordProbabilities[1][word] = math.log(prob, 10)

	return classProbabilities, wordProbabilities, totalUniqueVocab, femaleCounter, maleCounter

def testNaiveBayes(allFiles, testFile, curClassProbs, curWordProbs, totalUniqueVocab, femaleCounter, maleCounter):
	femaleProb = curClassProbs['female']
	maleProb = curClassProbs['male']
	constantNoAppearanceProbLie = math.log((float(1)/float(totalUniqueVocab + femaleCounter)), 10)
	constantNoAppearanceProbTrue = math.log((float(1)/float(totalUniqueVocab + maleCounter)), 10)
	for word in allFiles[testFile].split():
		if word in curWordProbs[0]:
			femaleProb += curWordProbs[0][word]
		else:
			femaleProb += constantNoAppearanceProbLie
		if word in curWordProbs[1]:
			maleProb += curWordProbs[1][word]
		else:
			maleProb += constantNoAppearanceProbTrue
	if femaleProb > maleProb:
		return "female"
	else:
		return "male"

def find10TopWords(curWordProbs):
	#print curWordProbs
	counter = 0
	for key in sorted(curWordProbs, key=curWordProbs.get, reverse=True):
		if counter < 10:
			print(str(key) + " " + str(curWordProbs[key]))
			counter += 1


if __name__ == "__main__":
	main()







