from psychopy import gui, logging, visual, data, event, os, core
from pdb import set_trace as bp
from psychopy.hardware.emulator import launchScan
import csv

###################################################################################################################################################################################
expName = "Fixation Task"
expInfo = {'subject name':'', 'session':'001'}
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

filename = 'tasks/fixation/data_Fixation Task' + os.path.sep + '%s_%s' %(expInfo['subject name'], expInfo['date'])
logFile = logging.LogFile(filename + '.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)

###################################################################################################################################################################################
sans = ['Arial','Gill Sans MT', 'Helvetica','Verdana']
win = visual.Window(fullscr=True, color=0, units='height')

###################################################################################################################################################################################
csv_file = ("tasks/fixation/data_Fixation Task/" + expInfo['subject name'] + "_" + expInfo['session'] + "_" + expInfo['date'] + "_" + ".csv")
with open(csv_file, "wb") as outcsv:
	writer = csv.writer(outcsv)
	writer.writerow(["fixation_start","fixation_end","fixation_duration"])

###################################################################################################################################################################################
msgTxt = visual.TextStim(win,text='default text', font=sans, name='message',
    height=float(0.04), wrapWidth=1100,
    color='black', 
    )

instrTxt = visual.TextStim(win,text='default text', font=sans, name='instruction',
    pos=[0,0], height=float(0.04), wrapWidth=100,
    color='black',
    ) #object to display instructions 

def instruction(inst_txt='tasks/fixation/Instructions/exp_instr.txt'):
    Instruction = open(inst_txt, 'r').read().split('#\n')
    #
    for i, cur in enumerate(Instruction):
        instrTxt.setText(cur)
        instrTxt.draw()
        win.flip()
        event.waitKeys(keyList=['2','3','4'])

instruction(inst_txt='tasks/fixation/Instructions/exp_instr.txt')

###################################################################################################################################################################################
# settings for launchScan:
MR_settings = {
'TR': 0.585, # duration (sec) per volume
'volumes': 1500, # number of whole-brain 3D volumes / frames
'sync': '5', # character to use as the sync timing event; assumed to come at start of a volume
'skip': 0, # number of volumes lacking a sync pulse at start of scan (for T1 stabilization)
}

vol = launchScan(win, MR_settings, mode='Scan', globalClock=myClock.reset())

###################################################################################################################################################################################
instrTxt.setText(open('tasks/semantic/Instructions/wait_trigger.txt', 'r').read())
instrTxt.draw()
win.flip()
core.wait(2)

###################################################################################################################################################################################
def key_press_time(myClock):
	key_press_onset = myClock.getTime()
	return key_press_onset

########################################################################
fixation = visual.TextStim(win, name='fixation', text='+',
                            font= sans, height=float(0.08), pos=(0,0),color='black')

def fixation_screen(myClock):
    fixation.draw()
    win.logOnFlip(level=logging.EXP, msg='fixation cross on screen') #new log haoting
    win.flip()
    fixation_onset = myClock.getTime() #fixation cross onset
    #event.waitKeys(keyList=['escape'])
    return fixation_onset

fixStart = fixation_screen(myClock)
key_pressed = event.waitKeys(keyList=['escape'])
fixEnd = key_press_time(myClock)

fixDur = fixEnd - fixStart

with open(csv_file, "ab") as p:
	writer = csv.writer(p)
	writer.writerow([fixStart, fixEnd, fixDur])

def end(end_txt='tasks/fixation/Instructions/end_instr.txt'):
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
			writer.writerow(['--'])
			writer.writerow(['End message'])
			writer.writerow([thank_you])
        #
        event.waitKeys(keyList=['space'])
        win.close()
        core.quit()

end(end_txt='tasks/fixation/Instructions/end_instr.txt')

###################################################################################################################################################################################

