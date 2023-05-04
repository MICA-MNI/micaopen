# dependency housekeeping
from rs_dependencies import *

os.system('clear')

# define video directories
currentDir = os.getcwd()

# determine path for VLC binary and videos
path = os.path.normpath(currentDir)
path = path.split(os.sep)

if path[2] == 'neichert':
    clipDir_6min = currentDir + '/videos/6min_clips/'
    clipDir_3min = currentDir + '/videos/3min_clips/'
    VLCBIN = '/Applications/VLC.app/Contents/MacOS/VLC'
elif path[2] == 'percy':
    clipDir_6min = '/data/mica3/7T_task_fMRI/videos/6min_clips/'
    clipDir_3min = '/data/mica3/7T_task_fMRI/videos/3min_clips/'
    VLCBIN = '/usr/bin/vlc'
elif path[2] == 'mica3':
    clipDir_6min = '/data/mica3/7T_task_fMRI/videos/6min_clips/'
    clipDir_3min = '/data/mica3/7T_task_fMRI/videos/3min_clips/'
    VLCBIN = '/usr/bin/vlc'
else:
    clipDir_6min = currentDir + '/videos/6min_clips/'
    clipDir_3min = currentDir + '/videos/3min_clips/'
    print('vlcbin not defined')
    sys.exit()


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
               'Block8': inFile[11][8:-1],
               'Block9': inFile[12][8:]}

    # throw error if no sequence selected
    if  'False' in expInfo['Block1'] and 'False' in expInfo['Block2'] and 'False' in expInfo['Block3'] and \
        'False' in expInfo['Block4'] and 'False' in expInfo['Block5'] and 'False' in expInfo['Block6'] and \
        'False' in expInfo['Block7'] and 'False' in expInfo['Block8'] and 'False' in expInfo['Block9']:
        print('You must select at least one sequence to run')

    else:
        # define scanner trigger function
        def Trigger(clock):
            Txt.setText('waiting for scanner...')
            Txt.draw()
            win.flip()
            event.waitKeys(keyList=['5'])
            clock.reset()

        # define video settings function
        def set_clip(win, clip, win_width):
            video = visual.MovieStim3(win, filename=clip)
            video_width = video.size[0]
            video_height = video.size[1]
            conversion_factor = win_width / video_width
            desired_height = conversion_factor * video_height
            video.size = (win_width, desired_height)
            return video

        ######################################## 3rd English protocol ##############################################
        ############################################################################################################
        if expInfo['language'] == 'English' and expInfo['protocol'] == 'III':
            print('\n\n\n\n-------------------------------------------------------------------------')
            print('ID:           ' + expInfo['ID'])
            print('Session:      ' + expInfo['session'])
            print('Language:     ' + expInfo['language'])
            print('Protocol:     ' + expInfo['protocol'])
            print('Block 1:      action sniper (6min) & experience sampling 1          ' + expInfo['Block1'])
            print('Block 2:      control seedlings (6min) & experience sampling 2      ' + expInfo['Block2'])
            print('Block 3:      action bathroom (3min) & experience sampling 3        ' + expInfo['Block3'])
            print('Block 4:      action caddy (3min) & experience sampling 4           ' + expInfo['Block4'])
            print('Block 5:      control harsh (3min) & experience sampling 5          ' + expInfo['Block5'])
            print('Block 6:      control pines (3min) & experience sampling 6          ' + expInfo['Block6'])
            print('Block 7:      control spring (3min) & experience sampling 7         ' + expInfo['Block7'])
            print('Block 8:      suspense kirsten (3min) & experience sampling 8       ' + expInfo['Block8'])
            print('Block 9:      resting state & experience sampling 9                 ' + expInfo['Block9'])
            print('-------------------------------------------------------------------------')

        # import experience sampling probes
        trialList_ES = data.importConditions('exp_sampling/ES_trials.csv')

        # create list of variable fixation cross durations for ES blocks
        n_trial_ES = len(trialList_ES)
        fix_increment_ES = 1 / (n_trial_ES - 1)
        range_trial_ES = range(0, n_trial_ES)
        fix_dur_ES = [2 + (x * fix_increment_ES) for x in range_trial_ES]

        # create subject-specific directory to keep logs
        rootLog = 'logs/sub-' + expInfo['ID'] + '/ses-' + expInfo['session'] + '/beh'

        if not os.path.isdir(rootLog):
                os.makedirs(rootLog)

        # define functions for ES
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

        # set up main clock & logging features
        mainClock = core.Clock()
        logging.setDefaultClock(mainClock)
        logging.console.setLevel(logging.ERROR)

        log_filename = rootLog + '/sub-' +  expInfo['ID'] + '_ses-' + expInfo['session'] + '_' + expInfo['date']
        logFile = logging.LogFile(log_filename + '.log', level=logging.EXP)

        # display window & get size properties
        win = visual.Window(fullscr=True, color=1, units='height')
        #win = visual.Window(fullscr=False, color=1, units='height')
        win.mouseVisible = False
        win_width = win.size[0]
        win_height = win.size[1]

        # text and fixation features
        sans = ['Arial', 'Gill Sans MT', 'Helvetica', 'Verdana']
        Txt = visual.TextStim(win, name='instruction', text='default text', font=sans, pos=(0, 0),
                              height=float(.04), wrapWidth=1100, color='black')
        fixation = visual.TextStim(win, name='fixation', text='+', font=sans, pos=(0, 0), height=float(.08),
                                   color='black')

        # define inter-block flags
        action_sniper = ES1 = eval(expInfo['Block1'])
        control_seedlings = ES2 = eval(expInfo['Block2'])
        action_bathroom = ES3 = eval(expInfo['Block3'])
        action_caddy = ES4 = eval(expInfo['Block4'])
        control_harsh = ES5 = eval(expInfo['Block5'])
        control_pines = ES6 = eval(expInfo['Block6'])
        control_spring = ES7 = eval(expInfo['Block7'])
        suspense_kirsten = ES8 = eval(expInfo['Block8'])
        RS = ES9 = eval(expInfo['Block9'])

        ######################################## Block 1: Action Sniper (6min) ####################################

        # run action_sniper if flag is True
        if action_sniper:

            # set video clip & fit size to window
            clip = clipDir_6min + 'action_sniper_6min.mp4'
            t_clip = 6*60
            #video = set_clip(win, clip, win_width)

            # launch scan
            Trigger(mainClock)

            # display block 1 sequence on console
            print('\nBlock 1: action sniper (6min)')
            print(str(datetime.datetime.now()))
            print('---------------------------')

            # play video clip
            win.flip()
            proc = subprocess.Popen([f'{VLCBIN} {clip}'], shell=True)
            time.sleep(t_clip)
            proc.terminate()

        ######################################## Block 1 (cont'd): ES1 ############################################

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

        # go back to GUI if no other sequence has been selected, otherwise proceed to next sequence
        if  control_seedlings == ES2 == action_bathroom == ES3 == action_caddy == ES4 == control_harsh == ES5 == \
            control_pines == ES6 == control_spring == ES7 == suspense_kirsten == ES8 == RS == False:
            sys.exit()
        else:
            pass

        ######################################## Block 2: Control Seedlings (6min) ################################

        # run control_seedlings if flag is True
        if control_seedlings:

            # set video clip & fit size to window
            clip = clipDir_6min + 'control_seedlings_6min.mp4'
            #video = set_clip(win, clip, win_width)
            t_clip = 6*60

            # launch scan
            Trigger(mainClock)

            # display block 2 sequence on console
            print('\nBlock 2: control seedlings (6min)')
            print(str(datetime.datetime.now()))
            print('---------------------------')

            # play video clip
            win.flip()
            proc = subprocess.Popen([f'{VLCBIN} {clip}'], shell=True)
            time.sleep(t_clip)
            proc.terminate()

        ######################################## Block 2 (cont'd): ES2 ############################################

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

        # go back to GUI if no other sequence has been selected, otherwise proceed to next sequence
        if  action_bathroom == ES3 == action_caddy == ES4 == control_harsh == ES5 == control_pines == ES6 == \
            control_spring == ES7 == suspense_kirsten == ES8 == RS == False:
            sys.exit()
        else:
            pass

        ######################################## Block 3: Action Bathroom (3min) ##################################

        # run action_bathroom if flag is True
        if action_bathroom:

            # set video clip & fit size to window
            clip = clipDir_3min + 'action_bathroom.mp4'
            #video = set_clip(win, clip, win_width)
            t_clip = 3*60


            # launch scan
            Trigger(mainClock)

            # display block 3 sequence on console
            print('\nBlock 3: action bathroom (3min)')
            print(str(datetime.datetime.now()))
            print('---------------------------')

            # play video clip
            win.flip()
            proc = subprocess.Popen([f'{VLCBIN} {clip}'], shell=True)
            time.sleep(t_clip)
            proc.terminate()

        ######################################## Block 3 (cont'd): ES3 ############################################

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
            print('\nBlock 5 (continued): ES3')
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

        # go back to GUI if no other sequence has been selected, otherwise proceed to next sequence
        if  action_caddy == ES4 == control_harsh == ES5 == control_pines == ES6 == control_spring == ES7 == \
            suspense_kirsten == ES8 == RS == False:
            sys.exit()
        else:
            pass

        ######################################## Block 4: Action Caddy (3min) #####################################

        # run action_caddy if flag is True
        if action_caddy:

            # set video clip & fit size to window
            clip = clipDir_3min + 'action_caddy.mp4'
            #video = set_clip(win, clip, win_width)
            t_clip = 3*60


            # launch scan
            Trigger(mainClock)

            # display block 4 sequence on console
            print('\nBlock 4: action caddy (3min)')
            print(str(datetime.datetime.now()))
            print('---------------------------')

            # play video clip
            win.flip()
            proc = subprocess.Popen([f'{VLCBIN} {clip}'], shell=True)
            time.sleep(t_clip)
            proc.terminate()

        ######################################## Block 4 (cont'd): ES4 ############################################

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
            print('\nBlock 7 (continued): ES4')
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

        # go back to GUI if no other sequence has been selected, otherwise proceed to next sequence
        if  control_harsh == ES5 == control_pines == ES6 == control_spring == ES7 == suspense_kirsten == \
            ES8 == RS == False:
            sys.exit()
        else:
            pass

        ######################################## Block 5: Control Harsh (3min) ####################################

        # run control_harsh if flag is True
        if control_harsh:

            # set video clip & fit size to window
            clip = clipDir_3min + 'control_harsh.mp4'
            #video = set_clip(win, clip, win_width)
            t_clip = 3*60

            # launch scan
            Trigger(mainClock)

            # display block 5 sequence on console
            print('\nBlock 5: control harsh (3min)')
            print(str(datetime.datetime.now()))
            print('---------------------------')

            # play video clip
            win.flip()
            proc = subprocess.Popen([f'{VLCBIN} {clip}'], shell=True)
            time.sleep(t_clip)
            proc.terminate()

        ######################################## Block 5 (cont'd): ES5 ############################################

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
            Txt.setText('End of task :)\n\nGet ready for the next sequence!')
            Txt.draw()
            win.flip()
            core.wait(4)

        # go back to GUI if no other sequence has been selected, otherwise proceed to next sequence
        if  control_pines == ES6 == control_spring == ES7 == suspense_kirsten == ES8 == RS == False:
            sys.exit()
        else:
            pass

        ######################################## Block 6: Control Pines (3min) ####################################

        # run control_pines if flag is True
        if control_pines:

            # set video clip & fit size to window
            clip = clipDir_3min + 'control_pines.mp4'
            #video = set_clip(win, clip, win_width)
            t_clip = 3*60

            # launch scan
            Trigger(mainClock)

            # display block 6 sequence on console
            print('\nBlock 6: control pines (3min)')
            print(str(datetime.datetime.now()))
            print('---------------------------')

            # play video clip
            win.flip()
            proc = subprocess.Popen([f'{VLCBIN} {clip}'], shell=True)
            time.sleep(t_clip)
            proc.terminate()

        ######################################## Block 6 (cont'd): ES6 ############################################

        # create .csv log file for experience sampling 6
        if ES6:
            task_lab = '_es6'
            prevRuns = glob.glob(rootLog + '/*' + task_lab + '*')
            if prevRuns:
                prevRuns.sort()
                numRun = len(prevRuns)
                newRun = str('{:02d}'.format(int(prevRuns[numRun-1][-6:-4]) + 1))
                ES6_csvFile = prevRuns[numRun-1][:-6] + newRun + '.csv'
            else:
                ES6_csvFile = rootLog + '/sub-' + expInfo['ID'] + '_ses-' + expInfo['session'] + task_lab + \
                              '_run-01.csv'
            with open(ES6_csvFile, 'w') as w_ES6:
                writer = csv.writer(w_ES6)
                writer.writerow(['Time', 'Trial_Number', 'Fixation', 'Fixation_Duration', 'Question',
                                 'Dimension', 'Low_end', 'High_end', 'Subject_Response', 'Reaction_Time'])

        # run ES6 if flag is True
        if ES6:
            # initialize important task variables
            shuffle(fix_dur_ES)
            iters_ES = range(0, n_trial_ES)
            ES6_trials = list(iters_ES)
            probe = visual.TextStim(win, color='black', height=.05)

            # display ES6 instructions
            Txt.setText(open('exp_sampling/text/ES_instructions.txt', 'r').read())
            Txt.draw()
            win.flip()
            event.waitKeys(keyList=['2','3','4'])

            # launch scan
            Trigger(mainClock)

            # display block 6 sequence on console
            print('\nBlock 6 (continued): ES6')
            print(str(datetime.datetime.now()))
            print('---------------------------')

            # randomize trial order
            shuffle(trialList_ES)

            # run ES6 loop
            for idx in ES6_trials:

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
                with open(ES6_csvFile, 'a') as a_ES6:
                    writer = csv.writer(a_ES6)
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

        # go back to GUI if no other sequence has been selected, otherwise proceed to next sequence
        if  control_spring == ES7 == suspense_kirsten == ES8 == RS == False:
            sys.exit()
        else:
            pass

        ######################################## Block 7: Control Spring (3min) ###################################

        # run control_spring if flag is True
        if control_spring:

            # set video clip & fit size to window
            clip = clipDir_3min + 'control_spring.mp4'
            #video = set_clip(win, clip, win_width)
            t_clip = 3*60

            # launch scan
            Trigger(mainClock)

            # display block 7 sequence on console
            print('\nBlock 7: control spring (3min)')
            print(str(datetime.datetime.now()))
            print('---------------------------')

            # play video clip
            win.flip()
            proc = subprocess.Popen([f'{VLCBIN} {clip}'], shell=True)
            time.sleep(t_clip)
            proc.terminate()

        ######################################## Block 7 (cont'd): ES7 ############################################

        # create .csv log file for experience sampling 7
        if ES7:
            task_lab = '_es7'
            prevRuns = glob.glob(rootLog + '/*' + task_lab + '*')
            if prevRuns:
                prevRuns.sort()
                numRun = len(prevRuns)
                newRun = str('{:02d}'.format(int(prevRuns[numRun-1][-6:-4]) + 1))
                ES7_csvFile = prevRuns[numRun-1][:-6] + newRun + '.csv'
            else:
                ES7_csvFile = rootLog + '/sub-' + expInfo['ID'] + '_ses-' + expInfo['session'] + task_lab + \
                              '_run-01.csv'
            with open(ES7_csvFile, 'w') as w_ES7:
                writer = csv.writer(w_ES7)
                writer.writerow(['Time', 'Trial_Number', 'Fixation', 'Fixation_Duration', 'Question',
                                 'Dimension', 'Low_end', 'High_end', 'Subject_Response', 'Reaction_Time'])

        # run ES7 if flag is True
        if ES7:
            # initialize important task variables
            shuffle(fix_dur_ES)
            iters_ES = range(0, n_trial_ES)
            ES7_trials = list(iters_ES)
            probe = visual.TextStim(win, color='black', height=.05)

            # display ES7 instructions
            Txt.setText(open('exp_sampling/text/ES_instructions.txt', 'r').read())
            Txt.draw()
            win.flip()
            event.waitKeys(keyList=['2','3','4'])

            # launch scan
            Trigger(mainClock)

            # display block 7 sequence on console
            print('\nBlock 7 (continued): ES7')
            print(str(datetime.datetime.now()))
            print('---------------------------')

            # randomize trial order
            shuffle(trialList_ES)

            # run ES7 loop
            for idx in ES7_trials:

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
                with open(ES7_csvFile, 'a') as a_ES7:
                    writer = csv.writer(a_ES7)
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

        # go back to GUI if no other sequence has been selected, otherwise proceed to next sequence
        if  suspense_kirsten == ES8 == RS == False:
            sys.exit()
        else:
            pass

        ######################################## Block 8: Suspense Kirsten (3min) #################################

        # run control_spring if flag is True
        if suspense_kirsten:

            # set video clip & fit size to window
            clip = clipDir_3min + 'suspense_kirsten_gets_hit.mp4'
            #video = set_clip(win, clip, win_width)
            t_clip = 3*60

            # launch scan
            Trigger(mainClock)

            # display block 8 sequence on console
            print('\nBlock 8: suspense kirsten (3min)')
            print(str(datetime.datetime.now()))
            print('---------------------------')

            win.flip()
            proc = subprocess.Popen([f'{VLCBIN} {clip}'], shell=True)
            time.sleep(t_clip)
            proc.terminate()

        ######################################## Block 8 (cont'd): ES8 ############################################

        # create .csv log file for experience sampling 8
        if ES8:
            task_lab = '_es8'
            prevRuns = glob.glob(rootLog + '/*' + task_lab + '*')
            if prevRuns:
                prevRuns.sort()
                numRun = len(prevRuns)
                newRun = str('{:02d}'.format(int(prevRuns[numRun-1][-6:-4]) + 1))
                ES8_csvFile = prevRuns[numRun-1][:-6] + newRun + '.csv'
            else:
                ES8_csvFile = rootLog + '/sub-' + expInfo['ID'] + '_ses-' + expInfo['session'] + task_lab + \
                              '_run-01.csv'
            with open(ES8_csvFile, 'w') as w_ES8:
                writer = csv.writer(w_ES8)
                writer.writerow(['Time', 'Trial_Number', 'Fixation', 'Fixation_Duration', 'Question',
                                 'Dimension', 'Low_end', 'High_end', 'Subject_Response', 'Reaction_Time'])

        # run ES8 if flag is True
        if ES8:
            # initialize important task variables
            shuffle(fix_dur_ES)
            iters_ES = range(0, n_trial_ES)
            ES8_trials = list(iters_ES)
            probe = visual.TextStim(win, color='black', height=.05)

            # display ES8 instructions
            Txt.setText(open('exp_sampling/text/ES_instructions.txt', 'r').read())
            Txt.draw()
            win.flip()
            event.waitKeys(keyList=['2','3','4'])

            # launch scan
            Trigger(mainClock)

            # display block 8 sequence on console
            print('\nBlock 8 (continued): ES8')
            print(str(datetime.datetime.now()))
            print('---------------------------')

            # randomize trial order
            shuffle(trialList_ES)

            # run ES8 loop
            for idx in ES8_trials:

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
                with open(ES8_csvFile, 'a') as a_ES8:
                    writer = csv.writer(a_ES8)
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

        # go back to GUI if final sequence has not been selected, otherwise proceed to final sequence
        if RS == False:
            sys.exit()
        else:
            pass

        ################################### Block 9: RS #######################################################

        # create .csv log file for experience sampling 9
        if RS:
            # display block 9 sequence on console
            print('\n\n\n\nBlock 9: RS')
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

        ################################### Block 9 (cont'd): ES9 #############################################

        # create .csv log file for experience sampling 9
        if ES9:
            task_lab = '_es9'
            prevRuns = glob.glob(rootLog + '/*' + task_lab + '*')
            if prevRuns:
                prevRuns.sort()
                numRun = len(prevRuns)
                newRun = str('{:02d}'.format(int(prevRuns[numRun - 1][-6:-4]) + 1))
                ES9_csvFile = prevRuns[numRun - 1][:-6] + newRun + '.csv'
            else:
                ES9_csvFile = rootLog + '/sub-' + expInfo['ID'] + '_ses-' + expInfo['session'] + task_lab + \
                              '_run-01.csv'
            with open(ES9_csvFile, 'w') as w_ES9:
                writer = csv.writer(w_ES9)
                writer.writerow(['Time', 'Trial_Number', 'Fixation', 'Fixation_Duration', 'Question',
                                 'Dimension', 'Low_end', 'High_end', 'Subject_Response', 'Reaction_Time'])

        # run ES9 if flag is True
        if ES9:
            # initialize important task variables
            shuffle(fix_dur_ES)
            iters_ES = range(0, n_trial_ES)
            ES9_trials = list(iters_ES)
            probe = visual.TextStim(win, color='black', height=.05)

            # display ES9 instructions
            Txt.setText(open('exp_sampling/text/ES_instructions.txt', 'r').read())
            Txt.draw()
            win.flip()
            event.waitKeys(keyList=['2', '3', '4'])

            # launch scan
            Trigger(mainClock)

            # display block 9 sequence on console
            print('\nBlock 9 (continued): ES9')
            print(str(datetime.datetime.now()))
            print('---------------------------')

            # randomize trial order
            shuffle(trialList_ES)

            # run ES9 loop
            for idx in ES9_trials:

                # get trial-specific probe labels
                Lab = trialList_ES[idx]['labels']

                # define rating scale parameters
                rating_scale = visual.RatingScale(win, scale=None, low=0, high=10, markerStart=5, leftKeys='2',
                                                  rightKeys='4', acceptKeys='3', labels=Lab,
                                                  tickMarks=['0', '10'], tickHeight=1, maxTime=6,
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
                with open(ES9_csvFile, 'a') as a_ES9:
                    writer = csv.writer(a_ES9)
                    writer.writerow([fixStart, trial_num, 'ON', Probe - fixStart, '--', '--', '--', '--', '--',
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

        # end of English protocol III
        sys.exit()

if __name__ == '__main__':
    execute()

############### FIN ###############
