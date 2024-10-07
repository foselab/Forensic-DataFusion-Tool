"""" Developed by Michele Verdi"""

""""Importazione librerie e funzioni dalle altre pagine"""
import tkinter as tk
from tkinter import *
from tkinter import ttk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt #traditional plots
import plotly.express as px #dynamic plots
from stampa_tabelle import stampaTabelle
import scipy.stats
import os
import webview
from stampa_tabelle import stampaTabelle
from sklearn import decomposition

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
    pca = decomposition.PCA(n_components)  
    variabile=variabile.drop(variabile.columns[[0,1]], axis=1)
    variabile.columns=variabile.columns.astype(str)
    pca_model = pca.fit_transform(variabile)
    PC_values = np.arange(pca.n_components_) + 1  
    plt.plot(PC_values, pca.explained_variance_ratio_, 'ro-', linewidth=2)
    plt.title('Scree Plot')
    plt.xlabel('Principal Component')
    plt.ylabel('Proportion of Variance Explained')
    plt.show()
    
    """Valuta la Explained variance (EV%) e il cumulative explained variance (CEV%)""" 
    print ("Proportion of Variance Explained : ", pca.explained_variance_ratio_)  
    out_sum = np.cumsum(pca.explained_variance_ratio_)  
    print ("Cumulative Prop. Variance Explained: ", out_sum)
    
    
    """ Valuta lo scree plot (sulla Cumulativ explained variance)"""
    plt.plot(PC_values, np.cumsum(pca.explained_variance_ratio_), 'ro-', linewidth=2)
    plt.title('Scree Plot')
    plt.xlabel('Principal Component')
    plt.ylabel('Cumulative Prop. Variance Explained')
    plt.show()
    
    
    """Ricostruisco il modello usando un numero deciso di PCs"""
    pca2 = decomposition.PCA(n_components) 
    pca2_model=pca2.fit_transform(variabile)
   
    global variab, sostanze, scores
    column_headers = list(newarray.columns.values)
    variab=column_headers[0]
    sostanze=column_headers[1] 
    
    scores = pd.DataFrame(data = pca2_model )
    scores.columns = ['PC'+str(x) for x in range(1, len(scores.columns)+1)] 
    scores.index = newarray.index       
    scores = pd.concat([newarray[variab], newarray[sostanze], scores], axis = 1) 
    valori={}
    valori[1]=scores 
    stampaTabelle(valori,1, "Scores", True)
    
    """Preparo il dataframe loadings"""
    global loadings
    newarray.columns=newarray.columns.astype(str)
    temp=newarray.drop(newarray.columns[[0,1]], axis=1)
    
    loadings = pd.DataFrame(pca.components_.T, index=temp.columns) 
    loadings.columns = ['PC'+str(x) for x in range(1, len(loadings.columns)+1)] 
    loadings["Attributes"] = loadings.index
    
    valori[1]=loadings
    stampaTabelle(valori,1, "Loadings", True)
    
    
    
def graficiPca():
    """Funzione grafici PCA"""
    variabilex=str(selected_option2)
    variabiley=str(selected_option3)
    variabilez=str(selected_option4)
    
    """Visaulizzo gli scores"""
    fig = px.scatter(scores, x=variabilex, y=variabiley, color=str(sostanze), hover_data=[str(sostanze)], hover_name=scores.index) 
    fig.update_xaxes(zeroline=True, zerolinewidth=1, zerolinecolor='Black')
    fig.update_yaxes(zeroline=True, zerolinewidth=1, zerolinecolor='Black')
    fig.update_layout(
    height=600,
    width=800,
    title_text='Scores Plot colored by'+ str(sostanze))
    fig.write_html('settima_figura.html', auto_open=False)
    html_file_path6 = os.path.join(os.getcwd(), "settima_figura.html")
    webview.create_window("Visualizzazione del grafico", url=html_file_path6, width=800, height=600)
    webview.start()
    
    fig1 = px.scatter_3d(scores, x=variabilex, y=variabiley, z=variabilez,color=str(sostanze), hover_data=[str(sostanze)], hover_name=scores.index)
    fig1.write_html('ottava_figura.html', auto_open=False)
    html_file_path7 = os.path.join(os.getcwd(), "ottava_figura.html")
    webview.create_window("Visualizzazione del grafico", url=html_file_path7, width=800, height=600)
    webview.start()
    """Visualizzo i loadings"""
    fig2 = px.scatter(loadings, x=variabilex, y=variabiley, text="Attributes")  
    fig2.update_xaxes(zeroline=True, zerolinewidth=1, zerolinecolor='Black')
    fig2.update_yaxes(zeroline=True, zerolinewidth=1, zerolinecolor='Black')
    fig2.update_traces(textposition='top center')
    fig2.update_layout(
    height=600,
    width=800,
    title_text='Loadings Plot')
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
    X1=temp2.drop(temp2.columns[[0,1]], axis=1)
   
    X1.columns=X1.columns.astype(str)
    n_components=int(selected_option1)
    """Prendo gli scores PCA"""
    T = scores.iloc[:,2:n_components+2] 
    
    """Prendo i loadings PCA"""
    P = loadings.iloc[:,0:n_components]  
    
    """Calcolo error array"""
    Err = X1 - np.dot(T,P.T)  
    
    """Calcolo Q-residuals"""
    Q = np.sum(Err**2, axis=1)
    """Calcolo Hotelling's T-squared"""
    Tsq = np.sum((T/np.std(T, axis=0))**2, axis=1)  

    
    """Fisso il livello di confidenza"""
    conf = 0.95 
    Tsq_conf = mean_confidence_interval(Tsq.values, confidence=conf)
    Tsq_conf = Tsq_conf[2]
    Q_conf = mean_confidence_interval(Q.values, confidence=conf)
    Q_conf = Q_conf[2]
    
    """Creo un dataframe usando solo T2 e Q-residuals"""
    hot_q_data = {'T2': Tsq, 'Qres': Q, str(sostanze): newarray[str(sostanze)]}  
    hot_q_data = pd.DataFrame(hot_q_data, index = newarray.index)
    valori2={}
    valori2[1]= hot_q_data
    stampaTabelle(valori2,1, "Dataframe with T2 and Q-Residuals", False)
   
    """Plot l'Hotelling T2 vs  Q-residuals plot"""
    fig1 = px.scatter(hot_q_data, x="T2", y="Qres", hover_data={'Sample': (hot_q_data.index)},  color = str(sostanze))  
    fig1.add_hline(y=abs(Q_conf),line_dash="dot", line_color='Red')
    fig1.add_vline(x=Tsq_conf,line_dash="dot", line_color='Red')
    fig1.update_traces(textposition='top center')
    fig1.update_layout(
        height=600,
        width=800,
    title_text="Hotelling's T2 vs Q-residuals")
    fig1.write_html('decima_figura.html', auto_open=False)
    html_file_path9 = os.path.join(os.getcwd(), "decima_figura.html")
    webview.create_window("Visualizzazione del grafico", url=html_file_path9, width=800, height=600)
    webview.start()
    
    """Normalizzo il Q-residuals e l'Hotelling's T-squared"""
    normalized_Q = Q / np.max(Q)
    normalized_Tsq = Tsq / np.max(Tsq)
    
    """Creo dataframe con valori normalizzati"""
    normalized_hot_q_data = {'T2': normalized_Tsq, 'Qres': normalized_Q, str(sostanze): newarray[str(sostanze)]} 
    normalized_hot_q_data = pd.DataFrame(normalized_hot_q_data, index=newarray.index)

    
    """plot il normalizzato Hotelling T2 vs Q-residuals plot"""
    fig_normalized = px.scatter(
    normalized_hot_q_data, x="T2", y="Qres", 
    hover_data={'Sample': (normalized_hot_q_data.index)}, color=str(sostanze))
    fig_normalized.add_hline(y=abs(Q_conf / np.max(Q)), line_dash="dot", line_color='Red')
    fig_normalized.add_vline(x=Tsq_conf / np.max(Tsq), line_dash="dot", line_color='Red')
    fig_normalized.update_traces(textposition='top center')
    fig_normalized.update_layout(
        height=600,
        width=800,
        title_text="Normalized Hotelling's T2 vs Q-residuals"
    )
    
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
            column_headers = list(database.columns.values)
            ID=column_headers[0]
            ID=str(ID)
            result= pd.merge(primo,database, on=[ID] )
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