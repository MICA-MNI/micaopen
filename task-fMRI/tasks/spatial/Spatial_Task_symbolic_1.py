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
import scipy

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

#win2 = visual.Window(size=(683, 384), fullscr=True, color=1, units='height')
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
########################################################################
########################################################################
########################################################################
########################################################################
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
	core.wait(3)
	#event.waitKeys()
	#event.clearEvents()
	return stimulus_onset	

#def d1_screen(myClock):
#	d1_im1.draw()
#	d1_im2.draw()
#	d1_im3.draw()
#	win.flip()
#	stimulus_onset = myClock.getTime() # stimulus onset
#	#core.wait(1)
#	event.waitKeys()
#	#event.clearEvents()
#	return stimulus_onset	

#def d2_screen(myClock):
#	d2_im1.draw()
#	d2_im2.draw()
#	d2_im3.draw()
#	win.flip()
#	stimulus_onset = myClock.getTime() # stimulus onset
#	#core.wait(1)
#	event.waitKeys()
#	#event.clearEvents()
#	return stimulus_onset	

#def tg_screen(myClock):
#	tg_im1.draw()
#	tg_im2.draw()
#	tg_im3.draw()
#	win.flip()
#	stimulus_onset = myClock.getTime() # stimulus onset
#	#core.wait(1)
#	event.waitKeys()
#	#event.clearEvents()
#	return stimulus_onset

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

#BLA = visual.TextStim(win, name='BLA', text='o',
#							font=sans, height=float(0.08), pos=(-0.8875,-0.4875), color='blue')

def response_screen(myClock):
	#BLA.draw()
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
	screen_onset = myClock.getTime() # onset of stimuli
	#core.wait(1)
	#key_pressed = event.waitKeys(keyList=['1','2','3'])
	#event.clearEvents()
	return screen_onset


#S1 = visual.TextStim(win, name='scr_1', text='screen 1', 
 #                           #font= sans, height=float(0.10), pos=(-0.6,0),color='black')
  #                          font= sans, height=float(0.065), pos=(-0.5,0),color='black')

#S2 = visual.TextStim(win, name='scr_2', text='screen 2', 
 #                           #font= sans, height=float(0.10), pos=(0,0),color='black')
  #                          font= sans, height=float(0.065), pos=(0,0),color='black')

#S3 = visual.TextStim(win, name='scr_3', text='screen 3', 
 #                           #font= sans, height=float(0.10), pos=(0.6,0),color='black')
  #                          font= sans, height=float(0.065), pos=(0.5,0),color='black')

#def Screens(myClock):
#	S1.draw()
#	S2.draw()
#	S3.draw()
#	win.flip()
#	screen_onset = myClock.getTime()
#	return screen_onset

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

#z = []
#for x in range(100):
#	x = randint(-38,39)*0.01
#	if x not in z:
#		z.append(x)
#print(set(z))
#
#h = []
#for x in z:
#	if x >= 0:
#		y = x-(randint(2,5)*0.1)
#	if x < 0:
#		y = x+(randint(2,5)*0.1)
#	h.append(y)
#
#w = []	
#for x in [h][0]:
#	if x >= 0:
#		v = x-(randint(2,5)*0.1)
#	if x < 0:
#		v = x+randint(2,5)*0.1
#	w.append(v)	

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
t_positions = [t1,t2,t3,t4,t5,t6,t7,t8,t9,t10]
shuffle(t_positions)

E_D = range(1,51)
shuffle(E_D)
########################################################################
uber_list = zip(item_1, item_2, item_3, t_positions, E_D, num)

angle = range(1,360)

os.chdir("/home/mica/Desktop/python/fMRIBatteryMay2017/")

for a,b,c,d,e,f in uber_list:
	############################ prime #################################
	prime_pos1 = d[0]
	prime_pos2 = d[1]
	prime_pos3 = d[2]
	
	random_angleA = random.choice(angle) #########################
	random_angleB = random.choice(angle) ########### rotation for single image
	random_angleC = random.choice(angle) #########################
	
	prime_im_a = Image.open(trialList[a]['stimulus_1'])
	prime_im_b = Image.open(trialList[b]['stimulus_2'])
	prime_im_c = Image.open(trialList[c]['stimulus_3'])
	
	r_prime_im_a = prime_im_a.rotate(random_angleA, expand=True)
	r_prime_im_b = prime_im_b.rotate(random_angleB, expand=True)
	r_prime_im_c = prime_im_c.rotate(random_angleC, expand=True)
	
	#prime_im1 = visual.ImageStim(win, name='stimPic1', image=r_prime_im_a, pos=prime_pos1)
	#prime_im2 = visual.ImageStim(win, name='stimPic2', image=r_prime_im_b, pos=prime_pos2)
	#prime_im3 = visual.ImageStim(win, name='stimPic3', image=r_prime_im_c, pos=prime_pos3)
	
	prime_im1 = visual.ImageStim(win, name='stimPic1', image=None, pos=prime_pos1, units='height')
	prime_im2 = visual.ImageStim(win, name='stimPic2', image=None, pos=prime_pos2, units='height')
	prime_im3 = visual.ImageStim(win, name='stimPic3', image=None, pos=prime_pos3, units='height')
	
	prime_POS = (prime_pos1,prime_pos2,prime_pos3)
	
	####################################################################
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
	
	####################### triplet_rotation ###########################
	rotation_angle = random.choice(angle)
	origin_point = (0,0)
	
	###################### tripartite position #########################
	#pos_val = [(0,0.25),(-0.25,-0.25),(0.25,-0.25)]
	pos_val = [(-0.5935,-0.25),(0,-0.25),(0.5935,-0.25)]
	shuffle(pos_val)
	
	######################### distractor 1 #####################################################
	############################################################################################
	choice1 = choices[0]
	
	d1_values = permuted_list[choice1]

	d1_pos1 = d1_values[0]
	d1_pos2 = d1_values[1]
	d1_pos3 = d1_values[2]
	
	random_angle1 = random.choice(angle) ###################
	random_angle2 = random.choice(angle) ######### rotation for single image (different than prime)
	random_angle3 = random.choice(angle) ###################

	##################### difficult condition ##########################
	##################### same rotation as prime #######################
	
	######## to determine the condition (i.e. E vs D) ##################
	### even number = e; odd numer = d ########
	if e % 2 == 0:
		ori_1 = random_angle1
		ori_2 = random_angle2
		ori_3 = random_angle3
		
	elif e % 2 > 0:
		ori_1 = random_angleA
		ori_2 = random_angleB
		ori_3 = random_angleC
	####################################################################
	
	d1_im_a = Image.open(trialList[a]['stimulus_1'])
	d1_im_b = Image.open(trialList[b]['stimulus_2'])
	d1_im_c = Image.open(trialList[c]['stimulus_3'])
	
	r_d1_im_a = d1_im_a.rotate(ori_1 - rotation_angle, expand=True) #####################
	r_d1_im_b = d1_im_b.rotate(ori_2 - rotation_angle, expand=True) #### single rotations
	r_d1_im_c = d1_im_c.rotate(ori_3 - rotation_angle, expand=True) #####################

	r_d1_pos1 = triplet_rotation(origin_point, d1_pos1, math.radians(rotation_angle)) ########################
	r_d1_pos2 = triplet_rotation(origin_point, d1_pos2, math.radians(rotation_angle)) ####### rotation for all images
	r_d1_pos3 = triplet_rotation(origin_point, d1_pos3, math.radians(rotation_angle)) ########################
	
	####################################################################
	####################################################################
	d1_bla1 = (r_d1_pos1[0]*0.25 + pos_val[0][0], r_d1_pos1[1]*0.25 + pos_val[0][1])
	d1_bla2 = (r_d1_pos2[0]*0.25 + pos_val[0][0], r_d1_pos2[1]*0.25 + pos_val[0][1])
	d1_bla3 = (r_d1_pos3[0]*0.25 + pos_val[0][0], r_d1_pos3[1]*0.25 + pos_val[0][1])
	####################################################################
	####################################################################
	
	#d1_im1 = visual.ImageStim(win, name='stimPic1', image=None, pos=r_d1_pos1)
	#d1_im2 = visual.ImageStim(win, name='stimPic2', image=None, pos=r_d1_pos2)
	#d1_im3 = visual.ImageStim(win, name='stimPic3', image=None, pos=r_d1_pos3) 
	
	#d1_im1 = visual.ImageStim(win, name='stimPic1', image=None, pos=d1_bla1, size=0.125, units='height')
	#d1_im2 = visual.ImageStim(win, name='stimPic2', image=None, pos=d1_bla2, size=0.125, units='height')
	#d1_im3 = visual.ImageStim(win, name='stimPic3', image=None, pos=d1_bla3, size=0.125, units='height') 
	
	######################### distractor 2 #####################################################
	############################################################################################
	choice2 = choices[1]

	d2_values = permuted_list[choice2]

	d2_pos1 = d2_values[0]
	d2_pos2 = d2_values[1]
	d2_pos3 = d2_values[2]
	
	####################### easy condition #############################
	random_anglea = random.choice(angle) ###############################
	random_angleb = random.choice(angle) ############ rotation for single image (different than prime)
	random_anglec = random.choice(angle) ###############################
	
	##################### difficult condition ##########################
	##################### same rotation as prime #######################
	
	######## to determine the condition (i.e. E vs D) ##################
	### even number = e; odd numer = d ########
	if e % 2 == 0:
		ori_a = random_anglea
		ori_b = random_angleb
		ori_c = random_anglec
		
	elif e % 2 > 0:
		ori_a = random_angleA
		ori_b = random_angleB
		ori_c = random_angleC
	####################################################################
	
	d2_im_a = Image.open(trialList[a]['stimulus_1'])
	d2_im_b = Image.open(trialList[b]['stimulus_2'])
	d2_im_c = Image.open(trialList[c]['stimulus_3'])
	
	r_d2_im_a = d2_im_a.rotate(ori_a - rotation_angle, expand=True)
	r_d2_im_b = d2_im_b.rotate(ori_b - rotation_angle, expand=True)
	r_d2_im_c = d2_im_c.rotate(ori_c - rotation_angle, expand=True)
	
	r_d2_pos1 = triplet_rotation(origin_point, d2_pos1, math.radians(rotation_angle))
	r_d2_pos2 = triplet_rotation(origin_point, d2_pos2, math.radians(rotation_angle))
	r_d2_pos3 = triplet_rotation(origin_point, d2_pos3, math.radians(rotation_angle))
	
	####################################################################
	####################################################################
	d2_bla1 = (r_d2_pos1[0]*0.25 + pos_val[1][0], r_d2_pos1[1]*0.25 + pos_val[1][1])
	d2_bla2 = (r_d2_pos2[0]*0.25 + pos_val[1][0], r_d2_pos2[1]*0.25 + pos_val[1][1])
	d2_bla3 = (r_d2_pos3[0]*0.25 + pos_val[1][0], r_d2_pos3[1]*0.25 + pos_val[1][1])
	####################################################################
	####################################################################
	
	#d2_im1 = visual.ImageStim(win, name='stimPic1', image=None, pos=r_d2_pos1)
	#d2_im2 = visual.ImageStim(win, name='stimPic2', image=None, pos=r_d2_pos2)
	#d2_im3 = visual.ImageStim(win, name='stimPic3', image=None, pos=r_d2_pos3) 
	
	#d2_im1 = visual.ImageStim(win, name='stimPic1', image=None, pos=d2_bla1, size=0.125, units='height')
	#d2_im2 = visual.ImageStim(win, name='stimPic2', image=None, pos=d2_bla2, size=0.125, units='height')
	#d2_im3 = visual.ImageStim(win, name='stimPic3', image=None, pos=d2_bla3, size=0.125, units='height') 
	
	######################### target ###########################################################
	############################################################################################
	tg_pos1 = d[0]
	tg_pos2 = d[1]
	tg_pos3 = d[2]
	
	tg_im_a = Image.open(trialList[a]['stimulus_1'])
	tg_im_b = Image.open(trialList[b]['stimulus_2'])
	tg_im_c = Image.open(trialList[c]['stimulus_3'])
	
	r_tg_im_a = tg_im_a.rotate(random_angleA - rotation_angle, expand=True)
	r_tg_im_b = tg_im_b.rotate(random_angleB - rotation_angle, expand=True)
	r_tg_im_c = tg_im_c.rotate(random_angleC - rotation_angle, expand=True)
	
	r_tg_pos1 = triplet_rotation(origin_point, tg_pos1, math.radians(rotation_angle)) ####################################
	r_tg_pos2 = triplet_rotation(origin_point, tg_pos2, math.radians(rotation_angle)) ############ rotation for all images
	r_tg_pos3 = triplet_rotation(origin_point, tg_pos3, math.radians(rotation_angle)) ####################################
	
	####################################################################
	####################################################################
	tg_bla1 = (r_tg_pos1[0]*0.25 + pos_val[2][0], r_tg_pos1[1]*0.25 + pos_val[2][1])
	tg_bla2 = (r_tg_pos2[0]*0.25 + pos_val[2][0], r_tg_pos2[1]*0.25 + pos_val[2][1])
	tg_bla3 = (r_tg_pos3[0]*0.25 + pos_val[2][0], r_tg_pos3[1]*0.25 + pos_val[2][1])
	####################################################################
	####################################################################	
	
	#tg_im1 = visual.ImageStim(win, name='stimPic1', image=None, pos=r_tg_pos1)
	#tg_im2 = visual.ImageStim(win, name='stimPic2', image=None, pos=r_tg_pos2)
	#tg_im3 = visual.ImageStim(win, name='stimPic3', image=None, pos=r_tg_pos3) 
	
	#tg_im1 = visual.ImageStim(win, name='stimPic1', image=None, pos=tg_bla1, size=0.125, units='height')
	#tg_im2 = visual.ImageStim(win, name='stimPic2', image=None, pos=tg_bla2, size=0.125, units='height')
	#tg_im3 = visual.ImageStim(win, name='stimPic3', image=None, pos=tg_bla3, size=0.125, units='height') 
	
	######################### s_prime_bla ##############################
	
	#
	r_prime_pos1 = triplet_rotation(origin_point, prime_pos1, math.radians(rotation_angle)) #################################
	r_prime_pos2 = triplet_rotation(origin_point, prime_pos2, math.radians(rotation_angle)) ######### rotation for all images
	r_prime_pos3 = triplet_rotation(origin_point, prime_pos3, math.radians(rotation_angle)) #################################
	#
	s_prime_bla1 = (r_prime_pos1[0]*0.25, r_prime_pos1[1]*0.25 + 0.25)
	s_prime_bla2 = (r_prime_pos2[0]*0.25, r_prime_pos2[1]*0.25 + 0.25)
	s_prime_bla3 = (r_prime_pos3[0]*0.25, r_prime_pos3[1]*0.25 + 0.25)
	
	#################################################################### PRIME PRESENTATION #######################################################################################################
	fixStart = fixation_screen(myClock) # to record fixation onset
	#
	prime_im1.setImage(r_prime_im_a)
	prime_im2.setImage(r_prime_im_b)
	prime_im3.setImage(r_prime_im_c)
	#
	prime_Start = prime_screen(myClock) # to record stimulus onset
	#
	event.clearEvents()
	#
	fixStart2 = fixation_screen2(myClock) # to record second fixation onset
	
	#################################################################### CONDITION 1 ##############################################################################################################
	###############################################################################################################################################################################################
	abc = random.sample([1,2,3], 1)
	#
	fixStartA = fixation_screen(myClock)
	#
	if abc[0] == 1:
		#
		s_prime_im1 = visual.ImageStim(win, name='stimPic1', image=r_prime_im_a, pos=s_prime_bla1, size=0.125, units='height')
		#
		s_prime_im2 = visual.ImageStim(win, name='blackDot', image="tasks/spatial/Spatial_symbolic/black_dot.png", pos=s_prime_bla2, size=0.125, units='height')
		#
		s_prime_im3 = visual.ImageStim(win, name='blackDot', image="tasks/spatial/Spatial_symbolic/black_dot.png", pos=s_prime_bla3, size=0.125, units='height')
		#
	elif abc[0] == 2:
		#
		s_prime_im1 = visual.ImageStim(win, name='blackDot', image="tasks/spatial/Spatial_symbolic/black_dot.png", pos=s_prime_bla1, size=0.125, units='height')
		#
		s_prime_im2 = visual.ImageStim(win, name='stimPic2', image=r_prime_im_b, pos=s_prime_bla2, size=0.125, units='height')
		#
		s_prime_im3 = visual.ImageStim(win, name='blackDot', image="tasks/spatial/Spatial_symbolic/black_dot.png", pos=s_prime_bla3, size=0.125, units='height')
		#	
	elif abc[0] == 3:
		#
		s_prime_im1 = visual.ImageStim(win, name='blackDot', image="tasks/spatial/Spatial_symbolic/black_dot.png", pos=s_prime_bla1, size=0.125, units='height')
		#
		s_prime_im2 = visual.ImageStim(win, name='blackDot', image="tasks/spatial/Spatial_symbolic/black_dot.png", pos=s_prime_bla2, size=0.125, units='height')
		#
		s_prime_im3 = visual.ImageStim(win, name='stimPic3', image=r_prime_im_c, pos=s_prime_bla3, size=0.125, units='height')
	#
	if abc[0] == 1:
		#
		d1_im1 = visual.ImageStim(win, name='stimPic1', image="tasks/spatial/Spatial_symbolic/black_dot.png", pos=d1_bla1, size=0.125, units='height')
		d1_im2 = visual.ImageStim(win, name='stimPic2', image=r_d1_im_b, pos=d1_bla2, size=0.125, units='height')
		d1_im3 = visual.ImageStim(win, name='stimPic3', image=r_d1_im_c, pos=d1_bla3, size=0.125, units='height')
		#
		d2_im1 = visual.ImageStim(win, name='stimPic1', image="tasks/spatial/Spatial_symbolic/black_dot.png", pos=d2_bla1, size=0.125, units='height')
		d2_im2 = visual.ImageStim(win, name='stimPic2', image=r_d2_im_b, pos=d2_bla2, size=0.125, units='height')
		d2_im3 = visual.ImageStim(win, name='stimPic3', image=r_d2_im_c, pos=d2_bla3, size=0.125, units='height')
		#
		tg_im1 = visual.ImageStim(win, name='stimPic1', image="tasks/spatial/Spatial_symbolic/black_dot.png", pos=tg_bla1, size=0.125, units='height')
		tg_im2 = visual.ImageStim(win, name='stimPic2', image=r_tg_im_b, pos=tg_bla2, size=0.125, units='height')
		tg_im3 = visual.ImageStim(win, name='stimPic3', image=r_tg_im_c, pos=tg_bla3, size=0.125, units='height')
		#
	elif abc[0] == 2:
		#
		d1_im1 = visual.ImageStim(win, name='stimPic1', image=r_d1_im_a, pos=d1_bla1, size=0.125, units='height')
		d1_im2 = visual.ImageStim(win, name='stimPic2', image="tasks/spatial/Spatial_symbolic/black_dot.png", pos=d1_bla2, size=0.125, units='height')
		d1_im3 = visual.ImageStim(win, name='stimPic3', image=r_d1_im_c, pos=d1_bla3, size=0.125, units='height')
		#
		d2_im1 = visual.ImageStim(win, name='stimPic1', image=r_d2_im_a, pos=d2_bla1, size=0.125, units='height')
		d2_im2 = visual.ImageStim(win, name='stimPic2', image="tasks/spatial/Spatial_symbolic/black_dot.png", pos=d2_bla2, size=0.125, units='height')
		d2_im3 = visual.ImageStim(win, name='stimPic3', image=r_d2_im_c, pos=d2_bla3, size=0.125, units='height')
		#
		tg_im1 = visual.ImageStim(win, name='stimPic1', image=r_tg_im_a, pos=tg_bla1, size=0.125, units='height')
		tg_im2 = visual.ImageStim(win, name='stimPic2', image="tasks/spatial/Spatial_symbolic/black_dot.png", pos=tg_bla2, size=0.125, units='height')
		tg_im3 = visual.ImageStim(win, name='stimPic3', image=r_tg_im_c, pos=tg_bla3, size=0.125, units='height')
		#	
	elif abc[0] == 3:
		#
		d1_im1 = visual.ImageStim(win, name='stimPic1', image=r_d1_im_a, pos=d1_bla1, size=0.125, units='height')
		d1_im2 = visual.ImageStim(win, name='stimPic2', image=r_d1_im_b, pos=d1_bla2, size=0.125, units='height')
		d1_im3 = visual.ImageStim(win, name='stimPic3', image="tasks/spatial/Spatial_symbolic/black_dot.png", pos=d1_bla3, size=0.125, units='height')
		#
		d2_im1 = visual.ImageStim(win, name='stimPic1', image=r_d2_im_a, pos=d2_bla1, size=0.125, units='height')
		d2_im2 = visual.ImageStim(win, name='stimPic2', image=r_d2_im_b, pos=d2_bla2, size=0.125, units='height')
		d2_im3 = visual.ImageStim(win, name='stimPic3', image="tasks/spatial/Spatial_symbolic/black_dot.png", pos=d2_bla3, size=0.125, units='height')
		#
		tg_im1 = visual.ImageStim(win, name='stimPic1', image=r_tg_im_a, pos=tg_bla1, size=0.125, units='height')
		tg_im2 = visual.ImageStim(win, name='stimPic2', image=r_tg_im_b, pos=tg_bla2, size=0.125, units='height')
		tg_im3 = visual.ImageStim(win, name='stimPic3', image="tasks/spatial/Spatial_symbolic/black_dot.png", pos=tg_bla3, size=0.125, units='height')
		#
	#d1_im1.setImage(r_d1_im_a)
	#d1_im2.setImage(r_d1_im_b)
	#d1_im3.setImage(r_d1_im_c)
	#
	#d2_im1.setImage(r_d2_im_a)
	#d2_im2.setImage(r_d2_im_b)
	#d2_im3.setImage(r_d2_im_c)
	#
	#tg_im1.setImage(r_tg_im_a)
	#tg_im2.setImage(r_tg_im_b)
	#tg_im3.setImage(r_tg_im_c)
	#
	response_Start = response_screen(myClock)
	#
	key_pressed = event.waitKeys(keyList=['1','2','3'])
	#
	keyStart = key_press_time(myClock)
	#
	event.clearEvents()
	#
	fixStartA2 = fixation_screen2(myClock)
	###############################################################################################################################################################################################
	###############################################################################################################################################################################################
	#
	#
	#
	# PUT CONDITION 2 HERE
	#
	#
	#
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
	
	#if start_order[0] == tg_screen and start_order[1] == d1_screen and start_order[2] == d2_screen:
	#	Tg_a = 'screen_1'
	#	D1_a = '--'
	#	D2_a = '--'
	#	
	#	Tg_b = '--'
	#	D1_b = 'screen_2'
	#	D2_b = '--'
	#	
	#	Tg_c = '--'
	#	D1_c = '--'
	#	D2_c = 'screen_3'

	#elif start_order[0] == tg_screen and start_order[1] == d2_screen and start_order[2] == d1_screen:
	#	Tg_a = 'screen_1'
	#	D1_a = '--'
	#	D2_a = '--'
	#	
	#	Tg_b = '--'
	#	D1_b = '--'
	#	D2_b = 'screen_2'
	#	
	#	Tg_c = '--'
	#	D1_c = 'screen_3'
	#	D2_c = '--'

	#elif start_order[0] == d1_screen and start_order[1] == tg_screen and start_order[2] == d2_screen:
	#	Tg_a = '--'
	#	D1_a = 'screen_1'
	#	D2_a = '--'
	#	
	#	Tg_b = 'screen_2'
	#	D1_b = '--'
	#	D2_b = '--'
	#	
	#	Tg_c = '--'
	#	D1_c = '--'
	#	D2_c = 'screen_3'
	#	
	#elif start_order[0] == d1_screen and start_order[1] == d2_screen and start_order[2] == tg_screen:
	#	Tg_a = '--'
	#	D1_a = 'screen_1'
	#	D2_a = '--'
	#	
	#	Tg_b = '--'
	#	D1_b = '--'
	#	D2_b = 'screen_2'
	#	
	#	Tg_c = 'screen_3'
	#	D1_c = '--'
	#	D2_c = '--'
	#	
	#elif start_order[0] == d2_screen and start_order[1] == tg_screen and start_order[2] == d1_screen:
	#	Tg_a = '--'
	#	D1_a = '--'
	#	D2_a = 'screen_1'
	#	
	#	Tg_b = 'screen_2'
	#	D1_b = '--'
	#	D2_b = '--'
	#	
	#	Tg_c = '--'
	#	D1_c = 'screen_3'
	#	D2_c = '--'

	#elif start_order[0] == d2_screen and start_order[1] == d1_screen and start_order[2] == tg_screen:
	#	Tg_a = '--'
	#	D1_a = '--'
	#	D2_a = 'screen_1'
	#	
	#	Tg_b = '--'
	#	D1_b = 'screen_2'
	#	D2_b = '--'
	#	
	#	Tg_c = 'screen_3'
	#	D1_c = '--'
	#	D2_c = '--'

	####################################################################
	
	######## to determine the condition (i.e. E vs D) ##################
	### even number = e; odd numer = d ########
	if e % 2 == 0:
		condition = 'E'	
	elif e % 2 > 0:
		condition = 'D'
	####################################################################
	
	if key_pressed == ['1']:
		SR = 'screen_1'
	elif key_pressed == ['2']:
		SR = 'screen_2'
	elif key_pressed == ['3']:
		SR = 'screen_3'
	
	RT = keyStart-response_Start
	
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
		#
		#writer.writerow([fixStartB, trial_num, condition, 'pre-stim +', '--', '--', '--', '--', '--', '--'])
		#writer.writerow([Start2, trial_num, condition, '--', '--', Tg_b, D1_b, D2_b, '--', '--'])
		#writer.writerow([fixStartB2, trial_num, condition, 'post-stim +', '--', '--', '--', '--', '--', '--'])
		#
		#writer.writerow([fixStartC, trial_num, condition, 'pre-stim +', '--', '--', '--', '--', '--', '--'])
		#writer.writerow([Start3, trial_num, condition, '--', '--', Tg_c, D1_c, D2_c, '--', '--'])
		#writer.writerow([fixStartC2, trial_num, condition, 'post-stim +', '--', '--', '--', '--', '--', '--'])
		#

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

