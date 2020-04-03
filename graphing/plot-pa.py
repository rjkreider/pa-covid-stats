import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
my_date = datetime.now()
print(my_date.isoformat())

path = 'data/pennsylvania.csv' # This is from https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv and just Pennsylvania is extracted
df = pd.read_csv(path)
df = df.set_index('Admin2')
plt.figure(figsize=(21,8))
plt.locator_params(axis="both", integer=True, tight=False)
year_columns = df.columns[11:]
years = [year for year in year_columns]
counties = [county for county in df.index]
max_date = str(max(years))
for county in counties:
	#plt.locator_params(axis="both", integer=True, tight=False)
	positive_cases = [df.loc[county][year] for year in year_columns]
	county_name = county
	plt.plot(years, positive_cases, label=county_name + '(' + str(max(positive_cases)) + ')')
	#plt.title(county_name + ' County COVID-19 Positive Cases')
	#plt.xlabel=('Day')
	#plt.ylabel=('Cases')
	#plt.xticks(np.arange(0, len(years), 1), rotation=45)
	#plt.yticks(np.arange(min(positive_cases), max(positive_cases)+50, 5.0))
	#plt.savefig("plots/" + county_name + ".png",bbox_inches='tight',dpi=100)
	#plt.legend(loc='lower right')
plt.title('Pennsylvania COVID-19 Pos. Cases by County as of ' + max_date)
plt.legend(loc='upper left',prop={"size":8},ncol=10)
plt.xlabel('Days\n\nPrepared by Rich Kreider using CSSE at Johns Hopkins University data on '+my_date.isoformat())
plt.ylabel('Cases')
plt.yticks(fontsize=8)
plt.xticks(np.arange(0, len(years), 3),rotation=45,fontsize=8)
plt.savefig("output.png",bbox_inches='tight',dpi=96)

#fig = plt.figure()
#fig_legend = plt.figure(figsize=(2, 1.25))
#ax = fig.add_subplot(111)
#lines = ax.plot(range(2), range(2), range(2), range(2), range(2), range(2), range(2), range(2))
#fig_legend.legend(lines, df.index, loc='center', frameon=False)
#plt.savefig("legend.png")
