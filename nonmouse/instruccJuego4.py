#Solo tiene por el momento pellizco flag
#Idea del juego: Casas al final tipo Plantas Vs Zombies no dejar que lleguen los insectos a las casitas pero cuidado con pellizcar un perrito
#Nuevo gesto? puede ser desplazar para tener mas tiempo gesto desplazar 
import tkinter as tk
from PIL import Image, ImageTk
from .baseJuego import GameWindow
import random
from PIL import Image, ImageTk
import os
from .utils2 import cargar_imagen, mostrar_gif
from .juego4 import logicaJuego4




def mostrar_instrucciones():
    root = tk.Tk()
    root.title("Instrucciones - Presionar Animales")
    root.geometry("1000x600")  # Ajustamos el tamaño para que haya espacio para todo
    # Cargar la imagen de fondo
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))  # Directorio actual
        project_dir = os.path.dirname(base_dir)  # Subir un nivel para llegar a la raíz del proyecto
        ruta_imagen_fondo = os.path.join(project_dir, "images","juego4", "fondoInstruccion.png")  # Ruta de la imagen de fondo

        imagen_fondo = Image.open(ruta_imagen_fondo)  # Cargar la imagen de fondo
        imagen_fondo = imagen_fondo.resize((1000, 600), Image.ANTIALIAS)  # Redimensionar para que quepa bien
        fondo_tk = ImageTk.PhotoImage(imagen_fondo)

        # Crear un Label para mostrar la imagen de fondo
        fondo_label = tk.Label(root, image=fondo_tk)
        fondo_label.place(relwidth=1, relheight=1)  # Ocupa toda la ventana
        fondo_label.image = fondo_tk  # Referencia a la imagen para evitar que se borre
    except Exception as e:
        print(f"No se pudo cargar la imagen de fondo: {e}")

    """
    # Título principal con place para control de posición
    tk.Label(
        root,
        text='Juego: Presionar Animales',
        font=("Arial", 17, "bold"),  # Establecer la fuente, tamaño y estilo (negrita)
        bg="#6da8db",  # Color de fondo (verde en este caso)
        fg="white",  # Color de la letra (blanco)
        padx=10,  # Relleno horizontal (opcional)
        pady=10,  # Relleno vertical (opcional)
    ).place(relx=0.5, y=45, anchor="n")

    """
    # Explicación 
    descripcion = """
    Apreta los insectos, por cada insecto que 
    aprietes subira tu score, pero si apretas un 
    lugar incorrecto o un animal mas de TRES veces
    el juego acabara, intenta tener el 
    mayor score posible
    """
    # Crear el Label con las instrucciones y posicionarlo
    tk.Label(
        root,
        text=descripcion,
        font=("Arial", 15),  # Fuente de letra y tamaño
        justify="center",  # Alinea el texto a la izquierda para que quede más organizado
        bg="#d4e7ff",  # Color de fondo (puedes elegir otro color)
        fg="black",  # Color de la letra
        width=42,  # Ancho del texto (puedes ajustarlo según el contenido)
        height=5,  # Altura para hacer que el texto ocupe más espacio si es necesario
        padx=2,  # Relleno horizontal
        pady=2,  # Relleno vertical
        anchor="nw"  # Ancla superior para que el texto se posicione desde la parte superior
    ).place(x=125, y=150)  # Posicionar en la ubicación deseada
        
    # Instrucción visual del pellizco correcto
    try:
        # Cargar la imagen de la instrucción
        base_dir = os.path.dirname(os.path.abspath(__file__))  # Directorio actual
        project_dir = os.path.dirname(base_dir)  # Subir un nivel para llegar a la raíz del proyecto
        ruta_imagen = os.path.join(project_dir, "images", "juego4", "pellizco.png")  # Ruta de la imagen

        imagen = Image.open(ruta_imagen)  # Cargar la imagen
        imagen = imagen.resize((150, 220), Image.ANTIALIAS)  # Redimensionar para que quepa bien
        imagen_tk = ImageTk.PhotoImage(imagen)

        # Mostrar la imagen de instrucción
        imagen_label = tk.Label(root, image=imagen_tk,bg="#d4e7ff" )
        imagen_label.image = imagen_tk  # Referencia a la imagen para evitar que se borre
        imagen_label.place(x=170, y=300) 
        
    except Exception as e:
        print(f"No se pudo cargar la imagen: {e}")
    
    # Explicación 
    descripcion2 = """
    Mira la imagen para ver cómo debes pellizcar. 
    ¡Usa tus dedos como si estuvieras 
    atrapando al insecto!
    """
    # Crear el Label con las instrucciones y posicionarlo
    tk.Label(
        root,
        text=descripcion2,
        font=("Arial", 15),  # Fuente de letra y tamaño
        justify="left",  # Alinea el texto a la izquierda para que quede más organizado
        bg="#d4e7ff",  # Color de fondo (puedes elegir otro color)
        fg="black",  # Color de la letra
        width=42,  # Ancho del texto (puedes ajustarlo según el contenido)
        height=5,  # Altura para hacer que el texto ocupe más espacio si es necesario
        padx=2,  # Relleno horizontal
        pady=2,  # Relleno vertical
        anchor="nw"  # Ancla superior para que el texto se posicione desde la parte superior
    ).place(x=370, y=300)  # Posicionar en la ubicación deseada

    # Botón de continuar
    def continuar():
        root.destroy()  # Cerrar ventana de instrucciones
        game_window = GameWindow("Juego4: Pellizca el insecto") # Inicio del juego
        game_window.setGameFrame(logicaJuego4)  # tener esta función definida
        game_window.run()

    boton_continuar = tk.Button(
        root, 
        text="Continuar",  # Texto del botón
        command=continuar,  # Función que se ejecuta al hacer clic en el botón
        fg="white",  # Color del texto del botón
        bg="#4CAF50",  # Color de fondo del botón (puedes elegir otro color)
        font=("Arial", 14, "bold"),  # Estilo de la fuente del botón
        relief="flat",  # Sin relieve para un estilo más limpio
        padx=20,  # Relleno horizontal
        pady=10  # Relleno vertical
    )

    # Coloca el botón en una ubicación exacta usando .place()
    boton_continuar.place(x=500, y=440) 

    
    root.mainloop()

