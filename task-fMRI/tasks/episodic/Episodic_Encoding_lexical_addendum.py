from psychopy import visual, core, event
from numpy.random import randint, shuffle
import numpy as np
from baseDef import*

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
    
def instruction(inst_txt='Instructions/exp_instr_lexical.txt'):
    Instruction = open(inst_txt, 'r').read().split('#\n')
    Ready = open('Instructions/wait_trigger.txt', 'r').read()
    #instructions screen
    for i, cur in enumerate(Instruction):
        instrTxt.setText(cur)
        instrTxt.draw()
        win.flip()
        event.waitKeys(keyList=['space'])

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
    
im = visual.ImageStim(win, name='stimPic', image = None)

def task(myClock, expInfo, f):
    stimuli_list = load_conditions_dict("Episodic_Encoding_lexical/Episodic_List" + expInfo['word list'] + '.csv')
    shuffle(stimuli_list)	
    
    for thisTrial in stimuli_list:
        fixStart = fixation_screen(myClock, np.arange(1.3,1.75,0.05)[randint(0,9)])
        im.setImage(thisTrial['wordpair'])
        im.draw()
        win.flip()
        core.wait(5)
        event.clearEvents()
        startT = myClock.getTime()
        fixStart = fixation_screen(myClock, np.arange(0.5,1,0.05)[randint(0,10)]) #final fixation cross before Thank You message  
            
    
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
    
    
    
    
    
    
    
