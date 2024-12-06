from tkinter import *
import os
import random

from PIL import Image, ImageTk

# Definir posiciones Y como variable global
posiciones_y = [90, 110, 110, 210, 210, 310]  
def crear_gif_con_fondo(root, gif_rutas, fondo_ruta, width, height, gif_height):  

    frames_resized_all_gifs = []

    # Crear el canvas con las dimensiones de la imagen
    canvas = Canvas(root, width=width, height=height)
    canvas.pack()

    # Cargar la imagen de fondo
    fondo = Image.open(fondo_ruta)
    fondo_width, fondo_height = width, height
    fondo = fondo.resize((fondo_width, fondo_height))  # Ajustar tamaño de fondo al tamaño del canvas
    fondo_tk = ImageTk.PhotoImage(fondo)  # Convertir la imagen de fondo para Tkinter
    
    canvas.create_image(0, 0, image=fondo_tk, anchor=NW)  # Coloca la imagen de fondo

    for gif_ruta in gif_rutas:
        gif_image = Image.open(gif_ruta)  # Cargar el GIF
        framesNum = gif_image.n_frames # Número de frames que tiene el gif
        print(framesNum)

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
        
        # Almacenar los frames redimensionados de cada gif
        frames_resized_all_gifs.append(frames_resized)

    # Diccionario para almacenar el ID  de cada GIF
    gif_ids = {}

    #Actualizar la imagen del gif en el canvas
    def update_gif(ind, frames_resized, tag, pos_x, pos_y):
        """Actualiza la imagen gif."""
        if tag not in gif_ids:
            return
        
        canvas.delete(tag)  # Elimina las imágenes previas del gif
        frame = frames_resized[ind]
        ind += 1
        if ind == len(frames_resized):
            ind = 0
        # Actualizar la imagen en el canvas con una etiqueta "gif" para poder eliminarla después
        canvas.create_image(190, 80, image=frame, anchor=NW, tags=tag)
        # Reprograma la actualización del GIF
        gif_ids[tag] = root.after(100, update_gif, ind, frames_resized, tag, pos_x, pos_y) # Número que regula la velocidad del gif

    # Iniciar el ciclo de actualización de cada gif
    for idx, frames_resized in enumerate(frames_resized_all_gifs):
       # Elegir una posición aleatoria en el eje X (dentro del ancho de la ventana)
        pos_x = random.randint(0, width - 1)
        # Elegir una posición aleatoria en el eje Y desde las posiciones predefinidas (globales)
        pos_y = random.choice(posiciones_y)

        tag = f"gif{idx}"
        # Guardar el ID del after para cada GIF
        gif_ids[tag] = root.after(0, update_gif, 0, frames_resized, tag, pos_x, pos_y)

    # Función para eliminar el GIF al hacer clic
    def eliminar_gif(event):
        # Obtener las coordenadas del clic       
        x, y = event.x, event.y
        entidad_id = canvas.find_closest(x, y)[0]  # Obtén el ID del objeto más cercano
        print(f"Entidad ID: {entidad_id}")
        tags = canvas.gettags(entidad_id)  # Obtén las tags asociadas al objeto
        print(f"Tags: {tags}")

        if tags:
            tag = tags[0]  # Tomamos el primer tag
            print(f"Tag del objeto: {tag}")
            # Eliminamos el GIF si existe
            if tag in gif_ids:
                root.after_cancel(gif_ids[tag])  # Detener la actualización
                del gif_ids[tag]  # Eliminar el 'after' del diccionario
                canvas.delete(tag)
                print(f"GIF con tag {tag} eliminado.")
                
            else:
                print(f"Tag {tag} no encontrado en gifs_tags.")

    # Vincular el evento de clic en el canvas
    canvas.bind("<Button-1>", eliminar_gif)

    
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

    crear_gif_con_fondo(root, 
                        [ruta_gif_insecto1_normalizada, ruta_gif_mascota1_normalizada], 
                        ruta_imagen_fondo_normalizada, 
                        width=1100, height=600, gif_height=100)
    

    print(ruta_gif_insecto1_normalizada)
    print(ruta_imagen_fondo_normalizada)
    print(ruta_gif_mascota1_normalizada)

    #prueba para las posiciones 
    posiciones = [(100, 200), (300, 100)]  
    crear_gif_con_fondo(root, 
                        [ruta_gif_insecto1_normalizada, ruta_gif_mascota1_normalizada], 
                        ruta_imagen_fondo_normalizada, 
                        width=1100, height=600, gif_height=100, posiciones=posiciones)
    
    root.mainloop()


if __name__ == "__main__":
    logicaJuego4()

