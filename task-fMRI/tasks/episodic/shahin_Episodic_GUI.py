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
        master.title("Episodic Memory Task")
           
        self.episodicPath = os.path.join(path, 'shahin_Episodic_List.py')
        self.episodic2Path = os.path.join(path, 'shahin_Episodic_Prompt.py')

        # Episodic memory encoding
        self.episodicButton = tk.Button(master, text = "Encoding phase", command = lambda: self.startTask(self.episodicPath))        
        # Episodic memory retrieval
        self.episodic2Button = tk.Button(master, text = "Retrieval phase", command = lambda: self.startTask(self.episodic2Path))            


        # Pack buttons
        self.episodicButton.pack(side = 'left')
        self.episodic2Button.pack(side = 'left')
        
    def startTask(self,path):
        os.system("python " + path)
    
root = tk.Tk()
GUI = TaskGUI(root)
root.mainloop()
