# -*- coding: utf-8 -*-
'''
Find the time and value of max load for each of the regions
COAST, EAST, FAR_WEST, NORTH, NORTH_C, SOUTHERN, SOUTH_C, WEST
and write the result out in a csv file, using pipe character | as the delimiter.

An example output can be seen in the "example.csv" file.
'''

import xlrd
import os
import csv
from zipfile import ZipFile

datafile = "2013_ERCOT_Hourly_Load_Data.xls"
outfile = "2013_Max_Loads.csv"


def open_zip(datafile):
    with ZipFile('{0}.zip'.format(datafile), 'r') as myzip:
        myzip.extractall()


def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)
    data = None
    # YOUR CODE HERE
    # Remember that you can use xlrd.xldate_as_tuple(sometime, 0) to convert
    # Excel date to Python tuple of (year, month, day, hour, minute, second)
    dates = sheet.col_values(0)
    coasts = sheet.col_values(1)
    easts =  sheet.col_values(2)
    farWests =  sheet.col_values(3)
    norths =  sheet.col_values(4)
    northcs = sheet.col_values(5)
    southerns = sheet.col_values(6)
    southcs = sheet.col_values(7)
    wests = sheet.col_values(8)
    data = []
    data.append(['Station', 'Year', 'Month', 'Day', 'Hour', 'Max Load'])

    s = [coasts[0]] + list(xlrd.xldate_as_tuple(dates[coasts.index(max(coasts[1:]))],0))
    s.append(max(coasts[1:]))
    data.append(s)

    s = [easts[0]] + list(xlrd.xldate_as_tuple(dates[easts.index(max(easts[1:]))],0))
    s.append(max(easts[1:]))
    data.append(s)

    s = [farWests[0]] + list(xlrd.xldate_as_tuple(dates[farWests.index(max(farWests[1:]))],0))
    s.append(max(farWests[1:]))
    data.append(s)

    s = [norths[0]] + list(xlrd.xldate_as_tuple(dates[norths.index(max(norths[1:]))],0))
    s.append(max(norths[1:]))
    data.append(s)

    s = [northcs[0]] + list(xlrd.xldate_as_tuple(dates[northcs.index(max(northcs[1:]))],0))
    s.append(max(northcs[1:]))
    data.append(s)

    s = [southerns[0]] + list(xlrd.xldate_as_tuple(dates[southerns.index(max(southerns[1:]))],0))
    s.append(max(southerns[1:]))
    data.append(s)

    s = [southcs[0]] + list(xlrd.xldate_as_tuple(dates[southcs.index(max(southcs[1:]))],0))
    s.append(max(southcs[1:]))
    data.append(s)

    s = [wests[0]] + list(xlrd.xldate_as_tuple(dates[wests.index(max(wests[1:]))],0))
    s.append(max(wests[1:]))
    data.append(s)

    print(data)
    return data

def save_file(data, filename):
    # YOUR CODE HERE
    with open(filename, 'wb') as f:
        writer = csv.writer(f, delimiter='|')
        for item in data:
	    print(item)
            writer.writerow(item)

    
def test():
    open_zip(datafile)
    data = parse_file(datafile)
    save_file(data, outfile)

    number_of_rows = 0
    stations = []

    ans = {'FAR_WEST': {'Max Load': '2281.2722140000024',
                        'Year': '2013',
                        'Month': '6',
                        'Day': '26',
                        'Hour': '17'}}
    correct_stations = ['COAST', 'EAST', 'FAR_WEST', 'NORTH',
                        'NORTH_C', 'SOUTHERN', 'SOUTH_C', 'WEST']
    fields = ['Year', 'Month', 'Day', 'Hour', 'Max Load']

    with open(outfile) as of:
        csvfile = csv.DictReader(of, delimiter="|")
        for line in csvfile:
            station = line['Station']
            if station == 'FAR_WEST':
                for field in fields:
                    # Check if 'Max Load' is within .1 of answer
                    if field == 'Max Load':
                        max_answer = round(float(ans[station][field]), 1)
                        max_line = round(float(line[field]), 1)
                        assert max_answer == max_line

                    # Otherwise check for equality
                    else:
                        assert ans[station][field] == line[field]

            number_of_rows += 1
            stations.append(station)

        # Output should be 8 lines not including header
        assert number_of_rows == 8

        # Check Station Names
        assert set(stations) == set(correct_stations)

        
if __name__ == "__main__":
    test()

