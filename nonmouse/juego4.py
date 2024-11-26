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
    #Fondo
    base_dir = os.path.dirname(os.path.abspath(__file__)) #Obtiene la direccion actual
    ruta_fondo = os.path.join(base_dir, "..", "images", "juego4", "fondo.jpg")
    fondo = cargar_imagen(ruta_fondo, altura=1200)
    
    if fondo:
        label_fondo = tk.Label(game_frame, image=fondo)
        label_fondo.place(relwidth=1, relheight=1)
        game_frame.image = fondo  # Mantener la referencia
    #Interfaz y logica del juego
    #Descripcion: Apreta los insectos, por cada insecto que aprietes subira tu score, pero si apretas un lugar incorrecto o un animal 
    #mas de tres veces el juego acabara, intenta tener el mayor score posible
    score = 0
    error = 0
    def movimientoAleatBoton(boton):
        x = random.randint(0,game_frame.winfo_width() - boton.winfo_width())
        y = random.randint(0,game_frame.winfo_with() - boton.winfo_width())
        boton.place(x=x,y=y)
    def apretasteInsecto(boton):
        print("Apretaste un insecto")
        score += 1
        movimientoAleatBoton(boton)
    def apretasteMal(boton):
        print("Apretaste mal, al tercer error se acaba el juego")
        error +=1

    def gameOver():
        print("Juego terminado")
    # Crear botones dinámicos
    print("Creando botones") #depuracion

    boton_insecto = tk.Button(game_frame, text="Insecto", bg="yellow", command=apretasteInsecto)
    boton_insecto.place(x=50, y=50)
    boton_animal = tk.Button(game_frame, text = "Animal", bg="red", command=apretasteMal)
    boton_animal.place(x=100, y=100)

    # Mover botones cada segundo
    def mover_botones():
        movimientoAleatBoton(boton_insecto)
        movimientoAleatBoton(boton_animal)
        game_frame.after(1000, mover_botones)
    


# Utiliza la misma función cargar_imagen para otros elementos como botones
def agregar_boton_con_imagen(frame, ruta_imagen, comando):
    imagen_boton = cargar_imagen(ruta_imagen, altura=50)
    if imagen_boton:
        boton = tk.Button(frame, image=imagen_boton, command=comando)
        boton.image = imagen_boton  # Mantener la referencia
        boton.pack(pady=10)
        return boton
    return None




    

