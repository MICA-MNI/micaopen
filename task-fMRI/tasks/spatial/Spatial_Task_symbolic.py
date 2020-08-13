from psychopy import gui, logging, visual, data, event, os, core
import numpy as np
from numpy.random import randint, shuffle, permutation
import random
from pdb import set_trace as bp
from psychopy.hardware.emulator import launchScan
import pickle
import csv
from PIL import Image
from itertools import permutations
import math
#
import PIL
from PIL import Image

###################################################################################################################################################################################
expName = "Spatial Task (symbolic)"
expInfo = {'subject name':'', 'session':'001', 'symbol list':['A','B','demo']}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)

if dlg.OK == False: core.quit()
expInfo['date'] = data.getDateStr()
expInfo['expName'] = expName

###################################################################################################################################################################################
myClock = core.Clock()
logging.setDefaultClock(myClock)

###################################################################################################################################################################################
if not os.path.isdir('data'):
	os.makedirs('data')

filename = 'tasks/spatial/data_Spatial Task (symbolic)/' + os.path.sep + '%s_%s' %(expInfo['subject name'], expInfo['date'])
logFile = logging.LogFile(filename + '.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)

###################################################################################################################################################################################
sans = ['Arial','Gill Sans MT', 'Helvetica','Verdana']
win = visual.Window(fullscr=True, color=1, units='height')

###################################################################################################################################################################################
csv_file = ("tasks/spatial/data_Spatial Task (symbolic)/" + expInfo['subject name'] + "_" + expInfo['session'] + "_" + expInfo['date'] + "_" +  expInfo['symbol list'] + ".csv")
with open(csv_file, "wb") as outcsv:
	writer = csv.writer(outcsv)
	writer.writerow(["Time", "Trial_Number", "Condition", "Fixation", "Fixation_Duration", "Prime", "Target", "Foil_1", "Foil_2", "Subject_Response", "Accuracy", "Reaction_Time"])

###################################################################################################################################################################################
msgTxt = visual.TextStim(win,text='default text', font=sans, name='message',
    height=float(0.04), wrapWidth=1100,
    color='black', 
    )

instrTxt = visual.TextStim(win,text='default text', font=sans, name='instruction',
    pos=[0,0], height=float(0.04), wrapWidth=100,
    color='black',
    ) #object to display instructions 

def instruction(inst_txt='tasks/spatial/Instructions/exp_instr_symbolic.txt'):
    Instruction = open(inst_txt, 'r').read().split('#\n')
    #
    for i, cur in enumerate(Instruction):
        instrTxt.setText(cur)
        instrTxt.draw()
        win.flip()
        event.waitKeys(keyList=['2','3','4'])

instruction(inst_txt='tasks/spatial/Instructions/exp_instr_symbolic.txt')

########################################################################
# settings for launchScan:
MR_settings = {
'TR': 0.585, # duration (sec) per volume
'volumes': 1500, # number of whole-brain 3D volumes / frames
'sync': '5', # character to use as the sync timing event; assumed to come at start of a volume
'skip': 0, # number of volumes lacking a sync pulse at start of scan (for T1 stabilization)
}

vol = launchScan(win, MR_settings, mode='Scan', globalClock=myClock.reset())

########################################################################
instrTxt.setText(open('tasks/spatial/Instructions/wait_trigger.txt', 'r').read())
instrTxt.draw()
win.flip()
core.wait(2)

########################################################################
fixation = visual.TextStim(win, name='fixation', text='+',
                            font= sans, height=float(0.08), pos=(0,0),color='black')

########################################################################
########################################################################
########################################################################
intg = 1.0/56 
spread_list = range(0,56)
pre_fix_dur_list = [x*intg for x in spread_list]
fix_dur_list = [x+2 for x in pre_fix_dur_list]
shuffle(fix_dur_list)
#
def fixation_screen(myClock):
    fixation.draw()
    win.logOnFlip(level=logging.EXP, msg='pre-stimulus fixation cross on screen') #
    win.flip()
    fixation_onset = myClock.getTime() #fixation cross onset
    
    if f == 14 or f == 28 or f == 42:
		core.wait(15)
    elif f == 0:
		core.wait(fix_dur_list[0])
    elif f == 1:
		core.wait(fix_dur_list[1])
    elif f == 2:
		core.wait(fix_dur_list[2])
    elif f == 3:
		core.wait(fix_dur_list[3])
    elif f == 4:
		core.wait(fix_dur_list[4])
    elif f == 5:
		core.wait(fix_dur_list[5])
    elif f == 6:
		core.wait(fix_dur_list[6])
    elif f == 7:
		core.wait(fix_dur_list[7])
    elif f == 8:
		core.wait(fix_dur_list[8])
    elif f == 9:
		core.wait(fix_dur_list[9])
    elif f == 10:
		core.wait(fix_dur_list[10])
    elif f == 11:
		core.wait(fix_dur_list[11])
    elif f == 12:
		core.wait(fix_dur_list[12])
    elif f == 13:
		core.wait(fix_dur_list[13])
    #elif f == 14:
	#	core.wait(fix_dur_list[14])
    elif f == 15:
		core.wait(fix_dur_list[15])
    elif f == 16:
		core.wait(fix_dur_list[16])
    elif f == 17:
		core.wait(fix_dur_list[17])
    elif f == 18:
		core.wait(fix_dur_list[18])
    elif f == 19:
		core.wait(fix_dur_list[19])
    elif f == 20:
		core.wait(fix_dur_list[20])
    elif f == 21:
		core.wait(fix_dur_list[21])
    elif f == 22:
		core.wait(fix_dur_list[22])
    elif f == 23:
		core.wait(fix_dur_list[23])
    elif f == 24:
		core.wait(fix_dur_list[24])
    elif f == 25:
		core.wait(fix_dur_list[25])
    elif f == 26:
		core.wait(fix_dur_list[26])
    elif f == 27:
		core.wait(fix_dur_list[27])
    #elif f == 28:
	#	core.wait(fix_dur_list[28])
    elif f == 29:
		core.wait(fix_dur_list[29])
    elif f == 30:
		core.wait(fix_dur_list[30])
    elif f == 31:
		core.wait(fix_dur_list[31])
    elif f == 32:
		core.wait(fix_dur_list[32])
    elif f == 33:
		core.wait(fix_dur_list[33])
    elif f == 34:
		core.wait(fix_dur_list[34])
    elif f == 35:
		core.wait(fix_dur_list[35])
    elif f == 36:
		core.wait(fix_dur_list[36])
    elif f == 37:
		core.wait(fix_dur_list[37])
    elif f == 38:
		core.wait(fix_dur_list[38])
    elif f == 39:
		core.wait(fix_dur_list[39])
    elif f == 40:
		core.wait(fix_dur_list[40])
    elif f == 41:
		core.wait(fix_dur_list[41])
    #elif f == 42:
	#	core.wait(fix_dur_list[42])
    elif f == 43:
		core.wait(fix_dur_list[43])
    elif f == 44:
		core.wait(fix_dur_list[44])
    elif f == 45:
		core.wait(fix_dur_list[45])
    elif f == 46:
		core.wait(fix_dur_list[46])
    elif f == 47:
		core.wait(fix_dur_list[47])
    elif f == 48:
		core.wait(fix_dur_list[48])
    elif f == 49:
		core.wait(fix_dur_list[49])
    elif f == 50:
		core.wait(fix_dur_list[50])
    elif f == 51:
		core.wait(fix_dur_list[51])
    elif f == 52:
		core.wait(fix_dur_list[52])
    elif f == 53:
		core.wait(fix_dur_list[53])
    elif f == 54:
		core.wait(fix_dur_list[54])
    elif f == 55:
		core.wait(fix_dur_list[55])
	#
    if event.getKeys(keyList=['escape']):
        core.quit()
    return fixation_onset
########################################################################
########################################################################
########################################################################

def prime_screen(myClock):
	#
	prime_im1.draw()
	prime_im2.draw()
	prime_im3.draw()
	#
	win.flip()
	#
	stimulus_onset = myClock.getTime() # stimulus onset
	#
	core.wait(4)
	return stimulus_onset
	
########################################################################
pre_fix_dur_list2 = [x*intg for x in spread_list]
fix_dur_list2 = [x+0.5 for x in pre_fix_dur_list2]
shuffle(fix_dur_list2)

def fixation_screen2(myClock):
	fixation.draw()
	win.logOnFlip(level=logging.EXP, msg='post-stimulus fixation cross on screen')
	win.flip()
	fixation_onset2 = myClock.getTime()
	#
	if f == 0:
		core.wait(fix_dur_list2[0])
	elif f == 1:
		core.wait(fix_dur_list2[1])
	elif f == 2:
		core.wait(fix_dur_list2[2])
	elif f == 3:
		core.wait(fix_dur_list2[3])
	elif f == 4:
		core.wait(fix_dur_list2[4])
	elif f == 5:
		core.wait(fix_dur_list2[5])
	elif f == 6:
		core.wait(fix_dur_list2[6])
	elif f == 7:
		core.wait(fix_dur_list2[7])
	elif f == 8:
		core.wait(fix_dur_list2[8])
	elif f == 9:
		core.wait(fix_dur_list2[9])
	elif f == 10:
		core.wait(fix_dur_list2[10])
	elif f == 11:
		core.wait(fix_dur_list2[11])
	elif f == 12:
		core.wait(fix_dur_list2[12])
	elif f == 13:
		core.wait(fix_dur_list2[13])
	elif f == 14:
		core.wait(fix_dur_list2[14])
	elif f == 15:
		core.wait(fix_dur_list2[15])
	elif f == 16:
		core.wait(fix_dur_list2[16])
	elif f == 17:
		core.wait(fix_dur_list2[17])
	elif f == 18:
		core.wait(fix_dur_list2[18])
	elif f == 19:
		core.wait(fix_dur_list2[19])
	elif f == 20:
		core.wait(fix_dur_list2[20])
	elif f == 21:
		core.wait(fix_dur_list2[21])
	elif f == 22:
		core.wait(fix_dur_list2[22])
	elif f == 23:
		core.wait(fix_dur_list2[23])
	elif f == 24:
		core.wait(fix_dur_list2[24])
	elif f == 25:
		core.wait(fix_dur_list2[25])
	elif f == 26:
		core.wait(fix_dur_list2[26])
	elif f == 27:
		core.wait(fix_dur_list2[27])
	elif f == 28:
		core.wait(fix_dur_list2[28])
	elif f == 29:
		core.wait(fix_dur_list2[29])
	elif f == 30:
		core.wait(fix_dur_list2[30])
	elif f == 31:
		core.wait(fix_dur_list2[31])
	elif f == 32:
		core.wait(fix_dur_list2[32])
	elif f == 33:
		core.wait(fix_dur_list2[33])
	elif f == 34:
		core.wait(fix_dur_list2[34])
	elif f == 35:
		core.wait(fix_dur_list2[35])
	elif f == 36:
		core.wait(fix_dur_list2[36])
	elif f == 37:
		core.wait(fix_dur_list2[37])
	elif f == 38:
		core.wait(fix_dur_list2[38])
	elif f == 39:
		core.wait(fix_dur_list2[39])
	elif f == 40:
		core.wait(fix_dur_list2[40])
	elif f == 41:
		core.wait(fix_dur_list2[41])
	elif f == 42:
		core.wait(fix_dur_list2[42])
	elif f == 43:
		core.wait(fix_dur_list2[43])
	elif f == 44:
		core.wait(fix_dur_list2[44])
	elif f == 45:
		core.wait(fix_dur_list2[45])
	elif f == 46:
		core.wait(fix_dur_list2[46])
	elif f == 47:
		core.wait(fix_dur_list2[47])
	elif f == 48:
		core.wait(fix_dur_list2[48])
	elif f == 49:
		core.wait(fix_dur_list2[49])
	elif f == 50:
		core.wait(fix_dur_list2[50])
	elif f == 51:
		core.wait(fix_dur_list2[51])
	elif f == 52:
		core.wait(fix_dur_list2[52])
	elif f == 53:
		core.wait(fix_dur_list2[53])
	elif f == 54:
		core.wait(fix_dur_list2[54])
	elif f == 55:
		core.wait(fix_dur_list2[55])
	#
	if event.getKeys(keyList=['escape']):
		core.quit()
	return fixation_onset2
########################################################################

def response_screen(myClock):
	#
	text_2.draw()
	text_3.draw()
	text_4.draw()
	#
	d1_im1.draw()
	d1_im2.draw()
	d1_im3.draw()
	#
	d2_im1.draw()
	d2_im2.draw()
	d2_im3.draw()
	#
	tg_im1.draw()
	tg_im2.draw()
	tg_im3.draw()
	#
	win.flip()
	screen_onset = myClock.getTime()
	#
	return screen_onset

##################### rotation function ################################
def triplet_rotation(origin,point,angle):
	ox, oy = origin
	px, py = point
	
	qx = ox + px*math.cos(angle) + py*math.sin(angle)
	qy = oy - px*math.sin(angle) + py*math.cos(angle)
	return qx, qy

#################################################################################################################################################################
trialList = data.importConditions("tasks/spatial/Spatial_symbolic/Spatial_List" + expInfo['symbol list'] + '.csv')

LIST = range(len(trialList))

triplet_list = zip(LIST,LIST,LIST) # creates a list of triplet items composed of list1, list2, and list3 items

##################################################################################
list_file = ("tasks/spatial/data_Spatial Task (symbolic)/" + expInfo['subject name'] + "_" + expInfo['session'] + "_" + expInfo['date'] + "_" +  expInfo['symbol list'])
with open(list_file, "wb") as fp:
	pickle.dump(triplet_list, fp)

################################################################################################################################################################################################

item_1 = [x[0] for x in triplet_list]
item_2 = [x[1] for x in triplet_list]
item_3 = [x[2] for x in triplet_list]
num = range(0,56)

###################### triangles #######################################

t1 = ((-0.3,-0.3),(0.3,-0.3),(0,0.3))
t2 = ((-0.3,-0.3),(0.3,-0.3),(0,0.28))
t3 = ((-0.3,-0.3),(0.3,-0.3),(0,0.26))
t4 = ((-0.3,-0.3),(0.3,-0.3),(0,0.24))
t5 = ((-0.3,-0.3),(0.3,-0.3),(0,0.22))
t6 = ((-0.3,-0.3),(0.3,-0.3),(0,0.2))
t7 = ((-0.3,-0.3),(0.3,-0.3),(0,0.18))
t8 = ((-0.3,-0.3),(0.3,-0.3),(0,0.16))
t9 = ((-0.3,-0.3),(0.3,-0.3),(0,0.14))
t10 = ((-0.3,-0.3),(0.3,-0.3),(0,0.12))
t11 = ((-0.3,-0.29),(0.3,-0.3),(0,0.3))
t12 = ((-0.3,-0.28),(0.3,-0.3),(0,0.28))
t13 = ((-0.3,-0.27),(0.3,-0.3),(0,0.26))
t14 = ((-0.3,-0.26),(0.3,-0.3),(0,0.24))
t15 = ((-0.3,-0.25),(0.3,-0.3),(0,0.22))
t16 = ((-0.3,-0.24),(0.3,-0.3),(0,0.2))
t17 = ((-0.3,-0.23),(0.3,-0.3),(0,0.18))
t18 = ((-0.3,-0.22),(0.3,-0.3),(0,0.16))
t19 = ((-0.3,-0.21),(0.3,-0.3),(0,0.14))
t20 = ((-0.3,-0.2),(0.3,-0.3),(0,0.12))
t21 = ((-0.3,-0.29),(0.2,-0.3),(0,0.3))
t22 = ((-0.3,-0.28),(0.21,-0.3),(0,0.28))
t23 = ((-0.3,-0.27),(0.22,-0.3),(0,0.26))
t24 = ((-0.3,-0.26),(0.23,-0.3),(0,0.24))
t25 = ((-0.3,-0.25),(0.24,-0.3),(0,0.22))
t26 = ((-0.3,-0.24),(0.25,-0.3),(0,0.2))
t27 = ((-0.3,-0.23),(0.26,-0.3),(0,0.18))
t28 = ((-0.3,-0.22),(0.27,-0.3),(0,0.16))
t29 = ((-0.3,-0.21),(0.28,-0.3),(0,0.14))
t30 = ((-0.3,-0.2),(0.29,-0.3),(0,0.12))
t31 = ((-0.3,-0.29),(0.2,-0.3),(0.29,0.3))
t32 = ((-0.3,-0.28),(0.21,-0.3),(0.28,0.28))
t33 = ((-0.3,-0.27),(0.22,-0.3),(0.27,0.26))
t34 = ((-0.3,-0.26),(0.23,-0.3),(0.26,0.24))
t35 = ((-0.3,-0.25),(0.24,-0.3),(0.25,0.22))
t36 = ((-0.3,-0.24),(0.25,-0.3),(0.24,0.2))
t37 = ((-0.3,-0.23),(0.26,-0.3),(0.23,0.18))
t38 = ((-0.3,-0.22),(0.27,-0.3),(0.22,0.16))
t39 = ((-0.3,-0.21),(0.28,-0.3),(0.21,0.14))
t40 = ((-0.3,-0.2),(0.29,-0.3),(0.2,0.12))
t41 = ((-0.2,-0.29),(0.2,-0.3),(0.29,0.3))
t42 = ((-0.21,-0.28),(0.21,-0.3),(0.28,0.28))
t43 = ((-0.22,-0.27),(0.22,-0.3),(0.27,0.26))
t44 = ((-0.23,-0.26),(0.23,-0.3),(0.26,0.24))
t45 = ((-0.24,-0.25),(0.24,-0.3),(0.25,0.22))
t46 = ((-0.25,-0.24),(0.25,-0.3),(0.24,0.2))
t47 = ((-0.26,-0.23),(0.26,-0.3),(0.23,0.18))
t48 = ((-0.27,-0.22),(0.27,-0.3),(0.22,0.16))
t49 = ((-0.28,-0.21),(0.28,-0.3),(0.21,0.14))
t50 = ((-0.29,-0.2),(0.29,-0.3),(0.2,0.12))
t51 = ((-0.295,-0.25),(0.295,-0.35),(0.25,0.125))
t52 = ((-0.275,-0.15),(0.275,-0.25),(0.15,0.125))
t53 = ((-0.275,-0.125),(0.285,-0.25),(0.15,0.125))
t54 = ((-0.215,-0.285),(0.215,-0.25),(0.28,0.115))
t55 = ((-0.215,-0.15),(0.255,-0.25),(0.28,0.12))
t56 = ((-0.22,-0.25),(0.255,-0.15),(0.15,0.12))

t_positions = [t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13,t14,t15,t16,t17,t18,t19,t20,t21,t22,t23,t24,t25,t26,t27,t28,t29,t30,t31,t32,t33,t34,t35,t36,t37,t38,t39,t40,t41,t42,t43,t44,t45,t46,t47,t48,t49,t50,t51,t52,t53,t54,t55,t56]
shuffle(t_positions)

if expInfo['symbol list'] == 'A':
	E_D = [22, 27, 12, 39, 7, 50, 45, 4, 23, 16, 48, 20, 44, 18, 35, 34, 25, 28, 31, 37, 47, 52, 17, 32, 2, 21, 11, 56, 6, 19, 55, 9, 24, 29, 8, 26, 46, 33, 1, 53, 30, 54, 13, 41, 10, 40, 43, 3, 49, 38, 36, 42, 15, 5, 14, 51]
elif expInfo['symbol list'] == 'B':
	E_D = [55, 23, 12, 10, 32, 15, 41, 39, 37, 6, 8, 21, 34, 48, 50, 30, 16, 42, 11, 25, 2, 26, 43, 29, 51, 5, 40, 53, 17, 27, 18, 24, 31, 13, 49, 38, 35, 22, 9, 1, 44, 20, 46, 47, 56, 4, 45, 52, 36, 54, 28, 14, 19, 7, 33, 3]
elif expInfo['symbol list'] == 'demo':
	E_D = [1, 2, 3, 4]

########################################################################
uber_list = zip(item_1, item_2, item_3, t_positions, E_D, num)

ang1 = range(1,46)
ang2 = range(315,360)
angle = list(set(ang1).union(ang2))

dis_mod = (-0.1, -0.05, 0.05, 0.1) #### distance modulation

for a,b,c,d,e,f in uber_list:
	
	### rotation angle & origin point for "triplet_rotation" function ##
	rotation_angle = random.choice(angle)
	origin_point = (0,0)

	############# PRIME ################################################
	####################################################################
	
	############################ prime positions #######################
	prime_pos1 = (d[0][0]*0.35, d[0][1]*0.35 + 0.25)
	prime_pos2 = (d[1][0]*0.35, d[1][1]*0.35 + 0.25)
	prime_pos3 = (d[2][0]*0.35, d[2][1]*0.35 + 0.25)
	
	################# open prime images ################################
	prime_im_a = Image.open(trialList[a]['stimulus_1'])
	prime_im_b = Image.open(trialList[b]['stimulus_2'])
	prime_im_c = Image.open(trialList[c]['stimulus_3'])
	
	######## perform orientation change on each prime item #############
	random_angleA = random.choice(angle)
	random_angleB = random.choice(angle)
	random_angleC = random.choice(angle)
	
	r_prime_im_a = prime_im_a.rotate(random_angleA, expand=True, resample=Image.BICUBIC)
	r_prime_im_b = prime_im_b.rotate(random_angleB, expand=True, resample=Image.BICUBIC)
	r_prime_im_c = prime_im_c.rotate(random_angleC, expand=True, resample=Image.BICUBIC)
	
	############## prepare for setting the oriented prime images #######
	prime_im1 = visual.ImageStim(win, name='stimPic1', image=None, pos=prime_pos1, size=0.175, units='height')
	prime_im2 = visual.ImageStim(win, name='stimPic2', image=None, pos=prime_pos2, size=0.175, units='height')
	prime_im3 = visual.ImageStim(win, name='stimPic3', image=None, pos=prime_pos3, size=0.175, units='height')
	
	############# center positions of tg, d1, and d2 ###################
	pos_val = [(-0.45,-0.25),(0,-0.25),(0.45,-0.25)]
	shuffle(pos_val)
	
	##### create permutations for change in distractor configuration ###
	prime_POS = (d[0], d[1], d[2])
	
	s = []
	for i in permutations(prime_POS):
		if i != prime_POS:
			s.append(i)
	print(set(s))
	
	permuted_list = list(set(s))
	
	choices = []
	for zzz in random.sample(range(0,5),2):
		choices.append(zzz)
	print choices

	#################### DISTRACTOR 1 ##################################
	####################################################################
	
	########### designate the d1 positions #############################
	if e % 2 == 0: ########### easy condition
		choice1 = choices[0]
		#
		d1_values = permuted_list[choice1] ### change configuration
		#
		d1_pos1 = (d1_values[0][0], d1_values[0][1] + random.choice(dis_mod)) ### change distances between items
		d1_pos2 = (d1_values[1][0] + random.choice(dis_mod), d1_values[1][1])
		d1_pos3 = (d1_values[2][0], d1_values[2][1] + random.choice(dis_mod))
	elif e % 2 > 0: ######### difficult condition
		d1_pos1 = (d[0][0], d[0][1] + random.choice(dis_mod)) ### only change distances between items; keep same configuration as prime
		d1_pos2 = (d[1][0] + random.choice(dis_mod), d[1][1])
		d1_pos3 = (d[2][0], d[2][1] + random.choice(dis_mod))

	############# open d1 images #######################################
	d1_im_a = Image.open(trialList[a]['stimulus_1'])
	d1_im_b = Image.open(trialList[b]['stimulus_2'])
	d1_im_c = Image.open(trialList[c]['stimulus_3'])

	######## perform orientation change on each d1 item ################
	r_d1_im_a = d1_im_a.rotate(random_angleA - rotation_angle, expand=True, resample=Image.BICUBIC)
	r_d1_im_b = d1_im_b.rotate(random_angleB - rotation_angle, expand=True, resample=Image.BICUBIC)
	r_d1_im_c = d1_im_c.rotate(random_angleC - rotation_angle, expand=True, resample=Image.BICUBIC)
	
	####################### rotate all d1 items about origin ###########
	r_d1_pos1 = triplet_rotation(origin_point, d1_pos1, math.radians(rotation_angle))
	r_d1_pos2 = triplet_rotation(origin_point, d1_pos2, math.radians(rotation_angle))
	r_d1_pos3 = triplet_rotation(origin_point, d1_pos3, math.radians(rotation_angle))
	
	#################### reposition d1 items for display ###############
	d1_bla1 = (r_d1_pos1[0]*0.35 + pos_val[0][0], r_d1_pos1[1]*0.35 + pos_val[0][1])
	d1_bla2 = (r_d1_pos2[0]*0.35 + pos_val[0][0], r_d1_pos2[1]*0.35 + pos_val[0][1])
	d1_bla3 = (r_d1_pos3[0]*0.35 + pos_val[0][0], r_d1_pos3[1]*0.35 + pos_val[0][1])
	
	######################### DISTRACTOR 2 #############################
	####################################################################
	
	######### designate the d2 positions ###############################
	if e % 2 == 0: ########### easy condition
		choice2 = choices[1]
		#
		d2_values = permuted_list[choice2]
		#
		d2_pos1 = (d2_values[0][0], d2_values[0][1] + random.choice(dis_mod))
		d2_pos2 = (d2_values[1][0] + random.choice(dis_mod), d2_values[1][1])
		d2_pos3 = (d2_values[2][0], d2_values[2][1] + random.choice(dis_mod))
	elif e % 2 > 0: ######### difficult condition
		d2_pos1 = (d[0][0], d[0][1] + random.choice(dis_mod))
		d2_pos2 = (d[1][0] + random.choice(dis_mod), d[1][1])
		d2_pos3 = (d[2][0], d[2][1] + random.choice(dis_mod))

	######## open d2 images ############################################
	d2_im_a = Image.open(trialList[a]['stimulus_1'])
	d2_im_b = Image.open(trialList[b]['stimulus_2'])
	d2_im_c = Image.open(trialList[c]['stimulus_3'])
	
	####### perform orientation change on each d2 item #################
	r_d2_im_a = d2_im_a.rotate(random_angleA - rotation_angle, expand=True, resample=Image.BICUBIC)
	r_d2_im_b = d2_im_b.rotate(random_angleB - rotation_angle, expand=True, resample=Image.BICUBIC)
	r_d2_im_c = d2_im_c.rotate(random_angleC - rotation_angle, expand=True, resample=Image.BICUBIC)
	
	########### rotate all d2 items about origin #######################
	r_d2_pos1 = triplet_rotation(origin_point, d2_pos1, math.radians(rotation_angle))
	r_d2_pos2 = triplet_rotation(origin_point, d2_pos2, math.radians(rotation_angle))
	r_d2_pos3 = triplet_rotation(origin_point, d2_pos3, math.radians(rotation_angle))
	
	######## reposition d2 items for display ###########################
	d2_bla1 = (r_d2_pos1[0]*0.35 + pos_val[1][0], r_d2_pos1[1]*0.35 + pos_val[1][1])
	d2_bla2 = (r_d2_pos2[0]*0.35 + pos_val[1][0], r_d2_pos2[1]*0.35 + pos_val[1][1])
	d2_bla3 = (r_d2_pos3[0]*0.35 + pos_val[1][0], r_d2_pos3[1]*0.35 + pos_val[1][1])
	
	######################### TARGET ###################################
	####################################################################
	
	######## target positions = prime positions ########################
	tg_pos1 = d[0]
	tg_pos2 = d[1]
	tg_pos3 = d[2]
	
	############### open tg images #####################################
	tg_im_a = Image.open(trialList[a]['stimulus_1'])
	tg_im_b = Image.open(trialList[b]['stimulus_2'])
	tg_im_c = Image.open(trialList[c]['stimulus_3'])
	
	############# perform orientation change on each tg item ###########
	r_tg_im_a = tg_im_a.rotate(random_angleA - rotation_angle, expand=True, resample=Image.BICUBIC)
	r_tg_im_b = tg_im_b.rotate(random_angleB - rotation_angle, expand=True, resample=Image.BICUBIC)
	r_tg_im_c = tg_im_c.rotate(random_angleC - rotation_angle, expand=True, resample=Image.BICUBIC)
	
	########## rotate all tg items about origin ########################
	r_tg_pos1 = triplet_rotation(origin_point, tg_pos1, math.radians(rotation_angle))
	r_tg_pos2 = triplet_rotation(origin_point, tg_pos2, math.radians(rotation_angle))
	r_tg_pos3 = triplet_rotation(origin_point, tg_pos3, math.radians(rotation_angle))
	
	########### reposition tg items for display ########################
	tg_bla1 = (r_tg_pos1[0]*0.35 + pos_val[2][0], r_tg_pos1[1]*0.35 + pos_val[2][1])
	tg_bla2 = (r_tg_pos2[0]*0.35 + pos_val[2][0], r_tg_pos2[1]*0.35 + pos_val[2][1])
	tg_bla3 = (r_tg_pos3[0]*0.35 + pos_val[2][0], r_tg_pos3[1]*0.35 + pos_val[2][1])
	
	########## PRIME PRESENTATION ######################################
	####################################################################
	
	######### pre-stim + ###############################################
	fixStart = fixation_screen(myClock) # to record fixation onset
	
	####### set prime images ###########################################
	prime_im1.setImage(r_prime_im_a)
	prime_im2.setImage(r_prime_im_b)
	prime_im3.setImage(r_prime_im_c)
	
	########## get prime stim onset time ###############################
	prime_Start = prime_screen(myClock)
	
	######## clear screen ##############################################
	event.clearEvents()
	
	############# post-stim + ##########################################
	fixStart2 = fixation_screen2(myClock)
	
	#################################################################### RESPONSE SCREEN ##########################################################################################################################
	###############################################################################################################################################################################################################
	
	text_2 = visual.TextStim(win, text='2', font=sans, name='instruction', pos=[-0.4423,0], height=float(0.04), wrapWidth=1100, color='black')
	text_3 = visual.TextStim(win, text='3', font=sans, name='instruction', pos=[0,0], height=float(0.04), wrapWidth=1100, color='black')
	text_4 = visual.TextStim(win, text='4', font=sans, name='instruction', pos=[0.4423,0], height=float(0.04), wrapWidth=1100, color='black')

	####################################################################
	d1_im1 = visual.ImageStim(win, name='stimPic1', image=r_d1_im_a, pos=d1_bla1, size=(0.175*(r_d1_im_a.size[0]*(1.0/r_prime_im_a.size[0])),0.175*(r_d1_im_a.size[1]*(1.0/r_prime_im_a.size[1]))), units='height')
	d1_im2 = visual.ImageStim(win, name='stimPic2', image=r_d1_im_b, pos=d1_bla2, size=(0.175*(r_d1_im_b.size[0]*(1.0/r_prime_im_b.size[0])),0.175*(r_d1_im_b.size[1]*(1.0/r_prime_im_b.size[1]))), units='height')
	d1_im3 = visual.ImageStim(win, name='stimPic3', image=r_d1_im_c, pos=d1_bla3, size=(0.175*(r_d1_im_c.size[0]*(1.0/r_prime_im_c.size[0])),0.175*(r_d1_im_c.size[1]*(1.0/r_prime_im_c.size[1]))), units='height')
	#
	d2_im1 = visual.ImageStim(win, name='stimPic1', image=r_d2_im_a, pos=d2_bla1, size=(0.175*(r_d2_im_a.size[0]*(1.0/r_prime_im_a.size[0])),0.175*(r_d2_im_a.size[1]*(1.0/r_prime_im_a.size[1]))), units='height')
	d2_im2 = visual.ImageStim(win, name='stimPic2', image=r_d2_im_b, pos=d2_bla2, size=(0.175*(r_d2_im_b.size[0]*(1.0/r_prime_im_b.size[0])),0.175*(r_d2_im_b.size[1]*(1.0/r_prime_im_b.size[1]))), units='height')
	d2_im3 = visual.ImageStim(win, name='stimPic3', image=r_d2_im_c, pos=d2_bla3, size=(0.175*(r_d2_im_c.size[0]*(1.0/r_prime_im_c.size[0])),0.175*(r_d2_im_c.size[1]*(1.0/r_prime_im_c.size[1]))), units='height')
	#
	tg_im1 = visual.ImageStim(win, name='stimPic1', image=r_tg_im_a, pos=tg_bla1, size=(0.175*(r_tg_im_a.size[0]*(1.0/r_prime_im_a.size[0])),0.175*(r_tg_im_a.size[1]*(1.0/r_prime_im_a.size[1]))), units='height')
	tg_im2 = visual.ImageStim(win, name='stimPic2', image=r_tg_im_b, pos=tg_bla2, size=(0.175*(r_tg_im_b.size[0]*(1.0/r_prime_im_b.size[0])),0.175*(r_tg_im_b.size[1]*(1.0/r_prime_im_b.size[1]))), units='height')
	tg_im3 = visual.ImageStim(win, name='stimPic3', image=r_tg_im_c, pos=tg_bla3, size=(0.175*(r_tg_im_c.size[0]*(1.0/r_prime_im_c.size[0])),0.175*(r_tg_im_c.size[1]*(1.0/r_prime_im_c.size[1]))), units='height')
	
	######## get onset time of response screen #########################
	response_Start = response_screen(myClock)
	
	###### get response ################################################
	#
	trialEndTime = response_Start + 5.5
	#
	flag = 0
	keyList = []
	#################
	event.clearEvents()
	#################
	while myClock.getTime() < trialEndTime:
		keypress = event.getKeys(keyList=['2','3','4'])
		if len(keypress) == 1 and flag == 0:
			keyList = keypress[0]
			flag = 1
			keyStart = myClock.getTime()
	#
	if len(keyList) == 1 and flag == 1:	
		key_pressed = keyList[0]
		RT = keyStart - response_Start
	else:
		keyStart = '--'
		RT = 'N/A'
	#
	
	event.clearEvents()

	###############################################################################################################################################################################################################
	###############################################################################################################################################################################################################
	
	####################################################################
	trial_num = range(1,57)[f] # to record trial number
	
	####################################################################
	prime_display = os.path.basename(os.path.normpath(trialList[a]['stimulus_1'])), os.path.basename(os.path.normpath(trialList[b]['stimulus_2'])), os.path.basename(os.path.normpath(trialList[c]['stimulus_3']))
	
	if tg_bla1 == (r_tg_pos1[0]*0.35 + -0.45, r_tg_pos1[1]*0.35 + -0.25):
		Tg_A = 'left'
	elif d1_bla1 == (r_d1_pos1[0]*0.35 + -0.45, r_d1_pos1[1]*0.35 + -0.25):
		D1_A = 'left'
	elif d2_bla1 == (r_d2_pos1[0]*0.35 + -0.45, r_d2_pos1[1]*0.35 + -0.25):
		D2_A = 'left'
	
	if tg_bla1 == (r_tg_pos1[0]*0.35, r_tg_pos1[1]*0.35 + -0.25):
		Tg_A = 'center'
	elif d1_bla1 == (r_d1_pos1[0]*0.35, r_d1_pos1[1]*0.35 + -0.25):
		D1_A = 'center'
	elif d2_bla1 == (r_d2_pos1[0]*0.35, r_d2_pos1[1]*0.35 + -0.25):
		D2_A = 'center' 
	
	if tg_bla1 == (r_tg_pos1[0]*0.35 + 0.45, r_tg_pos1[1]*0.35 + -0.25):
		Tg_A = 'right'
	elif d1_bla1 == (r_d1_pos1[0]*0.35 + 0.45, r_d1_pos1[1]*0.35 + -0.25):
		D1_A = 'right'
	elif d2_bla1 == (r_d2_pos1[0]*0.35 + 0.45, r_d2_pos1[1]*0.35 + -0.25):
		D2_A = 'right'
		
	######## to determine the condition (i.e. E vs D) ##################
	### even number = E; odd numer = D ########
	if e % 2 == 0:
		condition = 'E'	
	elif e % 2 > 0:
		condition = 'D'
	####################################################################

	if RT == 'N/A':
		SR = 'N/A'
	elif RT < 5.5:
		if key_pressed == '2':
			SR = 'left'
		elif key_pressed == '3':
			SR = 'center'
		elif key_pressed == '4':
			SR = 'right'
	####################################################################
	if SR == Tg_A:
		Acc = '1'
	elif SR != Tg_A:
		Acc = '0'
	####################################################################
	with open(csv_file, "ab") as p:
		writer = csv.writer(p)
		writer.writerow([fixStart, trial_num, condition, 'ON', prime_Start-fixStart, '--', '--', '--', '--', '--', '--', '--'])
		writer.writerow([prime_Start, trial_num, condition, 'OFF', '--', prime_display, '--', '--', '--', '--', '--', '--'])
		writer.writerow([fixStart2, trial_num, condition, 'ON', response_Start-fixStart2, '--', '--', '--', '--', '--', '--', '--'])
		writer.writerow([response_Start, trial_num, condition, '--', '--', '--', Tg_A, D1_A, D2_A, '--', '--', '--'])
		writer.writerow([keyStart, trial_num, condition, '--', '--', '--', '--', '--', '--', SR, Acc, '--'])
		writer.writerow(['--', trial_num, condition, '--', '--', '--', '--', '--', '--', '--', '--', RT])
		writer.writerow(['', '', '', '', '', '', '', '', '', '', '', ''])

def end(end_txt='tasks/spatial/Instructions/end_instr.txt'):
    End = open(end_txt, 'r').read().split('#\n')
    for i, cur in enumerate(End):
        msgTxt.setText(cur)
        msgTxt.draw()
        win.flip()
        #
        thank_you = myClock.getTime()
        #
        with open(csv_file, "ab") as f:
			writer = csv.writer(f)
			writer.writerow([thank_you, '--', 'End message', '--', '--', '--', '--'])
        #
        event.waitKeys(keyList=['space'])
        win.close()
        core.quit()

end(end_txt='tasks/spatial/Instructions/end_instr.txt')

###################################################################################################################################################################################

