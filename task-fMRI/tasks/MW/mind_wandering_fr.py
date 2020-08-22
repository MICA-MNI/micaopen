# -*- coding: utf-8 -*-   ### DO NOT REMOVE THIS LINE, even though it's commented, it somehow is necessary for recognizing the French accents
##################################################################
from psychopy import gui, visual, event, core, data, logging, os #
from numpy.random import shuffle                                 #
import csv                                                       #
from psychopy.hardware.emulator import launchScan                #
from pdb import set_trace as bp                                  #
##################################################################

###########################################
expName = "Mind wandering"
expInfo = {'subject name':'', 'session':'001'}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
#
if dlg.OK == False: core.quit()
expInfo['date'] = data.getDateStr()
expInfo['expName'] = expName

######################
myClock = core.Clock()
logging.setDefaultClock(myClock)

####################################################################################################
filename = 'tasks/MW/data_mind_wandering' + os.path.sep + '%s_%s' %(expInfo['subject name'], expInfo['date'])
logFile = logging.LogFile(filename + '.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)

######################################################
sans = ['Arial','Gill Sans MT', 'Helvetica','Verdana']
win = visual.Window(fullscr=True, color=1, units='height')

##################################################################################################################################
csv_file = ('tasks/MW/data_mind_wandering/' + expInfo['subject name'] + '_' + expInfo['session'] + '_' + expInfo['date'] + '.csv')
#
with open(csv_file, "wb") as outcsv:
	writer = csv.writer(outcsv)
	writer.writerow(["Time", "Trial_Number", "Fixation", "Fixation_Duration", "Question", "Dimension", "Low_end", "High_end", "Subject_Response", "Reaction_Time"])

################################################################################################################################################
IntroTxt = visual.TextStim(win, text='default tex', font=sans, name='instruction', pos=(0,0), height=float(0.04), wrapWidth=1100, color='black')
#
def instruction(intro_txt='tasks/MW/Instructions/mind_wandering_instr_fr.txt'):
    Instruction = open(intro_txt, 'r').read().split('#\n')
    #
    for i, cur in enumerate(Instruction):
        IntroTxt.setText(cur)
        IntroTxt.draw()
        win.flip()
        event.waitKeys(keyList=['2','3','4'])
#
instruction(intro_txt='tasks/MW/Instructions/mind_wandering_instr_fr.txt')

###############
MR_settings = {
'TR': 0.585, # duration (sec) per volume
'volumes': 1500, # number of whole-brain 3D volumes / frames
'sync': '5', # character to use as the sync timing event; assumed to come at start of a volume
'skip': 0, # number of volumes lacking a sync pulse at start of scan (for T1 stabilization)
}
#
vol = launchScan(win, MR_settings, mode='Scan', globalClock=myClock.reset())

##############################################################################
waitTxt = visual.TextStim(win, text='default tex', font=sans, name='wait_trigger', pos=(0,0), height=float(0.04), wrapWidth=1100, color='black')
waitTxt.setText(open('tasks/MW/Instructions/wait_trigger_fr.txt', 'r').read())
waitTxt.draw()
win.flip()
core.wait(2)

###################################################################################################################
fixation = visual.TextStim(win, name='fixation', text='+', font= sans, height=float(0.08), pos=(0,0),color='black')
#
intg = 1.0/13
spread_list = range(0,13)
pre_fix_dur_list = [x*intg for x in spread_list]
fix_dur_list = [x+2 for x in pre_fix_dur_list]
shuffle(fix_dur_list)
#
def fixation_screen(myClock):
    fixation.draw()
    win.logOnFlip(level=logging.EXP, msg='pre-stimulus fixation cross on screen')
    win.flip()
    #
    fixation_onset = myClock.getTime()
    #
    if y == 0:
		core.wait(fix_dur_list[0])
    elif y == 1:
		core.wait(fix_dur_list[1])
    elif y == 2:
		core.wait(fix_dur_list[2])
    elif y == 3:
		core.wait(fix_dur_list[3])
    elif y == 4:
		core.wait(fix_dur_list[4])
    elif y == 5:
		core.wait(fix_dur_list[5])
    elif y == 6:
		core.wait(fix_dur_list[6])
    elif y == 7:
		core.wait(fix_dur_list[7])
    elif y == 8:
		core.wait(fix_dur_list[8])
    elif y == 9:
		core.wait(fix_dur_list[9])
    elif y == 10:
		core.wait(fix_dur_list[10])
    elif y == 11:
		core.wait(fix_dur_list[11])
    elif y == 12:
		core.wait(fix_dur_list[12])
	#
    if event.getKeys(keyList=['escape']):
        core.quit()
    return fixation_onset

######################
def stimulus_screen(myClock):
	q.setText(trialList[x]['questions'])
	q.draw()
	win.flip()
	#
	stimulus_onset = myClock.getTime() # onset of questions
	#
	return stimulus_onset

#######################################################################
trialList = data.importConditions('tasks/MW/mind_wandering_trials_fr.csv')
#
LIST = range(1,13)
shuffle(LIST)
LIST.insert(0,0) # add a zero at the beginning of list (the first question is always the same, the rest is randomized)
#
num = range(0,13)
#
q = visual.TextStim(win, color='black', height=0.05)
#
main_list = zip(LIST,num)
#
for x,y in main_list:
	fixStart = fixation_screen(myClock)
	#
	if trialList[x]['questions'].startswith('Le'):
		rating_scale = visual.RatingScale(win, scale=None, labels=['négatif', 'positif'], high=11, markerStart=6, leftKeys='2', rightKeys='4',
		tickMarks=['1','11'], tickHeight=1, maxTime=7.5, markerColor='black', textColor='black', textSize=0.75, stretch=2.5, noMouse=True, lineColor='#4CB391',
		marker='slider', showValue=False, precision=5, showAccept=False)
	elif trialList[x]['questions'].endswith('étaient:'):
		rating_scale = visual.RatingScale(win, scale=None, labels=['spontanées', 'délibérées'], high=11, markerStart=6, leftKeys='2', rightKeys='4',
		tickMarks=['1','11'], tickHeight=1, maxTime=7.5, markerColor='black', textColor='black', textSize=0.75, stretch=2.5, noMouse=True, lineColor='#4CB391',
		marker='slider', showValue=False, precision=5, showAccept=False)	
	else:
		rating_scale = visual.RatingScale(win, scale=None, labels=['pas du tout', 'complètement'], high=11, markerStart=6, leftKeys='2', rightKeys='4',
		tickMarks=['1','11'], tickHeight=1, maxTime=7.5, markerColor='black', textColor='black', textSize=0.75, stretch=2.5, noMouse=True, lineColor='#4CB391',
		marker='slider', showValue=False, precision=5, showAccept=False)
	#
	stimStart = stimulus_screen(myClock) # draw and flip q
	#
	while rating_scale.noResponse:
		q.draw() # must draw and flip q a second time (first time to get accurate onset time, second time so that q and rating_scale appear on screen together)
		rating_scale.draw()
		win.flip()
	#
	trial_num = range(1,14)[y]
	#
	hist = rating_scale.getHistory()
	SR = hist[len(hist)-1][0]
	RT = hist[len(hist)-2][1]
	#
	accept_time = stimStart + RT
	#
	#if RT <= 5:
	#	accept_time = stimStart + RT
	#	rt = RT
	#	sr = SR
	#else:
	#	accept_time = '--'
	#	rt = 'N/A'
	#	sr = 'N/A'
	#
	question = os.path.basename(os.path.normpath(trialList[x]['questions']))
	dim = os.path.basename(os.path.normpath(trialList[x]['Dimension']))
	l_end = os.path.basename(os.path.normpath(trialList[x]['low_end']))
	h_end = os.path.basename(os.path.normpath(trialList[x]['high_end']))
	#
	with open(csv_file, "ab") as p:
		writer = csv.writer(p)
		writer.writerow([fixStart, trial_num, 'ON', stimStart-fixStart, '--', '--', '--', '--', '--', '--'])
		writer.writerow([stimStart, trial_num, 'OFF', '--', question, dim, l_end, h_end, '--', '--'])
		writer.writerow([accept_time, trial_num, 'OFF', '--', '--', '--', '--', '--', SR, RT])
		writer.writerow(['', '', '', '', '', '', '', '', '', ''])

##############################################################################################################################################
EndTxt = visual.TextStim(win, text='default tex', font=sans, name='instruction', pos=(0,0), height=float(0.04), wrapWidth=1100, color='black')
#
def end(end_txt='tasks/MW/Instructions/mind_wandering_end_fr.txt'):
    End = open(end_txt, 'r').read().split('#\n')
    #
    for i, cur in enumerate(End):
        EndTxt.setText(cur)
        EndTxt.draw()
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
#
end(end_txt='tasks/MW/Instructions/mind_wandering_end_fr.txt')

########################################################################
########################################################################
########################################################################
