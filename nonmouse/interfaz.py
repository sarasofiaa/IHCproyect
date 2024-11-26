import tkinter as tk
from tkinter import font
from PIL import Image, ImageTk
import os
from .selector import main_selector

# Función que se ejecutará al hacer clic en el botón "Iniciar todo"
def iniciar_aplicacion(window):
    window.destroy()
    main_selector()

def main_interfaz():
    ventana = tk.Tk()
    ventana.title("SkillPointer - Featuring multi-movement activities")
    ventana.geometry("900x500")  # Tamaño de la ventana
    
    # Cargar la imagen de fondo
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))  # Obtiene el directorio actual (nonmouse)
        project_dir = os.path.dirname(base_dir)  # Subir un nivel para llegar a la raíz del proyecto
        ruta_imagen = os.path.join(project_dir, "images", "fondo_imagen.png")

        # Cargar la imagen con Pillow
        imagen = Image.open(ruta_imagen)
        
        # Redimensionar la imagen para ajustarla al tamaño de la ventana
        altura = 500
        ancho = int(imagen.width * (altura / imagen.height))
        imagen_redimensionada = imagen.resize((ancho, altura), Image.ANTIALIAS)
        fondo = ImageTk.PhotoImage(imagen_redimensionada)
        
        # Crear el label con la imagen redimensionada
        label_fondo = tk.Label(ventana, image=fondo)
        label_fondo.place(relwidth=1, relheight=1)  # Ocupa toda la ventana con la imagen de fondo
        label_fondo.image = fondo  # Referencia para evitar el recolector de basura
    except Exception as e:
        print(f"No se pudo cargar la imagen de fondo: {e}")
    
    fondo = "#141240"
    # Crear un frame transparente para alinear texto encima del fondo
    frame_texto = tk.Frame(
        ventana,
        bg=fondo,  # Fondo del marco (puedes cambiar este color)
        highlightbackground=fondo,  # Color del borde
        highlightthickness=5,  # Grosor del borde
        width=400,  # Ancho del marco
        height=200,  # Alto del marco
        padx=20,  # Separación entre el borde y el contenido en el eje X
        pady=20   # Separación entre el borde y el contenido en el eje Y
    )
    frame_texto.place(relx=0.1, rely=0.5, anchor="w")  # Posición relativa al fondo

    # Cargar la imagen del título
    try:
        ruta_imagen_titulo = os.path.join(project_dir, "images", "titulo.png")  # Ruta de la imagen del título
        
        # Cargar la imagen con Pillow
        imagen_titulo = Image.open(ruta_imagen_titulo)
        
        # Redimensionar la imagen del título si es necesario
        imagen_titulo = imagen_titulo.resize((400, 100), Image.ANTIALIAS)  # Ajusta el tamaño si es necesario
        
        # Convertir la imagen a un formato que Tkinter pueda usar
        imagen_titulo_tk = ImageTk.PhotoImage(imagen_titulo)
        
        # Crear un label con la imagen del título
        label_titulo = tk.Label(frame_texto, image=imagen_titulo_tk, bg=fondo)
        label_titulo.image = imagen_titulo_tk  # Mantener la referencia a la imagen
        label_titulo.pack(pady=10)
        
    except Exception as e:
        print(f"No se pudo cargar la imagen del título: {e}")

    """
    # Título
    titulo = tk.Label(
        frame_texto,
        text="SKILLPOINTER",
        font=("Brick Sans", 35, "bold"),
        fg="#f1c40f",  # Color amarillo brillante para el texto
        highlightthickness=0,
        bg=fondo,  # Fondo en un tono marrón claro
        borderwidth=0
    )
        titulo.pack(pady=10)
    """



    # Descripción
    descripcion = tk.Label(
        frame_texto,
        text="Potenciando la motricidad fina y habilidades de escritura\nde los más pequeños",
        font=("Comic Sans MS", 13),
        fg="#ffffff",  # Negro para el texto de la descripción
        wraplength=400,
        bg=fondo,
        justify="center"
    )
    descripcion.pack(pady=10)

    # Botón
    boton_iniciar = tk.Button(
        frame_texto,
        text="Iniciar",
        font=("Comic Sans MS", 18, "bold"),
        fg="#ffffff",  # Color blanco para el texto
        bg="#4f722a",  # Color de fondo verde
        activebackground="#3c5d23",  # Color más oscuro de fondo al hacer clic
        activeforeground="#ffffff",  # Color blanco para el texto al hacer clic
        relief="flat",  # Sin bordes para un estilo plano
        cursor="hand2",  # Cambia el cursor al pasar sobre el botón
        width=10,  # Ancho del botón (en caracteres)
        height=1, 
        command=lambda: iniciar_aplicacion(ventana)

    )
    boton_iniciar.pack(pady=20)

    ventana.mainloop()

main_interfaz()
