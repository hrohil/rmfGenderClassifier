import sys
import os
import math







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
		classProbabilities['female'] = math.log(float(98)/float(195), 10)
		classProbabilities['male'] = math.log(float(97)/float(195), 10)

	# Create word probabilities for each class
	lieWords = {}
	truthWords = {}
	wordProbabilities.append(lieWords)
	wordProbabilities.append(truthWords)

	# Create all word probabilities for each class
	lieCounter = 0
	truthCounter = 0
	totalUniqueVocab = 0
	for file in allFiles:
		if file != omitFile:
			currentContent = allFiles[file]
			if 'lie' in file:
				for word in currentContent.split():
					lieCounter += 1
					word = tokenizeText(word)[0]
					if word in wordProbabilities[0]:
						wordProbabilities[0][word] += 1
					else:
						wordProbabilities[0][word] = 1
						if word not in wordProbabilities[1]:
							totalUniqueVocab += 1
			else:
				for word in currentContent.split():
					truthCounter += 1
					word = tokenizeText(word)[0]
					if word in wordProbabilities[1]:
						wordProbabilities[1][word] += 1
					else:
						wordProbabilities[1][word] = 1
						if word not in wordProbabilities[0]:
							totalUniqueVocab += 1

	# Calculate lie probabilities
	for word in wordProbabilities[0]:
		occurrence = wordProbabilities[0][word]
		prob = float(float(occurrence + 1) / float(lieCounter + totalUniqueVocab))
		wordProbabilities[0][word] = math.log(prob, 10)

	# Calculate truth probabilities
	for word in wordProbabilities[1]:
		occurrence = wordProbabilities[1][word]
		prob = float(float(occurrence + 1) / float(truthCounter + totalUniqueVocab))
		wordProbabilities[1][word] = math.log(prob, 10)

	return classProbabilities, wordProbabilities, totalUniqueVocab, lieCounter, truthCounter