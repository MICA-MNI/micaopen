#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 13:11:11 2017

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
        master.title("Lexical tasks")
           
        self.episodicPath = os.path.join(path, 'tasks', 'episodic', 'Encoding_Recall_lexical.py')
        self.semanticPath = os.path.join(path, 'tasks', 'semantic', 'Semantic_Task_lexical.py')
        self.spatialPath = os.path.join(path, 'tasks', 'spatial', 'Spatial_Task_lexical.py')

        # Episodic memory
        self.episodicButton = tk.Button(master, text = "Episodic", command = lambda: self.startTask(self.episodicPath))        
        # Semantic memory
        self.semanticButton = tk.Button(master, text = "Semantic", command = lambda: self.startTask(self.semanticPath))        
        # Spatial memory
	self.spatialButton = tk.Button(master, text = "Spatial", command = lambda: self.startTask(self.spatialPath))     


        # Pack buttons
        self.episodicButton.pack(side = 'left')
        self.semanticButton.pack(side = 'left')
       	self.spatialButton.pack(side = 'left')
        
        
    def startTask(self,path):
        os.system("python " + path)
    
root = tk.Tk()
GUI = TaskGUI(root)
root.mainloop()
