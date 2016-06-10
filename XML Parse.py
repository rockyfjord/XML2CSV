from bs4 import BeautifulSoup
from collections import defaultdict
import pandas as pd
import os.path
import errno
import sys


def location(xml_location):
    def make_sure_path_exists(path):
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
    directory = os.path.dirname(xml_location)
    output = "{}\{}".format(directory, 'CSV OUTPUT')
    make_sure_path_exists(output)
    filename = os.path.basename(xml_location)
    csv_filename = ''.join((filename[:-4], '.csv'))
    return dict(dir=output, file=csv_filename)


def main(xml_file):
    print("Processing {}".format(xml_file))
    soup = BeautifulSoup(open(xml_file), "xml")
    rows = soup.find_all('ROW')

    '''For some reason this xml file had a line break after each child <COLUMN></COLUMN> pair;
    we filter these out (function __ne__ is called by !=).'''
    cols = list(filter('\n'.__ne__, rows[0].contents))

    index = [r for r in range(len(rows))]
    columns = [c['name'] for c in cols]

    '''Using two dictionaries to create a DataFrame From dict of Series or dicts -
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
    save_to = "{dir}\{file}".format(**location(xml_file))
    df.to_csv(save_to, sep=',', encoding='utf-8', index=False)
    print(save_to)

if __name__ == '__main__':
    try:
        for file in filter(lambda f: f.lower().endswith('xml'), sys.argv[1:]):
            main(file)
    except IndexError:
        print("Drag XML files onto script.")
    input("Done. Press any key.")
