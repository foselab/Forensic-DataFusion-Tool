"""" Developed by Michele Verdi"""

""""Importazione librerie"""
import tkinter as tk
from tkinter import *
from tkinter import ttk
import pandas as pd
import seaborn as sns
import numpy as np
import plotly as plotly
import matplotlib.pyplot as plt #traditional plots
import plotly.express as px #dynamic plots
import os 
import webview

"""Ricezione dati"""
def passaggioscelta_grafici(dati,num):
    global Dati
    Dati=dati
    global Num
    Num=num

def elencofileSceltaGrafici(elenco,numerofile):
    global ElencoFile, nfile
    ElencoFile=elenco
    nfile=numerofile

def apriSceltaGrafici():
    """ Creazione pagina che visualizza scelta_Grafici.py"""
    root = tk.Tk()
    root.title("Graphs")
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
    
    """Creazione Frame della pagina"""
    global frameDatabase
    frameDatabase = Frame(root, bg="white")
    frameDatabase.pack(side=TOP, pady=30)
    
    """Creazione combo elenco file, serve per far selezionare il file all'utente e farlo ricevere al codice"""
    def combofile():
        listafile=[]
        for x in range(nfile) :
            listafile.append(ElencoFile[x])
            
        combo1['values']=listafile
        
        def option_selected1(event):
            global selected_option1
            selected_option1 = combo1.get()
              
            print("You selected:", selected_option1)
            
            
        combo1.bind("<<ComboboxSelected>>", option_selected1)
        if option_selected1!='':
            btn2['state']="active"
    
    combo1= ttk.Combobox(frameDatabase, state='readonly' ,postcommand=combofile)
    combo1.set('Select file')
    combo1.grid(row=1, columnspan=3, pady=20)
    
    
    """ Creazione comboelementi, serve a far selezionare un elemento all'utente e farlo ricevere al codice"""
    def comboelementi():
        global indice
        valore=selected_option1
        trovato=False
        
        
        for x in range (nfile):
            if ElencoFile[x]==valore:
                indice=x
                trovato=True
                
        if trovato==False:
             lista=['']     
             combo2['values']=lista
        
        if trovato==True:
            IDcolonne=Dati[indice].columns
            df2 =pd.DataFrame(Dati[indice])
            ncolonne=len(df2.columns)
            listacolonne=[]
            
            for y in range (ncolonne):
                listacolonne.append(IDcolonne[y])
            del listacolonne[0:2]
            combo2['values']= listacolonne
        
            def option_selected2(event):
                global selected_option2
                selected_option2 = combo2.get()
                
                print("You selected:", selected_option2)
                
                
            combo2.bind("<<ComboboxSelected>>", option_selected2)
    
    combo2= ttk.Combobox(frameDatabase, state='readonly' ,postcommand=comboelementi)
    combo2.set('Select X')
    combo2.grid(row=2, columnspan=3, pady=20)
    
    """ Creazione comboelementi2, serve a far selezionare un elemento all'utente e farlo ricevere al codice"""
    def comboelementi2():
        global indice
        valore=selected_option1
        trovato=False
        
        for x in range (nfile):
            if ElencoFile[x]==valore:
                indice=x
                trovato=True
                
        if trovato==False:
             lista=['']     
             combo3['values']=lista
        
        if trovato==True:
            IDcolonne=Dati[indice].columns
            df2 =pd.DataFrame(Dati[indice])
            ncolonne=len(df2.columns)
            listacolonne=[]
            
            for y in range (ncolonne):
                listacolonne.append(IDcolonne[y])
            del listacolonne[0:2]
            combo3['values']= listacolonne
        
            def option_selected3(event):
                global selected_option3
                selected_option3 = combo3.get()
                
                print("You selected:", selected_option3)
                
                
            combo3.bind("<<ComboboxSelected>>", option_selected3)
    
    combo3= ttk.Combobox(frameDatabase, state='readonly' ,postcommand=comboelementi2)
    combo3.set('Select Y')
    combo3.grid(row=3, columnspan=3, pady=20)
    
    """ Creazione comboelementi3, serve a far selezionare un elemento all'utente e farlo ricevere al codice"""
    def comboelementi3():
        global indice
        valore=selected_option1
        trovato=False
        
        
        for x in range (nfile):
            if ElencoFile[x]==valore:
                indice=x
                trovato=True
                
        if trovato==False:
             lista=['']     
             combo4['values']=lista
        
        if trovato==True:
            IDcolonne=Dati[indice].columns
            df2 =pd.DataFrame(Dati[indice])
            ncolonne=len(df2.columns)
            listacolonne=[]
            
            for y in range (ncolonne):
                listacolonne.append(IDcolonne[y])
            del listacolonne[0:2]
            combo4['values']= listacolonne
        
            def option_selected4(event):
                global selected_option4
                selected_option4 = combo4.get()
                
                print("You selected:", selected_option4)
                
                
            combo4.bind("<<ComboboxSelected>>", option_selected4)
    
    combo4= ttk.Combobox(frameDatabase, state='readonly' ,postcommand=comboelementi3)
    combo4.set('Select Z')
    combo4.grid(row=5, columnspan=3, pady=20)
    
    
    def openBivariate():
        """Funzione per creare i grafici bivariati"""
        """Ricezione dati scelti e assegnazione a variabili"""
        valori=pd.DataFrame(Dati[indice])
        column_headers = list(valori.columns.values)
        tipologia=column_headers[1]
        tipologia=str(tipologia)
        variabile=str(selected_option2) 
        variabile2=str(selected_option3) 
        
        """ Creazione prima immagine""" 
        fig1, axs=plt.subplots(ncols=2, nrows=2)
        fig1.suptitle('Grafici Bivariate')
        sns.set_style("whitegrid")
        sns.histplot(ax=axs[0,0], data=valori, x=variabile, hue =tipologia) 
        sns.histplot(ax=axs[0,1], data=valori, x=variabile, hue = tipologia, kde=True, stat='density')
        
        sns.displot(valori, x=variabile, hue = tipologia, kind = 'kde')
        
        numeric_data = valori.select_dtypes(include=[np.number])
        sns.heatmap(numeric_data.corr(), annot=False, cmap='Reds', vmin=-1, vmax=1, ax=axs[1,0]);
        sns.scatterplot(data=valori, x=variabile, y=variabile2, hue = tipologia, ax=axs[1,1]);
        sns.set_style("whitegrid")
          
        """Creazione seconda immagine"""
        global fig2   
        fig2 = px.scatter(valori, x=variabile, y=variabile2, color=tipologia)   
        
        """Visualizzazione prima immagine"""
        fig1.show()
        plt.show()
        """Visulizzazione seconda immagine"""
        fig2.write_html('prima_figura.html', auto_open=False)
        html_file_path = os.path.join(os.getcwd(), "prima_figura.html")
        webview.create_window("Visualizzazione del grafico", url=html_file_path, width=800, height=600)
        webview.start()
        
        
    def openMultivariate():
        """Funzione per creare i grafici bivariati"""
        """Ricezione dati scelti e assegnazione a variabili"""
        valori=pd.DataFrame(Dati[indice])
        column_headers = list(valori.columns.values)
        tipologia=column_headers[1]
        tipologia=str(tipologia)
        variabile=str(selected_option2) 
        variabile2=str(selected_option3)
        variabile3=str(selected_option4)
        
        """Creazione terza immagine e visualizzazione"""
        fig3 = px.scatter(valori, x=variabile, y=variabile2, color=tipologia, size=variabile3) 
        fig3.write_html('seconda_figura.html', auto_open=False)
        html_file_path = os.path.join(os.getcwd(), "seconda_figura.html")
        webview.create_window("Visualizzazione del grafico", url=html_file_path, width=800, height=600)
        webview.start()
        
        """Creazione quarta immagine e visualizzazione"""
        fig4 = px.scatter(valori, x=variabile, y=variabile2, color=variabile3)  
        fig4.write_html('terza_figura.html', auto_open=False)
        html_file_path2 = os.path.join(os.getcwd(), "terza_figura.html")
        webview.create_window("Visualizzazione del grafico", url= html_file_path2, width=800, height=600)
        webview.start()
    
    
    """ Creazione button"""
    btn2 = Button(frameDatabase, text="Bivariate", font=('arial', 18), width=30, bg="red", command=openBivariate)
    btn2.grid(row=4, columnspan=3, pady=30)
    btn3 = Button(frameDatabase, text="Multivariate", font=('arial', 18), width=30, bg="red", command=openMultivariate)
    btn3.grid(row=6, columnspan=3, pady=30)
    
    
    btnClose = tk.Button(root, text="Exit",font=('arial', 18), width=10, bg="red",command=root.withdraw )
    btnClose.place(rely=0.85, relx=0.6275)  
    
    btn2['state']="disabled"
    
    """ Serve per visualizzare pagina costruita"""
    if __name__ == "__main__":
        
        root.mainloop()
     
        
