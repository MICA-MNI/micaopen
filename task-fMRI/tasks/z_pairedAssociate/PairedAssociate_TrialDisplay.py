from psychopy import visual, core, event
from numpy.random import randint, shuffle
import numpy as np
from baseDef import*
import os

sans = ['Arial','Gill Sans MT', 'Helvetica','Verdana'] #use the first font found on this list
textSizeExp = 50
win = set_window(fullscr=True, gui=True, color=[0.700,0.700,0.700])

msgTxt = visual.TextStim(win,text='default text', font= sans, name='message',
    height=62, wrapWidth=900,
    color='black', 
    )

def PairedAssociate_Stimuli_All(expInfo):
    get_all_list = open('Stimuli' + os.sep + 'learninglist_all_List' + expInfo['wordlist'] + '.txt', 'r').read().split('\n')
    stimuli_list_all = []
    for p in get_all_list:
        p_temp = tuple(p.split('-'))
        stimuli_list_all.append(p_temp)
    
    from numpy.random import shuffle
    shuffle(stimuli_list_all)
    return stimuli_list_all

def PairedAssociate_Stimuli_Weak(expInfo):
    get_weak_list = open('Stimuli' + os.sep + 'learninglist_weak_List' + expInfo['wordlist'] + '.txt', 'r').read().split('\n')
    stimuli_list_weak = []
    for p in get_weak_list:
        p_temp = tuple(p.split('-'))
        stimuli_list_weak.append(p_temp)

    from numpy.random import shuffle
    shuffle(stimuli_list_weak)
    return stimuli_list_weak

def PairedAssociate_Stimuli_Strong(expInfo):
    get_strong_list = open('Stimuli' + os.sep + 'learninglist_strong_List' + expInfo['wordlist'] + '.txt', 'r').read().split('\n')
    stimuli_list_strong = []
    for p in get_strong_list:
        p_temp = tuple(p.split('-'))
        stimuli_list_strong.append(p_temp)
    
    from numpy.random import shuffle
    shuffle(stimuli_list_strong)
    return stimuli_list_strong

######################################################################################
#Delay only
question = visual.TextStim(win, name='Question',
   text='On a scale of 1-7, how confident you are about your answer?', font= sans,
   pos=(0,250), height=60, wrapWidth=1300,
   color='black')
#not using the rating scale module
descr = visual.TextStim(win, name='Descriptions',
   text='Not at all                            Completely', font= sans,
   pos=[0, -60], height=50, wrapWidth=1300,
   color='black')
scale = visual.TextStim(win, name='RatingScale',
   text='1      2       3       4       5       6       7', font= sans,
   pos=[0, -120], height=45, wrapWidth=1300,
   color='black', )

def reset_output():
    keyResp = None
    thisRT = np.nan
    respRT = np.nan
    return keyResp, thisRT, respRT

def getResp(startT, myClock):
    keyResp, thisRT, respRT = reset_output()
    while keyResp==None:
        show_questions()
        keyResp, thisRT = get_keyboard(myClock,win, respkeylist=['1', '2', '3', '4', '5', '6', '7'])
        if not np.isnan(thisRT):
            respRT = (thisRT - startT) * 1000
        else:
            pass
    return keyResp, respRT

def show_questions():
    question.draw()
    descr.draw()
    scale.draw()
    win.flip()

def Confidence_screen(myClock, thisTrial):
    show_questions()
    win.logOnFlip(level=logging.EXP, msg='Confidence Quesion on screen') #new log haoting
    startT = myClock.getTime()
    keyResp, respRT = getResp(startT, myClock)
    if event.getKeys(keyList = ['escape']):
        quitEXP(True)
    return keyResp, respRT

########################################################################################

instrTxt = visual.TextStim(win,text='default text', font= sans, name='instruction',
    pos=[-50,0], height=30, wrapWidth=900,
    color='black',
    ) #object to display instructions

def instruction(inst_txt='Instructions' + os.sep + 'exp_encode_instr.txt'):
    Instruction = open(inst_txt, 'r').read().split('#\n')
    Ready = open('Instructions' + os.sep + 'wait_trigger.txt', 'r').read()
    #instructions screen 
    for i, cur in enumerate(Instruction):
        instrTxt.setText(cur)
        instrTxt.draw()
        instructionsclock = core.Clock()
        win.flip()
        if i==0:
            while instructionsclock.getTime() < 20:
                if event.getKeys(['1','2','3','4']):
                    break
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

fixation = visual.TextStim(win, name='fixation', text='+', height=textSizeExp, pos=(0,0),color='black')#set pix pos

#fixation = visual.TextStim(win, name='fixation', text='+', 
#                            font= sans, height=textSizeExp, pos=(0,0),color='black')#set pix pos

def fixation_screen(myClock, waittime=1):
    fixation.draw()
    win.logOnFlip(level=logging.EXP, msg='fixation cross on screen') #new log haoting
    win.flip()
    fixStart = myClock.getTime() #fixation cross onset
    if event.getKeys(keyList = ['escape']):
        quitEXP(True)
    core.wait(waittime)
    return fixStart

# Show all the pairs
##############################################################################################

encodeleft  = visual.TextStim(win, name='encodeleft' , text='+', height=textSizeExp, pos=(-textSizeExp*.5,0),color='black',wrapWidth=1000, alignHoriz='right' )#set pix pos
encoderight = visual.TextStim(win, name='encoderight', text='+', height=textSizeExp, pos=(textSizeExp*.5,0) ,color='black',wrapWidth=1000, alignHoriz='left'  )#set pix pos
encodedash  = visual.TextStim(win, name='encodedash' , text='-', height=textSizeExp, pos=(0,0)              ,color='black',wrapWidth=1000, alignHoriz='center')#set pix pos
#encodepair = visual.TextStim(win,text='default text', font= sans, name='Encoding word pair', 
#    height=textSizeExp, color='black')

def encoding(myClock, stimuli_list_all):
    # wait for scanner
    message1 = visual.TextStim(win, pos=[0,+100], color='#000000', alignHoriz='center', name='topMsg', text="Waiting for scanner to start...")
    message1.draw()
    win.logOnFlip(level=logging.EXP, msg='Display WaitingForScanner')
    win.flip()
    keyPress = event.waitKeys(keyList=['5','q','escape'])
    if keyPress[0] in ['q','escape']:
        win.close()
        core.quit()
    # Do the scans.
    for this in stimuli_list_all:
#        cur_encode = ' - '.join(this)
        # Draw strings.
        fixation_screen(myClock, waittime=1)
        encodeleft.setText(this[0])
        encodeleft.draw()
        encoderight.setText(this[1])
        encoderight.draw()
        encodedash.draw()
#        encodepair.setText(cur_encode)
#        encodepair.draw()
        win.flip()
        core.wait(5)

# The Weak Trials
##############################################################################################################

Target = visual.TextStim(win, name='target on screen', height=textSizeExp, pos=(-300,250), wrapWidth=1000, alignHoriz='left',
                        text='test', font=sans, color='black')

def updateTheResponse(captured_string):
    Target.setText(captured_string)
    Target.draw()
    win.flip()

FeedBack = visual.TextStim(win, name='feedback on screen', height=textSizeExp, pos=(-300,250),
                            text='feedback',
                            font=sans, color='red')
TheAnsIs = visual.TextStim(win,text='The correct answer is', font= sans, name='feedback: correct ans',
                            height=42, pos=(0,100), wrapWidth=1100,
                            color='black',)
ShowCorrAns = visual.TextStim(win, name='show correct ans', height=textSizeExp, pos=(0,-0),
                            text='feedback',
                            font=sans, color='blue')

def feedback(CORR, captured_string, thisTrial):
    if CORR ==1:
        FeedBack.setText('Correct!')
        FeedBack.draw()
        win.flip()
    elif CORR ==0 and len(captured_string)==0:
        FeedBack.setText('No response detected.')
        ShowCorrAns.setText(thisTrial[1])
        TheAnsIs.draw()
        FeedBack.draw()
        ShowCorrAns.draw()
        win.flip()
    else:
        FeedBack.setText('Wrong!')
        ShowCorrAns.setText(thisTrial[1])
        TheAnsIs.draw()
        FeedBack.draw()
        ShowCorrAns.draw()
        win.flip()
    core.wait(3)

def ans_screen(myClock, thisTrial, condition, question_length=10):
    fixation_screen(myClock, waittime=1.5)
    event.clearEvents()
    captured_string = ''
    startT = myClock.getTime()
    updateTheResponse(thisTrial[0] + ' - ' + captured_string)
    thisRT = 0
    respRT = 0
    CORR = 0
    CaptureResp = True
    while CaptureResp and myClock.getTime() - startT <= question_length:
        for key in event.getKeys():
            if key == 'return':
                CaptureResp = False
                break
            elif key == 'backspace':
                captured_string = captured_string[:-1]
                updateTheResponse(thisTrial[0] + ' - ' + captured_string)
            elif key == 'escape':
                quitEXP(True)
            elif key in ['lshift','rshift', 'bracketleft', 'bracketright']:
                pass #do nothing when some keys are pressed
            else:
                captured_string += key
                updateTheResponse(thisTrial[0] + ' - ' + captured_string)
    thisRT = myClock.getTime()
    respRT = (thisRT-startT) * 1000
    if captured_string == thisTrial[1]:
        CORR = 1
    else:
        CORR = 0
    updateTheResponse(captured_string)
    resp  = captured_string

    if condition == 'encoding':
        feedback(CORR, captured_string, thisTrial)
        return resp, CORR, respRT

    else:
        ratingKey, ratingRT = Confidence_screen(myClock, thisTrial)
        return resp, CORR, respRT, ratingKey, ratingRT

def block_end(countCORR, attempts):
    showmessage = 'Your accuracy rate is %f'%(countCORR) + '%' + '\n\n\nPress SPACE to continue.'
    msgTxt.setText(showmessage)
    msgTxt.draw()
    win.flip()
    event.waitKeys(keyList=['space'])

def recall_weak(myClock, stimuli_list_weak, expInfo, f):
    fixation.pos = (-300,250)
    continueTest = True
    attempt = 0
    acc = 0

    if expInfo['conditions'] == 'encoding':
        def saveResp(f, attempt, i, thisTrial, expInfo, resp):
            write_datalog(f, data='%i,%i,%s,%s,%s,%i,%f,%s,%s\n'
                %(attempt, i, thisTrial[0], thisTrial[1], 
                    resp[0], resp[1], resp[2],
                    expInfo['subject'],expInfo['session']))
            event.clearEvents()
    else:
        def saveResp(f, attempt, i, thisTrial, expInfo, resp):
            write_datalog(f, data='%i,%i,%s,%s,%s,%i,%f,%s,%f,%s,%s\n'
                %(attempt, i, thisTrial[0], thisTrial[1], 
                    resp[0], resp[1], resp[2], resp[3], resp[4],
                    expInfo['subject'],expInfo['session']))
            event.clearEvents()
    attempts = 1
    while continueTest:
        countCORR = []
        acc = 0
        attempt +=1
        shuffle(stimuli_list_weak)
        for i, thisTrial in enumerate(stimuli_list_weak):
            if i==21:
                msgTxt.setText('You are half way through this task, if you wish you may take a short break.\n\nPess SPACE to continue.')
                msgTxt.draw()
                win.flip()
                event.waitKeys(keyList=['space'])
                resp = ans_screen(myClock, thisTrial, expInfo['conditions'], question_length=12)
            else:
                resp = ans_screen(myClock, thisTrial, expInfo['conditions'], question_length=12)
            countCORR.append(resp[1])
            saveResp(f, attempt, i, thisTrial, expInfo, resp)

        acc =  float(sum(countCORR)) / float(len(countCORR)) * 100

        write_datalog(f, data='%i,%s,%s,%s,%s,%i\n'
            %(attempt, 'accuracy', '', '', '', acc))
        if  attempt == 1:
            block_end(acc, attempts)
            continueTest = False
        elif expInfo['conditions'] == 'delayed':
            continueTest = False
        else:
            attempts -= 1
            block_end(acc, attempts)
            continueTest = True

# The Strong Trials
##############################################################################################################

Target = visual.TextStim(win, name='target on screen', height=textSizeExp, pos=(-300,250), wrapWidth=1000, alignHoriz='left',
                         text='test', font=sans, color='black')

def updateTheResponse(captured_string):
    Target.setText(captured_string)
    Target.draw()
    win.flip()

FeedBack = visual.TextStim(win, name='feedback on screen', height=textSizeExp, pos=(-300,250),
                           text='feedback',
                           font=sans, color='red')
TheAnsIs = visual.TextStim(win,text='The correct answer is', font= sans, name='feedback: correct ans',
                           height=textSizeExp, pos=(0,100), wrapWidth=1100,
                           color='black',)
ShowCorrAns = visual.TextStim(win, name='show correct ans', height=textSizeExp, pos=(0,-0),
                           text='feedback',
                           font=sans, color='blue')

def feedback(CORR, captured_string, thisTrial):
    if CORR ==1:
        FeedBack.setText('Correct!')
        FeedBack.draw()
        win.flip()
    elif CORR ==0 and len(captured_string)==0:
        FeedBack.setText('No response detected.')
        ShowCorrAns.setText(thisTrial[1])
        TheAnsIs.draw()
        FeedBack.draw()
        ShowCorrAns.draw()
        win.flip()
    else:
        FeedBack.setText('Wrong!')
        ShowCorrAns.setText(thisTrial[1])
        TheAnsIs.draw()
        FeedBack.draw()
        ShowCorrAns.draw()
        win.flip()
    core.wait(3)

def ans_screen(myClock, thisTrial, condition, question_length=10):
    fixation_screen(myClock, waittime=1.5)
    event.clearEvents()
    captured_string = ''
    startT = myClock.getTime()
    updateTheResponse(thisTrial[0] + ' - ' + captured_string)
    thisRT = 0
    respRT = 0
    CORR = 0
    CaptureResp = True
    while CaptureResp and myClock.getTime() - startT <= question_length:
        for key in event.getKeys():
            if key == 'return':
                CaptureResp = False
                break
            elif key == 'backspace':
                captured_string = captured_string[:-1]
                updateTheResponse(thisTrial[0] + ' - ' + captured_string)
            elif key == 'escape':
                quitEXP(True)
            elif key in ['lshift','rshift', 'bracketleft', 'bracketright']:
                pass #do nothing when some keys are pressed
            else:
                captured_string += key
                updateTheResponse(thisTrial[0] + ' - ' + captured_string)
    thisRT = myClock.getTime()
    respRT = (thisRT-startT) * 1000
    if captured_string == thisTrial[1]:
        CORR = 1
    else:
        CORR = 0
    updateTheResponse(captured_string)
    resp  = captured_string

    if condition == 'encoding':
        feedback(CORR, captured_string, thisTrial)
        return resp, CORR, respRT

    else:
        ratingKey, ratingRT = Confidence_screen(myClock, thisTrial)
        return resp, CORR, respRT, ratingKey, ratingRT

def block_end(countCORR, attempts):
    showmessage = 'Your accuracy rate is %f'%(countCORR) + '%' + '. Well done!' + '\n\n\nPess SPACE to continue.'
    msgTxt.setText(showmessage)
    msgTxt.draw()
    win.flip()
    event.waitKeys(keyList=['space'])

def recall_strong(myClock, stimuli_list_strong, expInfo, f):
    fixation.pos = (-300,250)
    continueTest = True
    attempt = 0
    acc = 0
    
    if expInfo['conditions'] == 'encoding':
        def saveResp(f, attempt, i, thisTrial, expInfo, resp):
            write_datalog(f, data='%i,%i,%s,%s,%s,%i,%f,%s,%s\n'
                          %(attempt, i, thisTrial[0], thisTrial[1],
                            resp[0], resp[1], resp[2],
                            expInfo['subject'],expInfo['session']))
            event.clearEvents()
    else:
        def saveResp(f, attempt, i, thisTrial, expInfo, resp):
            write_datalog(f, data='%i,%i,%s,%s,%s,%i,%f,%s,%f,%s,%s\n'
                          %(attempt, i, thisTrial[0], thisTrial[1],
                            resp[0], resp[1], resp[2], resp[3], resp[4],
                            expInfo['subject'],expInfo['session']))
            event.clearEvents()
    attempts = 3
    while continueTest:
        countCORR = []
        acc = 0
        attempt +=1
        shuffle(stimuli_list_strong)
        for i, thisTrial in enumerate(stimuli_list_strong):
            if i==21:
                msgTxt.setText('You are half way through this task, if you wish you may take a short break.\n\nPess SPACE to continue.')
                msgTxt.draw()
                win.flip()
                event.waitKeys(keyList=['space'])
                resp = ans_screen(myClock, thisTrial, expInfo['conditions'], question_length=12)
            else:
                resp = ans_screen(myClock, thisTrial, expInfo['conditions'], question_length=12)
            countCORR.append(resp[1])
            saveResp(f, attempt, i, thisTrial, expInfo, resp)
        
        acc =  float(sum(countCORR)) / float(len(countCORR)) * 100
        
        write_datalog(f, data='%i,%s,%s,%s,%s,%i\n'
            %(attempt, 'accuracy', '', '', '', acc))
        if attempt == 3:
            block_end(acc, attempts)
            continueTest = False
        elif expInfo['conditions'] == 'delayed':
            continueTest = False
        else:
            attempts -= 1
            block_end(acc, attempts)
            continueTest = True

#############################################################################################################

def endExp(f):
    endtxt = open('Instructions' + os.sep + 'end_instr.txt', 'r').read().split('#\n')[0]
    msgTxt.setText(endtxt)
    msgTxt.draw()
    win.flip()
    event.waitKeys(maxWait = 20)
    logging.flush()
    f.close()
    win.close()
    core.quit()
