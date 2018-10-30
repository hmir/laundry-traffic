import os
import json
from datetime import datetime
from flask import Flask, render_template, request

app = Flask(__name__)

facilities = {}
for i in open('facilities.txt'):
    facilities[i.strip().replace(' ', '')] = i.strip();
    
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
machines = ['washers', 'dryers']

@app.route('/')
def main():
    return render_template('index.html')

def processData(facility, day, machine):
    currentDate = str(datetime.now())[:10]

    folderPath = 'data/' + facilities[facility] + '/' + day + '/'
    files = [item for item in os.listdir(folderPath)]

    totalUsages = {}
    timeCounts = {}
    
    for i in range(len(files)):
        f = files[i]
        if f[:10] == currentDate:
            continue
        dateData = json.load(open(folderPath + f))
        for time in dateData:
            availible = int(dateData[time][machine + "Available"])
            total = int(dateData[time][machine + "Total"])
            if time in totalUsages:
                totalUsages[time] += (total-availible)/total
                timeCounts[time] += 1
            else:
                totalUsages[time] = (total-availible)/total
                timeCounts[time] = 1

    averageUsages = {}
    for time in totalUsages:
        averageUsages[time] = totalUsages[time]/timeCounts[time]

    return averageUsages

@app.route('/laundry_data')
def getProcessedData():
    facility = request.args.get('building')
    day = request.args.get('day')
    machine = request.args.get('machine')
    weeks = 8

    if facility not in facility or day not in days or machine not in machines:
        dataRaw = {}

    dataRaw = processData(facility, day, machine)
    return render_template('data.html', machineData=dataRaw)

if __name__ == '__main__':
    app.run()
