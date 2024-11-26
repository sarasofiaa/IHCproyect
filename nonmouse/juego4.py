import tkinter as tk
from .baseJuego import GameWindow
import random
from PIL import Image, ImageTk
import os
from .utils2 import cargar_imagen

#Variables globales 
score = 0
errores = 0
tiempo = 0 #Tiempo en segundos de acuerdo vaya avanzando aumenta la dificultad

def mostrar_instrucciones():
    root = tk.Tk()
    root.title("Instrucciones - Presionar Animales")
    root.geometry("900x600")  # Ajustamos el tamaño para que haya espacio para todo
    # Cargar la imagen de fondo
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))  # Directorio actual
        project_dir = os.path.dirname(base_dir)  # Subir un nivel para llegar a la raíz del proyecto
        ruta_imagen_fondo = os.path.join(project_dir, "images","juego4", "fondoInstru.png")  # Ruta de la imagen de fondo

        imagen_fondo = Image.open(ruta_imagen_fondo)  # Cargar la imagen de fondo
        imagen_fondo = imagen_fondo.resize((900, 600), Image.ANTIALIAS)  # Redimensionar para que quepa bien
        fondo_tk = ImageTk.PhotoImage(imagen_fondo)

        # Crear un Label para mostrar la imagen de fondo
        fondo_label = tk.Label(root, image=fondo_tk)
        fondo_label.place(relwidth=1, relheight=1)  # Ocupa toda la ventana
        fondo_label.image = fondo_tk  # Referencia a la imagen para evitar que se borre
    except Exception as e:
        print(f"No se pudo cargar la imagen de fondo: {e}")

    
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

    # Explicación 
    descripcion = """
    Descripcion: Apreta los insectos, por cada insecto que aprietes subira tu score, 
    pero si apretas un lugar incorrecto o un animal 
    mas de tres veces el juego acabara, intenta tener el mayor score posible
    """
    tk.Label(
        root,
        text=descripcion,
        font=("Arial", 12),  # Fuente de letra, tamaño 12
        justify="center",  # Justificación del texto al centro
        bg="#d4e7ff",  # Color de fondo (puedes elegir otro color)
        fg="black",  # Color de la letra
        width=70,
        padx=20,  # Relleno horizontal
        pady=2   # Relleno vertical
    ).place(relx=0.5, y=150, anchor="n")  # Posicionando el label
    
    # Instrucción visual del pellizco correcto
    try:
        # Cargar la imagen de la instrucción
        base_dir = os.path.dirname(os.path.abspath(__file__))  # Directorio actual
        project_dir = os.path.dirname(base_dir)  # Subir un nivel para llegar a la raíz del proyecto
        ruta_imagen = os.path.join(project_dir, "images", "juego4", "pellizco.png")  # Ruta de la imagen

        imagen = Image.open(ruta_imagen)  # Cargar la imagen
        imagen = imagen.resize((190, 250), Image.ANTIALIAS)  # Redimensionar para que quepa bien
        imagen_tk = ImageTk.PhotoImage(imagen)

        # Mostrar la imagen de instrucción
        imagen_label = tk.Label(root, image=imagen_tk)
        imagen_label.image = imagen_tk  # Referencia a la imagen para evitar que se borre
        imagen_label.place(x=170, y=250) 
        
    except Exception as e:
        print(f"No se pudo cargar la imagen: {e}")
    
    # Botón de continuar
    def continuar():
        root.destroy()  # Cerrar ventana de instrucciones
        game_window = GameWindow("Juego4: Pellizca el insecto")
        game_window.setGameFrame(logicaJuego4)  # Asegúrate de tener esta función definida
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
    boton_continuar.place(x=500, y=350) 

    
    root.mainloop()


def logicaJuego4(game_frame):
    #Fondo
    base_dir = os.path.dirname(os.path.abspath(__file__)) #Obtiene la direccion actual
    ruta_fondo = os.path.join(base_dir, "..", "images", "juego4", "fondo.jpg")
    fondo = cargar_imagen(ruta_fondo, altura=1200)
    
    if fondo:
        label_fondo = tk.Label(game_frame, image=fondo)
        label_fondo.place(relwidth=1, relheight=1)
        game_frame.image = fondo  # Mantener la referencia
    #Interfaz y logica del juego
    #Descripcion: Apreta los insectos, por cada insecto que aprietes subira tu score, pero si apretas un lugar incorrecto o un animal 
    #mas de tres veces el juego acabara, intenta tener el mayor score posible
    
    
    def movimientoAleatBoton(boton):
        x = random.randint(0,game_frame.winfo_width()-10 - boton.winfo_width())
        y = random.randint(0,game_frame.winfo_width()-10 - boton.winfo_width())
        boton.place(x=x,y=y)
    def apretasteInsecto(boton):
        global score
        print("Apretaste un insecto")
        score += 1
        movimientoAleatBoton(boton)
    def apretasteMal(boton):
        global errores
        print("Apretaste mal, al tercer error se acaba el juego")
        errores +=1

    def gameOver():
        print("Juego terminado")
    # Crear botones dinámicos
    print("Creando botones") #depuracion
    boton_insecto = tk.Button(game_frame, text="Insecto", bg="yellow", command=lambda: apretasteInsecto(boton_insecto))
    boton_insecto.place(x=50, y=50)
    boton_animal = tk.Button(game_frame, text = "Animal", bg="red",command=lambda: apretasteMal(boton_animal))
    boton_animal.place(x=100, y=100)
    """
    while(errores <= 3):
    """



    # Mover botones cada segundo
    def mover_botones(boton_insecto, boton_animal): #Hay un error
        movimientoAleatBoton(boton_insecto)
        movimientoAleatBoton(boton_animal)
        game_frame.after(1000, mover_botones)
    


# Utiliza la misma función cargar_imagen para otros elementos como botones
def agregar_boton_con_imagen(frame, ruta_imagen, comando):
    imagen_boton = cargar_imagen(ruta_imagen, altura=50)
    if imagen_boton:
        boton = tk.Button(frame, image=imagen_boton, command=comando)
        boton.image = imagen_boton  # Mantener la referencia
        boton.pack(pady=10)
        return boton
    return None




    

