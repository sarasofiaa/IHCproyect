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
        print("depu")
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

    carrusel_canva.winfo_toplevel().mainloop()