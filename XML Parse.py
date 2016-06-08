from bs4 import BeautifulSoup
import pandas as pd

xml_file = "DATA_DICTIONARY.xml"
soup = BeautifulSoup(open(xml_file), "xml")
rows = soup.find_all('ROW')

index = [r for r in range(len(rows))]

'''For some reason this xml file had a line break after each
child <COLUMN></COLUMN> pair and we filter these out.'''
cols = list(filter('\n'.__ne__, rows[0].contents))

#column titles in order to pass to DataFrame
columns = [c['name'] for c in cols]
print(columns)


'''Using two dictionaries to create a DataFrame 
	"From dict of Series or dicts:" 
http://pandas.pydata.org/pandas-docs/stable/dsintro.html'''

d = {}
for row in rows:
    for c in (list(filter('\n'.__ne__, row.contents))):
        values = d.get(c['name'], [])
        values.append(c.string)
        d[c['name']] = values
d2 = {}
for header in columns:
    d2[header] = pd.Series(d[header], index=index)
df = pd.DataFrame(d2, index=index, columns=columns)

#writer = pd.ExcelWriter(r"C:\Users\hippr\Desktop\xml2excel\Dixtionary.xlsx", engine='xlsxwriter')
#df.to_excel(writer, sheet_name='AlexPwned', index=False, encoding='utf-8')
#writer.close()

#CSV better for large XML files
df.to_csv("DATA_DICTIONARY.csv", sep=',', encoding='utf-8', index=False)
