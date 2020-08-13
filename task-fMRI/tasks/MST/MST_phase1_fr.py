from psychopy import gui, logging, visual, data, event, os, core
import numpy as np
from numpy.random import randint, shuffle
import random
from pdb import set_trace as bp
from psychopy.hardware.emulator import launchScan
import pickle
import csv


###################################################################################################################################################################################
expName = "MST Phase 1"
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

filename = 'tasks/MST/data_MST Phase 1/' + os.path.sep + '%s_%s' %(expInfo['subject name'], expInfo['date'])
logFile = logging.LogFile(filename + '.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)

###################################################################################################################################################################################
sans = ['Arial','Gill Sans MT', 'Helvetica','Verdana']
win = visual.Window(fullscr=True, color=1, units='height')

###################################################################################################################################################################################
csv_file = ("tasks/MST/data_MST Phase 1/" + expInfo['subject name'] + "_" + expInfo['session'] + "_" + expInfo['date'] + "_" +  expInfo['symbol list'] + ".csv")
with open(csv_file, "wb") as outcsv:
	writer = csv.writer(outcsv)
	writer.writerow(["Time", "Trial_Number", "Fixation", "Fixation_Duration", "Stim_ID","Subject_Response","Reaction_Time"])

###################################################################################################################################################################################
msgTxt = visual.TextStim(win, text='default text', font=sans, name='message',
    height=float(0.04), wrapWidth=1100,
    color='black', 
    )

instrTxt = visual.TextStim(win, text='default text', font=sans, name='instruction',
    pos=[0,0], height=float(0.04), wrapWidth=1100,
    color='black',
    )

def instruction(inst_txt='tasks/MST/Instructions/exp_instr_fr.txt'):
    Instruction = open(inst_txt, 'r').read().split('#\n')
    #
    for i, cur in enumerate(Instruction):
        instrTxt.setText(cur)
        instrTxt.draw()
        win.flip()
        event.waitKeys(keyList=['2','3','4'])

instruction(inst_txt='tasks/MST/Instructions/exp_instr_fr.txt')

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
instrTxt.setText(open('tasks/MST/Instructions/wait_trigger_fr.txt', 'r').read())
instrTxt.draw()
win.flip()
core.wait(2)

########################################################################
fixation = visual.TextStim(win, name='fixation', text='+', font=sans, height=float(0.08), pos=(0,0), color='black')

def fixation_screen(myClock):
    fixation.draw()
    win.logOnFlip(level=logging.EXP, msg='fixation cross on screen')
    win.flip()
    fixation_onset = myClock.getTime() #fixation cross onset
    core.wait(range(20,31)[randint(0,11)]*0.1)
    if event.getKeys(keyList=['escape']):
        core.quit()
    return fixation_onset

def key_press_time(myClock):
	key_press_onset = myClock.getTime()
	return key_press_onset

def stimulus_screen(myClock):
	in_out.draw()
	stimulus.draw()
	win.flip()
	screen_onset = myClock.getTime() # stimulus onset
	return screen_onset

#################################################################################################################################################################
trialList = data.importConditions("tasks/MST/MST_phase1/MST_phase1_List" + expInfo['symbol list'] + '.csv')

trialOrder = range(0,64)

num = range(0,64)

exp_list = zip(trialOrder, num)

stimulus = visual.ImageStim(win, name='stimPic', image = None, pos=(0,0))

for i,j in exp_list:
	fixStart = fixation_screen(myClock)
	#
	in_out = visual.TextStim(win, text='Indoors or Outdoors?', font=sans, name='instruction', pos=[0,0.4], height=float(0.04), wrapWidth=1100, color='black')
	in_out.setText(open('tasks/MST/Instructions/in_out_fr.txt', 'r').read())
	#
	stimulus.setImage(trialList[i]['stim'])
	#
	stimStart = stimulus_screen(myClock)
	#
	trialEndTime = stimStart + 2
	#
	flag = 0
	keyList = []
	#################
	event.clearEvents()
	#################
	while myClock.getTime() < trialEndTime:
		keypress = event.getKeys(keyList=['2','4'])
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
	trial_num = range(1,65)[j]
	#
	stim_ID = os.path.basename(os.path.normpath(trialList[i]['stim']))
	#
	if RT == 'N/A':
		SR = 'N/A'
	elif RT < 2:
		if key_pressed == '2':
			SR = 'indoors'
		elif key_pressed== '4':
			SR = 'outdoors'
	#
	with open(csv_file, "ab") as p:
		writer = csv.writer(p)
		writer.writerow([fixStart, trial_num, 'ON', stimStart-fixStart, '--', '--', '--'])
		writer.writerow([stimStart, trial_num, 'OFF', '--', stim_ID, '--', '--'])
		writer.writerow([keyStart, trial_num, 'OFF', '--', '--', SR,'--'])
		writer.writerow(['--', trial_num, 'OFF', '--', '--', '--', RT])
		writer.writerow(['', '', '', '', '', '', ''])

def end(end_txt='tasks/MST/Instructions/end_instr_fr.txt'):
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

end(end_txt='tasks/MST/Instructions/end_instr_fr.txt')

###################################################################################################################################################################################









