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
from .datosGlobales import get_game_active, get_instruction_active, set_instruction_active
from .utils2 import cargar_imagen
import math

class GameWindow:
    current_instance = None

    def __init__(self,gameName, is_instruction = False):
        self.root = tk.Tk()
        self.root.title(gameName) #Se asigna el nombre del juego llamado al crear el objeto
        set_instruction_active(is_instruction)
        if is_instruction:
            self.root.state('normal')
        else:
            self.root.attributes('-fullscreen', True)
            self.root.bind('<Escape>', self.exit_fullscreen)
        GameWindow.current_instance = self
            
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

        # Label con el logo en la descripción al inicio
        self.logo_label = tk.Label(self.logob_frame, image=imagen_logo)
        self.logo_label.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)  # Posiciona el logo en la fila 0
        self.logob_frame.image = imagen_logo  # Mantiene la imagen

        # Crear el label para mostrar la información del juego, que irá debajo del logo y encima del botón
        self.game_info_label = tk.Label(self.logob_frame, text="Información del juego", bg="lightblue", font=("Arial", 12))
        self.game_info_label.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)  # Posiciona la información en la fila 1

        # Botón de regresar, que irá debajo de la etiqueta de información
        self.back_button = tk.Button(self.logob_frame, text="Regresar", bg=color_botones, fg="white")
        self.back_button.grid(row=2, column=0, sticky="nsew", padx=5, pady=10)  # Posiciona el botón en la fila 2

        # Ajustar el layout del frame para expandirse correctamente
        self.logob_frame.grid_rowconfigure(0, weight=1)  # La fila del logo puede expandirse
        self.logob_frame.grid_rowconfigure(1, weight=1)  # La fila de la información del juego puede expandirse
        self.logob_frame.grid_rowconfigure(2, weight=1)  # La fila del botón puede expandirse
        self.logob_frame.grid_columnconfigure(0, weight=1)  # La columna única ocupa todo el ancho


        # Configuración inicial
        self.setup_camera()
        self.setup_mediapipe()
        self.setup_mouse_control()
        
        # Iniciar la actualización de la cámara
        self.update_camera()
    

    @staticmethod
    def get_current_instance():
        """Devuelve la instancia actual de GameWindow"""
        return GameWindow.current_instance
    
    # Método para actualizar la información del juego
    def update_game4_info(self, score, time_left):
        # Actualiza la etiqueta con el puntaje y el tiempo restante
        self.game_info_label.config(text=f"¡Pellizca para atrapar\n a los insectos!\nPuntaje: {score}\nTiempo restante: {time_left}s")
        
            
    # Expansion de la pantalla cuando se sale de la pantalla completa
    def exit_fullscreen(self, event=None):  # Asegúrate de recibir el evento para la tecla Escape
        self.root.attributes('-fullscreen', False)  # Sal del modo pantalla completa
        self.root.state('zoomed')  # Ajusta la ventana al modo pantalla extendida 100%
        self.main_frame.pack(expand=True, fill='both')  # Reajusta el frame principal
        print("Saliste del modo pantalla completa y ahora estás en modo extendido") #Depuracion BORRAR 


    # Set frame de juego en especifico
    def setGameFrame(self,game_logic):
        # Limpia el frame actual
        for widget in self.game_frame.winfo_children():
            widget.destroy()
        game_logic(self.game_frame)

    # Set frame de descripcion puntaje titulo etc (debajo de la camara) informacion del juego quizas?  
    def setDescriptionFrame(self,game_description): #Falta ajustar 
        game_description(self.description_frame)
        

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
        #JUEGO 4 PELIZCA EL insecto        
        if get_game_active() == 4:
            if get_instruction_active()  == True:
                #Ocultar el mouse
                self.root.configure(cursor="None")
                # Puntos clave para detectar el deslizamiento
                wrist = hand_landmarks.landmark[self.mp_hands.HandLandmark.WRIST]
                thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
                index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
                pinky_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_TIP]
                
                # Lista para almacenar posiciones anteriores de la mano
                if not hasattr(self, 'hand_positions'):
                    self.hand_positions = []
                
                # Calcular el centro de la mano
                hand_center_x = (wrist.x + thumb_tip.x + index_tip.x + pinky_tip.x) / 4
                
                # Guardar la posición actual
                self.hand_positions.append(hand_center_x)
                
                # Mantener solo las últimas 10 posiciones
                if len(self.hand_positions) > 10:
                    self.hand_positions.pop(0)
                
                # Detectar deslizamiento horizontal
                if len(self.hand_positions) >= 5:
                    # Calcular el movimiento total
                    total_movement = self.hand_positions[-1] - self.hand_positions[0]
                    
                    # Verificar si es un deslizamiento válido
                    # Verificar si es un deslizamiento válido
                    if abs(total_movement) > 0.15:  # Ajusta este valor según necesites
                        # Limpiar el historial de posiciones
                        self.hand_positions = []
                        self.root.event_generate('<<NextGif>>')
                        return True
                
                # Detectar gesto de "like" (pulgar arriba)
                thumb_up = thumb_tip.y < hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_IP].y
                fingers_closed = all(
                    hand_landmarks.landmark[tip].y > hand_landmarks.landmark[pip].y
                    for tip, pip in [
                        (self.mp_hands.HandLandmark.INDEX_FINGER_TIP, self.mp_hands.HandLandmark.INDEX_FINGER_PIP),
                        (self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP, self.mp_hands.HandLandmark.MIDDLE_FINGER_PIP),
                        (self.mp_hands.HandLandmark.RING_FINGER_TIP, self.mp_hands.HandLandmark.RING_FINGER_PIP),
                        (self.mp_hands.HandLandmark.PINKY_TIP, self.mp_hands.HandLandmark.PINKY_PIP)
                    ]
                )
                
                if thumb_up and fingers_closed:
                    try:
                        self.root.event_generate('<<StartGame>>')
                    except Exception as e:
                        print(f"Error al generar evento: {e}")
                    return True
            # Funcion de desplazar en las instrucciones
            # Mostrar el mensaje de info del juego
            #self.update_game4_info()
            # Detectar gesto de pellizco
            else:
                distancia_pellizco = calculate_distance(landmark4, landmark8)
                if distancia_pellizco < 0.05:
                    self.mouse.press(Button.left)
                    self.mouse.release(Button.left)
                    draw_circle(image, 
                            hand_landmarks.landmark[8].x * image.shape[1],  # Use image width
                            hand_landmarks.landmark[8].y * image.shape[0],  # Use image height 
                            20, (255, 105, 180))
                
                #

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

    def close(self):
        if hasattr(self, 'root'):
            self.root.quit()  # Finaliza el loop principal de la ventana
            self.root.destroy()  # Destruye la ventana
            print("Juego cerrado.")

    def run(self):
        self.root.mainloop()

    def cleanup(self):
        if self.cap is not None:
            self.cap.release()
        self.root.destroy()