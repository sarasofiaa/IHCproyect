#baseJuego.py Se reutilizo la funcionalidad de main.py 
#Descripción: Aqui se modifica todo lo que tiene que ver con funcionalidad del mouse para cada juego en especifico y ventana del juego
#lleno de comentarios y reutilizado para todos los juegos
import tkinter as tk
from PIL import Image, ImageTk
import cv2
import mediapipe as mp
import os
from pynput.mouse import Button, Controller
from nonmouse.utils2 import calculate_distance, draw_circle, calculate_moving_average
from .datosGlobales import get_game_active
from .utils2 import cargar_imagen

class GameWindow:
    def __init__(self,gameName):
        self.root = tk.Tk()
        self.root.title(gameName) #Se asigna el nombre del juego llamado al crear el objeto
        
        self.root.attributes('-fullscreen', True)  # Activa el modo de pantalla completa
        self.root.bind('<Escape>',self.exit_fullscreen) #Pantalla completa para el videojuego, esc para pantalla extendida
       
        #COLORES
        color_principal = "#141240" #Azul
        color_botones = "#4f722a" #Verde

        #IMAGENES
        base_dir = os.path.dirname(os.path.abspath(__file__)) #Obtiene la direccion actual
        ruta_logo = os.path.join(base_dir, "..", "images", "titulo.png")
        imagen_logo = cargar_imagen(ruta_logo,altura=50)

        # FRAMES 
        # Frame principal
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(expand=True, fill='both')

        # Frame para el juego (lado izquierdo) Se tiene que reemplazar con cada juego en especifico
        self.game_frame = tk.Frame(self.main_frame, width=1250, height=950)
        self.game_frame.pack(side='left', expand=True, fill='both')

        # Contenedor vertical para cámara y descripción
        self.camera_and_description_frame = tk.Frame(self.main_frame, bg="lightblue", width=270, height=850)
        self.camera_and_description_frame.pack(side='right', fill='both', padx=0, pady=0)

        # Frame para la cámara (dentro del contenedor)
        self.camera_frame = tk.Frame(self.camera_and_description_frame, width=250, height=180)
        self.camera_frame.pack(side='top', fill='both',  padx=10, pady=10)

        # Frame para la descripción (debajo de la cámara, dentro del contenedor)
        self.description_frame = tk.Frame(self.camera_and_description_frame, bg=color_principal, width=270, height=780)
        self.description_frame.pack(side='bottom', fill='both', expand=True)

        # Frame contenedor con el logo Y boton de regresar dentro de la descripción
        self.logob_frame = tk.Frame(self.description_frame, height = 60,bg= color_principal)
        self.logob_frame.pack(side="top", fill='x', expand=False)

        #LABELS
        # Label para mostrar el feed de la cámara
        self.camera_label = tk.Label(self.camera_frame)
        self.camera_label.pack(expand=True, fill='both')

        #Label con el logo en la descripcion al inicio
        self.logo_label = tk.Label(self.logob_frame, image=imagen_logo)
        self.logo_label.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)  # Posiciona el logo en la fila 0
        self.logob_frame.image = imagen_logo #Mantiene la imagen

        #boton de regresar
        self.back_button = tk.Button(self.logob_frame, text="Regresar", bg=color_botones, fg="white")
        self.back_button.grid(row=1, column=0, sticky="nsew", padx=5, pady=10)  # Posiciona el botón en la fila 1

        # Ajustar el layout del frame para expandirse correctamente
        self.logob_frame.grid_rowconfigure(0, weight=1)  # La fila del logo puede expandirse
        self.logob_frame.grid_rowconfigure(1, weight=1)  # La fila del botón puede expandirse
        self.logob_frame.grid_columnconfigure(0, weight=1)  # La columna única ocupa todo el ancho

        # Configuración inicial
        self.setup_camera()
        self.setup_mediapipe()
        self.setup_mouse_control()
        
        # Iniciar la actualización de la cámara
        self.update_camera()

    # Expansion de la pantalla cuando se sale de la pantalla completa
    def exit_fullscreen(self, event=None):  # Asegúrate de recibir el evento para la tecla Escape
        self.root.attributes('-fullscreen', False)  # Sal del modo pantalla completa
        self.root.state('zoomed')  # Ajusta la ventana al modo extendido
        self.main_frame.pack(expand=True, fill='both')  # Reajusta el frame principal
        print("Saliste del modo pantalla completa y ahora estás en modo extendido")


    # Set frame de juego 
    def setGameFrame(self,game_logic):
        # Limpia el frame actual
        for widget in self.game_frame.winfo_children():
            widget.destroy()
        game_logic(self.game_frame)
    # Set frame de descripcion puntaje titulo etc (debajo de la camara) informacion del juego quizas?  
    def setDescriptionFrame(self,game_description): #Falta ajustar 
        
        print("Falta ajustar")

#CONFIGURACION DE LA CAMARA ___________________________________________________________________________________________________________
    def setup_camera(self):
        self.cap_width = 250
        self.cap_height = 180
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FPS, 60)
        cfps = int(self.cap.get(cv2.CAP_PROP_FPS))
        if cfps < 30:
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.cap_width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.cap_height)
        
    def setup_mediapipe(self):
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            min_detection_confidence=0.8,# Confianza en la detección
            min_tracking_confidence=0.8,# Confianza en el seguimiento
            max_num_hands=1  # Número máximo de manos detectadas
        )

    def setup_mouse_control(self): #Valores predeterminados
        self.mouse = Controller()
        self.preX, self.preY = 0, 0
        self.nowCli, self.preCli = 0, 0
        self.norCli, self.prrCli = 0, 0
        self.douCli = 0
        self.i, self.k, self.h = 0, 0, 0
        self.LiTx, self.LiTy = [], []
        self.list0x, self.list0y = [], []
        self.list1x, self.list1y = [], []
        self.list4x, self.list4y = [], []
        self.list6x, self.list6y = [], []
        self.list8x, self.list8y = [], []
        self.list12x, self.list12y = [], []
        self.moving_average = [[0] * 3 for _ in range(3)]
        self.nowUgo = 1
        self.start = float('inf')
        self.c_start = float('inf')
        self.dis = 0.7
        self.kando =11.0  # Sensibilidad del mouse
        self.ran = 6  # Suavizado

    def process_hand_tracking(self, image, results):
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

                if self.i == 0:
                    self.preX = hand_landmarks.landmark[8].x
                    self.preY = hand_landmarks.landmark[8].y
                    self.i += 1

                # Procesar landmarks y movimiento del mouse
                self.process_landmarks(hand_landmarks, image)

                # Detectar color por gesto
                #color_detectado = self.detectar_color_con_gesto(results)
                #if color_detectado:
                #    self.procesar_gesto(color_detectado)  # Llama al método del juego

        return image

    def process_landmarks(self, hand_landmarks, image):
        # Calcular promedios móviles para los landmarks
        landmark0 = [calculate_moving_average(hand_landmarks.landmark[0].x, self.ran, self.list0x),
                    calculate_moving_average(hand_landmarks.landmark[0].y, self.ran, self.list0y)]
        landmark1 = [calculate_moving_average(hand_landmarks.landmark[1].x, self.ran, self.list1x),
                    calculate_moving_average(hand_landmarks.landmark[1].y, self.ran, self.list1y)]
        landmark4 = [calculate_moving_average(hand_landmarks.landmark[4].x, self.ran, self.list4x),
                    calculate_moving_average(hand_landmarks.landmark[4].y, self.ran, self.list4y)]
        landmark8 = [calculate_moving_average(hand_landmarks.landmark[8].x, self.ran, self.list8x),
                    calculate_moving_average(hand_landmarks.landmark[8].y, self.ran, self.list8y)]

        # Calcular movimiento del mouse
        nowX = calculate_moving_average(hand_landmarks.landmark[8].x, self.ran, self.LiTx)
        nowY = calculate_moving_average(hand_landmarks.landmark[8].y, self.ran, self.LiTy)
        
        dx = self.kando * (nowX - self.preX) * self.cap_width
        dy = self.kando * (nowY - self.preY) * self.cap_height
        
        self.preX = nowX
        self.preY = nowY

        # Mover el mouse
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        current_x, current_y = self.mouse.position

        new_x = max(0, min(screen_width, current_x + dx))
        new_y = max(0, min(screen_height, current_y + dy))
        
        self.mouse.position = (new_x, new_y)
#AQUI ESTA LA LOGICA SEGUN EL TIPO DE JUEGO ESCOGIDO FLAGS
        #JUEGO 4 PELIZCA EL ANIMAL
        # Detectar gesto de pellizco
        if get_game_active() == 4:
            distancia_pellizco = calculate_distance(landmark4, landmark8)
            if distancia_pellizco < 0.05:
                self.mouse.press(Button.left)
                self.mouse.release(Button.left)
                draw_circle(image, 
                          hand_landmarks.landmark[8].x * image.shape[1],  # Use image width
                          hand_landmarks.landmark[8].y * image.shape[0],  # Use image height 
                          20, (255, 105, 180))
            #Dibujar el juego en el frame donde va el juego

    def update_camera(self):
        success, image = self.cap.read()
        if success:
            image = cv2.flip(image, 1)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = self.hands.process(image_rgb)
            
            # Procesar el tracking de manos
            image = self.process_hand_tracking(image, results)
            
            # Convertir la imagen para mostrarla en Tkinter
            image = cv2.resize(image, (self.cap_width, self.cap_height))
            image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            image = ImageTk.PhotoImage(image=image)
            
            self.camera_label.configure(image=image)
            self.camera_label.image = image
            
        self.root.after(10, self.update_camera)

    def run(self):
        self.root.mainloop()

    def cleanup(self):
        if self.cap is not None:
            self.cap.release()
        self.root.destroy()