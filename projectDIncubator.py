#!/usr/bin/env python

import sys
import csv
import numpy as np
#import scipy.stats
import string
from pylab import *

"""
!!! Using Python 2.7.6 !!!
"""

####################################################################
# distance (in km) from USA using latitude and longitude data
def getXY(lat2, lon2):
    lat1 = 38.   # latitude of USA
    lon1 = -97.  # longitude of USA
    dx = (lon2-lon1)*40000*np.cos((lat1+lat2)*np.pi/360.)/360.
    dy = (lat2-lat1)*40000./360.
    return [dx, dy]
####################################################################

##########################################################################
# read latitude and longitude information
count = -1.0
cname = []
clalo = [[] for i in range(2)]
with open('worldbank/countries.csv', 'rb') as f:
    reader = csv.reader(f)

    for row in reader:
        count += 1.0
        if count==0:
            continue

        clalo[0].append(float(row[4]))
        clalo[1].append(float(row[5]))
        cname.append(row[2])
##########################################################################

##########################################################################
count     = -1.0
country   = [[] for i in range(2)] 
coord     = [[] for i in range(2)] 
data      = [[] for i in range(2)] 

# read world bank data 
with open('worldbank/set2/API_NY.GDP.MKTP.KD.ZG_DS2_en_csv_v2.csv', 'rb') as f:
#with open('worldbank/API_NE.CON.PRVT.CD_DS2_en_csv_v2.csv', 'rb') as f:
    reader = csv.reader(f)

    for row in reader:
        count += 1.0
        if count<5:
            continue

        cid = cname.index(row[1]) if row[1] in cname else -1
        if cid != -1 and row[54] != '' and row[59] != '':
                country[0].append(row[0])
                country[1].append(row[1])
                data[0].append(float(row[54]))
                data[1].append(float(row[59]))
                [x, y] = getXY(clalo[0][cid], clalo[1][cid])
                coord[0].append(x)
                coord[1].append(y)
##########################################################################

##########################################################################
xcoord = np.array(coord[0])
ycoord = np.array(coord[1])
for i in range(len(xcoord)):
    print sqrt(xcoord[i]**2+ycoord[i]**2), (data[1][i]-data[0][i])/(data[1][175]-data[0][175])

colors = [(data[1][i]-data[0][i])/(data[1][175]-data[0][175]) for i in range(len(xcoord))]
#print np.min(colors), np.max(colors)
area = [np.pi*12 for i in range(len(xcoord))]
fig = plt.figure(1)
ax  = fig.add_subplot(111, axisbg='black')
ax.set_xlabel('distance from USA [in km]')
ax.set_ylabel('distance from USA [in km]')
sc  = ax.scatter(xcoord, ycoord, s=area, c=colors, alpha=0.8, vmin=-100, vmax=100, cmap=cm.bwr)
fc = colorbar(sc)
fc.set_label('Relative change in GDP')
savefig("relativeGDP.png")
show()
##########################################################################
