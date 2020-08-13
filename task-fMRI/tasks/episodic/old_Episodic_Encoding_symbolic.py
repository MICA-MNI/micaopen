expName = 'Episodic Encoding Task (symbolic)'

#collect participant info, create logfile
pptInfo = {u'session': u'001', u'subject': u'',u'symbol list': ['A','B']}

from psychopy import core
from baseDef import*
from pdb import set_trace as bp

setDir()
expInfo, datafn = info_gui(expName, pptInfo)
from Episodic_Encoding_symbolic_addendum import*
instruction(inst_txt='Instructions/exp_instr_symbolic.txt')
myClock = core.Clock()
#f = open_datalog(datafn, dataformat='.csv', headers='stimulus_1, stimulus_2')
f = open_datalog(datafn, dataformat='.csv', headers='Time, Trial, Condition, Display')
myClock = core.Clock()
task(myClock, expInfo, f)

endExp(f)
