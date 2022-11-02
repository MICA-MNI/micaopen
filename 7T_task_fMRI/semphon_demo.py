# dependency housekeeping
from task_dependencies import *

warnings.filterwarnings(action='ignore')


# run paradigm
def execute():

    # define scanner trigger function
    def Trigger(clock):
        Txt.setText('waiting for scanner...')
        Txt.draw()
        win.flip()
        event.waitKeys(keyList=['5'])
        clock.reset()

    # semphon settings
    words_Ho = pd.read_excel('semphon/stimuli/stimuli.xlsx', 'Homophones_demo')
    words_Sy = pd.read_excel('semphon/stimuli/stimuli.xlsx', 'Synonyms_demo')
    words_Vi = pd.read_excel('semphon/stimuli/stimuli.xlsx', 'Visually_demo')

    conditions = np.array([['A1', 'B1', 'C1', 'D'],
                           ['C1', 'A1', 'B1', 'D']])

    # how many trials within one condition
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
    # 'yes' key
    key_code_L = '2'
    # 'no' key
    key_code_R = '4'

    def mergelists(wordlist):
        y = wordlist[['Y_1', 'Y_2']].rename(columns={"Y_1": "first", "Y_2": "second"}).dropna().reset_index(drop=True)
        y['is_correct'] = 1
        n = wordlist[['N_1', 'N_2']].rename(columns={"N_1": "first", "N_2": "second"}).dropna().reset_index(drop=True)
        n['is_correct'] = 0
        mylist = pd.concat([y, n])
        mylist = mylist.sample(frac=1)
        return mylist

    word_lists_Ho = mergelists(words_Ho)
    word_lists_Sy = mergelists(words_Sy)
    word_lists_Vi = mergelists(words_Vi)

    def semphon_task():
        # how many big blocks, i.e. repeats of all conditions
        n_big_blocks = conditions.shape[0]
        # how many sub blocks, i.e. conditions including rest
        n_sub_blocks = conditions.shape[1]
        # start clock counting from experiment start
        time_start_exp = clock.getTime()
        # master trial count
        trial_number_tot = 0
        # loop over big blocks (repeat all conditions with different order)
        for i_big_block in range(0, n_big_blocks):
            # loop over sub_blocks (will go through all conditions including rest)
            for i_sub_block in range(0, n_sub_blocks):
                # -------------------------- start condition block --------------------
                time_start_block = clock.getTime()
                condition = conditions[i_big_block, i_sub_block]

                # select context: first 4 sub_blocks select column 0, then column 1
                # note that it loops from 0 to 9
                if 'A' in condition:
                    words = word_lists_Ho
                    condition_instruction = "Do the words SOUND the same?"
                elif 'B' in condition:
                    words = word_lists_Sy
                    condition_instruction = "Do the words MEAN the same?"
                elif 'C' in condition:
                    words = word_lists_Vi
                    condition_instruction = "Do the words LOOK the same?"
                elif condition == 'D':
                    condition_instruction = "Rest"

                # display condition_instruction
                condition_text = visual.TextStim(win, text=condition_instruction, font=sans, pos=(0, 0),
                                                 height=float(.08), color='black')

                condition_text.draw()
                win.update()
                time_elapsed = 0

                # wait until t_instruction has passed
                while time_elapsed < (t_instruction):
                    time_elapsed = clock.getTime() - time_start_block

                # loop over trials
                if condition != 'D':
                    for i_trial in range(0, n_trials):
                        time_start_trial = clock.getTime()
                        trial_number_tot = trial_number_tot + 1
                        word1 = words.iloc[i_trial]['first']
                        word2 = words.iloc[i_trial]['second']
                        expected_answer = words.iloc[i_trial]['is_correct']

                        word1_text = visual.TextStim(win, text=word1, font=sans, pos=(0, float(.1)),
                                                     height=float(.08), color='black')

                        word2_text = visual.TextStim(win, text=word2, font=sans, pos=(0, -float(.1)),
                                                     height=float(.08), color='black')

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

                        t_start_RT = clock.getTime()
                        given_answer = np.nan
                        key_list = []
                        RT = np.nan
                        awaiting_response = 1
                        time_elapsed = 0
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
                                    sys.exit()
                                else:
                                    given_answer = np.nan
                                    RT = np.nan

                            time_elapsed = clock.getTime() - t_start_RT

                        core.wait(t_trial - (clock.getTime() - time_start_trial))

                # rest-block
                else:
                    onsettime = clock.getTime() - time_start_exp
                    fixation.draw()
                    win.update()
                    core.wait(t_rest_block)
                    # show blank screen
                    win.update()


    win = visual.Window(fullscr=False, color=1, units='height')
    win.mouseVisible = False

    # text and fixation features
    sans = ['Arial', 'Gill Sans MT', 'Helvetica', 'Verdana']
    Txt = visual.TextStim(win, name='instruction', text='default text', font=sans, pos=(0, 0),
                          height=float(.04), wrapWidth=1100, color='black')
    fixation = visual.TextStim(win, name='fixation', text='+', font=sans, pos=(0, 0), height=float(.08),
                               color='black')

    ################################### Block 1: Semphon1  ################################################
    # create .csv log file for encoding

    # display encoding instructions
    Txt.setText(open('semphon/text/task_instructions.txt', 'r').read())
    Txt.draw()
    win.flip()
    event.waitKeys(keyList=['2', '3', '4'])
    mainClock = core.Clock()

    # launch scan
    Trigger(mainClock)

    # display block 1 sequence on console
    print('\n\n\n\nBlock 1: Semphon')
    print(str(datetime.datetime.now()))
    print('---------------------------')
    semphon_task()

    # display inter-block instruction buffer
    Txt.setText('End of demo!')
    Txt.draw()
    win.flip()
    core.wait(4)
    sys.exit()


if __name__ == '__main__':
    execute()