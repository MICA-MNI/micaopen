from psychopy import gui, logging, visual, data, event, os, core
import numpy as np
from numpy.random import randint, shuffle, permutation
import random
from pdb import set_trace as bp
from psychopy.hardware.emulator import launchScan
import pickle
import csv
from itertools import permutations
import math
#
import PIL
from PIL import Image

###################################################################################################################################################################################
expName = "Semantic Task (symbolic)"
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

filename = 'tasks/semantic/data_Semantic Task (symbolic)/' + os.path.sep + '%s_%s' %(expInfo['subject name'], expInfo['date'])
logFile = logging.LogFile(filename + '.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)

###################################################################################################################################################################################
sans = ['Arial','Gill Sans MT', 'Helvetica','Verdana']
win = visual.Window(fullscr=True, color=1, units='height')

###################################################################################################################################################################################
csv_file = ("tasks/semantic/data_Semantic Task (symbolic)/" + expInfo['subject name'] + "_" + expInfo['session'] + "_" + expInfo['date'] + "_" +  expInfo['symbol list'] + ".csv")
with open(csv_file, "wb") as outcsv:
	writer = csv.writer(outcsv)
	writer.writerow(["Time", "Trial_Number", "Condition", "Fixation", "Fixation_Duration", "Prime", "Target", "Foil_1", "Foil_2", "Left_choice", "Center_choice", "Right_choice", "Subject_Response", "Key_pressed", "Accuracy", "Reaction_Time"])

###################################################################################################################################################################################
msgTxt = visual.TextStim(win,text='default text', font=sans, name='message',
    height=float(0.04), wrapWidth=1100,
    color='black', 
    )

instrTxt = visual.TextStim(win,text='default text', font=sans, name='instruction',
    pos=[0,0], height=float(0.04), wrapWidth=100,
    color='black',
    ) #object to display instructions 

def instruction(inst_txt='tasks/semantic/Instructions/exp_instr_symbolic_fr.txt'):
    Instruction = open(inst_txt, 'r').read().split('#\n')
    #
    for i, cur in enumerate(Instruction):
        instrTxt.setText(cur)
        instrTxt.draw()
        win.flip()
        event.waitKeys(keyList=['2','3','4'])

instruction(inst_txt='tasks/semantic/Instructions/exp_instr_symbolic_fr.txt')

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
instrTxt.setText(open('tasks/semantic/Instructions/wait_trigger_fr.txt', 'r').read())
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
    if f == 0:
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
    elif f == 14:
		core.wait(fix_dur_list[14])
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
    elif f == 28:
		core.wait(fix_dur_list[28])
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
    elif f == 42:
		core.wait(fix_dur_list[42])
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

def stimulus_screen(myClock):
	#
	prime_im.draw()
	#
	f1_im.draw()
	#
	f2_im.draw()
	#
	tg_im.draw()
	#
	win.flip()
	#
	screen_onset = myClock.getTime()
	#
	return screen_onset

#################################################################################################################################################################
trialList = data.importConditions("tasks/semantic/Semantic_symbolic/Semantic_List" + expInfo['symbol list'] + '.csv')

LIST = range(len(trialList))

quintuplet_list = zip(LIST,LIST,LIST,LIST,LIST)

################################################################################################################################################################################################
item_1 = [x[0] for x in quintuplet_list]
item_2 = [x[1] for x in quintuplet_list]
item_3 = [x[2] for x in quintuplet_list]
item_4 = [x[3] for x in quintuplet_list]
item_5 = [x[4] for x in quintuplet_list]
#
x_values = [-0.5,0,0.5] ##### target & d1, d1 x positions (i.e. y positions = -0.25)
#
num = range(0,56)
#
########################################################################
uber_list = zip(item_1, item_2, item_3, item_4, item_5, num)

for a,b,c,d,e,f in uber_list:
	#
	############## prepare prime #######################################
	prime_im = visual.ImageStim(win, name='stimPic1', image = None, pos=(0,0.25))
	#
	### randomize x_values and set tg_pos, d1_pos, and d2_pos
	shuffle(x_values)
	tg_x = x_values[0]
	f1_x = x_values[1]
	f2_x = x_values[2]
	#
	tg_pos = (tg_x, -0.25)
	f1_pos = (f1_x, -0.25)
	f2_pos = (f2_x, -0.25)
	#
	############## prepare tg, d1, and d2 ##############################
	tg_im = visual.ImageStim(win, name='stimPic2', image = None, pos=tg_pos)
	f1_im = visual.ImageStim(win, name='stimPic3', image = None, pos=f1_pos)
	f2_im = visual.ImageStim(win, name='stimPic4', image = None, pos=f2_pos)
	#
	############## present trial #######################################
	
	#################################
	x_dim = 240
	#
	PRIME = Image.open(trialList[a]['prime'])
	TG = Image.open(trialList[b]['target'])
	F1 = Image.open(trialList[c]['foil1'])
	F2 = Image.open(trialList[d]['foil2'])
	#
	wpercent1 = (x_dim/float(PRIME.size[0]))
	wpercent2 = (x_dim/float(TG.size[0]))
	wpercent3 = (x_dim/float(F1.size[0]))
	wpercent4 = (x_dim/float(F2.size[0]))
	#
	y1_dim = int((float(PRIME.size[1])*float(wpercent1)))
	y2_dim = int((float(TG.size[1])*float(wpercent2)))
	y3_dim = int((float(F1.size[1])*float(wpercent3)))
	y4_dim = int((float(F2.size[1])*float(wpercent4)))
	#
	Prime = PRIME.resize((x_dim,y1_dim), PIL.Image.ANTIALIAS)
	Target = TG.resize((x_dim,y2_dim), PIL.Image.ANTIALIAS)
	Foil1 = F1.resize((x_dim,y3_dim), PIL.Image.ANTIALIAS)
	Foil2 = F2.resize((x_dim,y4_dim), PIL.Image.ANTIALIAS)
	#################################
	#
	fixStart = fixation_screen(myClock)
	#
	prime_im.setImage(Prime)
	tg_im.setImage(Target)
	f1_im.setImage(Foil1)
	f2_im.setImage(Foil2)
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
	#
	trial_num = range(1,57)[f]
	#
	############## for csv log file ####################################
	#
	prime_display = os.path.basename(os.path.normpath(trialList[a]['prime']))
	tg_display = os.path.basename(os.path.normpath(trialList[b]['target']))
	f1_display = os.path.basename(os.path.normpath(trialList[c]['foil1']))
	f2_display = os.path.basename(os.path.normpath(trialList[d]['foil2']))
	#
	COND = os.path.basename(os.path.normpath(trialList[e]['condition']))
	#
	if RT == 'N/A':
		im_position = 'N/A'
		key_ID = 'N/A'
	elif RT < 2.5
		if key_pressed == '2':
			im_position = (-0.5,-0.25)
			key_ID = 'left'
		elif key_pressed == '3':
			im_position = (0,-0.25)
			key_ID = 'center'
		elif key_pressed == '4':
			im_position = (0.5,-0.25)
			key_ID = 'right'
	#
	if im_position == 'N/A':
		SR = 'N/A'
	elif im_position == tg_pos:
		SR = tg_display
	elif im_position == f1_pos:
		SR = f1_display
	elif im_position == f2_pos:
		SR = f2_display
	####################################################################
	if tg_pos == (-0.5,-0.25) and f1_pos == (0,-0.25) and f2_pos == (0.5,-0.25):
		left_choice = tg_display
		center_choice = f1_display
		right_choice = f2_display
	#
	elif tg_pos == (-0.5,-0.25) and f2_pos == (0,-0.25) and f1_pos == (0.5,-0.25):
		left_choice = tg_display
		center_choice = f2_display
		right_choice = f1_display
	#
	elif f1_pos == (-0.5,-0.25) and tg_pos == (0,-0.25) and f2_pos == (0.5,-0.25):
		left_choice = f1_display
		center_choice = tg_display
		right_choice = f2_display
	#	
	elif f1_pos == (-0.5,-0.25) and f2_pos == (0,-0.25) and tg_pos == (0.5,-0.25):
		left_choice = f1_display
		center_choice = f2_display
		right_choice = tg_display
	#
	elif f2_pos == (-0.5,-0.25) and tg_pos == (0,-0.25) and f1_pos == (0.5,-0.25):
		left_choice = f2_display
		center_choice = tg_display
		right_choice = f1_display
	#	
	elif f2_pos == (-0.5,-0.25) and f1_pos == (0,-0.25) and tg_pos == (0.5,-0.25):
		left_choice = f2_display
		center_choice = f1_display
		right_choice = tg_display
	####################################################################
	if SR == tg_display:
		Acc = '1'
	elif SR != tg_display:
		Acc = '0'
	####################################################################
	with open(csv_file, "ab") as p:
		writer = csv.writer(p)
		writer.writerow([fixStart, trial_num, COND, 'ON', stimStart-fixStart, '--', '--', '--', '--', '--', '--', '--', '--', '--', '--', '--'])
		writer.writerow([stimStart, trial_num, COND, 'OFF', '--', prime_display, tg_display, f1_display, f2_display, left_choice, center_choice, right_choice, '--', '--', '--', '--'])
		writer.writerow([keyStart, trial_num, COND, 'OFF', '--', '--', '--', '--', '--', '--', '--', '--', SR, key_ID, Acc, '--'])
		writer.writerow(['--', trial_num, COND, 'OFF', '--', '--', '--', '--', '--', '--', '--', '--', '--', '--', '--', RT])
		writer.writerow(['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])

def end(end_txt='tasks/semantic/Instructions/end_instr_fr.txt'):
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

end(end_txt='tasks/semantic/Instructions/end_instr_fr.txt')

###################################################################################################################################################################################

