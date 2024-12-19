#Funciones globales como cargar imagenes
import numpy as np
import cv2
from PIL import Image, ImageTk 
import os
import tkinter as tk

def calculate_distance(point1, point2):
    return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def draw_circle(image, x, y, radius, color):
    cv2.circle(image, (int(x), int(y)), radius, color, -1)

def calculate_moving_average(value, window_size, value_list):
    value_list.append(value)
    if len(value_list) > window_size:
        value_list.pop(0)
    return sum(value_list) / len(value_list)

#Reutilizar para la carga de imagenes
def cargar_imagen(ruta, altura=None):
    try:
        imagen = Image.open(ruta)
        if altura:
            # Redimensionar la imagen manteniendo la relación de aspecto
            ancho = int(imagen.width * (altura / imagen.height))
            imagen = imagen.resize((ancho, altura), Image.ANTIALIAS)
        return ImageTk.PhotoImage(imagen)
    except Exception as e:
        print(f"No se pudo cargar la imagen desde {ruta}: {e}")
        return None

# Reutilizar para cargar gifts
def cargar_gif(ruta, altura=None):
    try:
        # Abrir la imagen GIF
        imagen = Image.open(ruta)
        
        # Si se proporciona altura, redimensionar la imagen manteniendo la relación de aspecto
        if altura:
            ancho = int(imagen.width * (altura / imagen.height))
            imagen = imagen.resize((ancho, altura), Image.ANTIALIAS)  # Redimensionar con el filtro ANTIALIAS
        
        # Convertir la imagen PIL a ImageTk.PhotoImage para su uso en Tkinter
        # Si la imagen tiene múltiples frames (GIF animado), también necesitamos manejar eso
        if imagen.is_animated: 
            frames = []
            for i in range(imagen.n_frames):
                imagen.seek(i)  # Navegar a cada frame
                frame = imagen.copy()
                frames.append(ImageTk.PhotoImage(frame))
            return frames  # Devolver todos los frames si es un GIF animado
        else:
            return ImageTk.PhotoImage(imagen)  # Si no es un GIF animado, devolver una sola imagen

    except Exception as e:
        print(f"No se pudo cargar la imagen desde {ruta}: {e}")
        return None

def mostrar_gif(root, archivo,fondo, x=0, y=0, velocidad=20):
   
    try:
        # Abrir el GIF con Pillow
        img = Image.open(archivo)
        
        framesNum = img.n_frames
        
        # Crear una lista de frames extraídos del GIF
        frames = []
        for i in range(framesNum):
            img.seek(i)  # Moverse al frame i
            frame = ImageTk.PhotoImage(img.copy())  # Convertir la imagen a un objeto compatible con Tkinter
            frames.append(frame)

        # Obtener el tamaño de la imagen (ancho y alto)
        gif_width, gif_height = img.size

        # Abrir la imagen de fondo
        fondo_img = Image.open(fondo)
        fondo_img = fondo_img.resize((gif_width, gif_height))  # Asegurarse que el fondo tiene el mismo tamaño que el GIF
        fondo_tk = ImageTk.PhotoImage(fondo_img)

        # Crear el canvas donde se va a mostrar el gif
        canvas = tk.Canvas(root, width=gif_width, height=gif_height)
        canvas.pack()
        canvas.place(x=x, y=y)  # Posicionar el canvas en la ubicación deseada

        # Función para actualizar el GIF
        def update(ind):
            """ Actualiza la imagen del GIF sobre el fondo """
            # Mostrar el fondo
            canvas.create_image(0, 0, image=fondo_tk, anchor=tk.NW)
            # Mostrar el frame del GIF sobre el fondo
            canvas.create_image(0, 0, image=frames[ind], anchor=tk.NW)

            ind += 1
            if ind == len(frames):
                ind = 0  # Volver al primer frame si se alcanza el final
            root.after(velocidad, update, ind)  # Llama nuevamente a la función después de 'velocidad' ms

        # Iniciar la animación desde el primer frame
        root.after(0, update, 0)

    except Exception as e:
        print(f"Error al mostrar el GIF: {e}")

    
