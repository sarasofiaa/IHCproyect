# Contiene la ventana principal de la aplicación
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Crear la ventana principal
def main_inicio():
    root = tk.Tk()
    root.title("SkillPointer")
    root.geometry("600x600")
    root.configure(bg="#2e857d")

    # Crear título centrado
    titulo = tk.Label(root, text="Juegos de Aprendizaje", font=("Arial", 18, "bold"), bg="#2e857d", fg="white")
    titulo.grid(row=0, column=0, columnspan=2, pady=20)

    # Funciones para cada juego
    def escribir_letras():
        messagebox.showinfo("Juego", "¡Escribir Letras seleccionado!")

    def escribir_numeros():
        messagebox.showinfo("Juego", "¡Escribir Números seleccionado!")

    def presionar_colores():
        messagebox.showinfo("Juego", "¡Presionar Colores seleccionado!")

    def presionar_animales():
        messagebox.showinfo("Juego", "¡Presionar Animales seleccionado!")

    # Función para cargar imágenes desde una ruta local
    def cargar_imagen_desde_ruta(ruta):
        try:
            imagen = Image.open(ruta)
            imagen = imagen.resize((100, 100))  # Redimensionar la imagen
            return ImageTk.PhotoImage(imagen)
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")
            return None

    # Rutas locales de las imágenes
    ruta_letras = "C:/Users/user/Documents/GitHub/IHC/NonMouse/images/letras_option.png"
    ruta_numeros = "C:/Users/user/Documents/GitHub/IHC/NonMouse/images/numeros_option.png"
    ruta_colores = "C:/Users/user/Documents/GitHub/IHC/NonMouse/images/colores_option.png"
    ruta_animales = "C:/Users/user/Documents/GitHub/IHC/NonMouse/images/animales_option.png"

    # Cargar imágenes
    imagen_letras = cargar_imagen_desde_ruta(ruta_letras)
    imagen_numeros = cargar_imagen_desde_ruta(ruta_numeros)
    imagen_colores = cargar_imagen_desde_ruta(ruta_colores)
    imagen_animales = cargar_imagen_desde_ruta(ruta_animales)

    # Crear botones con imágenes para cada juego
    boton_letras = tk.Button(root, text="Escribir Letras", image=imagen_letras, compound="top", font=("Arial", 14), bg="white", command=escribir_letras)
    boton_numeros = tk.Button(root, text="Escribir Números", image=imagen_numeros, compound="top", font=("Arial", 14), bg="white", command=escribir_numeros)
    boton_colores = tk.Button(root, text="Presionar Colores", image=imagen_colores, compound="top", font=("Arial", 14), bg="white", command=presionar_colores)
    boton_animales = tk.Button(root, text="Presionar Animales", image=imagen_animales, compound="top", font=("Arial", 14), bg="white", command=presionar_animales)

    # Colocar los botones en una cuadrícula (2 arriba, 2 abajo)
    boton_letras.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
    boton_numeros.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
    boton_colores.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
    boton_animales.grid(row=2, column=1, padx=10, pady=10, sticky="nsew")

    # Hacer que las filas y columnas sean de igual tamaño
    root.grid_rowconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    root.mainloop()

# Ejecutar la ventana principal
main_inicio()
