import tkinter as tk
import os

path = os.path.realpath(__file__)
path = os.path.dirname(path)

class TaskGUI:
    def __init__(self,master):
        # Initialize
        self.master=master
        master.title("Evaluator")
        
        self.EPI_Path = os.path.join(path, 'Episodic_Evaluator.py')
        self.SEM_Path = os.path.join(path, 'Semantic_Evaluator.py')
        self.SPT_Path = os.path.join(path, 'Spatial_Evaluator.py')
        
        # episodic
        self.EPI_Button = tk.Button(master, text = "episodic", command = lambda: self.startTask(self.EPI_Path))
        # semantic
        self.SEM_Button = tk.Button(master, text = "semantic", command = lambda: self.startTask(self.SEM_Path))
        # spatial
        self.SPT_Button = tk.Button(master, text = "spatial", command = lambda: self.startTask(self.SPT_Path))

        # pack buttons
        self.EPI_Button.pack(side = 'left')
        self.SEM_Button.pack(side = 'left')
        self.SPT_Button.pack(side = 'left')

    def startTask(self,path):
        os.system("python " + path)

root = tk.Tk()
GUI = TaskGUI(root)
root.mainloop()
