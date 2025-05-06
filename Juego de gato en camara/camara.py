#Importar biblioteca
import cv2
import numpy as np
import pygame
import sys
from pygame.locals import *
import mediapipe as mp

# Configuración inicial
RESOLUCION_CAMARA = (640, 480)
TABLERO_SIZE = 3
CELDA_SIZE = 100
MARGEN = 50
ANCHO_VENTANA = TABLERO_SIZE * CELDA_SIZE + 2 * MARGEN
ALTO_VENTANA = TABLERO_SIZE * CELDA_SIZE + 2 * MARGEN

# Colores (BGR)
COLOR_JUGADOR1 = (255, 0, 0)   # Azul (Jugador 1 - cÃ­rculo)
COLOR_JUGADOR2 = (0, 0, 255)   # Rojo (Jugador 2 - cruz)
COLOR_LINEAS = (0, 0, 0)     # Negro para las lí­neas del tablero
COLOR_FONDO = (255, 255, 255)  # Blanco

# Inicializar PyGame
pygame.init()
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption('Tablero Digital - Picogames')

# Inicializar cámara
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, RESOLUCION_CAMARA[0])
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, RESOLUCION_CAMARA[1])

# Configuración MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7)

# Estado del juego
tablero = [[None for _ in range(TABLERO_SIZE)] for _ in range(TABLERO_SIZE)]
turno = 1
game_over = False
ganador = None
gesto_reconocido = ""

def dibujar_tablero():
    ventana.fill(COLOR_FONDO)
    
    # Dibujar lÃ­neas del tablero
    for i in range(1, TABLERO_SIZE):
        pygame.draw.line(ventana, COLOR_LINEAS, 
                        (MARGEN + i * CELDA_SIZE, MARGEN),
                        (MARGEN + i * CELDA_SIZE, ALTO_VENTANA - MARGEN), 2)
        pygame.draw.line(ventana, COLOR_LINEAS,
                        (MARGEN, MARGEN + i * CELDA_SIZE),
                        (ANCHO_VENTANA - MARGEN, MARGEN + i * CELDA_SIZE), 2)
    
    # Dibujar las jugadas
    for fila in range(TABLERO_SIZE):
        for col in range(TABLERO_SIZE):
            centro_x = MARGEN + col * CELDA_SIZE + CELDA_SIZE // 2
            centro_y = MARGEN + fila * CELDA_SIZE + CELDA_SIZE // 2
            
            if tablero[fila][col] == 1:
                pygame.draw.circle(ventana, COLOR_JUGADOR1, (centro_x, centro_y), CELDA_SIZE // 3, 2)
            elif tablero[fila][col] == 2:
                pygame.draw.line(ventana, COLOR_JUGADOR2, 
                               (centro_x - CELDA_SIZE // 3, centro_y - CELDA_SIZE // 3),
                               (centro_x + CELDA_SIZE // 3, centro_y + CELDA_SIZE // 3), 2)
                pygame.draw.line(ventana, COLOR_JUGADOR2,
                               (centro_x + CELDA_SIZE // 3, centro_y - CELDA_SIZE // 3),
                               (centro_x - CELDA_SIZE // 3, centro_y + CELDA_SIZE // 3), 2)

def detectar_gesto(hand_landmarks):
    # Pulgar e índice
    pulgar = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    indice = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

    # Distancia entre pulgar e índice
    distancia = np.sqrt((pulgar.x - indice.x)**2 + (pulgar.y - indice.y)**2)

    # Se considera círculo si pulgar e índice están cerca
    if distancia < 0.05:
        return "circulo"

    # Verificar si todos los dedos están doblados (puño)
    dedos_doblados = 0
    dedos = [mp_hands.HandLandmark.INDEX_FINGER_TIP,
             mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
             mp_hands.HandLandmark.RING_FINGER_TIP,
             mp_hands.HandLandmark.PINKY_TIP]

    nudillos = [mp_hands.HandLandmark.INDEX_FINGER_PIP,
                mp_hands.HandLandmark.MIDDLE_FINGER_PIP,
                mp_hands.HandLandmark.RING_FINGER_PIP,
                mp_hands.HandLandmark.PINKY_PIP]

    for dedo, nudillo in zip(dedos, nudillos):
        if hand_landmarks.landmark[dedo].y > hand_landmarks.landmark[nudillo].y:
            dedos_doblados += 1

    if dedos_doblados == 4:
        return "cruz"

    return "ninguno"

def procesar_mano(frame, hand_landmarks):
    global turno, tablero, game_over, ganador, gesto_reconocido
    
    mp_drawing.draw_landmarks(
        frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
        mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
        mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2))
    
    gesto = detectar_gesto(hand_landmarks)
    gesto_reconocido = gesto
    
    # Dibujar nombre del gesto cerca del centro de la mano
    x_prom = int(np.mean([p.x for p in hand_landmarks.landmark]) * frame.shape[1])
    y_prom = int(np.mean([p.y for p in hand_landmarks.landmark]) * frame.shape[0])
    cv2.putText(frame, f"Gesto: {gesto}", (x_prom - 50, y_prom - 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    if (gesto == "circulo" and turno == 1) or (gesto == "cruz" and turno == 2):
        conteo_por_celda = [[0 for _ in range(TABLERO_SIZE)] for _ in range(TABLERO_SIZE)]

        for punto in hand_landmarks.landmark:
            x_px = int(punto.x * frame.shape[1])
            y_px = int(punto.y * frame.shape[0])

            col = int(x_px / (RESOLUCION_CAMARA[0] / TABLERO_SIZE))
            fila = int(y_px / (RESOLUCION_CAMARA[1] / TABLERO_SIZE))

            if 0 <= fila < TABLERO_SIZE and 0 <= col < TABLERO_SIZE:
                conteo_por_celda[fila][col] += 1

        # Buscar la celda con más puntos clave
        max_fila, max_col = 0, 0
        max_conteo = 0
        for f in range(TABLERO_SIZE):
            for c in range(TABLERO_SIZE):
                if conteo_por_celda[f][c] > max_conteo:
                    max_conteo = conteo_por_celda[f][c]
                    max_fila, max_col = f, c

        # Si la celda más densa está vacía, juega ahí
        if tablero[max_fila][max_col] is None:
            tablero[max_fila][max_col] = turno
            if verificar_ganador(max_fila, max_col):
                game_over = True
                ganador = turno
            elif es_empate():
                game_over = True
            turno = 2 if turno == 1 else 1

def verificar_ganador(fila, col):
    if all(tablero[fila][c] == turno for c in range(TABLERO_SIZE)):
        return True
    if all(tablero[f][col] == turno for f in range(TABLERO_SIZE)):
        return True
    if fila == col and all(tablero[i][i] == turno for i in range(TABLERO_SIZE)):
        return True
    if fila + col == TABLERO_SIZE - 1 and all(tablero[i][TABLERO_SIZE-1-i] == turno for i in range(TABLERO_SIZE)):
        return True
    return False

def es_empate():
    return all(tablero[f][c] is not None for f in range(TABLERO_SIZE) for c in range(TABLERO_SIZE))

def mostrar_mensaje(mensaje):
    font = pygame.font.Font(None, 28)
    texto = font.render(mensaje, True, (0, 0, 0))
    rect = texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2))
    ventana.blit(texto, rect)

# Bucle principal
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            cap.release()
            hands.close()
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_r:
                tablero = [[None for _ in range(TABLERO_SIZE)] for _ in range(TABLERO_SIZE)]
                turno = 1
                game_over = False
                ganador = None
    
    ret, frame = cap.read()
    if not ret:
        continue
    
    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    results = hands.process(frame_rgb)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            if not game_over:
                procesar_mano(frame, hand_landmarks)
    
    cv2.putText(frame, f"Turno: Jugador {turno} ({'circulo' if turno == 1 else 'cruz'})", 
               (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    cv2.putText(frame, f"Gesto detectado: {gesto_reconocido}", 
               (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
     # Dibujar líneas guía del tablero en la cámara
    celda_w = RESOLUCION_CAMARA[0] // TABLERO_SIZE
    celda_h = RESOLUCION_CAMARA[1] // TABLERO_SIZE

    # Líneas verticales
    for i in range(1, TABLERO_SIZE):
        x = i * celda_w
        cv2.line(frame, (x, 0), (x, RESOLUCION_CAMARA[1]), (255, 255, 255), 2)

    # Líneas horizontales
    for i in range(1, TABLERO_SIZE):
        y = i * celda_h
        cv2.line(frame, (0, y), (RESOLUCION_CAMARA[0], y), (255, 255, 255), 2)
    
    cv2.imshow('Deteccion de Gestos', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    dibujar_tablero()
    
    if game_over:
        if ganador:
            mostrar_mensaje(f"¡Jugador {ganador} gana! Presiona R para reiniciar")
        else:
            mostrar_mensaje("¡Empate! Presiona R para reiniciar")
    
    pygame.display.update()

cap.release()
hands.close()
cv2.destroyAllWindows()
pygame.quit()