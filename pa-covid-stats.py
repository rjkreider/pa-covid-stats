import pandas as pd
from bs4 import BeautifulSoup
import requests

url = r'https://www.health.pa.gov/topics/disease/coronavirus/Pages/Cases.aspx'
html_content = requests.get(url).text

soup = BeautifulSoup(html_content, "lxml")
stats = soup.find("span",attrs={"class": "ms-rteStyle-Quote"})
lastupdated = stats.text[stats.text.find('last'):]

tables = pd.read_html(html_content, header=0)
df = tables[1]

totalCounties = 67

print("Pennsylvania Data ({})".format(lastupdated))
# Counties with cases
#print(df[df.Cases > 0])

deathsTotal = int(df["Deaths"].sum())
casesTotal  = int(df["Cases"].sum())
mortalityPercent = round((deathsTotal / casesTotal) * 100,2)
reportingTotal = int(df["County"].count())
reportingCases = df["Cases"]
reportingCasesPct = round((reportingCases.count() / totalCounties) * 100,2)
reportingDeathsObj = df.apply(lambda x: True if x['Deaths'] > 0 else False, axis=1)
reportingDeaths = len(reportingDeathsObj[reportingDeathsObj == True].index)
reportingDeathsPct = round((reportingDeaths / reportingTotal) * 100,2)

print("Cases: {}\nDeaths: {}\nMortality(%): {}\nCounties Reporting: {}\nCounties Positive: {}\nCounties Positive Affected(%): {}\nCounties Deaths: {}\nCounties Deaths(%): {}".format(casesTotal,deathsTotal,mortalityPercent,reportingTotal,reportingCases.count(),reportingCasesPct,reportingDeaths,reportingDeathsPct))
