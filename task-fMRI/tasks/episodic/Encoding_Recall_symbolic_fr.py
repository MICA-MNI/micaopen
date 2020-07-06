import Tkinter as tk
import os 

path = os.path.realpath(__file__)
path = os.path.dirname(path)

class TaskGUI:
    def __init__(self,master):
        # Initialize
        self.master=master
        master.title("Episodic")
           
        self.encodingPath = os.path.join(path,'Episodic_Encoding_symbolic_fr.py')
        self.recallPath = os.path.join(path,'Episodic_Recall_symbolic_fr.py')

        # Episodic encoding
        self.encodingButton = tk.Button(master, text = "Encoding", command = lambda: self.startTask(self.encodingPath))        
        # Episodic recall
        self.recallButton = tk.Button(master, text = "Recall", command = lambda: self.startTask(self.recallPath))            


        # Pack buttons
        self.encodingButton.pack(side = 'left')
        self.recallButton.pack(side = 'left')
        
        
    def startTask(self,path):
        os.system("python " + path)
    
root = tk.Tk()
GUI = TaskGUI(root)
root.mainloop()
