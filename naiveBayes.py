import sys
import os
import math
import pdb

female = "female"
male = "male"
allFemaleFiles = []
allMaleFiles = []
# Top words for female and male boosting (weighting of terms)
femaleBoosterWords = ["unclear", "other", "harder", "useless", "unfair", "pointless", "hot", "similar", "honest", "big", "careless", "random", "slower", "sweetest", "faster"]
maleBoosterWords = ["just", "sure", "actual", "easier", "late", "most", "stronger", "easiest", "obvious", "worthless", "sad", "incorrect", "smartest", "strong", "linear"]
booster = 7


def main():
	filesFolder = sys.argv[1]
	allFiles = {}
	allFiles, allFemaleFile, allMaleFile = createFileStructures(filesFolder)
	accurateResult = 0
	averageWordProbsFemale = {}
	averageWordProbsMale= {}
	o = open("naivebayes.output", "w")
	# Run the training/testing on all female data files
	counter = 0
	for curTestFile in allFemaleFile:
		curClassProbs = {}
		curWordProbs = {}
		curClassProbs, curWordProbs, totalUniqueVocab, femaleCounter, maleCounter = trainNaiveBayes(allFiles, curTestFile)
		result = testNaiveBayes(allFiles, curTestFile, curClassProbs, curWordProbs, totalUniqueVocab, femaleCounter, maleCounter)
		# Capture the word probability for each word to know top probabilities
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
		# If result is correct, add one accuracy
		if result == female:
			accurateResult += 1
	# Run the training/testing on all male data files
	for curTestFile in allMaleFile:
		curClassProbs = {}
		curWordProbs = {}
		curClassProbs, curWordProbs, totalUniqueVocab, femaleCounter, maleCounter = trainNaiveBayes(allFiles, curTestFile)
		result = testNaiveBayes(allFiles, curTestFile, curClassProbs, curWordProbs, totalUniqueVocab, femaleCounter, maleCounter)
		# Capture the word probability for each word to know top probabilities
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
		# If result is correct, add one accuracy
		if result == male:
			accurateResult += 1

	#Calculate the average top 10 words across all training sets
	for word in averageWordProbsFemale:
		averageWordProbsFemale[word] = float(averageWordProbsFemale[word]) / float(len(allFemaleFile))
	for word in averageWordProbsMale:
		averageWordProbsMale[word] = float(averageWordProbsMale[word]) / float(len(allMaleFile))
	
	print("Female Class Top 10 Words")
	find10TopWords(averageWordProbsFemale)
	print("Male Class Top 10 Words")
	find10TopWords(averageWordProbsMale)

	accuracy = float(accurateResult) / float(len(allFemaleFile) + len(allMaleFile))
	print("Booster level: " + str(booster))
	print("Accuracy: " + str(accuracy))



def createFileStructures(folder):
	"""Input name of folder. Output dictionary of all files' content for use later on."""
	allFiles = {}

	for filename in os.listdir(folder):
		with open(os.path.join(folder, filename)) as content:
			allFiles.update( {filename : content.read()} )
			if 'F' in filename:
				allFemaleFiles.append(filename)
			else:
				allMaleFiles.append(filename)
	allFemaleFiles.sort()
	allMaleFiles.sort()

	newFemaleFiles = ['']*103
	newMalesFiles = ['']*103
	for i in range(0, 103):
		newFemaleFiles[i] = allFemaleFiles[i]
		newMalesFiles[i] = allMaleFiles[i]

	return allFiles, newFemaleFiles, newMalesFiles


def trainNaiveBayes(allFiles, omitFile):
	"""Function to train files using NB Classifier."""
	classProbabilities = {}
	wordProbabilities = []

	# Create class probabilities depending on the file you're omitting
	if 'F' in omitFile:
		classProbabilities[female] = math.log(float(len(allFemaleFiles)/2 - 1)/float(len(allFemaleFiles)/2 + len(allMaleFiles)/2), 10)
		classProbabilities[male] = math.log(float(len(allMaleFiles)/2)/float(len(allFemaleFiles)/2 + len(allMaleFiles)/2), 10)
	else:
		classProbabilities[female] = math.log(float(len(allFemaleFiles)/2)/float(len(allFemaleFiles)/2 + len(allMaleFiles)/2), 10)
		classProbabilities[male] = math.log(float(len(allMaleFiles)/2 - 1)/float(len(allFemaleFiles)/2 + len(allMaleFiles)/2), 10)

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
			# Looking at all female class
			if 'F' in file:
				for word in currentContent.split():
					femaleCounter += 1
					if word in wordProbabilities[0]:
						# Checking to see if the word is a booster word
						if word in femaleBoosterWords:
							wordProbabilities[0][word] += booster
						else:
							wordProbabilities[0][word] += 1
					else:
						# Checking to see if the word is a booster word
						if word in femaleBoosterWords:
							wordProbabilities[0][word] = booster
						else:
							wordProbabilities[0][word] = 1
						if word not in wordProbabilities[1]:
							totalUniqueVocab += 1
			# Looking at the male class
			else:
				for word in currentContent.split():
					maleCounter += 1
					if word in wordProbabilities[1]:
						# Checking to see if the word is a booster word
						if word in maleBoosterWords:
							wordProbabilities[1][word] += booster
						else:
							wordProbabilities[1][word] += 1
					else:
						# Checking to see if the word is a booster word
						if word in maleBoosterWords:
							wordProbabilities[1][word] = booster
						else:
							wordProbabilities[1][word] = 1
						if word not in wordProbabilities[0]:
							totalUniqueVocab += 1

	# Calculate female probabilities
	for word in wordProbabilities[0]:
		occurrence = wordProbabilities[0][word]
		prob = float(float(occurrence + 1) / float(femaleCounter + totalUniqueVocab))
		wordProbabilities[0][word] = math.log(prob, 10)

	# Calculate male probabilities
	for word in wordProbabilities[1]:
		occurrence = wordProbabilities[1][word]
		prob = float(float(occurrence + 1) / float(maleCounter + totalUniqueVocab))
		wordProbabilities[1][word] = math.log(prob, 10)

	return classProbabilities, wordProbabilities, totalUniqueVocab, femaleCounter, maleCounter

def testNaiveBayes(allFiles, testFile, curClassProbs, curWordProbs, totalUniqueVocab, femaleCounter, maleCounter):
	# Testing naive bayes function
	femaleProb = curClassProbs[female]
	maleProb = curClassProbs[male]
	# Constant probabilities if word doesn't occur in a certain category (female, male)
	constantNoAppearanceProbFemale = math.log((float(1)/float(totalUniqueVocab + femaleCounter)), 10)
	constantNoAppearanceProbMale = math.log((float(1)/float(totalUniqueVocab + maleCounter)), 10)
	# Checks if the word occurs in each respective category (female, male) and adds the probability accordingly
	for word in allFiles[testFile].split():
		if word in curWordProbs[0]:
			femaleProb += curWordProbs[0][word]
		else:
			femaleProb += constantNoAppearanceProbFemale
		if word in curWordProbs[1]:
			maleProb += curWordProbs[1][word]
		else:
			maleProb += constantNoAppearanceProbMale
	if femaleProb > maleProb:
		return female
	else:
		return male

def find10TopWords(curWordProbs):
	# Get the top 10 probabilities of words by category
	counter = 0
	for key in sorted(curWordProbs, key=curWordProbs.get, reverse=True):
		if counter < 10:
			print(str(key) + " " + str(curWordProbs[key]))
			counter += 1


if __name__ == "__main__":
	main()







