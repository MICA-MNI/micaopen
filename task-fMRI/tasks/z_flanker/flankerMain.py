#!/usr/bin/env python2
"""Implement the Erikson Flanker Task
described in Eichele 2008 (doi: doi: 10.1073/pnas.0708965105)"""
# FlankerTask.py
# Created 1/22/15 by DJ based on NumericalSartTask.py
# Updated 11/9/15 by DJ - cleanup

from psychopy import core, visual, gui, data, event, sound, logging
from psychopy.tools.filetools import fromFile, toFile
from random import randint
import time, numpy as np
import math 
from pandas import DataFrame
import os, sys 
# import AppKit # for monitor size detection
  
# ====================== #
# ===== PARAMETERS ===== #
# ====================== #
# Declare primary task parameters
isPractice = False      # give subject feedback when they get it wrong?
blockLengths = [52,52] # how many trials in each block? The length of this list will be the number of blocks.
nBlocks = len(blockLengths) # how many blocks will there be?
proportionCongruent = .5 # The proportion of congruent-incongruent trials.
randomizeBlocks = True   # scramble the blockLengths list, or perform blocks in order given?
ITI_min = 4.5           # fixation dot before arrows appear
ITI_range = 3.0         # ITI will be between ITI_min and ITI_min + ITI_range (in seconds)
flankerDur = 0.080      # time flanker arrows are onscreen before target (in seconds)
targetDur = 0.030       # time target arrow is onscreen (in seconds)
respDur = 1.4           # max time (after onset of target) to respond (in seconds)
blankDur = 0            # time between response period and fixation dot reappearance (in seconds)
breakWait = 10          # breaktime between blocks
startWait = 0 			# Waiting time at start of first block. 
respKeys = ['3', '1']   # keys to be used for responses
triggerKey = ['5','t']        # key from scanner that says scan is starting
escapeKey = ['escape','q'] # key to exit the experiment 
isFullScreen = True     # run in full screen mode?
screenToShow = 0        # display on primary screen (0) or secondary (1)?
fixCrossSize = 10       # size of cross, in pixels
arrowChars = [u"\u2190", u"\u2192"]#, u"\u9633"] # unicode for left and right arrows and white square
arrowNames = ['Left','Right']#,'Neutral']
arrowSize  = 62
flankerPos = [arrowSize*x for x in [-2, -1, 1, 2]]
rtDeadline = 1.400      # responses after this time will be considered too slow (in seconds)
rtTooSlowDur = 0.600    # duration of 'too slow!' message (in seconds)
sans = []#['Arial','Gill Sans MT', 'Helvetica','Verdana'] # Use the first font on the list. 
#isRtThreshUsed = True   # determine response deadline according to a performance threshold?
#rtThreshFraction = 0.80 # recommend deadline (respDur) for next session as level at which this fraction of trials had RTs under the deadline.
#nCoherentsAtEnd = 0    # make last few stimuli coherent to allow mind-wandering before probes
# wanderKey = 'z'         # key to be used to indicate mind-wandering
# nTrialsPerBlock = 10    # how many trials between breaks?


# declare probe parameters
#probeProb = 0 # probablilty that a given block will be followed by a probe
#probe_strings = []
#probe_options = []
#probe_strings.append('Just now, what were you thinking about?')
#probe_options.append(['What I had to do in the task just now (like getting the current trial right)',
#    'Something else happening just now (like the scanner sounds)',
#    'Something else about the task (like how well I was doing)',
#    'Something else entirely (like what you had for breakfast)',
#    'I was asleep.'])
#probe_strings.append('Where was your attention focused just before this?')
#probe_options.append(['Completely on the task','Mostly on the task','Not sure','Mostly on inward thoughts','Completely on inward thoughts'])
#probe_strings.append('How aware were you of where your attention was?')
#probe_options.append(['Very aware','Somewhat aware','Neutral','Somewhat unaware','Very unaware'])


# randomize list of block lengths
if randomizeBlocks:
    np.random.shuffle(blockLengths)

# ========================== #
# ===== SET UP LOGGING ===== #
# ========================== #
try:#try to get a previous parameters file
    expInfo = fromFile('lastFlankerParams.pickle')
    expInfo['session'] +=1 # automatically increment session number
except:#if not there then use a default set
    expInfo = {'subject':'1', 'session':1}
dateStr = time.strftime("%b_%d_%H%M", time.localtime())#add the current time

#present a dialogue to change params
dlg = gui.DlgFromDict(expInfo, title='Flanker task', fixed=['date'], order=['subject','session'])
if dlg.OK:
    #toFile('lastFlankerParams.pickle', expInfo)#save params to file for next time
	# Skip
	tmpVar=True
else:
    core.quit()#the user hit cancel so exit

expName='Flanker'
expInfo['date'] = data.getDateStr()  # add a simple timestamp

# Output file path, add .csv .xlsx later. 
_thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
os.chdir(_thisDir)
filename = _thisDir + os.sep + 'data' + os.sep + '%s_%s_%s' %(expInfo['subject'], expName, expInfo['date'])

#make a log file to save parameter/event  data
# fileName = 'Flanker-%s-%d-%s'%(expInfo['subject'], expInfo['session'], dateStr) #'Sart-' + expInfo['subject'] + '-' + expInfo['session'] + '-' + dateStr
logging.LogFile((filename+'.log'), level=logging.INFO)#, mode='w') # w=overwrite
logging.log(level=logging.INFO, msg='---START PARAMETERS---')
logging.log(level=logging.INFO, msg='subject: %s'%expInfo['subject'])
logging.log(level=logging.INFO, msg='session: %s'%expInfo['session'])
logging.log(level=logging.INFO, msg='date: %s'%dateStr)
logging.log(level=logging.INFO, msg='isPractice: %i'%isPractice)
logging.log(level=logging.INFO, msg='blockLengths: %s'%blockLengths)
logging.log(level=logging.INFO, msg='randomizeBlocks: %d'%randomizeBlocks)
logging.log(level=logging.INFO, msg='ITI_min: %f'%ITI_min)
logging.log(level=logging.INFO, msg='ITI_range: %f'%ITI_range)
logging.log(level=logging.INFO, msg='flankerDur: %f'%flankerDur)
logging.log(level=logging.INFO, msg='targetDur: %f'%targetDur)
logging.log(level=logging.INFO, msg='respDur: %d'%respDur)
logging.log(level=logging.INFO, msg='blankDur: %f'%blankDur)
#logging.log(level=logging.INFO, msg='IBI: %f'%IBI)
logging.log(level=logging.INFO, msg='respKeys: %s'%respKeys)
#logging.log(level=logging.INFO, msg='wanderKey: %s'%wanderKey)
logging.log(level=logging.INFO, msg='triggerKey: %s'%triggerKey)
logging.log(level=logging.INFO, msg='isFullScreen: %i'%isFullScreen)
logging.log(level=logging.INFO, msg='fixCrossSize: %f'%fixCrossSize)
logging.log(level=logging.INFO, msg='rtDeadline: %f'%rtDeadline)
logging.log(level=logging.INFO, msg='rtTooSlowDur: %f'%rtTooSlowDur)
#logging.log(level=logging.INFO, msg='isRtThreshUsed: %i'%isRtThreshUsed)
#logging.log(level=logging.INFO, msg='rtThreshFraction: %f'%rtThreshFraction)
#logging.log(level=logging.INFO, msg='nCoherentsAtEnd: %d'%nCoherentsAtEnd)
#logging.log(level=logging.INFO, msg='probeProb: %f'%probeProb)
logging.log(level=logging.INFO, msg='---END PARAMETERS---')

# ========================== #
# ===== SET UP STIMULI ===== #
# ========================== #

# kluge for secondary monitor
# if isFullScreen and screenToShow>0: 
#     screens = AppKit.NSScreen.screens()
#     screenRes = screens[screenToShow].frame().size.width, screens[screenToShow].frame# ().size.height
#    screenRes = [1920, 1200]
#     isFullScreen = False
# else:
screenRes = [1024,768]


#create window and stimuli
globalClock = core.Clock()#to keep track of time
trialClock = core.Clock()#to keep track of time
win = visual.Window(screenRes, fullscr=isFullScreen, allowGUI=False, monitor='testMonitor', screen=screenToShow, units='pix', name='win', color=[0.700,0.700,0.700])
#fixation = visual.GratingStim(win, color='black', tex=None, mask='circle',size=0.2)
#fixation = visual.ShapeStim(win,lineColor='#000000',lineWidth=3.0,vertices=((-fixCrossSize/2,0),(fixCrossSize/2,0),(0,0),(0,fixCrossSize/2),(0,-fixCrossSize/2)),units='pix',closeShape=False);
fixation = visual.TextStim(win, name='fixation', text='+', height=62, pos=(0,0),color='black')#set pix pos
message1 = visual.TextStim(win, pos=[0,+100], color='#000000', alignHoriz='center', name='topMsg', text="aaa")
message2 = visual.TextStim(win, pos=[0,-100], color='#000000', alignHoriz='center', name='bottomMsg', text="bbb")
# make target arrow
target = visual.TextStim(win,pos=[0,0], color='#000000', alignHoriz='center', height=arrowSize, name='target', text = arrowChars[0],font=sans)
flankers = []
for i in range(0,len(flankerPos)):
    flankers.append(visual.TextStim(win,pos=[flankerPos[i],0], color='#000000', alignHoriz='center', height=arrowSize , name='flanker%d'%(i+1), text = arrowChars[1], font=sans))
# make too-slow message
tooSlowStim = visual.TextStim(win, pos=[0,0], color='red', alignHoriz='center', name='tooSlow', text="Too Slow!",height=30)



# declare list of prompts
topPrompts = ["Keep your eyes on the cross at the center of the screen when it appears. You will then see a series of arrows.",
    "Using your right hand, press the left button whenever the middle arrow points left and right button when it points right.",
#    "Please respond as quickly as possible without sacrificing accuracy.",
    "If you answer too slowly, you'll see a message reminding you to speed up. Please respond as accurately as possible without being slower than this deadline.",
#    "If at any time you notice that your mind has been wandering, press the '%c' key with your left index finger."%wanderKey.upper(),
#    "Sometimes, a question may appear. When this happens, answer the question using the number keys."]
	" "]
bottomPrompts = ["Press any key to continue.",
    "Press any key to continue.",
    "Press any key to continue.",
#    "Press any key to continue.",
    "When you're ready to begin, press any key."]

# ============================ #
# ======= SUBFUNCTIONS ======= #
# ============================ #

def RunTrial(targetDir,flankerDir,tStartTrial):
    
    # display fixation cross
    fixation.draw()
    win.logOnFlip(level=logging.EXP, msg='Display Fixation')
    win.flip()
    
    # wait until it's time to start the new trial
    while globalClock.getTime()<tStartTrial:
        pass # do nothing
    
    # get trial time
    tTrial = globalClock.getTime()
    # reset clock
    trialClock.reset()
    
    # display flankers
    for flanker in flankers:
        flanker.text = arrowChars[flankerDir]
        flanker.draw()
    win.logOnFlip(level=logging.EXP, msg='Display %sFlankers'%arrowNames[flankerDir])
    win.flip()
    core.wait(flankerDur,flankerDur)
    
    # display flankers AND target arrow
    for flanker in flankers:
        flanker.draw()
    target.text = arrowChars[targetDir]
    target.draw()
    win.logOnFlip(level=logging.EXP, msg='Display %sTarget'%arrowNames[targetDir])
    win.flip()
    tStim = trialClock.getTime() # get time when stim was displayed
    event.clearEvents() # flush buffer
    core.wait(targetDur,targetDur)
    
    #draw blank screen
    win.logOnFlip(level=logging.EXP, msg='Display Blank')
    win.flip()
    core.wait(respDur-targetDur, respDur-targetDur) #wait for specified ms (use a loop of x frames for more accurate timing)
    
    # get responses
    allKeys = event.getKeys(timeStamped=trialClock)
    # find RT
    RT = float('Inf')
    for thisKey in allKeys:
        if thisKey[0] in respKeys:
            RT = thisKey[1]-tStim
            break
                
    if RT >= rtDeadline:
        tooSlowStim.draw()
        win.logOnFlip(level=logging.EXP, msg='Display TooSlow')
        win.flip()
        core.wait(rtTooSlowDur,rtTooSlowDur)
                
    # return trial time, response(s)
    return (tTrial,allKeys)


def RunProbes():
    
    # initialize response list
    allKeys = []
    # set up stimuli
    for iProbe in range(0,len(probe_strings)):
        respText = ""
        for iResp in range(0,len(probe_options[iProbe])):
            respText.append('%d) %s\n'%(iResp+1),probe_options[iProbe][iResp])
        message1.setText(probe_strings[iProbe])
        message2.setText(respText)
        message1.draw()
        message2.draw()
        win.logOnFlip(level=logging.EXP, msg='Display Probe%d'%(iProbe+1))
        win.flip()
        # reset clock
        trialClock.reset()
        # get response
        newKey = event.waitKeys(keyList=['1','2','3','4','5','q','escape'],timeStamped=trialClock)
        allKeys.append(newKey)
    
    # return results
    return (allKeys)
    
def GetTrialsInBlock(nTrialsPerBlock,proportionCongruent):
    numCongruent = int(math.ceil(nTrialsPerBlock * proportionCongruent))
    trials = [[True] * numCongruent, [False] * (nTrialsPerBlock - numCongruent)]
    trials = [item for sublist in trials for item in sublist]
    np.random.shuffle(trials)
    return (trials)    

# =========================== #
# ======= RUN PROMPTS ======= #
# =========================== #

# display prompts
iProbe = 0
while iProbe < len(topPrompts):
    message1.setText(topPrompts[iProbe])
    message2.setText(bottomPrompts[iProbe])
    #display instructions and wait
    message1.draw()
    message2.draw()
    win.logOnFlip(level=logging.EXP, msg='Display Instructions%d'%(iProbe+1))
    win.flip()
    #check for a keypress
    thisKey = event.waitKeys()
    if thisKey[0] in escapeKey:
        win.close()
        core.quit()
    elif thisKey[0] == 'backspace':
        iProbe = 0
    else:
        iProbe += 1

# wait for scanner
message1.setText("Waiting for scanner to start...")
message2.setText("")
#message2.setText("(Press '%c' to override.)"%triggerKey.upper())
message1.draw()
message2.draw()
win.logOnFlip(level=logging.EXP, msg='Display WaitingForScanner')
win.flip()
keyPress = event.waitKeys(keyList=(triggerKey + escapeKey))
globalClock.reset()

if keyPress[0] in escapeKey:
    win.close()
    core.quit()

# do brief wait before first stimulus
fixation.draw()
win.logOnFlip(level=logging.EXP, msg='Display Fixation')
win.flip()
core.wait(startWait, startWait)

# =========================== #
# ===== MAIN EXPERIMENT ===== #
# =========================== #

# set up performance variables
wasTarget = False # was the last trial a target?
isCorrect_alltrials = np.zeros(sum(blockLengths), dtype=np.bool)
targetDir_alltrials = np.zeros(sum(blockLengths), dtype=np.bool)
flankerDir_alltrials = np.zeros(sum(blockLengths), dtype=np.bool)
isCongruent_alltrials = np.zeros(sum(blockLengths), dtype=np.bool)
startTime_alltrials = np.zeros(sum(blockLengths), dtype=np.float64)
RT_alltrials = np.zeros(sum(blockLengths))

# set up other stuff
logging.log(level=logging.EXP, msg='---START EXPERIMENT---')

for iBlock in range(0,nBlocks): # for each block of trials
    
    # determine next trial time
    ITI = ITI_min + np.random.random()*ITI_range
    tNextTrial = globalClock.getTime()+ITI
    # log new block
    logging.log(level=logging.EXP, msg='Start Block %d'%iBlock)
    nTrialsPerBlock = blockLengths[iBlock]
    trialList = GetTrialsInBlock(nTrialsPerBlock,proportionCongruent)
    
    for iTrial in range(0,nTrialsPerBlock): # for each trial
        
        # determine trial type
        flankerDir = (np.random.random() < 0.5)
        if trialList[iTrial] is True:
		    targetDir = flankerDir
        else:
            targetDir = not flankerDir 
	            
        # Run Trial
        [tTrial, allKeys] = RunTrial(targetDir,flankerDir,tNextTrial)
        
        # determine next trial time
        ITI = ITI_min + np.random.random()*ITI_range
        tNextTrial = tTrial+ITI
        
        # check responses
        keyChar = 0
        RT = np.nan
        for thisKey in allKeys:
            # check for escape keypresses
            if thisKey[0] in escapeKey:
                win.close()
                core.quit()#abort experiment
            # check for responses
            elif thisKey[0] in respKeys:
                keyChar = thisKey[0] #record key
                RT = thisKey[1]*1000 #in ms
        if keyChar == respKeys[targetDir]:
            thisResp = True # correct
        else:
            thisResp = False # incorrect
        event.clearEvents('mouse')#only really needed for pygame windows
        
        # give feedback if this is practice
        if isPractice and thisResp==0:
            message1.setText("Whoops! That was incorrect. Press the LEFT button whenever the middle arrow points LEFT and the RIGHT button when it points RIGHT.")
            message2.setText("Press any key to continue.")
            message1.draw()
            message2.draw()
            win.logOnFlip(level=logging.EXP, msg='Display Feedback')
            win.flip()
            core.wait(0.25) # quick pause to make sure they see it
            event.waitKeys()
        
#        print("Trial %d: key pressed = %s, isTarget = %r, correct = %d, RT= %.1f" %(iTrial+1,keyChar,isTarget,thisResp,RT))
        #log the data
        iLog = iBlock*nTrialsPerBlock + iTrial
        isCorrect_alltrials[iLog] = thisResp
        RT_alltrials[iLog] = RT
        isCongruent_alltrials[iLog] = (flankerDir == targetDir)
        flankerDir_alltrials[iLog] = flankerDir
        targetDir_alltrials[iLog] = targetDir
        startTime_alltrials[iLog] = tTrial
        # do ITI
        if blankDur > 0:
            win.logOnFlip(level=logging.EXP, msg='Display Blank')
            win.flip()
            core.wait(blankDur,blankDur)
        #===END TRIAL LOOP===#
    
    # Run probe trial
#    if (np.random.random() < probeProb):
#        # run probe trial
#        allKeys = RunProbes()
#        # check for escape keypresses
#        for thisKey in allKeys:
#            if thisKey[0] in ['q', 'escape']:
#                core.quit()#abort experiment
#        event.clearEvents('mouse')#only really needed for pygame windows
     
    # skip IBI on last block
    if iBlock < (nBlocks-1):
        # Display wait screen
        message1.setText("Take a break!")
        message1.draw()
        win.logOnFlip(level=logging.EXP, msg='Display BreakTime')
        win.flip()
        core.wait(breakWait,breakWait)
#        thisKey = event.waitKeys()
#        if thisKey[0] in escapeKey:
#            win.close()
#            core.quit() #abort experiment
        # do IBI (blank screen)
        win.logOnFlip(level=logging.EXP, msg='Display Blank')
        win.flip()
        core.wait(startWait,startWait)

# Save data
df = DataFrame({'Start Time': startTime_alltrials,'Congruent (1=yes)': isCongruent_alltrials, 'Correct': isCorrect_alltrials, 'Reaction Time': RT_alltrials,'Target Dir (0=left)':targetDir_alltrials})
df = df [['Start Time', 'Congruent (1=yes)', 'Correct','Reaction Time', 'Target Dir (0=left)']]
df.to_excel(filename + '.xlsx', sheet_name='sheet1',index=False,merge_cells=False)   
print df 
  

#give some performance output to user
#isC = isCongruent_alltrials!=0
#isI = np.logical_not(isCongruent_alltrials)
#print('---Performance:')
#print('All: %d/%d = %.2f%% correct' %(np.nansum(isCorrect_alltrials), len(isCorrect_alltrials), 100*np.nanmean(isCorrect_alltrials)))
#print('Congruent: %d/%d = %.2f%% correct' %(np.nansum(isCorrect_alltrials[isC]), np.nansum(isC), 100*np.nanmean(isCorrect_alltrials[isC])))
#print('Incongruent: %d/%d = %.2f%% correct' %(np.nansum(isCorrect_alltrials[isI]), np.nansum(isI), 100*np.nanmean(isCorrect_alltrials[isI])))
#print('---Reaction Time:')
#print('All: mean = %.4f, std = %.4f' %(np.nanmean(RT_alltrials), np.nanstd(RT_alltrials)))
#print('Congruent: mean = %.4f, std = %.4f' %(np.nanmean(RT_alltrials[isC]), np.nanstd(RT_alltrials[isC])))
#print('Incongruent: mean = %.4f, std = %.4f' %(np.nanmean(RT_alltrials[isI]), np.nanstd(RT_alltrials[isI])))
# exit experiment
win.close()
core.quit()
