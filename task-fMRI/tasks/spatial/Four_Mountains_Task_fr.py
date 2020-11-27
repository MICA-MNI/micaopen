expName = 'Four Mountains Task' 
#collect participant info, create logfile
pptInfo = {
    'subject': '', 
    'session': '001', 
    } #a pop up window will show up to collect these information

from psychopy import core
from baseDef import*

setDir()
expInfo, datafn = info_gui(expName, pptInfo)
from FourMountains_TrialDisplay_fr import*

instruction(inst_txt='FourMountains_Instructions/exp_instr_fr.txt')
myClock = core.Clock()
f = open_datalog(datafn, dataformat='.csv', headers='expimages,testimages,CorrAns,resp,resp_RT,resp_corr,rating,rating_RT,IDNO,session\n')
myClock = core.Clock()
task(myClock, expInfo, f)
endExp(f)


from psychopy import visual, core, event
from numpy.random import randint, shuffle
import numpy as np
from baseDef import*

sans = ['Arial','Gill Sans MT', 'Helvetica','Verdana'] #use the first font found on this list
win = set_window(fullscr=True, gui=True, color=1)

msgTxt = visual.TextStim(win,text='default text', font= sans, name='message',
    height=30, wrapWidth=1100,
    color='black', 
    )

########################################################################################
instrTxt = visual.TextStim(win,text='default text', font= sans, name='instruction',
    pos=[-50,0], height=30, wrapWidth=1100,
    color='black',
    ) #object to display instructions

def instruction(inst_txt='FourMountains_Instructions/exp_instr_fr.txt'):
    Instruction = open(inst_txt, 'r').read().split('#\n')
    Ready = open('Instructions/wait_trigger_fr.txt', 'r').read()
    #instructions screen 
    for i, cur in enumerate(Instruction):
        instrTxt.setText(cur)
        instrTxt.draw()
        win.flip()
        if i==0:
            core.wait(np.arange(1.3,1.75,0.05)[randint(0,9)])
        else:
            event.waitKeys(keyList=['space'])

        if event.getKeys(keyList = ['escape']):
            quitEXP(True)

    instrTxt.setText(Ready)
    instrTxt.draw()
    win.flip()
    if event.getKeys(keyList = ['escape']):
        quitEXP(True)
    #need to update a scanner trigger version
    core.wait(np.arange(1.3,1.75,0.05)[randint(0,9)])
############################################################################################  

fixation = visual.TextStim(win, name='fixation', text='+', 
                            font= sans, height=62, pos=(0,0),color='black')#set pix pos

def fixation_screen(myClock, waittime=1):
    fixation.draw()
    win.logOnFlip(level=logging.EXP, msg='fixation cross on screen') #new log haoting
    win.flip()
    fixStart = myClock.getTime() #fixation cross onset
    if event.getKeys(keyList = ['escape']):
        quitEXP(True)
    core.wait(waittime)
    return fixStart
######################################################################################
im = visual.ImageStim(win, name='stimPic', image = None, size = (960, 720), )

def show_meta():
    meta_description = open('FourMountains_Instructions/meta_instr_fr.txt', 'r').read()
    msgTxt.setText(meta_description)
    msgTxt.draw()
    win.flip()
def reset_output():
    keyResp = None
    thisRT = np.nan
    respRT = np.nan
    corr = np.nan
    return keyResp, thisRT, respRT, corr

def getMeta(startT, myClock):
    keyResp, thisRT, respRT, corr= reset_output()
    while keyResp==None:
        show_meta()
        keyResp, thisRT = get_keyboard(myClock,win, respkeylist=['1', '2'])
        if not np.isnan(thisRT):
            respRT = (thisRT - startT)
        else:
            pass
    keyResp = -(int(keyResp) - 2)
    return keyResp, respRT

def show_questions(thisTrial):
    im.setImage(thisTrial['testimages'])
    im.draw()
    win.flip()

def getResp(startT, myClock, thisTrial):
    keyResp, thisRT, respRT, corr = reset_output()
    while keyResp==None:
        show_questions(thisTrial)
        keyResp, thisRT = get_keyboard(myClock,win, respkeylist=['1', '2', '3', '4'])
        if not np.isnan(thisRT):
            respRT = thisRT - startT
            if keyResp == thisTrial['CorrAns']:
                corr = 1
            else:
                corr = 0
        else:
            pass
    return int(keyResp), respRT, corr

def Confidence_screen(myClock, thisTrial):
    show_meta()
    win.logOnFlip(level=logging.EXP, msg='Confidence Quesion on screen') #new log haoting
    startT = myClock.getTime()
    keyResp, respRT = getMeta(startT, myClock)
    if event.getKeys(keyList = ['escape']):
        quitEXP(True)
    return keyResp, respRT

def ans_screen(myClock, thisTrial):
    show_questions(thisTrial)
    win.logOnFlip(level=logging.EXP, msg='select answer') #new log haoting
    startT = myClock.getTime()
    keyResp, respRT, corr = getResp(startT, myClock, thisTrial)
    if event.getKeys(keyList = ['escape']):
        quitEXP(True)
    return keyResp, respRT, corr

def saveResp(f, thisTrial, expInfo, ans, rate):
    write_datalog(f, data='%s,%s,%s,%i,%f,%i,%i,%f,%s,%s\n'
        %(thisTrial['expimages'], thisTrial['testimages'], thisTrial['CorrAns'],
            ans[0], ans[1], ans[2], rate[0], rate[1],
            expInfo['subject'],expInfo['session']))
####################################################################################################################
def task(myClock, expInfo, f):
    stimuli_list = load_conditions_dict(csvFile='stimuli/4MTconditions.csv')
    for thisTrial in stimuli_list:
        fixStart = fixation_screen(myClock, np.arange(1.3,1.75,0.05)[randint(0,9)])
        im.setImage(thisTrial['expimages'])
        im.draw()
        win.flip()
        #core.wait(10)
        event.clearEvents()
        startT = myClock.getTime()
        show_questions(thisTrial)
        ans = ans_screen(myClock, thisTrial)
        fixStart = fixation_screen(myClock, np.arange(0.5,1,0.05)[randint(0,10)])
        rate = Confidence_screen(myClock, thisTrial)
        saveResp(f, thisTrial, expInfo, ans, rate)

def endExp(f):
    endtxt = open('FourMountains_Instructions/end_instr_fr.txt', 'r').read().split('#\n')[0]
    msgTxt.setText(endtxt)
    msgTxt.draw()
    win.flip()
    event.waitKeys(maxWait = 20)
    logging.flush()
    f.close()
    win.close()
    core.quit()
