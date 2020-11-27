from psychopy import gui, os, core, data
import csv
import re
import pandas as pd
from pdb import set_trace as bp
import numpy

#############################################################################################################################################################################################
expName = "MST Evaluator"
expInfo = {'subject name':'', 'session':'001'}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)

#############################################################################################################################################################################################
if dlg.OK == False: core.quit()
expInfo['date'] = data.getDateStr()
expInfo['expName'] = expName

#############################################################################################################################################################################################
csv_file = ("tasks/MST/data_MST Score/" + expInfo['subject name'] + "_" + expInfo['session'] + "_" + expInfo['date'] + "_SCORE" + ".csv")
with open(csv_file, "wb") as outcsv:
	writer = csv.writer(outcsv)
	writer.writerow(["Condition", "Correct", "Wrong", "Percent_correct", "Percent_wrong", "mean_RT_correct", "mean_RT_wrong", "mean_RT"])

#############################################################################################################################################################################################
regex = re.compile(expInfo['subject name'] + '_' + expInfo['session'] + '.*')
dirfiles = os.listdir('tasks/MST/data_MST Phase 2/')

#############################################################################################################################################################################################
targetfile = [z for z in dirfiles if z.startswith(expInfo['subject name'] + '_' + expInfo['session']) and z.endswith('.csv')]
log_file = 'tasks/MST/data_MST Phase 2/' + targetfile[0]

#############################################################################################################################################################################################
list_a = pd.read_csv(log_file).Condition.tolist()
list1 = list_a[1::5]
list2 = pd.read_csv(log_file, na_values='', keep_default_na=False).Subject_Response.tolist()
list3 = pd.read_csv(log_file, na_values='', keep_default_na=False).Reaction_Time.tolist()

#############################################################################################################################################################################################
while list2.count('--') > 0:
	list2.remove('--')

list2 = [x for x in list2 if isinstance(x,str)]
	
while list3.count('--') > 0:
	list3.remove('--')

list3 = [x for x in list3 if isinstance(x,str)]

list3 = list3[0:96] ### I forget why I added this in...

#############################################################################################################################################################################################
main_list = zip(list1,list2)

main_list1 = [x for x in main_list if x[0] == 'old']
main_list2 = [x for x in main_list if x[0] == 'similar']
main_list3 = [x for x in main_list if x[0] == 'new']

resp_list = []

for a,b in main_list:
	if a == b:
		resp_list.append('correct')
	elif a != b:
		resp_list.append('wrong')

main_list4_beta = zip(list1,resp_list,list3)  ### (condition, accuracy, RT)

main_list4 = [x for x in main_list4_beta if x[2] != 'N/A']  ### get rid of all trials in which participant did not respond

main_list4_old = [x for x in main_list4 if x[0] == 'old']  ### old trials (correct & wrong)
main_list4_similar = [x for x in main_list4 if x[0] == 'similar']  ### similar trials (correct & wrong)
main_list4_new = [x for x in main_list4 if x[0] == 'new']  ### new trials (correct & wrong)

main_list4_old_C = [x for x in main_list4_old if x[1] == 'correct']  ### old & correct trials
main_list4_old_W = [x for x in main_list4_old if x[1] == 'wrong']  ### old & wrong trials

main_list4_similar_C = [x for x in main_list4_similar if x[1] == 'correct']  ### similar & correct trials
main_list4_similar_W = [x for x in main_list4_similar if x[1] == 'wrong']  ### similar & wrong trials

main_list4_new_C = [x for x in main_list4_new if x[1] == 'correct']  ### new & correct trials
main_list4_new_W = [x for x in main_list4_new if x[1] == 'wrong']  ### new & wrong trials

##
RT_list = [float(x[2]) for x in main_list4] ### all RTs
##

old_C_RT_list = [float(x[2]) for x in main_list4_old_C] ### old & correct (only RTs)
old_W_RT_list = [float(x[2]) for x in main_list4_old_W] ### old & wrong (only RTs)
similar_C_RT_list = [float(x[2]) for x in main_list4_similar_C] ### similar & correct (only RTs)
similar_W_RT_list = [float(x[2]) for x in main_list4_similar_W] ### similar & wrong (only RTs)
new_C_RT_list = [float(x[2]) for x in main_list4_new_C] ### new & correct (only RTs)
new_W_RT_list = [float(x[2]) for x in main_list4_new_W] ### new & wrong (only RTs)

##
mean_RT = numpy.mean(RT_list)
##

mean_RT_old_C = numpy.mean(old_C_RT_list)
mean_RT_old_W = numpy.mean(old_W_RT_list)
mean_RT_similar_C = numpy.mean(similar_C_RT_list)
mean_RT_similar_W = numpy.mean(similar_W_RT_list)
mean_RT_new_C = numpy.mean(new_C_RT_list)
mean_RT_new_W = numpy.mean(new_W_RT_list)

#############################################################################################################################################################################################
old_list = []
similar_list = []
new_list = []

#############################################################################################################################################################################################
for a,b in main_list1:
	if a == b:
		old_list.append(a)

old_score = len(old_list)	
old2_score = len(main_list1) - old_score

for a,b in main_list2:
	if a == b:
		similar_list.append(a)

similar_score = len(similar_list)	
similar2_score = len(main_list2) - similar_score

for a,b in main_list3:
	if a == b:
		new_list.append(a)

new_score = len(new_list)	
new2_score = len(main_list3) - new_score

#############################################################################################################################################################################################
with open(csv_file, "ab") as p:
	writer = csv.writer(p)
	writer.writerow(['All', '--', '--', '--', '--', '--', '--', mean_RT])
	writer.writerow(['Old', old_score, old2_score, numpy.round(old_score*100.0/(len(main_list1))), numpy.round(old2_score*100.0/(len(main_list1))), mean_RT_old_C, mean_RT_old_W, '--'])
	writer.writerow(['Similar', similar_score, similar2_score, numpy.round(similar_score*100.0/(len(main_list2))), numpy.round(similar2_score*100.0/(len(main_list2))), mean_RT_similar_C, mean_RT_similar_W, '--'])
	writer.writerow(['New', new_score, new2_score, numpy.round(new_score*100.0/(len(main_list3))), numpy.round(new2_score*100.0/(len(main_list3))), mean_RT_new_C, mean_RT_new_W, '--'])

