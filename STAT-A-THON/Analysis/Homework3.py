import numpy as np
import pylab as pl
import urllib.request
import matplotlib.pyplot as plt


start_year = 1900
end_year   = 2014

# CRU temperature
T = []
#f = urllib.request.urlopen('http://www.cru.uea.ac.uk/cru/data/temperature/HadCRUT4-gl.dat')
with urllib.request.urlopen('http://www.cru.uea.ac.uk/cru/data/temperature/HadCRUT4-gl.dat')  as response:
    year=0
    for line in response:
        line_words=line.decode('utf-8')
        if line_words[1:3] == '19' or line_words[1:3] == '20':
            values = line.decode('utf-8').split()
            year= np.int16(values[0])
            if year!=y and year >= start_year and year <= end_year:
                T.append(np.float(values[-1]))
                #print (values[-1])
        y=year

CO2 = []
with urllib.request.urlopen('http://cdiac.ornl.gov/ftp/trends/co2/lawdome.smoothed.yr20') as response:
    for line in response:
        line_words=line.decode('utf-8')
        if len(line_words) > 30 and line_words[5] == '1':
            values = line.split()
            year   = np.int16(values[0])
            if year >= start_year and year < 1959:
                CO2.append(np.float32(values[1]))
print(len(CO2))

# MLO
with  urllib.request.urlopen('ftp://aftp.cmdl.noaa.gov/products/trends/co2/co2_annmean_mlo.txt') as response:
    for line in response:
        line = line.decode('utf-8')
        if line[0] != '#':
            values = line.split()
            year   = np.int16(values[0])
            if year >= 1959 and year <= end_year:
                CO2.append(np.float32(values[1]))

# first plot, only temperature
fig = plt.figure(1, figsize=(7.5, 4.5))
ax1 = fig.add_subplot(111)
years = np.arange(start_year, end_year+1)
ax1.plot(years, T, 'b-', linewidth=1.5)
ax1.set_xlabel('Year')
ax1.set_xlim(start_year-2, end_year+3)
ax1.set_ylabel('Global temperature anomaly ($^\circ$C)', color='b')
pl.grid()
for tl in ax1.get_yticklabels():
    tl.set_color('b')

pl.savefig('T.png', dpi=100)

# add CO2 concentration
ax2 = ax1.twinx()
ax2.plot(years, CO2, 'r-', linewidth=1.5)
ax2.set_xlim(start_year-2, end_year+3)
ax2.set_ylabel('CO$_2$ concentration (ppm or 0.0001%)', color='r')
for tl in ax2.get_yticklabels():
    tl.set_color('r')

pl.savefig('T_CO2.png', dpi=100)

