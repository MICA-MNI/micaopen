from psychopy import gui, logging, visual, data, event, os, core
import numpy as np
from numpy.random import randint, shuffle
import random
from pdb import set_trace as bp
from psychopy.hardware.emulator import launchScan
import pickle
import csv
#
import PIL
from PIL import Image

###################################################################################################################################################################################
expName = "Episodic Encoding Task (symbolic)"
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

filename = 'tasks/episodic/data_Episodic Encoding Task (symbolic)/' + os.path.sep + '%s_%s' %(expInfo['subject name'], expInfo['date'])
logFile = logging.LogFile(filename + '.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)

###################################################################################################################################################################################
sans = ['Arial','Gill Sans MT', 'Helvetica','Verdana']
win = visual.Window(fullscr=True, color=1, units='height')

###################################################################################################################################################################################
csv_file = ("tasks/episodic/data_Episodic Encoding Task (symbolic)/" + expInfo['subject name'] + "_" + expInfo['session'] + "_" + expInfo['date'] + "_" +  expInfo['symbol list'] + ".csv")
with open(csv_file, "wb") as outcsv:
	writer = csv.writer(outcsv)
	writer.writerow(["Time", "Trial_Number", "Condition", "Fixation", "Fixation_Duration", "Stim_1", "Stim_2"])

###################################################################################################################################################################################
msgTxt = visual.TextStim(win,text='default text', font= sans, name='message',
    height=float(0.04), wrapWidth=1100,
    color='black', 
    )

instrTxt = visual.TextStim(win,text='default text', font= sans, name='instruction',
    pos=[0,0], height=float(0.04), wrapWidth=1100,
    color='black',
    ) #object to display instructions 

def instruction(inst_txt='tasks/episodic/Instructions/exp_instr_symbolic_fr.txt'):
    Instruction = open(inst_txt, 'r').read().split('#\n')
    #
    for i, cur in enumerate(Instruction):
        instrTxt.setText(cur)
        instrTxt.draw()
        win.flip()
        event.waitKeys(keyList=['2','3','4'])

instruction(inst_txt='tasks/episodic/Instructions/exp_instr_symbolic_fr.txt')

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
                            font=sans, height=float(0.08), pos=(0,0), color='black')

#def fixation_screen(myClock):
#    fixation.draw()
#    win.logOnFlip(level=logging.EXP, msg='pre-stimulus fixation cross on screen') #
#    win.flip()
#    fixation_onset = myClock.getTime() #fixation cross onset
#    core.wait(range(20,31)[randint(0,11)]*0.1)
#    if event.getKeys(keyList=['escape']):
#        core.quit()
#    return fixation_onset

########################################################################
########################################################################
########################################################################
intg = 1.0/84
spread_list = range(0,84)
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
    if z == 0:
		core.wait(fix_dur_list[0])
    elif z == 1:
		core.wait(fix_dur_list[1])
    elif z == 2:
		core.wait(fix_dur_list[2])
    elif z == 3:
		core.wait(fix_dur_list[3])
    elif z == 4:
		core.wait(fix_dur_list[4])
    elif z == 5:
		core.wait(fix_dur_list[5])
    elif z == 6:
		core.wait(fix_dur_list[6])
    elif z == 7:
		core.wait(fix_dur_list[7])
    elif z == 8:
		core.wait(fix_dur_list[8])
    elif z == 9:
		core.wait(fix_dur_list[9])
    elif z == 10:
		core.wait(fix_dur_list[10])
    elif z == 11:
		core.wait(fix_dur_list[11])
    elif z == 12:
		core.wait(fix_dur_list[12])
    elif z == 13:
		core.wait(fix_dur_list[13])
    elif z == 14:
		core.wait(fix_dur_list[14])
    elif z == 15:
		core.wait(fix_dur_list[15])
    elif z == 16:
		core.wait(fix_dur_list[16])
    elif z == 17:
		core.wait(fix_dur_list[17])
    elif z == 18:
		core.wait(fix_dur_list[18])
    elif z == 19:
		core.wait(fix_dur_list[19])
    elif z == 20:
		core.wait(fix_dur_list[20])
    elif z == 21:
		core.wait(fix_dur_list[21])
    elif z == 22:
		core.wait(fix_dur_list[22])
    elif z == 23:
		core.wait(fix_dur_list[23])
    elif z == 24:
		core.wait(fix_dur_list[24])
    elif z == 25:
		core.wait(fix_dur_list[25])
    elif z == 26:
		core.wait(fix_dur_list[26])
    elif z == 27:
		core.wait(fix_dur_list[27])
    elif z == 28:
		core.wait(fix_dur_list[28])
    elif z == 29:
		core.wait(fix_dur_list[29])
    elif z == 30:
		core.wait(fix_dur_list[30])
    elif z == 31:
		core.wait(fix_dur_list[31])
    elif z == 32:
		core.wait(fix_dur_list[32])
    elif z == 33:
		core.wait(fix_dur_list[33])
    elif z == 34:
		core.wait(fix_dur_list[34])
    elif z == 35:
		core.wait(fix_dur_list[35])
    elif z == 36:
		core.wait(fix_dur_list[36])
    elif z == 37:
		core.wait(fix_dur_list[37])
    elif z == 38:
		core.wait(fix_dur_list[38])
    elif z == 39:
		core.wait(fix_dur_list[39])
    elif z == 40:
		core.wait(fix_dur_list[40])
    elif z == 41:
		core.wait(fix_dur_list[41])
    elif z == 42:
		core.wait(fix_dur_list[42])
    elif z == 43:
		core.wait(fix_dur_list[43])
    elif z == 44:
		core.wait(fix_dur_list[44])
    elif z == 45:
		core.wait(fix_dur_list[45])
    elif z == 46:
		core.wait(fix_dur_list[46])
    elif z == 47:
		core.wait(fix_dur_list[47])
    elif z == 48:
		core.wait(fix_dur_list[48])
    elif z == 49:
		core.wait(fix_dur_list[49])
    elif z == 50:
		core.wait(fix_dur_list[50])
    elif z == 51:
		core.wait(fix_dur_list[51])
    elif z == 52:
		core.wait(fix_dur_list[52])
    elif z == 53:
		core.wait(fix_dur_list[53])
    elif z == 54:
		core.wait(fix_dur_list[54])
    elif z == 55:
		core.wait(fix_dur_list[55])
    elif z == 56:
		core.wait(fix_dur_list[56])
    elif z == 57:
		core.wait(fix_dur_list[57])
    elif z == 58:
		core.wait(fix_dur_list[58])
    elif z == 59:
		core.wait(fix_dur_list[59])
    elif z == 60:
		core.wait(fix_dur_list[60])
    elif z == 61:
		core.wait(fix_dur_list[61])
    elif z == 62:
		core.wait(fix_dur_list[62])
    elif z == 63:
		core.wait(fix_dur_list[63])
    elif z == 64:
		core.wait(fix_dur_list[64])
    elif z == 65:
		core.wait(fix_dur_list[65])
    elif z == 66:
		core.wait(fix_dur_list[66])
    elif z == 67:
		core.wait(fix_dur_list[67])
    elif z == 68:
		core.wait(fix_dur_list[68])
    elif z == 69:
		core.wait(fix_dur_list[69])
    elif z == 70:
		core.wait(fix_dur_list[70])
    elif z == 71:
		core.wait(fix_dur_list[71])
    elif z == 72:
		core.wait(fix_dur_list[72])
    elif z == 73:
		core.wait(fix_dur_list[73])
    elif z == 74:
		core.wait(fix_dur_list[74])
    elif z == 75:
		core.wait(fix_dur_list[75])
    elif z == 76:
		core.wait(fix_dur_list[76])
    elif z == 77:
		core.wait(fix_dur_list[77])
    elif z == 78:
		core.wait(fix_dur_list[78])
    elif z == 79:
		core.wait(fix_dur_list[79])
    elif z == 80:
		core.wait(fix_dur_list[80])
    elif z == 81:
		core.wait(fix_dur_list[81])
    elif z == 82:
		core.wait(fix_dur_list[82])
    elif z == 83:
		core.wait(fix_dur_list[83])
	#
    if event.getKeys(keyList=['escape']):
        core.quit()
    return fixation_onset
########################################################################
########################################################################
########################################################################

def stimulus_screen(myClock):
	im1.draw()
	im2.draw()
	win.flip()
	stimulus_onset = myClock.getTime() # stimulus onset
	core.wait(2)
	event.clearEvents()
	return stimulus_onset

#################################################################################################################################################################
trialList = data.importConditions("tasks/episodic/Episodic_Encoding_symbolic/Episodic_List" + expInfo['symbol list'] + '.csv')
LIST = range(len(trialList))

num = range(0,84)

uber_list = zip(LIST, LIST, num)

im1 = visual.ImageStim(win, name='stimPic1', image = None, pos=(-0.2,0))
im2 = visual.ImageStim(win, name='stimPic2', image = None, pos=(0.2,0))

for x,y,z in uber_list:
	#fixStart = fixation_screen(myClock) # to record fixation onset
	####################################################################
	x_dim = 240
	#
	IM1 = Image.open(trialList[x]['stimulus_1'])
	IM2 = Image.open(trialList[y]['stimulus_2'])
	#
	wpercent1 = (x_dim/float(IM1.size[0]))
	wpercent2 = (x_dim/float(IM2.size[0]))
	#
	y1_dim = int((float(IM1.size[1])*float(wpercent1)))
	y2_dim = int((float(IM2.size[1])*float(wpercent2)))
	#
	IMAGE1 = IM1.resize((x_dim,y1_dim), PIL.Image.ANTIALIAS)
	IMAGE2 = IM2.resize((x_dim,y2_dim), PIL.Image.ANTIALIAS)
	####################################################################
	#
	fixStart = fixation_screen(myClock) # to record fixation onset
	#
	im1.setImage(IMAGE1)
	im2.setImage(IMAGE2)
	#
	stimStart = stimulus_screen(myClock) # to record stimulus onset
	trial_num = range(1,85)[z] # to record trial number
	
	if [r[0] for r in uber_list].count(x) == 2: #####
		condition = 'E'                         ##### to record condition (i.e., 'E' for easy; 'D' for difficult)
	elif [r[0] for r in uber_list].count(x) == 1: ###
		condition = 'D'                         #####    

	stim1 = os.path.basename(os.path.normpath(trialList[x]['stimulus_1']))
	stim2 = os.path.basename(os.path.normpath(trialList[y]['stimulus_2'])) # to record name of items in stimulus pair

	with open(csv_file, "ab") as p:
		writer = csv.writer(p)
		writer.writerow([fixStart, trial_num, condition,'ON', stimStart-fixStart,'--', '--'])
		writer.writerow([stimStart, trial_num, condition, 'OFF', '--', stim1, stim2])
		writer.writerow(['', '', '', '', '', '', ''])

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
