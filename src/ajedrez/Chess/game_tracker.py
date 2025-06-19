import cv2
import numpy as np
import chess.pgn  # Asegúrate de tener `python-chess` instalado
import io

class GameTracker:
    def __init__(self, camera_index=0, initial_pgn=None):
        self.cap = cv2.VideoCapture(camera_index)
        if not self.cap.isOpened():
            raise Exception("No se pudo abrir la cámara")
        
        self.base_frame = None  # Imagen base del tablero
        self.moves = []

        # Inicializa el tablero desde PGN o desde una posición inicial
        self.board = self._init_board_from_pgn(initial_pgn)

    def _init_board_from_pgn(self, pgn_text):
        if not pgn_text:
            print("♟️ Cargando tablero vacío (posición inicial)")
            return chess.Board()
        
        try:
            game = chess.pgn.read_game(io.StringIO(pgn_text))
            board = game.board()
            for move in game.mainline_moves():
                board.push(move)
            print("♟️ Tablero cargado desde PGN.")
            return board
        except Exception as e:
            print(f"⚠️ Error al cargar PGN: {e}")
            return chess.Board()

    def capture_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            raise Exception("Error al capturar el frame de la cámara")
        return frame

    def set_base_frame(self):
        self.base_frame = self.capture_frame()
        print("✅ Imagen base del tablero guardada.")

    def detect_moves(self, current_frame, threshold=30):
        if self.base_frame is None:
            print("⚠️ Base frame no configurado.")
            return None

        # Convertir a escala de grises
        base_gray = cv2.cvtColor(self.base_frame, cv2.COLOR_BGR2GRAY)
        curr_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)

        # Diferencia absoluta
        diff = cv2.absdiff(base_gray, curr_gray)

        # Umbral binario
        _, diff_thresh = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)

        # Contornos
        contours, _ = cv2.findContours(diff_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        moves_detected = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 500:  # Umbral ajustable
                x, y, w, h = cv2.boundingRect(cnt)
                moves_detected.append((x, y, w, h))

        if moves_detected:
            print(f"📦 Detectados {len(moves_detected)} cambios.")
        else:
            print("🟢 No se detectaron cambios.")

        return moves_detected

    def update_board_state(self, moves):
        # Placeholder: aquí deberías integrar lógica para convertir los movimientos detectados en jugadas legales
        # Por ejemplo, usar visión por computadora para identificar origen y destino
        print("⚙️ Actualizando el estado del tablero (no implementado).")

    def release(self):
        self.cap.release()
