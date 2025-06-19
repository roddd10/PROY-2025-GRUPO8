"""Helper functions used in the move detection logic."""
import cv2
import numpy as np

from math import sqrt



def perspective_transform(image, pts1, size=480):
    """Aplica transformación de perspectiva para alinear el tablero."""
    pts2 = np.float32([[0, 0], [0, size], [size, 0], [size, size]])
    M = cv2.getPerspectiveTransform(pts1, pts2)
    dst = cv2.warpPerspective(image, M, (size, size))
    return dst


def rotate_matrix(matrix):
    """Rota una matriz 90 grados en sentido horario."""
    size = len(matrix)
    for row in range(size // 2):
        for column in range(row, size - row - 1):
            temp = matrix[row][column]
            matrix[row][column] = matrix[column][size - 1 - row]
            matrix[column][size - 1 - row] = matrix[size - 1 - row][size - 1 - column]
            matrix[size - 1 - row][size - 1 - column] = matrix[size - 1 - column][row]
            matrix[size - 1 - column][row] = temp


def auto_canny(image):
    """Aplica Canny con umbrales automáticos."""
    sigma_upper = 0.2
    sigma_lower = 0.8
    median = np.median(image)
    lower = int(max(0, (1.0 - sigma_lower) * median))
    upper = int(min(255, (1.0 + sigma_upper) * median))
    return cv2.Canny(image, lower, upper)


def edge_detection(frame):
    """Detecta bordes combinando los 3 canales con técnicas de mejora."""
    kernel = np.ones((3, 3), np.uint8)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    edges = []

    for gray in cv2.split(frame):
        gray = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
        gray = clahe.apply(gray)
        gray = cv2.GaussianBlur(gray, (3, 3), 0)
        edge = auto_canny(gray)
        edges.append(edge)

    combined = cv2.bitwise_or(cv2.bitwise_or(edges[0], edges[1]), edges[2])
    return cv2.morphologyEx(combined, cv2.MORPH_CLOSE, kernel)


def get_square_image(row, col, board_img):
    """Extrae una casilla individual del tablero."""
    h, w = board_img.shape[:2]
    minX = int(col * w / 8)
    maxX = int((col + 1) * w / 8)
    minY = int(row * h / 8)
    maxY = int((row + 1) * h / 8)
    square = board_img[minY:maxY, minX:maxX]
    return square[3:-3, 3:-3]  # Evita bordes


def contains_piece(square, view):
    """Determina si una casilla contiene una pieza, según la orientación."""
    h, w = square.shape[:2]
    if view == (0, -1):
        half = square[:, w // 2 :]
    elif view == (0, 1):
        half = square[:, : w // 2]
    elif view == (1, 0):
        half = square[h // 2 :, :]
    elif view == (-1, 0):
        half = square[: h // 2, :]
    else:
        half = square

    # Heurística simple basada en brillo promedio
    if half.mean() < 1.0:
        return [False]
    elif square.mean() > 15.0:
        return [True]
    elif square.mean() > 6.0:
        return [True, False]
    return [False]


def detect_state(frame, view, roi_mask):
    """Detecta el estado binario del tablero (ocupado / vacío) usando la máscara ROI."""
    edges = edge_detection(frame)
    edges = cv2.bitwise_and(edges, roi_mask)

    board_image = [
        [get_square_image(row, col, edges) for col in range(8)] for row in range(8)
    ]
    state = [
        [contains_piece(board_image[row][col], view) for col in range(8)]
        for row in range(8)
    ]
    return state


def mark_corners(frame, corners, rotation_count=0):
    """Dibuja marcas en las esquinas detectadas del tablero."""
    h, w = frame.shape[:2]
    rot_frame = {
        0: frame,
        1: cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE),
        2: cv2.rotate(frame, cv2.ROTATE_180),
        3: cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE),
    }[rotation_count]

    for i, row in enumerate(corners):
        for j, pt in enumerate(row):
            if rotation_count == 1:
                index = f"{j},{8 - i}"
                pt = (h - pt[1], pt[0])
            elif rotation_count == 2:
                index = f"{8 - i},{8 - j}"
                pt = (w - pt[0], h - pt[1])
            elif rotation_count == 3:
                index = f"{8 - j},{i}"
                pt = (pt[1], w - pt[0])
            else:
                index = f"{i},{j}"

            pt = (int(pt[0]), int(pt[1]))
            cv2.putText(rot_frame, index, pt, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

    return rot_frame


def euclidean_distance(p1, p2):
    """Distancia euclidiana entre dos puntos."""
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

import chess.pgn
def save_pgn(game, filename="output.pgn"):
    """
    Guarda una partida de ajedrez en formato PGN.

    :param game: Objeto chess.pgn.Game con el historial de movimientos.
    :param filename: Nombre del archivo de salida.
    """
    with open(filename, "w", encoding="utf-8") as f:
        f.write(str(game))

