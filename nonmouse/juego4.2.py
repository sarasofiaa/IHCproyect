import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk
import random

def mostrar_gif(root, canvas, archivo, fondo_imagen, velocidad=20):
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

        # Abrir la imagen de fondo (ahora puede ser un PNG)
        fondo = Image.open(fondo_imagen)
        
        fondo_width, fondo_height = fondo.size
        fondo = fondo.resize((fondo_width, fondo_height))  # Ajustar tamaño de fondo al tamaño del canvas
        fondo_tk = ImageTk.PhotoImage(fondo)  # Convertir la imagen de fondo para Tkinter

        # Crear el canvas donde se va a mostrar el gif y colocar el fondo
        canvas.create_image(0, 0, image=fondo_tk, anchor=tk.NW)
        
        # Función para actualizar el GIF en el canvas
        def update(ind, x, y):
            """Actualiza la imagen del GIF en la ubicación deseada"""
            canvas.delete("all")  # Limpiar el canvas para reponer el fondo
            canvas.create_image(0, 0, image=fondo_tk, anchor=tk.NW)  # Reponer el fondo
            canvas.create_image(x, y, image=frames[ind], anchor=tk.NW)  # Colocar el siguiente frame del GIF
            ind += 1
            if ind == len(frames):
                ind = 0  # Volver al primer frame si se alcanza el final
            # Mover el GIF a una nueva posición aleatoria después de un tiempo
            new_x = random.randint(0, 100)  # Ajustar para que no se salga del canvas
            new_y = random.randint(0, 100)
            canvas.after(velocidad, update, ind, new_x, new_y)  # Llama nuevamente a la función después de 'velocidad' ms

        # Iniciar la animación desde el primer frame en una posición aleatoria
        update(0, random.randint(0, fondo_width - 100), random.randint(0, fondo_height - 100))

    except Exception as e:
        print(f"Error al mostrar el GIF: {e}")


# Crear la ventana de Tkinter
root = tk.Tk()
root.title("GIFs en Canvas con Fondo")

# Crear el canvas donde se va a mostrar el fondo y los GIFs
canvas_width = 1300
canvas_height = 850
canvas = Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack()

# Definir la imagen de fondo en formato PNG
fondo_imagen = r"C:\Users\fabia.PORSHA\UNSA\Github\IHC\IHCproyect\images\juego4\fondoPatio.png"  # Cambia la ruta al PNG
ruta_gif1 = r"C:\Users\fabia.PORSHA\UNSA\Github\IHC\IHCproyect\images\juego4\insecto1.gif"
ruta_gif2 = r"C:\Users\fabia.PORSHA\UNSA\Github\IHC\IHCproyect\images\juego4\perro1.gif"

# Cargar múltiples GIFs en el canvas (puedes agregar más archivos GIF aquí)
# Asegúrate de tener los archivos GIF en las rutas correctas
mostrar_gif(root, canvas, ruta_gif1 , fondo_imagen, velocidad=200)
#mostrar_gif(root, canvas, ruta_gif2 , fondo_imagen, velocidad=200)
#mostrar_gif(root, canvas, ruta_gif1 , fondo_imagen, velocidad=50)

root.mainloop()
