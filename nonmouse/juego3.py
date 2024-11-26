import tkinter as tk
from .baseJuego import GameWindow
from tkinter import messagebox
import random

def instrucciones():
    raiz = tk.Tk()
    raiz.title("Instrucciones")
    raiz.geometry("370x450")
    
    tk.Label(raiz, text='Instrucciones', font=("Arial", 14, "bold")).pack(pady=10)
    tk.Label(raiz, text='Usa tu dedo índice para seleccionar el color que se indica').pack(pady=20)
    
    def continuar():
        raiz.destroy()
        game_window = GameWindow("Juego 3: Selecciona los colores")
        game_window.run()

    boton_continuar = tk.Button(raiz, text="Continuar", command=continuar)
    boton_continuar.pack(pady=20)
    raiz.mainloop()