import cv2
import mediapipe as mp
import math

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

            # Calcular la distancia entre la muñeca y el dedo índice para detectar un "gesto de clic"
            wrist_x, wrist_y = int(wrist.x * frame.shape[1]), int(wrist.y * frame.shape[0])
            index_x, index_y = int(index_finger.x * frame.shape[1]), int(index_finger.y * frame.shape[0])

            distance = math.sqrt((index_x - wrist_x) ** 2 + (index_y - wrist_y) ** 2)

            # Si la distancia es suficientemente pequeña, consideramos un gesto de "clic"
            if distance < 50:
                return "click"  # El gesto es un clic
            else:
                return "no_click"  # No hay clic

    # Si no se detectan manos
    return "no_hand"

# Función para cerrar la cámara
def close_camera(camera):
    camera.release()
    cv2.destroyAllWindows()
