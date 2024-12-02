#Funciones globales como cargar imagenes
import numpy as np
import cv2
from PIL import Image, ImageTk 
import os

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
def cargar_gift(ruta, altura=None):
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
