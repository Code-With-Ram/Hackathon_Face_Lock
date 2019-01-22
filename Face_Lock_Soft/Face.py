from tkinter import*
from tkinter import messagebox
import pandas as pd
import fac_rec
import face_extract
import facetraining
import os
import pickle
class Face:

    def __init__(self,master):
    
        self.frame_header = Frame(master)
        self.frame_header.pack(side=TOP)
        self.logo=PhotoImage(file="/home/vineeth/python/Multiface_GUI/face_icon.png")
        Label(self.frame_header , text = "Welcome  to  FaceUnlocking   System      ").grid(row = 0,column=0,padx=180 ,pady=20,sticky='w')

        Label(self.frame_header , image = self.logo).grid(row = 1,column=0 ,padx=230,sticky='w')
        

        self.frame_content = Frame(master)
        self.frame_content.pack()
        Button(self.frame_content , text ="Set Face ID",command=self.Extract,width=20).grid(row =7,column=6,padx=5 ,pady=5,sticky='e')
        Button(self.frame_content , text ="Face Scanning",command =self.Recognize,width=20).grid(row = 8,column=6,padx=5 ,pady=5,sticky='w')
        Del = Button(self.frame_content , text ="Erase All Data" , command=self.Delete,width=20)
        Del.grid(row = 9,column=6,padx=5 ,sticky='w')
        Button(self.frame_content , text ="Quit",command =master.destroy,width=20).grid(row = 15,column=6,padx=5 ,pady=5,sticky='w')

        self.load_data()
    def SubmitId(self):
        self.names.append(self.entry_name.get())
        self.id_list.append(len(self.id_list)+1)
        
        pickle.dump(self.names,open("names.dat","wb"))
        pickle.dump(self.id_list,open("id_list.dat","wb"))
        self.profile.destroy()
        face_extract.main()
        self.Train()
    def load_data(self):
        try:
            self.names=pickle.load(open("names.dat","rb"))
            self.id_list=pickle.load(open("id_list.dat","rb"))
        except FileNotFoundError:
            self.names=['None']
            self.id_list=[]
            print ("Name file is not present, skipping the reading process...")	
            
    def Delete(self):            

        os.system("rm id_list.dat")
        os.system("rm names.dat")
        os.system("rm FaceSamples/*.jpg")
        os.system("rm trainer/*.*")
        
    def Train(self):
        facetraining.main()
    def Extract(self):
        self.profile = Tk()
        self.profile.title("Profile")
        self.profile.geometry("320x120")
        self.name = Label(self.profile, text = " Enter your name ")
        self.name.grid(row=2,column=0,pady=10)
        
        self.entry_name = Entry(self.profile,width = 20)
        self.entry_name.grid(row=2,column=1)
        self.entry_name.focus_set()
        self.Submit = Button(self.profile,text = "Submit",command=self.SubmitId)
        self.Submit.grid(row=4,column=1,sticky='w')
        
    def Recognize(self):
        fac_rec.main()
        


root =Tk()
root.geometry("620x380")
root.title("Face Unlocking")
face = Face(root)

root.mainloop()
        
