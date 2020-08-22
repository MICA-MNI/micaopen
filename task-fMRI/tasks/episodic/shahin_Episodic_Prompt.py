#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.84.1),
    on Wed 23 Nov 2016 10:03:30 GMT
If you publish work using this script please cite the PsychoPy publications:
    Peirce, JW (2007) PsychoPy - Psychophysics software in Python.
        Journal of Neuroscience Methods, 162(1-2), 8-13.
    Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy.
        Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008
"""

from __future__ import absolute_import, division
from psychopy import locale_setup, gui, visual, core, data, event, logging, sound
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import sys  # to get file system encoding

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
os.chdir(_thisDir)

# Store info about the experiment session
expName = 'Episodic_Task'  # from the Builder filename that created this script
expInfo = {u'session': u'001', u'participant': u'',u'promptlist': ['A','B','C','D']}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + 'data' + os.sep + '%s_%s_%s' %(expInfo['participant'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath=None,
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.INFO)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp

# Start Code - component code to be run before the window creation

# Setup the Window
win = visual.Window(
    size=(1920, 1080), fullscr=True, screen=0,
    allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0.700,0.700,0.700], colorSpace='rgb',
    blendMode='avg', useFBO=True)
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

# Initialize components for Routine "Instructions"
InstructionsClock = core.Clock()
instructions_text = visual.TextStim(win=win, name='instructions_text',
    text='Now that you have tried to memorize the first list of words, you will be presented a second list.\n\nOnce again, you will be prompted to one word at a time.\n\nFor each word, you must determine whether or not it belongs to the previous list.\n\nUse the button box to answer...bla bla bla...\n\n\n\nPress any button to start.',
    font='Arial',
    pos=[0, 0], height=0.075, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1,
    depth=0.0);



# Initialize components for Routine "WaitForTrigger"
WaitForTriggerClock = core.Clock()
from psychopy.hardware.emulator import launchScan
#
# settings for launchScan:
MR_settings = { 
    'TR': 0.585, # duration (sec) per volume
    'volumes': 1500, # number of whole-brain 3D volumes / frames
    'sync': '5', # character to use as the sync timing event; assumed to come at start of a volume
    'skip': 0, # number of volumes lacking a sync pulse at start of scan (for T1 stabilization)
    }

# Initialize components for Routine "dummy"
dummyClock = core.Clock()
dummy_text = visual.TextStim(win=win, name='dummy_text',
    text='+',
    font='Arial',
    pos=(0, 0), height=0.3, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1,
    depth=0.0);

# Initialize components for Routine "Episodic_Trial"
Episodic_TrialClock = core.Clock()
timerStarted = False
import random
xpositions = [-0.5,0,0.5]
posResponse = 0
prime_text = visual.TextStim(win=win, name='prime_text', 
    font='Arial',
    pos=[0, 0], height=0.15, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1,
    depth=0.0);
#target_text = visual.TextStim(win=win, name='target_text',
 #   text='default text',
  #  font='Arial',
   # pos=[0,0], height=0.15, wrapWidth=None, ori=0, 
    #color='black', colorSpace='rgb', opacity=1,
    #depth=-4.0);
#dist1_text = visual.TextStim(win=win, name='dist1_text',
 #   text='default text',
  #  font='Arial',
   # pos=[0,0], height=0.15, wrapWidth=None, ori=0, 
    #color='black', colorSpace='rgb', opacity=1,
    #depth=-5.0);
#dist2_text = visual.TextStim(win=win, name='dist2_text',
 #   text='default text',
  #  font='Arial',
   # pos=[0,0], height=0.15, wrapWidth=None, ori=0, 
    #color='black', colorSpace='rgb', opacity=1,
    #depth=-6.0);

# Initialize components for Routine "Fixation"
FixationClock = core.Clock()
fixList = [1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,1.5,2.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,2.0,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.0,3.5,3.5,3.5,3.5,3.5,3.5,3.5,3.5,3.5,3.5,3.5,3.5,3.5,3.5,3.5,3.5,3.5,3.5,3.5,3.5]
fixation_text = visual.TextStim(win=win, name='fixation_text',
    text='+',
    font='Arial',
    pos=[0, 0], height=0.3, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1,
    depth=-1.0);


# Initialize components for Routine "ThankYou"
ThankYouClock = core.Clock()
thankyou_text = visual.TextStim(win=win, name='thankyou_text',
    text='End of list',
    font='Arial',
    pos=[0, 0], height=0.1, wrapWidth=None, ori=0, 
    color='black', colorSpace='rgb', opacity=1,
    depth=0.0);

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# ------Prepare to start Routine "Instructions"-------
t = 0
InstructionsClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
key_resp_2 = event.BuilderKeyResponse()
# keep track of which components have finished
InstructionsComponents = [instructions_text, key_resp_2]
for thisComponent in InstructionsComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "Instructions"-------
while continueRoutine:
    # get current time
    t = InstructionsClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *instructions_text* updates
    if t >= 0.0 and instructions_text.status == NOT_STARTED:
        # keep track of start time/frame for later
        instructions_text.tStart = t
        instructions_text.frameNStart = frameN  # exact frame index
        instructions_text.setAutoDraw(True)
    
    # *key_resp_2* updates
    if t >= 0.0 and key_resp_2.status == NOT_STARTED:
        # keep track of start time/frame for later
        key_resp_2.tStart = t
        key_resp_2.frameNStart = frameN  # exact frame index
        key_resp_2.status = STARTED
        # keyboard checking is just starting
        event.clearEvents(eventType='keyboard')
    if key_resp_2.status == STARTED:
        theseKeys = event.getKeys(keyList=['1','2','3','4'])
        
        # check for quit:
        if "escape" in theseKeys:
            endExpNow = True
        if len(theseKeys) > 0:  # at least one key was pressed
            # a response ends the routine
            continueRoutine = False
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in InstructionsComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "Instructions"-------
for thisComponent in InstructionsComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# the Routine "Instructions" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "WaitForTrigger"-------
t = 0
WaitForTriggerClock.reset()  # clock
frameN = -1
continueRoutine = True
# update component parameters for each repeat
vol = launchScan(win, MR_settings, globalClock=globalClock,mode='Scan')
# keep track of which components have finished
WaitForTriggerComponents = []
for thisComponent in WaitForTriggerComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "WaitForTrigger"-------
while continueRoutine:
    # get current time
    t = WaitForTriggerClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in WaitForTriggerComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "WaitForTrigger"-------
for thisComponent in WaitForTriggerComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

# the Routine "WaitForTrigger" was not non-slip safe, so reset the non-slip timer
routineTimer.reset()

# ------Prepare to start Routine "dummy"-------
t = 0
dummyClock.reset()  # clock
frameN = -1
continueRoutine = True
routineTimer.add(6.000000)
# update component parameters for each repeat
# keep track of which components have finished
dummyComponents = [dummy_text]
for thisComponent in dummyComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "dummy"-------
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = dummyClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *dummy_text* updates
    if t >= 0.0 and dummy_text.status == NOT_STARTED:
        # keep track of start time/frame for later
        dummy_text.tStart = t
        dummy_text.frameNStart = frameN  # exact frame index
        dummy_text.setAutoDraw(True)
    frameRemains = 0.0 + 6.0- win.monitorFramePeriod * 0.75  # most of one frame period left
    if dummy_text.status == STARTED and t >= frameRemains:
        dummy_text.setAutoDraw(False)
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in dummyComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "dummy"-------
for thisComponent in dummyComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

# set up handler to look after randomisation of conditions etc
episodic_trials_loop = data.TrialHandler(nReps=1, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=data.importConditions(u'conds' + os.sep + 'Shahin_Episodic_Prompt' + expInfo['promptlist'] + '.csv'),
    seed=None, name='episodic_trials_loop')
thisExp.addLoop(episodic_trials_loop)  # add the loop to the experiment
thisEpisodic_trials_loop = episodic_trials_loop.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisEpisodic_trials_loop.rgb)
if thisEpisodic_trials_loop != None:
    for paramName in thisEpisodic_trials_loop.keys():
        exec(paramName + '= thisEpisodic_trials_loop.' + paramName)

for thisEpisodic_trials_loop in episodic_trials_loop:
    currentLoop = episodic_trials_loop
    # abbreviate parameter names if possible (e.g. rgb = thisEpisodic_trials_loop.rgb)
    if thisEpisodic_trials_loop != None:
        for paramName in thisEpisodic_trials_loop.keys():
            exec(paramName + '= thisEpisodic_trials_loop.' + paramName)
    
    # ------Prepare to start Routine "Episodic_Trial"-------
    t = 0
    Episodic_TrialClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    routineTimer.add(4.000000)
    # update component parameters for each repeat
    if not timerStarted: 
        startTime = globalClock.getTime() 
        timerStarted = True 
    
    # now save a start time for every trial (hence, not indented): 
    thisExp.addData("Trial_start", globalClock.getTime() - startTime)
    random.shuffle(xpositions)
    # now save the positions: 
    thisExp.addData("Position1", xpositions[0])
    thisExp.addData("Position2", xpositions[1])
    thisExp.addData("Position3", xpositions[2])
    if xpositions[0] == -0.5:
     posResponse = 3 # On our button box we have the following mapping: 1-right,2-bottom,3-left,4-top
    elif xpositions[0] == 0:
     posResponse = 2
    elif xpositions[0] == 0.5:
     posResponse = 1
    prime_text.setText(prompt)
    #target_text.setText(target)
    #target_text.setPos([xpositions[0], -0.2])
    #dist1_text.setText(dist1)
    #dist1_text.setPos([xpositions[1], -0.2])
    #dist2_text.setText(dist2)
    #dist2_text.setPos([xpositions[2], -0.2])
    key_response = event.BuilderKeyResponse()
    # keep track of which components have finished
    Episodic_TrialComponents = [prime_text, key_response]
    for thisComponent in Episodic_TrialComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "Episodic_Trial"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = Episodic_TrialClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        
        
        
        # *prime_text* updates
        if t >= 0.0 and prime_text.status == NOT_STARTED:
            # keep track of start time/frame for later
            prime_text.tStart = t
            prime_text.frameNStart = frameN  # exact frame index
            prime_text.setAutoDraw(True)
        frameRemains = 0.0 + 4.0- win.monitorFramePeriod * 0.75  # most of one frame period left
        if prime_text.status == STARTED and t >= frameRemains:
            prime_text.setAutoDraw(False)
        
        # *target_text* updates
        #if t >= 0.0 and target_text.status == NOT_STARTED:
            # keep track of start time/frame for later
         #   target_text.tStart = t
          #  target_text.frameNStart = frameN  # exact frame index
           # target_text.setAutoDraw(True)
        #frameRemains = 0.0 + 4.0- win.monitorFramePeriod * 0.75  # most of one frame period left
        #if target_text.status == STARTED and t >= frameRemains:
         #   target_text.setAutoDraw(False)
        
        # *dist1_text* updates
        #if t >= 0.0 and dist1_text.status == NOT_STARTED:
            # keep track of start time/frame for later
         #   dist1_text.tStart = t
          #  dist1_text.frameNStart = frameN  # exact frame index
           # dist1_text.setAutoDraw(True)
        #frameRemains = 0.0 + 4.0- win.monitorFramePeriod * 0.75  # most of one frame period left
        #if dist1_text.status == STARTED and t >= frameRemains:
         #   dist1_text.setAutoDraw(False)
        
        # *dist2_text* updates
        #if t >= 0.0 and dist2_text.status == NOT_STARTED:
            # keep track of start time/frame for later
         #   dist2_text.tStart = t
          #  dist2_text.frameNStart = frameN  # exact frame index
           # dist2_text.setAutoDraw(True)
        #frameRemains = 0.0 + 4.0- win.monitorFramePeriod * 0.75  # most of one frame period left
        #if dist2_text.status == STARTED and t >= frameRemains:
         #   dist2_text.setAutoDraw(False)
        
        # *key_response* updates
        if t >= 0.0 and key_response.status == NOT_STARTED:
            # keep track of start time/frame for later
            key_response.tStart = t
            key_response.frameNStart = frameN  # exact frame index
            key_response.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(key_response.clock.reset)  # t=0 on next screen flip
            event.clearEvents(eventType='keyboard')
        frameRemains = 0.0 + 4.0- win.monitorFramePeriod * 0.75  # most of one frame period left
        if key_response.status == STARTED and t >= frameRemains:
            key_response.status = STOPPED
        if key_response.status == STARTED:
            theseKeys = event.getKeys(keyList=['1', '2', '3'])
            
            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                key_response.keys = theseKeys[-1]  # just the last key pressed
                key_response.rt = key_response.clock.getTime()
                # was this 'correct'?
                if (key_response.keys == str(posResponse)) or (key_response.keys == posResponse):
                    key_response.corr = 1
                else:
                    key_response.corr = 0
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Episodic_TrialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "Episodic_Trial"-------
    for thisComponent in Episodic_TrialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    
    
    
    # check responses
    if key_response.keys in ['', [], None]:  # No response was made
        key_response.keys=None
        # was no response the correct answer?!
        if str(posResponse).lower() == 'none':
           key_response.corr = 1  # correct non-response
        else:
           key_response.corr = 0  # failed to respond (incorrectly)
    # store data for episodic_trials_loop (TrialHandler)
    episodic_trials_loop.addData('key_response.keys',key_response.keys)
    episodic_trials_loop.addData('key_response.corr', key_response.corr)
    if key_response.keys != None:  # we had a response
        episodic_trials_loop.addData('key_response.rt', key_response.rt)
    
    # ------Prepare to start Routine "Fixation"-------
    t = 0
    FixationClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # update component parameters for each repeat
    random.shuffle(fixList)
    fixDuration = fixList[0]
    
    # keep track of which components have finished
    FixationComponents = [fixation_text]
    for thisComponent in FixationComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    # -------Start Routine "Fixation"-------
    while continueRoutine:
        # get current time
        t = FixationClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        
        # *fixation_text* updates
        if t >= 0.0 and fixation_text.status == NOT_STARTED:
            # keep track of start time/frame for later
            fixation_text.tStart = t
            fixation_text.frameNStart = frameN  # exact frame index
            fixation_text.setAutoDraw(True)
        frameRemains = 0.0 + fixDuration- win.monitorFramePeriod * 0.75  # most of one frame period left
        if fixation_text.status == STARTED and t >= frameRemains:
            fixation_text.setAutoDraw(False)
        
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in FixationComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "Fixation"-------
    for thisComponent in FixationComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    
    thisExp.addData("Fixation duration", fixList[0])
    del fixList[0] 
    # the Routine "Fixation" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    thisExp.nextEntry()
    
# completed 1 repeats of 'episodic_trials_loop'


# ------Prepare to start Routine "ThankYou"-------
t = 0
ThankYouClock.reset()  # clock
frameN = -1
continueRoutine = True
routineTimer.add(5.000000)
# update component parameters for each repeat
# keep track of which components have finished
ThankYouComponents = [thankyou_text]
for thisComponent in ThankYouComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

# -------Start Routine "ThankYou"-------
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = ThankYouClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *thankyou_text* updates
    if t >= 0.0 and thankyou_text.status == NOT_STARTED:
        # keep track of start time/frame for later
        thankyou_text.tStart = t
        thankyou_text.frameNStart = frameN  # exact frame index
        thankyou_text.setAutoDraw(True)
    frameRemains = 0.0 + 5.0- win.monitorFramePeriod * 0.75  # most of one frame period left
    if thankyou_text.status == STARTED and t >= frameRemains:
        thankyou_text.setAutoDraw(False)
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in ThankYouComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()


# -------Ending Routine "ThankYou"-------
for thisComponent in ThankYouComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)






# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
