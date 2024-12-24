# Contiene la ventana principal de la aplicación  juegos
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
from.instruccJuego4 import mostrar_instrucciones
from .datosGlobales import set_game_active, set_instruction_active,get_game_active


# Crear la ventana principal
def main_selector():
    root = tk.Tk()
    root.title("SkillPointer")
    root.geometry("800x500")

    # Crear título centrado
    
    # Cargar la imagen de fondo
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))  # Obtiene el directorio actual (nonmouse)
        project_dir = os.path.dirname(base_dir)  # Subir un nivel para llegar a la raíz del proyecto
        ruta_imagen = os.path.join(project_dir, "images", "fondo_imagen.png")

        # Cargar la imagen con Pillow
        imagen = Image.open(ruta_imagen)
        
        # Redimensionar la imagen para ajustarla al tamaño de la ventana
        altura = 550
        ancho = int(imagen.width * (altura / imagen.height))
        imagen_redimensionada = imagen.resize((ancho, altura), Image.ANTIALIAS)
        fondo = ImageTk.PhotoImage(imagen_redimensionada)
        
        # Crear el label con la imagen redimensionada
        label_fondo = tk.Label(root, image=fondo)
        label_fondo.place(relwidth=1, relheight=1)  # Ocupa toda la ventana con la imagen de fondo
        label_fondo.image = fondo  # Referencia para evitar el recolector de basura
    except Exception as e:
        print(f"No se pudo cargar la imagen de fondo: {e}")
    
    # Cargar la imagen del título
    try:
        ruta_imagen_titulo = os.path.join(project_dir, "images", "titulo2.png")  # Ruta de la imagen del título
        
        # Cargar la imagen con Pillow
        imagen_titulo = Image.open(ruta_imagen_titulo)
        
        # Redimensionar la imagen del título si es necesario
        imagen_titulo = imagen_titulo.resize((200, 70), Image.ANTIALIAS)  # Ajusta el tamaño si es necesario
        
        # Convertir la imagen a un formato que Tkinter pueda usar
        imagen_titulo_tk = ImageTk.PhotoImage(imagen_titulo)
        
        # Crear un label con la imagen del título
        label_titulo = tk.Label(root, image=imagen_titulo_tk, bg="#1c5b79")
        label_titulo.image = imagen_titulo_tk  # Mantener la referencia a la imagen
        
        # Colocar la imagen del título en una ubicación específica
        label_titulo.place(x=300, y=20)  # Cambia estas coordenadas para mover el título

    except Exception as e:
        print(f"No se pudo cargar la imagen del título: {e}")


    # Funciones para cada juego AQUI CADA UNO LLAME A SUS JUEGOS EN NUEVO ARCHIVO JUEGO4 EJEMPLO

    def presionar_colores():
        set_game_active(3) 
        root.destroy()
        messagebox.showinfo("Juego", "¡Presionar Colores seleccionado!")

    def presionar_animales():
        set_game_active(4) 
        set_instruction_active(True)
        root.destroy()
        mostrar_instrucciones()

    # Función para cargar imágenes desde una ruta local
    def cargar_imagen_desde_ruta(ruta):
        try:
            imagen = Image.open(ruta)
            imagen = imagen.resize((150, 150))  # Redimensionar la imagen
            return ImageTk.PhotoImage(imagen)
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")
            return None

    # Construir las rutas relativas con os.path.join()
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Obtiene el directorio del script
    ruta_colores = os.path.join(base_dir, "..", "images", "juego3.png")
    ruta_animales = os.path.join(base_dir, "..", "images", "juego4.png")
    # Cargar imágenes
    imagen_colores = cargar_imagen_desde_ruta(ruta_colores)
    imagen_animales = cargar_imagen_desde_ruta(ruta_animales)

    # Crear botones con imágenes para cada juego
    boton_colores = tk.Button(root, text="Presionar Colores", image=imagen_colores, compound="bottom", font=("Arial", 14), bg="#f1d6bb", command=presionar_colores, width=20, height=20)
    boton_animales = tk.Button(root, text="Pellizca el insecto", image=imagen_animales, compound="bottom", font=("Arial", 14), bg="#beca68", command=presionar_animales, width=20, height=20)

    # Colocar los botones con el método 'place()' en posiciones específicas con tamaños definidos
    boton_colores.place(x=100, y=140, width=250, height=250)
    boton_animales.place(x=430, y=140, width=250, height=250)

    root.mainloop()

# Ejecutar la ventana 
#main_selector()
