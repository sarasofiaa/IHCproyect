import tkinter as tk
from PIL import Image, ImageTk
import os
from .baseJuego import GameWindow
from .juego3 import logicaJuego3

def instrucciones():
    root = tk.Tk()
    root.title("Instrucciones - Pad de Colores")
    root.geometry("1000x600")

    # Cargar la imagen de fondo
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.dirname(base_dir)
        ruta_imagen_fondo = os.path.join(project_dir, "images", "juego3", "fondo.jpg")
        print(f"Ruta absoluta de la imagen de fondo: {ruta_imagen_fondo}")

        imagen_fondo = Image.open(ruta_imagen_fondo)
        fondo_tk = ImageTk.PhotoImage(imagen_fondo)

        fondo_label = tk.Label(root, image=fondo_tk)
        fondo_label.place(relwidth=1, relheight=1)  # Ocupa todo el fondo
        fondo_label.image = fondo_tk  # Mantiene una referencia para evitar que se libere
    except Exception as e:
        print(f"No se pudo cargar la imagen de fondo: {e}")

    # Explicación principal
    descripcion = """
    ¡Pon a prueba tu memoria y ritmo! En este juego, 
    deberás seguir una secuencia de colores que se 
    irá mostrando. Al hacer clic en los colores correctos 
    en el mismo orden, podrás avanzar al siguiente nivel.
    Tu objetivo es recordar la secuencia y replicarla.
    """

    tk.Label(
        root,
        text=descripcion,
        font=("Arial", 15),
        justify="center",
        bg="#d4e7ff",
        fg="black",
        width=45,
        height=5,
        padx=2,
        pady=2,
        anchor="nw"
    ).place(x=220, y=40)

    # Instrucción visual del click
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.dirname(base_dir)
        ruta_imagen = os.path.join(project_dir, "images", "juego3", "click.png")

        imagen = Image.open(ruta_imagen)
        imagen = imagen.resize((150, 220), Image.ANTIALIAS)
        imagen_tk = ImageTk.PhotoImage(imagen)

        imagen_label = tk.Label(root, image=imagen_tk, bg="#d4e7ff")
        imagen_label.image = imagen_tk
        imagen_label.place(x=170, y=300)
    except Exception as e:
        print(f"No se pudo cargar la imagen: {e}")

    # Explicación de controles
    descripcion2 = """
    Sigue la secuencia de colores y haz clic en ellos en el 
    mismo orden para avanzar al siguiente nivel:
    
    ROJO - Primer color
    AZUL - Segundo color
    VERDE - Tercer color
    AMARILLO - Cuarto color

    ¡Recuerda! Si te equivocas, el juego terminará. ¿Podrás 
    llegar al nivel más alto?
    """

    tk.Label(
        root,
        text=descripcion2,
        font=("Arial", 15),
        justify="left",
        bg="#d4e7ff",
        fg="black",
        width=50,
        height=12,
        padx=2,
        pady=2,
        anchor="nw"
    ).place(x=200, y=160)

    # Botón de continuar
    def continuar():
        root.destroy()
        game_window = GameWindow("Juego 3: Pad de Colores")  # Inicio del juego
        game_window.setGameFrame(logicaJuego3)  # tener esta función definida
        game_window.run()

    boton_continuar = tk.Button(
        root,
        text="Continuar",
        command=continuar,
        fg="white",
        bg="#4CAF50",
        font=("Arial", 14, "bold"),
        relief="flat",
        padx=20,
        pady=10
    )

    boton_continuar.place(x=500, y=440)

    root.mainloop()

if __name__ == "__main__":
    instrucciones()