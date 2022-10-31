# dependency housekeeping
from task_dependencies import *

warnings.filterwarnings(action='ignore')


# run paradigm
def execute():
    # get GUI-generated info from tmp.txt file
    with open('tmp.txt') as f:
        inFile = f.readlines()

    # general info
    expInfo = {'ID': inFile[0][10:-1], 'session': inFile[1][10:-1], 'language': inFile[2][10:-1],
               'protocol': inFile[3][10:-1], 'list': 'A', 'date': data.getDateStr(), 'Block1': inFile[4][8:-1],
               'Block2': inFile[5][8:-1], 'Block3': inFile[6][8:-1], 'Block4': inFile[7][8:-1],
               'Block5': inFile[8][8:-1], 'Block6': inFile[9][8:-1], 'Block7': inFile[10][8:-1],
               'Block8': inFile[11][8:]}

    # delete tmp.txt file
    # os.remove('tmp.txt')

    # throw error if no sequence selected
    if 'False' in expInfo['Block1'] and 'False' in expInfo['Block2'] and 'False' in expInfo['Block3'] and 'False' in \
            expInfo['Block4'] and 'False' in expInfo['Block5'] and 'False' in expInfo['Block6'] and 'False' in expInfo[
        'Block7'] and 'False' in expInfo['Block8']:
        print('You must select at least one sequence to run')

    else:
        # define scanner trigger function
        def Trigger(clock):
            Txt.setText('waiting for scanner...')
            Txt.draw()
            win.flip()
            event.waitKeys(keyList=['5'])
            clock.reset()

        ####################################### 1st English protocol ##############################################
        ###########################################################################################################
        if expInfo['language'] == 'English' and expInfo['protocol'] == 'IV':
            print('\n\n\n\n-------------------------------------------------------------------------')
            print('ID:           ' + expInfo['ID'])
            print('Session:      ' + expInfo['session'])
            print('Language:     ' + expInfo['language'])
            print('Protocol:     ' + expInfo['protocol'])
            print('Block 1:      semphon1 & experience sampling 1                      ' + expInfo['Block1'])
            print('Block 2:      quantitative T1-mapping                               ' + expInfo['Block2'])
            print('Block 3:      semphon2 & experience sampling 2                      ' + expInfo['Block3'])
            print('Block 4:      T2*-weighted imaging                                  ' + expInfo['Block4'])
            print('Block 5:      audiobook1 & experience sampling 3    ' + expInfo['Block5'])
            print('Block 6:      diffusion-weighted imaging                            ' + expInfo['Block6'])
            print('Block 7:      audiobook2 & experience sampling 4    ' + expInfo['Block7'])
            print('Block 8:      resting state & experience sampling 5                 ' + expInfo['Block8'])
            print('-------------------------------------------------------------------------')

            # import stimuli for each block
            trialList_ES = data.importConditions('exp_sampling/ES_trials.csv')
            words_Ho = pd.read_excel('semphon/stimuli/stimuli.xlsx', 'Homophones')
            words_Sy = pd.read_excel('semphon/stimuli/stimuli.xlsx', 'Synonyms')
            words_Vi = pd.read_excel('semphon/stimuli/stimuli.xlsx', 'Visually')

            n_trial_ES = len(trialList_ES)
            fix_increment_ES = 1 / (n_trial_ES - 1)
            range_trial_ES = range(0, n_trial_ES)
            fix_dur_ES = [2 + (x * fix_increment_ES) for x in range_trial_ES]

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
                    sys.exit()
                event.clearEvents()
                return fixation_onset

            def MindProbe(clock, idx):
                flag = 1
                inc = 0.1
                pos = rating_scale.markerStart
                keyState = key.KeyStateHandler()
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
                        print('trial', trial_num, ' |', dimension, '|', question, Space2 * empty, '|',
                              confirmation_status, SR, '(0-10)')
                    elif Dim == 'focus':
                        print('trial', trial_num, ' |', dimension, Space1 * empty, '|', question, '|',
                              confirmation_status, SR, '(0-10)')
                    else:
                        print('trial', trial_num, ' |', dimension, Space1 * empty, '|', question, Space2 * empty, '|',
                              confirmation_status, SR, '(0-10)')
                else:
                    if Dim == 'intrusiveness':
                        print('trial', trial_num, '|', dimension, '|', question, Space2 * empty, '|',
                              confirmation_status, SR, '(0-10)')
                    elif Dim == 'focus':
                        print('trial', trial_num, '|', dimension, Space1 * empty, '|', question, '|',
                              confirmation_status, SR, '(0-10)')
                    else:
                        print('trial', trial_num, '|', dimension, Space1 * empty, '|', question, Space2 * empty, '|',
                              confirmation_status, SR, '(0-10)')

            # define inter-block flags
            semphon1 = ES1 = eval(expInfo['Block1'])
            qT1 = eval(expInfo['Block2'])
            semphon2 = ES2 = eval(expInfo['Block3'])
            T2star = eval(expInfo['Block4'])
            AB1 = ES3 = eval(expInfo['Block5'])
            DWI = eval(expInfo['Block6'])
            AB2 = ES4 = eval(expInfo['Block7'])
            RS = ES5 = eval(expInfo['Block8'])

            # set up main clock & logging features
            mainClock = core.Clock()
            logging.setDefaultClock(mainClock)
            logging.console.setLevel(logging.ERROR)

            log_filename = rootLog + '/sub-' + expInfo['ID'] + '_ses-' + expInfo['session'] + '_' + expInfo['date']
            logFile = logging.LogFile(log_filename + '.csv', level=logging.EXP)

            # display window
            win = visual.Window(fullscr=True, color=1, units='height')
            win.mouseVisible = False

            # text and fixation features
            sans = ['Arial', 'Gill Sans MT', 'Helvetica', 'Verdana']
            Txt = visual.TextStim(win, name='instruction', text='default text', font=sans, pos=(0, 0),
                                  height=float(.04), wrapWidth=1100, color='black')
            fixation = visual.TextStim(win, name='fixation', text='+', font=sans, pos=(0, 0), height=float(.08),
                                       color='black')

            ################################### Block 1: Semphon1  ################################################
            # create .csv log file for encoding
            if semphon1:
                task_lab = '_sp1'
                prevRuns = glob.glob(rootLog + '/*' + task_lab + '*')
                if prevRuns:
                    prevRuns.sort()
                    numRun = len(prevRuns)
                    newRun = str('{:02d}'.format(int(prevRuns[numRun - 1][-6:-4]) + 1))
                    sp1_tsvFile = prevRuns[numRun - 1][:-6] + newRun + '.tsv'
                else:
                    sp1_tsvFile = rootLog + '/sub-' + expInfo['ID'] + '_ses-' + expInfo[
                        'session'] + task_lab + '_run-01.tsv'
                sp1_enc = open(sp1_tsvFile, 'a')
                writer = csv.writer(sp1_enc, delimiter='\t', lineterminator='\n')
                writer.writerow(
                    ['Onset', 'Trial_Duration', 'Trial_Number', 'Condition', 'RT', 'Stimulus_1', 'Stimulus_2', 'Expected_answer', 'Given_answer'])

                # display encoding instructions
                Txt.setText(open('semphon/text/task_instructions.txt', 'r').read())
                Txt.draw()
                win.flip()
                event.waitKeys(keyList=['2', '3', '4'])

                # launch scan
                Trigger(mainClock)

                # display block 1 sequence on console
                print('\n\n\n\nBlock 1: Semphon')
                print(str(datetime.datetime.now()))
                print('---------------------------')

                ##--- Nicole section start ---###

                # latin square to determine order of conditions
                # rows: diffent big_block, column: different sub_block (i.e. condition)
                conditions = np.array([['A', 'B', 'C', 'D'],
                                       ['C', 'A', 'B', 'D'],
                                       ['B', 'C', 'A', 'D'],
                                       ['A', 'B', 'C', 'D']])

                # how many big blocks, i.e. repeats of all conditions
                n_big_blocks = conditions.shape[0]
                # how many sub blocks, i.e. conditions including rest
                n_sub_blocks = conditions.shape[1]
                # how many trials whithin one condition
                n_trials = 10

                # time for instruction for condition on screen
                t_instruction = 3
                # time for fixation cross
                t_fixation = 0.5
                # time words shown
                t_words = 0.5
                # time for pause between trials (clear screen), awaiting response
                t_blank = 2
                # extra gap time
                t_gap = 0.15
                # time for one trial
                t_trial = t_fixation + t_words + t_blank

                # time for resting block
                t_rest_block = n_trials * t_trial

                # percentage of correct trials
                p_correct = 0.5
                n_correct = int(np.floor(n_trials * p_correct))
                rand_correct = np.zeros(n_trials)
                rand_correct[0:n_correct] = 1

                # yes key
                key_code_L = '2'
                # no key
                key_code_R = '4'

                # randomization of trial list
                whole_list = np.arange(1, 25)
                shuffle(whole_list)
                A_list = whole_list[0: n_trials]
                B_list = whole_list[n_trials: n_trials * 2]

                # start clock counting from experiment start
                time_start_exp = clock.getTime()

                # master trial count
                trial_number_tot = 0
                # loop over big blocks (repeat all conditions with different order)
                for i_big_block in range(0, n_big_blocks):

                    # loop over sub_blocks (will go through all conditions including rest)
                    for i_sub_block in range(0, n_sub_blocks):

                        # -------------------------- start condition block --------------------
                        condition = conditions[i_big_block, i_sub_block]

                        # get time of condition block and write to log file
                        time_start_block = clock.getTime()

                        # select context: first 4 sub_blocks select column 0, then column 1
                        # note that it loops from 0 to 9
                        if condition == 'A':
                            words = words_Ho
                            condition_instruction = "Do the words sound the same?"
                        elif condition == 'B':
                            words = words_Sy
                            condition_instruction = "Do the words have the same meaning?"
                        elif condition == 'C':
                            words = words_Vi
                            condition_instruction = "Are the two letter strings the same?"
                        elif condition == 'D':
                            condition_instruction = "Rest"

                        # randomization of correct and incorrect
                        # rand_correct = np.random.permutation(np.repeat(np.array([1, 0]), round(n_trials / 2.)))
                        shuffle(rand_correct)

                        # initialize counter for trials
                        count_trial = 1

                        # display condition_instruction
                        condition_text = visual.TextStim(win, text=condition_instruction, font=sans, pos=(0, 0), height=float(.08),
                                       color='black')

                        condition_text.draw()
                        win.update()
                        time_elapsed = 0

                        # wait until t_instruction has passed
                        while time_elapsed < (t_instruction):
                            time_elapsed = clock.getTime() - time_start_block

                        # loop over trials
                        if condition != 'D':
                            for i_trial in range(0, n_trials):
                                trial_number_tot = trial_number_tot + 1

                                # get time for start of trial
                                time_start_trial = clock.getTime()

                                if i_big_block == 0:
                                    ind_trial = A_list[i_trial]
                                elif i_big_block == 1:
                                    ind_trial = A_list[i_trial] + 25
                                elif i_big_block == 2:
                                    ind_trial = B_list[i_trial]
                                elif i_big_block == 3:
                                    ind_trial = B_list[i_trial] + 25

                                is_correct = rand_correct[i_trial]

                                if is_correct:
                                    word1 = words.Y_1[ind_trial - 1]
                                    word2 = words.Y_2[ind_trial - 1]
                                elif is_correct == 0:
                                    word1 = words.N_1[ind_trial - 1]
                                    word2 = words.N_2[ind_trial - 1]

                                word1_text = visual.TextStim(win, text=word1, font=sans, pos=(0, float(.1)), height=float(.08),
                                       color='black')

                                word2_text = visual.TextStim(win, text=word2, font=sans, pos=(0, -float(.1)), height=float(.08),
                                       color='black')

                                fixation = visual.TextStim(win=win, text="+", height=float(.08), color='black')

                                # show fixation cross
                                onsettime = clock.getTime() - time_start_exp
                                fixation.draw()
                                win.update()
                                core.wait(t_fixation)

                                # show words
                                word1_text.draw()
                                word2_text.draw()
                                fixation.draw()
                                win.update()
                                core.wait(t_words)
                                # show blank screen
                                win.update()
                                given_answer = np.nan
                                key_list = []
                                RT = np.nan
                                awaiting_response = 1
                                time_elapsed = 0
                                t_start_RT = clock.getTime()

                                # clear events key press buffer so that any key can be captured
                                event.clearEvents()

                                while time_elapsed < (t_blank - t_gap):
                                    # Capture for first response only
                                    if awaiting_response:
                                        keys_list = event.getKeys()
                                        if any(key_code_L in key for key in keys_list):
                                            given_answer = int(1)
                                            awaiting_response = 0
                                            RT = clock.getTime() - t_start_RT
                                        elif any(key_code_R in key for key in keys_list):
                                            given_answer = int(0)
                                            awaiting_response = 0
                                            RT = clock.getTime() - t_start_RT
                                        # check if escape key has been pressed during the fixation period
                                        elif any("escape" in key for key in keys_list):
                                            # Esc has been pressed
                                            time_stop = clock.getTime()
                                            # write down note in logfile
                                            #writer.writerow(
                                            #    ["", round((time_stop - time_start_exp), 2), "stopped by escape key"])
                                            # close experiment
                                            #logfile.close()
                                            #win.close()
                                            #core.quit()
                                            sys.exit()
                                        else:
                                            given_answer = np.nan
                                            RT = np.nan

                                    time_elapsed = clock.getTime() - t_start_RT

                                writer.writerow(
                                    [onsettime, t_trial, trial_number_tot, condition, RT, word1,
                                     word2, int(is_correct), given_answer])
                        # rest-block
                        else:
                            onsettime = clock.getTime() - time_start_exp
                            fixation.draw()
                            win.update()
                            core.wait(t_rest_block)
                            # show blank screen
                            win.update()
                            writer.writerow(
                                [onsettime, t_rest_block, '-', condition, '-', '-', '-', '-', '-'])



                ##--- Nicole section stop ---###

                # log complete trial info in csv file
                # TODO log

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
                    newRun = str('{:02d}'.format(int(prevRuns[numRun - 1][-6:-4]) + 1))
                    ES1_csvFile = prevRuns[numRun - 1][:-6] + newRun + '.csv'
                else:
                    ES1_csvFile = rootLog + '/sub-' + expInfo['ID'] + '_ses-' + expInfo[
                        'session'] + task_lab + '_run-01.csv'
                with open(ES1_csvFile, 'w') as w_ES1:
                    writer = csv.writer(w_ES1)
                    writer.writerow(
                        ['Time', 'Trial_Number', 'Fixation', 'Fixation_Duration', 'Question', 'Dimension', 'Low_end',
                         'High_end', 'Subject_Response', 'Reaction_Time'])

                # initialize important task variables
                shuffle(fix_dur_ES)
                iters_ES = range(0, n_trial_ES)
                ES1_trials = list(iters_ES)
                probe = visual.TextStim(win, color='black', height=.05)

                # display ES1 instructions
                Txt.setText(open('exp_sampling/text/ES_instructions.txt', 'r').read())
                Txt.draw()
                win.flip()
                event.waitKeys(keyList=['2', '3', '4'])

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
                                                      rightKeys='4', acceptKeys='3', labels=Lab, tickMarks=['0', '10'],
                                                      tickHeight=1, maxTime=6, markerColor='red', textColor='black',
                                                      textSize=.75, stretch=2.5, noMouse=True, lineColor='#3355FF',
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
                        writer.writerow(
                            [fixStart, trial_num, 'ON', Probe - fixStart, '--', '--', '--', '--', '--', '--'])
                        writer.writerow(
                            [Probe, trial_num, 'OFF', '--', question, dimension, low_end, high_end, '--', '--'])
                        writer.writerow([respT, trial_num, 'OFF', '--', '--', '--', '--', '--', SR, RT])
                        writer.writerow(['', '', '', '', '', '', '', '', '', ''])

                # display inter-block instruction buffer
                Txt.setText('End of task :)\n\nGet ready for the next sequence!')
                Txt.draw()
                win.flip()
                core.wait(4)

            # go back to GUI if no other sequence has been selected, otherwise proceed to next sequence
            if qT1 == semphon2 == T2star == AB1 == DWI == AB2 == RS == False:
                sys.exit()
            else:
                pass

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
                event.waitKeys(keyList=['escape'])

            # go back to GUI if no other sequence has been selected, otherwise proceed to next sequence
            if semphon2 == T2star == AB1 == DWI == AB2 == RS == False:
                sys.exit()
            else:
                pass

            ################################### Block 3: Retrieval  ###############################################

            # create .csv log file for retrieval
            if semphon2:
                task_lab = '_sp2'
                prevRuns = glob.glob(rootLog + '/*' + task_lab + '*')
                if prevRuns:
                    prevRuns.sort()
                    numRun = len(prevRuns)
                    newRun = str('{:02d}'.format(int(prevRuns[numRun - 1][-6:-4]) + 1))
                    ret_csvFile = prevRuns[numRun - 1][:-6] + newRun + '.csv'
                else:
                    ret_csvFile = rootLog + '/sub-' + expInfo['ID'] + '_ses-' + expInfo[
                        'session'] + task_lab + '_run-01.tsv'
                with open(ret_csvFile, 'w') as w_ret:
                    writer = csv.writer(w_ret)
                    writer.writerow(
                        ['Time', 'Trial_Number', 'Condition', 'Fixation', 'Fixation_Duration', 'Prime', 'Target',
                         'Foil_1', 'Foil_2', 'Left_choice', 'Center_choice', 'Right_choice', 'Subject_Response',
                         'Key_pressed', 'Accuracy', 'Reaction_Time'])


                # display retrieval instructions
                Txt.setText(open('semphon/text/task_instructions.txt', 'r').read())
                Txt.draw()
                win.flip()
                event.waitKeys(keyList=['2', '3', '4'])

                # launch scan
                Trigger(mainClock)

                # display block 3 sequence on console
                print('\n\n\n\nBlock 3: Semphon')
                print(str(datetime.datetime.now()))
                print('---------------------------')

                # TODO semphon2

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
                    newRun = str('{:02d}'.format(int(prevRuns[numRun - 1][-6:-4]) + 1))
                    ES2_csvFile = prevRuns[numRun - 1][:-6] + newRun + '.csv'
                else:
                    ES2_csvFile = rootLog + '/sub-' + expInfo['ID'] + '_ses-' + expInfo[
                        'session'] + task_lab + '_run-01.csv'
                with open(ES2_csvFile, 'w') as w_ES2:
                    writer = csv.writer(w_ES2)
                    writer.writerow(
                        ['Time', 'Trial_Number', 'Fixation', 'Fixation_Duration', 'Question', 'Dimension', 'Low_end',
                         'High_end', 'Subject_Response', 'Reaction_Time'])

                # initialize important task variables
                shuffle(fix_dur_ES)
                iters_ES = range(0, n_trial_ES)
                ES2_trials = list(iters_ES)
                probe = visual.TextStim(win, color='black', height=.05)

                # display ES2 instructions
                Txt.setText(open('exp_sampling/text/ES_instructions.txt', 'r').read())
                Txt.draw()
                win.flip()
                event.waitKeys(keyList=['2', '3', '4'])

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
                                                      rightKeys='4', acceptKeys='3', labels=Lab, tickMarks=['0', '10'],
                                                      tickHeight=1, maxTime=6, markerColor='red', textColor='black',
                                                      textSize=.75, stretch=2.5, noMouse=True, lineColor='#3355FF',
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
                        writer.writerow(
                            [fixStart, trial_num, 'ON', Probe - fixStart, '--', '--', '--', '--', '--', '--'])
                        writer.writerow(
                            [Probe, trial_num, 'OFF', '--', question, dimension, low_end, high_end, '--', '--'])
                        writer.writerow([respT, trial_num, 'OFF', '--', '--', '--', '--', '--', SR, RT])
                        writer.writerow(['', '', '', '', '', '', '', '', '', ''])

                # display inter-block instruction buffer
                Txt.setText('End of task :)\n\nGet ready for the next sequence!')
                Txt.draw()
                win.flip()
                core.wait(4)

            # go back to GUI if no other sequence has been selected, otherwise proceed to next sequence
            if T2star == AB1 == DWI == AB2 == RS == False:
                sys.exit()
            else:
                pass

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
                event.waitKeys(keyList=['escape'])

            # go back to GUI if no other sequence has been selected, otherwise proceed to next sequence
            if AB1 == DWI == AB2 == RS == False:
                sys.exit()
            else:
                pass

            ################################### Block 5: AB1 #####################################################

            # create .csv log file for AB1
            if AB1:
                task_lab = '_ab1'


                # display block 5 sequence on console
                print('\n\n\n\nBlock 5: AB1')
                print(str(datetime.datetime.now()))
                print('---------------------------')

                #TODO: Audiobook 1

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
                    newRun = str('{:02d}'.format(int(prevRuns[numRun - 1][-6:-4]) + 1))
                    ES3_csvFile = prevRuns[numRun - 1][:-6] + newRun + '.csv'
                else:
                    ES3_csvFile = rootLog + '/sub-' + expInfo['ID'] + '_ses-' + expInfo[
                        'session'] + task_lab + '_run-01.csv'
                with open(ES3_csvFile, 'w') as w_ES3:
                    writer = csv.writer(w_ES3)
                    writer.writerow(
                        ['Time', 'Trial_Number', 'Fixation', 'Fixation_Duration', 'Question', 'Dimension', 'Low_end',
                         'High_end', 'Subject_Response', 'Reaction_Time'])

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
                event.waitKeys(keyList=['2', '3', '4'])

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
                                                      rightKeys='4', acceptKeys='3', labels=Lab, tickMarks=['0', '10'],
                                                      tickHeight=1, maxTime=6, markerColor='red', textColor='black',
                                                      textSize=.75, stretch=2.5, noMouse=True, lineColor='#3355FF',
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
                        writer.writerow(
                            [fixStart, trial_num, 'ON', Probe - fixStart, '--', '--', '--', '--', '--', '--'])
                        writer.writerow(
                            [Probe, trial_num, 'OFF', '--', question, dimension, low_end, high_end, '--', '--'])
                        writer.writerow([respT, trial_num, 'OFF', '--', '--', '--', '--', '--', SR, RT])
                        writer.writerow(['', '', '', '', '', '', '', '', '', ''])

                # display inter-block instruction buffer
                Txt.setText('End of task :)\n\nGet ready for the next sequence!')
                Txt.draw()
                win.flip()
                core.wait(4)

            # go back to GUI if no other sequence has been selected, otherwise proceed to next sequence
            if DWI == AB2 == RS == False:
                sys.exit()
            else:
                pass

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
                event.waitKeys(keyList=['escape'])

            # go back to GUI if no other sequence has been selected, otherwise proceed to next sequence
            if AB2 == RS == False:
                sys.exit()
            else:
                pass

            ################################### Block 7: AB2 #####################################################
            if AB2:

                # launch scan
                Trigger(mainClock)

                # display block 7 sequence on console
                print('\n\n\n\nBlock 7: MST2')
                print(str(datetime.datetime.now()))
                print('---------------------------')

               # TODO: Audiobook2


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
                    newRun = str('{:02d}'.format(int(prevRuns[numRun - 1][-6:-4]) + 1))
                    ES4_csvFile = prevRuns[numRun - 1][:-6] + newRun + '.csv'
                else:
                    ES4_csvFile = rootLog + '/sub-' + expInfo['ID'] + '_ses-' + expInfo[
                        'session'] + task_lab + '_run-01.csv'
                with open(ES4_csvFile, 'w') as w_ES4:
                    writer = csv.writer(w_ES4)
                    writer.writerow(
                        ['Time', 'Trial_Number', 'Fixation', 'Fixation_Duration', 'Question', 'Dimension', 'Low_end',
                         'High_end', 'Subject_Response', 'Reaction_Time'])

                # initialize important task variables
                shuffle(fix_dur_ES)
                iters_ES = range(0, n_trial_ES)
                ES4_trials = list(iters_ES)
                probe = visual.TextStim(win, color='black', height=.05)

                # display ES4 instructions
                Txt.setText(open('exp_sampling/text/ES_instructions.txt', 'r').read())
                Txt.draw()
                win.flip()
                event.waitKeys(keyList=['2', '3', '4'])

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
                                                      rightKeys='4', acceptKeys='3', labels=Lab, tickMarks=['0', '10'],
                                                      tickHeight=1, maxTime=6, markerColor='red', textColor='black',
                                                      textSize=.75, stretch=2.5, noMouse=True, lineColor='#3355FF',
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
                        writer.writerow(
                            [fixStart, trial_num, 'ON', Probe - fixStart, '--', '--', '--', '--', '--', '--'])
                        writer.writerow(
                            [Probe, trial_num, 'OFF', '--', question, dimension, low_end, high_end, '--', '--'])
                        writer.writerow([respT, trial_num, 'OFF', '--', '--', '--', '--', '--', SR, RT])
                        writer.writerow(['', '', '', '', '', '', '', '', '', ''])

                # display inter-block instruction buffer
                Txt.setText('End of task :)\n\nGet ready for the next sequence!')
                Txt.draw()
                win.flip()
                core.wait(4)

            # go back to GUI if final sequence has not been selected, otherwise proceed to final sequence
            if RS == False:
                sys.exit()
            else:
                pass

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
                event.waitKeys(keyList=['2', '3', '4'])

                # launch scan
                Trigger(mainClock)

                # display RS fixation cross
                RS_FixCross = visual.TextStim(win, name='RS fixation cross', text='+', font=sans, pos=(0, 0),
                                              height=float(.16), color='gray')
                RS_FixCross.draw()
                win.flip()

                # get onset time of gray fixation cross
                fixOn = mainClock.getTime()

                # display fixation for six minutes
                RS_scanDur = 360
                fixDur = fixOn + RS_scanDur
                core.wait(fixDur)
                # event.waitKeys(keyList=['escape'])

                # display end of task screen
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
                    newRun = str('{:02d}'.format(int(prevRuns[numRun - 1][-6:-4]) + 1))
                    ES5_csvFile = prevRuns[numRun - 1][:-6] + newRun + '.csv'
                else:
                    ES5_csvFile = rootLog + '/sub-' + expInfo['ID'] + '_ses-' + expInfo[
                        'session'] + task_lab + '_run-01.csv'
                with open(ES5_csvFile, 'w') as w_ES5:
                    writer = csv.writer(w_ES5)
                    writer.writerow(
                        ['Time', 'Trial_Number', 'Fixation', 'Fixation_Duration', 'Question', 'Dimension', 'Low_end',
                         'High_end', 'Subject_Response', 'Reaction_Time'])

                # initialize important task variables
                shuffle(fix_dur_ES)
                iters_ES = range(0, n_trial_ES)
                ES5_trials = list(iters_ES)
                probe = visual.TextStim(win, color='black', height=.05)

                # display ES5 instructions
                Txt.setText(open('exp_sampling/text/ES_instructions.txt', 'r').read())
                Txt.draw()
                win.flip()
                event.waitKeys(keyList=['2', '3', '4'])

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
                                                      rightKeys='4', acceptKeys='3', labels=Lab, tickMarks=['0', '10'],
                                                      tickHeight=1, maxTime=6, markerColor='red', textColor='black',
                                                      textSize=.75, stretch=2.5, noMouse=True, lineColor='#3355FF',
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
                        writer.writerow(
                            [fixStart, trial_num, 'ON', Probe - fixStart, '--', '--', '--', '--', '--', '--'])
                        writer.writerow(
                            [Probe, trial_num, 'OFF', '--', question, dimension, low_end, high_end, '--', '--'])
                        writer.writerow([respT, trial_num, 'OFF', '--', '--', '--', '--', '--', SR, RT])
                        writer.writerow(['', '', '', '', '', '', '', '', '', ''])

                # display inter-block instruction buffer
                Txt.setText('End of protocol.')
                Txt.draw()
                win.flip()
                core.wait(4)

            # end of English protocol I
            sys.exit()


if __name__ == '__main__':
    execute()
