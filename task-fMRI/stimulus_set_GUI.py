#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 10:24:39 2017

@author: Shahin (using Reinder's "mainGUI.py" as scaffold)
"""

import Tkinter as tk
import os 

path = os.path.realpath(__file__)
path = os.path.dirname(path)

class TaskGUI:
    def __init__(self,master):
        # Initialize
        self.master=master
        master.title("Stimulus set")
           
        self.lexicalPath = os.path.join(path, 'lexical_tasks_GUI.py')
        self.symbolicPath = os.path.join(path, 'symbolic_tasks_GUI.py')

        # Lexical stimuli
        self.lexicalButton = tk.Button(master, text = "Lexical", command = lambda: self.startTask(self.lexicalPath))        
        # Symbolic stimuli
        self.symbolicButton = tk.Button(master, text = "Symbolic", command = lambda: self.startTask(self.symbolicPath))           
        
         # Pack buttons
        self.lexicalButton.pack(side = 'left')
        self.symbolicButton.pack(side = 'left')
        
    def startTask(self,path):
        os.system("python " + path)
    
root = tk.Tk()
GUI = TaskGUI(root)
root.mainloop()
