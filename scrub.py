import time
import pprint

from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import json

driver = webdriver.Chrome()

def login():
    #read in username and password from credentials.txt
    credentialsFile = open('credentials.txt', 'r')
    credentials = []
    for i in credentialsFile:
        credentials.append(i[9:].strip())

    driver.get('https://csg-web1.eservices.virginia.edu/login/index.php')

    #click navigates browser to netbadge
    driver.find_elements_by_tag_name('a')[3].click()

    usern = driver.find_element_by_name('user')
    pword = driver.find_element_by_name('pass')

    #input username and password into netbadge
    usern.send_keys(credentials[0])
    pword.send_keys(credentials[1])

    #netbadge login
    driver.find_elements_by_name('submit')[1].click()

def getLaundryData():
    #go to laundry room status page
    driver.get('https://csg-web1.eservices.virginia.edu/student/laundry/room_status.php')

    #wait at most ten seconds to load in laundry room data
    rows = driver.find_elements_by_class_name('row1') + driver.find_elements_by_class_name('row2')
    sleepCount = 0
    loginCount = 0
    while len(rows) == 0:
        if loginCount > 2:
            print('Could not log in, retrying...')
            time.sleep(1)
            loginCount = 0
        if sleepCount > 10:
            login()
            sleepCount = 0
            login += 1
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
    return laundryData

def writeToOutput(fileToCreate, dataToWrite):
    f = open(fileToCreate, 'w')
    f.write(dataToWrite)
    f.close()

login()

checkedThisMinute = False
globalDict = {}
while True:
    if datetime.now().minute % 5 == 0 and not checkedThisMinute:
        if str(datetime.now().month) + '-' + str(datetime.now().day) not in globalDict:
            globalDict[str(datetime.now())[5:10]] = {}
        globalDict[str(datetime.now())[5:10]][str(datetime.now())[11:16]] = getLaundryData()
        checkedThisMinute = True
    elif datetime.now().hour == 23 and datetime.now().minute == 59:
        globalDict = {}
        time.sleep(1)
    elif datetime.now().minute % 5 != 0 and checkedThisMinute:
        checkedThisMinute = False
        writeToOutput(str(datetime.now())[5:10] + '.json', json.dumps(globalDict))

    time.sleep(1)
