#:! python3 %
#:!!
import pandas as pd
from bs4 import BeautifulSoup
import requests
import os
import re

url = r'https://www.covidtracking.com/data/state/pennsylvania/'
html_content = requests.get(url).text
soup = BeautifulSoup(html_content, "lxml")

tables = pd.read_html(html_content, header=0)
df = tables[1]


tests = df["Total test resultsPositive + Negative"]

#print("Tests: {}".format(tests))
#print(df.iloc[ : , 5 ])
print(df.iloc[ : , : ])

