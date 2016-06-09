from bs4 import BeautifulSoup
import pandas as pd
from collections import defaultdict

xml_file = "DATA_DICTIONARY.xml"
soup = BeautifulSoup(open(xml_file), "xml")
rows = soup.find_all('ROW')

'''For some reason this xml file had a line break after each
child <COLUMN></COLUMN> pair and we filter these out.
(function __ne__ is called by !=)'''
cols = list(filter('\n'.__ne__, rows[0].contents))

index = [r for r in range(len(rows))]
columns = [c['name'] for c in cols]
print(columns)

'''Using two dictionaries to create a DataFrame 
From dict of Series or dicts -
http://pandas.pydata.org/pandas-docs/stable/dsintro.html'''

d = defaultdict(list)
for row in rows:
    for c in (list(filter('\n'.__ne__, row.contents))):
        values = d[c['name']]
        values.append(c.string)
d2 = {}
for header in columns:
    d2[header] = pd.Series(d[header], index=index)
df = pd.DataFrame(d2, index=index, columns=columns)
df.to_csv("DATA_DICTIONARY.csv", sep=',', encoding='utf-8', index=False)
