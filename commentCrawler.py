import selenium
from selenium import webdriver
from bs4 import BeautifulSoup
import time

# teachers is a dictionary of dictionaries, mapping teacher id to teacher name, comments, and gender
teachers = {}
teacherIdsList = []

def main():
	outfile = open("commentCrawler.output", "w")

	# count number of reviews for male and female teachers
	femaleReviews = 0
	maleReviews = 0

	exitedWithError = False
	driver = webdriver.Chrome()

	driver.set_page_load_timeout(30)
	urls = ["http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=University+of+Michigan&schoolID=1258&queryoption=TEACHER",
	"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Central+Michigan+University&schoolID=200&queryoption=TEACHER", 
	"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Michigan+State+University&schoolID=601&queryoption=TEACHER", ]
	
	for url in urls:
		getTeacherNames(driver, url)
	for teacherId in teacherIdsList:
		# if page doesn't load in 30 seconds, close window and retry
		if exitedWithError: 
			driver = webdriver.Chrome()
			driver.set_page_load_timeout(30)
			time.sleep(5)
		exitedWithError = getTeacherComments(driver, teacherId)
		if "gender" in teachers[teacherId]:
			print(teachers[teacherId]["name"] + " " + teachers[teacherId]["gender"])
			if teachers[teacherId]["gender"] == "female":
				femaleReviews += len(teachers[teacherId]["comments"])
			elif teachers[teacherId]["gender"] == "male":
				maleReviews += len(teachers[teacherId]["comments"])
		
	print("number of female reviews: " + str(femaleReviews))
	print("number of male reviews: " + str(maleReviews))

	for teacherId in teachers:
		outfile.write("Teacher name: " + teachers[teacherId]["name"] + "\n")
		outfile.write("Teacher gender: " + teachers[teacherId]["gender"] + "\n")
		outfile.write("Teacher comments: \n")
		for comment in teachers[teacherId]["comments"]:
			outfile.write(str(comment) + "\n")

	driver.close()

def getTeacherNames(driver, url):
	teacherListElement = " "
	try:
		driver.get(url)
		teacherListElement = driver.find_elements_by_class_name('result-list')
	except:
		print("timeout")
		urls.append(url)
	if teacherListElement != " ":
		# get html text that includes teacher ids
		htmlText = teacherListElement[1].get_attribute('innerHTML')
		soup = BeautifulSoup(htmlText, 'html.parser')
		divs = soup.find_all("li")
		# get teacher ids and names
		for li in divs:
			li = str(li)
			# find end index of teacher id, start index is 21
			end = li.find('"', 21)
			teacherId = li[21:end]
			nameStart = li.find("name") + 6
			end = li.find(" ", nameStart)
			teacherLastName = li[nameStart:end]
			lastNameEnd = li.find(" ", end + 1)
			teacherFirstName = li[end:lastNameEnd]
			fullname = teacherLastName + teacherFirstName
			beginSpamIndex = fullname.find("<")
			fullname = fullname[:beginSpamIndex].strip()

			teachers[teacherId] = {}
			teachers[teacherId]["name"] = fullname
			teacherIdsList.append(teacherId)


def getTeacherComments(driver, teacherId):
	url = "http://www.ratemyprofessors.com/ShowRatings.jsp?tid=" + teacherId + "&showMyProfs=true"
	commentsElement = " "
	try:
		driver.get(url)
		commentsElement = driver.find_elements_by_class_name('commentsParagraph')
	# if timeout, add teacherId to back of list to revisit
	except selenium.common.exceptions.TimeoutException:
		print("timeout")
		driver.close()
		teacherIdsList.append(teacherId)
		return True
	if commentsElement != " ":
		maleCount = 0
		femaleCount = 0

		# identify gender based on pronouns
		for element in commentsElement:
			comment = element.get_attribute('innerHTML').strip()
			if comment.find(" his") != -1:
				maleCount += 1
			if comment.find(" her ") != -1:
				femaleCount += 1

			# add comments to teachers
			if "comments" not in teachers[teacherId]:
				teachers[teacherId]["comments"] = [comment]
			else:
				teachers[teacherId]["comments"].append(comment)
		if maleCount > femaleCount:
			teachers[teacherId]["gender"] = "male"
		elif femaleCount > maleCount:
			teachers[teacherId]["gender"] = "female"

		# if we can't determine gender, remove from dict
		else:
			teachers.pop(teacherId, None)

		time.sleep(5)
		return False

if __name__ == "__main__":
	main()

