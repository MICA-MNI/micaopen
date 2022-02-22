# dependency housekeeping
import os
import time
import tasks
import fileinput
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.switch import Switch
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.togglebutton import ToggleButton

# disable window resizing & remove pesky red dots
from kivy.config import Config
Config.set('graphics', 'resizable', False)
Config.set('input', 'mouse', 'mouse,disable_multitouch')

# main GUI
class GUI(App):
    
    # construct GUI
    def build(self):
        
        # define outer layout
        self.title = ''
        self.outer = GridLayout(spacing=20, padding=85)
        self.outer.cols = 1

        # define inner layout
        self.inner = GridLayout(spacing=5)
        self.inner.cols = 2
        
        # add neuro & mica logos
        self.outer.add_widget(Image(source='mica_logo.png', size_hint=(1, 1.25)))

        # define labels
        fontSize = 18
        self.inner.subLabel = Label(text='ID', font_size=fontSize, bold=True)
        self.inner.scanSessLabel = Label(text='session', font_size=fontSize, bold=True)
        
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
        
        # define button callbacks
        self.inner.ENG.bind(on_press=self.instructions_ENG)
        self.inner.FR.bind(on_press=self.instructions_FR)
        self.inner.PI.bind(on_press=self.protocol_I)
        self.inner.PII.bind(on_press=self.protocol_II)
        
        # add buttons
        self.inner.add_widget(self.inner.ENG)
        self.inner.add_widget(self.inner.FR)
        self.inner.add_widget(self.inner.PI)
        self.inner.add_widget(self.inner.PII)

        # add inner layout
        self.outer.add_widget(self.inner)
        
        # define & add 'initialize' button & callback
        buttID = 'I  N  I  T  I  A  L  I  Z  E'
        bgCol = buttColor
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
        self.inner.PI.color = 'yellow'
        self.inner.PII.color = 'white'
        self.inner.PI.state='down'
        self.inner.PII.state='normal'
    
    # 'Protocol II' callback function
    def protocol_II(self, buttPress):
        self.inner.PII.bold = True
        self.inner.PI.bold = False
        self.inner.PII.color = 'yellow'
        self.inner.PI.color = 'white'
        self.inner.PII.state='down'
        self.inner.PI.state='normal'
    
    # popup for english, protocol1
    def popup1(self):
        mainPop = GridLayout(spacing=2.5, padding=50)
        mainPop.cols = 1
        
        pop = GridLayout(padding=15)
        pop.cols = 2
        
        switches = []
        switch_lab = ['Encoding & ES1', 'qT1', 'Retrieval & ES2', 'T2*', 'MST1 & ES3', 'DWI',                                 'MST2 & ES4', 'RS & ES5']
        
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
        mainPop.start = Button(text='S T A R T', font_size=18, bold=True, color='yellow',                                              background_color=bgCol, background_normal='', size_hint=(.1, .15))
        mainPop.start.bind(on_release=self.start_tasks)
        mainPop.add_widget(pop)
        mainPop.add_widget(mainPop.start)
        
        newWin = Popup(title='English: protocol I', content=mainPop, size_hint=(.82, .8))
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
                self.popup1()
            elif self.inner.ENG.state=='down' and self.inner.PII.state=='down':
                if os.path.isfile(outTmp):
                    os.remove(outTmp)
                outFile = open('tmp.txt', 'w')
                outFile.write('ID:       ' + self.inner.sub.text +
                              '\nsession:  ' + f'{int(self.inner.scan_sess.text):02}' +
                              '\nlanguage: English' + '\nprotocol: II')
                outFile.close()
                #self.popup2()
            elif self.inner.FR.state=='down' and self.inner.PI.state=='down':
                if os.path.isfile(outTmp):
                    os.remove(outTmp)
                outFile = open('tmp.txt', 'w')
                outFile.write('ID:       ' + self.inner.sub.text +
                              '\nsession:  ' + f'{int(self.inner.scan_sess.text):02}' +
                              '\nlanguage: French' + '\nprotocol: I')
                outFile.close()
                #self.popup3()
            elif self.inner.FR.state=='down' and self.inner.PII.state=='down':
                if os.path.isfile(outTmp):
                    os.remove(outTmp)
                outFile = open('tmp.txt', 'w')
                outFile.write('ID:       ' + self.inner.sub.text +
                              '\nsession:  ' + f'{int(self.inner.scan_sess.text):02}' +
                              '\nlanguage: French' + '\nprotocol: II')
                outFile.close()
                #self.popup4()

    def start_tasks(self, buttPress):
        tasks.execute()

if __name__ == '__main__':
    GUI().run()

############### FIN ###############

