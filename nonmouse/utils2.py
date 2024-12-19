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
        imagen = Image.open(ruta)
        frames = []
        
        try:
            while True:
                if altura:
                    # Calcular el nuevo ancho manteniendo la proporción
                    ratio = altura / imagen.height
                    nuevo_ancho = int(imagen.width * ratio)
                    frame_actual = imagen.resize((nuevo_ancho, altura), Image.Resampling.LANCZOS)
                else:
                    frame_actual = imagen.copy()
                
                frames.append(ImageTk.PhotoImage(frame_actual))
                imagen.seek(len(frames))  # Ir al siguiente frame
        except EOFError:
            # Se alcanzó el final del GIF
            pass
        
        return frames
    except Exception as e:
        print(f"No se pudo cargar la imagen desde {ruta}: {e}")
        return None

def mostrar_gif(root, archivo, fondo, x=0, y=0, velocidad=20):
    try:
        # Cargar el GIF y obtener sus dimensiones originales
        with Image.open(archivo) as img:
            gif_width, gif_height = img.size
        
        # Crear y posicionar el canvas
        canvas = tk.Canvas(root, width=gif_width, height=gif_height)
        canvas.pack()
        canvas.place(x=x, y=y)
        
        # Cargar el fondo
        fondo_img = Image.open(fondo)
        fondo_img = fondo_img.resize((gif_width, gif_height))
        fondo_tk = ImageTk.PhotoImage(fondo_img)
        
        # Cargar todos los frames del GIF
        frames = cargar_gif(archivo)
        
        def update(ind):
            # Mostrar el fondo
            canvas.create_image(0, 0, image=fondo_tk, anchor=tk.NW)
            # Mostrar el frame actual del GIF
            canvas.create_image(0, 0, image=frames[ind], anchor=tk.NW)
            
            # Actualizar al siguiente frame
            next_ind = (ind + 1) % len(frames)
            canvas.after(velocidad, update, next_ind)
        
        # Iniciar la animación
        canvas.after(0, update, 0)
        
        return canvas
        
    except Exception as e:
        print(f"Error al mostrar el GIF: {e}")
        return None


def resize_gif_frames(frames, target_width, target_height, preserve_aspect=True):
    """
    Redimensiona todos los frames de un GIF manteniendo la proporción si se desea.
    
    Args:
        frames: Lista de frames PhotoImage
        target_width: Ancho objetivo
        target_height: Alto objetivo
        preserve_aspect: Si se debe mantener la proporción de aspecto
    
    Returns:
        Lista de frames redimensionados
    """
    if not frames:
        return []
    
    # Obtener dimensiones del primer frame
    orig_width = frames[0].width()
    orig_height = frames[0].height()
    
    if preserve_aspect:
        # Calcular ratio para mantener proporción
        width_ratio = target_width / orig_width
        height_ratio = target_height / orig_height
        ratio = min(width_ratio, height_ratio)
        
        new_width = int(orig_width * ratio)
        new_height = int(orig_height * ratio)
    else:
        new_width = target_width
        new_height = target_height
    
    resized_frames = []
    for frame in frames:
        # Convertir PhotoImage a PIL Image
        pil_image = Image.new('RGBA', (orig_width, orig_height))
        pixel_data = zip(*(iter(frame.get()),) * 4)
        pixels = list(pixel_data)
        pil_image.putdata(pixels)
        
        # Redimensionar
        resized_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Convertir de vuelta a PhotoImage
        photo_image = ImageTk.PhotoImage(resized_image)
        resized_frames.append(photo_image)
    
    return resized_frames

def cargar_gif_adaptativo(ruta):
    """
    Carga un GIF y prepara sus frames para ser redimensionados posteriormente.
    
    Args:
        ruta: Ruta al archivo GIF
    
    Returns:
        Lista de frames originales y sus dimensiones originales
    """
    try:
        gif = Image.open(ruta)
        frames = []
        
        try:
            while True:
                frames.append(ImageTk.PhotoImage(gif.copy()))
                gif.seek(len(frames))
        except EOFError:
            pass
        
        return frames, gif.size
    except Exception as e:
        print(f"Error al cargar el GIF {ruta}: {e}")
        return None, None
