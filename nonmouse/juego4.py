import tkinter as tk
from .baseJuego import GameWindow
import random
from PIL import Image, ImageTk
import os
from .utils2 import cargar_imagen


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
    base_dir = os.path.dirname(os.path.abspath(__file__)) #Obtiene la direccion actual
    ruta_fondo = os.path.join(base_dir, "..", "images", "juego4", "fondo.jpg")
    fondo = cargar_imagen(ruta_fondo, altura=800)
    
    if fondo:
        label_fondo = tk.Label(game_frame, image=fondo)
        label_fondo.place(relwidth=1, relheight=1)
        game_frame.image = fondo  # Mantener la referencia
    
    game_frame.config(bg='green')  # Funcional

# Utiliza la misma función cargar_imagen para otros elementos como botones
def agregar_boton_con_imagen(frame, ruta_imagen, comando):
    imagen_boton = cargar_imagen(ruta_imagen, altura=50)
    if imagen_boton:
        boton = tk.Button(frame, image=imagen_boton, command=comando)
        boton.image = imagen_boton  # Mantener la referencia
        boton.pack(pady=10)
        return boton
    return None

# Lógica de ejemplo para agregar un botón con imagen
def ejemplo_boton():
    print("Botón presionado")


    

