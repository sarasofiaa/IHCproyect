from tkinter import *
import os
import random
from PIL import Image, ImageTk

# Variables Globales
insects_pass = 0  # Puntaje de insectos pasados
pet_pass = 0  # Puntaje de mascotas pasadas
error = 0  # ¿Para qué se usaría este? Puedes aclararlo si lo necesitas
tiempo = 20000  # Tiempo de juego en milisegundos (20 segundos)
posiciones_y = [80, 180, 280, 380, 480]  

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
        framesNum = gif_image.n_frames  # Número de frames que tiene el gif
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

    # Función para generar nuevos GIFs aleatorios
    def generar_gif_aleatorio():
        print("Se genero un gif aleatorio")
        # Elegir un GIF aleatorio
        gif_ruta = random.choice(gif_rutas)
        frames_resized = frames_resized_all_gifs[gif_rutas.index(gif_ruta)]
        pos_x = width
        pos_y = random.choice(posiciones_y)
        tag = f"gif_{random.randint(1000, 9999)}"  # Genera un tag único para cada gif
        # Iniciar el ciclo de actualización de este gif
        gif_ids[tag] = root.after(0, update_gif, 0, frames_resized, tag, pos_x, pos_y)

    # Actualizar la imagen del gif en el canvas
    def update_gif(ind, frames_resized, tag, pos_x, pos_y):
        """Actualiza la imagen gif."""
        global insects_pass, pet_pass, tiempo

        if tag not in gif_ids:
            return
        
        canvas.delete(tag)  # Elimina las imágenes previas del gif
        frame = frames_resized[ind]
        ind += 1
        if ind == len(frames_resized):
            ind = 0
        # Actualizar la imagen en el canvas con una etiqueta "gif" para poder eliminarla después
        canvas.create_image(pos_x, pos_y, image=frame, anchor=NW, tags=tag)
        # Mover el GIF hacia la izquierda
        pos_x -= 5  # Ajustar este valor para controlar la velocidad del movimiento

        # Si el gif ha llegado al borde izquierdo, lo reiniciamos
        posDesaparece = 120
        if pos_x < posDesaparece:
            pos_x = width
            if 'insecto' in tag:
                insects_pass += 1  # Incrementa si es un insecto
            else:
                pet_pass += 1  # Incrementa si es una mascota
            print(f"Insectos pasados: {insects_pass}, Mascotas pasadas: {pet_pass}")
            print(tag)

        # Reprograma la actualización del GIF
        gif_ids[tag] = root.after(100, update_gif, ind, frames_resized, tag, pos_x, pos_y)  # Número que regula la velocidad del gif

    # Generar GIFs repetidamente
    def generar_gifs_repetidamente():
        global tiempo
        if tiempo > 0:  # Mientras quede tiempo en el juego
            generar_gif_aleatorio()  # Generar un GIF aleatorio
            tiempo -= 1000  # Decrementa 1 segundo
            root.after(4000, generar_gifs_repetidamente)  # Llamar a la función cada segundo
        else:
            fin_del_juego()

    def fin_del_juego():
        print("Fin del juego")

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

    root.after(4000, generar_gifs_repetidamente)
    root.mainloop()


def logicaJuego4(): 
    # Fondo en canvas
    base_dir = os.path.dirname(os.path.abspath(__file__)) # Obtiene la dirección actual
    ruta_fondo = os.path.join(base_dir, "..", "images", "juego4", "fondoPatio.png")

    # Carga de gifs
    # Rutas
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

if __name__ == "__main__":
    logicaJuego4()
