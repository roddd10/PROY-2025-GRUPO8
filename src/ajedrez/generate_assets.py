import pygame
import chess

class ChessApp:
    def __init__(self):
        self.size = 640
        self.square_size = self.size // 8
        self.screen = pygame.display.set_mode((self.size, self.size))
        pygame.display.set_caption("Tablero de Ajedrez Virtual")

        self.board = chess.Board()
        self.selected_square = None
        self.move_stack = []

        self.piece_images = self.load_piece_images()

    def load_piece_images(self):
        images = {}  
        pieces = ["P", "R", "N", "B", "Q", "K"]

        for piece in pieces:
            # Cargar piezas blancas
            white_path = f"assets/white/{piece}.png"
            try:
                img_white = pygame.image.load(white_path)
                images[piece] = pygame.transform.scale(img_white, (self.square_size, self.square_size))
            except FileNotFoundError:
                print(f"Imagen blanca no encontrada: {white_path}")

            # Cargar piezas negras (clave en minúscula)
            black_path = f"assets/black/{piece}.png"
            try:
                img_black = pygame.image.load(black_path)
                images[piece.lower()] = pygame.transform.scale(img_black, (self.square_size, self.square_size))
            except FileNotFoundError:
                print(f"Imagen negra no encontrada: {black_path}")

        return images  
