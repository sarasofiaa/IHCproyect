from tkinter import *
import os
from PIL import Image, ImageTk

def crear_gif_con_fondo(root, gif_ruta, fondo_ruta, width, height):   
    #root = Tk()

    framesNum = 2  # Número de frames que tiene el gif

    # Lista de todas las imágenes del gif
    frames = [PhotoImage(file=gif_ruta, format='gif -index %i' % (i)) for i in range(framesNum)]


    # Crear el canvas con las dimensiones de la imagen
    canvas = Canvas(root, width=width, height=height)
    canvas.pack()



    # Cargar la imagen de fondo
    fondo = Image.open(fondo_ruta)
    fondo_width, fondo_height = width, height
    fondo = fondo.resize((fondo_width, fondo_height))  # Ajustar tamaño de fondo al tamaño del canvas
    fondo_tk = ImageTk.PhotoImage(fondo)  # Convertir la imagen de fondo para Tkinter
    

    canvas.create_image(0, 0, image=fondo_tk, anchor=NW)  # Coloca la imagen de fondo

    def update(ind):
        """Actualiza la imagen gif."""
        canvas.delete("gif")  # Elimina las imágenes previas del gif
        frame = frames[ind]
        ind += 1
        if ind == framesNum:
            ind = 0
        # Actualizar la imagen en el canvas con una etiqueta "gif" para poder eliminarla después
        canvas.create_image(0, 0, image=frame, anchor=NW, tags="gif")
        root.after(100, update, ind)  # Número que regula la velocidad del gif

    # Iniciar el ciclo de actualización del gif
    root.after(0, update, 0)
    root.mainloop()


root = Tk()

# Obtener la ruta normalizada
base_dir = os.path.dirname(os.path.abspath(__file__))  # Directorio actual
project_dir = os.path.dirname(base_dir)  # Subir un nivel para llegar a la raíz del proyecto
ruta_imagen_fondo = os.path.join(project_dir, "images", "juego4", "fondoPatio.png")
ruta_gif_insecto1 = os.path.join(project_dir, "images", "juego4", "insecto1.gif")

# Normalizar las rutas para asegurarse de que usan las barras invertidas correctamente
ruta_gif_insecto1_normalizada = os.path.normpath(ruta_gif_insecto1)
ruta_imagen_fondo_normalizada = os.path.normpath(ruta_imagen_fondo)

print(ruta_gif_insecto1_normalizada)
print(ruta_imagen_fondo_normalizada)
crear_gif_con_fondo(root,ruta_gif_insecto1_normalizada, ruta_imagen_fondo_normalizada, width=1100, height=600)