import Tkinter as tk
import os 

path = os.path.realpath(__file__)
path = os.path.dirname(path)

class TaskGUI:
    def __init__(self,master):
        # Initialize
        self.master=master
        master.title("Fixation")
           
        self.crossPath = os.path.join(path,'fixation_cross_fr.py')
        self.mvPath = os.path.join(path,'fixation_mv_fr.py')

        # Cross
        self.crossButton = tk.Button(master, text = "Fixation Cross", command = lambda: self.startTask(self.crossPath))        
        # Movie
        self.mvButton = tk.Button(master, text = "Fixation Movie", command = lambda: self.startTask(self.mvPath))            


        # Pack buttons
        self.crossButton.pack(side = 'left')
        self.mvButton.pack(side = 'left')
        
        
    def startTask(self,path):
        os.system("python " + path)
    
root = tk.Tk()
GUI = TaskGUI(root)
root.mainloop()
