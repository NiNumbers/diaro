# import modules

import sys
import os
import re
import numpy as np
import pandas as pd
from datetime import datetime


# Load Diarodata from file and inputdata
def loaddata(external_file=None):
    """
        load diarofile for further use

        Parameters:
        ----------
        :param external_file: str    absolute path incl. file if data not in diaro/data folder
    """
    if external_file:
        importfileandpath = external_file
    else:
        homepath = os.path.dirname(os.path.dirname(__file__))
        importfileandpath = os.path.join(homepath, 'data', 'entryExport.txt')
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


# test if Diarodata is up to date
def screendata(external_file=None):
    """
        test if diarodata is up to date

        Parameters:
        ----------
        :param external_file: str    absolute path incl. file if data not in diaro/data folder
    """
    diarotext = loaddata(external_file)
    firstline = diarotext.partition('\n')[0]
    print('Latest entry: ', firstline)
    inp1 = input('Is the Diaro data export up to date? [Y/N] ')

    if inp1.lower() == 'n' or inp1.lower() == 'no':
        sys.exit('So please go to diaroapp.com and download the data, then come back an try again.')
    return


# search the Diarodata for textpattern
def searchpattern(regexpattern, external_file=None):
    """
        search the diarodatafile for textpattern
        Further instruction for regular expressions: https://www.debuggex.com/cheatsheet/regex/python

        Parameters:
        ----------
        regexpattern: regular expression, pattern to search for in data
        :param external_file: str    absolute path incl. file if data not in diaro/data folder
    """
    diarotext = loaddata(external_file)
    text_match = re.findall(regexpattern, diarotext)
    return text_match

# search the Diarodata for dates
def extractdate(external_file=None):
    """
        search the diarodatafile for dates and transforms it into datetime format
        optimised for the diaro format

        Parameters:
        ----------
        :param external_file: str    absolute path incl. file if data not in diaro/data folder
    """
    diarotext = loaddata(external_file=None)
    date_match = re.findall(r'\d+ \w+ 2019', diarotext)
    datetext = np.array(date_match)
    date = [datetime.strptime(x, '%d %B %Y').date() for x in datetext]
    return date