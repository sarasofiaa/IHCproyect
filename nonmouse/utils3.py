import cv2
import mediapipe as mp
import math
import numpy as np

# Inicializar MediaPipe para detección de manos
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Función para detectar gestos
def detect_gesture(frame):
    # Convertir la imagen de BGR a RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    # Si se detectan manos
    if result.multi_hand_landmarks:
        for landmarks in result.multi_hand_landmarks:
            # Dibujar los puntos de la mano detectada en la imagen
            mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

            # Obtener la posición de la muñeca (punto de referencia)
            wrist = landmarks.landmark[mp_hands.HandLandmark.WRIST]
            index_finger = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            # Si la distancia entre el pulgar y el índice es pequeña, podría indicar un clic
            thumb_tip = landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            # Calcular la distancia entre el pulgar y el índice (simple ejemplo)
            distance = np.sqrt((thumb_tip.x - index_tip.x) ** 2 + (thumb_tip.y - index_tip.y) ** 2)

            if distance < 0.05:  # Si la distancia es pequeña, detectar un "click"
                return "click"

    # Si no se detectan manos
    return "no_hand"

# Función para cerrar la cámara
def close_camera(camera):
    camera.release()
    cv2.destroyAllWindows()
