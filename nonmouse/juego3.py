import tkinter as tk
import random
import os
import cv2
import mediapipe as mp
from PIL import Image, ImageTk
from .baseJuego import GameWindow
from .utils2 import cargar_imagen, mostrar_gif

def instrucciones():
    root = tk.Tk()
    root.title("Instrucciones - Atrapa los Colores")
    root.geometry("1000x600")

    # Cargar imagen de fondo
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.dirname(base_dir)
        ruta_imagen_fondo = os.path.join(project_dir, "images", "juego3", "fondoInstruccion.png")

        imagen_fondo = Image.open(ruta_imagen_fondo)
        imagen_fondo = imagen_fondo.resize((1000, 600), Image.ANTIALIAS)
        fondo_tk = ImageTk.PhotoImage(imagen_fondo)

        fondo_label = tk.Label(root, image=fondo_tk)
        fondo_label.place(relwidth=1, relheight=1)
        fondo_label.image = fondo_tk
    except Exception as e:
        print(f"No se pudo cargar la imagen de fondo: {e}")

    # Descripción del juego con gestos
    descripcion = """
    ¡Atrapa los colores correctos con el gesto correspondiente!
    
    Reglas:
    - Cada color requiere un gesto específico
    - Atrapa el color correcto con el gesto correcto
    - Tienes 3 oportunidades de fallar
    - Acumula la mayor puntuación posible

    Gestos:
    - Rojo: Puño cerrado
    - Verde: Palma abierta
    - Azul: Mano en forma de L
    - Amarillo: Mano con 3 dedos
    - Naranja: Mano con 4 dedos
    """

    # Label de descripción
    tk.Label(
        root,
        text=descripcion,
        font=("Arial", 15),
        justify="center",
        bg="#d4e7ff",
        fg="black",
        width=60,
        height=20,
        padx=2,
        pady=2,
        anchor="nw"
    ).place(x=125, y=130)

    # Instrucción visual
    try:
        ruta_imagen = os.path.join(project_dir, "images", "juego3", "color_catch.png")
        imagen = Image.open(ruta_imagen)
        imagen = imagen.resize((200, 200), Image.ANTIALIAS)
        imagen_tk = ImageTk.PhotoImage(imagen)

        imagen_label = tk.Label(root, image=imagen_tk, bg="#d4e7ff")
        imagen_label.image = imagen_tk
        imagen_label.place(x=170, y=450)
        
    except Exception as e:
        print(f"No se pudo cargar la imagen: {e}")

    # Botón de continuar
    def continuar():
        root.destroy()
        game_window = GameWindow("Juego 3: Color Match")
        game_window.setGameFrame(logica_juego3)
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
    boton_continuar.place(x=500, y=500)

    root.mainloop()

def logica_juego3(game_frame):
    # Configuración de mediapipe para probar
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.8
    )

    #diccionario de gestos por color
    GESTOS_POR_COLOR = {
        "Rojo": "puño",
        "Verde": "palma",
        "Azul": "l",
        "Amarillo": "tres_dedos",
        "Naranja": "cuatro_dedos"
    }

    #diccionar de colores
    COLORES_HEX = {
        "Rojo": "#FF0000",
        "Verde": "#00FF00",
        "Azul": "#0000FF", 
        "Amarillo": "#FFFF00",
        "Naranja": "#FFA500"
    }

    #variables
    COLORES_OBJETIVO = list(GESTOS_POR_COLOR.keys())
    color_actual = None
    gesto_actual = None
    score = 0
    juego_activo = True
    esperando_gesto_correcto = False

    cap = cv2.VideoCapture(0)

    #canvas para el juego
    canvas_game = tk.Canvas(game_frame)
    canvas_game.pack(fill="both", expand=True)

    #canvas de camara
    video_canvas = tk.Label(game_frame)
    video_canvas.place(relx=0.85, rely=0.5, anchor="center", width=300, height=225)

    # Configurar fondo
    #base_dir = os.path.dirname(os.path.abspath(__file__))
    #ruta_fondo = os.path.join(base_dir, "..", "images", "juego3", "fondoPatio.png")

    '''
    def ajustar_fondo(event=None):
        frame_height = game_frame.winfo_height()
        fondo = cargar_imagen(ruta_fondo, altura=frame_height)
        if fondo:
            canvas_game.create_image(0, 0, image=fondo, anchor="nw")
            canvas_game.image = fondo

    game_frame.bind("<Configure>", ajustar_fondo)
    '''

    #labels con info del juego
    score_label = tk.Label(game_frame, text=f"Puntuación: {score}", font=("Arial", 16))
    score_label.place(x=10, y=10)

    color_objetivo_label = tk.Label(
        game_frame, 
        text="Color", 
        font=("Arial", 24, "bold"), 
        width=10, 
        height=2
    )
    color_objetivo_label.place(relx=0.4, rely=0.2, anchor="center")

    gesto_label = tk.Label(
        game_frame, 
        text="Gesto", 
        font=("Arial", 20), 
        fg="black"
    )
    gesto_label.place(relx=0.4, rely=0.3, anchor="center")

    feedback_label = tk.Label(
        game_frame, 
        text="", 
        font=("Arial", 18, "bold"), 
        width=30
    )
    feedback_label.place(relx=0.4, rely=0.4, anchor="center")

    def detectar_gesto(landmarks):
        """
        Detecta el gesto basado en la posición de los dedos
        landmarks: resultados de MediaPipe Hands
        """
        if not landmarks:
            return None

        # Extraer puntos de las puntas de los dedos y nudillos
        tips = [
            landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP],
            landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP],
            landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP],
            landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP],
            landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]
        ]

        dedos_levantados = 0
        for i, tip in enumerate(tips):
            if tip.y < landmarks.landmark[mp_hands.HandLandmark.WRIST].y:
                dedos_levantados += 1

        #mapeo de gestos
        if dedos_levantados == 0:
            return "puño"
        elif dedos_levantados == 5:
            return "palma"
        elif dedos_levantados == 1 and tips[1].y < landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y:
            return "l"
        elif dedos_levantados == 3:
            return "tres_dedos"
        elif dedos_levantados == 4:
            return "cuatro_dedos"
        
        return None

    def iniciar_nueva_ronda():
        nonlocal color_actual, gesto_actual, esperando_gesto_correcto
        color_actual = random.choice(COLORES_OBJETIVO)
        gesto_actual = GESTOS_POR_COLOR[color_actual]
        esperando_gesto_correcto = False
        
        #color de label con el color obj
        color_objetivo_label.config(
            text=color_actual, 
            bg=COLORES_HEX[color_actual], 
            fg="white" if color_actual != "Amarillo" else "black"
        )
        
        gesto_label.config(text=f"Gesto: {gesto_actual}")
        
        feedback_label.config(text="", bg="SystemButtonFace")

    def iniciar_nuevo_juego():
        nonlocal score, color_actual, gesto_actual, esperando_gesto_correcto, juego_activo
        
        # Restablecer estado inicial del juego
        score = 0
        color_actual = None
        gesto_actual = None
        esperando_gesto_correcto = False
        juego_activo = True

        canvas_game.delete("all")

        #ocultar widgets relacionados con el final del juego
        for widget in game_frame.winfo_children():
            widget.place_forget()

        #restablecer etiquetas
        score_label.config(text=f"Puntuación: {score}")
        score_label.place(x=10, y=10)
        color_objetivo_label.place(relx=0.4, rely=0.2, anchor="center")
        gesto_label.place(relx=0.4, rely=0.3, anchor="center")
        feedback_label.place(relx=0.4, rely=0.4, anchor="center")
        boton_detener.place(x=10, y=70)
        video_canvas.place(relx=0.85, rely=0.5, anchor="center", width=300, height=225)

        # Iniciar nueva ronda y procesamiento de video
        iniciar_nueva_ronda()
        procesar_frame()
        #la camara se queda pegada

    def detener_juego():
        nonlocal juego_activo
        juego_activo = False
        cap.release()
        
        #mostrar puntuación
        canvas_game.delete("all")
        resultado_label = tk.Label(
            game_frame, 
            text=f"Juego terminado\nPuntuación: {score}", 
            font=("Arial", 20, "bold"), 
            bg="lightgray", 
            fg="black"
        )
        resultado_label.place(relx=0.5, rely=0.4, anchor="center")

        #btn para inicar juego nuevo
        boton_nuevo_juego = tk.Button(
            game_frame, 
            text="Iniciar Nuevo Juego", 
            font=("Arial", 14), 
            bg="blue", 
            fg="white",
            command=iniciar_nuevo_juego
        )
        boton_nuevo_juego.place(relx=0.5, rely=0.6, anchor="center")

    #btn para detener el juego
    boton_detener = tk.Button(
        game_frame, 
        text="Detener Juego", 
        command=detener_juego,
        font=("Arial", 12),
        bg="red",
        fg="white"
    )
    boton_detener.place(x=10, y=70)

    def procesar_frame():
        nonlocal score, esperando_gesto_correcto
        
        # Salir si el juego no está activo
        if not juego_activo:
            return

        ret, frame = cap.read()
        if not ret:
            return

        #ajustes de frame
        frame = cv2.flip(frame, 1)

        # Convertir a RGB para MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Procesar con mediapipe
        results = hands.process(rgb_frame)

        gesto_detectado = None
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Dibujar landmarks
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                # Detectar gesto
                gesto_detectado = detectar_gesto(hand_landmarks)

        # Convertir frame a formato de Tkinter
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        img_tk = ImageTk.PhotoImage(image=img)
        video_canvas.img_tk = img_tk
        video_canvas.configure(image=img_tk)

        # Si se detectó un gesto, procesar
        if gesto_detectado and not esperando_gesto_correcto:
            if gesto_detectado == gesto_actual:
                # Acierto
                score += 1
                score_label.config(text=f"Puntuación: {score}")
                
                feedback_label.config(
                    text="¡Correcto!", 
                    bg="green", 
                    fg="white"
                )
                
                esperando_gesto_correcto = True
                game_frame.after(1000, iniciar_nueva_ronda)
            else:
                # Gesto incorrecto
                feedback_label.config(
                    text="¡Gesto incorrecto!", 
                    bg="red", 
                    fg="white"
                )

        game_frame.after(50, procesar_frame)

    #iniciar el juego
    iniciar_nueva_ronda()
    
    #iniciar procesamiento de video
    procesar_frame()