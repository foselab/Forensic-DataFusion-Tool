"""" Developed by Michele Verdi"""

""""Importazione librerie e funzioni delle altre pagine"""
import tkinter as tk
import pandas as pd
from tkinter import *
from tkinter import filedialog
from tabelle import caricamentoTabelle
from scelta_PreProcessing import apriSceltaOperazioni
from scelta_Grafici import apriSceltaGrafici, elencofileSceltaGrafici
from data_removal import elencofile
from scelta_Exploration import elencofileExploration
from Pre_Processing import elencofileProcessing
from scelta_Exploration import invioSource
import os




def apriPagina_iniziale():
    """ Creazione pagina che visualizza pagina_iniziale.py"""
    root = tk.Tk()
    root.title("Database")
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
        
        
    def formInserisci():
        """Creazione form inserisci"""
        global frameDatabase
        global btn2
        frameDatabase = Frame(root, bg="white")
        frameDatabase.pack(side=TOP, pady=60)
        btn = Button(frameDatabase, text="Insert excel file", font=('arial', 18), width=30, bg="red", command=openFile)
        btn.grid(row=1, columnspan=2, pady=20)
        
        btn2 = Button(frameDatabase, text="Graphs", font=('arial', 18), width=30, bg="red", command=openGrafici)
        btn2.grid(row=3, columnspan=2, pady=40)
        btn2['state']="disabled"
        btnClose = tk.Button(root, text="Next",font=('arial', 18), width=10, bg="red",command=avanti ) 
        btnClose.place(rely=0.85, relx=0.6275)
    
    global a

        
    def openFile():
        """Apertura finsetra che consente di inserire i file dalla directory del computer"""
        tk.Tk().withdraw()
        elenco=""
        global dataframe_collection
        dataframe_collection ={}
        global n
        root.withdraw()
        n=0    
        nomi={}
        a=0
        
        filepath = filedialog.askopenfilenames(initialdir="C:\\Users\\Cakow\\PycharmProjects\\Main",
                                                title="Open file okay?",
                                                filetypes= (("excel files","*.xlsx "),
                                                            ("all file","*.*")))
        """ ciclo che conta il numero di file selezionati e li mette in un array"""
        for x in filepath:
            name= (os.path.basename(x))
            ext = os.path.splitext(name)[1]
            variabile=x
            
            nomi[a]=name
            a+=1
            
            """ Creazione elenco utile per il visualizzare il nome dei file inseriti"""
            elenco+="\n"+name
            
            """controllo che il file sia di tipo excel"""
            try:
                ext == '.xlsx'
                Dati= pd.read_excel(x)
                dataframe_collection[n] = pd.DataFrame(Dati)
                caricamentoTabelle(dataframe_collection,n)
                n+=1 
                lbl = Label(frameDatabase, text="Elenco file inseriti: "+ elenco, font=('arial', 25), bd=18, bg="white")
                lbl.grid(row=2, padx=120) 
                    
            except ValueError:
                tk.messagebox.showerror("Information", "the file "+ name+" is invalid")
                root.withdraw()
                root.deiconify()
                return None
        root.deiconify() 
        btn2["state"]="active"
        """invio elenco file alle altre pagine python"""
        elencofile(nomi, a)
        elencofileProcessing(nomi,a)
        elencofileSceltaGrafici(nomi,a)
        elencofileExploration(nomi,a)
        invioSource(variabile)
        
    """ Apri pagina scelta_grafici"""
    def openGrafici():
        apriSceltaGrafici()    
    

        
    """Apri pagina scelta_PreProcessing"""
    def avanti():
        apriSceltaOperazioni()    
    
    
    formInserisci()            
        
    

     
    """ Serve per visualizzare pagina costruita"""   
    if __name__ == "__main__":
        
        root.mainloop()