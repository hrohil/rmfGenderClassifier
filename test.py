import selenium
from selenium import webdriver
from bs4 import BeautifulSoup
import time

# teachers is a dictionary of dictionaries, mapping teacher id to teacher name, comments, and gender
teachers = {}

def main():
	femaleReviews = 0
	maleReviews = 0
	exitedWithError = False
	driver = webdriver.Chrome()
	driver.set_page_load_timeout(30)
	urls = ["http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=University+of+Michigan&schoolID=1258&queryoption=TEACHER", "http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Central+Michigan+University&schoolID=200&queryoption=TEACHER", "http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Michigan+State+University&schoolID=601&queryoption=TEACHER"]
	for url in urls:
		getTeacherNames(driver, url)
	for teacherId in teachers:
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
	print("number of female reviews: " + femaleReviews)
	print("number of male reviews: " + maleReviews)


def getTeacherNames(driver, url):
	try:
		driver.get(url)
	except:
		print("timeout")
	finally:
		# get html text that includes teacher ids
		teacherListElement = driver.find_elements_by_class_name('result-list')
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

def getTeacherComments(driver, teacherId):
	url = "http://www.ratemyprofessors.com/ShowRatings.jsp?tid=" + teacherId + "&showMyProfs=true"
	commentsElement = " "
	try:
		driver.get(url)
		commentsElement = driver.find_elements_by_class_name('commentsParagraph')
	except selenium.common.exceptions.TimeoutException:
		print("timeout")
		driver.close()
		return True
	if commentsElement != " ":
		maleCount = 0
		femaleCount = 0
		for element in commentsElement:
			comment = element.get_attribute('innerHTML').strip()
			if comment.find("his") != -1:
				maleCount += 1
			if comment.find("her") != -1:
				femaleCount += 1
			if "comments" not in teachers[teacherId]:
				teachers[teacherId]["comments"] = [comment]
			else:
				teachers[teacherId]["comments"].append(comment)
		if maleCount > femaleCount:
			teachers[teacherId]["gender"] = "male"
		elif femaleCount > maleCount:
			teachers[teacherId]["gender"] = "female"
		else:
			teachers[teacherId]["gender"] = "N/A"
		time.sleep(5)
		return False

if __name__ == "__main__":
	main()

