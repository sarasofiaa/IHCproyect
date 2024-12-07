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



#JUEGO_____________________________________________________________________________________________________________________________
def logicaJuego4(game_frame): 
    #Variables globales 
    global insects_past, insects_score, error, time # Asegúrate de definir score y errores globalmente
    
    insects_pass = 0  # Apenas pase un mosquito se termina el juego con el score de animales pasados
    pet_pass = 0 #Score del juego
    error = 0 # ?? No recuerdo
    time = 0 # cuando acabe el tiempo y ningun mosquito haya entrado ganas el juego 
    
    def ajustar_fondo(event=None):
        frame_height = game_frame.winfo_height()
        print(f"Dimensiones del frame:x{frame_height}")  # Para depuración y conocer 

        fondo = cargar_imagen(ruta_fondo, altura=frame_height)
        if fondo:
            canvas_game.create_image(0, 0, image=fondo, anchor="nw") # Se crea la imagen segun la dimension
            canvas_game.image = fondo  # Prevenir que el fondo sea recolectado por el Garbage Collector y se muestre


    #Canvas
    canvas_game = tk.Canvas(game_frame)
    canvas_game.pack(fill="both", expand=True)

    #Fondo en canvas
    base_dir = os.path.dirname(os.path.abspath(__file__)) #Obtiene la direccion actual
    ruta_fondo = os.path.join(base_dir, "..", "images", "juego4", "fondoPatio.png") #dirección del fondo
    # Asegurarse de que el tamaño del frame sea actualizado
    # Vincular el evento de redimensionamiento
    game_frame.bind("<Configure>", ajustar_fondo)

    #Interfaz y logica del juego
    #Descripcion: Pellizca los insectos antes que lleguen a la casa del perrito ubicado a la izquierda, pero cuidado con apretar a las mascotas
    def insect_passed():
        global insects_pass
        if (insects_pass == 0):
            gameOver()
        #FALTA: animacion de picadura a animal en la pantalla o sonido de grito de perrito

    def animal_pressed():
        global error
        error +=1 
        #FALTA:  animal desaparecer y label en instrucciones con 1/3 errores 

    def pet_passed():
        global pet_pass #Score
        pet_pass +=1

    def endgame():
        global pet_pass
        print(pet_pass)
        
        # FALRA : insecto desaparece y label de score aumenta

    def gameOver():
        print("¡Juego terminado!")
        mensaje_gameOver = tk.Label(
            game_frame, 
            text=f"¡Juego terminado! Puntuación: {pet_pass}", 
            font=("Arial", 14, "bold"), 
            bg="red", 
            fg="white"
        )
        mensaje_gameOver.place(relx=0.5, rely=0.5, anchor="center")
    # Reemplazar conn juego4.2
    # Carga de gifts
    #Rutas
    ruta_insecto1 = os.path.join(base_dir, "..", "images", "juego4", "insecto1.gif")
    ruta_mascota1 = os.path.join(base_dir, "..", "images", "juego4", "perro1.gif")

    #Insectos
    #gift_insecto1 = cargar_gift(ruta_insecto1, altura = 25)
    
    #mostrar_gif(game_frame, ruta_insecto1 , x=50, y=50, velocidad=20)
    base_dir = os.path.dirname(os.path.abspath(__file__)) #Obtiene la direccion actual
    ruta_fondo = os.path.join(base_dir, "..", "images", "juego4", "fondoPatio.png")

    mostrar_gif(game_frame, ruta_insecto1, ruta_fondo, x=50, y=50, velocidad=20)


    # Llamar al método para mostrar el GIF
    """
    if gift_insecto1:
        insecto1_label = tk.Label(game_frame, image=gift_insecto1[0], bg=None)  # Primer frame de insecto
        insecto1_label.place(x=100, y=100)  # Posicionar en el canvas
        insecto1_label.image = gift_insecto1[0]  # Mantener la referencia

    #Animales
    gift_mascota1 = cargar_gift(ruta_mascota1, altura = 25)
    if gift_mascota1:
        mascota1_label = tk.Label(game_frame, image=gift_mascota1[0], bg=None)  # Primer frame de mascota
        mascota1_label.place(x=300, y=200)  # Posicionar en el canvas
        mascota1_label.image = gift_mascota1[0]  # Mantener la referencia
    """
    
    
    
    #Canvas_game insercion de gifts
    
    """
    ruta_insecto = os.path.join(base_dir, "..", "images", "juego4", "insecto1.png")
    imagen_insecto = cargar_imagen(ruta_insecto, altura=150)
    
    #Mascotas
    gift_mascota1 =
    ruta_animal1 = os.path.join(base_dir, "..", "images", "juego4", "animal1.png")
    imagen_animal1 = cargar_imagen(ruta_animal1, altura=150)

    #Creacion de label con eventos click 
    labelInsecto = tk.Label(game_frame, image=imagen_insecto, bg=None, borderwidth=0)
    labelInsecto.image = imagen_insecto
    labelInsecto.place(x=50, y=50)
    labelInsecto.bind("<Button-1>", lambda event: apretasteInsecto(labelInsecto))
    
    labelAnimal = tk.Label(game_frame, image=imagen_animal1, bg=None, borderwidth=0)
    labelAnimal.image = imagen_animal1
    labelAnimal.place(x=300, y=130)
    labelAnimal.bind("<Button-1>", lambda event: apretasteMal(labelAnimal))

    # Mover animales/insectos cada segundo
    def mover(labelInsecto,labelAnimal): #Hay un error
        movimientoAleat(labelInsecto)
        movimientoAleat(labelAnimal)
        if errores < 3:  # Mientras no haya terminado el juego
            game_frame.after(1000, mover)
        else:
            gameOver()
    """
    


