import sys
import numpy as np
import re
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from extraction.extract_patterns import screendata, searchpattern, extractdate
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


# screen data
print()
print("-------- required inputdata -------")
print()
screendata()
print()

print("-------- Data provided -------")

raus_match = searchpattern(r"::: \d+ raus")

if raus_match:  # see https://docs.python.org/2/library/re.html#match-objects
    print("There are {} rausdatapoints for your search" .format(len(raus_match)))
else:
    sys.exit("did not find any data, is the regular expression correct?")

print("head of data: ", raus_match[0:5])

rausstring = [i.split(' ')[1] for i in raus_match]
rausnumbers = np.array([int(i) for i in rausstring])
raussum = np.sum(rausnumbers)
rausavg = int(np.average(rausnumbers))
rausmedian = int(np.median(rausnumbers))
rausmax = int(np.max(rausnumbers))

print()
print("-------- Data analysed -------")
print("Total tossed things:        ", raussum)
print("Most things tossed per day:  ", rausmax)

# extract date
# TODO: extractdate() with only the dates, where 'raus' is in title.. use pandas?
date = extractdate()

# plot data
# plt.figure()
# plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%Y'))  # X-Achse format: ohne wird nur Jahr angezeigt
# # plt.gca().xaxis.set_major_locator(mdates.DayLocator())  # jeder TAg auf Achse anzeigen
# plt.bar(date, rausnumbers)  # Art des Plots festlegen
# plt.gcf().autofmt_xdate()  # setzt Datum schräg
# plt.show()
