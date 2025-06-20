"""" Developed by Michele Verdi"""

""""Importazione librerie e funzioni presenti in altre pagine"""
import tkinter as tk
from tkinter import *
from initial_page import apriPagina_iniziale
from PIL import ImageTk, Image
from instruction import apripdf
import sys
import os

""" Creazione pagina che visualizza home.py  """
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

""" Serve per prendere il path del computer su cui sta girando il codice """
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(os.path.dirname(__file__))

    return os.path.join(base_path, "resources", relative_path)


""" Inserimento frame, button, label e logo"""
frameDatabase = Frame(root, bg="white")
frameDatabase.pack(side=TOP, pady=30)
lbl = Label(frameDatabase, text="Low Level Data Fusion\n Developed by" , font=('arial', 25), bd=18, bg="white")
lbl.grid(row=2, padx=60) 
logo_path = resource_path("logo.png")
img = ImageTk.PhotoImage(Image.open(logo_path))
lbl2=Label(frameDatabase, image=img)
lbl2.grid(row=3, padx=10) 
btn2 = Button(frameDatabase, text="Start", font=('arial', 18), width=30, bg="red", command=apriPagina_iniziale)
btn2.grid(row=4, columnspan=2, pady=30)
btn3 = Button(frameDatabase, text="Instruction", font=('arial', 18), width=30, bg="red", command=apripdf)
btn3.grid(row=5, columnspan=2, pady=30)

""" Serve per visualizzare pagina costruita"""
if __name__ == "__main__":
    root.protocol("WM_DELETE_WINDOW", root.destroy)
    root.mainloop()
   