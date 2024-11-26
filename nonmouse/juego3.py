import tkinter as tk
import random
import cv2
import mediapipe as mp
from .baseJuego import GameWindow

# Definimos los colores
COLORES = {
    "Rojo": "#FF0000",
    "Verde": "#00FF00",
    "Azul": "#0000FF",
    "Amarillo": "#FFFF00",
    "Naranja": "#FFA500",
    "Morado": "#800080",
}

class JuegoColores(GameWindow):
    def __init__(self):
        self.deteccion_habilitada = True
        
        #Llamar al constructor padre
        super().__init__("Juego de Colores")
        
        self.color_actual = None
        self.color_actual_nombre = None

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
        self.mp_drawing = mp.solutions.drawing_utils

        self.setup_game_ui()
        self.nueva_ronda()
        self.update_camera()

    def setup_game_ui(self):
        """
        Configura los elementos de la interfaz del juego.
        """
        #Título del color
        self.titulo = tk.Label(self.game_frame, text="", font=("Arial", 18, "bold"))
        self.titulo.pack(pady=10)

        #Etiqueta de feedback
        self.feedback_label = tk.Label(self.game_frame, text="", font=("Arial", 20))
        self.feedback_label.pack(pady=10)

        # Configuración de la cámara
        self.camera_frame = tk.Label(self.game_frame)
        self.camera_frame.pack(pady=10, fill="both", expand=True)

    def nueva_ronda(self):
        #Configura una nueva ronda del juego seleccionando un color aleatorio.
        self.deteccion_habilitada = True
        self.feedback_label.config(text="")
        self.color_actual_nombre = random.choice(list(COLORES.keys()))
        self.color_actual = COLORES[self.color_actual_nombre]
        self.titulo.config(text=f"Selecciona el color: {self.color_actual_nombre}")

    def procesar_gesto(self, color_detectado):
        #Procesa el color detectado según el gesto realizado.
        if color_detectado == self.color_actual_nombre and self.deteccion_habilitada:
            self.deteccion_habilitada = False
            self.feedback_label.config(text="✔ Correcto!", fg="green")
            
            # Pausar 3 segundos antes de la nueva ronda
            self.root.after(3000, self.nueva_ronda)
        elif color_detectado and self.deteccion_habilitada:
            self.feedback_label.config(text="✘ Incorrecto.", fg="red")

    def detectar_color_con_gesto(self, results):
        #Detecta gestos basados en la posición de los dedos y los mapea a colores.
        if not results.multi_hand_landmarks:
            return None  #Si no se detecta una mano, no hay color

        hand_landmarks = results.multi_hand_landmarks[0]  # Usamos la primera mano detectada

        landmarks = hand_landmarks.landmark

        # Posiciones de las puntas de los dedos
        finger_tips = [landmarks[i] for i in [4, 8, 12, 16, 20]]

        # Posiciones de las bases de los dedos (nudos)
        finger_bases = [landmarks[i] for i in [2, 6, 10, 14, 18]]

        # Determinar si los dedos están levantados
        dedos_levantados = [
            finger_tips[i].y < finger_bases[i].y for i in range(len(finger_tips))
        ]

        # Mapeo de gestos a colores
                                #Pulgar, índica, medio, anular, meñique
        if dedos_levantados == [False, False, True, True, True]:
            return "Rojo"
        elif dedos_levantados == [False, True, True, False, False]:
            return "Verde"
        elif dedos_levantados == [True, True, True, True, True]:
            return "Azul"
        elif dedos_levantados == [True, False, False, False, False]:
            return "Amarillo"
        elif dedos_levantados == [True, True, False, False, False]:
            return "Naranja"
        elif dedos_levantados == [False, False, False, False, False]:
            return "Morado"

        return None

    def process_hand_tracking(self, image, results):
        #Sobrescribe el método para incluir la detección de colores.
        image = super().process_hand_tracking(image, results)
        if self.deteccion_habilitada:
            color_detectado = self.detectar_color_con_gesto(results)
            if color_detectado:
                self.procesar_gesto(color_detectado)
        return image

    def run(self):
        #Inicia la interfaz principal del juego.
        self.root.mainloop()


def instrucciones():
    #Ventana emergente con las instrucciones del juego de colores.
    def continuar():
        root.destroy()
        juego = JuegoColores()
        juego.run()

    root = tk.Tk()
    root.title("Instrucciones")
    root.geometry("500x500")

    tk.Label(root, text="Instrucciones", font=("Arial", 16, "bold")).pack(pady=10)

    tk.Label(
        root,
        text=(
            "El objetivo del juego es seleccionar el color mostrado en pantalla "
            "realizando gestos con las manos.\n\n"
            "Usa los siguientes gestos:\n"
            "- Medio, anula y meñique levantados: Rojo\n"
            "- Índice y medio levantados: Verde\n"
            "- Todos los dedos levantados: Azul\n"
            "- Solo el pulgar levantado: Amarillo\n"
            "- Pulgar e índice levantados: Naranja\n"
            "- Mano cerrada: Morado"
        ),
        wraplength=450,
        justify="left",
    ).pack(pady=20)

    tk.Button(root, text="Continuar", command=continuar).pack(pady=20)
    
    root.mainloop()

if __name__ == "__main__":
    instrucciones()