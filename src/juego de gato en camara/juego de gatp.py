# Importar bibliotecas
import cv2
import pygame
import numpy as np
import sys

# Configuración de la cámara
RESOLUCION_CAMARA = (640, 480)
TABLERO_SIZE = 3
CELDA_SIZE = 100
MARGEN = 50
ANCHO_VENTANA = TABLERO_SIZE * CELDA_SIZE + 2 * MARGEN
ALTO_VENTANA = TABLERO_SIZE * CELDA_SIZE + 2 * MARGEN

# Colores (RGB)
COLOR_JUGADOR1 = (255, 0, 0)   # Jugador 1 - círculo
COLOR_JUGADOR2 = (0, 0, 255)   # Jugador 2 - cruz
COLOR_LINEAS = (0, 0, 0)
COLOR_FONDO = (255, 255, 255)

# Inicializar PyGame
pygame.init()
ventana = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
pygame.display.set_caption('Tablero Digital - Picogames')

# Inicializar cámara
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, RESOLUCION_CAMARA[0])
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, RESOLUCION_CAMARA[1])

# Estado del juego
tablero = [[None for _ in range(TABLERO_SIZE)] for _ in range(TABLERO_SIZE)]
turno = 1
game_over = False
ganador = None

# --- Funciones ---

def dibujo_detectado(frame):
    gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gris, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)

    # Detección de líneas diagonales (cruz)
    lineas = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=50, maxLineGap=10)
    diagonales = []

    if lineas is not None:
        for linea in lineas:
            x1, y1, x2, y2 = linea[0]
            dx = x2 - x1
            dy = y2 - y1

            if dx == 0:
                continue
            angulo = abs(np.degrees(np.arctan2(dy, dx)))
            if 30 < angulo < 60 or 120 < angulo < 150:
                diagonales.append(((x1, y1), (x2, y2)))
                cv2.line(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)

    if len(diagonales) >= 2:
        (x1, y1), (x2, y2) = diagonales[0]
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        return ("cruz", (cx, cy))

    # Detección de círculos
    _, thresh = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY_INV)
    contornos, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contornos:
        area = cv2.contourArea(cnt)
        if area < 300:
            continue

        perimetro = cv2.arcLength(cnt, True)
        if perimetro == 0:
            continue

        circularidad = 4 * np.pi * (area / (perimetro ** 2))
        if circularidad > 0.7:
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                cv2.circle(frame, (cx, cy), 20, (255, 255, 255), 2)
                return ("circulo", (cx, cy))

    return None

def verificar_ganador(fila, col, jugador):
    if all(tablero[fila][c] == jugador for c in range(TABLERO_SIZE)):
        return True
    if all(tablero[f][col] == jugador for f in range(TABLERO_SIZE)):
        return True
    if fila == col and all(tablero[i][i] == jugador for i in range(TABLERO_SIZE)):
        return True
    if fila + col == TABLERO_SIZE - 1 and all(tablero[i][TABLERO_SIZE - 1 - i] == jugador for i in range(TABLERO_SIZE)):
        return True
    return False

def es_empate():
    return all(tablero[f][c] is not None for f in range(TABLERO_SIZE) for c in range(TABLERO_SIZE))

def mostrar_mensaje(ventana, mensaje):
    font = pygame.font.Font(None, 28)
    texto = font.render(mensaje, True, (0, 0, 0))
    rect = texto.get_rect(center=(ANCHO_VENTANA // 2, ALTO_VENTANA // 2))
    ventana.blit(texto, rect)

def dibujar_tablero():
    ventana.fill(COLOR_FONDO)
    for i in range(1, TABLERO_SIZE):
        pygame.draw.line(ventana, COLOR_LINEAS, (MARGEN + i * CELDA_SIZE, MARGEN), (MARGEN + i * CELDA_SIZE, ALTO_VENTANA - MARGEN), 2)
        pygame.draw.line(ventana, COLOR_LINEAS, (MARGEN, MARGEN + i * CELDA_SIZE), (ANCHO_VENTANA - MARGEN, MARGEN + i * CELDA_SIZE), 2)

    for fila in range(TABLERO_SIZE):
        for col in range(TABLERO_SIZE):
            cx = MARGEN + col * CELDA_SIZE + CELDA_SIZE // 2
            cy = MARGEN + fila * CELDA_SIZE + CELDA_SIZE // 2
            if tablero[fila][col] == 1:
                pygame.draw.circle(ventana, COLOR_JUGADOR1, (cx, cy), CELDA_SIZE // 3, 2)
            elif tablero[fila][col] == 2:
                pygame.draw.line(ventana, COLOR_JUGADOR2, (cx - CELDA_SIZE // 3, cy - CELDA_SIZE // 3),
                                 (cx + CELDA_SIZE // 3, cy + CELDA_SIZE // 3), 2)
                pygame.draw.line(ventana, COLOR_JUGADOR2, (cx + CELDA_SIZE // 3, cy - CELDA_SIZE // 3),
                                 (cx - CELDA_SIZE // 3, cy + CELDA_SIZE // 3), 2)

# --- Bucle principal ---

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
                game_over = False
                ganador = None

    ret, frame = cap.read()
    if not ret:
        continue

    frame = cv2.flip(frame, 1)
    resultado = dibujo_detectado(frame)

    if not game_over and resultado:
        gesto, (x, y) = resultado
        jugador = 1 if gesto == "circulo" else 2
        if jugador == turno:
            fila = y * 3 // RESOLUCION_CAMARA[1]
            col = x * 3 // RESOLUCION_CAMARA[0]
            if tablero[fila][col] is None:
                tablero[fila][col] = jugador
                if verificar_ganador(fila, col, jugador):
                    game_over = True
                    ganador = jugador
                elif es_empate():
                    game_over = True
                else:
                    turno = 2 if turno == 1 else 1

    # Dibujar líneas guía en la cámara
    celda_w = RESOLUCION_CAMARA[0] // TABLERO_SIZE
    celda_h = RESOLUCION_CAMARA[1] // TABLERO_SIZE
    for i in range(1, TABLERO_SIZE):
        cv2.line(frame, (i * celda_w, 0), (i * celda_w, RESOLUCION_CAMARA[1]), (255, 255, 255), 2)
        cv2.line(frame, (0, i * celda_h), (RESOLUCION_CAMARA[0], i * celda_h), (255, 255, 255), 2)

    # Texto del turno
    cv2.putText(frame, f"Turno: Jugador {turno} ({'circulo' if turno == 1 else 'cruz'})", 
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    cv2.imshow("Camara", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    # Dibujar en Pygame
    dibujar_tablero()
    if game_over:
        if ganador:
            mostrar_mensaje(ventana, f"¡Jugador {ganador} gana! Presiona R para reiniciar")
        else:
            mostrar_mensaje(ventana, "¡Empate! Presiona R para reiniciar")

    pygame.display.update()

cap.release()
cv2.destroyAllWindows()
pygame.quit()