import tkinter as tk
from .baseJuego import GameWindow
import random

def mostrar_instrucciones():
    root = tk.Tk()
    root.title("Instrucciones")
    root.geometry("370x450")
    
    tk.Label(root, text='Instrucciones', font=("Arial", 14, "bold")).pack(pady=10)
    tk.Label(root, text='Pellizca los insectos usando tus dedos índice y pulgar').pack(pady=20)
    
    def continuar():
        root.destroy()
        game_window = GameWindow("Juego4: Pellizca el insecto")
        game_window.setGameFrame(logicaJuego4)
        game_window.run()

    boton_continuar = tk.Button(root, text="Continuar", command=continuar)
    boton_continuar.pack(pady=20)
    root.mainloop()

def logicaJuego4(game_frame):
    game_frame.config(bg = 'green') #Probando juego 4 inicializar de manera simple
    