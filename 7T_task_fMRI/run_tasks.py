# dependency housekeeping
from gui_dependencies import *

# disable window resizing & remove pesky red dots
from kivy.config import Config
Config.set('graphics', 'resizable', False)
Config.set('input', 'mouse', 'mouse,disable_multitouch')

# disable annoying pygame greeting
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

os.system('clear')

# get current directory
currentDir = os.getcwd()

# main GUI
class GUI(App):
    
    # construct GUI
    def build(self):
        
        # define outer layout
        self.title = ''
        self.outer = GridLayout(spacing=20, padding=85)
        self.outer.cols = 1

        # define inner layout
        self.inner = GridLayout(spacing=4)
        self.inner.cols = 2
        
        # add neuro & mica logos
        self.outer.add_widget(Image(source='mica_logo.png', size_hint=(1, 1.25)))

        # define labels
        fontSize = 14
        self.inner.subLabel = Label(text='ID', font_size=fontSize, bold=True)
        self.inner.scanSessLabel = Label(text='SESSION', font_size=fontSize, bold=True)
        
        # add text boxes
        self.inner.sub = TextInput(multiline=False, font_size=fontSize, halign='center')
        self.inner.add_widget(self.inner.subLabel)
        self.inner.add_widget(self.inner.sub)

        self.inner.scan_sess = TextInput(multiline=False, font_size=fontSize, halign='center')
        self.inner.add_widget(self.inner.scanSessLabel)
        self.inner.add_widget(self.inner.scan_sess)
        
        # define buttons
        fontColor = 'white'
        buttColor = (37/255, 121/255, 203/255, 1)
        
        self.inner.ENG = ToggleButton(text='English', font_size=fontSize, bold=False, color=fontColor,
                                      background_color=buttColor, background_normal='')
        self.inner.FR = ToggleButton(text='French', font_size=fontSize, bold=False, color=fontColor,
                                     background_color=buttColor, background_normal='')
        self.inner.PI = ToggleButton(text='Protocol I', font_size=fontSize, bold=False, color=fontColor,
                                     background_color=buttColor, background_normal='')
        self.inner.PII = ToggleButton(text='Protocol II', font_size=fontSize, bold=False, color=fontColor,
                                      background_color=buttColor, background_normal='')
        self.inner.PIII = ToggleButton(text='Protocol III', font_size=fontSize, bold=False, color=fontColor,
                                       background_color=buttColor, background_normal='')
        self.inner.PIV = ToggleButton(text='Protocol IV', font_size=fontSize, bold=False, color=fontColor,
                                       background_color=buttColor, background_normal='')
        
        # define button callbacks
        self.inner.ENG.bind(on_press=self.instructions_ENG)
        self.inner.FR.bind(on_press=self.instructions_FR)
        self.inner.PI.bind(on_press=self.protocol_I)
        self.inner.PII.bind(on_press=self.protocol_II)
        self.inner.PIII.bind(on_press=self.protocol_III)
        self.inner.PIV.bind(on_press=self.protocol_IV)
        
        # add buttons
        self.inner.add_widget(self.inner.ENG)
        self.inner.add_widget(self.inner.FR)
        self.inner.add_widget(self.inner.PI)
        self.inner.add_widget(self.inner.PII)
        self.inner.add_widget(self.inner.PIII)
        self.inner.add_widget(self.inner.PIV)

        # add inner layout
        self.outer.add_widget(self.inner)
        
        # define & add 'initialize' button & callback
        buttID = 'I  N  I  T  I  A  L  I  Z  E'
        bgCol = buttColor
        # initialize protocol_day as 0
        self.protocol_day = 0
        self.initialize = Button(text=buttID, font_size=fontSize, bold=True, color='yellow',
                                 background_color=bgCol, background_normal='', size_hint=(1, .25))
        self.initialize.bind(on_release=self.Initialize)
        self.outer.add_widget(self.initialize)

        # return GUI
        return self.outer
    
    # 'English' button callback function
    def instructions_ENG(self, buttPress):
        self.inner.ENG.bold = True
        self.inner.FR.bold = False
        self.inner.ENG.color = 'yellow'
        self.inner.FR.color = 'white'
        self.inner.ENG.state='down'
        self.inner.FR.state='normal'
    
    # 'French' button callback function
    def instructions_FR(self, buttPress):
        self.inner.FR.bold = True
        self.inner.ENG.bold = False
        self.inner.FR.color = 'yellow'
        self.inner.ENG.color = 'white'
        self.inner.FR.state='down'
        self.inner.ENG.state='normal'

    # 'Protocol I' callback function
    def protocol_I(self, buttPress):
        self.inner.PI.bold = True
        self.inner.PII.bold = False
        self.inner.PIII.bold = False
        self.inner.PIV.bold = False
        self.inner.PI.color = 'yellow'
        self.inner.PII.color = 'white'
        self.inner.PIII.color = 'white'
        self.inner.PIV.color = 'white'
        self.inner.PI.state='down'
        self.inner.PII.state='normal'
        self.inner.PIII.state='normal'
        self.inner.PIV.state='normal'
    
    # 'Protocol II' callback function
    def protocol_II(self, buttPress):
        self.inner.PII.bold = True
        self.inner.PI.bold = False
        self.inner.PIII.bold = False
        self.inner.PIV.bold = False
        self.inner.PII.color = 'yellow'
        self.inner.PI.color = 'white'
        self.inner.PIII.color = 'white'
        self.inner.PIV.color = 'white'
        self.inner.PII.state='down'
        self.inner.PI.state='normal'
        self.inner.PIII.state='normal'
        self.inner.PIV.state='normal'
    
    # 'Protocol III' callback function
    def protocol_III(self, buttPress):
        self.inner.PIII.bold = True
        self.inner.PI.bold = False
        self.inner.PII.bold = False
        self.inner.PIV.bold = False
        self.inner.PIII.color = 'yellow'
        self.inner.PI.color = 'white'
        self.inner.PII.color = 'white'
        self.inner.PIV.color = 'white'
        self.inner.PIII.state='down'
        self.inner.PI.state='normal'
        self.inner.PII.state='normal'
        self.inner.PIV.state='normal'
    
    # 'Protocol IV' callback function
    def protocol_IV(self, buttPress):
        self.inner.PIV.bold = True
        self.inner.PI.bold = False
        self.inner.PII.bold = False
        self.inner.PIII.bold = False
        self.inner.PIV.color = 'yellow'
        self.inner.PI.color = 'white'
        self.inner.PII.color = 'white'
        self.inner.PIII.color = 'white'
        self.inner.PIV.state='down'
        self.inner.PI.state='normal'
        self.inner.PII.state='normal'
        self.inner.PIII.state='normal'
    
    # popup for english, protocol1
    def popup1(self):
        mainPop = GridLayout(spacing=2.5, padding=50)
        mainPop.cols = 1
        
        pop = GridLayout(padding=15)
        pop.cols = 2
        
        switches = []
        switch_lab = ['Encoding & ES1', 'qT1', 'Retrieval & ES2', 'T2*', 'MST1 & ES3', 'DWI',
	                  'MST2 & ES4', 'RS & ES5']
        
        addFile = open('tmp.txt', 'a')
        for s in range(len(switch_lab)):
            pop.add_widget(Label(text=switch_lab[s]))
            switches.append(Switch(active=True))
            addFile.write('\nBlock' + str(s+1) + ': True')
            pop.add_widget(switches[s])
        addFile.close()
        
        switches[0].bind(active=self.switchBlock1)
        switches[1].bind(active=self.switchBlock2)
        switches[2].bind(active=self.switchBlock3)
        switches[3].bind(active=self.switchBlock4)
        switches[4].bind(active=self.switchBlock5)
        switches[5].bind(active=self.switchBlock6)
        switches[6].bind(active=self.switchBlock7)
        switches[7].bind(active=self.switchBlock8)
        
        bgCol = (37/255, 121/255, 203/255, 1)
        mainPop.start = Button(text='S T A R T', font_size=18, bold=True, color='yellow',
	                           background_color=bgCol, background_normal='', size_hint=(.1, .15))
        mainPop.start.bind(on_release=self.start_tasks)
        mainPop.add_widget(pop)
        mainPop.add_widget(mainPop.start)
        
        newWin = Popup(title='English: protocol I', content=mainPop, size_hint=(.82, .8))
        newWin.open()

    # popup for english, protocol2
    def popup2(self):
        mainPop = GridLayout(spacing=2.5, padding=50)
        mainPop.cols = 1
        
        pop = GridLayout(padding=15)
        pop.cols = 2

        switches = []
        switch_lab = ['Spatial1 & ES1', 'qT1', 'Spatial2 & ES2', 'T2*', 'Semantic1 & ES3', 'DWI',
	                  'Semantic2 & ES4', 'RS & ES5']
        
        addFile = open('tmp.txt', 'a')
        for s in range(len(switch_lab)):
            pop.add_widget(Label(text=switch_lab[s]))
            switches.append(Switch(active=True))
            addFile.write('\nBlock' + str(s+1) + ': True')
            pop.add_widget(switches[s])
        addFile.close()
        
        switches[0].bind(active=self.switchBlock1)
        switches[1].bind(active=self.switchBlock2)
        switches[2].bind(active=self.switchBlock3)
        switches[3].bind(active=self.switchBlock4)
        switches[4].bind(active=self.switchBlock5)
        switches[5].bind(active=self.switchBlock6)
        switches[6].bind(active=self.switchBlock7)
        switches[7].bind(active=self.switchBlock8)
        
        bgCol = (37/255, 121/255, 203/255, 1)
        mainPop.start = Button(text='S T A R T', font_size=18, bold=True, color='yellow',
	                           background_color=bgCol, background_normal='', size_hint=(.1, .15))
        mainPop.start.bind(on_release=self.start_tasks)
        #mainPop.start.bind(on_release=self.close_pop)
        mainPop.add_widget(pop)
        mainPop.add_widget(mainPop.start)
        
        newWin = Popup(title='English: protocol II', content=mainPop, size_hint=(.82, .8))
        newWin.open()
    
    # popup for english, protocol3
    def popup3(self):
        mainPop = GridLayout(spacing=2.5, padding=50)
        mainPop.cols = 1
        
        pop = GridLayout(padding=15)
        pop.cols = 2
        
        switches = []
        switch_lab = ['Action Sniper & ES1', 'Control Seedlings & ES2', 'Action Bathroom & ES3',
                      'Action Caddy & ES4', 'Control Harsh & ES5', 'Control Pines & ES6', 'Control Sping & ES7',
                      'Suspense Kirsten & ES8']
        
        addFile = open('tmp.txt', 'a')
        for s in range(len(switch_lab)):
            pop.add_widget(Label(text=switch_lab[s]))
            switches.append(Switch(active=True))
            addFile.write('\nBlock' + str(s+1) + ': True')
            pop.add_widget(switches[s])
        addFile.close()
        
        switches[0].bind(active=self.switchBlock1)
        switches[1].bind(active=self.switchBlock2)
        switches[2].bind(active=self.switchBlock3)
        switches[3].bind(active=self.switchBlock4)
        switches[4].bind(active=self.switchBlock5)
        switches[5].bind(active=self.switchBlock6)
        switches[6].bind(active=self.switchBlock7)
        switches[7].bind(active=self.switchBlock8)
        
        bgCol = (37/255, 121/255, 203/255, 1)
        mainPop.start = Button(text='S T A R T', font_size=18, bold=True, color='yellow',
	                           background_color=bgCol, background_normal='', size_hint=(.1, .15))
        mainPop.start.bind(on_release=self.start_resting_state)
        #mainPop.start.bind(on_release=self.close_pop)
        mainPop.add_widget(pop)
        mainPop.add_widget(mainPop.start)
        
        newWin = Popup(title='English: protocol III', content=mainPop, size_hint=(.82, .8))
        newWin.open()

    def popup4(self):
        # popup for english, protocol4
        mainPop = GridLayout(spacing=2.5, padding=50)
        mainPop.cols = 1

        pop = GridLayout(padding=15)
        pop.cols = 2

        switches = []
        switch_lab = ['semphon1 & ES1', 'qT1', 'semphon2 & ES2', 'T2*', '?? & ES3', 'DWI', '?? & ES4',
                      'RS & ES5']

        addFile = open('tmp.txt', 'a')
        for s in range(len(switch_lab)):
            pop.add_widget(Label(text=switch_lab[s]))
            switches.append(Switch(active=True))
            addFile.write('\nBlock' + str(s + 1) + ': True')
            pop.add_widget(switches[s])
        addFile.close()

        switches[0].bind(active=self.switchBlock1)
        switches[1].bind(active=self.switchBlock2)
        switches[2].bind(active=self.switchBlock3)
        switches[3].bind(active=self.switchBlock4)
        switches[4].bind(active=self.switchBlock5)
        switches[5].bind(active=self.switchBlock6)
        switches[6].bind(active=self.switchBlock7)
        switches[7].bind(active=self.switchBlock8)

        bgCol = (37 / 255, 121 / 255, 203 / 255, 1)
        mainPop.start = Button(text='S T A R T', font_size=18, bold=True, color='yellow', background_color=bgCol,
                               background_normal='', size_hint=(.1, .15))
        mainPop.start.bind(on_release=self.start_tasks)
        # mainPop.start.bind(on_release=self.close_pop)
        mainPop.add_widget(pop)
        mainPop.add_widget(mainPop.start)

        newWin = Popup(title='English: protocol IV', content=mainPop, size_hint=(.82, .8))
        newWin.open()

    def switchBlock1(self, instance, value):
        for line in fileinput.input('tmp.txt', inplace=True):
            if not value:
                print(line.rstrip().replace('Block1: True', 'Block1: False'))
            else:
                print(line.rstrip().replace('Block1: False', 'Block1: True'))
        fileinput.close()
        
    def switchBlock2(self, instance, value):
        for line in fileinput.input('tmp.txt', inplace=True):
            if not value:
                print(line.rstrip().replace('Block2: True', 'Block2: False'))
            else:
                print(line.rstrip().replace('Block2: False', 'Block2: True'))
        fileinput.close()
    
    def switchBlock3(self, instance, value):
        for line in fileinput.input('tmp.txt', inplace=True):
            if not value:
                print(line.rstrip().replace('Block3: True', 'Block3: False'))
            else:
                print(line.rstrip().replace('Block3: False', 'Block3: True'))
        fileinput.close()
    
    def switchBlock4(self, instance, value):
        for line in fileinput.input('tmp.txt', inplace=True):
            if not value:
                print(line.rstrip().replace('Block4: True', 'Block4: False'))
            else:
                print(line.rstrip().replace('Block4: False', 'Block4: True'))
        fileinput.close()
    
    def switchBlock5(self, instance, value):
        for line in fileinput.input('tmp.txt', inplace=True):
            if not value:
                print(line.rstrip().replace('Block5: True', 'Block5: False'))
            else:
                print(line.rstrip().replace('Block5: False', 'Block5: True'))
        fileinput.close()
    
    def switchBlock6(self, instance, value):
        for line in fileinput.input('tmp.txt', inplace=True):
            if not value:
                print(line.rstrip().replace('Block6: True', 'Block6: False'))
            else:
                print(line.rstrip().replace('Block6: False', 'Block6: True'))
        fileinput.close()
    
    def switchBlock7(self, instance, value):
        for line in fileinput.input('tmp.txt', inplace=True):
            if not value:
                print(line.rstrip().replace('Block7: True', 'Block7: False'))
            else:
                print(line.rstrip().replace('Block7: False', 'Block7: True'))
        fileinput.close()
    
    def switchBlock8(self, instance, value):
        for line in fileinput.input('tmp.txt', inplace=True):
            if not value:
                print(line.rstrip().replace('Block8: True', 'Block8: False'))
            else:
                print(line.rstrip().replace('Block8: False', 'Block8: True'))
        fileinput.close()

    # 'Initialize' callback function
    def Initialize(self, buttPress):
        
        outTmp = 'tmp.txt'
        
        if not self.inner.sub.text or not self.inner.scan_sess.text:
            print('ID and/or session info missing')
        else:
            if self.inner.ENG.state=='down' and self.inner.PI.state=='down':
                if os.path.isfile(outTmp):
                    os.remove(outTmp)
                outFile = open('tmp.txt', 'w')
                outFile.write('ID:       ' + self.inner.sub.text +
                              '\nsession:  ' + f'{int(self.inner.scan_sess.text):02}' +
                              '\nlanguage: English' + '\nprotocol: I')
                outFile.close()
                self.protocol_day = 1
                self.popup1()
            elif self.inner.ENG.state=='down' and self.inner.PII.state=='down':
                if os.path.isfile(outTmp):
                    os.remove(outTmp)
                outFile = open('tmp.txt', 'w')
                outFile.write('ID:       ' + self.inner.sub.text +
                              '\nsession:  ' + f'{int(self.inner.scan_sess.text):02}' +
                              '\nlanguage: English' + '\nprotocol: II')
                outFile.close()
                self.protocol_day = 2
                self.popup2()
            elif self.inner.ENG.state=='down' and self.inner.PIII.state=='down':
                if os.path.isfile(outTmp):
                    os.remove(outTmp)
                outFile = open('tmp.txt', 'w')
                outFile.write('ID:       ' + self.inner.sub.text +
                              '\nsession:  ' + f'{int(self.inner.scan_sess.text):02}' +
                              '\nlanguage: English' + '\nprotocol: III')
                outFile.close()
                self.protocol_day = 3
                self.popup3()
            elif self.inner.ENG.state=='down' and self.inner.PIV.state=='down':
                if os.path.isfile(outTmp):
                    os.remove(outTmp)
                outFile = open('tmp.txt', 'w')
                outFile.write('ID:       ' + self.inner.sub.text +
                              '\nsession:  ' + f'{int(self.inner.scan_sess.text):02}' +
                              '\nlanguage: English' + '\nprotocol: IV')
                outFile.close()
                self.protocol_day = 4
                self.popup4()
            elif self.inner.FR.state=='down' and self.inner.PI.state=='down':
                if os.path.isfile(outTmp):
                    os.remove(outTmp)
                outFile = open('tmp.txt', 'w')
                outFile.write('ID:       ' + self.inner.sub.text +
                              '\nsession:  ' + f'{int(self.inner.scan_sess.text):02}' +
                              '\nlanguage: French' + '\nprotocol: I')
                outFile.close()
                #self.popup6()
            elif self.inner.FR.state=='down' and self.inner.PII.state=='down':
                if os.path.isfile(outTmp):
                    os.remove(outTmp)
                outFile = open('tmp.txt', 'w')
                outFile.write('ID:       ' + self.inner.sub.text +
                              '\nsession:  ' + f'{int(self.inner.scan_sess.text):02}' +
                              '\nlanguage: French' + '\nprotocol: II')
                outFile.close()
                #self.popup7()

    # execute tasks
    def start_tasks(self, buttPress):
        if self.protocol_day == 4:
            subprocess.run(['python3.8', currentDir + '/' + 'tasks_protocol4_E.py'])
        else:
            subprocess.run(['python3.8', currentDir + '/' + 'tasks.py'])
    
    # execute resting state
    def start_resting_state(self, buttPress):
        subprocess.run(['python3.8', currentDir + '/' + 'resting_state.py'])

if __name__ == '__main__':
    GUI().run()

############### FIN ###############
