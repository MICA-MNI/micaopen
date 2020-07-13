#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May  8 16:54:48 2017

@author: reinder
"""

import Tkinter as tk
import os 

path = os.path.realpath(__file__)
path = os.path.dirname(path)

class TaskGUI:
    def __init__(self,master):
        # Initialize
        self.master=master
        master.title("Task fMRI GUI")
          
        self.flankerPracticePath    = os.path.join(path, 'tasks', 'flanker', 'flankerPractice.py')
        self.flankerPath            = os.path.join(path, 'tasks', 'flanker', 'flankerMain.py') 
        self.episodicPath           = os.path.join(path, 'tasks', 'episodic', 'Episodic_Task.py')
        self.semanticPath           = os.path.join(path, 'tasks', 'semantic', 'Semantic_Task.py')
        self.pairedAssociatePath    = os.path.join(path, 'tasks', 'pairedAssociate', 'PairedAssociate.py')
        self.fixationCross          = os.path.join(path, 'tasks', 'fixationCross', 'fixationCross.py')

        # Flanker Practice Task
        self.flankerPracticeButton  = tk.Button(master, text = "Flanker Practice Task", 
                                                command = lambda: self.startTask(self.flankerPracticePath))
        # Flanker Task
        self.flankerButton          = tk.Button(master, text = "Flanker Task", 
                                                command = lambda: self.startTask(self.flankerPath))
        # Episodic memory
        self.episodicButton         = tk.Button(master, text = "Episodic Memory Task", 
                                                command = lambda: self.startTask(self.episodicPath))        
        # Semantic memory
        self.semanticButton         = tk.Button(master, text = "Semantic Task", 
                                                command = lambda: self.startTask(self.semanticPath))        
        # Paired Associate
        self.pairedAssociateButton  = tk.Button(master, text = "Paired Associate Task", 
                                                command = lambda: self.startTask(self.pairedAssociatePath))     
        # Flanker Task
        self.fixationCrossButton          = tk.Button(master, text = "Fixation Cross", 
                                                command = lambda: self.startTask(self.fixationCross))
        # Pack buttons
        self.pairedAssociateButton.pack(side='left')
        self.fixationCrossButton.pack(side='left')
        self.episodicButton.pack(side='left')
        self.semanticButton.pack(side='left')
        self.flankerPracticeButton.pack(side='left')
        self.flankerButton.pack(side='left')
        
        
    def startTask(self,path):
        os.system("python " + path)
    
root = tk.Tk()
GUI = TaskGUI(root)
root.mainloop()
