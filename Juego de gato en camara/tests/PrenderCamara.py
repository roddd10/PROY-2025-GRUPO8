import cv2
import mediapipe as mp
import numpy as np

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2)
mp_draw = mp.solutions.drawing_utils

# Iniciar la cámara
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Voltear horizontal para efecto espejo
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    # Dibujar la cuadrícula 3x3
    color = (255, 255, 255)
    thickness = 2
    step_x = w // 3
    step_y = h // 3

    for i in range(1, 3):
        # Líneas verticales
        cv2.line(frame, (i * step_x, 0), (i * step_x, h), color, thickness)
        # Líneas horizontales
        cv2.line(frame, (0, i * step_y), (w, i * step_y), color, thickness)

    # Procesar la imagen para detección de manos
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Dibujar la mano
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Obtener el centro de la palma (landmark 0)
            cx = int(hand_landmarks.landmark[0].x * w)
            cy = int(hand_landmarks.landmark[0].y * h)

            # Dibujar círculo y mostrar coordenadas
            cv2.circle(frame, (cx, cy), 10, (0, 255, 0), -1)
            cv2.putText(frame, f"({cx}, {cy})", (cx + 10, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Mostrar en pantalla
    cv2.imshow("Tres en línea + Detección de manos", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()