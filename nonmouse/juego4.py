from tkinter import *
import os
import random
from PIL import Image, ImageTk
from .baseJuego import GameWindow
from tkinter import Toplevel, Label, Button

# Variables Globales
insects_pass = 0  # Puntaje de insectos pasados
pet_pass = 0  # Puntaje de mascotas pasadas
error = 0  # ¿Para qué se usaría este? Puedes aclararlo si lo necesitas
tiempo = 20000  # Tiempo de juego en milisegundos (20 segundos)
posiciones_y = [80, 180, 280, 380, 480]
pasaron_gifs = set()  # Conjunto para almacenar los GIFs que ya han pasado

def crear_gif_con_fondo(root, insectos_rutas, mascotas_rutas, fondo_ruta, width, height, gif_height):  
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
        global tiempo, insects_pass
        if tiempo > 0 and insects_pass == 0:  # Mientras quede tiempo en el juego
            generar_gif_aleatorio()  # Generar un GIF aleatorio
            tiempo -= 1000  # Decrementa 1 segundo
            print("Tiempo que va ...", tiempo)
            root.after(4000, generar_gifs_repetidamente)  # Llamar a la función cada segundo
        else:
            print("-------------Termino el tiempo -------------------------")
            fin_del_juego()

    def fin_del_juego():
        global insects_pass
        if insects_pass == 0:  # Si no se ha dejado pasar ningún insecto
            print("¡Has ganado! Tiempo terminado y no ha pasado ningún insecto.")
            mostrar_resultado(root, "¡Ganaste!")
        else:
            print(f"Game Over! Insectos pasados: {insects_pass}, Mascotas pasadas: {pet_pass}")
            mostrar_resultado(root, "¡Perdiste!")
        # Detener la creación de nuevos GIFs y detener los actuales
        for tag in gif_ids.keys():
            root.after_cancel(gif_ids[tag])  # Detener la animación de los GIFs
        # Detener la función de generación de GIFs
        root.after_cancel(generar_gifs_repetidamente)  # Cancela la función que crea los GIFs nuevos

    # Función para eliminar el GIF al hacer clic
    def eliminar_gif(event):
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
            elif "mascota" in tag:  # Si el tag contiene "mascota", es una mascota
                grupo = "mascota"
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

    # Vincular el evento de clic en el canvas
    canvas.bind("<Button-1>", eliminar_gif)

    root.after(4000, generar_gifs_repetidamente)
    root.mainloop()

def mostrar_resultado(root, mensaje):
    """Crea una ventana modal simple para mostrar el mensaje."""
    # Crear una nueva ventana Toplevel
    ventana_resultado = Toplevel()
    ventana_resultado.title("Resultado")
    ventana_resultado.geometry("300x150")  # Dimensiones de la ventana
    ventana_resultado.resizable(False, False)  # Evitar que la ventana sea redimensionable
    # Etiqueta para mostrar el mensaje
    label_mensaje = Label(ventana_resultado, text=mensaje, font=("Arial", 12), wraplength=250)
    label_mensaje.pack(pady=20)
    # Botón para cerrar la ventana
    boton_cerrar = Button(ventana_resultado, text="Cerrar", command=ventana_resultado.destroy)
    boton_cerrar.pack(pady=10)
    # Centrar la ventana modal sobre la ventana principal
    ventana_resultado.transient(root)  # Relacionar la ventana con la ventana principal
    ventana_resultado.grab_set()  # Hacer que sea modal (previene la interacción con otras ventanas)
    root.wait_window(ventana_resultado)  # Esperar hasta que la ventana sea cerrada

def logicaJuego4(frame):
    # Fondo en canvas
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Obtiene la dirección actual
    ruta_fondo = os.path.join(base_dir, "..", "images", "juego4", "fondoPatio.png")

    # Carga de gifs
    ruta_insecto1 = os.path.join(base_dir, "..", "images", "juego4", "insecto1.gif")
    ruta_insecto2 = os.path.join(base_dir, "..", "images", "juego4", "insecto2.gif")
    ruta_insecto3 = os.path.join(base_dir, "..", "images", "juego4", "insecto3.gif")
    ruta_insecto4 = os.path.join(base_dir, "..", "images", "juego4", "insecto4.gif")
    ruta_mascota1 = os.path.join(base_dir, "..", "images", "juego4", "perro1.gif")
    ruta_mascota2 = os.path.join(base_dir, "..", "images", "juego4", "perro2.gif")
    ruta_mascota3 = os.path.join(base_dir, "..", "images", "juego4", "perro3.gif")
    ruta_mascota4 = os.path.join(base_dir, "..", "images", "juego4", "perro4.gif")

    root = Tk()

    # Configuramos el canvas dentro del frame proporcionado
    canvas = Canvas(frame, width=1100, height=600)  # Crear el canvas dentro del frame
    canvas.pack()  # O usa .grid() o .place() si prefieres otro layout

    # Normalizar las rutas para asegurarse de que usan las barras invertidas correctamente
    ruta_gif_insecto1_normalizada = os.path.normpath(ruta_insecto1)
    ruta_gif_insecto2_normalizada = os.path.normpath(ruta_insecto2)
    ruta_gif_insecto3_normalizada = os.path.normpath(ruta_insecto3)
    ruta_gif_insecto4_normalizada = os.path.normpath(ruta_insecto4)
    ruta_gif_mascota1_normalizada = os.path.normpath(ruta_mascota1)
    ruta_gif_mascota2_normalizada = os.path.normpath(ruta_mascota2)
    ruta_gif_mascota3_normalizada = os.path.normpath(ruta_mascota3)
    ruta_gif_mascota4_normalizada = os.path.normpath(ruta_mascota4)
    ruta_imagen_fondo_normalizada = os.path.normpath(ruta_fondo)

    grupoInsectos = [ruta_gif_insecto1_normalizada, ruta_gif_insecto2_normalizada,ruta_gif_insecto3_normalizada,ruta_gif_insecto4_normalizada]
    grupoMascotas = [ruta_gif_mascota1_normalizada, ruta_gif_mascota2_normalizada,ruta_gif_mascota3_normalizada,ruta_gif_mascota4_normalizada]
    crear_gif_con_fondo(root, 
                        grupoInsectos,  # Lista de insectos
                        grupoMascotas,  # Lista de mascotas
                        ruta_imagen_fondo_normalizada, 
                        width=1100, height=600, gif_height=100)
    root.mainloop() 
def logicaJuego4(frame):
    # Fondo en canvas
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Obtiene la dirección actual
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