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
from .utils2 import cargar_imagen, mostrar_gif, cargar_gif
from .datosGlobales import set_instruction_active


  

def mostrar_instrucciones():
    instructions_window = GameWindow("Instrucciones del juego 4",is_instruction=True)
    instructions_window.setGameFrame(instructions_game4)
    instructions_window.run()


def instructions_game4(game_frame):
    # Lista de rutas de los GIFs
    base_dir = os.path.dirname(os.path.abspath(__file__))
    rutas_gifs = [
        os.path.join(base_dir, "..", "images", "juego4", "instrucciones", f"inst{i}.gif") 
        for i in range(1, 6)
    ]
    
    # Canvas con dimensiones iniciales
    carrusel_canva = tk.Canvas(game_frame, width=800, height=600)
    carrusel_canva.pack(fill="both", expand=True)
    height = 500

    # Estado del carrusel 
    estado = {
        'gifs': [cargar_gif(ruta, altura=height) for ruta in rutas_gifs],
        'indice_actual': 0,
        'animation_id': None,
        'canvas_ready': False  # Nuevo estado para controlar si el canvas está listo
    }

    def limpiar_canvas():
        if estado['animation_id']:
            carrusel_canva.after_cancel(estado['animation_id'])
            estado['animation_id'] = None
        carrusel_canva.delete("all")

    def mostrar_gif(indice):
        frames = estado['gifs'][indice]
        if not frames:
            return
            
        # Usamos las dimensiones del canvas
        width = carrusel_canva.winfo_width()
        height = carrusel_canva.winfo_height()
        
        # Calculamos el centro
        center_x = width // 2
        center_y = height // 2
        
        limpiar_canvas()
        
        if len(frames) > 1:
            velocidad = 60
            frame_actual = [0]
            
            def animar():
                limpiar_canvas()
                carrusel_canva.create_image(
                    center_x, center_y,
                    image=frames[frame_actual[0]], 
                    anchor=tk.CENTER, 
                    tags="gif"
                )
                frame_actual[0] = (frame_actual[0] + 1) % len(frames)
                estado['animation_id'] = carrusel_canva.after(velocidad, animar)
            
            animar()
        else:
            carrusel_canva.create_image(
                center_x, center_y,
                image=frames[0], 
                anchor=tk.CENTER, 
                tags="gif"
            )
    
    def siguiente_gif():
        print("Desplazando a siguiente")
        limpiar_canvas()
        estado['indice_actual'] = (estado['indice_actual'] + 1) % len(rutas_gifs)
        
        
        mostrar_gif(estado['indice_actual'])
    

    def jugar():
        limpiar_canvas()
        root_window = carrusel_canva.winfo_toplevel()
        root_window.destroy()
        set_instruction_active(False) #Activar flags normales de mpellizco
        game_window = GameWindow("Juego4: Pellizca el insecto", is_instruction = False)
        game_window.setGameFrame(logicaJuego4)
        game_window.run()

    def on_canvas_configure(event):
        if not estado['canvas_ready']:
            estado['canvas_ready'] = True
            mostrar_gif(estado['indice_actual'])
    
    window = GameWindow.get_current_instance()
    if window and window.root:
        window.root.bind('<<NextGif>>', lambda e: siguiente_gif())
        window.root.bind('<<StartGame>>', lambda e: jugar())
        
    # Bind to both root and game_frame for redundancy
    game_frame.bind('<<NextGif>>', lambda e: siguiente_gif())
    # Esperamos a que el canvas esté listo antes de mostrar el primer GIF
    carrusel_canva.bind('<Configure>', on_canvas_configure)