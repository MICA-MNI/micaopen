import Tkinter as tk
import os 

path = os.path.realpath(__file__)
path = os.path.dirname(path)

class TaskGUI:
    def __init__(self,master):
        # Initialize
        self.master=master
        master.title("Mnemonic Similarity Task")
           
        self.Phase1Path = os.path.join(path,'MST_phase1_fr.py')
        self.Phase2Path = os.path.join(path,'MST_phase2_fr.py')

        # MST phase 1
        self.Phase1Button = tk.Button(master, text = "MST Phase 1", command = lambda: self.startTask(self.Phase1Path))        
        # MST phase 2
        self.Phase2Button = tk.Button(master, text = "MST Phase 2", command = lambda: self.startTask(self.Phase2Path))            


        # Pack buttons
        self.Phase1Button.pack(side = 'left')
        self.Phase2Button.pack(side = 'left')
        
        
    def startTask(self,path):
        os.system("python " + path)
    
root = tk.Tk()
GUI = TaskGUI(root)
root.mainloop()
