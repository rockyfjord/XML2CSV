from bs4 import BeautifulSoup
from collections import defaultdict
import pandas as pd
import os


xml_files = []
directory = os.listdir("LIST DIRECTORY HERE!")

for thing in directory:
    if thing.lower().endswith('.xml'):
        xml_files.append(thing)
for thing in xml_files:
    xml_file = thing
    soup = BeautifulSoup(open(xml_file), encoding='utf-8', 'xml')
    rows = soup.find_all('ROW')
    
    '''For some reason this xml file had a line break after each
    child <COLUMN></COLUMN> pair and we filter these out.
    (function __ne__ is called by !=)'''
    cols = list(filter('\n'.__ne__, rows[0].contents))
    
    index = [r for r in range(len(rows))]
    columns = [c['name'] for c in cols]
    
    '''Create a DataFrame "From dict of Series" -
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
    df.to_csv(thing[:-4]+'.csv', sep=',', encoding='utf-8', index=False)
    print(thing + " has been converted to csv.")
