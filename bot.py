import getpass
import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

driver = Chrome()

def OpenLinkedin():
	driver.get("https://linkedin.com/login")

def SignIn(usernameValue, passwordValue):
	username = driver.find_element_by_id("username")
	password = driver.find_element_by_id("password")
	signIn = driver.find_element_by_class_name("btn__primary--large")
	username.send_keys(usernameValue)
	password.send_keys(passwordValue)
	signIn.click()

def WaitForClass(nameClass):
	WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, nameClass)))

def GetProfiles(keyword, page):
	url = "https://www.linkedin.com/search/results/people/?keywords=" + keyword + "&page=" + page
	driver.get(url)
	links = []
	driver.implicitly_wait(10)
	driver.execute_script("window.scrollTo(0, 700);")
	time.sleep(1)
	peoples = driver.find_elements_by_xpath("//a[contains(@class, 'search-result__result-link')]")
	try:
		for people in peoples:
			links.append(people.get_attribute("href"))
	except StaleElementReferenceException as Exception:
		time.sleep(1)
		peoples = driver.find_elements_by_xpath("//a[contains(@class, 'search-result__result-link')]")
		for people in peoples:
			links.append(people.get_attribute("href"))
	return (links)

def VisiteProfiles(profiles):
	for i in range (len(profiles) // 2):
		driver.get(profiles[2 * i])
		time.sleep(10)

def main():
	#Get config of the user
	config = open("config", "r")
	lines = config.read().splitlines()
	username = lines[0]
	password = lines[1]
	keyword = lines[2]

	profiles = []
	OpenLinkedin()
	SignIn(username, password)
	for i in range (1, 11):
		profiles += GetProfiles(keyword, str(i))
	VisiteProfiles(profiles)
	driver.quit()

if __name__ == '__main__':
	main()