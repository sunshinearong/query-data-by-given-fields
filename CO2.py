import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scatterplot import *
import math
import sys
global filename#filename glabal
filename = 'co2_levels.csv'
def main():
    try:
        data = pd.read_csv(filename)#read file
    except Exception,e:
        print("ERROR: could not open file " + filename)#print error message
        sys.exit(0)#quit
    try:
        field = int(raw_input("field [one of 3,4,5,6]: "))#input field
    except Exception,e:
        print("ERROR: illegal value for field")#print error message
    assert field >2 and field<7#assert statement
    try:
        start_year = int(raw_input("start year: "))#input start year
        stop_year = int(raw_input("stop year: "))#input stop year
    except Exception,e:
        sys.exit(0)#error quit
    index1 = data['# Year']>=start_year
    index2 = data['# Year']<=stop_year
    index = index1 & index2#time range
    query = data[index]#query result
    whether_gragh = raw_input("graph? [y/n] ")#display
    if whether_gragh == 'n':
        for i in range(len(query)):
            try:
                year = int(query.iloc[i,0])#year
                month = int(query.iloc[i,1])#month
                data_value = query.iloc[i,field]#data_value
                if math.isnan(data_value) == 0:#not null
                    print("{:d} {:d} -- {:f}".format( year, month, data_value ))
            except Exception,e:
                print('ERROR: [line {:d}]: Bad value(s): {} {} {}'.format(i, year, month, data_value))#error message
    else:
        data_list = []
        for value in query.iloc[:,field].values:
            if math.isnan(value) == 0:
                data_list.append(value)
        data_list = zip(range(len(data_list)),data_list)#data_list
        draw_scatterplot(data_list, 'red', '*')#draw plot
main()    

