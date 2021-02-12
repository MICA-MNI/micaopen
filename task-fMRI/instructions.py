# -*- coding: utf-8 -*-

import tkinter as tk
import os 

path = os.path.realpath(__file__)
path = os.path.dirname(path)

class TaskGUI:
    def __init__(self,master):
        # Initialize
        self.master=master
        master.title("Instructions")
           
        self.ENG_Path = os.path.join(path, 'symbolic_tasks_GUI.py')
        self.FR_Path = os.path.join(path, 'symbolic_tasks_GUI_fr.py')

        # English
        self.ENG_Button = tk.Button(master, text = "English", command = lambda: self.startTask(self.ENG_Path))        
        # French
        self.FR_Button = tk.Button(master, text = "Français", command = lambda: self.startTask(self.FR_Path))           
        
         # Pack buttons
        self.ENG_Button.pack(side = 'left')
        self.FR_Button.pack(side = 'left')
        
    def startTask(self,path):
        os.system("python " + path)
    
root = tk.Tk()
GUI = TaskGUI(root)
root.mainloop()
