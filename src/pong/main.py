# importar librerías
import cv2
import mediapipe as mp
import numpy as np

# configuración inicial
RESOLUCION_CAMARA = (640, 480)

# iniciar cámara
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, RESOLUCION_CAMARA[0])
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, RESOLUCION_CAMARA[1])

# configurar mediapipe hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# Pelota
ball_pos = np.array([320, 240], dtype=np.float32)
ball_radius = 15
ball_vel = np.array([4.0, 3.0], dtype=np.float32)
max_speed = 100.0
acceleration = 0.07  # Aumenta con cada frame

score_left = 0
score_right = 0
font = cv2.FONT_HERSHEY_SIMPLEX

# Bucle principal
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)


    hand_lines = []

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Centro de la paleta (landmark 9)
            cx = int(hand_landmarks.landmark[9].x * RESOLUCION_CAMARA[0])
            cy = int(hand_landmarks.landmark[9].y * RESOLUCION_CAMARA[1])
            center = np.array([cx, cy], dtype=np.float32)

            # Dirección de la paleta (de landmark 0 a 9)
            x0 = int(hand_landmarks.landmark[0].x * RESOLUCION_CAMARA[0])
            y0 = int(hand_landmarks.landmark[0].y * RESOLUCION_CAMARA[1])
            dir_vec = center - np.array([x0, y0], dtype=np.float32)
            length = np.linalg.norm(dir_vec)
            if length == 0:
                continue
            unit_dir = dir_vec / length

            # Largo fijo de la paleta
            fixed_half_length = 60
            offset = unit_dir * fixed_half_length

            pt1 = (int(cx - offset[0]), int(cy - offset[1]))
            pt2 = (int(cx + offset[0]), int(cy + offset[1]))

            # Dibujar paleta
            cv2.line(frame, pt1, pt2, (0, 255, 0), 5)
            hand_lines.append((pt1, pt2))

    # Mover la pelota
    ball_pos += ball_vel

    # Aplicar aceleración si no ha alcanzado velocidad máxima
    speed = np.linalg.norm(ball_vel)
    if speed < max_speed:
        ball_vel += (ball_vel / speed) * acceleration

    bx, by = int(ball_pos[0]), int(ball_pos[1])

    # Rebote en los bordes superior e inferior
    if by - ball_radius <= 0 or by + ball_radius >= RESOLUCION_CAMARA[1]:
        ball_vel[1] *= -1

    # Si la pelota toca los bordes izquierdo o derecho, actualiza marcador y reinicia posición y velocidad
    if bx - ball_radius <= 0:
        score_right += 1
        ball_pos = np.array([RESOLUCION_CAMARA[0] // 2, RESOLUCION_CAMARA[1] // 2], dtype=np.float32)
        ball_vel = np.array([4.0, 3.0], dtype=np.float32)  # reinicio velocidad hacia la derecha

    elif bx + ball_radius >= RESOLUCION_CAMARA[0]:
        score_left += 1
        ball_pos = np.array([RESOLUCION_CAMARA[0] // 2, RESOLUCION_CAMARA[1] // 2], dtype=np.float32)
        ball_vel = np.array([-4.0, 3.0], dtype=np.float32)  # reinicio velocidad hacia la izquierda

    # Rebote con paletas (manos)
    for (x1, y1), (x2, y2) in hand_lines:
        # Vector de la paleta
        paddle_vec = np.array([x2 - x1, y2 - y1], dtype=np.float32)
        paddle_len = np.linalg.norm(paddle_vec)
        if paddle_len == 0:
            continue
        paddle_unit = paddle_vec / paddle_len

        # Vector normal a la paleta (perpendicular)
        normal = np.array([-paddle_unit[1], paddle_unit[0]], dtype=np.float32)

        # Vector desde punto medio de paleta hasta la pelota
        mid_point = np.array([(x1 + x2) / 2, (y1 + y2) / 2], dtype=np.float32)
        to_ball = ball_pos - mid_point

        # Comprobar si la pelota está cerca de la paleta (distancia corta)
        distance = abs(np.dot(to_ball, normal))
        proj_along_paddle = np.dot(to_ball, paddle_unit)
        if distance < ball_radius + 5 and abs(proj_along_paddle) < paddle_len / 2:
            # Reflejar la velocidad respecto a la normal
            print("collision",  2 * np.dot(ball_vel, normal) * normal)
            ball_vel = ball_vel - 2 * np.dot(ball_vel, normal) * normal

    # Dibujar la pelota
    cv2.circle(frame, (bx, by), ball_radius, (255, 0, 0), -1)

    # Dibujar marcador centrado arriba
    score_text = f"{score_left} - {score_right}"
    (text_width, text_height), _ = cv2.getTextSize(score_text, font, 1.5, 3)
    text_x = (RESOLUCION_CAMARA[0] - text_width) // 2
    cv2.putText(frame, score_text, (text_x, 50), font, 1.5, (0, 0, 0), 3, cv2.LINE_AA)

    # Mostrar en pantalla
    cv2.imshow("Pong con manos", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC para salir
        break

cap.release()
cv2.destroyAllWindows()
