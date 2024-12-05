from tkinter import *
import os
from PIL import Image, ImageTk

def crear_gif_con_fondo(root, gif_ruta, fondo_ruta, width, height, gif_height):  

    gif_image = Image.open(gif_ruta)  # Cargar el GIF
    framesNum = gif_image.n_frames # Número de frames que tiene el gif
    print(framesNum)

    # Obtener el ancho y alto originales del GIF
    gif_original_width, gif_original_height = gif_image.size

    # Calcular el nuevo ancho basado en la altura proporcionada (manteniendo la proporción original)
    aspect_ratio = gif_original_width / gif_original_height
    gif_width = int(aspect_ratio * gif_height)

    # Lista de todas las imágenes del gif
    frames = [
        PhotoImage(file=gif_ruta, format='gif -index %i' % (i)) for i in range(framesNum)
    ]
    frames_resized = []
    
    
    # Redimensionar los frames del gif según los nuevos tamaños proporcionados
    for frame in frames:
        frame_image = frame.subsample(int(frame.width() // gif_width), int(frame.height() // gif_height))
        frames_resized.append(frame_image)
    

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
        frame = frames_resized[ind]
        ind += 1
        if ind == framesNum:
            ind = 0
        # Actualizar la imagen en el canvas con una etiqueta "gif" para poder eliminarla después
        canvas.create_image(0, 0, image=frame, anchor=NW, tags="gif")
        root.after(100, update, ind)  # Número que regula la velocidad del gif

    # Iniciar el ciclo de actualización del gif
    root.after(0, update, 0)
    root.mainloop()


def logicaJuego4(): 
    
    #Fondo en canvas
    base_dir = os.path.dirname(os.path.abspath(__file__)) #Obtiene la direccion actual
    ruta_fondo = os.path.join(base_dir, "..", "images", "juego4", "fondoPatio.png")

    # Carga de gifts
    #Rutas
    ruta_insecto1 = os.path.join(base_dir, "..", "images", "juego4", "insecto1.gif")
    ruta_mascota1 = os.path.join(base_dir, "..", "images", "juego4", "perro2.gif")

    root = Tk()

    # Normalizar las rutas para asegurarse de que usan las barras invertidas correctamente
    ruta_gif_insecto1_normalizada = os.path.normpath(ruta_insecto1)
    ruta_gif_mascota1_normalizada = os.path.normpath(ruta_mascota1)
    ruta_imagen_fondo_normalizada = os.path.normpath(ruta_fondo)

    print(ruta_gif_insecto1_normalizada)
    print(ruta_imagen_fondo_normalizada)
    print(ruta_gif_mascota1_normalizada)
    crear_gif_con_fondo(root,ruta_gif_mascota1_normalizada, ruta_imagen_fondo_normalizada, width=1100, height=600, gif_height=100)
    
    root.mainloop()


if __name__ == "__main__":
    logicaJuego4()

