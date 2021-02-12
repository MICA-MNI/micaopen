import tkinter as tk
import os 

path = os.path.realpath(__file__)
path = os.path.dirname(path)

class TaskGUI:
    def __init__(self,master):
        # Initialize
        self.master=master
        master.title("Tâche cognitive")
           
        self.episodicPath = os.path.join(path, 'tasks', 'episodic', 'Encoding_Recall_symbolic_fr.py')
        self.semanticPath = os.path.join(path, 'tasks', 'semantic', 'Semantic_Task_symbolic_fr.py')
        self.spatialPath = os.path.join(path, 'tasks', 'spatial', 'Spatial_Task_symbolic_fr.py')

        # Episodic memory
        self.episodicButton = tk.Button(master, text = "épisodique", command = lambda: self.startTask(self.episodicPath))        
        # Semantic memory
        self.semanticButton = tk.Button(master, text = "sémantique", command = lambda: self.startTask(self.semanticPath))        
        # Spatial memory
        self.spatialButton = tk.Button(master, text = "spatiale", command = lambda: self.startTask(self.spatialPath))

        # Pack buttons
        self.episodicButton.pack(side = 'left')
        self.semanticButton.pack(side = 'left')
       	self.spatialButton.pack(side = 'left')
        
        
    def startTask(self,path):
        os.system("python " + path)
    
root = tk.Tk()
GUI = TaskGUI(root)
root.mainloop()
