import pandas as pd
from bs4 import BeautifulSoup
import requests
import os
import re

url = r'https://www.health.pa.gov/topics/disease/coronavirus/Pages/Cases.aspx'
html_content = requests.get(url).text
lastupdatedfile = "lastupdated.txt"
soup = BeautifulSoup(html_content, "lxml")
stats = soup.find("span",attrs={"class": "ms-rteStyle-Quote"})
#TODO: byte / string issue here on updatecheck
updatecheck = stats.text[stats.text.find("at "):][3:]

if os.path.isfile(lastupdatedfile):
	lastupdate = open(lastupdatedfile).read()
	if lastupdate == updatecheck:
		print("Skipping check, no new update.")
		os._exit(0)
	else:
		print("***UPDATE***\nOld: {}".format(lastupdate))
		print("New: {}".format(updatecheck))

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


f=open(lastupdatedfile,"w")
f.write(updatecheck)
f.close()
# Add some notification stuff here...

