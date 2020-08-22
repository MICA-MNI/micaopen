from psychopy import gui, logging, visual, data, event, os, core
import numpy as np
from numpy.random import randint, shuffle
import random
from pdb import set_trace as bp
from psychopy.hardware.emulator import launchScan
import pickle
import csv
import re
import pandas as pd
#
import PIL
from PIL import Image

###################################################################################################################################################################################

expName = "Episodic Recall Task (symbolic)"
expInfo = {'subject name':'', 'session':'001', 'symbol list':['A','B','demo']}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)

###################################################################################################################################################################################

if dlg.OK == False: core.quit()
expInfo['date'] = data.getDateStr()
expInfo['expName'] = expName

###################################################################################################################################################################################
myClock = core.Clock()

logging.setDefaultClock(myClock)

if not os.path.isdir('data'):
	os.makedirs('data')

filename = 'tasks/episodic/data_Episodic Recall Task (symbolic)/' + os.path.sep + '%s_%s' %(expInfo['subject name'], expInfo['date'])
logFile = logging.LogFile(filename + '.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)

###################################################################################################################################################################################
sans = ['Arial','Gill Sans MT', 'Helvetica','Verdana']
win = visual.Window(fullscr=True, color=1, units='height')

###################################################################################################################################################################################
csv_file = ("tasks/episodic/data_Episodic Recall Task (symbolic)/" + expInfo['subject name'] + "_" + expInfo['session'] + "_" + expInfo['date'] + "_" +  expInfo['symbol list'] + ".csv")
with open(csv_file, "wb") as outcsv:
	writer = csv.writer(outcsv)
	writer.writerow(["Time", "Trial_Number", "Condition", "Fixation", "Fixation_Duration", "Prime", "Target", "Foil_1", "Foil_2", "Left_choice", "Center_choice", "Right_choice", "Subject_Response", "Key_pressed", "Accuracy", "Reaction_Time"])

###################################################################################################################################################################################
msgTxt = visual.TextStim(win,text='default text', font= sans, name='message',
    height=float(0.04), wrapWidth=1100,
    color='black', 
    )

instrTxt = visual.TextStim(win,text='default text', font= sans, name='instruction',
    pos=[0,0], height=float(0.04), wrapWidth=1100,
    color='black',
    ) #object to display instructions 

def instruction(inst_txt='tasks/episodic/Instructions/exp_instr2_symbolic_fr.txt'):
    Instruction = open(inst_txt, 'r').read().split('#\n')
    #
    for i, cur in enumerate(Instruction):
        instrTxt.setText(cur)
        instrTxt.draw()
        win.flip()
        event.waitKeys(keyList=['2','3','4'])

instruction(inst_txt='tasks/episodic/Instructions/exp_instr2_symbolic_fr.txt')

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
instrTxt.setText(open('tasks/episodic/Instructions/wait_trigger_fr.txt', 'r').read())
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
    #
    if e == 0:
		core.wait(fix_dur_list[0])
    elif e == 1:
		core.wait(fix_dur_list[1])
    elif e == 2:
		core.wait(fix_dur_list[2])
    elif e == 3:
		core.wait(fix_dur_list[3])
    elif e == 4:
		core.wait(fix_dur_list[4])
    elif e == 5:
		core.wait(fix_dur_list[5])
    elif e == 6:
		core.wait(fix_dur_list[6])
    elif e == 7:
		core.wait(fix_dur_list[7])
    elif e == 8:
		core.wait(fix_dur_list[8])
    elif e == 9:
		core.wait(fix_dur_list[9])
    elif e == 10:
		core.wait(fix_dur_list[10])
    elif e == 11:
		core.wait(fix_dur_list[11])
    elif e == 12:
		core.wait(fix_dur_list[12])
    elif e == 13:
		core.wait(fix_dur_list[13])
    elif e == 14:
		core.wait(fix_dur_list[14])
    elif e == 15:
		core.wait(fix_dur_list[15])
    elif e == 16:
		core.wait(fix_dur_list[16])
    elif e == 17:
		core.wait(fix_dur_list[17])
    elif e == 18:
		core.wait(fix_dur_list[18])
    elif e == 19:
		core.wait(fix_dur_list[19])
    elif e == 20:
		core.wait(fix_dur_list[20])
    elif e == 21:
		core.wait(fix_dur_list[21])
    elif e == 22:
		core.wait(fix_dur_list[22])
    elif e == 23:
		core.wait(fix_dur_list[23])
    elif e == 24:
		core.wait(fix_dur_list[24])
    elif e == 25:
		core.wait(fix_dur_list[25])
    elif e == 26:
		core.wait(fix_dur_list[26])
    elif e == 27:
		core.wait(fix_dur_list[27])
    elif e == 28:
		core.wait(fix_dur_list[28])
    elif e == 29:
		core.wait(fix_dur_list[29])
    elif e == 30:
		core.wait(fix_dur_list[30])
    elif e == 31:
		core.wait(fix_dur_list[31])
    elif e == 32:
		core.wait(fix_dur_list[32])
    elif e == 33:
		core.wait(fix_dur_list[33])
    elif e == 34:
		core.wait(fix_dur_list[34])
    elif e == 35:
		core.wait(fix_dur_list[35])
    elif e == 36:
		core.wait(fix_dur_list[36])
    elif e == 37:
		core.wait(fix_dur_list[37])
    elif e == 38:
		core.wait(fix_dur_list[38])
    elif e == 39:
		core.wait(fix_dur_list[39])
    elif e == 40:
		core.wait(fix_dur_list[40])
    elif e == 41:
		core.wait(fix_dur_list[41])
    elif e == 42:
		core.wait(fix_dur_list[42])
    elif e == 43:
		core.wait(fix_dur_list[43])
    elif e == 44:
		core.wait(fix_dur_list[44])
    elif e == 45:
		core.wait(fix_dur_list[45])
    elif e == 46:
		core.wait(fix_dur_list[46])
    elif e == 47:
		core.wait(fix_dur_list[47])
    elif e == 48:
		core.wait(fix_dur_list[48])
    elif e == 49:
		core.wait(fix_dur_list[49])
    elif e == 50:
		core.wait(fix_dur_list[50])
    elif e == 51:
		core.wait(fix_dur_list[51])
    elif e == 52:
		core.wait(fix_dur_list[52])
    elif e == 53:
		core.wait(fix_dur_list[53])
    elif e == 54:
		core.wait(fix_dur_list[54])
    elif e == 55:
		core.wait(fix_dur_list[55])
	#
    if event.getKeys(keyList=['escape']):
        core.quit()
    return fixation_onset
########################################################################
########################################################################
########################################################################

def stimulus_screen(myClock):
	prime_im.draw()
	tg_im.draw()
	foil1_im.draw()
	foil2_im.draw()
	win.flip()
	stimulus_onset = myClock.getTime() # stimulus onset
	return stimulus_onset

#################################################################################################################################################################
trialList = data.importConditions("tasks/episodic/Episodic_Encoding_symbolic/Episodic_Recall_List" + expInfo['symbol list'] + '.csv') # loads stimuli from specified directory
LIST = range(len(trialList))

#############################################################################################################################
dirfiles = os.listdir('tasks/episodic/data_Episodic Encoding Task (symbolic)/')
targetfile = [z for z in dirfiles if z.startswith(expInfo['subject name'] + '_' + expInfo['session']) and z.endswith('.csv')] 

if expInfo['symbol list'] == 'demo':
	main_order = range(0,4)
elif expInfo['symbol list'] != 'demo':
	main_order = range(0,56)

encoded_log_file = 'tasks/episodic/data_Episodic Encoding Task (symbolic)/' + targetfile[0]
stim1_list = pd.read_csv(encoded_log_file).Stim_1.tolist()
stim2_list = pd.read_csv(encoded_log_file).Stim_2.tolist()

########################################################################

x_values = [-0.5,0,0.5] # the y value for the target images is always the same (i.e., -0.4); only the x values must to be specified

num = range(0,56)
uber_list = zip(LIST, LIST, LIST, LIST, num)

for a,b,c,d,e in uber_list:
	shuffle(x_values) # shuffle the order of elements in x_values
	tg1 = x_values[0] # get the x value for the first position inside x_values
	tg2 = x_values[1] # get the x value for the second position...
	tg3 = x_values[2] # get the x value for the thrid position...
	
	prime_pos = (0,0.25)
	tg_pos = (tg1,-0.25)
	foil1_pos = (tg2,-0.25)
	foil2_pos = (tg3,-0.25)
	
	####################################################################
	x_dim = 240
	#
	PRIME = Image.open(trialList[a]['prime'])
	TG = Image.open(trialList[b]['target'])
	Foil1 = Image.open(trialList[c]['foil1'])
	Foil2 = Image.open(trialList[d]['foil2'])
	#
	wpercent1 = (x_dim/float(PRIME.size[0]))
	wpercent2 = (x_dim/float(TG.size[0]))
	wpercent3 = (x_dim/float(Foil1.size[0]))
	wpercent4 = (x_dim/float(Foil2.size[0]))
	#
	y1_dim = int((float(PRIME.size[1])*float(wpercent1)))
	y2_dim = int((float(TG.size[1])*float(wpercent2)))
	y3_dim = int((float(Foil1.size[1])*float(wpercent3)))
	y4_dim = int((float(Foil2.size[1])*float(wpercent4)))
	#
	Prime = PRIME.resize((x_dim,y1_dim), PIL.Image.ANTIALIAS)
	tg = TG.resize((x_dim,y2_dim), PIL.Image.ANTIALIAS)
	foil1 = Foil1.resize((x_dim,y3_dim), PIL.Image.ANTIALIAS)
	foil2 = Foil2.resize((x_dim,y4_dim), PIL.Image.ANTIALIAS)
	####################################################################
	
	prime_im = visual.ImageStim(win, name='stimPic1', image = None, pos=prime_pos)
	tg_im = visual.ImageStim(win, name='stimPic2', image = None, pos=tg_pos)
	foil1_im = visual.ImageStim(win, name='stimPic3', image = None, pos=foil1_pos)
	foil2_im = visual.ImageStim(win, name='stimPic4', image = None, pos=foil2_pos)
	#
	fixStart = fixation_screen(myClock)
	#
	prime_im.setImage(Prime)
	tg_im.setImage(tg)
	foil1_im.setImage(foil1)
	foil2_im.setImage(foil2)
	#
	stimStart = stimulus_screen(myClock)
	#
	trialEndTime = stimStart + 2.5
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
		RT = keyStart - stimStart
	else:
		keyStart = '--'
		RT = 'N/A'
	#
	event.clearEvents()

	trial_num = range(1,57)[e]
	
	prime_display = os.path.basename(os.path.normpath(trialList[a]['prime']))
	#
	if stim1_list.count(prime_display) == 2:    
		condition = 'E'                         
	elif stim2_list.count(prime_display) == 2:  
		condition = 'E'                          
	elif stim1_list.count(prime_display) == 1:  
		condition = 'D'                         
	elif stim2_list.count(prime_display) == 1: 
		condition = 'D'                         
	#
	tg_display = os.path.basename(os.path.normpath(trialList[b]['target']))
	foil1_display = os.path.basename(os.path.normpath(trialList[c]['foil1']))
	foil2_display = os.path.basename(os.path.normpath(trialList[d]['foil2']))
	
	if RT == 'N/A':
		im_position = 'N/A'
		key_ID = 'N/A'
	elif RT < 2.5:
		if key_pressed == '2':
			im_position = (-0.5,-0.25)
			key_ID = 'left'
		elif key_pressed == '3':
			im_position = (0,-0.25)
			key_ID = 'center'
		elif key_pressed == '4':
			im_position = (0.5,-0.25)
			key_ID = 'right'

	if im_position == 'N/A':
		SR = 'N/A'
	elif im_position == tg_pos:
		SR = tg_display
	elif im_position == foil1_pos:
		SR = foil1_display
	elif im_position == foil2_pos:
		SR = foil2_display
	####################################################################
	if tg_pos == (-0.5,-0.25) and foil1_pos == (0,-0.25) and foil2_pos == (0.5,-0.25):
		left_choice = tg_display
		center_choice = foil1_display
		right_choice = foil2_display
	#
	elif tg_pos == (-0.5,-0.25) and foil2_pos == (0,-0.25) and foil1_pos == (0.5,-0.25):
		left_choice = tg_display
		center_choice = foil2_display
		right_choice = foil1_display
	#
	elif foil1_pos == (-0.5,-0.25) and tg_pos == (0,-0.25) and foil2_pos == (0.5,-0.25):
		left_choice = foil1_display
		center_choice = tg_display
		right_choice = foil2_display
	#	
	elif foil1_pos == (-0.5,-0.25) and foil2_pos == (0,-0.25) and tg_pos == (0.5,-0.25):
		left_choice = foil1_display
		center_choice = foil2_display
		right_choice = tg_display
	#
	elif foil2_pos == (-0.5,-0.25) and tg_pos == (0,-0.25) and foil1_pos == (0.5,-0.25):
		left_choice = foil2_display
		center_choice = tg_display
		right_choice = foil1_display
	#	
	elif foil2_pos == (-0.5,-0.25) and foil1_pos == (0,-0.25) and tg_pos == (0.5,-0.25):
		left_choice = foil2_display
		center_choice = foil1_display
		right_choice = tg_display
	####################################################################
	if SR == tg_display:
		Acc = '1'
	elif SR != tg_display:
		Acc = '0'
	####################################################################
	with open(csv_file, "ab") as p:
		writer = csv.writer(p)
		writer.writerow([fixStart, trial_num, condition, 'ON', stimStart-fixStart, '--', '--', '--', '--', '--', '--', '--', '--', '--', '--', '--'])
		writer.writerow([stimStart, trial_num, condition, 'OFF', '--', prime_display, tg_display, foil1_display, foil2_display, left_choice, center_choice, right_choice, '--', '--', '--', '--'])
		writer.writerow([keyStart, trial_num, condition, 'OFF', '--', '--', '--', '--', '--', '--', '--', '--', SR, key_ID, Acc, '--'])
		writer.writerow(['--', trial_num, condition, 'OFF', '--', '--', '--', '--', '--', '--', '--', '--', '--', '--', '--', RT])
		writer.writerow(['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])

def end(end_txt='tasks/episodic/Instructions/end_instr_fr.txt'):
    End = open(end_txt, 'r').read().split('#\n')
    #
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

end(end_txt='tasks/episodic/Instructions/end_instr_fr.txt')

###################################################################################################################################################################################
