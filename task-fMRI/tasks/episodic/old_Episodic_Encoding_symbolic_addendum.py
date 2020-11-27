from psychopy import visual, core, event
from numpy.random import randint, shuffle, choice, random, sample
import random 
import numpy as np
from baseDef import*
import csv
import pickle
from pdb import set_trace as bp
import os
from psychopy.hardware.emulator import launchScan

sans = ['Arial','Gill Sans MT', 'Helvetica','Verdana'] #use the first font found on this list
win = visual.Window(fullscr=True, color=1, units='norm')

msgTxt = visual.TextStim(win,text='default text', font= sans, name='message',
    height=float(0.07), wrapWidth=1100,
    color='black', 
    )
    
instrTxt = visual.TextStim(win,text='default text', font= sans, name='instruction',
    pos=[0,0], height=float(0.07), wrapWidth=1100,
    color='black',
    ) #object to display instructions 
    
def instruction(inst_txt='Instructions/exp_instr_symbolic.txt'):
    Instruction = open(inst_txt, 'r').read().split('#\n')
    Ready = open('Instructions/wait_trigger.txt', 'r').read()
    #instructions screen
    for i, cur in enumerate(Instruction):
        instrTxt.setText(cur)
        instrTxt.draw()
        win.flip()
        event.waitKeys(keyList=['space'])
    # settings for launchScan:
    MR_settings = {
    'TR': 0.585, # duration (sec) per volume
    'volumes': 1500, # number of whole-brain 3D volumes / frames
    'sync': 'q', # character to use as the sync timing event; assumed to come at start of a volume
    'skip': 0, # number of volumes lacking a sync pulse at start of scan (for T1 stabilization)
    }
    vol = launchScan(win, MR_settings, mode='Scan')    

    instrTxt.setText(Ready)
    instrTxt.draw()
    win.flip()
    event.waitKeys(maxWait = 2)
    if event.getKeys(keyList = ['escape']):
        quitEXP(True)
    #need to update a scanner trigger version
    core.wait(np.arange(1.3,1.75,0.05)[randint(0,9)])        

fixation = visual.TextStim(win, name='fixation', text='+', 
                            font= sans, height=float(0.15), pos=(0,0),color='black')#set pix pos

def fixation_screen(myClock, waittime=1):
    fixation.draw()
    win.logOnFlip(level=logging.EXP, msg='fixation cross on screen') #new log haoting
    win.flip()
    fixStart = myClock.getTime() #fixation cross onset
    if event.getKeys(keyList = ['escape']):
        quitEXP(True)
    core.wait(waittime)
    return fixStart

#def saveResp(f, expInfo, myClock):
 #   write_datalog(f, data='%s,%s,%s,%i,%f,%i,%i,%f,%s,%s\n'
  #      %(expInfo['subject'],expInfo['session']), myClock=myClock)

im1 = visual.ImageStim(win, name='stimPic1', image = None, pos=(-0.2,0))
im2 = visual.ImageStim(win, name='stimPic2', image = None, pos=(0.2,0))

def task(myClock, expInfo, f):
	
    stimuli_list = load_conditions_dict("Episodic_Encoding_symbolic/Episodic_List" + expInfo['symbol list'] + '.csv') # loads stimuli from specified directory
    list1 = random.sample(range(0,len(stimuli_list)),len(stimuli_list)) # creates a list containing randomized items for one set of stimuli (i.e., stimulus_1) 
    list2 = random.sample(range(0,len(stimuli_list)),len(stimuli_list)) # creates a list containing randomized items for another set of stimuli (i.e., stimulus_2)
    list3 = zip(list1,list2) # creates a list of paired items composed of list1 & list2 items
    
    # to save current list3 for subsequent use in episodic recall task #
    list_file = ("data_Episodic Encoding Task (symbolic)/" + expInfo['subject'] + "_" + expInfo['session'] + "_" + expInfo['date'] + "_" +  expInfo['symbol list'])
    with open(list_file, "wb") as fp:
		pickle.dump(list3, fp)
	####################################################################
	   
    pseudo_easy_list = list3[:(len(list3)+1)/2] # creates a list containing the first half of the paired items from list3
    easy_list = pseudo_easy_list*3 # creates a list in which paired items from pseudo_easy_list have been tripled ("easy" pairs will be displayed 3 times during the experiment)
    difficult_list = list3[(len(list3)+1)/2:] # creates a list containing the second half of the paired items from list3 ("difficult" pairs will only be display once during the experiment)
    meta_list = easy_list + difficult_list # creates a final list encompassing the easy_list & difficult_list paired items
    shuffle(meta_list) # shuffles the paired items within meta_list
    
    for x,y in meta_list:
        fixStart = fixation_screen(myClock, np.arange(1.3,1.75,0.05)[randint(0,9)])
        im1.setImage(stimuli_list[x]['stimulus_1'])
        im1.draw()
        im2.setImage(stimuli_list[y]['stimulus_2'])
        im2.draw()		
        win.flip()
        core.wait(5)
        event.clearEvents()
        startT = myClock.getTime()
        fixStart = fixation_screen(myClock, np.arange(0.5,1,0.05)[randint(0,10)])

    
def endExp(f):
    endtxt = open('Instructions/end_instr.txt', 'r').read().split('#\n')[0]
    msgTxt.setText(endtxt)
    msgTxt.draw()
    win.flip()
    event.waitKeys(maxWait = 20)
    logging.flush()
    f.close()
    win.close()
    core.quit()
    
    
    
        
