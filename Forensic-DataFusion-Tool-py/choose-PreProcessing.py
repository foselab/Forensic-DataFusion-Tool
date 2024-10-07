"""" Developed by Michele Verdi"""

""""Importazione librerie e funzioni dalle altre pagine"""
import tkinter as tk
from tkinter import *
from data_removal import dataRemoval
from Pre_Processing import PreProcessing
from scelta_Exploration  import apriSceltaExploration

        
def openDataRemoval():
        dataRemoval()        

def OpenPreProcessing():
        PreProcessing() 

def openExploration():
        apriSceltaExploration()

def apriSceltaOperazioni():
        """ Creazione pagina che visualizza scelta_PreProcessing.py"""
        root = tk.Tk()
        root.title("Operations Choice")
        root.config(bg="white") 
        width = 600
        height = 600
        root.geometry("600x600")
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        root.geometry("%dx%d+%d+%d" % (width, height, x, y))
        root.resizable(0,0)
        
        """Creazione frame e button"""
        global frameDatabase
        frameDatabase = Frame(root, bg="white")
        frameDatabase.pack(side=TOP, pady=60)
        btn = Button(frameDatabase, text="Data Removal", font=('arial', 18), width=30, bg="red", command=openDataRemoval)
        btn.grid(row=4, columnspan=2, pady=30)
        btn2 = Button(frameDatabase, text="Pre-Processing", font=('arial', 18), width=30, bg="red", command=OpenPreProcessing)
        btn2.grid(row=5, columnspan=2, pady=30)
        btn3 = Button(frameDatabase, text="Exploration", font=('arial', 18), width=30, bg="red", command=openExploration)
        btn3.grid(row=6, columnspan=2, pady=30)  
        btnClose = tk.Button(root, text="Exit",font=('arial', 18), width=10, bg="red",command=root.withdraw )
        btnClose.place(rely=0.85, relx=0.6275)  
    
         
    
        """ Serve per visualizzare pagina costruita"""
        if __name__ == "__main__":
                root.mainloop()
     
        


         