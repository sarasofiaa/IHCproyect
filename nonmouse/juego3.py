from tkinter import *
import os
import random
import pygame
from PIL import Image, ImageTk

pygame.mixer.init()

# Variables globales
colores_pad = ["red", "blue", "green", "yellow"]
secuencia = []
entrada_usuario = []
nivel = 1
nivel_maximo = 10
puntaje = 0
mejor_nivel = 0

sonidos = {
    "red": pygame.mixer.Sound(os.path.join("sounds", "Sound1.wav")),
    "blue": pygame.mixer.Sound(os.path.join("sounds", "Sound2.wav")),
    "green": pygame.mixer.Sound(os.path.join("sounds", "Sound3.wav")),
    "yellow": pygame.mixer.Sound(os.path.join("sounds", "Sound4.wav")),
    "passed": pygame.mixer.Sound(os.path.join("sounds", "passed.wav")),
    "error": pygame.mixer.Sound(os.path.join("sounds", "error.wav")),
}

# Función para actualizar el marcador
def actualizar_marcador(label):
    label.config(
        text=f"Nivel: {nivel} | Puntaje: {puntaje} | Mejor Nivel: {mejor_nivel}"
    )

# Verificar la entrada del usuario
def verificar_entrada(canvas, marcador):
    global secuencia, entrada_usuario, nivel, puntaje, mejor_nivel

    if entrada_usuario == secuencia:
        sonidos["passed"].play()
        puntaje += nivel * 10
        mejor_nivel = max(mejor_nivel, nivel)
        nivel += 1
        entrada_usuario = []

        if nivel > nivel_maximo:
            mostrar_resultado(canvas.master, "¡Felicidades! Has completado el nivel máximo.")
            reiniciar_juego(canvas, marcador)
        else:
            canvas.after(1000, iniciar_nivel, canvas, marcador)
    elif len(entrada_usuario) >= len(secuencia):
        sonidos["error"].play()
        mostrar_resultado(canvas.master, "¡Perdiste! Inicia desde el nivel 1.")
        reiniciar_juego(canvas, marcador)

# Reiniciar el juego
def reiniciar_juego(canvas, marcador):
    global nivel, puntaje, secuencia
    nivel = 1
    puntaje = 0
    secuencia = []
    iniciar_nivel(canvas, marcador)

# Iniciar un nivel
def iniciar_nivel(canvas, marcador):
    global secuencia, entrada_usuario
    entrada_usuario = []
    generar_secuencia()
    mostrar_secuencia(canvas)
    actualizar_marcador(marcador)

# Generar la secuencia de colores
def generar_secuencia():
    global secuencia, nivel
    secuencia = [random.choice(colores_pad) for _ in range(nivel)]

# Mostrar la secuencia al usuario
def mostrar_secuencia(canvas):
    for i, color in enumerate(secuencia):
        canvas.after(i * 500, lambda c=color: parpadear_color(canvas, c))

# Hacer parpadear un color
def parpadear_color(canvas, color):
    sonidos[color].play()
    canvas.itemconfig(color, fill="white")
    canvas.after(500, lambda: canvas.itemconfig(color, fill=color))

# Manejar clics del usuario
def manejar_click(event, canvas, marcador):
    global entrada_usuario
    x, y = event.x, event.y
    item = canvas.find_closest(x, y)
    tags = canvas.gettags(item)

    if tags:
        color = tags[0]
        if color in colores_pad:
            sonidos[color].play()
            entrada_usuario.append(color)
            verificar_entrada(canvas, marcador)

# Crear el pad de colores
def crear_pad_colores(canvas):
    pad_size = 200
    for i, color in enumerate(colores_pad):
        x0 = (i % 2) * pad_size
        y0 = (i // 2) * pad_size
        x1 = x0 + pad_size
        y1 = y0 + pad_size
        canvas.create_rectangle(x0, y0, x1, y1, fill=color, tags=color)

# Mostrar el resultado
def mostrar_resultado(root, mensaje):
    ventana_resultado = Toplevel()
    ventana_resultado.title("Resultado")
    ventana_resultado.geometry("400x200")
    ventana_resultado.resizable(False, False)

    label_mensaje = Label(
        ventana_resultado, text=mensaje, font=("Comic Sans MS", 16), fg="blue"
    )
    label_mensaje.pack(pady=20)

    boton_cerrar = Button(ventana_resultado, text="Cerrar", command=ventana_resultado.destroy)
    boton_cerrar.pack(pady=10)

# Lógica principal del juego
def logicaJuego3(frame):
    global nivel, puntaje, mejor_nivel

    canvas = Canvas(frame, width=400, height=400)
    canvas.pack()

    marcador = Label(
        frame,
        text="Nivel: 1 | Puntaje: 0 | Mejor Nivel: 0",
        font=("Comic Sans MS", 14),
        bg="lightyellow",
        fg="black",
        width=40,
        relief="ridge",
    )
    marcador.pack(pady=10)

    boton_reiniciar = Button(
        frame,
        text="Reiniciar",
        font=("Comic Sans MS", 12),
        bg="lightblue",
        command=lambda: reiniciar_juego(canvas, marcador),
    )
    boton_reiniciar.pack(pady=5)

    crear_pad_colores(canvas)
    canvas.bind("<Button-1>", lambda event: manejar_click(event, canvas, marcador))
    iniciar_nivel(canvas, marcador)

if __name__ == "__main__":
    root = Tk()
    root.title("Juego del Pad de Colores")
    root.geometry("500x600")
    root.config(bg="lightpink")

    frame_juego = Frame(root, bg="lightpink")
    frame_juego.pack(pady=20)

    logicaJuego3(frame_juego)
    root.mainloop()
