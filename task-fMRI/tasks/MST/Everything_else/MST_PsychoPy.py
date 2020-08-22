#!/usr/bin/env python2
from __future__ import print_function, division

""" 
Mnemonic Similarity Task in PsychoPy

Copyright 2017, Craig Stark

Forked from v0.95 of the C++ version of MST on July 28, 2017

8/9/17: First solidly-working version

1/7/18: Shifted from inaccurate da to d' measures in 2-choice output metrics
        Self-paced mode added
        Instructions now stay up all the time the image is up

"""

"""
TBD:
- Touch box responses

"""

import numpy as np
import csv
import os
from psychopy import visual, core, data, tools, event
from psychopy import gui
from datetime import datetime
from scipy.stats import norm

def get_parameters(skip_gui=False):
    # Setup my global parameters
    try:#try to get a previous parameters file 
        param_settings = tools.filetools.fromFile('lastParams.pickle')
    except:
        param_settings = [1234,2.0,0.5,'Phase 1','1','1VC','2B','3NM',False,False,32,1,-1]
    #print(param_settings)    
    if not skip_gui:
        param_dialog = gui.Dlg('Experimental parameters')
        param_dialog.addField('ID',param_settings[0],tip='Must be numeric only')
        param_dialog.addField('Duration',param_settings[1])
        param_dialog.addField('ISI',param_settings[2])
        param_dialog.addField('Phase', choices=['Phase 1','Phase 2'],initial=param_settings[3])
        param_dialog.addField('Set', choices=['1','2','3','4','5','6','C','D','E','F','ScC'],initial=param_settings[4])
        param_dialog.addField('Resp 1 keys',param_settings[5])
        param_dialog.addField('Resp 2 keys',param_settings[6])
        param_dialog.addField('Resp 3 keys',param_settings[7])
        param_dialog.addField('Self-Paced', initial=param_settings[8])
        param_dialog.addField('Two-Choice', initial=param_settings[9])
        param_dialog.addField('NStim per set', choices=[20,32,40,64],initial=param_settings[10])
        param_dialog.addField('sublist',choices=[1,2,3],initial=param_settings[11]-1)  # It's treating this one like an index
        param_dialog.addField('Randomization',param_settings[12],tip='-1=Use ID, 0=Use time, >0 = Use specific seed')
        param_settings=param_dialog.show()
        #print(ok_data)
        if param_dialog.OK:
            tools.filetools.toFile('lastParams.pickle', param_settings)
            params = {'ID': param_settings[0],
                  'Duration': param_settings[1],
                  'ISI':param_settings[2],
                  'Phase': param_settings[3],
                  'Set': param_settings[4],
                  'Resp1Keys':param_settings[5],
                  'Resp2Keys':param_settings[6],
                  'Resp3Keys':param_settings[7],
                  'SelfPaced': param_settings[8],
                  'TwoChoice': param_settings[9],
                  'NStimPerSet': param_settings[10],
                  'sublist':param_settings[11],
                  'Randomization':param_settings[12] }
        else:
            core.quit()
    else:
        params = {'ID': param_settings[0],
          'Duration': param_settings[1],
          'ISI':param_settings[2],
          'Phase': param_settings[3],
          'Set': param_settings[4],
          'Resp1Keys':param_settings[5],
          'Resp2Keys':param_settings[6],
          'Resp3Keys':param_settings[7],
          'SelfPaced': param_settings[8],
          'TwoChoice': param_settings[9],
          'NStimPerSet': param_settings[10],
          'sublist':param_settings[11],
          'Randomization':param_settings[12] }
 
    return params


  
def check_files(SetName):
    """ 
    SetName should be something like "C" or "1"
    Checks to make sure there are the right #of images in the image directory
    Loads the lure bin ratings into the global set_bins list and returns this
    """
    import glob
    import os

    #print(SetName)
    #print(P_N_STIM_PER_LIST)
    
    bins = []  # Clear out any existing items in the bin list
    
    # Load the bin file
    with open("Set"+str(SetName)+" bins.txt","rb") as bin_file:
        reader=csv.reader(bin_file,delimiter='\t')
        for row in reader:
            if int(row[0]) > 192:
                raise ValueError('Stimulus number ({0}) too large - not in 1-192 in binfile'.format(row[0]))
            if int(row[0]) < 1:
                raise ValueError('Stimulus number ({0}) too small - not in 1-192 in binfile'.format(row[0]))
            bins.append(int(row[1]))
    if len(bins) != 192:
        raise ValueError('Did not read correct number of bins in binfile')
    
    # Check the stimulus directory
    img_list=glob.glob("Set " +str(SetName) + os.sep + '*.jpg')
    if len(img_list) < 384:
        raise ValueError('Not enough files in stimulus directory {0}'.format("Set " +str(SetName) + os.sep + '*.jpg'))
    for i in range(1,193):
        if not os.path.isfile("Set " +str(SetName) + os.sep + '{0:03}'.format(i) + 'a.jpg'):
            raise ValueError('Cannot find: ' + "Set " +str(SetName) + os.sep + '{0:03}'.format(i) + 'a.jpg')
        if not os.path.isfile("Set " +str(SetName) + os.sep + '{0:03}'.format(i) + 'b.jpg'):
            raise ValueError('Cannot find: ' + "Set " +str(SetName) + os.sep + '{0:03}'.format(i) + 'b.jpg')
    return bins

            
def setup_list_permuted(set_bins,set_size=64,sublist=0):
    """
    set_bins = list of bin values for each of the 192 stimuli -- set specific
    
    Assumes check_files() has been run so we have the bin numbers for each stimulus

    Returns lists with the image numbers for each stimulus type (study, repeat...)
    in the to-be-used permuted order with the to-be-used list size

    """

    
    if len(set_bins) != 192:
        raise ValueError('Set bin length is not the same as the stimulus set length (192)')

    
    # Figure the image numbers for the lure bins
    lure1=np.where(set_bins == 1)[0] + 1
    lure2=np.where(set_bins == 2)[0] + 1
    lure3=np.where(set_bins == 3)[0] + 1
    lure4=np.where(set_bins == 4)[0] + 1
    lure5=np.where(set_bins == 5)[0] + 1
    
    # Permute these
    lure1 = np.random.permutation(lure1)
    lure2 = np.random.permutation(lure2)
    lure3 = np.random.permutation(lure3)
    lure4 = np.random.permutation(lure4)
    lure5 = np.random.permutation(lure5)
    
    lures = np.empty(64,dtype=int)
    # Make the Lure list to go L1, 2, 3, 4, 5, 1, 2 ... -- 64 total of them (max)
    lure_count = np.zeros(5,dtype=int)
    nonlures = np.arange(1,193,dtype=int)
    for i in range(64):  
        if i % 5 == 0:
            lures[i]=lure1[lure_count[0]]
            lure_count[0]+=1
        elif i % 5 == 1:
            lures[i]=lure2[lure_count[1]]
            lure_count[1]+=1
        elif i % 5 == 2:
            lures[i]=lure3[lure_count[2]]
            lure_count[2]+=1
        elif i % 5 == 3:
            lures[i]=lure4[lure_count[3]]
            lure_count[3]+=1
        elif i % 5 == 4:
            lures[i]=lure5[lure_count[4]]
            lure_count[4]+=1
        nonlures=np.delete(nonlures,np.argwhere(nonlures == lures[i]))
            
    # Randomize the non-lures and split into 64-length repeat and foils
    nonlures=np.random.permutation(nonlures)
    foils = nonlures[0:64]
    repeats = nonlures[64:128]
           
    # At this point, we're full 64-item length lists for everything -- need to
    # break these down into sublists starting at the right point
    if set_size == 32:
        if sublist == 1:
            repeatstim=repeats[0:32]
            lurestim=lures[0:32]
            foilstim=foils[0:32]
        else:
            repeatstim=repeats[32:64]
            lurestim=lures[32:64]
            foilstim=foils[32:64]
    elif set_size == 20:
        if sublist == 1:
            repeatstim=repeats[0:20]
            lurestim=lures[0:20]
            foilstim=foils[0:20]
        elif sublist == 2:
            repeatstim=repeats[20:40]
            lurestim=lures[20:40]
            foilstim=foils[20:40]
        else:
            repeatstim=repeats[40:60]
            lurestim=lures[40:60]
            foilstim=foils[40:60]
    elif set_size == 40:
        repeatstim=repeats[0:40]
        lurestim=lures[0:40]
        foilstim=foils[0:40]
    else:  # Full 64 by default
        repeatstim = repeats
        lurestim=lures
        foilstim=foils
    
    # Our lures are still in L1, 2, 3, 4, 5, 1, 2, ... order -- fix that
    lurestim=np.random.permutation(lurestim)
            
    
    return (repeatstim,lurestim,foilstim)
    

def create_order(p_set, repeatstim, lurestim, foilstim):
    """
    p_set = Set we're using (e.g., '1', or 'C')
    repeatstim,lurestim,foilstim: Lists (np.arrays actually) created by setup_list_permuted
    
    Returns lists with the filenames and conditions for each trial in both the
    study and test phases
        
    """
    n_per = len(repeatstim)
    # Do the study phase - easy as we already have the list and it's still
    # setup with the first half being the to-be-repeated and the 2nd half
    # being the to-be-lured stimuli
    # Create the study list - note the first half are the to-be-repeated and
    # the second half are the to-be-lured at this point
    study_stim = np.concatenate((repeatstim,lurestim)) 
    # Set up a condition list to reflect this
    study_cond = ['SR']*n_per
    study_cond[n_per:2*n_per] = ['SL']*n_per
    study_cond=np.array(study_cond)  # Make it an np-array so we can index easiy
    order = np.random.permutation(n_per*2)
    study_cond = list(study_cond[order])
    study_list=[]
    for i in range(0,n_per*2):
        study_list.append('Set {0}{1}{2:03}a.jpg'.format(p_set, os.sep, study_stim[order[i]]))
    

    # Do the test phase in a similar way 
    test_stim = np.concatenate((repeatstim,lurestim,foilstim)) 
    test_cond=['TR']*n_per
    test_cond[n_per:2*n_per] = ['TL']*n_per
    test_cond[2*n_per:3*n_per] = ['TF']*n_per
    test_cond=np.array(test_cond)  # Make it an np-array so we can index easiy
    order = np.random.permutation(n_per*3)
    test_cond = list(test_cond[order])
    test_list=[]
    for i in range(0,n_per*3):
        if test_cond[i] == 'TL':  # Use the 'b' version only for the lures
            test_list.append('Set {0}{1}{2:03}b.jpg'.format(p_set,os.sep,test_stim[order[i]]))
        else:
            test_list.append('Set {0}{1}{2:03}a.jpg'.format(p_set,os.sep,test_stim[order[i]]))
        
        
    return (study_list,study_cond,test_list,test_cond)

def decode_response(params,response):
    if params['Resp1Keys'].lower().find(response.lower()) >= 0:
        respcode = 1
    elif params['Resp2Keys'].lower().find(response.lower()) >= 0:
        respcode = 2
    elif params['Resp3Keys'].lower().find(response.lower()) >= 0:
        respcode = 3
    elif response == '5':  # Scanner trigger
        respcode = 99
    elif response in ['escape','esc']:
        respcode = -1
    return respcode
    

def show_study(params,study_list,study_cond,set_bins):
    """ Shows the study phase """
    global log
    global win
    

    instructions1=visual.TextStim(win,text="Indoor or Outdoor?",pos=(0,0.9),
        color=(-1,-1,-1),wrapWidth=1.75,alignHoriz='center',alignVert='center')
    instructions2=visual.TextStim(win,text="Press the spacebar to begin",pos=(0,-0.25),
        color=(-0.5,-0.5,-0.5),wrapWidth=1.75,alignHoriz='center',alignVert='center')
    
    instructions1.draw()
    instructions2.draw()
    win.flip()
    key = event.waitKeys(keyList=['space','5','esc','escape'])
    if key and key[0] in ['escape','esc']:
        print('Escape hit - bailing')
        return -1
    
    log.write('Study phase started at {0}\n'.format(str(datetime.now())))
    log.write('Trial,Stim,Cond,StartT,Resp,RT\n')

    
    local_timer = core.MonotonicClock()
    duration = params['Duration']
    isi = params['ISI']
    log.flush()
    valid_keys = list(params['Resp1Keys'].lower()) + list(params['Resp2Keys'].lower()) + list(params['Resp3Keys'].lower()) + ['esc','escape']
    for trial in range(len(study_list)):
        if params['SelfPaced']:
            t1=local_timer.getTime()
        else:
            t1 = trial * (duration + isi)  # Time when this trial should have started
        log.write('{0},{1},{2},{3:.3f},'.format(trial+1,study_list[trial],study_cond[trial],local_timer.getTime()))
        log.flush()
        image = visual.ImageStim(win, image=study_list[trial])
        image.draw()
        instructions1.draw()
        win.flip()
        RT=0
        key = event.waitKeys(duration,keyList=valid_keys)  # Wait our normal duration
        if key and key[0] in ['escape','esc']:
            log.write('\nEscape key aborted experiment\n')
            print('Escape hit - bailing')
            return -1
        elif key:
            RT=local_timer.getTime() - t1
            core.wait(t1 + duration - local_timer.getTime()) # Wait the remainder of the trial
        win.flip() # Clear the screen for the ISI
        if params['SelfPaced'] and (RT < 0.05):  # Continue waiting until we get something
            key = event.waitKeys(keyList=valid_keys)
            RT=local_timer.getTime() - t1
        if params['SelfPaced']:
            core.wait(isi)
        else:  # Do the ISI locking to the clock cleaning and allow a response in it if we don't have one
            while local_timer.getTime() < (t1 + duration + isi):
                if (RT < 0.05):
                    key = event.getKeys(keyList=valid_keys)
                    if key:
                        RT=local_timer.getTime() - t1
        if RT > 0.05: # We have a response
            log.write('{0},{1:.3f}\n'.format(decode_response(params,key[0]),RT))
        else:
            log.write('NA\n')
    return 0
        

def show_test(params,test_list,test_cond,set_bins):
    global log, win
    
    if params['TwoChoice']==True:
        instructions1=visual.TextStim(win,text="Old or New?",pos=(0,0.9),
            color=(-1,-1,-1),wrapWidth=1.75,alignHoriz='center',alignVert='center')
    else:
        instructions1=visual.TextStim(win,text="Old, Similar, or New?",pos=(0,0.9),
            color=(-1,-1,-1),wrapWidth=1.75,alignHoriz='center',alignVert='center')
    
    instructions2=visual.TextStim(win,text="Press the spacebar to begin",pos=(0,-0.25),
        color=(-0.5,-0.5,-0.5),wrapWidth=1.75,alignHoriz='center',alignVert='center')
    
    instructions1.draw()
    instructions2.draw()
    win.flip()
    key = event.waitKeys(keyList=['space','5','esc','escape'])
    if key and key[0] in ['escape','esc']:
        print('Escape  hit - bailing')
        return -1
    TLF_trials = np.zeros(3)  # Number of trials of each type we have a response to
    TLF_response_matrix = np.zeros((3,3))  # Rows = O,(S),N  Cols = T,L,R
    lure_bin_matrix = np.zeros((4,5)) # Rows: O,S,N,NR  Cols=Lure bins
    
    log.write('Test phase started at {0}\n'.format(str(datetime.now())))
    log.write('Trial,Stim,Cond,LBin,StartT,Resp,RT,Corr\n')
    local_timer = core.MonotonicClock()
    duration = params['Duration']
    isi = params['ISI']
    ncorrect = 0
    log.flush()
    valid_keys = list(params['Resp1Keys'].lower()) + list(params['Resp2Keys'].lower()) + list(params['Resp3Keys'].lower()) + ['esc','escape']
    for trial in range(len(test_list)):
        if params['SelfPaced']:
            t1=local_timer.getTime()
        else:
            t1 = trial * (duration + isi)  # Time when this trial should have started
        stim_path = test_list[trial]
        stim_number = int(stim_path[-8:-5])
        log.write('{0},{1},{2},{3},{4:.3f},'.format(trial+1,test_list[trial],test_cond[trial],set_bins[stim_number-1],local_timer.getTime()))
        log.flush()
        image = visual.ImageStim(win, image=test_list[trial])
        image.draw()
        instructions1.draw()
        win.flip()
        response = 0
        correct = 0
        RT = 0
        key = event.waitKeys(duration,keyList=valid_keys)  # Wait our normal duration
        if key and key[0] in ['escape','esc']:
            print('Escape hit - bailing')
            log.write('\nEscape key aborted experiment\n')
            return -1
        elif key:
            RT=local_timer.getTime() - t1
            core.wait(t1 + duration - local_timer.getTime()) # Wait the remainder of the trial
        win.flip() # Clear the screen for the ISI
        if params['SelfPaced'] and (RT < 0.05):  # Continue waiting until we get something
            key = event.waitKeys(keyList=valid_keys)
            RT=local_timer.getTime() - t1
        if params['SelfPaced']:
            core.wait(isi)
        else:  # Do the ISI locking to the clock cleaning and allow a response in it if we don't have one
            while local_timer.getTime() < (t1 + duration + isi):
                if (RT < 0.05):
                    key = event.getKeys(keyList=valid_keys)
                    if key:
                        RT=local_timer.getTime() - t1
        if RT > 0.05: # We have a response
            response = decode_response(params,key[0])
            if test_cond[trial]=='TR':  # Increment the appropriate trial type counter (for count of # they responded to)
                TLF_trials[0] += 1
                trial_type = 1
            elif test_cond[trial]=='TL':
                TLF_trials[1] += 1
                trial_type = 2
            elif test_cond[trial]=='TF':
                TLF_trials[2] += 1
                trial_type = 3
            TLF_response_matrix[response-1,trial_type-1] += 1  # Increment the response x type  matrix as needed
            if params['TwoChoice']==True:  # Old/new variant
                if trial_type == 1 and response == 1:  # Hit
                    correct=1
                elif trial_type == 2 and response == 2:  #Lure-CR
                    correct=1
                elif trial_type == 3 and response == 2:  #CR
                    correct=1
            else:  #Old/similar/new variant
                if trial_type == 1 and response == 1:  # Hit
                    correct=1
                elif trial_type == 2 and response == 2:  #Lure-Similar
                    correct=1
                elif trial_type == 3 and response == 3:  #CR
                    correct=1
            log.write('{0},{1},{2:.3f}\n'.format(response,correct,RT))
        else:
            log.write('NA\n')
        if test_cond[trial] == 'TL':  # Take care of the lure-bin details
            bin_index = set_bins[stim_number-1] - 1  # Make it 0-indexed
            resp_index = response - 1  # Make this 0-indexed
            if resp_index == -1:
                resp_index = 3  # Loop the no-responses into the 4th entry here
            lure_bin_matrix[resp_index,bin_index] += 1
        ncorrect += correct
    # Print some summary stats to the log file
    log.write('\nValid responses:\nTargets, {0:d}\nlures, {1:d}\nfoils, {2:d}'.format(TLF_trials[0],TLF_trials[1],TLF_trials[2]))
    log.write('\nCorrected rates\n')
    log.write('\nRateMatrix,Targ,Lure,Foil\n')
    # Fix up any no-response cell here so we don't divide by zero
    TLF_trials[TLF_trials==0.0]=0.00001
    log.write('Old,{0:.2f},{1:.2f},{2:.2f}\n'.format(
        TLF_response_matrix[0,0] / TLF_trials[0], 
        TLF_response_matrix[0,1] / TLF_trials[1],
        TLF_response_matrix[0,2] /  TLF_trials[2]))
    log.write('Similar,{0:.2f},{1:.2f},{2:.2f}\n'.format(
        TLF_response_matrix[1,0] / TLF_trials[0], 
        TLF_response_matrix[1,1] / TLF_trials[1],
        TLF_response_matrix[1,2] /  TLF_trials[2]))
    log.write('New,{0:.2f},{1:.2f},{2:.2f}\n'.format(
        TLF_response_matrix[2,0] / TLF_trials[0], 
        TLF_response_matrix[2,1] / TLF_trials[1],
        TLF_response_matrix[2,2] /  TLF_trials[2]))

    log.write('\nRaw counts')
    log.write('\nRawRespMatrix,Targ,Lure,Foil\n')
    log.write('Old,{0:d},{1:d},{2:d}\n'.format(TLF_response_matrix[0,0], TLF_response_matrix[0,1],TLF_response_matrix[0,2]))
    log.write('Similar,{0:d},{1:d},{2:d}\n'.format(TLF_response_matrix[1,0], TLF_response_matrix[1,1],TLF_response_matrix[1,2]))
    log.write('New,{0:d},{1:d},{2:d}\n'.format(TLF_response_matrix[2,0], TLF_response_matrix[2,1],TLF_response_matrix[2,2]))
    
    log.write('\n\nLureRawRespMatrix,Bin1,Bin2,Bin3,Bin4,Bin5\n')
    log.write('Old,{0:d},{1:d},{2:d},{3:d},{4:d}\n'.format(
        lure_bin_matrix[0,0], lure_bin_matrix[0,1],lure_bin_matrix[0,2],lure_bin_matrix[0,3],lure_bin_matrix[0,4]))
    log.write('Similar,{0:d},{1:d},{2:d},{3:d},{4:d}\n'.format(
        lure_bin_matrix[1,0], lure_bin_matrix[1,1],lure_bin_matrix[1,2],lure_bin_matrix[1,3],lure_bin_matrix[1,4]))
    log.write('New,{0:d},{1:d},{2:d},{3:d},{4:d}\n'.format(
        lure_bin_matrix[2,0], lure_bin_matrix[2,1],lure_bin_matrix[2,2],lure_bin_matrix[2,3],lure_bin_matrix[2,4]))
    log.write('NR,{0:d},{1:d},{2:d},{3:d},{4:d}\n'.format(
        lure_bin_matrix[3,0], lure_bin_matrix[3,1],lure_bin_matrix[3,2],lure_bin_matrix[3,3],lure_bin_matrix[3,4]))

    log.write('\nPercent-correct (corrected),{0:.2}\n'.format(ncorrect / TLF_trials.sum()))
    log.write('Percent-correct (raw),{0:.2}\n'.format(ncorrect / len(test_list)))

    hit_rate = TLF_response_matrix[0,0] / TLF_trials[0]
    false_rate = TLF_response_matrix[0,2] / TLF_trials[2]
    log.write('\nCorrected recognition (p(Old|Target)-p(Old|Foil)), {0:.2f}'.format(hit_rate - false_rate))

    if params['TwoChoice']==True:
        log.write('\nTwo-choice test metrics\n')
        log.write('\nTwo-choice test metrics\n')
        lure_rate = TLF_response_matrix[0,1] / TLF_trials[1]
        if hit_rate == 0.0:
            hit_rate = 0.5 / TLF_trials[0]
        if false_rate == 0.0:
            false_rate = 0.5 / TLF_trials[2]
        if lure_rate == 0.0:
            lure_rate = 0.5 / TLF_trials[1]
            
        log.write('Endorsement rates')
        log.write('Targets: {0:.2f}'.format(hit_rate))
        log.write('Lures: {0:.2f}'.format(lure_rate))
        log.write('Foils and Firsts: {0:.2f}'.format(false_rate))
        
        
        dpTF = norm.ppf(hit_rate) - norm.ppf(false_rate)
        dpTL = norm.ppf(hit_rate) - norm.ppf(lure_rate)
        dpLF = norm.ppf(lure_rate) - norm.ppf(false_rate)
        
        log.write("d' Target:Foil, {0:.2f}".format(dpTF))
        log.write("d' Target:Lure, {0:.2f}".format(dpTL))
        log.write("d' Lure:Foil, {0:.2f}".format(dpLF))
    else:
        log.write('\nThree-choice test metrics\n')
        sim_lure_rate = TLF_response_matrix[1,1] / TLF_trials[1]
        sim_foil_rate = TLF_response_matrix[1,2] / TLF_trials[2]
        log.write('LDI,{0:.2f}'.format(sim_lure_rate - sim_foil_rate))
    log.flush()
    return 0
 
    
    
    
# ------------------------------------------------------------------------    
# Main routine
params = get_parameters()
print(params)
# Set our random seed
if params['Randomization'] == -1:
    seed = params['ID']
elif params['Randomization']==0:
    seed = None
else:
    seed = params['Randomization']
np.random.seed(seed)

# Get my log file going in append mode
log = open('MST_{0}.txt'.format(params['ID']),"a+")
log.write('MST Task\nStarted at {0}\n'.format(str(datetime.now())))
log.write('ID: {0}\n'.format(params['ID']))
log.write('Duration: {0}\n'.format(params['Duration']))
log.write('ISI: {0}\n'.format(params['ISI']))
log.write('Phase: {0}\n'.format(params['Phase']))
log.write('Set: {0}\n'.format(params['Set']))
log.write('Respkeys: {0} {1} {2}\n'.format(params['Resp1Keys'],params['Resp1Keys'],params['Resp1Keys']))
log.write('Self-paced: {0}\n'.format(params['SelfPaced']))
log.write('Two-choice: {0}\n'.format(params['TwoChoice']))
log.write('NStimPerSet: {0}\n'.format(params['NStimPerSet']))
log.write('sublist: {0}\n'.format(params['sublist']))
log.write('Rnd-mode: {0} with seed {1}\n'.format(params['Randomization'],seed))
log.write('Raw params: {0}'.format(params))
log.write('\n\n')
log.flush()

# Load up the bin file and check the stimulus directory.  Note, the set_bins
# is such that 001a/b.jpg will be first, 002a/b.jpg will be second, etc.       
set_bins = np.array(check_files(params['Set']))



# Figure out which stimuli will be shown in which conditions
(repeatstim, lurestim, foilstim) = setup_list_permuted(set_bins,params['NStimPerSet'],params['sublist'])

# Create the actual order of filenames to be shown
(study_list,study_cond,test_list,test_cond) = create_order(params['Set'],repeatstim, lurestim, foilstim)

win = visual.Window([800, 800], monitor='testMonitor',color='white')

if params['Phase'] == 'Phase 1':
    show_study(params,study_list,study_cond,set_bins)
else:
    show_test(params,test_list,test_cond,set_bins)
    
win.close()  
log.close()
core.quit()
