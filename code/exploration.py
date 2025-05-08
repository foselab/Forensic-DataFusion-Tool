"""" Developed by Michele Verdi"""

""""Importazione librerie e funzioni dalle altre pagine"""
import tkinter as tk
from tkinter import *
from tkinter import ttk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt #traditional plots
import plotly.express as px #dynamic plots
from print_table import stampaTabelle
import scipy.stats
import os
import webview
from core import fuse_data, compute_pca, generate_scree_plots, get_scores_and_loadings, generate_pca_html_2d_scatters, generate_pca_html_3d_scatters, detect_outliers, generate_outliers_html_scatters

"""Ricezione dati"""
def passaggioColonne(colonne):
    global colonnaID, colonnaNomi
    data=pd.DataFrame(colonne)
    colonnaID=data.iloc[:,0]
    colonnaNomi=data.iloc[:, 1]
    
def passaggioExploration(dati,num):
    global Dati
    Dati=dati
    global Num
    Num=num

def invioSource(filepath):
    global Filepath
    Filepath=filepath


def elencofileExploration(elenco,numerofile):
    global ElencoFile, nfile
    ElencoFile=elenco
    nfile=numerofile
    
autoscaling={}
def passaggioAutoscaling(valoripassati, risposta):
    
    global autoscaling
    if risposta=="si":
        
        autoscaling=valoripassati
        
    else:
        autoscaling={}
        

mean={}
def passaggioMean(valoripassati,risposta):
    global mean
    if risposta=="si":
        
        mean=valoripassati
        
    else: 
        mean={}

snv={}
def passaggioSnv(valoripassati,risposta):
    global snv
    if risposta=="si":
        snv=valoripassati
        
    else: 
        snv={}
        

savitzki={}
def passaggioSavitzki(valoripassati, risposta):
    global savitzki
    if risposta=="si":
        savitzki=valoripassati
        
    else:
        savitzki={}
        

snv_savitzki={}

def passaggioSnv_savitzki(valoripassati, risposta):
    global snv_savitzki
    if risposta=="si":
        snv_savitzki= valoripassati
        
    else:
        snv_savitzki={}
        
    

"""funzione per mantenere in memoria il file concatenato"""
def passaggioPCA(arrayconcatenato):
    global newarray
    newarray=arrayconcatenato
      


def Pca():
    """Funzione PCA"""
    variabile=newarray
    
    n_components=int(selected_option1)
    pca, transformed_data = compute_pca(n_components, variabile)
    fig1, fig2 = generate_scree_plots(pca)
    fig1.show()
    fig2.show()
   
    global variab, sostanze, scores, loadings
    variab = newarray.columns[0]
    sostanze = newarray.columns[1]
    scores, loadings = get_scores_and_loadings(pca, transformed_data, newarray)

    valori={}
    valori[1]=scores 
    stampaTabelle(valori,1, "Scores", True)
    
    valori[1]=loadings
    stampaTabelle(valori,1, "Loadings", True)
    
    
    
def graficiPca():
    """Funzione grafici PCA"""
    variabilex=str(selected_option2)
    variabiley=str(selected_option3)
    variabilez=str(selected_option4)
    
    fig, fig2 = generate_pca_html_2d_scatters(scores, loadings, sostanze, variabilex, variabiley)
    fig1 = generate_pca_html_3d_scatters(scores, sostanze, variabilex, variabiley, variabilez)

    """Visaulizzo gli scores"""
    fig.write_html('settima_figura.html', auto_open=False)
    html_file_path6 = os.path.join(os.getcwd(), "settima_figura.html")
    webview.create_window("Visualizzazione del grafico", url=html_file_path6, width=800, height=600)
    webview.start()
    fig1.write_html('ottava_figura.html', auto_open=False)
    html_file_path7 = os.path.join(os.getcwd(), "ottava_figura.html")
    webview.create_window("Visualizzazione del grafico", url=html_file_path7, width=800, height=600)
    webview.start()
    """Visualizzo i loadings"""
    fig2.write_html('nona_figura.html', auto_open=False)
    html_file_path8 = os.path.join(os.getcwd(), "nona_figura.html")
    webview.create_window("Visualizzazione del grafico", url=html_file_path8, width=800, height=600)
    webview.start()


def mean_confidence_interval(data, confidence):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m, m-h, m+h

def outlierDetection1():
    temp2=pd.DataFrame(newarray)
    n_components=int(selected_option1)
    hot_q_data, normalized_hot_q_data, Q, Tsq, Q_conf, Tsq_conf = detect_outliers(temp2, scores, loadings, sostanze, n_components)
    fig1, fig_normalized = generate_outliers_html_scatters(hot_q_data, normalized_hot_q_data, Q, Tsq, Q_conf, Tsq_conf, sostanze)
    fig1.write_html('decima_figura.html', auto_open=False)
    html_file_path9 = os.path.join(os.getcwd(), "decima_figura.html")
    webview.create_window("Visualizzazione del grafico", url=html_file_path9, width=800, height=600)
    webview.start()
    fig_normalized.write_html('undicesima_figura.html', auto_open=False)
    html_file_path10 = os.path.join(os.getcwd(), "undicesima_figura.html")
    webview.create_window("Visualizzazione del grafico", url=html_file_path10, width=800, height=600)
    webview.start()
    
    
  
def esportaTabelle():
    """Funzione esporta tabelle"""
    file= pd.DataFrame(newarray)
    filescores=pd.DataFrame(scores)
    fileloadings=pd.DataFrame(loadings)
    """ Trovo percorso al desktop del computer di chi usa il codice """
    path=os.path.expanduser("~/Desktop") + "/export_complete_table.xlsx"
    path2=os.path.expanduser("~/Desktop") + "/export_Scores.xlsx" 
    path3=os.path.expanduser("~/Desktop") + "/export_Loadings.xlsx"    
    
    """converto il file in un excel e lo salvo"""
    file.to_excel(path)
    filescores.to_excel(path2)
    fileloadings.to_excel(path3)
    
    lbl = Label(frameDatabase, text="File succesfully saved ", font=('arial', 25), bd=18, bg="white")
    lbl.grid(row=12, padx=100)
   
    
a=0
b=0
temp2={}
nuovoarray={}

def apriSceltaExploration():
    """ Creazione pagina che visualizza scelta_Exploration.py"""
    root = tk.Tk()
    root.title("Exploration choice")
    root.config(bg="white") 
    width = 800
    height = 900
    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    root.geometry("%dx%d+%d+%d" % (width, height, x, y))
    root.resizable(0,0)
        
    
    """Creazione frame"""
    global frameDatabase
    frameDatabase = Frame(root, bg="white")
    frameDatabase.pack(side=TOP, pady=20)
    
    """funzione per aggiungere colonne mancanti"""
    def aggiungicolonne(change):
        
            if len(change)!=0:
                temp4=""
                temp5=""
               
                temp4=pd.DataFrame(colonnaNomi)
                listaColonnaNomi=list(temp4.columns.values)
                nomeColonnaNomi=listaColonnaNomi[0]
                
                
                temp5=pd.DataFrame(colonnaID)
                listaColonnaID=list(temp5.columns.values)
                nomeColonnaID=listaColonnaID[0]
                
                newchange=pd.DataFrame(change)
                listanewchange=list(newchange.columns.values)
                nomenewchange=listanewchange[0]
                if str(nomenewchange)!=str(nomeColonnaID):
                    change.insert(0, column=str(nomeColonnaNomi), value=colonnaNomi)
                    change.insert(0, column=str(nomeColonnaID),value=colonnaID)
            
    global autoscaling, snv, mean, snv_savitzki, savitzki
    aggiungicolonne(autoscaling)
    aggiungicolonne(snv)
    aggiungicolonne(mean)
    aggiungicolonne(snv_savitzki)
    aggiungicolonne(savitzki)
    
    
    def passaggionewarray(nuovalista):
        global nuovoarray
        nuovoarray=nuovalista
        
    
    def ConcatenaDati():
        """Funzione concatena dati"""
        global a, temp2, nuovoarray
        
        def concatena(database, primo):
            """Funzione concatena dati, serve per ocncatenare le tabelle che gli vengono passate"""
            global a
            database=database.drop(database.columns[1], axis=1)
            result = fuse_data(primo, database)
            primo=result
            passaggionewarray(primo)
            newprimo={}
            newprimo[0]=primo
            stampaTabelle(newprimo,0, "tabella concatenata", True)
            passaggioPCA(primo)
            
        def controllo(parametro):
            """Funzione controllo, verifica se ci sono già tabelle inserite, oppure è la prima tabella da concatenare"""
            global nuovoarray, temp2
            if len(nuovoarray)==0:
                temp2[0]=parametro
                stampaTabelle(temp2,0,"tabella concatenata", True)
                passaggionewarray(temp2[0])
                passaggioPCA(temp2[0])
            else:
                temp2[0]=parametro
                concatena(temp2[0], nuovoarray)
                
 
       
        """serie di if per controllare che cosa seleziona l'utente ed effettuare controllo """
        if str(selected_option6)=="Autoscaling":
            controllo(autoscaling)
        
        if str(selected_option6)=="Mean Centering":
            controllo(mean)
            
        if str(selected_option6)=="SNV":
            controllo(snv)
        
        if str(selected_option6)=="Savitzki-Golay smoothing":
            controllo(savitzki)
        
        if str(selected_option6)=="SNV + Savitzki-Golay":
            controllo(snv_savitzki)
        
        for x in range (nfile):
            
            if str(ElencoFile[x])==str(selected_option6):
                controllo(Dati[x])
                
    """combo che contiene i differenti dati presi dai diversi preProcess e l'elenco dei file inseriti (con eventuali modifiche fatte)"""
    def combofile():
        listafile=[]
        for x in range(nfile) :
            listafile.append(ElencoFile[x])
        listafile.append("Autoscaling")
        listafile.append("Mean Centering")
        listafile.append("SNV")
        listafile.append("Savitzki-Golay smoothing")
        listafile.append("SNV + Savitzki-Golay") 
        combo6['values']=listafile
        
        def option_selected6(event):
            global selected_option6
            selected_option6 = combo6.get()
            print("You selected:", selected_option6)
        combo6.bind("<<ComboboxSelected>>", option_selected6)   
        
    
    
    
    combo6 = ttk.Combobox(frameDatabase, postcommand=combofile)
    combo6.set("Select Pre-Process")
    combo6.grid(row=1, columnspan=3, pady=15)
    
    
  
    """funzione che serve in acso in cui l'utente abbia sbagliato a creare la tabella concatenata, cosicchè non debba far ripartire l'applicazione"""
    def clearTabella():
        vuoto={}
        passaggionewarray(vuoto)
    
    """ Creazione button"""
    btn = Button(frameDatabase, text="Concatenate Data", font=('arial', 18), width=30, bg="red", command=ConcatenaDati)
    btn.grid(row=2, columnspan=2, pady=15)
    btn6 = Button(frameDatabase, text="Clear concatenate table", font=('arial', 18), width=30, bg="red", command=clearTabella)
    btn6.grid(row=3, columnspan=2, pady=15)
    
    """creazione combocomponenti"""
    def combocomponenti():
        
        global ID
        
        listarighe=['']
        df1 =pd.DataFrame(Dati[Num])
        column_headers = list(df1.columns.values)
        ID=column_headers[0]
        
        IDrighe = df1[ID].to_numpy()
        nrighe=len(IDrighe)
        
        for x in range (nrighe) :
            listarighe.append(x)
            
        combo['values']= listarighe   
        
        def option_selected(event):
                global selected_option1
                    
                selected_option1 = combo.get()
                
                print("You selected:", selected_option1)
        combo.bind("<<ComboboxSelected>>", option_selected)    
    
    """ Creazione combox, l'utente seleziona quali dati inserire nell'asse x dei grafici"""
    def combox():
        
        listacolonne=[]
        
        temp=scores.drop(scores.columns[[0,1]], axis=1)
        column_headers = list(temp.columns.values)
        for x in range (len(column_headers)):
             listacolonne.append(column_headers[x])
        
        combo2['values']= listacolonne
        
        def option_selected2(event):
            global selected_option2
                    
            selected_option2 = combo2.get()
                
            print("You selected:", selected_option2)
        combo2.bind("<<ComboboxSelected>>", option_selected2)  
    
    """ Creazione comboy, l'utente seleziona quali dati inserire nell'asse y dei grafici"""
    def comboy():
    
        listacolonne=[]
        temp=scores.drop(scores.columns[[0,1]], axis=1)
        column_headers = list(temp.columns.values)
        for x in range (len(column_headers)):
             listacolonne.append(column_headers[x])
        
        combo3['values']= listacolonne
        
        def option_selected3(event):
            global selected_option3
                    
            selected_option3 = combo3.get()
                
            print("You selected:", selected_option3)
        combo3.bind("<<ComboboxSelected>>", option_selected3)  
    
    """ Creazione comboz, l'utente seleziona quali dati inserire nell'asse z dei grafici"""
    def comboz():
        listacolonne=[]
        temp=scores.drop(scores.columns[[0,1]], axis=1)
        column_headers = list(temp.columns.values)
        for x in range (len(column_headers)):
             listacolonne.append(column_headers[x])
        
        combo4['values']= listacolonne
        
        def option_selected4(event):
            global selected_option4
                    
            selected_option4 = combo4.get()
                
            print("You selected:", selected_option4)
        combo4.bind("<<ComboboxSelected>>", option_selected4)      
    
    """inserimento combo e button"""
    combo = ttk.Combobox(frameDatabase, state='readonly', postcommand=combocomponenti)
    combo.set('Select nr PCs')
    combo.grid(row=4, columnspan=3, pady=15)
    btn2 = Button(frameDatabase, text="PCA", font=('arial', 18), width=30, bg="red", command=Pca)
    btn2.grid(row=5,columnspan=3, pady=15)
    combo2 = ttk.Combobox(frameDatabase, state='readonly', postcommand=combox)
    combo2.set('Select x')
    combo2.grid(row=6, columnspan=3, pady=15)
    
    combo3 = ttk.Combobox(frameDatabase, state='readonly', postcommand=comboy)
    combo3.set('Select y')
    combo3.grid(row=7, columnspan=3, pady=15)
    
    combo4 = ttk.Combobox(frameDatabase, state='readonly', postcommand=comboz)
    combo4.set('Select z')
    combo4.grid(row=8, columnspan=3, pady=15)
    btn3 = Button(frameDatabase, text="Pca plot", font=('arial', 18), width=30, bg="red",  command=graficiPca)
    btn3.grid(row=9, columnspan=2, pady=15 )
    btn4 = Button(frameDatabase, text="Outlier detection", font=('arial', 18), width=30, bg="red",  command=outlierDetection1)
    btn4.grid(row=10, columnspan=4, pady=15)
    btn5 = Button(frameDatabase, text="Export tables", font=('arial', 18), width=30, bg="red",  command=esportaTabelle)
    btn5.grid(row=11, columnspan=4, pady=15)
    lbl = Label(frameDatabase, text="", font=('arial', 25), bd=18, bg="white")
    lbl.grid(row=12, columnspan=4) 
    btnClose = tk.Button(root, text="Exit",font=('arial', 18), width=10, bg="red",command=root.withdraw )
    btnClose.place(rely=0.90, relx=0.6275)  
    
    """ Serve per visualizzare pagina costruita"""
    if __name__ == "__main__":
        root.mainloop()