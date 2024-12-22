from tkinter import *
import random
import os
from PIL import Image, ImageTk
from .baseJuego import GameWindow

# variables globales
color_pass = 0
tiempo = 20000

def background(root, fondo_ruta, ancho, alto):
    canvas = Canvas(root, width = ancho, height = alto)
    canvas.pack

    # Cargar la imagen de fondo
    fondo = Image.open(fondo_ruta)
    an_fondo, al_fondo = ancho, alto
    fondo = fondo.resize((an_fondo, al_fondo))
    fondo_tk = ImageTk.PhotoImage(fondo)

    canvas.create_image(0, 0, image = fondo_tk, anchor = NW)

# función para que los colores aparezcan aleatoriamente
def generar_color_aleatorio():

#función para que el juego pase el color cuando sea correto
def color_correcto():

#función para hacer conteo del puntaje
def puntaje():

#función para mostrar el resultado al hacer click en un boton
def mostrar_resultado(root, mensaje):
    ventana_resultado = Toplevel()
    ventana_resultado.title("Resultado")
    ventana_resultado.geometry("300x150")  # Dimensiones de la ventana
    ventana_resultado.resizable(False, False)  # Evitar que la ventana sea redimensionable

    # Etiqueta para mostrar el mensaje
    label_mensaje = Label(ventana_resultado, text=mensaje, font=("Arial", 12), wraplength=250)
    label_mensaje.pack(pady=20)

    # Botón para cerrar la ventana
    boton_cerrar = Button(ventana_resultado, text="Cerrar", command=ventana_resultado.destroy)
    boton_cerrar.pack(pady=10)

    # Centrar la ventana modal sobre la ventana principal
    ventana_resultado.transient(root)  # Relacionar la ventana con la ventana principal
    ventana_resultado.grab_set()  # Hacer que sea modal (previene la interacción con otras ventanas)
    root.wait_window(ventana_resultado)  # Esperar hasta que la ventana sea cerrada

def logicaJuego3(frame):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ruta_fondo = os.path.join(base_dir, "..", "images", "juego3", "fondo.avif")

    canvas = Canvas(frame, width=1100, height=600)
    canvas.pack()

    ruta_img_fondo_norm = os.path.normpath(ruta_fondo)
    background(frame, ruta_fondo, width=1100, height=600)

def mostrar_base_juego(frame):
    # Ejemplo simple de usar un texto o elementos gráficos para la base del juego
    label = Label(frame, text="¡Bienvenido al juego!", font=("Arial", 24))
    label.pack(pady=20)

if __name__ == "__main__":
    root = Tk()
    root.title("Juego con Lógica y Base de Juego")

    paned_window = PanedWindow(root, orient=HORIZONTAL)
    paned_window.pack(fill=BOTH, expand=True)

    # Crear el panel para la lógica del juego
    panel_juego = Frame(paned_window, width=600, height=600)
    paned_window.add(panel_juego)

    # Crear el panel para la base del juego
    panel_base = Frame(paned_window, width=400, height=600)
    paned_window.add(panel_base)

     # Llamar a las funciones correspondientes para llenar cada sección
    logicaJuego3(panel_juego)  # Lógica del juego en el primer panel
    mostrar_base_juego(panel_base)  # Interfaz base en el segundo panel

    root.mainloop()