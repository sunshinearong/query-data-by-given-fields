import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from operator import itemgetter
import sys
def main():
    filename = raw_input("Data file: ")#input file
    try:
        data = pd.read_csv(filename)#read file
    except Exception,e:
        print("ERROR: Could not open file " + filename)#print error message
        sys.exit(0)#quit
    while(True):
        try:
            rounds = raw_input('Rounds: ')#input rounds
            if rounds == '':#no input, break
                break
            else:
                rounds = int(rounds)
            prob = float(raw_input('Probability: '))#input probability
        except Exception,e:
            print("ERROR: illegal query value(s)")#print error message
            continue
        assert rounds > 0 and rounds < 8 #assert statement
        assert prob >= 0 and prob <= 1#assert statement
        query = data[data.iloc[:,rounds+2]>prob]#query result
        query_sort = sorted(query.values,key=itemgetter(rounds+2),reverse = True)#sort query
        for query_s in query_sort:
            team = query_s[-4]#team name
            probability = query_s[rounds+2]#probability
            print("{} : {:f}".format(team, probability))


main()    
        
