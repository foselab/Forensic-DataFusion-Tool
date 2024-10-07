"""" Developed by Michele Verdi"""

""""Importazione librerie"""
import tkinter as tk
from tkinter import *
from pypdf import PdfReader
from tkinter.scrolledtext import ScrolledText



def apripdf():
    """ Creazione pagina che visualizza istruzioni.py"""
    root = tk.Tk()
    root.title("Home")
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
    frameDatabase = Frame(root, bg="white")
    frameDatabase.pack(side=TOP, pady=20)
    text= ScrolledText(frameDatabase,width= 70,height=25)
    text.pack(pady=20)
    
   
    """Lettura del pdf e inserimento nella pagina"""
    reader = PdfReader("Instruction.pdf")
    testo = ""
    for page in reader.pages:
        testo += page.extract_text() + "\n"
    
    """Creazione ed inserimento del testo, una textbox"""
    text.insert(INSERT, testo)
    text.config(state=DISABLED)
    
    """Creazione bottone per chiudere la pagina"""
    btnClose = tk.Button(root, text="exit",font=('arial', 18), width=10, bg="red",command=root.withdraw )
    btnClose.place(rely=0.85, relx=0.6275) 
    
    """ Serve per visualizzare pagina costruita"""
    if __name__ == "__main__":
        
        root.mainloop()

    
