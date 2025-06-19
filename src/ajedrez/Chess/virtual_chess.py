import pygame
import chess
import cv2 

class ChessApp:
    def __init__(self):
        pygame.init()
        self.size = 640
        self.square_size = self.size // 8
        self.screen = pygame.display.set_mode((self.size, self.size))
        pygame.display.set_caption("Tablero de Ajedrez Virtual")

        self.board = chess.Board()
        self.selected_square = None
        self.move_stack = []

        self.piece_images = self.load_piece_images()  # carga imágenes aquí

    def load_piece_images(self):
        images = {}
        for piece in "PNBRQK":
            path = f"assets/white/{piece}.png"
            try:
                img = pygame.image.load(path)
                img = pygame.transform.scale(img, (self.square_size, self.square_size))
                images[piece] = img
            except FileNotFoundError:
                print(f"Imagen blanca no encontrada: {path}")

        for piece in "PNBRQK":
            path = f"assets/black/{piece}.png"
            try:
                img = pygame.image.load(path)
                img = pygame.transform.scale(img, (self.square_size, self.square_size))
                images[piece.lower()] = img
            except FileNotFoundError:
                print(f"Imagen negra no encontrada: {path}")

        return images

    # Resto de métodos...
  

    def draw_board(self):
        colors = [pygame.Color("#C4C4B5"), pygame.Color("#0B1303")]
        for r in range(8):
            for c in range(8):
                color = colors[(r + c) % 2]
                rect = pygame.Rect(c * self.square_size, r * self.square_size, self.square_size, self.square_size)
                pygame.draw.rect(self.screen, color, rect)

                square = chess.square(c, 7 - r)
                piece = self.board.piece_at(square)
                if piece:
                    self.screen.blit(self.piece_images[piece.symbol()], rect)

    def run(self, gesture_controller):
        clock = pygame.time.Clock()
        running = True
        grabbing = False

        
        cap = cv2.VideoCapture(0)
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_z:
                        if self.move_stack:
                            self.board.pop()
                            self.move_stack.pop()

            ret, frame = cap.read()
            if not ret:
                continue
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            gesture, pos = gesture_controller.detect(frame_rgb)

            self.screen.fill(pygame.Color("gray"))
            self.draw_board()

            if gesture and pos:
                cursor_rect = pygame.Rect(pos[0], pos[1], 10, 10)
                pygame.draw.rect(self.screen, pygame.Color("red"), cursor_rect)

                if gesture == "closed":
                    if not grabbing:
                        grabbing = True
                        file = pos[0] // self.square_size
                        rank = 7 - (pos[1] // self.square_size)
                        self.selected_square = chess.square(file, rank)

                elif gesture == "open":
                    if grabbing and self.selected_square is not None:
                        grabbing = False
                        file = pos[0] // self.square_size
                        rank = 7 - (pos[1] // self.square_size)
                        to_square = chess.square(file, rank)
                        move = chess.Move(self.selected_square, to_square)
                        if move in self.board.legal_moves:
                            self.board.push(move)
                            self.move_stack.append(move)
                        self.selected_square = None

            pygame.display.flip()
            clock.tick(30)

        cap.release()
        cv2.destroyAllWindows()
        pygame.quit()

