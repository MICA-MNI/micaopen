# dependency housekeeping
import csv
import PIL
import glob
import random
import datetime
import warnings
import numpy as np
from pyglet.window import key, Window
from numpy.random import randint, shuffle
from psychopy import core, data, event, logging, os, sys, visual
from pdb import set_trace as bp
warnings.filterwarnings(action='ignore')

# run paradigm
def execute():
        
    # get GUI-generated info from tmp.txt file
    with open('tmp.txt') as f:
        inFile = f.readlines()
    
    # general info
    expInfo = {'ID': inFile[0][10:-1],
               'session': inFile[1][10:-1],
               'language': inFile[2][10:-1],
               'protocol': inFile[3][10:-1],
               'list': 'A',
               'date': data.getDateStr(),
               'Block1': inFile[4][8:-1],
               'Block2': inFile[5][8:-1],
               'Block3': inFile[6][8:-1],
               'Block4': inFile[7][8:-1],
               'Block5': inFile[8][8:-1],
               'Block6': inFile[9][8:-1],
               'Block7': inFile[10][8:-1],
               'Block8': inFile[11][8:]}

    # delete tmp.txt file
    os.remove('tmp.txt')

    # define scanner trigger function
    def Trigger(clock):
        Txt.setText('waiting for scanner...')
        Txt.draw()
        win.flip()    
        event.waitKeys(keyList=['5'])
        clock.reset()
    
    ####################################### 1st English protocol ##############################################
    ###########################################################################################################
    if expInfo['language'] == 'English' and expInfo['protocol'] == 'I':
        print('\n\n\n\n-------------------------------------------------------------------------')
        print('ID:           ' + expInfo['ID'])
        print('Session:      ' + expInfo['session']) 
        print('Language:     ' + expInfo['language'])
        print('Protocol:     ' + expInfo['protocol'])
        print('Block 1:      encoding & experience sampling 1                      ' + expInfo['Block1'])
        print('Block 2:      quantitative T1-mapping                               ' + expInfo['Block2'])
        print('Block 3:      retrieval & experience sampling 2                     ' + expInfo['Block3'])
        print('Block 4:      T2*-weighted imaging                                  ' + expInfo['Block4'])
        print('Block 5:      mnemonic similarity task 1 & experience sampling 3    ' + expInfo['Block5'])
        print('Block 6:      diffusion-weighted imaging                            ' + expInfo['Block6'])
        print('Block 7:      mnemonic similarity task 2 & experience sampling 4    ' + expInfo['Block7'])
        print('Block 8:      resting state & experience sampling 5                 ' + expInfo['Block8'])
        print('-------------------------------------------------------------------------')
        
        # import stimuli for each block
        trialList_enc = data.importConditions('episodic/Encoding/enc_List' + expInfo['list'] + '.csv') 
        trialList_ES = data.importConditions('exp_sampling/ES_trials.csv')
        trialList_ret = data.importConditions('episodic/Retrieval/ret_List' + expInfo['list'] + '.csv')
        trialList_mst1 = data.importConditions('MST/MST1/MST1_List' + expInfo['list'] + '.csv')
        trialList_mst2 = data.importConditions('MST/MST2/MST2_List' + expInfo['list'] + '.csv')
        
        # create list of variable fixation cross durations for each block
        n_trial_enc = len(trialList_enc)
        fix_increment_enc = 1 / (n_trial_enc - 1)
        range_trial_enc = range(0, n_trial_enc)
        fix_dur_enc = [2 + (x * fix_increment_enc) for x in range_trial_enc]
        
        n_trial_ES = len(trialList_ES)
        fix_increment_ES = 1 / (n_trial_ES - 1)
        range_trial_ES = range(0, n_trial_ES)
        fix_dur_ES = [2 + (x * fix_increment_ES) for x in range_trial_ES]
        
        n_trial_ret = len(trialList_ret)
        fix_increment_ret = 1 / (n_trial_ret - 1)
        range_trial_ret = range(0, n_trial_ret)
        fix_dur_ret = [4 + (x * fix_increment_ret) for x in range_trial_ret]
        
        n_trial_mst1 = len(trialList_mst1)
        fix_increment_mst1 = 1 / (n_trial_mst1 - 1)
        range_trial_mst1 = range(0, n_trial_mst1)
        fix_dur_mst1 = [2.75 + (x * fix_increment_mst1) for x in range_trial_mst1]
        
        n_trial_mst2 = len(trialList_mst2)
        fix_increment_mst2 = 1 / (n_trial_mst2 - 1)
        range_trial_mst2 = range(0, n_trial_mst2)
        fix_dur_mst2 = [.65 + (x * fix_increment_mst2) for x in range_trial_mst2]
        
        # create subject-specific directory to keep logs
        rootLog = 'logs/sub-' + expInfo['ID'] + '/ses-' + expInfo['session'] + '/beh'
        
        if not os.path.isdir(rootLog):
            os.makedirs(rootLog)

        # define functions for each block
        def FixationCross(clock, fix_dur, trialNum):
            fixation.draw()
            win.logOnFlip(level=logging.EXP, msg='fixation cross')
            win.flip()
            fixation_onset = clock.getTime()
            core.wait(fix_dur[trialNum])
            if event.getKeys(keyList=['escape']):
                core.quit()
            event.clearEvents()
            return fixation_onset
        
        def StimPairs(clock):
            im1.setImage(IMAGE1)
            im2.setImage(IMAGE2)
            im1.draw()
            im2.draw()
            win.logOnFlip(level=logging.EXP, msg='stimulus pair')
            win.flip()
            stim_pair_onset = clock.getTime()
            core.wait(2)
            event.clearEvents()
            return stim_pair_onset
        
        def MindProbe(clock, idx):
            flag = 1
            inc = 0.1
            pos = rating_scale.markerStart
            keyState=key.KeyStateHandler()
            win.winHandle.push_handlers(keyState)
            while rating_scale.noResponse:
                if keyState[key._2]:
                    pos -= inc
                elif keyState[key._4]:
                    pos += inc
                if pos > 9.9:
                    pos = 10
                elif pos < 0.1:
                    pos = 0
                probe.setText(trialList_ES[idx]['question'])
                probe.draw()
                rating_scale.setMarkerPos(pos)
                rating_scale.draw()
                win.logOnFlip(level=logging.EXP, msg='experience sampling probe')
                win.flip()
                if flag == 1:
                    probe_onset = clock.getTime()
                    flag = 0
            return probe_onset

        def ProbePrint(trialNum, Dim, Quest, SR):
            n_letters = len('intrusiveness')
            n_chars = len('My thoughts were focused on an external task or activity.')
            empty = ' '
            SR = '{:.1f}'.format(SR)
            if n_letters != len(Dim):
                Space1 = n_letters - len(Dim) - 1
            if n_chars != len(Quest):
                Space2 = n_chars - len(Quest) - 1
            if trialNum <= 9:
                if Dim == 'intrusiveness':
                    print('trial', trial_num, ' |', dimension, '|', question, Space2*empty, '|',
		          confirmation_status, SR, '(0-10)')
                elif Dim == 'focus':
                    print('trial', trial_num, ' |', dimension, Space1*empty,'|', question, '|',
		          confirmation_status, SR, '(0-10)')
                else:    
                    print('trial', trial_num, ' |', dimension, Space1*empty, '|', question, Space2*empty, '|',
		          confirmation_status, SR, '(0-10)')                                
            else:
                if Dim == 'intrusiveness':
                    print('trial', trial_num, '|', dimension, '|', question, Space2*empty, '|',
		          confirmation_status, SR, '(0-10)')
                elif Dim == 'focus':
                    print('trial', trial_num, '|', dimension, Space1*empty,'|', question, '|',
		          confirmation_status, SR, '(0-10)')
                else:
                    print('trial', trial_num, '|', dimension, Space1*empty, '|', question, Space2*empty, '|',
		          confirmation_status, SR, '(0-10)')
           
        def RetrievalScreen(clock, prime_pos, target_pos, foil1_pos, foil2_pos): 
            prime_im = visual.ImageStim(win, name='stimPic1', image = None, pos=prime_pos)
            tg_im = visual.ImageStim(win, name='stimPic2', image = None, pos=target_pos)
            foil1_im = visual.ImageStim(win, name='stimPic3', image = None, pos=foil1_pos)
            foil2_im = visual.ImageStim(win, name='stimPic4', image = None, pos=foil2_pos)
            prime_im.setImage(Prime)
            tg_im.setImage(Target)
            foil1_im.setImage(Foil1)
            foil2_im.setImage(Foil2)
            prime_im.draw()
            tg_im.draw()
            foil1_im.draw()
            foil2_im.draw()
            win.logOnFlip(level=logging.EXP, msg='retrieval screen')
            win.flip()
            RetrievalScreen_onset = clock.getTime()
            return RetrievalScreen_onset
        
        def RetrievalResponse(clock, trialEndTime, stimStart):
            flag = 0
            keyList = []
            keypress = []
            while clock.getTime() < trialEndTime:
                keypress = event.getKeys(keyList=['2','3','4'])
                if len(keypress) == 1 and flag == 0:
                    keyList = keypress[0]
                    flag = 1
                    keyStart = clock.getTime()
            if len(keyList) == 1 and flag == 1:    
                    key_pressed = keyList[0]
                    RT = keyStart - stimStart
            else:
                keyStart = '--'
                key_pressed = 'N/A'
                RT = 'N/A'
            event.clearEvents()
            return keyStart, key_pressed, RT
        
        def RetrievalInfo(RT, y_val, target_pos, foil1_pos, foil2_pos, target_name, foil1_name, foil2_name):
            if RT == 'N/A':
                im_position = 'N/A'
                key_ID = 'N/A'
                subChoice = 'N/A'
                accuracy = 0
            elif RT < 2.5:
                if key_pressed == '2':
                    im_position = (-.5, y_val)
                    key_ID = 'left'
                elif key_pressed == '3':
                    im_position = (0, y_val)
                    key_ID = 'center'
                elif key_pressed == '4':
                    im_position = (.5, y_val)
                    key_ID = 'right'
            if im_position == target_pos:
                subChoice = target_name[:-4]
                accuracy = 1
            elif im_position == foil1_pos:
                subChoice = foil1_name[:-4]
                accuracy = 0
            elif im_position == foil2_pos:
                subChoice = foil2_name[:-4]
                accuracy = 0
            if target_pos == (-.5, y_val) and foil1_pos == (0, y_val) and foil2_pos == (.5, y_val):
                left_choice = target_name[:-4]
                center_choice = foil1_name[:-4]
                right_choice = foil2_name[:-4]
            elif target_pos == (-.5, y_val) and foil2_pos == (0, y_val) and foil1_pos == (.5, y_val):
                left_choice = target_name[:-4]
                center_choice = foil2_name[:-4]
                right_choice = foil1_name[:-4]
            elif foil1_pos == (-.5, y_val) and target_pos == (0, y_val) and foil2_pos == (.5, y_val):
                left_choice = foil1_name[:-4]
                center_choice = target_name[:-4]
                right_choice = foil2_name[:-4]
            elif foil1_pos == (-.5, y_val) and foil2_pos == (0, y_val) and target_pos == (.5, y_val):
                left_choice = foil1_name[:-4]
                center_choice = foil2_name[:-4]
                right_choice = target_name[:-4]
            elif foil2_pos == (-.5, y_val) and target_pos == (0, y_val) and foil1_pos == (.5, y_val):
                left_choice = foil2_name[:-4]
                center_choice = target_name[:-4]
                right_choice = foil1_name[:-4]
            elif foil2_pos == (-.5, y_val) and foil1_pos == (0, y_val) and target_pos == (.5, y_val):
                left_choice = foil2_name[:-4]
                center_choice = foil1_name[:-4]
                right_choice = target_name[:-4]
            return key_ID, subChoice, left_choice, center_choice, right_choice, accuracy
        
        def MSTScreen(clock):
            im.setImage(IMAGE)
            im.draw()
            MSTtext.draw()
            win.logOnFlip(level=logging.EXP, msg='stimulus')
            win.flip()
            MSTScreen_onset = clock.getTime()
            event.clearEvents()
            return MSTScreen_onset
        
        def MST1Response(clock, trialEndTime, stimStart):
            flag = 0
            keyList = []
            keypress = []
            while clock.getTime() < trialEndTime:
                keypress = event.getKeys(keyList=['2','4'])
                if len(keypress) == 1 and flag == 0:
                    keyList = keypress[0]
                    flag = 1
                    keyStart = clock.getTime()
            if len(keyList) == 1 and flag == 1:    
                    key_pressed = keyList[0]
                    RT = keyStart - stimStart
            else:
                keyStart = '--'
                key_pressed = 'N/A'
                RT = 'N/A'
            if RT == 'N/A':
                SR = 'N/A'
            elif RT < 2:
                if key_pressed == '2':
                    SR = 'indoors'
                elif key_pressed == '4':
                    SR = 'outdoors'        
            event.clearEvents()
            return keyStart, SR, RT
        
        def MST2Response(clock, trialEndTime, stimStart):
            flag = 0
            keyList = []
            keypress = []
            while clock.getTime() < trialEndTime:
                keypress = event.getKeys(keyList=['2','3','4'])
                if len(keypress) == 1 and flag == 0:
                    keyList = keypress[0]
                    flag = 1
                    keyStart = clock.getTime()
            if len(keyList) == 1 and flag == 1:    
                    key_pressed = keyList[0]
                    RT = keyStart - stimStart
            else:
                keyStart = '--'
                key_pressed = 'N/A'
                RT = 'N/A'
            if RT == 'N/A':
                SR = 'N/A'
            elif RT < 2.5:
                if key_pressed == '2':
                    SR = 'old'
                elif key_pressed == '3':
                    SR = 'similar'
                elif key_pressed == '4':
                    SR = 'new'        
            event.clearEvents()
            return keyStart, SR, RT
        
        # define inter-block flags
        encoding = ES1 = eval(expInfo['Block1'])
        qT1 = eval(expInfo['Block2'])
        retrieval = ES2 = eval(expInfo['Block3'])
        T2star = eval(expInfo['Block4'])
        MST1 = ES3 = eval(expInfo['Block5'])
        DWI = eval(expInfo['Block6'])
        MST2 = ES4 = eval(expInfo['Block7'])
        RS = ES5 = eval(expInfo['Block8'])

        # set up main clock & logging features
        mainClock = core.Clock()
        logging.setDefaultClock(mainClock)
        logging.console.setLevel(logging.WARNING)
        
        log_filename = rootLog + '/sub-' +  expInfo['ID'] + '_ses-' + expInfo['session'] + '_' + expInfo['date']
        logFile = logging.LogFile(log_filename + '.log', level=logging.EXP)

        # display window
        win = visual.Window(size=(933.33, 700), color=1, units='height')
        win.mouseVisible = False
        
        # text and fixation features
        sans = ['Arial', 'Gill Sans MT', 'Helvetica', 'Verdana']
        Txt = visual.TextStim(win, name='instruction', text='default text', font=sans, pos=(0, 0),
                              height=float(.04), wrapWidth=1100, color='black')
        fixation = visual.TextStim(win, name='fixation', text='+', font=sans, pos=(0, 0), height=float(.08),
                                   color='black')

        ################################### Block 1: Encoding  ################################################
        
        # create .csv log file for encoding
        if encoding:
            task_lab = '_encoding'
            prevRuns = glob.glob(rootLog + '/*' + task_lab + '*')
            if prevRuns:
                prevRuns.sort()
                numRun = len(prevRuns)
                newRun = str('{:02d}'.format(int(prevRuns[numRun-1][-6:-4]) + 1))
                enc_csvFile = prevRuns[numRun-1][:-6] + newRun + '.csv'
            else:
                enc_csvFile = rootLog + '/sub-' + expInfo['ID'] + '_ses-' + expInfo['session'] + task_lab + \
		                      '_run-01.csv'            
            with open(enc_csvFile, 'w') as w_enc:
                writer = csv.writer(w_enc)
                writer.writerow(['Time', 'Trial_Number', 'Condition', 'Fixation', 'Fixation_Duration',
		                         'Stim_1', 'Stim_2'])
        
        # run encoding if flag is True
        if encoding:
            # initialize important task variables
            shuffle(fix_dur_enc)
            iters_enc = range(0, n_trial_enc)
            encoding_trials = list(iters_enc)
            im1 = visual.ImageStim(win, name='stimPic1', image = None, pos=(-.2, 0))
            im2 = visual.ImageStim(win, name='stimPic2', image = None, pos=(.2, 0))

            # display encoding instructions
            Txt.setText(open('episodic/text/encoding_instructions.txt', 'r').read())
            Txt.draw()
            win.flip()    
            event.waitKeys(keyList=['2','3','4'])

            # launch scan
            Trigger(mainClock)

            # display block 1 sequence on console
            print('\n\n\n\nBlock 1: Encoding')
            print(str(datetime.datetime.now()))
            print('---------------------------')

            # run encoding loop
            for idx in encoding_trials:

                # set stimulus pair
                IMAGE1 = PIL.Image.open(trialList_enc[idx]['stimulus_1'])
                IMAGE2 = PIL.Image.open(trialList_enc[idx]['stimulus_2'])
                
                # record trial number, condition, & stimulus pair
                trial_num = trialList_enc[idx]['trial_num']
                condition = trialList_enc[idx]['condition']
                stim1 = os.path.basename(os.path.normpath(trialList_enc[idx]['stimulus_1']))
                stim2 = os.path.basename(os.path.normpath(trialList_enc[idx]['stimulus_2']))

                # display fixation cross and record its onset
                fixStart = FixationCross(mainClock, fix_dur_enc, idx)

                # print trial info on console
                if trial_num <= 9:
                    print('trial', trial_num, ' |', condition, '|', stim1[:-4], ' & ', stim2[:-4])
                else:
                    print('trial', trial_num, '|', condition, '|', stim1[:-4], ' & ', stim2[:-4])

                # display stimulus pair and record its onset
                stimStart = StimPairs(mainClock)

                # log complete trial info in csv file
                with open(enc_csvFile, 'a') as a_enc:
                    writer = csv.writer(a_enc)
                    writer.writerow([fixStart, trial_num, condition,'ON', stimStart-fixStart,'--', '--'])
                    writer.writerow([stimStart, trial_num, condition, 'OFF', '--', stim1, stim2])
                    writer.writerow(['', '', '', '', '', '', ''])

            # display inter-block instruction buffer
            Txt.setText('End of task :)\n\nGet ready for the next sequence!')
            Txt.draw()
            win.flip()    
            core.wait(4)

        ################################### Block 1 (cont'd): ES1 #############################################
        
        # create .csv log file for experience sampling 1
        if ES1:
            task_lab = '_es1'
            prevRuns = glob.glob(rootLog + '/*' + task_lab + '*')
            if prevRuns:
                prevRuns.sort()
                numRun = len(prevRuns)
                newRun = str('{:02d}'.format(int(prevRuns[numRun-1][-6:-4]) + 1))
                ES1_csvFile = prevRuns[numRun-1][:-6] + newRun + '.csv'
            else:
                ES1_csvFile = rootLog + '/sub-' + expInfo['ID'] + '_ses-' + expInfo['session'] + task_lab + \
		                      '_run-01.csv'          
            with open(ES1_csvFile, 'w') as w_ES1:
                writer = csv.writer(w_ES1)
                writer.writerow(['Time', 'Trial_Number', 'Fixation', 'Fixation_Duration', 'Question',
		                         'Dimension', 'Low_end', 'High_end', 'Subject_Response', 'Reaction_Time'])
        
        # run ES1 if flag is True
        if ES1:
            # initialize important task variables
            shuffle(fix_dur_ES)
            iters_ES = range(0, n_trial_ES)
            ES1_trials = list(iters_ES)
            probe = visual.TextStim(win, color='black', height=.05)

            # display ES1 instructions
            Txt.setText(open('exp_sampling/text/ES_instructions.txt', 'r').read())
            Txt.draw()
            win.flip()    
            event.waitKeys(keyList=['2','3','4'])

            # launch scan
            Trigger(mainClock)

            # display block 1 sequence on console
            print('\nBlock 1 (continued): ES1')
            print(str(datetime.datetime.now()))
            print('---------------------------')

            # randomize trial order
            shuffle(trialList_ES)

            # run ES1 loop
            for idx in ES1_trials:

                # get trial-specific probe labels
                Lab = trialList_ES[idx]['labels']

                # define rating scale parameters
                rating_scale = visual.RatingScale(win, scale=None, low=0, high=10, markerStart=5, leftKeys='2',
		                                          rightKeys='4', acceptKeys='3', labels=Lab,
                                                  tickMarks=['0','10'], tickHeight=1, maxTime=6,
                                                  markerColor='red', textColor='black', textSize=.75,
                                                  stretch=2.5, noMouse=True, lineColor='#3355FF',
                                                  marker='triangle', showValue=False, precision=10,
                                                  showAccept=False, disappear=True)
                
                # record trial number, question, dimension, low/high rates
                trial_num = idx + 1
                question = trialList_ES[idx]['question']
                dimension = trialList_ES[idx]['dimension']
                low_end = trialList_ES[idx]['low_end']
                high_end = trialList_ES[idx]['high_end']

                # display fixation cross and record its onset
                fixStart = FixationCross(mainClock, fix_dur_ES, idx)

                # display probe
                Probe = MindProbe(mainClock, idx)

                # record subject response, reaction time, response time, & confirmation of response status
                SR = rating_scale.getRating()
                RT = rating_scale.getRT()
                respT = Probe + RT
                if RT <= 6:
                    confirmation_status = 'response confirmed:'
                else:
                    confirmation_status = 'response not confirmed:'

                # print trial info on console
                ProbePrint(trial_num, dimension, question, SR)

                # log complete trial info in csv file
                with open(ES1_csvFile, 'a') as a_ES1:
                    writer = csv.writer(a_ES1)
                    writer.writerow([fixStart, trial_num, 'ON', Probe-fixStart, '--', '--', '--', '--', '--',
                                     '--'])
                    writer.writerow([Probe, trial_num, 'OFF', '--', question, dimension, low_end, high_end,
                                     '--', '--'])
                    writer.writerow([respT, trial_num, 'OFF', '--', '--', '--', '--', '--', SR, RT])
                    writer.writerow(['', '', '', '', '', '', '', '', '', ''])

            # display inter-block instruction buffer
            Txt.setText('End of task :)\n\nGet ready for the next sequence!')
            Txt.draw()
            win.flip()
            core.wait(4)

        ################################### Block 2: qT1 ######################################################

        if qT1:
            # display block 2 sequence on console
            print('\n\n\n\nBlock 2: qT1')
            print(str(datetime.datetime.now()))
            print('---------------------------')
            
            # display instructions
            Txt.setText('Scan is in progress.\n\nPlease remain still.')
            Txt.draw()
            win.flip()
            event.waitKeys(keyList=['5'])
       
        ################################### Block 3: Retrieval  ###############################################
        
        # create .csv log file for retrieval
        if retrieval:
            task_lab = '_retrieval'
            prevRuns = glob.glob(rootLog + '/*' + task_lab + '*')
            if prevRuns:
                prevRuns.sort()
                numRun = len(prevRuns)
                newRun = str('{:02d}'.format(int(prevRuns[numRun-1][-6:-4]) + 1))
                ret_csvFile = prevRuns[numRun-1][:-6] + newRun + '.csv'
            else:
                ret_csvFile = rootLog + '/sub-' + expInfo['ID'] + '_ses-' + expInfo['session'] + task_lab + \
		                      '_run-01.csv'
            with open(ret_csvFile, 'w') as w_ret:
                writer = csv.writer(w_ret)
                writer.writerow(['Time', 'Trial_Number', 'Condition', 'Fixation', 'Fixation_Duration', 'Prime',
                                 'Target', 'Foil_1', 'Foil_2', 'Left_choice', 'Center_choice', 'Right_choice',
                                 'Subject_Response', 'Key_pressed', 'Accuracy', 'Reaction_Time'])
        
        # run retrieval if flag is True
        if retrieval:
            # initialize important task variables
            shuffle(fix_dur_ret)
            iters_ret = range(0, n_trial_ret)
            retrieval_trials = list(iters_ret)
            x_values = [-.5, 0, .5]
            y_val = -.25
            retE_acc = []
            retE_RT_hit = []
            retE_RT_miss = []
            retD_acc = []
            retD_RT_hit = []
            retD_RT_miss = []

            # display retrieval instructions
            Txt.setText(open('episodic/text/retrieval_instructions.txt', 'r').read())
            Txt.draw()
            win.flip()    
            event.waitKeys(keyList=['2','3','4'])

            # launch scan
            Trigger(mainClock)

            # display block 3 sequence on console
            print('\n\n\n\nBlock 3: Retrieval')
            print(str(datetime.datetime.now()))
            print('---------------------------')
            
            # run retrieval loop
            for idx in retrieval_trials:

                # set stimuli
                Prime = PIL.Image.open(trialList_ret[idx]['prime'])
                Target = PIL.Image.open(trialList_ret[idx]['target'])
                Foil1 = PIL.Image.open(trialList_ret[idx]['foil1'])
                Foil2 = PIL.Image.open(trialList_ret[idx]['foil2'])

                # set stimuli positions
                shuffle(x_values)
                tg_x = x_values[0]
                foil1_x = x_values[1]
                foil2_x = x_values[2]

                prime_pos = (0, abs(y_val))
                target_pos = (tg_x, y_val)
                foil1_pos = (foil1_x, y_val)
                foil2_pos = (foil2_x, y_val)

                # record trial number, condition, prime, target, foil1, & foil2
                trial_num = trialList_ret[idx]['trial_num']
                condition = trialList_ret[idx]['condition']
                prime_name = os.path.basename(os.path.normpath(trialList_ret[idx]['prime']))
                target_name = os.path.basename(os.path.normpath(trialList_ret[idx]['target']))
                foil1_name = os.path.basename(os.path.normpath(trialList_ret[idx]['foil1']))
                foil2_name = os.path.basename(os.path.normpath(trialList_ret[idx]['foil2']))

                # display fixation cross and record its onset
                fixStart = FixationCross(mainClock, fix_dur_ret, idx)

                # print trial info on console
                if trial_num <= 9:
                    print('trial', trial_num, ' |', condition, '| prime:', prime_name[:-4], '| target: ',
			              target_name[:-4], '| foils: ', foil1_name[:-4], ' & ', foil2_name[:-4])
                else:
                    print('trial', trial_num, '|', condition, '| prime:', prime_name[:-4], '| target: ',
			              target_name[:-4], '| foils: ', foil1_name[:-4], ' & ', foil2_name[:-4])

                # display stimuli and record onset
                stimStart = RetrievalScreen(mainClock, prime_pos, target_pos, foil1_pos, foil2_pos)
                
                # get subject response info
                trialEndTime = stimStart + 2.5
                subResp = RetrievalResponse(mainClock, trialEndTime, stimStart)
                keyPressTime = subResp[0]
                key_pressed = subResp[1]
                RT = subResp[2]
                respInfo = RetrievalInfo(RT, y_val, target_pos, foil1_pos, foil2_pos, target_name, foil1_name,
                                         foil2_name)
                key_ID = respInfo[0]
                subChoice = respInfo[1]
                left_choice = respInfo[2]
                center_choice = respInfo[3]
                right_choice = respInfo[4]
                accuracy = respInfo[5]
                
                # display subject response info on console
                if accuracy == 1:
                    print('Subject CORRECTLY chose "' + subChoice + '" in ', RT, 'sec')
                    print('\n')
                else:
                    if RT == 'N/A':
                        print('Subject did not respond/was too slow')
                        print('\n')
                    else:
                        print('Subject INCORRECTLY chose "' + subChoice + '" in ', RT, 'sec')
                        print('\n')
                
                # append trial info to accuracy & RT lists
                if condition == 'E':
                    retE_acc.append(accuracy)
                    if accuracy == 1:
                        retE_RT_hit.append(RT)
                    elif accuracy == 0:
                        if RT != 'N/A':
                            retE_RT_miss.append(RT)
                elif condition == 'D':
                    retD_acc.append(accuracy)
                    if accuracy == 1:
                        retD_RT_hit.append(RT)
                    elif accuracy == 0:
                        if RT != 'N/A':
                            retD_RT_miss.append(RT)
                
                # log complete trial info in csv file
                with open(ret_csvFile, 'a') as a_ret:
                    writer = csv.writer(a_ret)
                    writer.writerow([fixStart, trial_num, condition, 'ON', stimStart-fixStart, '--', '--',
                                     '--', '--', '--', '--', '--', '--', '--', '--', '--'])
                    writer.writerow([stimStart, trial_num, condition, 'OFF', '--', prime_name, target_name,
		                             foil1_name, foil2_name, left_choice, center_choice, right_choice,
                                     '--', '--', '--', '--'])
                    writer.writerow([keyPressTime, trial_num, condition, 'OFF', '--', '--', '--', '--', '--',
				                     '--', '--', '--', subChoice, key_ID, accuracy, RT])
                    writer.writerow(['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])

            # compute scores & display on console
            retE_score = (sum(retE_acc) / len(retE_acc)) * 100
            retD_score = (sum(retD_acc) / len(retD_acc)) * 100
                        
            if retE_RT_hit:
                mean_retE_RT_hit = sum(retE_RT_hit) / len(retE_RT_hit)
            else:
                mean_retE_RT_hit = 'N/A'
            
            if retD_RT_hit:
                mean_retD_RT_hit = sum(retD_RT_hit) / len(retD_RT_hit)
            else:
                mean_retD_RT_hit = 'N/A'
            
            if retE_RT_miss:
                mean_retE_RT_miss = sum(retE_RT_miss) / len(retE_RT_miss)
            else:
                mean_retE_RT_miss = 'N/A'
            
            if retD_RT_miss:
                mean_retD_RT_miss = sum(retD_RT_miss) / len(retD_RT_miss)
            else:
                mean_retD_RT_miss = 'N/A'
            
            print('retE score:          ', retE_score, '%')
            print('retD score:          ', retD_score, '%')
            print('mean retE RT (hit):  ', mean_retE_RT_hit, 'sec')
            print('mean retD RT (hit):  ', mean_retD_RT_hit, 'sec')
            print('mean retE RT (miss): ', mean_retE_RT_miss, 'sec')
            print('mean retD RT (miss): ', mean_retD_RT_miss, 'sec')

            # display inter-block instruction buffer
            Txt.setText('End of task :)\n\nGet ready for the next sequence!')
            Txt.draw()
            win.flip()    
            core.wait(4)

        ################################### Block 3 (cont'd): ES2 #############################################
        
        # create .csv log file for experience sampling 2
        if ES2:
            task_lab = '_es2'
            prevRuns = glob.glob(rootLog + '/*' + task_lab + '*')
            if prevRuns:
                prevRuns.sort()
                numRun = len(prevRuns)
                newRun = str('{:02d}'.format(int(prevRuns[numRun-1][-6:-4]) + 1))
                ES2_csvFile = prevRuns[numRun-1][:-6] + newRun + '.csv'
            else:
                ES2_csvFile = rootLog + '/sub-' + expInfo['ID'] + '_ses-' + expInfo['session'] + task_lab + \
                              '_run-01.csv'
            with open(ES2_csvFile, 'w') as w_ES2:
                writer = csv.writer(w_ES2)
                writer.writerow(['Time', 'Trial_Number', 'Fixation', 'Fixation_Duration', 'Question',
                                 'Dimension', 'Low_end', 'High_end', 'Subject_Response', 'Reaction_Time'])
        
        # run ES2 if flag is True
        if ES2:
            # initialize important task variables
            shuffle(fix_dur_ES)
            iters_ES = range(0, n_trial_ES)
            ES2_trials = list(iters_ES)
            probe = visual.TextStim(win, color='black', height=.05)

            # display ES2 instructions
            Txt.setText(open('exp_sampling/text/ES_instructions.txt', 'r').read())
            Txt.draw()
            win.flip()    
            event.waitKeys(keyList=['2','3','4'])

            # launch scan
            Trigger(mainClock)

            # display block 3 sequence on console
            print('\nBlock 3 (continued): ES2')
            print(str(datetime.datetime.now()))
            print('---------------------------')

            # randomize trial order
            shuffle(trialList_ES)

            # run ES2 loop
            for idx in ES2_trials:

                # get trial-specific probe labels
                Lab = trialList_ES[idx]['labels']

                # define rating scale parameters
                rating_scale = visual.RatingScale(win, scale=None, low=0, high=10, markerStart=5, leftKeys='2',
                                                  rightKeys='4', acceptKeys='3', labels=Lab,
                                                  tickMarks=['0','10'], tickHeight=1, maxTime=6,
                                                  markerColor='red', textColor='black', textSize=.75,
                                                  stretch=2.5, noMouse=True, lineColor='#3355FF',
                                                  marker='triangle', showValue=False, precision=10,
                                                  showAccept=False, disappear=True)

                # record trial number, question, dimension, low/high rates
                trial_num = idx + 1
                question = trialList_ES[idx]['question']
                dimension = trialList_ES[idx]['dimension']
                low_end = trialList_ES[idx]['low_end']
                high_end = trialList_ES[idx]['high_end']

                # display fixation cross and record its onset
                fixStart = FixationCross(mainClock, fix_dur_ES, idx)

                # display probe
                Probe = MindProbe(mainClock, idx)

                # record subject response, reaction time, response time, & confirmation of response status
                SR = rating_scale.getRating()
                RT = rating_scale.getRT()
                respT = Probe + RT
                if RT <= 6:
                    confirmation_status = 'response confirmed:'
                else:
                    confirmation_status = 'response not confirmed:'

                # print trial info on console
                ProbePrint(trial_num, dimension, question, SR)

                # log complete trial info in csv file
                with open(ES2_csvFile, 'a') as a_ES2:
                    writer = csv.writer(a_ES2)
                    writer.writerow([fixStart, trial_num, 'ON', Probe-fixStart, '--', '--', '--', '--', '--',
                                     '--'])
                    writer.writerow([Probe, trial_num, 'OFF', '--', question, dimension, low_end, high_end,
                                     '--', '--'])
                    writer.writerow([respT, trial_num, 'OFF', '--', '--', '--', '--', '--', SR, RT])
                    writer.writerow(['', '', '', '', '', '', '', '', '', ''])

            # display inter-block instruction buffer
            Txt.setText('End of task :)\n\nGet ready for the next sequence!')
            Txt.draw()
            win.flip()
            core.wait(4)

        ################################### Block 4: T2* ######################################################
        
        if T2star:
            # display block 4 sequence on console
            print('\n\n\n\nBlock 4: T2*')
            print(str(datetime.datetime.now()))
            print('---------------------------')
            
            # display instructions
            Txt.setText('Scan is in progress.\n\nPlease remain still.')
            Txt.draw()
            win.flip()
            event.waitKeys(keyList=['5'])
        
        ################################### Block 5: MST1 #####################################################
        
        # create .csv log file for MST1
        if MST1:
            task_lab = '_mst1'
            prevRuns = glob.glob(rootLog + '/*' + task_lab + '*')
            if prevRuns:
                prevRuns.sort()
                numRun = len(prevRuns)
                newRun = str('{:02d}'.format(int(prevRuns[numRun-1][-6:-4]) + 1))
                mst1_csvFile = prevRuns[numRun-1][:-6] + newRun + '.csv'
            else:
                mst1_csvFile = rootLog + '/sub-' + expInfo['ID'] + '_ses-' + expInfo['session'] + task_lab + \
                               '_run-01.csv'
            with open(mst1_csvFile, 'w') as w_mst1:
                writer = csv.writer(w_mst1)
                writer.writerow(['Time', 'Trial_Number', 'Fixation', 'Fixation_Duration', 'Stim_ID',
                                 'Subject_Response', 'Reaction_Time'])
        
        if MST1:
            # initialize important task variables
            shuffle(fix_dur_mst1)
            iters_mst1 = range(0, n_trial_mst1)
            mst1_trials = list(iters_mst1)
            im = visual.ImageStim(win, name='stimPic', image = None, pos=(0, 0))
            
            # display MST1 instructions
            Txt.setText(open('MST/text/MST1_instructions.txt', 'r').read())
            Txt.draw()
            win.flip()    
            event.waitKeys(keyList=['2','3','4'])

            # launch scan
            Trigger(mainClock)

            # display block 5 sequence on console
            print('\n\n\n\nBlock 5: MST1')
            print(str(datetime.datetime.now()))
            print('---------------------------')
            
            # run mst1 loop
            for idx in mst1_trials:

                # set stimulus pair
                IMAGE = PIL.Image.open(trialList_mst1[idx]['stimulus'])
                
                # record trial number and stimulus
                trial_num = trialList_mst1[idx]['trial_num']
                stim = os.path.basename(os.path.normpath(trialList_mst1[idx]['stimulus']))
                
                # display fixation cross and record its onset
                fixStart = FixationCross(mainClock, fix_dur_mst1, idx)
                
                # print trial info on console
                if trial_num <= 9:
                    print('trial', trial_num, ' |', stim[:-4])
                else:
                    print('trial', trial_num, '|', stim[:-4])

                # display stimulus and record its onset
                MSTtext = visual.TextStim(win, text='Indoors or Outdoors?', font=sans, name='instruction',
                                          pos=(0, .4), height=float(.04), wrapWidth=1100, color='black')
	            
                stimStart = MSTScreen(mainClock)
                
                # get subject response info
                trialEndTime = stimStart + 2
                subResp = MST1Response(mainClock, trialEndTime, stimStart)
                keyPressTime = subResp[0]
                SR = subResp[1]
                RT = subResp[2]
                
                # display subject response info on console
                if RT == 'N/A':
                        print('Subject did not respond/was too slow')
                        print('\n')
                else:
                    print('Subject chose "' + SR + '" in ', RT, 'sec')
                    print('\n')
                
                # log complete trial info in csv file
                with open(mst1_csvFile, 'a') as a_mst1:
                    writer = csv.writer(a_mst1)
                    writer.writerow([fixStart, trial_num, 'ON', stimStart-fixStart, '--', '--', '--'])
                    writer.writerow([stimStart, trial_num, 'OFF', '--', stim, '--', '--'])
                    writer.writerow([keyPressTime, trial_num, 'OFF', '--', '--', SR, RT])
                    writer.writerow(['', '', '', '', '', '', ''])

            # display inter-block instruction buffer
            Txt.setText('End of task :)\n\nGet ready for the next sequence!')
            Txt.draw()
            win.flip()    
            core.wait(4)
        
        ################################### Block 5 (cont'd): ES3 #############################################
        
        # create .csv log file for experience sampling 3
        if ES3:
            task_lab = '_es3'
            prevRuns = glob.glob(rootLog + '/*' + task_lab + '*')
            if prevRuns:
                prevRuns.sort()
                numRun = len(prevRuns)
                newRun = str('{:02d}'.format(int(prevRuns[numRun-1][-6:-4]) + 1))
                ES3_csvFile = prevRuns[numRun-1][:-6] + newRun + '.csv'
            else:
                ES3_csvFile = rootLog + '/sub-' + expInfo['ID'] + '_ses-' + expInfo['session'] + task_lab + \
                              '_run-01.csv'            
            with open(ES3_csvFile, 'w') as w_ES3:
                writer = csv.writer(w_ES3)
                writer.writerow(['Time', 'Trial_Number', 'Fixation', 'Fixation_Duration', 'Question',
                                 'Dimension', 'Low_end', 'High_end', 'Subject_Response', 'Reaction_Time'])
        
        # run ES3 if flag is True
        if ES3:
            # initialize important task variables
            shuffle(fix_dur_ES)
            iters_ES = range(0, n_trial_ES)
            ES3_trials = list(iters_ES)
            probe = visual.TextStim(win, color='black', height=.05)

            # display ES3 instructions
            Txt.setText(open('exp_sampling/text/ES_instructions.txt', 'r').read())
            Txt.draw()
            win.flip()    
            event.waitKeys(keyList=['2','3','4'])

            # launch scan
            Trigger(mainClock)

            # display block 5 sequence on console
            print('Block 5 (continued): ES3')
            print(str(datetime.datetime.now()))
            print('---------------------------')

            # randomize trial order
            shuffle(trialList_ES)

            # run ES3 loop
            for idx in ES3_trials:

                # get trial-specific probe labels
                Lab = trialList_ES[idx]['labels']

                # define rating scale parameters
                rating_scale = visual.RatingScale(win, scale=None, low=0, high=10, markerStart=5, leftKeys='2',
                                                  rightKeys='4', acceptKeys='3', labels=Lab,
                                                  tickMarks=['0','10'], tickHeight=1, maxTime=6,
                                                  markerColor='red', textColor='black', textSize=.75,
                                                  stretch=2.5, noMouse=True, lineColor='#3355FF',
                                                  marker='triangle', showValue=False, precision=10,
                                                  showAccept=False, disappear=True)
                
                # record trial number, question, dimension, low/high rates
                trial_num = idx + 1
                question = trialList_ES[idx]['question']
                dimension = trialList_ES[idx]['dimension']
                low_end = trialList_ES[idx]['low_end']
                high_end = trialList_ES[idx]['high_end']

                # display fixation cross and record its onset
                fixStart = FixationCross(mainClock, fix_dur_ES, idx)

                # display probe
                Probe = MindProbe(mainClock, idx)

                # record subject response, reaction time, response time, & confirmation of response status
                SR = rating_scale.getRating()
                RT = rating_scale.getRT()
                respT = Probe + RT
                if RT <= 6:
                    confirmation_status = 'response confirmed:'
                else:
                    confirmation_status = 'response not confirmed:'

                # print trial info on console
                ProbePrint(trial_num, dimension, question, SR)

                # log complete trial info in csv file
                with open(ES3_csvFile, 'a') as a_ES3:
                    writer = csv.writer(a_ES3)
                    writer.writerow([fixStart, trial_num, 'ON', Probe-fixStart, '--', '--', '--', '--', '--',
                                     '--'])
                    writer.writerow([Probe, trial_num, 'OFF', '--', question, dimension, low_end, high_end,
                                     '--', '--'])
                    writer.writerow([respT, trial_num, 'OFF', '--', '--', '--', '--', '--', SR, RT])
                    writer.writerow(['', '', '', '', '', '', '', '', '', ''])

            # display inter-block instruction buffer
            Txt.setText('End of task :)\n\nGet ready for the next sequence!')
            Txt.draw()
            win.flip()
            core.wait(4)
        
        ################################### Block 6: DWI ######################################################
        
        if DWI:
            # display block 4 sequence on console
            print('\n\n\n\nBlock 6: DWI')
            print(str(datetime.datetime.now()))
            print('---------------------------')
            
            # display instructions
            Txt.setText('Scan is in progress.\n\nPlease remain still.')
            Txt.draw()
            win.flip()
            event.waitKeys(keyList=['5'])
        
        ################################### Block 7: MST2 #####################################################

        # create .csv log file for MST2
        if MST2:
            task_lab = '_mst2'
            prevRuns = glob.glob(rootLog + '/*' + task_lab + '*')
            if prevRuns:
                prevRuns.sort()
                numRun = len(prevRuns)
                newRun = str('{:02d}'.format(int(prevRuns[numRun-1][-6:-4]) + 1))
                mst2_csvFile = prevRuns[numRun-1][:-6] + newRun + '.csv'
            else:
                mst2_csvFile = rootLog + '/sub-' + expInfo['ID'] + '_ses-' + expInfo['session'] + task_lab + \
                               '_run-01.csv'            
            with open(mst2_csvFile, 'w') as w_mst2:
                writer = csv.writer(w_mst2)
                writer.writerow(['Time', 'Trial_Number', 'Condition', 'Fixation', 'Fixation_Duration',
                                 'Stim_ID', 'Subject_Response', 'Accuracy', 'Reaction_Time'])
        
        if MST2:
            # initialize important task variables
            shuffle(fix_dur_mst2)
            iters_mst2 = range(0, n_trial_mst2)
            mst2_trials = list(iters_mst2)
            im = visual.ImageStim(win, name='stimPic', image = None, pos=(0, 0))
            
            # display MST2 instructions
            Txt.setText(open('MST/text/MST2_instructions.txt', 'r').read())
            Txt.draw()
            win.flip()    
            event.waitKeys(keyList=['2','3','4'])

            # launch scan
            Trigger(mainClock)

            # display block 7 sequence on console
            print('\n\n\n\nBlock 7: MST2')
            print(str(datetime.datetime.now()))
            print('---------------------------')
            
            # run mst2 loop
            for idx in mst2_trials:

                # set stimulus pair
                IMAGE = PIL.Image.open(trialList_mst2[idx]['stimulus'])
                
                # record trial number and stimulus
                trial_num = trialList_mst2[idx]['trial_num']
                condition = trialList_mst2[idx]['condition']
                stim = os.path.basename(os.path.normpath(trialList_mst2[idx]['stimulus']))
                
                # display fixation cross and record its onset
                fixStart = FixationCross(mainClock, fix_dur_mst2, idx)
                
                # print trial info on console
                if trial_num <= 9:
                    print('trial', trial_num, ' |', condition, '|', stim[:-4])
                else:
                    print('trial', trial_num, '|', condition, '|', stim[:-4])

                # display stimulus and record its onset
                MSTtext = visual.TextStim(win, text='Old, Similar, or New?', font=sans, name='instruction',
		                                  pos=(0, .4), height=float(.04), wrapWidth=1100, color='black')
                
                stimStart = MSTScreen(mainClock)
                
                # get subject response info
                trialEndTime = stimStart + 2.5
                subResp = MST2Response(mainClock, trialEndTime, stimStart)
                keyPressTime = subResp[0]
                SR = subResp[1]
                RT = subResp[2]
                
                # display subject response info on console
                if RT == 'N/A':
                    accuracy = 0
                    print('Subject did not respond/was too slow')
                    print('\n')
                else:
                    if SR == condition:
                        accuracy = 1
                        print('Subject CORRECTLY chose "' + SR + '" in ', RT, 'sec')
                        print('\n')
                    elif SR != condition:
                        accuracy = 0
                        print('Subject INCORRECTLY chose "' + SR + '" in ', RT, 'sec')
                        print('\n')
                
                # log complete trial info in csv file
                with open(mst2_csvFile, 'a') as a_mst2:
                    writer = csv.writer(a_mst2)
                    writer.writerow([fixStart, trial_num, condition, 'ON', stimStart-fixStart, '--', '--',
                                     '--', '--'])
                    writer.writerow([stimStart, trial_num, condition, 'OFF', '--', stim, '--', '--', '--'])
                    writer.writerow([keyPressTime, trial_num, condition, 'OFF', '--', '--', SR, accuracy, RT])
                    writer.writerow(['', '', '', '', '', '', '', '', ''])

            # display inter-block instruction buffer
            Txt.setText('End of task :)\n\nGet ready for the next sequence!')
            Txt.draw()
            win.flip()    
            core.wait(4)

        ################################### Block 7 (cont'd): ES4 #############################################
        
        # create .csv log file for experience sampling 4
        if ES4:
            task_lab = '_es4'
            prevRuns = glob.glob(rootLog + '/*' + task_lab + '*')
            if prevRuns:
                prevRuns.sort()
                numRun = len(prevRuns)
                newRun = str('{:02d}'.format(int(prevRuns[numRun-1][-6:-4]) + 1))
                ES4_csvFile = prevRuns[numRun-1][:-6] + newRun + '.csv'
            else:
                ES4_csvFile = rootLog + '/sub-' + expInfo['ID'] + '_ses-' + expInfo['session'] + task_lab + \
                              '_run-01.csv'
            with open(ES4_csvFile, 'w') as w_ES4:
                writer = csv.writer(w_ES4)
                writer.writerow(['Time', 'Trial_Number', 'Fixation', 'Fixation_Duration', 'Question',
                                 'Dimension', 'Low_end', 'High_end', 'Subject_Response', 'Reaction_Time'])
        
        # run ES4 if flag is True
        if ES4:
            # initialize important task variables
            shuffle(fix_dur_ES)
            iters_ES = range(0, n_trial_ES)
            ES4_trials = list(iters_ES)
            probe = visual.TextStim(win, color='black', height=.05)

            # display ES4 instructions
            Txt.setText(open('exp_sampling/text/ES_instructions.txt', 'r').read())
            Txt.draw()
            win.flip()    
            event.waitKeys(keyList=['2','3','4'])

            # launch scan
            Trigger(mainClock)

            # display block 7 sequence on console
            print('Block 7 (continued): ES4')
            print(str(datetime.datetime.now()))
            print('---------------------------')

            # randomize trial order
            shuffle(trialList_ES)

            # run ES4 loop
            for idx in ES4_trials:

                # get trial-specific probe labels
                Lab = trialList_ES[idx]['labels']

                # define rating scale parameters
                rating_scale = visual.RatingScale(win, scale=None, low=0, high=10, markerStart=5, leftKeys='2',
                                                  rightKeys='4', acceptKeys='3', labels=Lab,
                                                  tickMarks=['0','10'], tickHeight=1, maxTime=6,
                                                  markerColor='red', textColor='black', textSize=.75,
                                                  stretch=2.5, noMouse=True, lineColor='#3355FF',
                                                  marker='triangle', showValue=False, precision=10,
                                                  showAccept=False, disappear=True)
                
                # record trial number, question, dimension, low/high rates
                trial_num = idx + 1
                question = trialList_ES[idx]['question']
                dimension = trialList_ES[idx]['dimension']
                low_end = trialList_ES[idx]['low_end']
                high_end = trialList_ES[idx]['high_end']

                # display fixation cross and record its onset
                fixStart = FixationCross(mainClock, fix_dur_ES, idx)

                # display probe
                Probe = MindProbe(mainClock, idx)

                # record subject response, reaction time, response time, & confirmation of response status
                SR = rating_scale.getRating()
                RT = rating_scale.getRT()
                respT = Probe + RT
                if RT <= 6:
                    confirmation_status = 'response confirmed:'
                else:
                    confirmation_status = 'response not confirmed:'

                # print trial info on console
                ProbePrint(trial_num, dimension, question, SR)

                # log complete trial info in csv file
                with open(ES4_csvFile, 'a') as a_ES4:
                    writer = csv.writer(a_ES4)
                    writer.writerow([fixStart, trial_num, 'ON', Probe-fixStart, '--', '--', '--', '--', '--',
                                     '--'])
                    writer.writerow([Probe, trial_num, 'OFF', '--', question, dimension, low_end, high_end,
                                     '--', '--'])
                    writer.writerow([respT, trial_num, 'OFF', '--', '--', '--', '--', '--', SR, RT])
                    writer.writerow(['', '', '', '', '', '', '', '', '', ''])

            # display inter-block instruction buffer
            Txt.setText('End of task :)\n\nGet ready for the next sequence!')
            Txt.draw()
            win.flip()
            core.wait(4)
        
        ################################### Block 8: RS #######################################################
        
        if RS:
            # display block 8 sequence on console
            print('\n\n\n\nBlock 8: RS')
            print(str(datetime.datetime.now()))
            print('---------------------------')
            
            # display RS instructions
            Txt.setText(open('RS/text/RS_instructions.txt', 'r').read())
            Txt.draw()
            win.flip()
            event.waitKeys(keyList=['2','3','4'])
            
            # launch scan
            Trigger(mainClock)
            
            # display RS fixation cross
            RS_FixCross = visual.TextStim(win, name='RS fixation cross', text='+', font=sans, pos=(0, 0),
	                                  height=float(.16), color='gray')
            RS_FixCross.draw()
            win.flip()
            event.waitKeys(keyList=['space']) 
            
            Txt.setText('End of task :)\n\nGet ready for the next sequence!')
            Txt.draw()
            win.flip()
            core.wait(4)
        
        ################################### Block 8 (cont'd): ES5 #############################################
        
        # create .csv log file for experience sampling 5
        if ES5:
            task_lab = '_es5'
            prevRuns = glob.glob(rootLog + '/*' + task_lab + '*')
            if prevRuns:
                prevRuns.sort()
                numRun = len(prevRuns)
                newRun = str('{:02d}'.format(int(prevRuns[numRun-1][-6:-4]) + 1))
                ES5_csvFile = prevRuns[numRun-1][:-6] + newRun + '.csv'
            else:
                ES5_csvFile = rootLog + '/sub-' + expInfo['ID'] + '_ses-' + expInfo['session'] + task_lab + \
                              '_run-01.csv'            
            with open(ES5_csvFile, 'w') as w_ES5:
                writer = csv.writer(w_ES5)
                writer.writerow(['Time', 'Trial_Number', 'Fixation', 'Fixation_Duration', 'Question',
                                 'Dimension', 'Low_end', 'High_end', 'Subject_Response', 'Reaction_Time'])
        
        # run ES5 if flag is True
        if ES5:
            # initialize important task variables
            shuffle(fix_dur_ES)
            iters_ES = range(0, n_trial_ES)
            ES5_trials = list(iters_ES)
            probe = visual.TextStim(win, color='black', height=.05)

            # display ES5 instructions
            Txt.setText(open('exp_sampling/text/ES_instructions.txt', 'r').read())
            Txt.draw()
            win.flip()    
            event.waitKeys(keyList=['2','3','4'])

            # launch scan
            Trigger(mainClock)

            # display block 8 sequence on console
            print('\nBlock 8 (continued): ES5')
            print(str(datetime.datetime.now()))
            print('---------------------------')

            # randomize trial order
            shuffle(trialList_ES)

            # run ES5 loop
            for idx in ES5_trials:

                # get trial-specific probe labels
                Lab = trialList_ES[idx]['labels']

                # define rating scale parameters
                rating_scale = visual.RatingScale(win, scale=None, low=0, high=10, markerStart=5, leftKeys='2',
                                                  rightKeys='4', acceptKeys='3', labels=Lab,
                                                  tickMarks=['0','10'], tickHeight=1, maxTime=6,
                                                  markerColor='red', textColor='black', textSize=.75,
                                                  stretch=2.5, noMouse=True, lineColor='#3355FF',
                                                  marker='triangle', showValue=False, precision=10,
                                                  showAccept=False, disappear=True)
                
                # record trial number, question, dimension, low/high rates
                trial_num = idx + 1
                question = trialList_ES[idx]['question']
                dimension = trialList_ES[idx]['dimension']
                low_end = trialList_ES[idx]['low_end']
                high_end = trialList_ES[idx]['high_end']

                # display fixation cross and record its onset
                fixStart = FixationCross(mainClock, fix_dur_ES, idx)

                # display probe
                Probe = MindProbe(mainClock, idx)

                # record subject response, reaction time, response time, & confirmation of response status
                SR = rating_scale.getRating()
                RT = rating_scale.getRT()
                respT = Probe + RT
                if RT <= 6:
                    confirmation_status = 'response confirmed:'
                else:
                    confirmation_status = 'response not confirmed:'

                # print trial info on console
                ProbePrint(trial_num, dimension, question, SR)

                # log complete trial info in csv file
                with open(ES5_csvFile, 'a') as a_ES5:
                    writer = csv.writer(a_ES5)
                    writer.writerow([fixStart, trial_num, 'ON', Probe-fixStart, '--', '--', '--', '--', '--',
                                     '--'])
                    writer.writerow([Probe, trial_num, 'OFF', '--', question, dimension, low_end, high_end,
                                     '--', '--'])
                    writer.writerow([respT, trial_num, 'OFF', '--', '--', '--', '--', '--', SR, RT])
                    writer.writerow(['', '', '', '', '', '', '', '', '', ''])

            # display inter-block instruction buffer
            Txt.setText('End of protocol.')
            Txt.draw()
            win.flip()
            core.wait(4)
       
    ####################################### 2nd English protocol ##############################################
    ###########################################################################################################
    elif expInfo['language'] == 'English' and expInfo['protocol'] == 'II':
        print('\n\n\n\n-------------------------------------------------------------------------')
        print('ID:           ' + expInfo['ID'])
        print('Session:      ' + expInfo['session']) 
        print('Language:     ' + expInfo['language'])
        print('Protocol:     ' + expInfo['protocol'])
        print('Block 1:      spatial 1 & experience sampling 1                     ' + expInfo['Block1'])
        print('Block 2:      quantitative T1-mapping                               ' + expInfo['Block2'])
        print('Block 3:      spatial 2 & experience sampling 2                     ' + expInfo['Block3'])
        print('Block 4:      T2*-weighted imaging                                  ' + expInfo['Block4'])
        print('Block 5:      semantic 1 & experience sampling 3                    ' + expInfo['Block5'])
        print('Block 6:      diffusion-weighted imaging                            ' + expInfo['Block6'])
        print('Block 7:      semantic 2 & experience sampling 4                    ' + expInfo['Block7'])
        print('Block 8:      resting state & experience sampling 5                 ' + expInfo['Block8'])
        print('-------------------------------------------------------------------------')
	
	    ## import stimuli for each block
        trialList_ES = data.importConditions('exp_sampling/ES_trials.csv')
        trialList_spa = data.importConditions('spatial/spa_List' + expInfo['list'] + '.csv')
        trialList_spa1 = trialList_spa[0:24]
        trialList_spa2 = trialList_spa[24:48]
        trialList_sem1 = data.importConditions('semantic/sem1_List' + expInfo['list'] + '.csv')
        #trialList_sem2 = data.importConditions('semantic/sem2_List' + expInfo['list'] + '.csv')
	
	    # create list of variable fixation cross durations for each block
        n_trial_ES = len(trialList_ES)
        fix_increment_ES = 1 / (n_trial_ES - 1)
        range_trial_ES = range(0, n_trial_ES)
        fix_dur_ES = [2 + (x * fix_increment_ES) for x in range_trial_ES]
        
        n_trial_spa1 = len(trialList_spa1)
        fix_increment_spa1 = 1 / (n_trial_spa1 - 1)
        range_trial_spa1 = range(0, n_trial_spa1)
        ITI_spa1 = [3 + (x * fix_increment_spa1) for x in range_trial_spa1]
        ISI_spa1 = [.5 + (x * fix_increment_spa1) for x in range_trial_spa1]
        
        # n_trial_spa2 = len(trialList_spa2)
        # fix_increment_spa2 = 1 / (n_trial_spa2 - 1)
        # range_trial_spa2 = range(0, n_trial_spa2)
        # fix_dur_spa2 = [4 + (x * fix_increment_spa2) for x in range_trial_spa2]
        
        n_trial_sem1 = len(trialList_sem1)
        fix_increment_sem1 = 1 / (n_trial_sem1 - 1)
        range_trial_sem1 = range(0, n_trial_sem1)
        fix_dur_sem1 = [4 + (x * fix_increment_sem1) for x in range_trial_sem1]
        
        #n_trial_sem2 = len(trialList_sem2)
        #fix_increment_sem2 = 1 / (n_trial_sem2 - 1)
        #range_trial_sem2 = range(0, n_trial_sem2)
        #fix_dur_sem2 = [4 + (x * fix_increment_sem2) for x in range_trial_sem2]
        
        # create subject-specific directory to keep logs
        rootLog = 'logs/sub-' + expInfo['ID'] + '/ses-' + expInfo['session'] + '/beh'
        
        if not os.path.isdir(rootLog):
            os.makedirs(rootLog)
        
        # define functions for each block
        def FixationCross(clock, fix_dur, trialNum):
            fixation.draw()
            win.logOnFlip(level=logging.EXP, msg='fixation cross')
            win.flip()
            fixation_onset = clock.getTime()
            core.wait(fix_dur[trialNum])
            if event.getKeys(keyList=['escape']):
                core.quit()
            event.clearEvents()
            return fixation_onset
        
        def spatialPrimeScreen(clock, prime_pos):
            prime_im = visual.ImageStim(win, name='prime', image = None, pos=prime_pos)
            prime_im.setImage(Prime)
            prime_im.draw()
            win.logOnFlip(level=logging.EXP, msg='spatial prime screen')
            win.flip()
            spatialPrimeScreen_onset = clock.getTime()
            core.wait(4)
            event.clearEvents()
            return spatialPrimeScreen_onset
        
        def spatialChoiceScreen(clock, target_pos, foil1_pos, foil2_pos): 
            tg_im = visual.ImageStim(win, name='target', image = None, pos=target_pos)
            foil1_im = visual.ImageStim(win, name='foil1', image = None, pos=foil1_pos)
            foil2_im = visual.ImageStim(win, name='foil2', image = None, pos=foil2_pos)
            tg_im.setImage(Target)
            foil1_im.setImage(Foil1)
            foil2_im.setImage(Foil2)
            tg_im.draw()
            foil1_im.draw()
            foil2_im.draw()
            win.logOnFlip(level=logging.EXP, msg='spatial choice screen')
            win.flip()
            spatialChoiceScreen_onset = clock.getTime()
            return spatialChoiceScreen_onset
        
        def SpatialResponse(clock, trialEndTime, choiceStart):
            flag = 0
            keyList = []
            keypress = []
            while clock.getTime() < trialEndTime:
                keypress = event.getKeys(keyList=['2','3','4'])
                if len(keypress) == 1 and flag == 0:
                    keyList = keypress[0]
                    flag = 1
                    keyStart = clock.getTime()
            if len(keyList) == 1 and flag == 1:    
                    key_pressed = keyList[0]
                    RT = keyStart - choiceStart
            else:
                keyStart = '--'
                key_pressed = 'N/A'
                RT = 'N/A'
            event.clearEvents()
            return keyStart, key_pressed, RT
        
        def SpatialInfo(RT, y_val, target_pos, foil1_pos, foil2_pos, target_name, foil1_name, foil2_name):
            if RT == 'N/A':
                im_position = 'N/A'
                key_ID = 'N/A'
                subChoice = 'N/A'
                accuracy = 0
            elif RT < 5.5:
                if key_pressed == '2':
                    im_position = (-.5, y_val)
                    key_ID = 'left'
                elif key_pressed == '3':
                    im_position = (0, y_val)
                    key_ID = 'center'
                elif key_pressed == '4':
                    im_position = (.5, y_val)
                    key_ID = 'right'
            if im_position == target_pos:
                subChoice = target_name[:-4]
                accuracy = 1
            elif im_position == foil1_pos:
                subChoice = foil1_name[:-4]
                accuracy = 0
            elif im_position == foil2_pos:
                subChoice = foil2_name[:-4]
                accuracy = 0
            if target_pos == (-.5, y_val) and foil1_pos == (0, y_val) and foil2_pos == (.5, y_val):
                left_choice = target_name[:-4]
                center_choice = foil1_name[:-4]
                right_choice = foil2_name[:-4]
            elif target_pos == (-.5, y_val) and foil2_pos == (0, y_val) and foil1_pos == (.5, y_val):
                left_choice = target_name[:-4]
                center_choice = foil2_name[:-4]
                right_choice = foil1_name[:-4]
            elif foil1_pos == (-.5, y_val) and target_pos == (0, y_val) and foil2_pos == (.5, y_val):
                left_choice = foil1_name[:-4]
                center_choice = target_name[:-4]
                right_choice = foil2_name[:-4]
            elif foil1_pos == (-.5, y_val) and foil2_pos == (0, y_val) and target_pos == (.5, y_val):
                left_choice = foil1_name[:-4]
                center_choice = foil2_name[:-4]
                right_choice = target_name[:-4]
            elif foil2_pos == (-.5, y_val) and target_pos == (0, y_val) and foil1_pos == (.5, y_val):
                left_choice = foil2_name[:-4]
                center_choice = target_name[:-4]
                right_choice = foil1_name[:-4]
            elif foil2_pos == (-.5, y_val) and foil1_pos == (0, y_val) and target_pos == (.5, y_val):
                left_choice = foil2_name[:-4]
                center_choice = foil1_name[:-4]
                right_choice = target_name[:-4]
            return key_ID, subChoice, left_choice, center_choice, right_choice, accuracy
        
        def MindProbe(clock, idx):
            flag = 1
            inc = 0.1
            pos = rating_scale.markerStart
            keyState=key.KeyStateHandler()
            win.winHandle.push_handlers(keyState)
            while rating_scale.noResponse:
                if keyState[key._2]:
                    pos -= inc
                elif keyState[key._4]:
                    pos += inc
                if pos > 9.9:
                    pos = 10
                elif pos < 0.1:
                    pos = 0
                probe.setText(trialList_ES[idx]['question'])
                probe.draw()
                rating_scale.setMarkerPos(pos)
                rating_scale.draw()
                win.logOnFlip(level=logging.EXP, msg='experience sampling probe')
                win.flip()
                if flag == 1:
                    probe_onset = clock.getTime()
                    flag = 0
            return probe_onset
        
        def ProbePrint(trialNum, Dim, Quest, SR):
            n_letters = len('intrusiveness')
            n_chars = len('My thoughts were focused on an external task or activity.')
            empty = ' '
            SR = '{:.1f}'.format(SR)
            if n_letters != len(Dim):
                Space1 = n_letters - len(Dim) - 1
            if n_chars != len(Quest):
                Space2 = n_chars - len(Quest) - 1
            if trialNum <= 9:
                if Dim == 'intrusiveness':
                    print('trial', trial_num, ' |', dimension, '|', question, Space2*empty, '|',
		          confirmation_status, SR, '(0-10)')
                elif Dim == 'focus':
                    print('trial', trial_num, ' |', dimension, Space1*empty,'|', question, '|',
		          confirmation_status, SR, '(0-10)')
                else:    
                    print('trial', trial_num, ' |', dimension, Space1*empty, '|', question, Space2*empty, '|',
		          confirmation_status, SR, '(0-10)')                                
            else:
                if Dim == 'intrusiveness':
                    print('trial', trial_num, '|', dimension, '|', question, Space2*empty, '|',
		          confirmation_status, SR, '(0-10)')
                elif Dim == 'focus':
                    print('trial', trial_num, '|', dimension, Space1*empty,'|', question, '|',
		          confirmation_status, SR, '(0-10)')
                else:
                    print('trial', trial_num, '|', dimension, Space1*empty, '|', question, Space2*empty, '|',
		          confirmation_status, SR, '(0-10)')
        
        def SemanticScreen(clock, prime_pos, target_pos, foil1_pos, foil2_pos): 
            prime_im = visual.ImageStim(win, name='stimPic1', image = None, pos=prime_pos)
            tg_im = visual.ImageStim(win, name='stimPic2', image = None, pos=target_pos)
            foil1_im = visual.ImageStim(win, name='stimPic3', image = None, pos=foil1_pos)
            foil2_im = visual.ImageStim(win, name='stimPic4', image = None, pos=foil2_pos)
            prime_im.setImage(Prime)
            tg_im.setImage(Target)
            foil1_im.setImage(Foil1)
            foil2_im.setImage(Foil2)
            prime_im.draw()
            tg_im.draw()
            foil1_im.draw()
            foil2_im.draw()
            win.logOnFlip(level=logging.EXP, msg='semantic screen')
            win.flip()
            SemanticScreen_onset = clock.getTime()
            return SemanticScreen_onset
        
        def SemanticResponse(clock, trialEndTime, stimStart):
            flag = 0
            keyList = []
            keypress = []
            while clock.getTime() < trialEndTime:
                keypress = event.getKeys(keyList=['2','3','4'])
                if len(keypress) == 1 and flag == 0:
                    keyList = keypress[0]
                    flag = 1
                    keyStart = clock.getTime()
            if len(keyList) == 1 and flag == 1:    
                    key_pressed = keyList[0]
                    RT = keyStart - stimStart
            else:
                keyStart = '--'
                key_pressed = 'N/A'
                RT = 'N/A'
            event.clearEvents()
            return keyStart, key_pressed, RT
        
        def SemanticInfo(RT, y_val, target_pos, foil1_pos, foil2_pos, target_name, foil1_name, foil2_name):
            if RT == 'N/A':
                im_position = 'N/A'
                key_ID = 'N/A'
                subChoice = 'N/A'
                accuracy = 0
            elif RT < 2.5:
                if key_pressed == '2':
                    im_position = (-.5, y_val)
                    key_ID = 'left'
                elif key_pressed == '3':
                    im_position = (0, y_val)
                    key_ID = 'center'
                elif key_pressed == '4':
                    im_position = (.5, y_val)
                    key_ID = 'right'
            if im_position == target_pos:
                subChoice = target_name[:-4]
                accuracy = 1
            elif im_position == foil1_pos:
                subChoice = foil1_name[:-4]
                accuracy = 0
            elif im_position == foil2_pos:
                subChoice = foil2_name[:-4]
                accuracy = 0
            if target_pos == (-.5, y_val) and foil1_pos == (0, y_val) and foil2_pos == (.5, y_val):
                left_choice = target_name[:-4]
                center_choice = foil1_name[:-4]
                right_choice = foil2_name[:-4]
            elif target_pos == (-.5, y_val) and foil2_pos == (0, y_val) and foil1_pos == (.5, y_val):
                left_choice = target_name[:-4]
                center_choice = foil2_name[:-4]
                right_choice = foil1_name[:-4]
            elif foil1_pos == (-.5, y_val) and target_pos == (0, y_val) and foil2_pos == (.5, y_val):
                left_choice = foil1_name[:-4]
                center_choice = target_name[:-4]
                right_choice = foil2_name[:-4]
            elif foil1_pos == (-.5, y_val) and foil2_pos == (0, y_val) and target_pos == (.5, y_val):
                left_choice = foil1_name[:-4]
                center_choice = foil2_name[:-4]
                right_choice = target_name[:-4]
            elif foil2_pos == (-.5, y_val) and target_pos == (0, y_val) and foil1_pos == (.5, y_val):
                left_choice = foil2_name[:-4]
                center_choice = target_name[:-4]
                right_choice = foil1_name[:-4]
            elif foil2_pos == (-.5, y_val) and foil1_pos == (0, y_val) and target_pos == (.5, y_val):
                left_choice = foil2_name[:-4]
                center_choice = foil1_name[:-4]
                right_choice = target_name[:-4]
            return key_ID, subChoice, left_choice, center_choice, right_choice, accuracy
        
        # define inter-block flags
        spatial1 = ES1 = eval(expInfo['Block1'])
        qT1 = eval(expInfo['Block2'])
        spatial2 = ES2 = eval(expInfo['Block3'])
        T2star = eval(expInfo['Block4'])
        semantic1 = ES3 = eval(expInfo['Block5'])
        DWI = eval(expInfo['Block6'])
        semantic2 = ES4 = eval(expInfo['Block7'])
        RS = ES5 = eval(expInfo['Block8'])

        # set up main clock & logging features
        mainClock = core.Clock()
        logging.setDefaultClock(mainClock)
        logging.console.setLevel(logging.WARNING)
        
        log_filename = rootLog + '/sub-' +  expInfo['ID'] + '_ses-' + expInfo['session'] + '_' + expInfo['date']
        logFile = logging.LogFile(log_filename + '.log', level=logging.EXP)

        # display window
        win = visual.Window(size=(933.33, 700), color=1, units='height')
        win.mouseVisible = False
        
        # text and fixation features
        sans = ['Arial', 'Gill Sans MT', 'Helvetica', 'Verdana']
        Txt = visual.TextStim(win, name='instruction', text='default text', font=sans, pos=(0, 0),
                              height=float(.04), wrapWidth=1100, color='black')
        fixation = visual.TextStim(win, name='fixation', text='+', font=sans, pos=(0, 0), height=float(.08),
                                   color='black')
	
        ################################### Block 1: Spatial1 #################################################
        
        # create .csv log file for spatial1
        if spatial1:
            task_lab = '_spatial1'
            prevRuns = glob.glob(rootLog + '/*' + task_lab + '*')
            if prevRuns:
                prevRuns.sort()
                numRun = len(prevRuns)
                newRun = str('{:02d}'.format(int(prevRuns[numRun-1][-6:-4]) + 1))
                spa1_csvFile = prevRuns[numRun-1][:-6] + newRun + '.csv'
            else:
                spa1_csvFile = rootLog + '/sub-' + expInfo['ID'] + '_ses-' + expInfo['session'] + task_lab + \
                               '_run-01.csv'
            with open(spa1_csvFile, 'w') as w_spa1:
                writer = csv.writer(w_spa1)
                writer.writerow(['Time', 'Trial_Number', 'Condition', 'Fixation', 'Fixation_Duration', 'Prime',
                                 'Target', 'Foil_1', 'Foil_2', 'Subject_Response', 'Key_pressed', 'Accuracy',
                                 'Reaction_Time'])
        
        # run spatial1 if flag is True
        if spatial1:
            # initialize important task variables
            shuffle(ITI_spa1)
            shuffle(ISI_spa1)
            iters_spa1 = range(0, n_trial_spa1)
            spatial1_trials = list(iters_spa1)
            x_values = [-.5, 0, .5]
            y_val = -.25
            spa1E_acc = []
            spa1E_RT_hit = []
            spa1E_RT_miss = []
            spa1D_acc = []
            spa1D_RT_hit = []
            spa1D_RT_miss = []
        
            # display spatial1 instructions
            Txt.setText(open('spatial/text/instructions.txt', 'r').read())
            Txt.draw()
            win.flip()    
            event.waitKeys(keyList=['2','3','4'])

            # launch scan
            Trigger(mainClock)

            # display block 1 sequence on console
            print('\n\n\n\nBlock 1: Spatial1')
            print(str(datetime.datetime.now()))
            print('---------------------------')
            
            # run spatial1 loop
            for idx in spatial1_trials:

                # set stimuli
                Prime = PIL.Image.open(trialList_spa1[idx]['prime'])
                Target = PIL.Image.open(trialList_spa1[idx]['target'])
                Foil1 = PIL.Image.open(trialList_spa1[idx]['foil1'])
                Foil2 = PIL.Image.open(trialList_spa1[idx]['foil2'])

                # set stimuli positions
                shuffle(x_values)
                tg_x = x_values[0]
                foil1_x = x_values[1]
                foil2_x = x_values[2]

                prime_pos = (0, abs(y_val))
                target_pos = (tg_x, y_val)
                foil1_pos = (foil1_x, y_val)
                foil2_pos = (foil2_x, y_val)

                # record trial number, condition, prime, target, foil1, & foil2
                trial_num = trialList_spa1[idx]['trial_num']
                condition = trialList_spa1[idx]['condition']
                prime_name = os.path.basename(os.path.normpath(trialList_spa1[idx]['prime']))
                target_name = os.path.basename(os.path.normpath(trialList_spa1[idx]['target']))
                foil1_name = os.path.basename(os.path.normpath(trialList_spa1[idx]['foil1']))
                foil2_name = os.path.basename(os.path.normpath(trialList_spa1[idx]['foil2']))
                
                # display ITI fixation cross and record its onset
                ITIStart = FixationCross(mainClock, ITI_spa1, idx)
                
                # display prime and record onset
                primeStart = spatialPrimeScreen(mainClock, prime_pos)
                
                # display ISI fixation cross and record its onset
                ISIStart = FixationCross(mainClock, ISI_spa1, idx)
                
                # display choices and record onset
                choiceStart = spatialChoiceScreen(mainClock, target_pos, foil1_pos, foil2_pos)
                
                # print trial info on console
                if target_pos[0] == -.5:
                    target = 'left'
                elif target_pos[0] == 0:
                    target = 'center'
                elif target_pos[0] == .5:
                    target = 'right'

                if trial_num <= 9:
                    print('trial', trial_num, ' |', condition, '| target: ', target)
                else:
                    print('trial', trial_num, '|', condition, '| target: ', target)
                
                # get subject response info
                trialEndTime = choiceStart + 5.5
                subResp = SpatialResponse(mainClock, trialEndTime, choiceStart)
                keyPressTime = subResp[0]
                key_pressed = subResp[1]
                RT = subResp[2]
                respInfo = SpatialInfo(RT, y_val, target_pos, foil1_pos, foil2_pos, target_name, foil1_name,
                                       foil2_name)
                key_ID = respInfo[0]
                subChoice = respInfo[1]
                left_choice = respInfo[2]
                center_choice = respInfo[3]
                right_choice = respInfo[4]
                accuracy = respInfo[5]
                
                # display subject response info on console
                if accuracy == 1:
                    print('Subject CORRECTLY chose "' + key_ID + '" in ', RT, 'sec')
                    print('\n')
                else:
                    if RT == 'N/A':
                        print('Subject did not respond/was too slow')
                        print('\n')
                    else:
                        print('Subject INCORRECTLY chose "' + key_ID + '" in ', RT, 'sec')
                        print('\n')
                
                # append trial info to accuracy & RT lists
                if condition == 'E':
                    spa1E_acc.append(accuracy)
                    if accuracy == 1:
                        spa1E_RT_hit.append(RT)
                    elif accuracy == 0:
                        if RT != 'N/A':
                            spa1E_RT_miss.append(RT)
                elif condition == 'D':
                    spa1D_acc.append(accuracy)
                    if accuracy == 1:
                        spa1D_RT_hit.append(RT)
                    elif accuracy == 0:
                        if RT != 'N/A':
                            spa1D_RT_miss.append(RT)
                
                # log complete trial info in csv file
                if foil1_pos[0] == -.5:
                    foil1 = 'left'
                elif foil1_pos[0] == 0:
                    foil1 = 'center'
                elif foil1_pos[0] == .5:
                    foil1 = 'right'
                
                if foil2_pos[0] == -.5:
                    foil2 = 'left'
                elif foil2_pos[0] == 0:
                    foil2 = 'center'
                elif foil2_pos[0] == .5:
                    foil2 = 'right'
                
                with open(spa1_csvFile, 'a') as a_spa1:
                    writer = csv.writer(a_spa1)
                    writer.writerow([ITIStart, trial_num, condition, 'ON', primeStart-ITIStart, '--', '--',
                                     '--', '--', '--', '--', '--', '--'])
                    writer.writerow([primeStart, trial_num, condition, 'OFF', '--', prime_name, '--', '--',
                                     '--', '--', '--', '--', '--'])
                    writer.writerow([ISIStart, trial_num, condition, 'ON', choiceStart-ISIStart, '--', '--',
                                     '--', '--', '--', '--', '--', '--'])
                    writer.writerow([choiceStart, trial_num, condition, 'OFF', '--', '--', target, foil1,
                                     foil2, '--', '--', '--', '--'])
                    writer.writerow([keyPressTime, trial_num, condition, 'OFF', '--', '--', '--', '--', '--',
                                     subChoice, key_ID, accuracy, RT])
                    writer.writerow(['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])
            
            # compute scores & display on console
            spa1E_score = (sum(spa1E_acc) / len(spa1E_acc)) * 100
            spa1D_score = (sum(spa1D_acc) / len(spa1D_acc)) * 100
                        
            if spa1E_RT_hit:
                mean_spa1E_RT_hit = sum(spa1E_RT_hit) / len(spa1E_RT_hit)
            else:
                mean_spa1E_RT_hit = 'N/A'
            
            if spa1D_RT_hit:
                mean_spa1D_RT_hit = sum(spa1D_RT_hit) / len(spa1D_RT_hit)
            else:
                mean_spa1D_RT_hit = 'N/A'
            
            if spa1E_RT_miss:
                mean_spa1E_RT_miss = sum(spa1E_RT_miss) / len(spa1E_RT_miss)
            else:
                mean_spa1E_RT_miss = 'N/A'
            
            if spa1D_RT_miss:
                mean_spa1D_RT_miss = sum(spa1D_RT_miss) / len(spa1D_RT_miss)
            else:
                mean_spa1D_RT_miss = 'N/A'
            
            print('spa1E score:          ', spa1E_score, '%')
            print('spa1D score:          ', spa1D_score, '%')
            print('mean spa1E RT (hit):  ', mean_spa1E_RT_hit, 'sec')
            print('mean spa1D RT (hit):  ', mean_spa1D_RT_hit, 'sec')
            print('mean spa1E RT (miss): ', mean_spa1E_RT_miss, 'sec')
            print('mean spa1D RT (miss): ', mean_spa1D_RT_miss, 'sec')

            # display inter-block instruction buffer
            Txt.setText('End of task :)\n\nGet ready for the next sequence!')
            Txt.draw()
            win.flip()    
            core.wait(4)

	    ################################### Block 1 (cont'd): ES1 #############################################
        
        # create .csv log file for experience sampling 1
        if ES1:
            task_lab = '_es1'
            prevRuns = glob.glob(rootLog + '/*' + task_lab + '*')
            if prevRuns:
                prevRuns.sort()
                numRun = len(prevRuns)
                newRun = str('{:02d}'.format(int(prevRuns[numRun-1][-6:-4]) + 1))
                ES1_csvFile = prevRuns[numRun-1][:-6] + newRun + '.csv'
            else:
                ES1_csvFile = rootLog + '/sub-' + expInfo['ID'] + '_ses-' + expInfo['session'] + task_lab + \
		                      '_run-01.csv'          
            with open(ES1_csvFile, 'w') as w_ES1:
                writer = csv.writer(w_ES1)
                writer.writerow(['Time', 'Trial_Number', 'Fixation', 'Fixation_Duration', 'Question',
		                         'Dimension', 'Low_end', 'High_end', 'Subject_Response', 'Reaction_Time'])
        
        # run ES1 if flag is True
        if ES1:
            # initialize important task variables
            shuffle(fix_dur_ES)
            iters_ES = range(0, n_trial_ES)
            ES1_trials = list(iters_ES)
            probe = visual.TextStim(win, color='black', height=.05)

            # display ES1 instructions
            Txt.setText(open('exp_sampling/text/ES_instructions.txt', 'r').read())
            Txt.draw()
            win.flip()    
            event.waitKeys(keyList=['2','3','4'])

            # launch scan
            Trigger(mainClock)

            # display block 1 sequence on console
            print('\nBlock 1 (continued): ES1')
            print(str(datetime.datetime.now()))
            print('---------------------------')

            # randomize trial order
            shuffle(trialList_ES)

            # run ES1 loop
            for idx in ES1_trials:

                # get trial-specific probe labels
                Lab = trialList_ES[idx]['labels']

                # define rating scale parameters
                rating_scale = visual.RatingScale(win, scale=None, low=0, high=10, markerStart=5, leftKeys='2',
		                                          rightKeys='4', acceptKeys='3', labels=Lab,
                                                  tickMarks=['0','10'], tickHeight=1, maxTime=6,
                                                  markerColor='red', textColor='black', textSize=.75,
                                                  stretch=2.5, noMouse=True, lineColor='#3355FF',
                                                  marker='triangle', showValue=False, precision=10,
                                                  showAccept=False, disappear=True)
                
                # record trial number, question, dimension, low/high rates
                trial_num = idx + 1
                question = trialList_ES[idx]['question']
                dimension = trialList_ES[idx]['dimension']
                low_end = trialList_ES[idx]['low_end']
                high_end = trialList_ES[idx]['high_end']

                # display fixation cross and record its onset
                fixStart = FixationCross(mainClock, fix_dur_ES, idx)

                # display probe
                Probe = MindProbe(mainClock, idx)

                # record subject response, reaction time, response time, & confirmation of response status
                SR = rating_scale.getRating()
                RT = rating_scale.getRT()
                respT = Probe + RT
                if RT <= 6:
                    confirmation_status = 'response confirmed:'
                else:
                    confirmation_status = 'response not confirmed:'

                # print trial info on console
                ProbePrint(trial_num, dimension, question, SR)

                # log complete trial info in csv file
                with open(ES1_csvFile, 'a') as a_ES1:
                    writer = csv.writer(a_ES1)
                    writer.writerow([fixStart, trial_num, 'ON', Probe-fixStart, '--', '--', '--', '--', '--',
                                     '--'])
                    writer.writerow([Probe, trial_num, 'OFF', '--', question, dimension, low_end, high_end,
                                     '--', '--'])
                    writer.writerow([respT, trial_num, 'OFF', '--', '--', '--', '--', '--', SR, RT])
                    writer.writerow(['', '', '', '', '', '', '', '', '', ''])

            # display inter-block instruction buffer
            Txt.setText('End of task :)\n\nGet ready for the next sequence!')
            Txt.draw()
            win.flip()
            core.wait(4)

        ################################### Block 2: qT1 ######################################################

        if qT1:
            # display block 2 sequence on console
            print('\n\n\n\nBlock 2: qT1')
            print(str(datetime.datetime.now()))
            print('---------------------------')
            
            # display instructions
            Txt.setText('Scan is in progress.\n\nPlease remain still.')
            Txt.draw()
            win.flip()
            event.waitKeys(keyList=['5'])
    
        ################################### Block 3: Spatial2 #################################################
        
        ################################### Block 3 (cont'd): ES2 #############################################
        
        # create .csv log file for experience sampling 2
        if ES2:
            task_lab = '_es2'
            prevRuns = glob.glob(rootLog + '/*' + task_lab + '*')
            if prevRuns:
                prevRuns.sort()
                numRun = len(prevRuns)
                newRun = str('{:02d}'.format(int(prevRuns[numRun-1][-6:-4]) + 1))
                ES2_csvFile = prevRuns[numRun-1][:-6] + newRun + '.csv'
            else:
                ES2_csvFile = rootLog + '/sub-' + expInfo['ID'] + '_ses-' + expInfo['session'] + task_lab + \
                              '_run-01.csv'
            with open(ES2_csvFile, 'w') as w_ES2:
                writer = csv.writer(w_ES2)
                writer.writerow(['Time', 'Trial_Number', 'Fixation', 'Fixation_Duration', 'Question',
                                 'Dimension', 'Low_end', 'High_end', 'Subject_Response', 'Reaction_Time'])
        
        # run ES2 if flag is True
        if ES2:
            # initialize important task variables
            shuffle(fix_dur_ES)
            iters_ES = range(0, n_trial_ES)
            ES2_trials = list(iters_ES)
            probe = visual.TextStim(win, color='black', height=.05)

            # display ES2 instructions
            Txt.setText(open('exp_sampling/text/ES_instructions.txt', 'r').read())
            Txt.draw()
            win.flip()    
            event.waitKeys(keyList=['2','3','4'])

            # launch scan
            Trigger(mainClock)

            # display block 3 sequence on console
            print('\nBlock 3 (continued): ES2')
            print(str(datetime.datetime.now()))
            print('---------------------------')

            # randomize trial order
            shuffle(trialList_ES)

            # run ES2 loop
            for idx in ES2_trials:

                # get trial-specific probe labels
                Lab = trialList_ES[idx]['labels']

                # define rating scale parameters
                rating_scale = visual.RatingScale(win, scale=None, low=0, high=10, markerStart=5, leftKeys='2',
                                                  rightKeys='4', acceptKeys='3', labels=Lab,
                                                  tickMarks=['0','10'], tickHeight=1, maxTime=6,
                                                  markerColor='red', textColor='black', textSize=.75,
                                                  stretch=2.5, noMouse=True, lineColor='#3355FF',
                                                  marker='triangle', showValue=False, precision=10,
                                                  showAccept=False, disappear=True)

                # record trial number, question, dimension, low/high rates
                trial_num = idx + 1
                question = trialList_ES[idx]['question']
                dimension = trialList_ES[idx]['dimension']
                low_end = trialList_ES[idx]['low_end']
                high_end = trialList_ES[idx]['high_end']

                # display fixation cross and record its onset
                fixStart = FixationCross(mainClock, fix_dur_ES, idx)

                # display probe
                Probe = MindProbe(mainClock, idx)

                # record subject response, reaction time, response time, & confirmation of response status
                SR = rating_scale.getRating()
                RT = rating_scale.getRT()
                respT = Probe + RT
                if RT <= 6:
                    confirmation_status = 'response confirmed:'
                else:
                    confirmation_status = 'response not confirmed:'

                # print trial info on console
                ProbePrint(trial_num, dimension, question, SR)

                # log complete trial info in csv file
                with open(ES2_csvFile, 'a') as a_ES2:
                    writer = csv.writer(a_ES2)
                    writer.writerow([fixStart, trial_num, 'ON', Probe-fixStart, '--', '--', '--', '--', '--',
                                     '--'])
                    writer.writerow([Probe, trial_num, 'OFF', '--', question, dimension, low_end, high_end,
                                     '--', '--'])
                    writer.writerow([respT, trial_num, 'OFF', '--', '--', '--', '--', '--', SR, RT])
                    writer.writerow(['', '', '', '', '', '', '', '', '', ''])

            # display inter-block instruction buffer
            Txt.setText('End of task :)\n\nGet ready for the next sequence!')
            Txt.draw()
            win.flip()
            core.wait(4)

        ################################### Block 4: T2* ######################################################
        
        if T2star:
            # display block 4 sequence on console
            print('\n\n\n\nBlock 4: T2*')
            print(str(datetime.datetime.now()))
            print('---------------------------')
            
            # display instructions
            Txt.setText('Scan is in progress.\n\nPlease remain still.')
            Txt.draw()
            win.flip()
            event.waitKeys(keyList=['5'])
        
        ################################### Block 5: Semantic1 ################################################
	
        # create .csv log file for semantic1
        if semantic1:
            task_lab = '_semantic1'
            prevRuns = glob.glob(rootLog + '/*' + task_lab + '*')
            if prevRuns:
                prevRuns.sort()
                numRun = len(prevRuns)
                newRun = str('{:02d}'.format(int(prevRuns[numRun-1][-6:-4]) + 1))
                sem1_csvFile = prevRuns[numRun-1][:-6] + newRun + '.csv'
            else:
                sem1_csvFile = rootLog + '/sub-' + expInfo['ID'] + '_ses-' + expInfo['session'] + task_lab + \
                               '_run-01.csv'
            with open(sem1_csvFile, 'w') as w_sem1:
                writer = csv.writer(w_sem1)
                writer.writerow(['Time', 'Trial_Number', 'Condition', 'Fixation', 'Fixation_Duration', 'Prime',
                                 'Target', 'Foil_1', 'Foil_2', 'Left_choice', 'Center_choice', 'Right_choice',
                                 'Subject_Response', 'Key_pressed', 'Accuracy', 'Reaction_Time'])
        
        # run semantic1 if flag is True
        if semantic1:
            # initialize important task variables
            shuffle(fix_dur_sem1)
            iters_sem1 = range(0, n_trial_sem1)
            semantic1_trials = list(iters_sem1)
            x_values = [-.5, 0, .5]
            y_val = -.25
            sem1E_acc = []
            sem1E_RT_hit = []
            sem1E_RT_miss = []
            sem1D_acc = []
            sem1D_RT_hit = []
            sem1D_RT_miss = []

            # display semantic1 instructions
            Txt.setText(open('semantic/text/instructions.txt', 'r').read())
            Txt.draw()
            win.flip()    
            event.waitKeys(keyList=['2','3','4'])

            # launch scan
            Trigger(mainClock)

            # display block 5 sequence on console
            print('\n\n\n\nBlock 5: Semantic1')
            print(str(datetime.datetime.now()))
            print('---------------------------')
            
            # run semantic1 loop
            for idx in semantic1_trials:

                # set stimuli
                Prime = PIL.Image.open(trialList_sem1[idx]['prime'])
                Target = PIL.Image.open(trialList_sem1[idx]['target'])
                Foil1 = PIL.Image.open(trialList_sem1[idx]['foil1'])
                Foil2 = PIL.Image.open(trialList_sem1[idx]['foil2'])

                # set stimuli positions
                shuffle(x_values)
                tg_x = x_values[0]
                foil1_x = x_values[1]
                foil2_x = x_values[2]

                prime_pos = (0, abs(y_val))
                target_pos = (tg_x, y_val)
                foil1_pos = (foil1_x, y_val)
                foil2_pos = (foil2_x, y_val)

                # record trial number, condition, prime, target, foil1, & foil2
                trial_num = trialList_sem1[idx]['trial_num']
                condition = trialList_sem1[idx]['condition']
                prime_name = os.path.basename(os.path.normpath(trialList_sem1[idx]['prime']))
                target_name = os.path.basename(os.path.normpath(trialList_sem1[idx]['target']))
                foil1_name = os.path.basename(os.path.normpath(trialList_sem1[idx]['foil1']))
                foil2_name = os.path.basename(os.path.normpath(trialList_sem1[idx]['foil2']))

                # display fixation cross and record its onset
                fixStart = FixationCross(mainClock, fix_dur_sem1, idx)
                
                # print trial info on console
                if trial_num <= 9:
                    print('trial', trial_num, ' |', condition, '| prime:', prime_name[:-4], '| target: ',
			              target_name[:-4], '| foils: ', foil1_name[:-4], ' & ', foil2_name[:-4])
                else:
                    print('trial', trial_num, '|', condition, '| prime:', prime_name[:-4], '| target: ',
			              target_name[:-4], '| foils: ', foil1_name[:-4], ' & ', foil2_name[:-4])
                
                # display stimuli and record onset
                stimStart = SemanticScreen(mainClock, prime_pos, target_pos, foil1_pos, foil2_pos)
                
                # get subject response info
                trialEndTime = stimStart + 2.5
                subResp = SemanticResponse(mainClock, trialEndTime, stimStart)
                keyPressTime = subResp[0]
                key_pressed = subResp[1]
                RT = subResp[2]
                respInfo = SemanticInfo(RT, y_val, target_pos, foil1_pos, foil2_pos, target_name,
                                        foil1_name, foil2_name)
                key_ID = respInfo[0]
                subChoice = respInfo[1]
                left_choice = respInfo[2]
                center_choice = respInfo[3]
                right_choice = respInfo[4]
                accuracy = respInfo[5]
                
                # display subject response info on console
                if accuracy == 1:
                    print('Subject CORRECTLY chose "' + subChoice + '" in ', RT, 'sec')
                    print('\n')
                else:
                    if RT == 'N/A':
                        print('Subject did not respond/was too slow')
                        print('\n')
                    else:
                        print('Subject INCORRECTLY chose "' + subChoice + '" in ', RT, 'sec')
                        print('\n')
                
                # append trial info to accuracy & RT lists
                if condition == 'E':
                    sem1E_acc.append(accuracy)
                    if accuracy == 1:
                        sem1E_RT_hit.append(RT)
                    elif accuracy == 0:
                        if RT != 'N/A':
                            sem1E_RT_miss.append(RT)
                elif condition == 'D':
                    sem1D_acc.append(accuracy)
                    if accuracy == 1:
                        sem1D_RT_hit.append(RT)
                    elif accuracy == 0:
                        if RT != 'N/A':
                            sem1D_RT_miss.append(RT)
                            
                # log complete trial info in csv file
                with open(sem1_csvFile, 'a') as a_sem1:
                    writer = csv.writer(a_sem1)
                    writer.writerow([fixStart, trial_num, condition, 'ON', stimStart-fixStart, '--', '--',
                                     '--', '--', '--', '--', '--', '--', '--', '--', '--'])
                    writer.writerow([stimStart, trial_num, condition, 'OFF', '--', prime_name, target_name,
		                             foil1_name, foil2_name, left_choice, center_choice, right_choice,
                                     '--', '--', '--', '--'])
                    writer.writerow([keyPressTime, trial_num, condition, 'OFF', '--', '--', '--', '--', '--',
				                     '--', '--', '--', subChoice, key_ID, accuracy, '--'])
                    writer.writerow(['--', trial_num, condition, 'OFF', '--', '--', '--', '--', '--', '--',
                                     '--', '--', '--', '--', '--', RT])
                    writer.writerow(['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])
            
            # compute scores & display on console
            sem1E_score = (sum(sem1E_acc) / len(sem1E_acc)) * 100
            sem1D_score = (sum(sem1D_acc) / len(sem1D_acc)) * 100
                        
            if sem1E_RT_hit:
                mean_sem1E_RT_hit = sum(sem1E_RT_hit) / len(sem1E_RT_hit)
            else:
                mean_sem1E_RT_hit = 'N/A'
            
            if sem1D_RT_hit:
                mean_sem1D_RT_hit = sum(sem1D_RT_hit) / len(sem1D_RT_hit)
            else:
                mean_sem1D_RT_hit = 'N/A'
            
            if sem1E_RT_miss:
                mean_sem1E_RT_miss = sum(sem1E_RT_miss) / len(sem1E_RT_miss)
            else:
                mean_sem1E_RT_miss = 'N/A'
            
            if sem1D_RT_miss:
                mean_sem1D_RT_miss = sum(sem1D_RT_miss) / len(sem1D_RT_miss)
            else:
                mean_retD_RT_miss = 'N/A'
            
            print('sem1E score:          ', sem1E_score, '%')
            print('sem1D score:          ', sem1D_score, '%')
            print('mean sem1E RT (hit):  ', mean_sem1E_RT_hit, 'sec')
            print('mean sem1D RT (hit):  ', mean_sem1D_RT_hit, 'sec')
            print('mean sem1E RT (miss): ', mean_sem1E_RT_miss, 'sec')
            print('mean sem1D RT (miss): ', mean_sem1D_RT_miss, 'sec')

            # display inter-block instruction buffer
            Txt.setText('End of task :)\n\nGet ready for the next sequence!')
            Txt.draw()
            win.flip()    
            core.wait(4)
        
        ################################### Block 5 (cont'd): ES3 #############################################
        
        # create .csv log file for experience sampling 3
        if ES3:
            task_lab = '_es3'
            prevRuns = glob.glob(rootLog + '/*' + task_lab + '*')
            if prevRuns:
                prevRuns.sort()
                numRun = len(prevRuns)
                newRun = str('{:02d}'.format(int(prevRuns[numRun-1][-6:-4]) + 1))
                ES3_csvFile = prevRuns[numRun-1][:-6] + newRun + '.csv'
            else:
                ES3_csvFile = rootLog + '/sub-' + expInfo['ID'] + '_ses-' + expInfo['session'] + task_lab + \
                              '_run-01.csv'            
            with open(ES3_csvFile, 'w') as w_ES3:
                writer = csv.writer(w_ES3)
                writer.writerow(['Time', 'Trial_Number', 'Fixation', 'Fixation_Duration', 'Question',
                                 'Dimension', 'Low_end', 'High_end', 'Subject_Response', 'Reaction_Time'])
        
        # run ES3 if flag is True
        if ES3:
            # initialize important task variables
            shuffle(fix_dur_ES)
            iters_ES = range(0, n_trial_ES)
            ES3_trials = list(iters_ES)
            probe = visual.TextStim(win, color='black', height=.05)

            # display ES3 instructions
            Txt.setText(open('exp_sampling/text/ES_instructions.txt', 'r').read())
            Txt.draw()
            win.flip()    
            event.waitKeys(keyList=['2','3','4'])

            # launch scan
            Trigger(mainClock)

            # display block 5 sequence on console
            print('Block 5 (continued): ES3')
            print(str(datetime.datetime.now()))
            print('---------------------------')

            # randomize trial order
            shuffle(trialList_ES)

            # run ES3 loop
            for idx in ES3_trials:

                # get trial-specific probe labels
                Lab = trialList_ES[idx]['labels']

                # define rating scale parameters
                rating_scale = visual.RatingScale(win, scale=None, low=0, high=10, markerStart=5, leftKeys='2',
                                                  rightKeys='4', acceptKeys='3', labels=Lab,
                                                  tickMarks=['0','10'], tickHeight=1, maxTime=6,
                                                  markerColor='red', textColor='black', textSize=.75,
                                                  stretch=2.5, noMouse=True, lineColor='#3355FF',
                                                  marker='triangle', showValue=False, precision=10,
                                                  showAccept=False, disappear=True)
                
                # record trial number, question, dimension, low/high rates
                trial_num = idx + 1
                question = trialList_ES[idx]['question']
                dimension = trialList_ES[idx]['dimension']
                low_end = trialList_ES[idx]['low_end']
                high_end = trialList_ES[idx]['high_end']

                # display fixation cross and record its onset
                fixStart = FixationCross(mainClock, fix_dur_ES, idx)

                # display probe
                Probe = MindProbe(mainClock, idx)

                # record subject response, reaction time, response time, & confirmation of response status
                SR = rating_scale.getRating()
                RT = rating_scale.getRT()
                respT = Probe + RT
                if RT <= 6:
                    confirmation_status = 'response confirmed:'
                else:
                    confirmation_status = 'response not confirmed:'

                # print trial info on console
                ProbePrint(trial_num, dimension, question, SR)

                # log complete trial info in csv file
                with open(ES3_csvFile, 'a') as a_ES3:
                    writer = csv.writer(a_ES3)
                    writer.writerow([fixStart, trial_num, 'ON', Probe-fixStart, '--', '--', '--', '--', '--',
                                     '--'])
                    writer.writerow([Probe, trial_num, 'OFF', '--', question, dimension, low_end, high_end,
                                     '--', '--'])
                    writer.writerow([respT, trial_num, 'OFF', '--', '--', '--', '--', '--', SR, RT])
                    writer.writerow(['', '', '', '', '', '', '', '', '', ''])

            # display inter-block instruction buffer
            Txt.setText('End of task :)\n\nGet ready for the next sequence!')
            Txt.draw()
            win.flip()
            core.wait(4)
        
        ################################### Block 6: DWI ######################################################
        
        if DWI:
            # display block 4 sequence on console
            print('\n\n\n\nBlock 6: DWI')
            print(str(datetime.datetime.now()))
            print('---------------------------')
            
            # display instructions
            Txt.setText('Scan is in progress.\n\nPlease remain still.')
            Txt.draw()
            win.flip()
            event.waitKeys(keyList=['5'])
        
        ################################### Block 7: Semantic2 ################################################
        
        ################################### Block 7 (cont'd): ES4 #############################################
        
        # create .csv log file for experience sampling 4
        if ES4:
            task_lab = '_es4'
            prevRuns = glob.glob(rootLog + '/*' + task_lab + '*')
            if prevRuns:
                prevRuns.sort()
                numRun = len(prevRuns)
                newRun = str('{:02d}'.format(int(prevRuns[numRun-1][-6:-4]) + 1))
                ES4_csvFile = prevRuns[numRun-1][:-6] + newRun + '.csv'
            else:
                ES4_csvFile = rootLog + '/sub-' + expInfo['ID'] + '_ses-' + expInfo['session'] + task_lab + \
                              '_run-01.csv'
            with open(ES4_csvFile, 'w') as w_ES4:
                writer = csv.writer(w_ES4)
                writer.writerow(['Time', 'Trial_Number', 'Fixation', 'Fixation_Duration', 'Question',
                                 'Dimension', 'Low_end', 'High_end', 'Subject_Response', 'Reaction_Time'])
        
        # run ES4 if flag is True
        if ES4:
            # initialize important task variables
            shuffle(fix_dur_ES)
            iters_ES = range(0, n_trial_ES)
            ES4_trials = list(iters_ES)
            probe = visual.TextStim(win, color='black', height=.05)

            # display ES4 instructions
            Txt.setText(open('exp_sampling/text/ES_instructions.txt', 'r').read())
            Txt.draw()
            win.flip()    
            event.waitKeys(keyList=['2','3','4'])

            # launch scan
            Trigger(mainClock)

            # display block 7 sequence on console
            print('Block 7 (continued): ES4')
            print(str(datetime.datetime.now()))
            print('---------------------------')

            # randomize trial order
            shuffle(trialList_ES)

            # run ES4 loop
            for idx in ES4_trials:

                # get trial-specific probe labels
                Lab = trialList_ES[idx]['labels']

                # define rating scale parameters
                rating_scale = visual.RatingScale(win, scale=None, low=0, high=10, markerStart=5, leftKeys='2',
                                                  rightKeys='4', acceptKeys='3', labels=Lab,
                                                  tickMarks=['0','10'], tickHeight=1, maxTime=6,
                                                  markerColor='red', textColor='black', textSize=.75,
                                                  stretch=2.5, noMouse=True, lineColor='#3355FF',
                                                  marker='triangle', showValue=False, precision=10,
                                                  showAccept=False, disappear=True)
                
                # record trial number, question, dimension, low/high rates
                trial_num = idx + 1
                question = trialList_ES[idx]['question']
                dimension = trialList_ES[idx]['dimension']
                low_end = trialList_ES[idx]['low_end']
                high_end = trialList_ES[idx]['high_end']

                # display fixation cross and record its onset
                fixStart = FixationCross(mainClock, fix_dur_ES, idx)

                # display probe
                Probe = MindProbe(mainClock, idx)

                # record subject response, reaction time, response time, & confirmation of response status
                SR = rating_scale.getRating()
                RT = rating_scale.getRT()
                respT = Probe + RT
                if RT <= 6:
                    confirmation_status = 'response confirmed:'
                else:
                    confirmation_status = 'response not confirmed:'

                # print trial info on console
                ProbePrint(trial_num, dimension, question, SR)

                # log complete trial info in csv file
                with open(ES4_csvFile, 'a') as a_ES4:
                    writer = csv.writer(a_ES4)
                    writer.writerow([fixStart, trial_num, 'ON', Probe-fixStart, '--', '--', '--', '--', '--',
                                     '--'])
                    writer.writerow([Probe, trial_num, 'OFF', '--', question, dimension, low_end, high_end,
                                     '--', '--'])
                    writer.writerow([respT, trial_num, 'OFF', '--', '--', '--', '--', '--', SR, RT])
                    writer.writerow(['', '', '', '', '', '', '', '', '', ''])

            # display inter-block instruction buffer
            Txt.setText('End of task :)\n\nGet ready for the next sequence!')
            Txt.draw()
            win.flip()
            core.wait(4)
        
        ################################### Block 8: RS #######################################################
        
        if RS:
            # display block 8 sequence on console
            print('\n\n\n\nBlock 8: RS')
            print(str(datetime.datetime.now()))
            print('---------------------------')
            
            # display RS instructions
            Txt.setText(open('RS/text/RS_instructions.txt', 'r').read())
            Txt.draw()
            win.flip()
            event.waitKeys(keyList=['2','3','4'])
            
            # launch scan
            Trigger(mainClock)
            
            # display RS fixation cross
            RS_FixCross = visual.TextStim(win, name='RS fixation cross', text='+', font=sans, pos=(0, 0),
	                                  height=float(.16), color='gray')
            RS_FixCross.draw()
            win.flip()
            event.waitKeys(keyList=['space']) 
            
            Txt.setText('End of task :)\n\nGet ready for the next sequence!')
            Txt.draw()
            win.flip()
            core.wait(4)
        
        ################################### Block 8 (cont'd): ES5 #############################################
        
        # create .csv log file for experience sampling 5
        if ES5:
            task_lab = '_es5'
            prevRuns = glob.glob(rootLog + '/*' + task_lab + '*')
            if prevRuns:
                prevRuns.sort()
                numRun = len(prevRuns)
                newRun = str('{:02d}'.format(int(prevRuns[numRun-1][-6:-4]) + 1))
                ES5_csvFile = prevRuns[numRun-1][:-6] + newRun + '.csv'
            else:
                ES5_csvFile = rootLog + '/sub-' + expInfo['ID'] + '_ses-' + expInfo['session'] + task_lab + \
                              '_run-01.csv'            
            with open(ES5_csvFile, 'w') as w_ES5:
                writer = csv.writer(w_ES5)
                writer.writerow(['Time', 'Trial_Number', 'Fixation', 'Fixation_Duration', 'Question',
                                 'Dimension', 'Low_end', 'High_end', 'Subject_Response', 'Reaction_Time'])
        
        # run ES5 if flag is True
        if ES5:
            # initialize important task variables
            shuffle(fix_dur_ES)
            iters_ES = range(0, n_trial_ES)
            ES5_trials = list(iters_ES)
            probe = visual.TextStim(win, color='black', height=.05)

            # display ES5 instructions
            Txt.setText(open('exp_sampling/text/ES_instructions.txt', 'r').read())
            Txt.draw()
            win.flip()    
            event.waitKeys(keyList=['2','3','4'])

            # launch scan
            Trigger(mainClock)

            # display block 8 sequence on console
            print('\nBlock 8 (continued): ES5')
            print(str(datetime.datetime.now()))
            print('---------------------------')

            # randomize trial order
            shuffle(trialList_ES)

            # run ES5 loop
            for idx in ES5_trials:

                # get trial-specific probe labels
                Lab = trialList_ES[idx]['labels']

                # define rating scale parameters
                rating_scale = visual.RatingScale(win, scale=None, low=0, high=10, markerStart=5, leftKeys='2',
                                                  rightKeys='4', acceptKeys='3', labels=Lab,
                                                  tickMarks=['0','10'], tickHeight=1, maxTime=6,
                                                  markerColor='red', textColor='black', textSize=.75,
                                                  stretch=2.5, noMouse=True, lineColor='#3355FF',
                                                  marker='triangle', showValue=False, precision=10,
                                                  showAccept=False, disappear=True)
                
                # record trial number, question, dimension, low/high rates
                trial_num = idx + 1
                question = trialList_ES[idx]['question']
                dimension = trialList_ES[idx]['dimension']
                low_end = trialList_ES[idx]['low_end']
                high_end = trialList_ES[idx]['high_end']

                # display fixation cross and record its onset
                fixStart = FixationCross(mainClock, fix_dur_ES, idx)

                # display probe
                Probe = MindProbe(mainClock, idx)

                # record subject response, reaction time, response time, & confirmation of response status
                SR = rating_scale.getRating()
                RT = rating_scale.getRT()
                respT = Probe + RT
                if RT <= 6:
                    confirmation_status = 'response confirmed:'
                else:
                    confirmation_status = 'response not confirmed:'

                # print trial info on console
                ProbePrint(trial_num, dimension, question, SR)

                # log complete trial info in csv file
                with open(ES5_csvFile, 'a') as a_ES5:
                    writer = csv.writer(a_ES5)
                    writer.writerow([fixStart, trial_num, 'ON', Probe-fixStart, '--', '--', '--', '--', '--',
                                     '--'])
                    writer.writerow([Probe, trial_num, 'OFF', '--', question, dimension, low_end, high_end,
                                     '--', '--'])
                    writer.writerow([respT, trial_num, 'OFF', '--', '--', '--', '--', '--', SR, RT])
                    writer.writerow(['', '', '', '', '', '', '', '', '', ''])

            # display inter-block instruction buffer
            Txt.setText('End of protocol.')
            Txt.draw()
            win.flip()
            core.wait(4)

    # ####################################### 1st French protocol ###############################################
    # ###########################################################################################################
    # elif expInfo['language'] == 'French' and expInfo['protocol'] == 'I':
        # print('\n\n\n\n------------------------------------------------------------')
        # print('ID:           ' + expInfo['ID'])
        # print('Session:      ' + expInfo['session']) 
        # print('Language:     ' + expInfo['language'])
        # print('Protocol:     ' + expInfo['protocol'])
        # print('Blocks 1-4:   Encoding 1  -> ES 1.1 -> Encoding 2  -> ES 1.2')
        # print('Blocks 5-8:   0-back 1.1  -> ES 2.1 -> 0-back 1.2  -> ES 2.2')
        # print('Blocks 9-12:  Retrieval 1 -> ES 3.1 -> Retrieval 2 -> ES 3.2')
        # print('Blocks 13-16: MST 1.1     -> ES 4.1 -> MST 1.2     -> ES 4.2')
        # print('Blocks 17-20: 0-back 2.1  -> ES 5.1 -> 0-back 2.2  -> ES 5.2')
        # print('Blocks 21-24: MST 2.1     -> ES 6.1 -> MST 2.2     -> ES 6.2')
        # print('Blocks 25-28: Rest 1.1    -> ES 7.1 -> Rest 1.2    -> ES 7.2')
        # print('Blocks 29-32: Rest 2      -> ES 8')
        # print('------------------------------------------------------------')
        
    # ####################################### 2nd French protocol ###############################################
    # ###########################################################################################################
    # elif expInfo['language'] == 'French' and expInfo['protocol'] == 'II':
        # print('\n\n\n\n----------------------------------------------------')
        # print('ID:         ' + expInfo['ID'])
        # print('Session:    ' + expInfo['session']) 
        # print('Language:   ' + expInfo['language'])
        # print('Protocol:   ' + expInfo['protocol'])
        # print('Blocks 1-4: spatial 1  -> ES 1 -> spatial 1  -> ES 2')
        # print('Blocks 5-8: spatial 2  -> ES 1 -> spatial 2  -> ES 2')
        # print('Blocks 9-?: spatial 3  -> ??????')
        # print('Blocks ??:  semantic 1 -> ES 1 -> semantic 1 -> ES 2')
        # print('Blocks ??:  slef-other -> ES 1 -> self-other -> ES 2')
        # print('Blocks ??:  language   -> ES 1 -> language   -> ES 2')
        # print('Blocks ??:  rest 1     -> ES 1 -> rest 1     -> ES 2')
        # print('Blocks ??:  rest 2     -> ES 1')
        # print('----------------------------------------------------')


if __name__ == '__main__':
    execute()

