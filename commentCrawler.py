import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import os

# teachers is a dictionary of dictionaries, mapping teacher id to teacher name, comments, and gender
teachers = {}
teacherIdsList = []

def main():
	if(not os.path.isdir(os.getcwd() + "/commentCrawlerOutput")):
		os.mkdir("commentCrawlerOutput")
	os.chdir(os.getcwd() + "/commentCrawlerOutput")
	print(os.getcwd())

	# count number of reviews for male and female teachers
	femaleReviews = 0
	maleReviews = 0

	exitedWithError = False
	driver = webdriver.Chrome()

	driver.set_page_load_timeout(30)

	urlsByRegion = {}
	urlsByRegion["west"] = ["http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Stanford+University&schoolID=953&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=California+Institute+of+Technology&schoolID=148&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=University+of+California+Berkeley&schoolID=1072&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Pomona+College&schoolID=774&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Harvey+Mudd+College&schoolID=400&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Claremont+McKenna+College&schoolID=234&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=University+of+Southern+California&schoolID=1381&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=United+States+Air+Force+Academy&schoolID=1049&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=University+of+California+Los+Angeles+%28UCLA%29&schoolID=1075&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Scripps+College&schoolID=889&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Pitzer+College&schoolID=768&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=University+of+Washington&schoolID=1530&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Santa+Clara+University&schoolID=882&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=University+of+California+San+Diego&schoolID=1079&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Whitman+College&schoolID=1194&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Colorado+College&schoolID=273&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=University+of+California+Santa+Barbara&schoolID=1077&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Brigham+Young+University&schoolID=135&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Reedley+College&schoolID=2731&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=University+of+Colorado+-+Boulder&schoolID=1087&queryoption=TEACHER"]

	urlsByRegion["east"] = ["http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Massachusetts+Institute+of+Technology&schoolID=580&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Harvard+University&schoolID=399&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Yale+University&schoolID=1222&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Princeton+University&schoolID=780&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=University+of+Pennsylvania&schoolID=1275&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Columbia+University&schoolID=278&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Brown+University&schoolID=137&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Bowdoin+College&schoolID=125&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Dartmouth+College&schoolID=1339&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Cornell+University&schoolID=298&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Georgetown+University&schoolID=355&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Amherst+College&schoolID=33&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Tufts+University&schoolID=1040&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Johns+Hopkins+University&schoolID=464&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Swarthmore+College&schoolID=990&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Wellesley+College&schoolID=1156&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Bates+College&schoolID=87&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=New+York+University&schoolID=675&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Wesleyan+University&schoolID=1161&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Boston+University&schoolID=124&queryoption=TEACHER"]

	urlsByRegion["south"] = ["http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Duke+University&schoolID=1350&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Rice+University&schoolID=799&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Vanderbilt+University&schoolID=4002&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Emory+University&schoolID=340&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=University+of+Virginia&schoolID=1277&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Washington+and+Lee+University&schoolID=1139&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Georgia+Institute+of+Technology&schoolID=361&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=University+of+North+Carolina+at+Chapel+Hill&schoolID=1232&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Wake+Forest+University&schoolID=1130&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Virginia+Tech&schoolID=1349&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=University+of+Texas+at+Austin&schoolID=1255&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=University+of+Florida&schoolID=1100&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=University+of+Richmond&schoolID=4102&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Tulane+University&schoolID=1041&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Clemson+University&schoolID=242&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Trinity+University&schoolID=1033&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Auburn+University&schoolID=60&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Sewanee%3A+The+University+of+the+South&schoolID=4582&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Mississippi+State+University&schoolID=617&queryoption=TEACHER",
							"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Texas+Tech+University&schoolID=1011&queryoption=TEACHER"]

	urlsByRegion["midwest"] = ["http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=University+of+Chicago&schoolID=1085&queryoption=TEACHER",
								"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Northwestern+University&schoolID=709&queryoption=TEACHER",
								"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=University+of+Notre+Dame&schoolID=1576&queryoption=TEACHER",
								"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Carleton+College&schoolID=179&queryoption=TEACHER",
								"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Kenyon+College&schoolID=486&queryoption=TEACHER",
								"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=University+Of+Illinois+at+Urbana+-+Champaign&schoolID=1112&queryoption=TEACHER",
								"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Grinnell+College&schoolID=383&queryoption=TEACHER",
								"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Oberlin+College&schoolID=718&queryoption=TEACHER",
								"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=University+of+Wisconsin+-+Madison&schoolID=1256&queryoption=TEACHER",
								"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Macalester+College&schoolID=550&queryoption=TEACHER",
								"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Case+Western+Reserve+University&schoolID=186&queryoption=TEACHER",
								"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=DePauw+University&schoolID=1523&queryoption=TEACHER",
								"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=St.+Olaf+College&schoolID=862&queryoption=TEACHER",
								"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Wheaton+College&schoolID=1191&queryoption=TEACHER",
								"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=The+Ohio+State+University&schoolID=724&queryoption=TEACHER",
								"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Purdue+University+-+West+Lafayette&schoolID=783&queryoption=TEACHER",
								"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Denison+University&schoolID=4119&queryoption=TEACHER",
								"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Indiana+University+Bloomington&schoolID=440&queryoption=TEACHER",
								"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Michigan+State+University&schoolID=601&queryoption=TEACHER",
								"http://www.ratemyprofessors.com/search.jsp?queryBy=schoolId&schoolName=Kalamazoo+College&schoolID=474&queryoption=TEACHER"]

	
	for region in urlsByRegion:							
		for url in urlsByRegion[region]:
			getTeacherNames(driver, url)
		for teacherId in teacherIdsList:
			teachers[teacherId]["region"] = region
			# if page doesn't load in 30 seconds, close window and retry
			if exitedWithError: 
				driver = webdriver.Chrome()
				driver.set_page_load_timeout(30)
				time.sleep(5)
			exitedWithError = getTeacherComments(driver, teacherId)
			try:
				if "gender" in teachers[teacherId] and teacherId in teachers:
					print(teachers[teacherId]["name"] + " " + teachers[teacherId]["gender"])
					if teachers[teacherId]["gender"] == "F":
						femaleReviews += len(teachers[teacherId]["comments"])
					elif teachers[teacherId]["gender"] == "M":
						maleReviews += len(teachers[teacherId]["comments"])

			except Exception as e:
				print(e)
			continue
		teacherIdsList.clear()
		
	print("number of female reviews: " + str(femaleReviews))
	print("number of male reviews: " + str(maleReviews))
	
	maleCounter = 1
	femaleCounter = 1
	for teacherId in teachers:
		if teachers[teacherId]["gender"] == "M":
			printData(teacherId, maleCounter)
			maleCounter += 1
		else:
			printData(teacherId, femaleCounter)
			femaleCounter += 1

	driver.close()

def printData(teacherId, counter):
		filename = str(teachers[teacherId]["rating"]) + str(teachers[teacherId]["gender"]) + str(counter)
		outfile = open(filename, "w")
		for comment in teachers[teacherId]["comments"]:
			outfile.write(str(comment) + "\n")



def getTeacherNames(driver, url):
	teacherListElement = " "
	try:
		driver.get(url)
		inputElement = driver.find_element_by_id("professor-name")
		inputElement.send_keys("Computer Science")
		inputElement.send_keys(Keys.ENTER)
		time.sleep(2)
		teacherListElement = driver.find_elements_by_class_name('result-list')
		schoolName = driver.find_element_by_class_name('school-name')
	except Exception as e:
		print("timeout")
		print(e)
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
			print(str(schoolName.get_attribute('innerHTML')))
			teachers[teacherId]["school"] = str(schoolName.get_attribute('innerHTML'))
			teacherIdsList.append(teacherId)


def getTeacherComments(driver, teacherId):
	url = "http://www.ratemyprofessors.com/ShowRatings.jsp?tid=" + teacherId + "&showMyProfs=true"
	commentsElement = " "
	try:
		driver.get(url)
		commentsElement = driver.find_elements_by_class_name('commentsParagraph')
		gradeElement = driver.find_element_by_class_name("grade")
	# if timeout, add teacherId to back of list to revisit
	except selenium.common.exceptions.TimeoutException:
		print("timeout")
		driver.close()
		teacherIdsList.append(teacherId)
		return True
	if commentsElement != " ":
		maleCount = 0
		femaleCount = 0

		teachers[teacherId]["rating"] = gradeElement.get_attribute("innerHTML")
		print(teachers[teacherId]["rating"])
		# identify gender based on pronouns
		for element in commentsElement:
			comment = element.get_attribute('innerHTML').strip()
			if comment.find(" his ") != -1:
				maleCount += 1
			if comment.find(" he ") != -1:
				maleCount += 1
			if comment.find(" her ") != -1:
				femaleCount += 1
			if comment.find(" she ") != -1:
				femaleCount += 1

			# add comments to teachers
			if "comments" not in teachers[teacherId]:
				teachers[teacherId]["comments"] = [comment]
			else:
				teachers[teacherId]["comments"].append(comment)
		if maleCount > femaleCount:
			teachers[teacherId]["gender"] = "M"
		elif femaleCount > maleCount:
			teachers[teacherId]["gender"] = "F"

		# if we can't determine gender, remove from dict
		else:
			teachers.pop(teacherId, None)

		time.sleep(5)
		return False

if __name__ == "__main__":
	main()

