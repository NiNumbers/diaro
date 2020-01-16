# import modules

import sys
import os
import re
import numpy as np
import pandas as pd
from datetime import datetime


# Load Diarodata from file and inputdata
def loaddata(importfile='entryExport.txt', path=None):
    """
        load diarofile for further use

        Parameters:
        ----------
        importfile: name of the textfile, normaly entyExport.txt
        path: has to be given if file is located in different location
    """
    if path != None:
        importfileandpath = os.path.join(path, importfile)
    else:
        importfileandpath = importfile

    try:
        f = open(importfileandpath, 'r', encoding='utf8')
    except IOError as detail:
        print('Cannot open file ' + importfileandpath, detail)
        sys.exit()
    else:
        with f:
            diarotext = f.read()
    f.close()
    return diarotext

# extract the whole data in form of a pandas dataframe
def extractentries(importfile = 'entryExport.txt', path = None):
    """
        search the diarodatafile for dates and transforms it into datetime format
        optimised for the diaro format

        Parameters:
        ----------
        importfile: name of the text file, normally entryExport.txt
        path: has to be given if file is located in different location
    """
    diaro_text = loaddata(importfile, path)
    diaro_text = diaro_text.replace('------------------------------------------------------------------------------------------------', '¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬')
    diaro_text = diaro_text + '\n\n ¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬'
    entry_match = re.findall(r'(\d+ \w+ 20\d\d)([\s\S]|[^\¬{}]*)(¬¬¬¬¬¬¬¬)', diaro_text)
    entries = np.array(entry_match)
    df = pd.DataFrame(entries)

    df = df.drop(2, axis=1)
    df = df.rename(columns={0: 'Date'})
    df['Coma'], df['rest'] = df[1].str.split(' ', 1).str
    df = df.drop('Coma', axis=1)
    df = df.drop(1, axis=1)
    df['Day'], df['rest'] = df['rest'].str.split('\n\n', 1).str
    df['rest'], df['Footer'] = df['rest'].str.split('Folder: ', 1).str
    df['Footer'], df['Mood'] = df['Footer'].str.split('Mood: ', 1).str
    df['Folder'], df['Tags'] = df['Footer'].str.split('Tags: ', 1).str
    df['Main entry1'], df['Header'] = df['rest'].str.split(':::', 1).str
    df['Header'], df['Main entry2'] = df['Header'].str.split(':::', 1).str

    # remove NaN
    df = df.fillna('')

    df['Main entry'] = df['Main entry1'] + df['Main entry2']
    df = df.drop('rest', axis=1).drop('Main entry1', axis=1).drop('Main entry2', axis=1).drop('Footer', axis=1)
    df = df[['Date', 'Day', 'Header', 'Main entry', 'Folder', 'Tags', 'Mood']]

    df = df.replace(r'\n', ' ', regex=True)

    return df
