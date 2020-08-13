from psychopy import core, event, logging, visual, gui, data
import time
import numpy as np
import sys, os, errno # to get file system encoding
import csv

def setDir():
    _thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
    os.chdir(_thisDir)
    return _thisDir

def set_window(fullscr=False, gui=True, color=1):
    if fullscr:
        gui = False
    win = visual.Window(size=(1024, 768), color=color, fullscr=fullscr, allowGUI=gui, winType='pyglet', monitor='testMonitor', units ='pix', screen=0)
    return win
def timelog(datalog_fn): 
    logFile = logging.LogFile(datalog_fn+'.log', level=logging.EXP)
    logging.console.setLevel(logging.WARNING) 

def info_gui(expName, expInfo):
    infoDlg = gui.DlgFromDict(expInfo, title = '%s Subject details:'%(expName), order=['subject','session','wordlist','conditions']) #set the name of the pop up window
    expInfo['date'] = data.getDateStr()  # add a simple timestamp to the experiment
    expInfo['expName'] = expName
    datalog_fn = 'data_' + expName + os.sep  + '%s_%s_%s_%s' %(expInfo['subject'], expInfo['session'], expName, expInfo['date'])
    def make_sure_path_exists(path):
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise    
    make_sure_path_exists('data_' + expName)
    timelog(datalog_fn)
    if infoDlg.OK == False: #stop experiment if press cancel 
        print 'User Cancelled'
        core.quit()  # user pressed cancel
    return expInfo, datalog_fn

def load_conditions_dict(csvFile='test.csv'):
    reader = csv.DictReader(open(condiitonfile))
    trials = []
    for row in reader:
        trials.append(row)
    return trials

def open_datalog(datalog_fn, dataformat='_behave.csv', headers='nBack,TrialInd,keyResp,ANS,CORR,RT,IDNO,Session\n'):
    f = open(datalog_fn + dataformat, 'w+') # create log file
    f.write(headers) # write headers
    return f

def write_datalog(f, data):
    f.write(data)
    f.flush()
    return f

def quitEXP(endExpNow):
    if endExpNow:
        print 'User Cancelled'
        core.quit()

def get_keyboard(myClock,win, respkeylist):
    keyResp = None
    thisRT = np.nan
    keylist = ['escape', 'q'] + respkeylist
    for key, RT in event.getKeys(keyList=keylist, timeStamped=myClock):
        if key in ['escape','q']:
            quitEXP(True)
        else:
            keyResp = key
            thisRT = RT
    return keyResp, thisRT

#######################################################################################################################    
#fMRI related modules
def setup_input(input_method):
    """
    If input_method is 'keyboard', we don't do anything
    If input_method is 'serial', we set up the serial port for fMRI responses
    """
    if input_method == 'keyboard':
        # Don't do anything
        resp_device = None
    elif input_method == 'serial':
        # Serial - we need to set it up
        import serial
        if sys.platform == 'linux2':
            port = '/dev/ttyS0'
        else:
            port = 'COM1'
        resp_device = serial.Serial(port=port, baudrate=9600)
        resp_device.setTimeout(0.0001)
    else:
        raise Exception('Unknown input method')
    return resp_device

def clear_buffer(input_method, resp_device):
    """
    Clear whichever buffer is appropriate for our input method
    """
    if input_method == 'keyboard':
        # Clear the keyboard buffer
        event.clearEvents()
    else:
        # Clear the serial buffer
        resp_device.flushInput()

def scanner(in_scanner=False):
    if in_scanner:
        import ynicstim.parallel_compat
        import ynicstim.trigger
        port = '/dev/parport0'
        p = ynicstim.parallel_compat.getParallelPort(port)
        ts = ynicstim.trigger.ParallelInterruptTriggerSource(port=p)
        trig_collector = ynicstim.trigger.TriggerCollector(triggersource=ts, slicespervol=slices_per_vol)
    else:
        trig_collector = None
    return trig_collector



def get_LRresponse(input_method, resp_device, timeStamped,trig_collector,win):
    #if participants don't respond we will set up a null value so we don't get an error
    thisResp = None
    thisRT = np.nan
    if input_method == 'keyboard':
        for key, RT in event.getKeys(keyList = ['escape', 'q', 'left', 'right'], timeStamped = timeStamped): # changed allowed keys here for trial list
            if key in ['escape','q']:
                endExpNow = True
                
                if trig_collector:
                    trig_collector.endCollection()
                quitEXP(endExpNow)
            else:
                thisResp = key
                thisRT = timeStamped.getTime()
    else:
        thisResp = resp_device.read(1)
        thisRT = timeStamped.getTime()
        if len(thisResp) == 0:
            thisResp = None
            thisRT = np.nan
        else:
            # Map button numbers to side
            ## Blue == 1, Green == 3
            if thisResp in ['1', '2']: 
                thisResp = 'left'
            elif thisResp in ['3', '4']:
                thisResp = 'right'
        # Quickly check for a 'q' response on the keyboard to quit
        for key, RT in event.getKeys(keyList = ['escape', 'q'], timeStamped = timeStamped):
            if key in ['escape', 'q']:
                trials.saveAsText(datalog_fn + '_data.csv')
                if trig_collector:
                    trig_collector.endCollection()
                quitEXP(True)
    return thisResp, thisRT


def get_rating(input_method, resp_device, timeStamped,trig_collector,win):
    #if participants don't respond we will set up a null value so we don't get an error
    thisResp = None
    thisRT = np.nan
    if input_method == 'keyboard':
        for key, RT in event.getKeys(keyList = ['escape', 'q', '1', '2', '3', '4'], timeStamped = timeStamped):
            if key in ['escape','q']:
                print 'User Cancelled'

                if trig_collector:
                    trig_collector.endCollection()
                quitEXP(True)
            else:
                thisResp = key
                thisRT = timeStamped.getTime()
    else:
        thisResp = resp_device.read(1)
        thisRT = timeStamped.getTime()
        if len(thisResp) == 0:
            thisResp = None
            thisRT = np.nan
        else:
            pass
        # Quickly check for a 'escape' response on the keyboard to quit
        for key, RT in event.getKeys(keyList = ['escape'], timeStamped = timeStamped):
            if key in ['escape']:
                print 'User cancelled'
                trials.saveAsText(datalog_fn + '_data.csv')
                if trig_collector:
                    trig_collector.endCollection()
                quitEXP(True)
    return thisResp, thisRT

