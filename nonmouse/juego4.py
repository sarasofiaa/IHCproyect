import tkinter as tk
from .baseJuego import GameWindow
import random
from PIL import Image, ImageTk
import os
from .utils2 import cargar_imagen



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

    # Título principal
    tk.Label(root, text='Juego: Presionar Animales', font=("Arial", 16, "bold")).pack(pady=10)
    
    # Explicación 
    descripcion = """
    En este juego, debes pellizcar a los animales que aparecen en la pantalla.
    Usa tus dedos índice y pulgar para pellizcar a los animales.
    ¡Ganas cuando seleccionas todos los animales correctamente!
    """
    tk.Label(root, text=descripcion, font=("Arial", 12), justify="center").pack(pady=20)
    
    # Instrucción visual del pellizco correcto
    try:
        # Cargar la imagen de la instrucción
        base_dir = os.path.dirname(os.path.abspath(__file__))  # Directorio actual
        project_dir = os.path.dirname(base_dir)  # Subir un nivel para llegar a la raíz del proyecto
        ruta_imagen = os.path.join(project_dir, "images", "juego4", "pellizco.jpg")  # Ruta de la imagen

        imagen = Image.open(ruta_imagen)  # Cargar la imagen
        imagen = imagen.resize((250, 250), Image.ANTIALIAS)  # Redimensionar para que quepa bien
        imagen_tk = ImageTk.PhotoImage(imagen)

        # Mostrar la imagen de instrucción
        imagen_label = tk.Label(root, image=imagen_tk)
        imagen_label.image = imagen_tk  # Referencia a la imagen para evitar que se borre
        imagen_label.pack(pady=10)
        
    except Exception as e:
        print(f"No se pudo cargar la imagen: {e}")
    
    # Botón de continuar
    def continuar():
        root.destroy()  # Cerrar ventana de instrucciones
        game_window = GameWindow("Juego4: Pellizca el insecto")
        game_window.setGameFrame(logicaJuego4)  # Asegúrate de tener esta función definida
        game_window.run()

    boton_continuar = tk.Button(root, text="Continuar", command=continuar)
    boton_continuar.pack(pady=20)
    
    root.mainloop()


def logicaJuego4(game_frame):
    #Variables globales 
    score = 0
    errores = 0
    tiempo = 0 #Tiempo en segundos de acuerdo vaya avanzando aumenta la dificultad

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
    
    
    def movimientoAleat(boton):
        x = random.randint(0,game_frame.winfo_width() - boton.winfo_width())
        y = random.randint(0,game_frame.winfo_width() - boton.winfo_width())
        boton.place(x=x,y=y)
        
    def apretasteInsecto(boton):
        print("Hasta aqui llega????") #depuracion
        global score
        print("Apretaste un insecto")
        score += 1
        print(f"¡Apretaste un insecto! Puntos: {score}")
        movimientoAleat(boton)

    def apretasteMal(boton):
        global errores
        errores += 1
        print(f"Apretaste mal. Errores: {errores}/3")
        if errores >= 3:
            gameOver()

    def gameOver():
        print("¡Juego terminado!")
        mensaje_gameOver = tk.Label(
            game_frame, 
            text=f"¡Juego terminado! Puntuación: {score}", 
            font=("Arial", 14, "bold"), 
            bg="red", 
            fg="white"
        )
        mensaje_gameOver.place(relx=0.5, rely=0.5, anchor="center")

    # Crear botones dinámicos
    print("Creando botones") #depuracion
    #Imagenes para los botones 
    #Insecto
    ruta_insecto = os.path.join(base_dir, "..", "images", "juego4", "insecto.png")
    imagen_insecto = cargar_imagen(ruta_insecto, altura=150)
    #Animal (Perro)
    ruta_animal1 = os.path.join(base_dir, "..", "images", "juego4", "animal1.jpg")
    imagen_animal1 = cargar_imagen(ruta_animal1, altura=150)

    #Creacion de label con eventos click 
    print("Hasta aqui llega") #depuracion
    
    labelInsecto = tk.Label(game_frame, image=imagen_insecto, bg="white", borderwidth=0)
    
    print("Hasta aqui llega") #depuraciona
    labelInsecto.image = imagen_insecto
    labelInsecto.place(x=50, y=50)
    labelInsecto.bind("<Button-1>", lambda event: apretasteInsecto(labelInsecto))
    print("Hasta aqui llega?") #depuracion
    
    labelAnimal = tk.Label(game_frame, image=imagen_animal1, bg="white", borderwidth=0)
    labelAnimal.image = imagen_animal1
    labelAnimal.place(x=100, y=100)
    labelAnimal.bind("<Button-1>", lambda event: apretasteMal(labelAnimal))



    # Mover animales/insectos cada segundo
    def mover(): #Hay un error
        movimientoAleat(boton_insecto)
        movimientoAleat(labelAnimal)
        if errores < 3:  # Mientras no haya terminado el juego
            game_frame.after(1000, mover)
        else:
            gameOver()
    


# Utiliza la misma función cargar_imagen para otros elementos como botones
def agregar_boton_con_imagen(frame, ruta_imagen, comando):
    imagen_boton = cargar_imagen(ruta_imagen, altura=50)
    if imagen_boton:
        boton = tk.Button(frame, image=imagen_boton, command=comando)
        boton.image = imagen_boton  # Mantener la referencia
        boton.pack(pady=10)
        return boton
    return None




    

