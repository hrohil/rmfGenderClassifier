from bs4 import BeautifulSoup
import urllib
import re
import queue
import sys

def main():
    #seed url file
    file = sys.argv[1]

    #file with seed URLS
    seedFile = open(file,"r").read()

    #when count is 51 or more, gender switches to Female, total 100 professors(50 M and 50 F)
    count = 1

    for seedURL in seedFile.split():
        reviewFinder(seedURL, count)
        count += 1

def reviewFinder(url, count):
    #assign gender according to count
    if count < 51:
        gender = "Male"
    else:
        gender = "Female"

    #open a file to put output data in
    outFile = open("training.data/" + gender + str(count) + ".data","w+")

    html_page = urllib.request.urlopen(url)
    soup = BeautifulSoup(html_page)
    for review in soup.findAll("p", class_ = "commentsParagraph"):
        #gets only the text part of each review and writes it to an output files
        review = review.get_text()
        outFile.write(review)

if __name__ == "__main__":
    main()