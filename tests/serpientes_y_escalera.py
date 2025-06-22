import pygame
import random
import sys

pygame.init()

CELL_SIZE = 60
BOARD_SIZE = 10
WIDTH = HEIGHT = CELL_SIZE * BOARD_SIZE
FONT = pygame.font.SysFont('arial', 16)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
ORANGE = (255, 165, 0)

serpientes = {16: 6, 48: 30, 64: 60, 79: 19, 93: 68, 95: 24, 97: 76, 98: 78}
escaleras = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}

posiciones = {"Jugador 1": 0, "Jugador 2": 0}
jugadores = list(posiciones.keys())
turno_actual = 0

screen = pygame.display.set_mode((WIDTH, HEIGHT + 100))
pygame.display.set_caption("Serpientes y Escaleras")

def casilla_a_xy(casilla):
    casilla -= 1
    row = casilla // 10
    col = casilla % 10 if row % 2 == 0 else 9 - (casilla % 10)
    x = col * CELL_SIZE + CELL_SIZE // 2
    y = (9 - row) * CELL_SIZE + CELL_SIZE // 2
    return x, y

def dibujar_linea(start, end, color):
    x1, y1 = casilla_a_xy(start)
    x2, y2 = casilla_a_xy(end)
    pygame.draw.line(screen, color, (x1, y1), (x2, y2), 4)

def dibujar_tablero():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            pygame.draw.rect(screen, WHITE, (x, y, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)

            num = (9 - row) * 10 + col + 1 if (9 - row) % 2 == 0 else (9 - row) * 10 + (9 - col) + 1
            num_text = FONT.render(str(num), True, BLACK)
            screen.blit(num_text, (x + 5, y + 5))

    for start, end in serpientes.items():
        dibujar_linea(start, end, RED)
    for start, end in escaleras.items():
        dibujar_linea(start, end, GREEN)

def dibujar_jugadores():
    for i, jugador in enumerate(jugadores):
        pos = posiciones[jugador]
        if pos == 0:
            continue
        x, y = casilla_a_xy(pos)
        color = BLUE if i == 0 else ORANGE
        offset = -10 if i == 0 else 10
        pygame.draw.circle(screen, color, (x + offset, y), 10)

def mostrar_mensaje(mensaje):
    pygame.draw.rect(screen, WHITE, (0, HEIGHT, WIDTH, 100))
    lines = mensaje.split("\n")
    for i, line in enumerate(lines):
        text = FONT.render(line, True, BLACK)
        screen.blit(text, (10, HEIGHT + 10 + i * 20))

def tirar_dado():
    global turno_actual
    jugador = jugadores[turno_actual]
    dado = random.randint(1, 6)
    mensaje = f"{jugador} tiró el dado: {dado}"

    nueva_pos = posiciones[jugador] + dado
    if nueva_pos > 100:
        mensaje += "\n¡No puedes pasar la casilla 100!"
    else:
        mensaje += f"\nAvanzas a la casilla {nueva_pos}"
        if nueva_pos in serpientes:
            nueva_pos = serpientes[nueva_pos]
            mensaje += f"\n¡Oh no! Una serpiente te lleva a la casilla {nueva_pos}"
        elif nueva_pos in escaleras:
            nueva_pos = escaleras[nueva_pos]
            mensaje += f"\n¡Bien! Subes una escalera a la casilla {nueva_pos}"
        posiciones[jugador] = nueva_pos

    if posiciones[jugador] == 100:
        mensaje += f"\n🎉 ¡{jugador} ha ganado! 🎉"
        mostrar_mensaje(mensaje)
        return "FIN"

    turno_actual = (turno_actual + 1) % 2
    mostrar_mensaje(mensaje + f"\nTurno: {jugadores[turno_actual]}")
    return "CONTINUAR"

# Bucle principal
running = True
mensaje_actual = f"Turno: {jugadores[turno_actual]}"
estado_juego = "CONTINUAR"

while running:
    screen.fill((200, 200, 255))
    dibujar_tablero()
    dibujar_jugadores()
    mostrar_mensaje(mensaje_actual)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and estado_juego == "CONTINUAR":
            if event.key == pygame.K_SPACE:
                estado_juego = tirar_dado()
                mensaje_actual = ""

pygame.quit()
sys.exit()

