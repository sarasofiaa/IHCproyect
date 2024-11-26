 # Contiene la pantalla de bienvenida
import tkinter as tk
from tkinter import font
from tkinter import messagebox
from tkinter import PhotoImage
from .selector import main_selector
from PIL import Image, ImageTk
import os

# Función que se ejecutará al hacer clic en el botón "Iniciar todo"
def iniciar_aplicacion(window):
    #messagebox.showinfo("SkillPointer", "Iniciando la aplicación...")
    window.destroy()
    main_selector()
    

def main_interfaz():
    ventana = tk.Tk()
    ventana.title("SkillPointer - Featuring multi-movement activities")
    ventana.geometry("900x500")  # Tamaño de la ventana
    ventana.config(bg="#2c3e50")  # Color de fondo oscuro para un aspecto moderno
    
    # Cargar la imagen de fondo
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))  # Obtiene el directorio actual (nonmouse)
        project_dir = os.path.dirname(base_dir)  # Subir un nivel para llegar a la raíz del proyecto
        #print(f"Directorio raíz del proyecto: {project_dir}") 

        ruta_imagen = os.path.join(project_dir, "images", "fondo_imagen.png")

        # Cargar la imagen con Pillow
        imagen = Image.open(ruta_imagen)
        
        # Redimensionar la imagen: Ajusta la altura a 500px, y el ancho se ajusta automáticamente
        altura = 500
        ancho = int(imagen.width * (altura / imagen.height))
        imagen_redimensionada = imagen.resize((ancho, altura), Image.ANTIALIAS)
        
        # Convertir la imagen redimensionada a un formato compatible con Tkinter
        fondo = ImageTk.PhotoImage(imagen_redimensionada)
        
        # Crear el label con la imagen redimensionada
        label_fondo = tk.Label(ventana, image=fondo)
        label_fondo.place(relwidth=1, relheight=1)  # Coloca la imagen de fondo para que ocupe toda la ventana
        
        # Mantener la referencia a la imagen para evitar que se recoja por el recolector de basura
        label_fondo.image = fondo
    except Exception as e:
        print(f"No se pudo cargar la imagen de fondo: {e}")


    # Configuración del título en la ventana
    titulo = tk.Label(
        ventana,
        text="SkillPointer",
        font=("Helvetica", 24, "bold"),
        fg="#ecf0f1",
        bg="#2c3e50"
    )
    titulo.pack(pady=20)  # Espacio alrededor del título

    # Configuración de la descripción en la ventana
    descripcion = tk.Label(
        ventana,
        text="Potenciando la motricidad fina y habilidades de escritura de los mas pequeños",
        font=("Helvetica", 12),
        fg="#bdc3c7",
        bg="#2c3e50",
        wraplength=400,  # Limita el ancho de la descripción
        justify="center"
    )
    descripcion.pack(pady=10)

    # Configuración del botón de inicio
    boton_iniciar = tk.Button(
        ventana,
        text="Iniciar",
        font=("Helvetica", 14, "bold"),
        fg="#2c3e50",
        bg="#1abc9c",
        activebackground="#16a085",  # Color al hacer clic
        activeforeground="#ecf0f1",
        relief="flat",  # Quita los bordes para un estilo más moderno
        cursor="hand2",  # Cambia el cursor al pasar el mouse
        command=lambda:iniciar_aplicacion(ventana)
    )
    boton_iniciar.pack(pady=30)

# Inicia el bucle principal de la ventana
    ventana.mainloop()
main_interfaz()