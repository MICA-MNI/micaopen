import tkinter as tk
import os 

path = os.path.realpath(__file__)
path = os.path.dirname(path)

class TaskGUI:
    def __init__(self,master):
        # Initialize
        self.master=master
        master.title("episodic task")
           
        self.encodingPath = os.path.join(path,'Episodic_Encoding_symbolic.py')
        self.recallPath = os.path.join(path,'Episodic_Recall_symbolic.py')

        # Episodic encoding
        self.encodingButton = tk.Button(master, text = "encoding", command = lambda: self.startTask(self.encodingPath))        
        # Episodic retrieval
        self.recallButton = tk.Button(master, text = "retrieval", command = lambda: self.startTask(self.recallPath))            


        # Pack buttons
        self.encodingButton.pack(side = 'left')
        self.recallButton.pack(side = 'left')
        
        
    def startTask(self,path):
        os.system("python " + path)
    
root = tk.Tk()
GUI = TaskGUI(root)
root.mainloop()
