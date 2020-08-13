from psychopy import gui, logging, visual, data, event, os, core
from pdb import set_trace as bp
from psychopy.hardware.emulator import launchScan
import csv

###################################################################################################################################################################################
expName = "Fixation Task (Movie)"
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
	writer.writerow(["movie_start","movie_end","movie_duration"])

###################################################################################################################################################################################
msgTxt = visual.TextStim(win,text='default text', font=sans, name='message',
    height=float(0.04), wrapWidth=1100,
    color='black', 
    )

instrTxt = visual.TextStim(win,text='default text', font=sans, name='instruction',
    pos=[0,0], height=float(0.04), wrapWidth=100,
    color='black',
    ) #object to display instructions 

def instruction(inst_txt='tasks/fixation/Instructions/exp_instr_mv.txt'):
    Instruction = open(inst_txt, 'r').read().split('#\n')
    #
    for i, cur in enumerate(Instruction):
        instrTxt.setText(cur)
        instrTxt.draw()
        win.flip()
        event.waitKeys(keyList=['2','3','4'])

instruction(inst_txt='tasks/fixation/Instructions/exp_instr_mv.txt')

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

def movie_screen(myClock):
	mov = visual.MovieStim3(win, 'tasks/fixation/Inscapes.avi', size=(1024,768), loop=True)
	mov.draw()
	win.flip()
	movie_onset = myClock.getTime()
	while mov.status != visual.FINISHED:
		mov.draw()
		win.flip()
		if event.getKeys(keyList=['escape']):
			break
	return movie_onset

movStart = movie_screen(myClock)
movEnd = myClock.getTime()
movDur = movEnd - movStart

with open(csv_file, "ab") as p:
	writer = csv.writer(p)
	writer.writerow([movStart, movEnd, movDur])

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

