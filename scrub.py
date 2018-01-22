import time
import pprint

from datetime import datetime

import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

dcap = dict(DesiredCapabilities.PHANTOMJS)

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
dorms = ['Balz-Dobie', 'East Lawn', 'Lile-Maupin', 'Bice House', 'Faulkner Apartments', 'Metcalf', 'Brown College', 'French House', 'Munford', 'Cauthen', 'Gibbons House', 'Shannon House', 'Copeley Bldg 829', 'Gooch', 'Shea House', 'Copeley Bldg 833', 'Gwathmey', 'Spanish House', 'Copeley Bldg 836', 'Hereford College (Runk)', 'Tuttle-Dunnington', 'Copeley Bldg 839', 'Kellogg', 'Watson-Webb', 'Dabney', 'Lambeth', 'Dillard', 'Lewis']

# driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=TLSv1'])
driver = webdriver.PhantomJS(desired_capabilities=dcap, service_args=['--ignore-ssl-errors=true'])
driver.set_window_size(1120, 550)
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
        newData = getLaundryData()
        for dorm in dorms:
            if dorm not in globalDict:
                globalDict[dorm] = {}
            globalDict[dorm][str(datetime.now())[11:16]] = newData[dorm]
        # if str(datetime.now().month) + '-' + str(datetime.now().day) not in globalDict:
        #     globalDict[str(datetime.now())[5:10]] = {}
        # globalDict[str(datetime.now())[5:10]][str(datetime.now())[11:16]] = getLaundryData()
        checkedThisMinute = True
    elif datetime.now().hour == 23 and datetime.now().minute == 59:
        globalDict = {}
        time.sleep(1)
    elif datetime.now().minute % 5 != 0 and checkedThisMinute:
        checkedThisMinute = False
        weekday = days[datetime.today().weekday()]
        for dorm in dorms:
            writeToOutput('data/' + str(dorm) + weekday + str(datetime.now())[:10] + '.json', json.dumps(globalDict))

    time.sleep(1)
