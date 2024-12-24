from tkinter import *
import os
import random
from PIL import Image, ImageTk
from .baseJuego import GameWindow
from tkinter import Toplevel, Label, Button
import pygame
# Inicializar pygame
pygame.mixer.init()  # Esto es necesario para usar los sonidos en pygame
# Cargar sonidos
base_dir = os.path.dirname(os.path.abspath(__file__)) 

sonido_insecto = pygame.mixer.Sound(os.path.join(base_dir, "..","sonido", "insecto_sound.mp3"))
sonido_mascota = pygame.mixer.Sound(os.path.join(base_dir, "..","sonido", "mascota_sound.mp3"))
sonido_general = pygame.mixer.Sound(os.path.join(base_dir, "..","sonido",  "sonido_general.mp3"))

# Variables Globales
insects_pass = 0  # Puntaje de insectos pasados
pet_pass = 0  # Puntaje de mascotas pasadas
insectos_pellizcados = 0  
mascotas_pellizcadas = 0
tiempo = 20000  # Tiempo de juego en milisegundos (20 segundos)
posiciones_y = [80, 180, 280, 380, 480]
pasaron_gifs = set()  # Conjunto para almacenar los GIFs que ya han pasado

def reiniciar_valores_globales():
    """Reinicia todas las variables globales a sus valores iniciales."""
    global insects_pass, pet_pass, insectos_pellizcados, mascotas_pellizcadas, error, tiempo, pasaron_gifs
    insects_pass = 0
    pet_pass = 0
    insectos_pellizcados = 0
    mascotas_pellizcadas = 0
    error = 0
    tiempo = 20000
    pasaron_gifs = set()


def crear_gif_con_fondo(root, insectos_rutas, mascotas_rutas, fondo_ruta, width, height, gif_height):  
    global insectos_pellizcados, mascotas_pellizcadas
    frames_resized_all_insectos = []
    frames_resized_all_mascotas = []

    # Crear el canvas con las dimensiones de la imagen
    canvas = Canvas(root, width=width, height=height)
    canvas.pack()

    # Cargar la imagen de fondo
    fondo = Image.open(fondo_ruta)
    fondo_width, fondo_height = width, height
    fondo = fondo.resize((fondo_width, fondo_height))  # Ajustar tamaño de fondo al tamaño del canvas
    fondo_tk = ImageTk.PhotoImage(fondo)  # Convertir la imagen de fondo para Tkinter

    canvas.create_image(0, 0, image=fondo_tk, anchor=NW)  # Coloca la imagen de fondo

    # Cargar los GIFs de insectos
    for gif_ruta in insectos_rutas:
        gif_image = Image.open(gif_ruta)  # Cargar el GIF
        framesNum = gif_image.n_frames  # Número de frames que tiene el gif
        print(f"Frames de insecto: {framesNum}")

        gif_original_width, gif_original_height = gif_image.size

        # Calcular el nuevo ancho basado en la altura proporcionada (manteniendo la proporción original)
        aspect_ratio = gif_original_width / gif_original_height
        gif_width = int(aspect_ratio * gif_height)

        # Lista de todas las imágenes del gif
        frames = [
            PhotoImage(file=gif_ruta, format='gif -index %i' % (i)) for i in range(framesNum)
        ]
        frames_resized = []

        # Redimensionar los frames del gif según los nuevos tamaños proporcionados
        for frame in frames:
            frame_image = frame.subsample(int(frame.width() // gif_width), int(frame.height() // gif_height))
            frames_resized.append(frame_image)

        # Almacenar los frames redimensionados de cada gif de insectos
        frames_resized_all_insectos.append(frames_resized)

    # Cargar los GIFs de mascotas
    for gif_ruta in mascotas_rutas:
        gif_image = Image.open(gif_ruta)  # Cargar el GIF
        framesNum = gif_image.n_frames  # Número de frames que tiene el gif
        print(f"Frames de mascota: {framesNum}")

        gif_original_width, gif_original_height = gif_image.size

        # Calcular el nuevo ancho basado en la altura proporcionada (manteniendo la proporción original)
        aspect_ratio = gif_original_width / gif_original_height
        gif_width = int(aspect_ratio * gif_height)

        # Lista de todas las imágenes del gif
        frames = [
            PhotoImage(file=gif_ruta, format='gif -index %i' % (i)) for i in range(framesNum)
        ]
        frames_resized = []

        # Redimensionar los frames del gif según los nuevos tamaños proporcionados
        for frame in frames:
            frame_image = frame.subsample(int(frame.width() // gif_width), int(frame.height() // gif_height))
            frames_resized.append(frame_image)

        # Almacenar los frames redimensionados de cada gif de mascotas
        frames_resized_all_mascotas.append(frames_resized)

    # Diccionario para almacenar el ID  de cada GIF
    gif_ids = {}

    # Función para generar nuevos GIFs aleatorios
    def generar_gif_aleatorio():
        # Elegir un GIF aleatorio de insectos o mascotas
        grupo = random.choice(['insecto', 'mascota'])
        if grupo == 'insecto':
            gif_ruta = random.choice(insectos_rutas)
            frames_resized = frames_resized_all_insectos[insectos_rutas.index(gif_ruta)]
            tag = f"insecto_{random.randint(1000, 9999)}"  # Genera un tag único para cada gif de insecto
        else:
            gif_ruta = random.choice(mascotas_rutas)
            frames_resized = frames_resized_all_mascotas[mascotas_rutas.index(gif_ruta)]
            tag = f"mascota_{random.randint(1000, 9999)}"  # Genera un tag único para cada gif de mascota

        pos_x = width
        pos_y = random.choice(posiciones_y)
        # Iniciar el ciclo de actualización de este gif
        gif_ids[tag] = root.after(0, update_gif, 0, frames_resized, tag, pos_x, pos_y, grupo)

    # Actualizar la imagen del gif en el canvas
    def update_gif(ind, frames_resized, tag, pos_x, pos_y, grupo):
        """Actualiza la imagen gif."""
        global insects_pass, pet_pass, tiempo

        if tag not in gif_ids:
            return

        canvas.delete(tag)  # Elimina las imágenes previas del gif
        frame = frames_resized[ind]
        ind += 1
        if ind == len(frames_resized):
            ind = 0
        # Actualizar la imagen en el canvas con una etiqueta "gif" para poder eliminarla después
        canvas.create_image(pos_x, pos_y, image=frame, anchor=NW, tags=tag)
        # Mover el GIF hacia la izquierda
        pos_x -= 5  # Ajustar este valor para controlar la velocidad del movimiento

        # Si el gif ha llegado al borde izquierdo, lo reiniciamos
        posDesaparece = 120
        if pos_x < posDesaparece and tag not in pasaron_gifs:
            #canvas.delete(tag)  # Eliminar el GIF

            canvas.delete(tag)  # Eliminar el GIF del canvas

            pasaron_gifs.add(tag)  # Asegurarse de que este GIF ya ha pasado una vez
            if grupo == 'insecto':
                insects_pass += 1  # Incrementa si es un insecto

                print("-------------Insecto pasó -------------------------")
                print("fin del juego -insectopaso")
                fin_del_juego()

            else:
                pet_pass += 1  # Incrementa si es una mascota


            # Cancelar la animación
            if tag in gif_ids:
                root.after_cancel(gif_ids[tag])  # Detener la actualización de este GIF
            return  # Salir de la función para evitar que el GIF siga siendo actualizado


        # Reprograma la actualización del GIF
        gif_ids[tag] = root.after(100, update_gif, ind, frames_resized, tag, pos_x, pos_y, grupo)  # Número que regula la velocidad del gif

    # Generar GIFs repetidamente
    def generar_gifs_repetidamente():
        global tiempo, insects_pass, insectos_pellizcados, mascotas_pellizcadas
        if tiempo > 0 and insects_pass == 0:  # Mientras quede tiempo en el juego
            generar_gif_aleatorio()  # Generar un GIF aleatorio
            tiempo -= 1000  # Decrementa 1 segundo
            print("Tiempo que va ...", tiempo)

            tiempo_pasado= tiempo//1000
            score= insectos_pellizcados-mascotas_pellizcadas
            game_window = GameWindow.get_current_instance()

            # Verificar que la instancia no sea None
            if game_window:
                # Actualizar la información del juego
                game_window.update_game4_info(score=score, time_left=tiempo_pasado)
            else:
                print("No se encontró una instancia de GameWindow.")

            root.after(4000, generar_gifs_repetidamente)  # Llamar a la función cada segundo
        elif(insects_pass > 0):
            print("ya mprmio")

        else:
            print("-------------Termino el tiempo -------------------------")
            print("fin del juego -generargif")
            fin_del_juego()

    def fin_del_juego():
        global insects_pass

        # Detener la creación de nuevos GIFs y detener los actuales
        for tag in gif_ids.keys():
            root.after_cancel(gif_ids[tag])  # Detener la animación de los GIFs
        # Detener la función de generación de GIFs
        root.after_cancel(generar_gifs_repetidamente)  # Cancela la función que crea los GIFs nuevos

        if insects_pass == 0:  # Si no se ha dejado pasar ningún insecto
            print("¡Has ganado! Tiempo terminado y no ha pasado ningún insecto.")
            mostrar_resultado(root, "¡Ganaste!")
        else:
            print(f"Game Over! Insectos pasados: {insects_pass}, Mascotas pasadas: {pet_pass}")
            mostrar_resultado(root, "¡Perdiste!")
        

    # Función para eliminar el GIF al hacer clic
    def eliminar_gif(event):
        global insectos_pellizcados, mascotas_pellizcadas
        # Obtener las coordenadas del clic
        x, y = event.x, event.y
        entidad_id = canvas.find_closest(x, y)[0]  # Obtén el ID del objeto más cercano
        tags = canvas.gettags(entidad_id)  # Obtén las tags asociadas al objeto

        if tags :
            tag = tags[0]  # Tomamos el primer tag
            print(f"Tag del objeto: {tag}")
            # Eliminar el GIF
            if "insecto" in tag:  # Si el tag contiene "insecto", es un insecto
                grupo = "insecto"
                insectos_pellizcados += 1
                sonido_insecto.play() 
            elif "mascota" in tag:  # Si el tag contiene "mascota", es una mascota
                grupo = "mascota"
                mascotas_pellizcadas += 1
                sonido_mascota.play() 
            else:
                return  # Si no es ni insecto ni mascota, no hacer nada

            # Eliminar el GIF solo si es un insecto
            if grupo == "insecto":
                if tag in gif_ids:
                    root.after_cancel(gif_ids[tag])  # Detener la actualización
                    del gif_ids[tag]  # Eliminar el 'after' del diccionario
                    canvas.delete(tag)
                    print(f"GIF con tag {tag} eliminado.")
            else:
                print("No se puede eliminar mascotas")
                
        tiempo_pasado= tiempo//1000
        score= insectos_pellizcados-mascotas_pellizcadas
        game_window = GameWindow.get_current_instance()

        # Verificar que la instancia no sea None
        if game_window:
            # Actualizar la información del juego
            game_window.update_game4_info(score=score, time_left=tiempo_pasado)
        else:
            print("No se encontró una instancia de GameWindow.")

    # Vincular el evento de clic en el canvas
    canvas.bind("<Button-1>", eliminar_gif)

    root.after(4000, generar_gifs_repetidamente)
    root.mainloop()
    #actualizar_info(panel_base)

def cerrar_juego(root, ventana_resultado=None):
    """Función para cerrar el juego y todas las ventanas abiertas."""
    print("Juego cerrado.")
    if ventana_resultado:
        ventana_resultado.destroy()  # Cierra la ventana modal de resultado si está abierta
    root.quit()  # Termina el loop principal de la ventana
    root.destroy()  # Destruye la ventana principal (root)
    exit()  # Esto cerrará el programa.

def reintentar(root, ventana_resultado=None):
    # Si la ventana de resultado está abierta, ciérrala
    try:
        if ventana_resultado:  # Solo intentar destruir si la ventana de resultado existe
            ventana_resultado.destroy()
    except TclError:
        pass  # Si la ventana ya está cerrada, no hacer nada
    
    # Cerrar la instancia actual del juego (si existe)
    if GameWindow.get_current_instance():
        GameWindow.get_current_instance().close()  # Cierra la instancia existente de GameWindow
    
    # Intentar cerrar la ventana principal (root)
    try:
        root.quit()  # Termina el mainloop si aún está en ejecución
        root.destroy()  # Destruye la ventana
    except TclError:
        pass  # Si la ventana ya ha sido destruida, no hacer nada
    reiniciar_valores_globales()
    # Crear una nueva instancia del juego
    game_window2 = GameWindow("Juego4: Pellizca el insecto")  # Nueva instancia de la ventana del juego
    game_window2.setGameFrame(logicaJuego4)  # Establecer el marco del juego (lógica)
    game_window2.run()  # Ejecutar el ciclo principal del juego

def mostrar_resultado(root, mensaje):
    """Crea una ventana modal simple para mostrar el mensaje con un fondo dependiendo del resultado."""
    
    # Crear una nueva ventana Toplevel
    ventana_resultado = Toplevel()
    ventana_resultado.title("Resultado")
    
    # Obtener las dimensiones de la pantalla
    screen_width = root.winfo_screenwidth()  # Ancho de la pantalla
    screen_height = root.winfo_screenheight()  # Alto de la pantalla
    
    # Definir las dimensiones de la ventana
    ancho_ventana = 600
    alto_ventana = 350

    # Calcular la posición de la ventana para centrarla en la pantalla
    x_position = (screen_width - ancho_ventana) // 2
    y_position = (screen_height - alto_ventana) // 2

    # Establecer la geometría de la ventana (tamaño y posición)
    ventana_resultado.geometry(f"{ancho_ventana}x{alto_ventana}+{x_position}+{y_position}")
    
    # Evitar que la ventana sea redimensionable
    ventana_resultado.resizable(False, False)

    base_dir = os.path.dirname(os.path.abspath(__file__))  # Obtiene la dirección actual

    # Determinar el fondo según el mensaje (ganaste o perdiste)
    if mensaje == "¡Ganaste!":
        ruta_fondo = os.path.join(base_dir, "..", "images", "juego4", "ganaste.png")
    else:
        ruta_fondo = os.path.join(base_dir, "..", "images", "juego4", "perdiste.png")
    
    # Cargar la imagen de fondo
    fondo = Image.open(ruta_fondo)
    
    # Redimensionar la imagen de fondo para ajustarse a la ventana
    fondo_redimensionado = fondo.resize((ancho_ventana, alto_ventana), Image.ANTIALIAS)
    fondo_tk = ImageTk.PhotoImage(fondo_redimensionado)

    # Crear un Canvas para dibujar la imagen de fondo
    canvas = Canvas(ventana_resultado, width=ancho_ventana, height=alto_ventana)
    canvas.pack(fill=BOTH, expand=True)

    # Dibujar la imagen de fondo en el canvas
    canvas.create_image(0, 0, image=fondo_tk, anchor=NW)

    # Crear los botones "Cerrar juego" y "Reintentar"
    frame_botones = Frame(ventana_resultado, bg="#ebdcbc")
    frame_botones.place(x=(ancho_ventana - 150) // 2, y=180)  # Colocar los botones en el centro de la ventana

    # Cargar imágenes de fondo distintas para cada botón
    fondo_boton_cerrar = Image.open(os.path.join(base_dir, "..", "images", "juego4", "buttonExit.png"))  # Imagen para el botón "Cerrar"
    fondo_boton_cerrar_tk = ImageTk.PhotoImage(fondo_boton_cerrar.resize((130, 30), Image.ANTIALIAS))  # Redimensionar

    fondo_boton_reintentar = Image.open(os.path.join(base_dir, "..", "images", "juego4", "buttonrestart.png"))  # Imagen para el botón "Reintentar"
    fondo_boton_reintentar_tk = ImageTk.PhotoImage(fondo_boton_reintentar.resize((130, 30), Image.ANTIALIAS))  # Redimensionar

    # Botón "Cerrar juego" con su imagen de fondo
    boton_cerrar = Button(frame_botones, command=lambda: cerrar_juego(root, ventana_resultado),
                          image=fondo_boton_cerrar_tk, compound="center", relief="flat")  # Imagen de fondo
    boton_cerrar.grid(row=1, column=0, padx=10)

    # Botón "Reintentar" con su imagen de fondo
    boton_reintentar = Button(frame_botones,  command=lambda: reintentar(root, ventana_resultado),
                              image=fondo_boton_reintentar_tk, compound="center", relief="flat")  # Imagen de fondo
    boton_reintentar.grid(row=0, column=0, padx=10)

    # Centrar la ventana modal sobre la ventana principal
    ventana_resultado.transient(root)  # Relacionar la ventana con la ventana principal
    ventana_resultado.grab_set()  # Hacer que sea modal (previene la interacción con otras ventanas)
    
    # Mantener la referencia de las imágenes de los botones
    boton_cerrar.image = fondo_boton_cerrar_tk
    boton_reintentar.image = fondo_boton_reintentar_tk

    # Mantener la referencia de la imagen de fondo de la ventana
    canvas.image = fondo_tk

    root.wait_window(ventana_resultado)  # Esperar hasta que la ventana sea cerrada
    
def logicaJuego4(frame):
    # Fondo en canvas
    # Cargar música de fondo
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Obtiene la dirección actual
    ruta_musica_fondo = os.path.join(base_dir, "..", "sonido", "sonido_general.mp3")  # Ruta a tu archivo MP3
    
    # Reproducir música de fondo en bucle
    pygame.mixer.music.load(ruta_musica_fondo)  # Cargar la música
    pygame.mixer.music.play(loops=-1, start=0.0)  # Reproducir música en bucle infinito (loops=-1)

    ruta_fondo = os.path.join(base_dir, "..", "images", "juego4", "fondoPatio.png")

    # Carga de gifs
    ruta_insecto1 = os.path.join(base_dir, "..", "images", "juego4", "insecto1.gif")
    ruta_mascota1 = os.path.join(base_dir, "..", "images", "juego4", "perro2.gif")

    # Llamamos a la función con el frame en lugar de crear un nuevo root
    crear_gif_con_fondo(frame, 
                        [ruta_insecto1],  # Lista de insectos
                        [ruta_mascota1],  # Lista de mascotas
                        ruta_fondo, 
                        width=1100, height=600, gif_height=100)

def mostrar_base_juego(frame):
    """Aquí puedes mostrar la interfaz base de tu juego"""
    # Ejemplo simple de usar un texto o elementos gráficos para la base del juego
    label = Label(frame, text="¡Bienvenido al juego!", font=("Arial", 24))
    label.pack(pady=20)




if __name__ == "__main__":
    # Crear la ventana principal
    root = Tk()
    root.title("Juego con Lógica y Base de Juego")

    # Crear un PanedWindow para dividir la pantalla
    paned_window = PanedWindow(root, orient=HORIZONTAL)
    paned_window.pack(fill=BOTH, expand=True)

    # Crear el panel para la lógica del juego
    panel_juego = Frame(paned_window, width=600, height=600)
    paned_window.add(panel_juego)

    # Crear el panel para la base del juego
    panel_base = Frame(paned_window, width=400, height=600)
    paned_window.add(panel_base)

    # Llamar a las funciones correspondientes para llenar cada sección
    logicaJuego4(panel_juego)  # Lógica del juego en el primer panel
    mostrar_base_juego(panel_base)  # Interfaz base en el segundo panel

    root.mainloop()