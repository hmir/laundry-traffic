import sys
import time
import pprint

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#read in username and password from credentials.txt
credentialsFile = open('credentials.txt', 'r')
credentials = []
for i in credentialsFile:
    credentials.append(i[9:].strip())

driver = webdriver.Chrome()
driver.get('https://csg-web1.eservices.virginia.edu/login/index.php')

#click navigates broswer to netbadge
driver.find_elements_by_tag_name('a')[3].click()

usern = driver.find_element_by_name('user')
pword = driver.find_element_by_name('pass')

#input username and password into netbadge
usern.send_keys(credentials[0])
pword.send_keys(credentials[1])

#netbadge login
driver.find_elements_by_name('submit')[1].click()

#go to laundry room status page
driver.get('https://csg-web1.eservices.virginia.edu/student/laundry/room_status.php')

#wait at most ten seconds to load in laundry room data
rows = driver.find_elements_by_class_name('row1') + driver.find_elements_by_class_name('row2')
sleepCount = 0
while len(rows) == 0:
    if sleepCount > 10:
        print('Server timed out')
        driver.close()
        sys.exit()
    time.sleep(1)
    sleepCount += 1
    rows = driver.find_elements_by_class_name('row1') + driver.find_elements_by_class_name('row2')

laundryData = {}

#iterate through rows of laundry data to build dictionary
for row in rows:
    rowText = row.text.split(' ')

    dorm = ''
    washersAvailable = -1
    washersTotal = -1
    dryersAvailable = -1
    dryersTotal = -1


    for item in range(len(rowText)):
        if rowText[item] == '/':
            if washersAvailable == -1:
                washersAvailable = rowText[item-1]
                washersTotal = rowText[item + 1]
                dorm = ' '.join([rowText[i] for i in range(0, item-1)])
            else:
                dryersAvailable = rowText[item-1]
                dryersTotal = rowText[item+1]
                break

    laundryData[dorm] = {'washersAvailable':washersAvailable, 'washersTotal':washersTotal, 'dryersAvailable':dryersAvailable, 'dryersTotal':dryersTotal}

driver.close()

pprint.pprint(laundryData)
