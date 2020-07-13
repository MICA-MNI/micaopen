from psychopy import visual, core, event
from numpy.random import randint, shuffle, choice, random, sample
import random 
import numpy as np
from baseDef import*
import csv
import pickle
from pdb import set_trace as bp
import re
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
    
def instruction(inst_txt='Instructions/exp_instr2_symbolic.txt'):
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

def task(myClock, expInfo, f):
	stimuli_list = load_conditions_dict("Episodic_Encoding_symbolic/Episodic_List" + expInfo['symbol list'] + '.csv') # loads stimuli from specified directory
	regex = re.compile(expInfo['subject'] + '_' + expInfo['session'] + '.*' + expInfo['symbol list']) # '.*[A-B]$'
	dirfiles = os.listdir('data_Episodic Encoding Task (symbolic)/')
	targetfile = [s for s in dirfiles if re.match(regex,s)]
	if len(targetfile) > 1: 
		pass #Add some error	
	with open('data_Episodic Encoding Task (symbolic)/' + targetfile[0], "rb") as fp:
		list3 = pickle.load(fp)
		
	encoded_list = list3 # name change to reflect that list3 contained the pairs that were encoded		
	shuffle(encoded_list) # shuffle order of paired items from encoded_list
	prime_and_correct_stimuli = [[stimuli_list[x[0]]['stimulus_1'], stimuli_list[x[1]]['stimulus_2']] for x in encoded_list] # create a library of the prime and correct target stimuli
	
	# to create the prime_stimuli & correct_tg_stimuli #########################################################################
	prime_and_correct_array = np.asarray(prime_and_correct_stimuli) # create an array version of prime_and_correct_stimuli
	R_list = [(0,1),(1,0)] # create a list for the permutation factor "R"
	R = np.asarray(R_list) # create the "R" factor array
	new_array = prime_and_correct_array[:,R] # create all possible permutations for prime_and_correct_array given "R" as factor
	new_stimuli = np.array(new_array).tolist() # convert the new_array into list format
	random_stimuli = [random.choice(x) for x in new_stimuli] # randomize the new_stimuli
	prime_stimuli = [x[0] for x in random_stimuli] # this is the prime_stimuli
	correct_tg_stimuli = [x[1] for x in random_stimuli] # this is the correct_tg_stimuli
    ############################################################################################################################

	# to load the other set of stimuli# 
	if expInfo['symbol list'] == 'A':
		AorB = 'B'	
	if expInfo['symbol list'] == 'B':  ### elif...
		AorB = 'A'	
	###################################
	
	stimuli_list2 = load_conditions_dict("Episodic_Encoding_symbolic/Episodic_List" + AorB + '.csv') # other stimuli list
	random_sample_list1 = random.sample(range(0,len(stimuli_list2)),len(stimuli_list2)) # creates a list containing randomized items for one set of stimuli
	random_sample_list2 = random.sample(range(0,len(stimuli_list2)),len(stimuli_list2)) # creates another list containing randomized items for one set of stimuli
	random_sample_list = zip(random_sample_list1,random_sample_list2)
	false_tg1_stimuli = [stimuli_list2[x[0]]['stimulus_1'] for x in random_sample_list]
	false_tg2_stimuli = [stimuli_list2[x[1]]['stimulus_2'] for x in random_sample_list]
	
	# set positions #######################################################
	prime_position = (0,0.4) # the position of the prime is always the same
	x_values = [-0.5,0,0.5] # the y value for the target images is always the same (i.e., -0.4); only the x values must to be specified
	###########################################################################################################################################
	
	meta_stimuli = zip(prime_stimuli,correct_tg_stimuli,false_tg1_stimuli,false_tg2_stimuli)
	shuffle(meta_stimuli)
	
	for a,b,c,d in meta_stimuli:
		shuffle(x_values) # shuffle the order of elements in x_values
		tg1 = x_values[0] # get the x value for the first position inside x_values
		tg2 = x_values[1] # get the x value for the second position...
		tg3 = x_values[2] # get the x value for the thrid position...
		
		prime_im = visual.ImageStim(win, name='stimPic1', image = None, pos=prime_position)
		correct_tg_im = visual.ImageStim(win, name='stimPic2', image = None, pos=(tg1,-0.4))
		false_tg1_im = visual.ImageStim(win, name='stimPic3', image = None, pos=(tg2,-0.4))
		false_tg2_im = visual.ImageStim(win, name='stimPic4', image = None, pos=(tg3,-0.4))
		fixStart = fixation_screen(myClock, np.arange(1.3,1.75,0.05)[randint(0,9)])
		prime_im.setImage(a)
		prime_im.draw()
		correct_tg_im.setImage(b)
		correct_tg_im.draw()
		false_tg1_im.setImage(c)
		false_tg1_im.draw()
		false_tg2_im.setImage(d)
		false_tg2_im.draw()
		win.flip()
		event.waitKeys(keyList=['1','2','3'])
		event.clearEvents()
		startT = myClock.getTime()
		fixStart = fixation_screen(myClock, np.arange(0.5,1,0.05)[randint(0,10)])

def endExp(f):
	endtxt = open('Instructions/end_instr.txt', 'r').read().split('#\n')[0]
	msgTxt.setText(endtxt)
	msgTxt.draw()
	win.flip()
	event.waitKeys(maxWait = 20)
	f.close()
	win.close()
	core.quit()

