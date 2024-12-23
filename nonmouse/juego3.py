from tkinter import *
import os
import random
from PIL import Image, ImageTk
from .baseJuego import GameWindow

# Variables globales
colores_pad = ["red", "blue", "green", "yellow"]  # Colores del pad
secuencia = []  # Secuencia de colores generada
entrada_usuario = []  # Secuencia ingresada por el usuario
nivel = 1  # Nivel actual
tiempo = 20000  # Tiempo de juego en milisegundos (20 segundos)

# Crear el pad de colores
def crear_pad_colores(root, canvas, width, height):
    """Crea un pad interactivo de colores."""
    pad_size = 200  # Tamaño de cada sección del pad
    pad_coords = []

    for i, color in enumerate(colores_pad):
        x0 = (i % 2) * pad_size
        y0 = (i // 2) * pad_size
        x1 = x0 + pad_size
        y1 = y0 + pad_size
        pad_coords.append((x0, y0, x1, y1))
        canvas.create_rectangle(x0, y0, x1, y1, fill=color, tags=color)

    return pad_coords

# Generar la secuencia de colores
def generar_secuencia():
    global secuencia, nivel
    secuencia = [random.choice(colores_pad) for _ in range(nivel)]
    print("Secuencia generada:", secuencia)

# Mostrar la secuencia al usuario
def mostrar_secuencia(canvas):
    """Muestra la secuencia de colores al usuario parpadeando los colores en el pad."""
    for i, color in enumerate(secuencia):
        canvas.after(i * 1000, lambda c=color: parpadear_color(canvas, c))

# Hacer parpadear un color
def parpadear_color(canvas, color):
    """Simula el parpadeo de un color en el canvas."""
    canvas.itemconfig(color, fill="white")
    canvas.after(500, lambda: canvas.itemconfig(color, fill=color))

# Verificar la entrada del usuario
def verificar_entrada(canvas):
    global secuencia, entrada_usuario, nivel

    if entrada_usuario == secuencia:
        nivel += 1
        entrada_usuario = []
        canvas.after(1000, iniciar_nivel, canvas)
    elif len(entrada_usuario) >= len(secuencia):
        print("¡Has perdido!")
        mostrar_resultado(canvas.master, "¡Perdiste! Intenta de nuevo.")

# Iniciar un nivel
def iniciar_nivel(canvas):
    global secuencia, entrada_usuario
    entrada_usuario = []
    generar_secuencia()
    mostrar_secuencia(canvas)

# Manejar clics del usuario
def manejar_click(event, canvas):
    global entrada_usuario
    x, y = event.x, event.y
    item = canvas.find_closest(x, y)
    tags = canvas.gettags(item)

    if tags:
        color = tags[0]
        if color in colores_pad:
            entrada_usuario.append(color)
            print("Entrada del usuario:", entrada_usuario)
            verificar_entrada(canvas)

# Función para mostrar el resultado
def mostrar_resultado(root, mensaje):
    """Crea una ventana modal simple para mostrar el mensaje."""
    ventana_resultado = Toplevel()
    ventana_resultado.title("Resultado")
    ventana_resultado.geometry("300x150")
    ventana_resultado.resizable(False, False)

    label_mensaje = Label(ventana_resultado, text=mensaje, font=("Arial", 12), wraplength=250)
    label_mensaje.pack(pady=20)

    boton_cerrar = Button(ventana_resultado, text="Cerrar", command=ventana_resultado.destroy)
    boton_cerrar.pack(pady=10)

    ventana_resultado.transient(root)
    ventana_resultado.grab_set()
    root.wait_window(ventana_resultado)

def logicaJuego3(frame):
    """Lógica principal del juego del pad de colores."""
    root = frame.master
    canvas = Canvas(frame, width=400, height=400)
    canvas.pack()

    # Crear el pad de colores
    crear_pad_colores(root, canvas, width=400, height=400)

    # Vincular clics del usuario
    canvas.bind("<Button-1>", lambda event: manejar_click(event, canvas))

    # Iniciar el primer nivel
    iniciar_nivel(canvas)

if __name__ == "__main__":
    root = Tk()
    root.title("Juego del Pad de Colores")

    frame_juego = Frame(root, width=400, height=400)
    frame_juego.pack()

    logicaJuego3(frame_juego)

    root.mainloop()