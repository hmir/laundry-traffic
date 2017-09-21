from selenium import webdriver
from selenium.webdriver.common.keys import Keys

credentialsFile = open("credentials.txt", "r")

credentials = []
for i in credentialsFile:
    credentials.append(i[9:].strip())

driver = webdriver.Chrome()
driver.get("https://csg-web1.eservices.virginia.edu/login/index.php")

driver.find_elements_by_tag_name("a")[3].click()

usern = driver.find_element_by_name("user")
pword = driver.find_element_by_name("pass")

usern.send_keys(credentials[0])
pword.send_keys(credentials[1])

driver.find_elements_by_name("submit")[1].click()

driver.get("https://csg-web1.eservices.virginia.edu/student/laundry/room_status.php")
