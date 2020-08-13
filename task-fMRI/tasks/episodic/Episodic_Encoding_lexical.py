expName = 'Episodic Encoding Task (lexical)'

#collect participant info, create logfile
pptInfo = {u'session': u'001', u'subject': u'',u'word list': ['A','B']}

from psychopy import core
from baseDef import*

setDir()
expInfo, datafn = info_gui(expName, pptInfo)
from Episodic_Encoding_lexical_addendum import*
instruction(inst_txt='Instructions/exp_instr_lexical.txt')
myClock = core.Clock()
f = open_datalog(datafn, dataformat='.csv', headers='wordpair, list_AB')
myClock = core.Clock()
task(myClock, expInfo, f)

endExp(f)
