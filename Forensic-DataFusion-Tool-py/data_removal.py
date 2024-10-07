import tkinter as tk
from tkinter import *
from tkinter import ttk
import pandas as pd
from Pre_Processing import passaggioPreProcessing
from stampa_tabelle import stampaTabelle
from scelta_Exploration import passaggioExploration

def passaggiodataremoval(dati,num):
    global Dati
    Dati=dati
    global Num
    Num=num
    
def elencofile(elenco,numerofile):
    global ElencoFile, nfile
    ElencoFile=elenco
    nfile=numerofile
    

def dataRemoval():
    
    
    root = tk.Tk()
    root.title("Data removal")
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
   
    
    global frameDatabase
    
    
   
    frameDatabase = Frame(root, bg="white")
    frameDatabase.pack(side=TOP, pady=60)
    
    def comborighe():
        
        global ID
        
        listarighe=['']
        df1 =pd.DataFrame(Dati[Num])
        column_headers = list(df1.columns.values)
        ID=column_headers[0]
        
        IDrighe = df1[ID].to_numpy()
        nrighe=len(IDrighe)
        
       
            
        for x in range (nrighe) :
            listarighe.append(IDrighe[x])
            
       
                
        combo['values']= listarighe   
        
        
            
        def option_selected(event):
                global selected_option1
                    
                selected_option1 = combo.get()
                
                print("You selected:", selected_option1)
        combo.bind("<<ComboboxSelected>>", option_selected)
     
    def combofile():
        listafile=['']
        for x in range(nfile) :
            listafile.append(ElencoFile[x])
            
        combo2['values']=listafile
        
        def option_selected2(event):
            global selected_option2
            selected_option2 = combo2.get()
              
            print("You selected:", selected_option2)
            
            
        combo2.bind("<<ComboboxSelected>>", option_selected2)
        
     
    
    def combocolonne():
        global indice
        valore=selected_option2
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
            listacolonne=['']
        
            for y in range (ncolonne):
                listacolonne.append(IDcolonne[y])
        
            combo3['values']= listacolonne
            def option_selected3(event):
                global selected_option3
                selected_option3 = combo3.get()
                print("You selected:", selected_option3)
            combo3.bind("<<ComboboxSelected>>", option_selected3)  
        
         
    combo = ttk.Combobox(frameDatabase, state='readonly', postcommand=comborighe)
    combo.set('Select ID')
    combo.grid(row=2, columnspan=3, pady=20)
    
    
    combo2= ttk.Combobox(frameDatabase, state='readonly' ,postcommand=combofile)
    combo2.set('Select File')
    combo2.grid(row=4, columnspan=3, pady=20)
    
    
    combo3= ttk.Combobox(frameDatabase, state='readonly', postcommand=combocolonne)
    combo3.set('Select Variable')
    combo3.grid(row=5, columnspan=3, pady=20) 
       
        
    global df, nuovalista, array
    df={}
    nuovalista={}
    array={}
    
    global b,c
    
    
    def removerow():
        
        riga=selected_option1 
        b=0
        c=0
        indicetemp=0
        if riga!='':
            for x in range (Num+1):
                array[b]=Dati[x]
                df =pd.DataFrame(array[b])
                column_headers = list(df.columns.values)
                ID=column_headers[0]
                IDrighe = df[ID].to_numpy()
                nrighe=len(IDrighe)
                for x in range (nrighe) :
                    if str(IDrighe[x])==str(riga):
                        indicetemp=x
        
                temp=df.drop(df.index[indicetemp])
                nuovalista[c]=temp
                stampaTabelle(nuovalista,c,"Dati aggiornati", True)
                
                b+=1
                c+=1
            combo.set('Select')
            passaggiodataremoval(nuovalista, c-1)
            passaggioPreProcessing(nuovalista,c-1)
            passaggioExploration(nuovalista,c-1)
            
        
        if riga=='':
            for x in range (Num+1):
                array[b]=Dati[x]
                df = pd.DataFrame(array[b])
                nuovalista[c]=df
                stampaTabelle(nuovalista,c, "Dati aggiornati" , True)
                
                b+=1
                c+=1
            passaggiodataremoval(nuovalista, c-1)
            passaggioPreProcessing(nuovalista,c-1)
            passaggioExploration(nuovalista,c-1)
            
        
            
            
    global data, data2 , newlist  
    data={}
    data2={}
    newlist={}
        
    def removecolumn() :
        colonna=selected_option3  
        val=0
        b=0
        c=0
       
        if colonna!= '':
            for x in range (Num+1):
                if x==indice:
                    dataframe= pd.DataFrame(Dati[indice])
            
                    column_headers=list(dataframe.columns.values)
                    for y in range (len(column_headers)):
                        if str(column_headers[y])==str(colonna):
                            val=y
                    temp=dataframe     
                    temp=temp.drop(temp.columns[val], axis=1)
                    newlist[c]=temp
                    stampaTabelle(newlist,c,"Dati aggiornati", True)
                    c+=1
                 
                else : 
                    data2[b]=Dati[x]
                    df = pd.DataFrame(data2[b])

                    newlist[c]=df
                    b+=1
                    c+=1
            combo2.set('Select')
            combo3.set('Select')
            passaggiodataremoval(newlist, c-1)
            passaggioPreProcessing(newlist,c-1) 
            passaggioExploration(newlist,c-1)   
        
        if colonna=='':
             for x in range (Num+1):
                 array[b]=Dati[x]
                 df = pd.DataFrame(array[b])
                 newlist[c]=df
                 stampaTabelle(newlist,c,"Dati aggiornati", True)
                 b+=1
                 c+=1
             passaggiodataremoval(newlist, c-1)
             passaggioPreProcessing(newlist,c-1)
             passaggioExploration(newlist,c-1)
               
        
   
    btn2 = Button(frameDatabase, text="Remove row", font=('arial', 18), width=30, bg="red", command=removerow)
    btn2.grid(row=3, columnspan=3, pady=20)
    btn3 = Button(frameDatabase, text="Remove column", font=('arial', 18), width=30, bg="red", command=removecolumn)
    btn3.grid(row=6, columnspan=3, pady=20)
    btnClose = tk.Button(root, text="Exit",font=('arial', 18), width=10, bg="red",command=root.withdraw )
    btnClose.place(rely=0.85, relx=0.6275)
        
    
    if __name__ == "__main__":
            root.mainloop()
            
