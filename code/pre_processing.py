"""" Developed by Michele Verdi"""

""""Importazione librerie e funzioni dalle altre pagine"""
import tkinter as tk
from tkinter import *
from tkinter import ttk
import pandas as pd
import plotly.express as px #dynamic plots
import numpy as np
import webview
import os
from exploration import passaggioAutoscaling
from exploration import passaggioMean
from exploration import passaggioSnv
from exploration import passaggioSavitzki
from exploration import passaggioSnv_savitzki
from exploration import passaggioColonne
from core import compute_autoscaling, compute_meancentering, compute_snv, compute_savitzky_golay, generate_preprocessing_plot


"""Ricezione dati"""
def passaggioPreProcessing(dati,num):
    global Dati
    Dati=dati
    global Num
    Num=num

def elencofileProcessing(elenco,numerofile):
    global ElencoFile, nfile
    ElencoFile=elenco
    nfile=numerofile

def PreProcessing():
    """ Creazione pagina che visualizza Pre_processing.py"""
    root = tk.Tk()
    root.title("Pre-Processing")
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
    
    """Creazione frame, combo"""
    global frameDatabase
        
    frameDatabase = Frame(root, bg="white")
    frameDatabase.pack(side=TOP, pady=60)
    combo = ttk.Combobox(frameDatabase, values=["DataFrame", "Spettri" ])
    combo.set("Select typology")
    combo.grid(row=2, columnspan=3, pady=20)
    
    """Creazione combo elenco file, serve per far selezionare il file all'utente e farlo ricevere al codice"""
    def combofile():
        listafile=[]
        for x in range(nfile) :
            listafile.append(ElencoFile[x])
            
        combo3['values']=listafile
        
        def option_selected3(event):
            global selected_option3
            selected_option3 = combo3.get()
              
            print("You selected:", selected_option3)
            
            
        combo3.bind("<<ComboboxSelected>>", option_selected3)
    
    combo3= ttk.Combobox(frameDatabase, state='readonly' ,postcommand=combofile)
    combo3.set('Select file')
    combo3.grid(row=1, columnspan=3, pady=40)
    
    """Creazione combo PreProcess, l'utente seleziona il tipo di Pre Process che vuole effettuare e viene mandato al codice"""
    def option_selected(event):
            global selected_option
            selected_option = combo.get()
            print("You selected:", selected_option)
    combo.bind("<<ComboboxSelected>>", option_selected)
    #faccio dopo autoscaling ecc..
    combo2 = ttk.Combobox(frameDatabase, values=["Autoscaling", "Mean Centering", "SNV", "Savitzki-Golay smoothing", "SNV + Savitzki-Golay" ])
    combo2.set("Select Pre-Process")
    combo2.grid(row=3, columnspan=3, pady=40)
    
    def option_selected2(event):
            global selected_option2
            selected_option2 = combo2.get()
            print("You selected:", selected_option2)
    combo2.bind("<<ComboboxSelected>>", option_selected2)
    ##### fine combo autoscaling ecc...
    
    
    
    def autoscaling():
        """funzione autoscaling"""
        temp1=pd.DataFrame(Dati[indice])
        passaggioColonne(pd.DataFrame(Dati[indice]))
        
        """Creazione tabella contenente tutto tranne le prime due colonne (ID e Sostanze)"""
        X1=temp1.drop(temp1.columns[[0,1]], axis=1)
        
        """Creazione fig1  e visualizzazione"""
        fig1=px.parallel_coordinates(X1)
        fig1.write_html('quarta_figura.html', auto_open=False)
        html_file_path3 = os.path.join(os.getcwd(), "quarta_figura.html")
        webview.create_window("Visualizzazione del grafico", url=html_file_path3, width=800, height=600)
        webview.start()

        """creazione x_autosc """
        X_autosc = compute_autoscaling(X1)

        passaggioAutoscaling(X_autosc, "si" )
        
        """Creazione fig2  e visualizzazione"""
        fig2 = px.parallel_coordinates(X_autosc)
        fig2.write_html('quinta_figura.html', auto_open=False)
        html_file_path4 = os.path.join(os.getcwd(), "quinta_figura.html")
        webview.create_window("Visualizzazione del grafico", url=html_file_path4, width=800, height=600)
        webview.start()
        
        
    def meancentering():
        """funzione mean centering"""
        temp2=pd.DataFrame(Dati[indice])
        passaggioColonne(pd.DataFrame(Dati[indice]))
        
        """Creazione tabella contenente tutto tranne le prime due colonne (ID e Sostanze)"""
        X2=temp2.drop(temp2.columns[[0,1]], axis=1)
        data_centered = compute_meancentering(X2)
        data_centered.mean()
        
        passaggioMean(data_centered, "si")
        
        """Creazione fig2  e visualizzazione"""
        fig3 = px.parallel_coordinates(data_centered)
        fig3.write_html('sesta_figura.html', auto_open=False)
        html_file_path5 = os.path.join(os.getcwd(), "sesta_figura.html")
        webview.create_window("Visualizzazione del grafico", url=html_file_path5, width=800, height=600)
        webview.start()
           
    def snv():
        """funzione snv"""
        arrayColonne1=[]
        
        temp3=pd.DataFrame(Dati[indice])
        passaggioColonne(pd.DataFrame(Dati[indice]))
        arrayColonne1=list(temp3.columns.values.tolist())
        
        del arrayColonne1[0:2]
        
        temp4=pd.DataFrame(Dati[indice])
        
        """Creo due database temporanei, uno su cui svolgere le operazioni,uno per mandare i dati corretti ad un'altra pagina python"""
        X3=temp4.drop(temp4.columns[[0,1]], axis=1)
        X5=temp4.drop(temp4.columns[[0,1]], axis=1)
        
        Xsnv = compute_snv(X3.values)
        X3=np.array(X3)
        """Creazione fig4"""
        fig4 = generate_preprocessing_plot(X3, Xsnv, arrayColonne1, 'SNV')
        """visualizzazione fig4 """
        fig4.show()
        
        Xsnv=pd.DataFrame(Xsnv)
        Xsnv.columns = X5.columns
        Xsnv.index = X5.index
        passaggioSnv(Xsnv, "si" )
        
        
        
        
    def savgol():
        """Funzione savitzky golay"""
        arrayColonne2=[]
        temp5=pd.DataFrame(Dati[indice])
        passaggioColonne(pd.DataFrame(Dati[indice]))
        arrayColonne2=list(temp5.columns.values.tolist())
        del arrayColonne2[0:2]
        temp6=pd.DataFrame(Dati[indice])
        """Creo due database temporanei, uno su cui svolgere le operazioni,uno per mandare i dati corretti ad un'altra pagina python"""
        X4=temp6.drop(temp6.columns[[0,1]], axis=1)
        X7=temp6.drop(temp6.columns[[0,1]], axis=1)
        X_savgol = compute_savitzky_golay(X4)

        X4=np.array(X4)
        """Creazione fig5"""
        fig5 = generate_preprocessing_plot(X4, X_savgol, arrayColonne2, 'Savitzki-Golay - smoothing')
        
        """Visualizza fig5"""
        fig5.show()
        
        X_savgol=pd.DataFrame(X_savgol)
        X_savgol.columns = X7.columns
        X_savgol.index = X7.index
        
        passaggioSavitzki(X_savgol,  "si")
       
        
       
            
    def snvsavgol():
        """fuznione snvsavgol"""
        arrayColonne3=[]
        
        temp7=pd.DataFrame(Dati[indice])
        passaggioColonne(pd.DataFrame(Dati[indice]))
        arrayColonne3=list(temp7.columns.values.tolist())
        del arrayColonne3[0:2]
        
        temp8=pd.DataFrame(Dati[indice])
        """Creo due database temporanei, uno su cui svolgere le operazioni,uno per mandare i dati corretti ad un'altra pagina python"""
        X5=temp8.drop(temp8.columns[[0,1]], axis=1)
        X8=temp8.drop(temp8.columns[[0,1]], axis=1)
        X_savgol = compute_savitzky_golay(X5)
        X_snv_savgol = compute_snv(X_savgol)
       
        X5=np.array(X5)
        """Creazione fig6"""
        fig6 = generate_preprocessing_plot(X5, X_snv_savgol, arrayColonne3, 'Savitzki-Golay - smoothing + SNV')
        """Visualizzazione fig6"""
        fig6.show()
        
        X_snv_savgol=pd.DataFrame(X_snv_savgol)
        X_snv_savgol.columns = X8.columns
        X_snv_savgol.index = X8.index
        
        
        passaggioSnv_savitzki(X_snv_savgol, "si" )
       
        
        


    def PreProcessing2():
        """Funzione PreProcessing"""
        """In base al valore selezionato dall'utente, fa eseguire un PreProcess invaindolo alla sua funzione"""
        tipoprocessing= selected_option2
        valore=selected_option3
        IDcolonne=Dati[Num].columns
        variabile=IDcolonne[1]
        
        global indice
        for x in range (nfile):
            
            if ElencoFile[x]==valore:
                indice=x
                
        if tipoprocessing=='Autoscaling':
            autoscaling()
                
        if tipoprocessing=='Mean Centering':
            meancentering()
            
        if tipoprocessing=='SNV':
            snv()
            
        if tipoprocessing=='Savitzki-Golay smoothing':
            savgol()
            
        if tipoprocessing=='SNV + Savitzki-Golay':
            snvsavgol()
            
    btn1 = Button(frameDatabase, text="Plot Pre-Processed", font=('arial', 18), width=30, bg="red", command=PreProcessing2)
    btn1.grid(row=4, columnspan=3, pady=60)
    btnClose = tk.Button(root, text="Exit",font=('arial', 18), width=10, bg="red",command=root.withdraw )
    btnClose.place(rely=0.85, relx=0.6275)
    
    """ Serve per visualizzare pagina costruita"""
    if __name__ == "__main__":
        root.mainloop()    