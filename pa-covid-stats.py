import pandas as pd
from bs4 import BeautifulSoup
import requests
import os
import re
import smtplib
from email.message import EmailMessage

# Uncomment this and look at the sendNotification function to configure email notification.  Useful if you run this from cron
sendEmailNotifyOnUpdate=False

url = r'https://www.health.pa.gov/topics/disease/coronavirus/Pages/Cases.aspx'
html_content = requests.get(url).text
lastupdatedfile = "lastupdated.txt"
soup = BeautifulSoup(html_content, "lxml")
stats = soup.find("span",attrs={"class": "ms-rteStyle-Quote"})
#TODO: byte / string issue here on updatecheck
updatecheck = stats.text[stats.text.find("at "):][3:]
newStatsAvailable = False

if os.path.isfile(lastupdatedfile):
	lastupdate = open(lastupdatedfile).read()
	if lastupdate == updatecheck:
		print("Skipping check, no new update.")
		os._exit(0)
	else:
		print("***UPDATE***\nOld: {}".format(lastupdate))
		print("New: {}".format(updatecheck))
		newStatsAvailable = True

tables = pd.read_html(html_content, header=0)
df = tables[3]

totalCounties = 67

print("Pennsylvania Data ({})".format(updatecheck))

deathsTotal = int(df["Deaths"].sum())
casesTotal  = int(df["Number of Cases"].sum())
mortalityPercent = round((deathsTotal / casesTotal) * 100,2)
reportingTotal = int(df["County"].count())
reportingCases = df["Number of Cases"]
reportingCasesPct = round((reportingCases.count() / totalCounties) * 100,2)
reportingDeathsObj = df.apply(lambda x: True if x['Deaths'] > 0 else False, axis=1)
reportingDeaths = len(reportingDeathsObj[reportingDeathsObj == True].index)
reportingDeathsPct = round((reportingDeaths / reportingTotal) * 100,2)

print("Total Cases: {}".format(casesTotal))
print("Total Deaths: {}".format(deathsTotal))
print("Mortality Rate(%): {}".format(mortalityPercent))
print("Counties Reporting Cases: {}".format(reportingCases.count()))
print("Counties Reporting Cases(%): {}".format(reportingCasesPct))
print("Counties Reporting Deaths: {}".format(reportingDeaths))
print("Counties Reporting Deaths(% of counties reporting cases): {}".format(reportingDeathsPct))

if newStatsAvailable:
	if sendEmailNotifyOnUpdate: 
		output = ("Updated: {}\n"+
			"Total Cases: {}\n"+
			"Total Deaths: {} \n"+
			"Mortality Rate: {} \n"
			"County Cases: {} \n"+
			"County Cases(%): {} \n"+
			"County Deaths: {} \n"+
			"County Deaths(%): {} \n").format(updatecheck,casesTotal,deathsTotal,mortalityPercent,reportingCases.count(),reportingCasesPct,reportingDeaths,reportingDeathsPct)
		sendNotification(output)

f=open(lastupdatedfile,"w")
f.write(updatecheck)
f.close()



# Add some notification stuff here...

def sendNotification(output):
        msg = EmailMessage()
        msg.set_content(output)
        msg['Subject'] = f'PA COVID-19 Update'
        msg['From'] = f'PA-COVID-STATS'
        msg['To'] = f'email@email.com, email2@email.com'

        s = smtplib.SMTP('localhost')
        s.send_message(msg)
        s.quit()
        print(f'Email notification sent!')

