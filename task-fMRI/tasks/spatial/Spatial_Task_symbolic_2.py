from psychopy import gui, logging, visual, data, event, os, core
import numpy as np
from numpy.random import randint, shuffle, permutation
import random
from pdb import set_trace as bp
from psychopy.hardware.emulator import launchScan
import pickle
import csv
from PIL import Image
#from itertools import permutations
import math

###################################################################################################################################################################################
expName = "Spatial Task (symbolic)"
expInfo = {'subject name':'', 'session':'001', 'symbol list':['A','B']}
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
#win = visual.Window(fullscr=True, color=1, units='norm')
win = visual.Window(size=(1366, 768), fullscr=True, color=1, units='height')

###################################################################################################################################################################################

# settings for launchScan:
MR_settings = {
'TR': 0.585, # duration (sec) per volume
'volumes': 1500, # number of whole-brain 3D volumes / frames
'sync': 'q', # character to use as the sync timing event; assumed to come at start of a volume
'skip': 0, # number of volumes lacking a sync pulse at start of scan (for T1 stabilization)
}

vol = launchScan(win, MR_settings, mode='Scan', globalClock=myClock.reset())

###################################################################################################################################################################################
csv_file = ("tasks/spatial/data_Spatial Task (symbolic)/" + expInfo['subject name'] + "_" + expInfo['session'] + "_" + expInfo['date'] + "_" +  expInfo['symbol list'] + ".csv")
with open(csv_file, "wb") as outcsv:
	writer = csv.writer(outcsv)
	writer.writerow(["Time", "Trial_Number", "Condition", "Fixation", "Prime", "Target", "Distractor_1", "Distractor_2", "Subject_Response", "Reaction_Time" ])

###################################################################################################################################################################################
msgTxt = visual.TextStim(win,text='default text', font=sans, name='message',
    #height=float(0.07), wrapWidth=1100,
    height=float(0.04), wrapWidth=1100,
    color='black', 
    )

instrTxt = visual.TextStim(win,text='default text', font=sans, name='instruction',
    #pos=[0,0], height=float(0.07), wrapWidth=100,
    pos=[0,0], height=float(0.04), wrapWidth=100,
    color='black',
    ) #object to display instructions 

def instruction(inst_txt='tasks/spatial/Instructions/exp_instr_symbolic.txt'):
    Instruction = open(inst_txt, 'r').read().split('#\n')
    Ready = open('tasks/spatial/Instructions/wait_trigger.txt', 'r').read()
    for i, cur in enumerate(Instruction):
        instrTxt.setText(cur)
        instrTxt.draw()
        win.flip()
        event.waitKeys(keyList=['space'])
    
    instrTxt.setText(Ready)
    instrTxt.draw()
    win.flip()
    event.waitKeys(maxWait = 2)

instruction(inst_txt='tasks/spatial/Instructions/exp_instr_symbolic.txt')

########################################################################
fixation = visual.TextStim(win, name='fixation', text='+', 
                            #font= sans, height=float(0.15), pos=(0,0),color='black')
                            font= sans, height=float(0.08), pos=(0,0),color='black')

def fixation_screen(myClock):
    fixation.draw()
    win.logOnFlip(level=logging.EXP, msg='pre-stimulus fixation cross on screen') #new log haoting
    win.flip()
    fixation_onset = myClock.getTime() #fixation cross onset
    core.wait(np.arange(1.3, 1.75, 0.05)[randint(0,9)])
    if event.getKeys(keyList=['escape']):
        core.quit()
    return fixation_onset

def prime_screen(myClock):
	prime_im1.draw()
	prime_im2.draw()
	prime_im3.draw()
	win.flip()
	stimulus_onset = myClock.getTime() # stimulus onset
	core.wait(2.5)
	return stimulus_onset

def fixation_screen2(myClock):
	fixation.draw()
	win.logOnFlip(level=logging.EXP, msg='post-stimulus fixation cross on screen')
	win.flip()
	fixation_onset2 = myClock.getTime()
	core.wait(np.arange(0.5,1,0.05)[randint(0,10)])
	if event.getKeys(keyList=['escape']):
		core.quit()
	return fixation_onset2

separator_1 = visual.TextStim(win, name='separator1', text='__________________',
                            font= sans, height=float(0.08), pos=(0,0.04),color='green')

separator_1a = visual.TextStim(win, name='separator1', text='________________',
                            font= sans, height=float(0.08), pos=(-0.66,0.04),color='green')

separator_1b = visual.TextStim(win, name='separator1', text='________________',
                            font= sans, height=float(0.08), pos=(0.66,0.04),color='green')

separator_2 = visual.TextStim(win, name='separator2', text='|',
                            font= sans, height=float(0.08), pos=(-0.2995,-0.05),color='green')

separator_3 = visual.TextStim(win, name='separator3', text='|',
                            font= sans, height=float(0.08), pos=(-0.2995,-0.15),color='green')

separator_4 = visual.TextStim(win, name='separator4', text='|',
                            font= sans, height=float(0.08), pos=(-0.2995,-0.25),color='green')

separator_5 = visual.TextStim(win, name='separator5', text='|',
                            font= sans, height=float(0.08), pos=(-0.2995,-0.35),color='green')

separator_6 = visual.TextStim(win, name='separator6', text='|',
                            font= sans, height=float(0.08), pos=(-0.2995,-0.45),color='green')

separator_7 = visual.TextStim(win, name='separator7', text='|',
                            font= sans, height=float(0.08), pos=(0.2995,-0.05),color='green')

separator_8 = visual.TextStim(win, name='separator8', text='|',
                            font= sans, height=float(0.08), pos=(0.2995,-0.15),color='green')

separator_9 = visual.TextStim(win, name='separator9', text='|',
                            font= sans, height=float(0.08), pos=(0.2995,-0.25),color='green')

separator_10 = visual.TextStim(win, name='separator10', text='|',
                            font= sans, height=float(0.08), pos=(0.2995,-0.35),color='green')

separator_11 = visual.TextStim(win, name='separator11', text='|',
                            font= sans, height=float(0.08), pos=(0.2995,-0.45),color='green')

def response_screen(myClock):
	separator_1.draw()
	separator_1a.draw()
	separator_1b.draw()
	separator_2.draw()
	separator_3.draw()
	separator_4.draw()
	separator_5.draw()
	separator_6.draw()
	separator_7.draw()
	separator_8.draw()
	separator_9.draw()
	separator_10.draw()
	separator_11.draw()
	#
	s_prime_im1.draw()
	s_prime_im2.draw()
	s_prime_im3.draw()
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

########################################################################
def key_press_time(myClock):
	key_press_onset = myClock.getTime()
	return key_press_onset

##################### rotation function ################################
def triplet_rotation(origin,point,angle):
	ox, oy = origin
	px, py = point
	
	qx = ox + px*math.cos(angle) + py*math.sin(angle)
	qy = oy - px*math.sin(angle) + py*math.cos(angle)
	return qx, qy

#################################################################################################################################################################
trialList = data.importConditions("tasks/spatial/Spatial_symbolic/Spatial_List" + expInfo['symbol list'] + '.csv')

list1 = random.sample(range(0,len(trialList)),len(trialList)) # creates a list containing randomized items for one set of stimuli (i.e., stimulus_1) 
list2 = random.sample(range(0,len(trialList)),len(trialList)) # creates a list containing randomized items for another set of stimuli (i.e., stimulus_2)
list3 = random.sample(range(0,len(trialList)),len(trialList)) # creates a list containing randomized items for another set of stimuli (i.e., stimulus_3)
triplet_list = zip(list1,list2,list3) # creates a list of triplet items composed of list1, list2, and list3 items

##################################################################################
list_file = ("tasks/spatial/data_Spatial Task (symbolic)/" + expInfo['subject name'] + "_" + expInfo['session'] + "_" + expInfo['date'] + "_" +  expInfo['symbol list'])
with open(list_file, "wb") as fp:
	pickle.dump(triplet_list, fp)

################################################################################################################################################################################################
shuffle(triplet_list) # shuffles the triplet items within triplet_list
item_1 = [x[0] for x in triplet_list]
item_2 = [x[1] for x in triplet_list]
item_3 = [x[2] for x in triplet_list]
num = range(0,50)

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

#t_positions = [t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13,t14,t15,t16,t17,t18,t19,t20,t21,t22,t23,t24,t25,t26,t27,t28,t29,t30,t31,t32,t33,t34,t35,t36,t37,t38,t39,t40,t41,t42,t43,t44,t45,t46,t47,t48,t49,t50]
t_positions = [t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13,t14,t15,t16,t17,t18,t19,t20,t21,t22,t23,t24,t25,t26,t27,t28,t29,t30]
shuffle(t_positions)

E_D = range(1,51)
shuffle(E_D)
########################################################################
uber_list = zip(item_1, item_2, item_3, t_positions, E_D, num)

angle = range(1,360)

os.chdir("/home/mica/Desktop/python/fMRIBatteryMay2017/")

for a,b,c,d,e,f in uber_list:
	
	### rotation angle & origin point for "triplet_rotation" function ##
	rotation_angle = random.choice(angle)
	origin_point = (0,0)
	
	############# PRIME ################################################
	####################################################################
	
	############################ prime positions #######################
	prime_pos1 = d[0]
	prime_pos2 = d[1]
	prime_pos3 = d[2]
	
	################ orientation angles for each prime item ############
	random_angleA = random.choice(angle)
	random_angleB = random.choice(angle)
	random_angleC = random.choice(angle)
	
	################# open prime images ################################
	prime_im_a = Image.open(trialList[a]['stimulus_1'])
	prime_im_b = Image.open(trialList[b]['stimulus_2'])
	prime_im_c = Image.open(trialList[c]['stimulus_3'])
	
	########## perform orientation change on each prime item ###########
	r_prime_im_a = prime_im_a.rotate(random_angleA, expand=True)
	r_prime_im_b = prime_im_b.rotate(random_angleB, expand=True)
	r_prime_im_c = prime_im_c.rotate(random_angleC, expand=True)
	
	############## prepare for setting the oriented prime images #######
	prime_im1 = visual.ImageStim(win, name='stimPic1', image=None, pos=prime_pos1, units='height')
	prime_im2 = visual.ImageStim(win, name='stimPic2', image=None, pos=prime_pos2, units='height')
	prime_im3 = visual.ImageStim(win, name='stimPic3', image=None, pos=prime_pos3, units='height')
	
	########### make list of prime positions ###########################
	prime_POS = (prime_pos1,prime_pos2,prime_pos3)
	
	############# center positions of tg, d1, and d2 ###################
	pos_val = [(-0.5935,-0.25),(0,-0.25),(0.5935,-0.25)]
	shuffle(pos_val)
	
	#################### DISTRACTOR 1 ##################################
	####################################################################
	
	########### designate the d1 positions #############################	
	d1_pos1 = prime_pos1
	d1_pos2 = prime_pos2
	d1_pos3 = prime_pos3
	
	############# orientation angles for each d1 item ##################
	#
	E_angle = range(60,90) 
	D_angle = range(10,15)
	#
	if e % 2 == 0:
		ANGLE = E_angle
	elif e % 2 >= 0:
		ANGLE = D_angle
	#
	random_angle1_d1 = []
	xxx = random.choice(ANGLE)
	while xxx in [random_angleA]:
		xxx = random.choice(ANGLE)
	random_angle1_d1.append(xxx)
	#
	random_angle2_d1 = []
	xxy = random.choice(ANGLE)
	while xxy in [random_angleB]:
		xxy = random.choice(ANGLE)
	random_angle2_d1.append(xxy)
	#
	random_angle3_d1 = []
	xyy = random.choice(ANGLE)
	while xyy in [random_angleC]:
		xyy = random.choice(ANGLE)
	random_angle3_d1.append(xyy)
	
	############# open d1 images #######################################
	d1_im_a = Image.open(trialList[a]['stimulus_1'])
	d1_im_b = Image.open(trialList[b]['stimulus_2'])
	d1_im_c = Image.open(trialList[c]['stimulus_3'])
	
	######## perform orientation change on each d1 item ################
	r_d1_im_a = d1_im_a.rotate(random_angle1_d1[0] - rotation_angle, expand=True)
	r_d1_im_b = d1_im_b.rotate(random_angle2_d1[0] - rotation_angle, expand=True)
	r_d1_im_c = d1_im_c.rotate(random_angle3_d1[0] - rotation_angle, expand=True)
	
	####################### rotate all d1 items about origin ###########
	r_d1_pos1 = triplet_rotation(origin_point, d1_pos1, math.radians(rotation_angle))
	r_d1_pos2 = triplet_rotation(origin_point, d1_pos2, math.radians(rotation_angle))
	r_d1_pos3 = triplet_rotation(origin_point, d1_pos3, math.radians(rotation_angle))
	
	#################### reposition d1 items for display ###############
	d1_bla1 = (r_d1_pos1[0]*0.25 + pos_val[0][0], r_d1_pos1[1]*0.25 + pos_val[0][1])
	d1_bla2 = (r_d1_pos2[0]*0.25 + pos_val[0][0], r_d1_pos2[1]*0.25 + pos_val[0][1])
	d1_bla3 = (r_d1_pos3[0]*0.25 + pos_val[0][0], r_d1_pos3[1]*0.25 + pos_val[0][1])
	
	######################### DISTRACTOR 2 #############################
	####################################################################
	
	######### designate the d2 positions ###############################
	d2_pos1 = prime_pos1
	d2_pos2 = prime_pos2
	d2_pos3 = prime_pos3
	
	############ orientation angels for each d2 item ###################
	#
	E_angle = range(45,90) 
	D_angle = range(5,15)
	#
	if e % 2 == 0:
		ANGLE = E_angle
	elif e % 2 >= 0:
		ANGLE = D_angle
	#
	random_angle1_d2 = []
	yyy = random.choice(ANGLE)
	while yyy in [random_angleA]:
		yyy = random.choice(ANGLE)
	random_angle1_d2.append(yyy)
	#
	random_angle2_d2 = []
	yyx = random.choice(ANGLE)
	while yyx in [random_angleB]:
		yyx = random.choice(ANGLE)
	random_angle2_d2.append(yyx)	
	#
	random_angle3_d2 = []
	yxx = random.choice(ANGLE)
	while yxx in [random_angleC]:
		yxx = random.choice(ANGLE)
	random_angle3_d2.append(yxx)
	
	######## open d2 images ############################################
	d2_im_a = Image.open(trialList[a]['stimulus_1'])
	d2_im_b = Image.open(trialList[b]['stimulus_2'])
	d2_im_c = Image.open(trialList[c]['stimulus_3'])
	
	####### perform orientation change on each d2 item #################
	r_d2_im_a = d2_im_a.rotate(random_angle1_d2[0] - rotation_angle, expand=True)
	r_d2_im_b = d2_im_b.rotate(random_angle2_d2[0] - rotation_angle, expand=True)
	r_d2_im_c = d2_im_c.rotate(random_angle3_d2[0] - rotation_angle, expand=True)
	
	########### rotate all d2 items about origin #######################
	r_d2_pos1 = triplet_rotation(origin_point, d2_pos1, math.radians(rotation_angle))
	r_d2_pos2 = triplet_rotation(origin_point, d2_pos2, math.radians(rotation_angle))
	r_d2_pos3 = triplet_rotation(origin_point, d2_pos3, math.radians(rotation_angle))
	
	######## reposition d2 items for display ###########################
	d2_bla1 = (r_d2_pos1[0]*0.25 + pos_val[1][0], r_d2_pos1[1]*0.25 + pos_val[1][1])
	d2_bla2 = (r_d2_pos2[0]*0.25 + pos_val[1][0], r_d2_pos2[1]*0.25 + pos_val[1][1])
	d2_bla3 = (r_d2_pos3[0]*0.25 + pos_val[1][0], r_d2_pos3[1]*0.25 + pos_val[1][1])
	
	######################### TARGET ###################################
	####################################################################
	
	######## target positions = prime positions ########################
	tg_pos1 = prime_pos1
	tg_pos2 = prime_pos2
	tg_pos3 = prime_pos3
	
	############### open tg images #####################################
	tg_im_a = Image.open(trialList[a]['stimulus_1'])
	tg_im_b = Image.open(trialList[b]['stimulus_2'])
	tg_im_c = Image.open(trialList[c]['stimulus_3'])
	
	############# perform orientation change on each tg item ###########
	r_tg_im_a = tg_im_a.rotate(random_angleA - rotation_angle, expand=True)
	r_tg_im_b = tg_im_b.rotate(random_angleB - rotation_angle, expand=True)
	r_tg_im_c = tg_im_c.rotate(random_angleC - rotation_angle, expand=True)
	
	########## rotate all tg items about origin ########################
	r_tg_pos1 = triplet_rotation(origin_point, tg_pos1, math.radians(rotation_angle))
	r_tg_pos2 = triplet_rotation(origin_point, tg_pos2, math.radians(rotation_angle))
	r_tg_pos3 = triplet_rotation(origin_point, tg_pos3, math.radians(rotation_angle))
	
	########### reposition tg items for display ########################
	tg_bla1 = (r_tg_pos1[0]*0.25 + pos_val[2][0], r_tg_pos1[1]*0.25 + pos_val[2][1])
	tg_bla2 = (r_tg_pos2[0]*0.25 + pos_val[2][0], r_tg_pos2[1]*0.25 + pos_val[2][1])
	tg_bla3 = (r_tg_pos3[0]*0.25 + pos_val[2][0], r_tg_pos3[1]*0.25 + pos_val[2][1])
	
	######################### small PRIME ##############################
	####################################################################
	
	######## perform orientation change on each s_prime item ###########	
	s_r_prime_im_a = prime_im_a.rotate(random_angleA - rotation_angle, expand=True)
	s_r_prime_im_b = prime_im_b.rotate(random_angleB - rotation_angle, expand=True)
	s_r_prime_im_c = prime_im_c.rotate(random_angleC - rotation_angle, expand=True)
	
	###################### rotate all s_prime items about origin #######
	s_r_prime_pos1 = triplet_rotation(origin_point, prime_pos1, math.radians(rotation_angle))
	s_r_prime_pos2 = triplet_rotation(origin_point, prime_pos2, math.radians(rotation_angle))
	s_r_prime_pos3 = triplet_rotation(origin_point, prime_pos3, math.radians(rotation_angle))
	
	########### reposition s_prime items for display ###################
	s_prime_bla1 = (s_r_prime_pos1[0]*0.25, s_r_prime_pos1[1]*0.25 + 0.25)
	s_prime_bla2 = (s_r_prime_pos2[0]*0.25, s_r_prime_pos2[1]*0.25 + 0.25)
	s_prime_bla3 = (s_r_prime_pos3[0]*0.25, s_r_prime_pos3[1]*0.25 + 0.25)
	
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
	
	#################################################################### RESPONSE SCREEN ##########################################################################################################
	###############################################################################################################################################################################################
	
	############# choose randomly one number from [1,2,3] ##############
	ABC = random.sample([1,2,3], 1)
	
	##### pre-stim + ###################################################
	fixStartA = fixation_screen(myClock)
	
	####################################################################
	if ABC[0] == 1:
		#
		s_prime_im1 = visual.ImageStim(win, name='stimPic1', image=s_r_prime_im_a, pos=s_prime_bla1, size=0.125, units='height') ######## downsize & set s_r_pime_im_a
		s_prime_im2 = visual.ImageStim(win, name='blackDot', image=s_r_prime_im_b, pos=s_prime_bla2, size=0.125, units='height') ######## downsize & set s_r_prime_im_b
		s_prime_im3 = visual.ImageStim(win, name='blackDot', image="tasks/spatial/Spatial_symbolic/black_dot.png", pos=s_prime_bla3, size=0.125, units='height') ### downsize & set black dot instead of s_r_prime_im_c
		#
		d1_im1 = visual.ImageStim(win, name='stimPic1', image="tasks/spatial/Spatial_symbolic/black_dot.png", pos=d1_bla1, size=0.125, units='height') ######### downsize & set black dot instead of r_d1_im_a
		d1_im2 = visual.ImageStim(win, name='stimPic2', image="tasks/spatial/Spatial_symbolic/black_dot.png", pos=d1_bla2, size=0.125, units='height') ######### downsize & set black dot instead of r_d1_im_b
		d1_im3 = visual.ImageStim(win, name='stimPic3', image=r_d1_im_c, pos=d1_bla3, size=0.125, units='height') ##### downsize & set r_d1_im_c
		#
		d2_im1 = visual.ImageStim(win, name='stimPic1', image="tasks/spatial/Spatial_symbolic/black_dot.png", pos=d2_bla1, size=0.125, units='height')
		d2_im2 = visual.ImageStim(win, name='stimPic2', image="tasks/spatial/Spatial_symbolic/black_dot.png", pos=d2_bla2, size=0.125, units='height')
		d2_im3 = visual.ImageStim(win, name='stimPic3', image=r_d2_im_c, pos=d2_bla3, size=0.125, units='height')
		#
		tg_im1 = visual.ImageStim(win, name='stimPic1', image="tasks/spatial/Spatial_symbolic/black_dot.png", pos=tg_bla1, size=0.125, units='height')
		tg_im2 = visual.ImageStim(win, name='stimPic2', image="tasks/spatial/Spatial_symbolic/black_dot.png", pos=tg_bla2, size=0.125, units='height')
		tg_im3 = visual.ImageStim(win, name='stimPic3', image=r_tg_im_c, pos=tg_bla3, size=0.125, units='height')
		#
	elif ABC[0] == 2:
		#
		s_prime_im1 = visual.ImageStim(win, name='blackDot', image="tasks/spatial/Spatial_symbolic/black_dot.png", pos=s_prime_bla1, size=0.125, units='height')
		s_prime_im2 = visual.ImageStim(win, name='stimPic2', image=s_r_prime_im_b, pos=s_prime_bla2, size=0.125, units='height')
		s_prime_im3 = visual.ImageStim(win, name='blackDot', image=s_r_prime_im_c, pos=s_prime_bla3, size=0.125, units='height')
		#
		d1_im1 = visual.ImageStim(win, name='stimPic1', image=r_d1_im_a, pos=d1_bla1, size=0.125, units='height') ########### downsize & set r_d1_im_a
		d1_im2 = visual.ImageStim(win, name='stimPic2', image="tasks/spatial/Spatial_symbolic/black_dot.png", pos=d1_bla2, size=0.125, units='height') ###### downsize & set black dot instead of r_d1_im_b
		d1_im3 = visual.ImageStim(win, name='stimPic3', image="tasks/spatial/Spatial_symbolic/black_dot.png", pos=d1_bla3, size=0.125, units='height') ###### downsize & set black dot instead of r_d1_im_c
		#
		d2_im1 = visual.ImageStim(win, name='stimPic1', image=r_d2_im_a, pos=d2_bla1, size=0.125, units='height')
		d2_im2 = visual.ImageStim(win, name='stimPic2', image="tasks/spatial/Spatial_symbolic/black_dot.png", pos=d2_bla2, size=0.125, units='height')
		d2_im3 = visual.ImageStim(win, name='stimPic3', image="tasks/spatial/Spatial_symbolic/black_dot.png", pos=d2_bla3, size=0.125, units='height')
		#
		tg_im1 = visual.ImageStim(win, name='stimPic1', image=r_tg_im_a, pos=tg_bla1, size=0.125, units='height')
		tg_im2 = visual.ImageStim(win, name='stimPic2', image="tasks/spatial/Spatial_symbolic/black_dot.png", pos=tg_bla2, size=0.125, units='height')
		tg_im3 = visual.ImageStim(win, name='stimPic3', image="tasks/spatial/Spatial_symbolic/black_dot.png", pos=tg_bla3, size=0.125, units='height')
		#
	elif ABC[0] == 3:
		#
		s_prime_im1 = visual.ImageStim(win, name='blackDot', image=s_r_prime_im_a, pos=s_prime_bla1, size=0.125, units='height')
		s_prime_im2 = visual.ImageStim(win, name='blackDot', image="tasks/spatial/Spatial_symbolic/black_dot.png", pos=s_prime_bla2, size=0.125, units='height')
		s_prime_im3 = visual.ImageStim(win, name='stimPic3', image=s_r_prime_im_c, pos=s_prime_bla3, size=0.125, units='height')
		#
		d1_im1 = visual.ImageStim(win, name='stimPic1', image="tasks/spatial/Spatial_symbolic/black_dot.png", pos=d1_bla1, size=0.125, units='height') ####### downsize & set black dot instead of r_d1_im_a
		d1_im2 = visual.ImageStim(win, name='stimPic2', image=r_d1_im_b, pos=d1_bla2, size=0.125, units='height') ########### downsize & set r_d1_im_b
		d1_im3 = visual.ImageStim(win, name='stimPic3', image="tasks/spatial/Spatial_symbolic/black_dot.png", pos=d1_bla3, size=0.125, units='height') ####### downsize & set black dot instead of r_d1_im_c
		#
		d2_im1 = visual.ImageStim(win, name='stimPic1', image="tasks/spatial/Spatial_symbolic/black_dot.png", pos=d2_bla1, size=0.125, units='height')
		d2_im2 = visual.ImageStim(win, name='stimPic2', image=r_d2_im_b, pos=d2_bla2, size=0.125, units='height')
		d2_im3 = visual.ImageStim(win, name='stimPic3', image="tasks/spatial/Spatial_symbolic/black_dot.png", pos=d2_bla3, size=0.125, units='height')
		#
		tg_im1 = visual.ImageStim(win, name='stimPic1', image="tasks/spatial/Spatial_symbolic/black_dot.png", pos=tg_bla1, size=0.125, units='height')
		tg_im2 = visual.ImageStim(win, name='stimPic2', image=r_tg_im_b, pos=tg_bla2, size=0.125, units='height')
		tg_im3 = visual.ImageStim(win, name='stimPic3', image="tasks/spatial/Spatial_symbolic/black_dot.png", pos=tg_bla3, size=0.125, units='height')
	
	######## get onset time of response screen #########################
	response_Start = response_screen(myClock)
	
	########## wait for subject to press 1, 2, or 3 (NB must include max wait time)
	key_pressed = event.waitKeys(keyList=['1','2','3'], maxWait=5)
	
	######## get onset of response (i.e. key press) ####################
	keyStart = key_press_time(myClock)
	
	######## clear events ##############################################
	event.clearEvents()
	
	######### post-stim + ##############################################
	fixStartA2 = fixation_screen2(myClock)
	
	###############################################################################################################################################################################################
	###############################################################################################################################################################################################
	
	####################################################################
	trial_num = range(1,51)[f] # to record trial number
	
	####################################################################
	prime_display = os.path.basename(os.path.normpath(trialList[a]['stimulus_1'])), os.path.basename(os.path.normpath(trialList[b]['stimulus_2'])), os.path.basename(os.path.normpath(trialList[c]['stimulus_3']))
	
	if tg_bla1 == (r_tg_pos1[0]*0.25 + -0.5935, r_tg_pos1[1]*0.25 + -0.25):
		Tg_A = 'screen_1'
	elif d1_bla1 == (r_d1_pos1[0]*0.25 + -0.5935, r_d1_pos1[1]*0.25 + -0.25):
		D1_A = 'screen_1'
	elif d2_bla1 == (r_d2_pos1[0]*0.25 + -0.5935, r_d2_pos1[1]*0.25 + -0.25):
		D2_A = 'screen_1'
	
	if tg_bla1 == (r_tg_pos1[0]*0.25, r_tg_pos1[1]*0.25 + -0.25):
		Tg_A = 'screen_2'
	elif d1_bla1 == (r_d1_pos1[0]*0.25, r_d1_pos1[1]*0.25 + -0.25):
		D1_A = 'screen_2'
	elif d2_bla1 == (r_d2_pos1[0]*0.25, r_d2_pos1[1]*0.25 + -0.25):
		D2_A = 'screen_2' 
	
	if tg_bla1 == (r_tg_pos1[0]*0.25 + 0.5935, r_tg_pos1[1]*0.25 + -0.25):
		Tg_A = 'screen_3'
	elif d1_bla1 == (r_d1_pos1[0]*0.25 + 0.5935, r_d1_pos1[1]*0.25 + -0.25):
		D1_A = 'screen_3'
	elif d2_bla1 == (r_d2_pos1[0]*0.25 + 0.5935, r_d2_pos1[1]*0.25 + -0.25):
		D2_A = 'screen_3'
		
	######## to determine the condition (i.e. E vs D) ##################
	### even number = e; odd numer = d ########
	if e % 2 == 0:
		condition = 'E'	
	elif e % 2 > 0:
		condition = 'D'
	####################################################################

	RT = keyStart-response_Start
	
	if RT >= 5:
		SR = 'nothing'
	elif RT < 5:
		if key_pressed == ['1']:
			SR = 'screen_1'
		elif key_pressed == ['2']:
			SR = 'screen_2'
		elif key_pressed == ['3']:
			SR = 'screen_3'
	
	with open(csv_file, "ab") as p:
		writer = csv.writer(p)
		#
		writer.writerow([fixStart, trial_num, condition, 'pre-stim +', '--', '--', '--', '--', '--', '--'])
		writer.writerow([prime_Start, trial_num, condition, '--', prime_display, '--', '--', '--', '--', '--'])
		writer.writerow([fixStart2, trial_num, condition, 'post-stim +', '--', '--', '--', '--', '--', '--'])
		#
		writer.writerow([fixStartA, trial_num, condition, 'pre-stim +', '--', '--', '--', '--', '--', '--'])
		writer.writerow([response_Start, trial_num, condition, '--', '--', Tg_A, D1_A, D2_A, '--', '--'])
		writer.writerow([keyStart, trial_num, condition, '--', '--', '--', '--', '--', SR, '--'])
		writer.writerow([fixStartA2, trial_num, condition, 'post-stim +', '--', '--', '--', '--', '--', '--'])
		#
		writer.writerow(['--', trial_num, condition, '--', '--', '--', '--', '--', '--', RT])

def end(end_txt='tasks/spatial/Instructions/end_instr.txt'):
    End = open(end_txt, 'r').read().split('#\n')
    for i, cur in enumerate(End):
        msgTxt.setText(cur)
        msgTxt.draw()
        win.flip()
        event.waitKeys(maxWait=20)
        win.close()
        core.quit()

end(end_txt='tasks/spatial/Instructions/end_instr.txt')

