from requests import get
from pdb import set_trace as bp
import csv
import pandas as pd

########################################################################
url = "http://swoogle.umbc.edu/SimService/GetSimilarity"

def sss(s1, s2):
    try:
        response = get(url, params={'operation':'api','phrase1':s1,'phrase2':s2,'type':'concept','corpus':'webbase'})
        return float(response.text.strip())
    except:
        print 'Error in getting similarity for %s: %s' % ((s1,s2), response)
        return 0.0

########################################################################
csv_file = "/home/mica/Desktop/python/fMRIBatteryMay2017/tasks/semantic/semantic_matrix.csv"

########################################################################
list_a = pd.read_csv(csv_file).Name.tolist()

########################################################################
sim_index_matrix = []

for a in list_a:
	for z in list_a[0]:
		bla = sss(z,a)
		sim_index_matrix.append(bla)

bp()

yoyo = 1 + 2

