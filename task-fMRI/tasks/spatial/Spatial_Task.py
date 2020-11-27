expName = 'FourMountains_ageing' 
#collect participant info, create logfile
pptInfo = {
    'subject': 'R0001_001', 
    'session': '001', 
    } #a pop up window will show up to collect these information

from psychopy import core
from baseDef import*

setDir()
expInfo, datafn = info_gui(expName, pptInfo)
from FourMountains_TrialDisplay import*
instruction(inst_txt='Instructions/exp_instr.txt')
myClock = core.Clock()
f = open_datalog(datafn, dataformat='.csv', headers='expimages,testimages,CorrAns,resp,resp_RT,resp_corr,rating,rating_RT,IDNO,session\n')
myClock = core.Clock()
task(myClock, expInfo, f)
endExp(f)
