from psychopy import gui, os, core, data
import csv
import re
import pandas as pd
from pdb import set_trace as bp
import numpy

#############################################################################################################################################################################################
expName = "Episodic Evaluator"
expInfo = {'subject name':'', 'session':'001', 'symbol list':['A','B','demo']}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)

#############################################################################################################################################################################################
if dlg.OK == False: core.quit()
expInfo['date'] = data.getDateStr()
expInfo['expName'] = expName

#############################################################################################################################################################################################
if os.path.isdir('tasks/episodic/data_score') == False:
    os.makedirs('tasks/episodic/data_score')

csv_file = ("tasks/episodic/data_score/" + expInfo['subject name'] + "_" + expInfo['session'] + "_" + expInfo['date'] + "_" +  expInfo['symbol list'] + "_SCORE" + ".csv")
with open(csv_file, "w") as outcsv:
	writer = csv.writer(outcsv)
	writer.writerow(["Condition", "Correct", "Wrong", "Percent_correct", "Percent_wrong", "mean_RT_correct", "mean_RT_wrong", "mean_RT"])

#############################################################################################################################################################################################
regex = re.compile(expInfo['subject name'] + '_' + expInfo['session'] + '.*' + expInfo['symbol list'])
dirfiles = os.listdir('tasks/episodic/data_retrieval/')

#############################################################################################################################################################################################
targetfile = [s for s in dirfiles if re.match(regex,s)]
log_file = 'tasks/episodic/data_retrieval/' + targetfile[0]

#############################################################################################################################################################################################
list_a = pd.read_csv(log_file).Condition.tolist()
list1 = list_a[1::5]
list2 = pd.read_csv(log_file).Target.tolist()
list3 = pd.read_csv(log_file, na_values='', keep_default_na=False).Subject_Response.tolist()
list4 = pd.read_csv(log_file, na_values='', keep_default_na=False).Reaction_Time.tolist()

#############################################################################################################################################################################################
while list2.count('--') > 0:
	list2.remove('--')

list2 = [x for x in list2 if isinstance(x,str)]
	
while list3.count('--') > 0:
	list3.remove('--')

list3 = [x for x in list3 if isinstance(x,str)]

while list4.count('--') > 0:
	list4.remove('--')

list4 = [x for x in list4 if isinstance(x,str)]

list4 = list4[0:56] ### I forget why I added this in...

#############################################################################################################################################################################################
main_list = list(zip(list1,list2,list3))

main_list1 = [x for x in main_list if x[0] == 'D']
main_list2 = [x for x in main_list if x[0] == 'E']

resp_list = []

for a,b,c in main_list:
	if b == c:
		resp_list.append('correct')
	elif b != c:
		resp_list.append('wrong')

main_list3 = list(zip(list1,resp_list,list4))  ### (condition, accuracy, RT)

main_list4 = [x for x in main_list3 if x[2] != 'N/A']  ### get rid of all trials in which participant did not respond

main_list4D = [x for x in main_list4 if x[0] == 'D']  ### difficult trials (correct & wrong)
main_list4E = [x for x in main_list4 if x[0] == 'E']  ### easy trials (correct & wrong)

main_list4D_C = [x for x in main_list4D if x[1] == 'correct']  ### difficult & correct trials
main_list4D_W = [x for x in main_list4D if x[1] == 'wrong']  ### difficult & wrong trials

main_list4E_C = [x for x in main_list4E if x[1] == 'correct']  ### easy & correct trials
main_list4E_W = [x for x in main_list4E if x[1] == 'wrong']  ### easy & wrong trials

###
RT_list = [float(x[2]) for x in main_list4] ### all RTs
###

D_C_RT_list = [float(x[2]) for x in main_list4D_C] ### difficult & correct (only RTs)
D_W_RT_list = [float(x[2]) for x in main_list4D_W] ### difficult & wrong (only RTs)
E_C_RT_list = [float(x[2]) for x in main_list4E_C] ### easy & correct (only RTs)
E_W_RT_list = [float(x[2]) for x in main_list4E_W] ### easy & wrong (only RTs)

###
mean_RT = numpy.mean(RT_list)
###

mean_RT_D_C = numpy.mean(D_C_RT_list)
mean_RT_D_W = numpy.mean(D_W_RT_list)
mean_RT_E_C = numpy.mean(E_C_RT_list)
mean_RT_E_W = numpy.mean(E_W_RT_list)

#############################################################################################################################################################################################
D_list = []
E_list = []

#############################################################################################################################################################################################
for a,b,c in main_list1:
	if b == c:
		D_list.append(b)

D_score = len(D_list)	
D2_score = len(main_list1) - D_score

for a,b,c in main_list2:
	if b == c:
		E_list.append(b)

E_score = len(E_list)	
E2_score = len(main_list2) - E_score

#############################################################################################################################################################################################
with open(csv_file, "a") as p:
	writer = csv.writer(p)
	writer.writerow(['All', '--', '--', '--', '--', '--', '--', mean_RT])	
	writer.writerow(['D', D_score, D2_score, numpy.round(D_score*100.0/(len(main_list1))), numpy.round(D2_score*100.0/(len(main_list1))), mean_RT_D_C, mean_RT_D_W, '--'])
	writer.writerow(['E', E_score, E2_score, numpy.round(E_score*100.0/(len(main_list2))), numpy.round(E2_score*100.0/(len(main_list2))), mean_RT_E_C, mean_RT_E_W, '--'])
