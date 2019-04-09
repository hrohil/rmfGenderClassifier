import sys
import os
import pdb


def main():
	# Opens the file that contains all info
	with open("commentCrawler.output", "r") as fullFile:
		femaleCounter = 0
		maleCounter = 0
		for line in fullFile.readlines():
			line = line.strip()
			# Checks the gender of the professor to name the file
			if "Teacher gender:" in line:
				gender = line[16:]
				print gender
				print "here too"
				if gender == "male":
					print "Camer"
					fileName = "allData/" + "male" + str(maleCounter) + ".txt"
					newReview = open(fileName, "w+")
					maleCounter += 1
				if gender == "female":
					print "here too"
					fileName = "allData/" + "female" + str(femaleCounter) + ".txt"
					newReview = open(fileName, "w+")
					femaleCounter += 1
			# Collects each review and writes it to the appropriate file
			if "Teacher name: " not in line:
				if "School name: " not in line:
					if "Teacher gender: " not in line:
						if "Teacher comments:" not in line:
							print line
							newReview.write(line + '\n')




if __name__ == "__main__":
	main()
