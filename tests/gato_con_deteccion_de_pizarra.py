import cv2
import numpy as np
import pygame
import sys
from skimage.metrics import structural_similarity as ssim
import time

# Configuración inicial
RESOLUCION_CAMARA = (640, 480)
TABLERO_SIZE = 3
CELDA_SIZE = 100
MARGEN = 50
ANCHO_VENTANA = TABLERO_SIZE * CELDA_SIZE + 2 * MARGEN
ALTO_VENTANA = TABLERO_SIZE * CELDA_SIZE + 2 * MARGEN

COLOR_JUGADOR1 = (255, 0, 0)
COLOR_JUGADOR2 = (0, 0, 255)
COLOR_LINEAS = (0, 0, 0)
COLOR_FONDO = (255, 255, 255)

pygame.init()
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption('Detector de Figuras - Picogames')
fuente = pygame.font.SysFont(None, 24)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, RESOLUCION_CAMARA[0])
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, RESOLUCION_CAMARA[1])

tablero = [[None for _ in range(TABLERO_SIZE)] for _ in range(TABLERO_SIZE)]
turno = 1
game_over = False

# Variables para detección de fondo
fondo_inicial = None
fondo_actual = None
tiempo_actualizacion_fondo = 0

# Función para verificar similitud de fondo
def fondo_parecido(frame_gray):
    global fondo_inicial
    if fondo_inicial is None:
        return False
    score, _ = ssim(fondo_inicial, frame_gray, full=True)
    return score > 0.85

# Función para actualizar el fondo
def actualizar_fondo(frame_gray):
    global fondo_inicial, fondo_actual, tiempo_actualizacion_fondo
    fondo_inicial = frame_gray.copy()
    fondo_actual = frame_gray.copy()
    tiempo_actualizacion_fondo = time.time()

# Función para dibujar el tablero
def dibujar_tablero():
    ventana.fill(COLOR_FONDO)
    for i in range(1, TABLERO_SIZE):
        pygame.draw.line(ventana, COLOR_LINEAS,
                         (MARGEN + i * CELDA_SIZE, MARGEN),
                         (MARGEN + i * CELDA_SIZE, ALTO_VENTANA - MARGEN), 2)
        pygame.draw.line(ventana, COLOR_LINEAS,
                         (MARGEN, MARGEN + i * CELDA_SIZE),
                         (ANCHO_VENTANA - MARGEN, MARGEN + i * CELDA_SIZE), 2)
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

# Función para detectar formas (círculos y cruces)
def detectar_formas(frame_gray, frame_color):
    global turno
    circulos = cv2.HoughCircles(frame_gray, cv2.HOUGH_GRADIENT, 1, 30,
                                 param1=50, param2=30, minRadius=30, maxRadius=60)
    if circulos is not None:
        circulos = np.uint16(np.around(circulos))
        for c in circulos[0, :]:
            col = int(c[0] / (RESOLUCION_CAMARA[0] / TABLERO_SIZE))
            fila = int(c[1] / (RESOLUCION_CAMARA[1] / TABLERO_SIZE))
            if 0 <= fila < TABLERO_SIZE and 0 <= col < TABLERO_SIZE and tablero[fila][col] is None:
                tablero[fila][col] = 1
                turno = 2

    edges = cv2.Canny(frame_gray, 50, 150)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=80, minLineLength=80, maxLineGap=10)
    if lines is not None:
        line_map = np.zeros((TABLERO_SIZE, TABLERO_SIZE), dtype=int)
        for l in lines:
            x1, y1, x2, y2 = l[0]
            cx = (x1 + x2) // 2
            cy = (y1 + y2) // 2
            col = int(cx / (RESOLUCION_CAMARA[0] / TABLERO_SIZE))
            fila = int(cy / (RESOLUCION_CAMARA[1] / TABLERO_SIZE))
            if 0 <= fila < TABLERO_SIZE and 0 <= col < TABLERO_SIZE:
                line_map[fila][col] += 1

        for f in range(TABLERO_SIZE):
            for c in range(TABLERO_SIZE):
                if line_map[f][c] >= 2 and tablero[f][c] is None:
                    tablero[f][c] = 2
                    turno = 1

# Función para mostrar texto de ayuda
def mostrar_instrucciones():
    instrucciones = [
        "Presiona 'R' para reiniciar el tablero",
        "Presiona 'U' para actualizar el fondo",
        "Presiona 'Q' o cierra la ventana para salir"
    ]
    y = 10
    for texto in instrucciones:
        render = fuente.render(texto, True, (0, 0, 0))
        ventana.blit(render, (10, y))
        y += 25

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cap.release()
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                tablero = [[None for _ in range(TABLERO_SIZE)] for _ in range(TABLERO_SIZE)]
                turno = 1
            elif event.key == pygame.K_u:  # Tecla 'U' para actualizar el fondo
                if time.time() - tiempo_actualizacion_fondo > 2:
                    actualizar_fondo(blur)
            elif event.key == pygame.K_q:
                cap.release()
                pygame.quit()
                sys.exit()

    ret, frame = cap.read()
    if not ret:
        continue

    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray, 5)

    if fondo_inicial is None:
        actualizar_fondo(blur)

    if fondo_parecido(blur):
        if time.time() - tiempo_actualizacion_fondo > 2:
            tiempo_actualizacion_fondo = time.time()
    else:
        detectar_formas(blur, frame)

    dibujar_tablero()
    mostrar_instrucciones()
    pygame.display.update()
    cv2.imshow('Detección de Figuras', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
pygame.quit()
