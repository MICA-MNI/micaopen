expName = 'PairedAssociate_MPsych' 
#collect participant info, create logfile
pptInfo = {
    'subject': '', 
    'session': '', 
    'conditions' : ['encoding'],
    'wordlist': ['A','B']
    } #a pop up window will show up to collect these information

from psychopy import core
from baseDef import*
import os
setDir()
expInfo, datafn = info_gui(expName, pptInfo)

from PairedAssociate_TrialDisplay import*
stimuli_list_all = PairedAssociate_Stimuli_All(expInfo) 
stimuli_list_weak = PairedAssociate_Stimuli_Weak(expInfo)
stimuli_list_strong = PairedAssociate_Stimuli_Strong(expInfo)

if expInfo['conditions'] == 'encoding':
    instruction(inst_txt='Instructions' + os.sep + 'exp_encode_instr.txt')
    myClock = core.Clock()
    encoding(myClock, stimuli_list_all)
#    instruction(inst_txt='Instructions/exp_recall_instr.txt')
#    f = open_datalog(datafn, dataformat='_immediate.csv', headers='ExpIndex,TrialIndex,target,Ans,Resp,corr,RT(ms),IDNO,session\n')
#    myClock = core.Clock()
#    
#    recall_weak(myClock, stimuli_list_weak, expInfo, f)
#    myClock = core.Clock()
#    recall_strong(myClock, stimuli_list_strong, expInfo, f)
#    endExp(f)
    
else:
    instruction(inst_txt='Instructions' + os.sep + 'exp_delay_instr.txt')
    f = open_datalog(datafn, dataformat='_delay.csv', headers='ExpIndex,TrialIndex,target,Ans,Resp,corr,RT(ms),RatingResp,RatingRT(ms),IDNO,session\n')
    myClock = core.Clock()
    recall(myClock, stimuli_list, expInfo, f)
    endExp(f) 
