#Solo tiene por el momento pellizco flag
#Idea del juego: Casas al final tipo Plantas Vs Zombies no dejar que lleguen los insectos a las casitas pero cuidado con pellizcar un perrito
#Nuevo gesto? puede ser desplazar para tener mas tiempo gesto desplazar solo los insectos voladores, tiene una herramienta sobrecargada de un ventilador y se active con un gesto
import tkinter as tk
from PIL import Image, ImageTk
from .baseJuego import GameWindow
import random
from PIL import Image, ImageTk
import os
from .utils2 import cargar_imagen, mostrar_gif, cargar_gif 




def mostrar_instrucciones():
    instructions_window = GameWindow("Instrucciones del juego 4")
    print("bb") #Depuracion completada
    instructions_window.setGameFrame(instructions_game4)
    instructions_window.run()


def instructions_game4(game_frame):
    # Lista de rutas de los GIFs
    base_dir = os.path.dirname(os.path.abspath(__file__))
    rutas_gifs = [
        os.path.join(base_dir, "..", "images", "juego4", "instrucciones", f"inst{i}.gif") 
        for i in range(1, 6)
    ]
    # Canvas
    carrusel_canva = tk.Canvas(game_frame)
    carrusel_canva.pack(fill="both", expand=True)

    #E Estado del carrusel 
    estado = {
        'gifs': [cargar_gif(ruta) for ruta in rutas_gifs],
        'indice_actual': 0,
        'animation_id': None  # Para guardar el ID de la animación actual
    }
    def limpiar_canvas():
        # Cancela cualquier animación pendiente
        if estado['animation_id']:
            carrusel_canva.after_cancel(estado['animation_id'])
            estado['animation_id'] = None
        # Limpia el canvas
        carrusel_canva.delete("all")

    def mostrar_gif(indice):
        frames = estado['gifs'][indice]
        if not frames:
            return
        
        limpiar_canvas()
        
        if len(frames) > 1:
            velocidad = 100  # Ajustado para mejor rendimiento
            frame_actual = [0]
            
            def animar():
                limpiar_canvas()
                carrusel_canva.create_image(
                    400, 300, 
                    image=frames[frame_actual[0]], 
                    anchor=tk.CENTER, 
                    tags="gif"
                )
                frame_actual[0] = (frame_actual[0] + 1) % len(frames)
                estado['animation_id'] = carrusel_canva.after(velocidad, animar)
            
            animar()
        else:
            carrusel_canva.create_image(
                400, 300, 
                image=frames[0], 
                anchor=tk.CENTER, 
                tags="gif"
            )
    
    def siguiente_gif():
        limpiar_canvas()
        estado['indice_actual'] = (estado['indice_actual'] + 1) % len(rutas_gifs)
        
        if estado['indice_actual'] == len(rutas_gifs) - 1:
            boton_siguiente.destroy()
            crear_boton_jugar()
        
        mostrar_gif(estado['indice_actual'])
    
    def crear_boton_jugar():
        boton_jugar = tk.Button(
            carrusel_canva,
            text="JUGAR",
            command=jugar,
            fg="white",
            bg="#4CAF50",
            font=("Arial", 14, "bold"),
            relief="flat",
            padx=20,
            pady=10
        )
        boton_jugar.place(x=500, y=440)
    
    def jugar():
        limpiar_canvas()
        root_window = carrusel_canva.winfo_toplevel()
        root_window.destroy()

        game_window = GameWindow("Juego4: Pellizca el insecto")
        game_window.setGameFrame(logicaJuego4)
        game_window.run()
    
    # Botón siguiente
    boton_siguiente = tk.Button(
        carrusel_canva, 
        text="Siguiente", 
        command=siguiente_gif
    )
    boton_siguiente.place(x=700, y=550)
    
    # Mostrar el primer GIF
    mostrar_gif(estado['indice_actual'])



#JUEGO_____________________________________________________________________________________________________________________________
def logicaJuego4(game_frame): 
    #Variables globales 
    global insects_past, insects_score, error, time # Asegúrate de definir score y errores globalmente
    
    insects_pass = 0  # Apenas pase un mosquito se termina el juego con el score de animales pasados
    pet_pass = 0 #Score del juego
    error = 0 # ?? Presionas animal se baja el score
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
    


