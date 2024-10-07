"""" Developed by Michele Verdi"""

""""Importazione librerie"""
import tkinter as tk
from tkinter import * 
from pandastable import Table


   
    
def stampaTabelle(Dati,n,nometabella, valore):    
    """ Creazione pagina che visualizza stampa_tabelle.py"""
    
    root = tk.Tk()
    root.title(nometabella)
    root.config(bg="white") 
    width = 1200
    height = 800
    root.geometry("1200x800")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    root.geometry("%dx%d+%d+%d" % (width, height, x, y))
    root.resizable(0,0)
    
    """L'attributo topmost serve per mettere la pagina davanti a tutte le altre"""
    root.attributes("-topmost", valore)
    

    """ Creazione Frame e Table per visualizzare dati"""
    frameDatabase = Frame(root, bg="white")
    frameDatabase.pack(side=TOP, expand=True, fill="both")
    
    table=Table(frameDatabase, dataframe=Dati[n])
    table.show()
    
    #la parte commentata sotto può essere utilizzata per la visualizzazione in caso in cui la funzione table venga deprecata
    # Dovrà essere sistemata in un futuro, siccome ha un limite di spazio di visualizzazione dei dati
    
    """
    tv1 = ttk.Treeview(frame1)
    tv1.place(relheight=1, relwidth=1) # set the height and width of the widget to 100% of its container (frame1).

    treescrolly = tk.Scrollbar(frame1, orient="vertical", command=tv1.yview) # command means update the yaxis view of the widget
    treescrollx = tk.Scrollbar(frame1, orient="horizontal", command=tv1.xview) # command means update the xaxis view of the widget
    tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set) # assign the scrollbars to the Treeview Widget
    treescrollx.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
    treescrolly.pack(side="right", fill="y") # make the scrollbar fill the y axis of the Treeview widget
    
    def clear_data():
       tv1.delete(*tv1.get_children())
       return None
    
    display(Dati[n])
    
    clear_data()
    tv1["column"] = list(Dati[n].columns)
    tv1["show"] = "headings"
   
    for column in tv1["columns"]:
        tv1.heading(column, text=column) # let the column heading = column name
        tv1.column(column, width=100, stretch=FALSE)
        
     
   

    df_rows = Dati[n].to_numpy().tolist() # turns the dataframe into a list of lists
    
    for row in df_rows:
        tv1.insert("", "end", values=row) # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert
        
    """
    
    """ Serve per visualizzare pagina costruita"""
    if __name__ == "__main__":
        root.mainloop()   
        
        
        

    