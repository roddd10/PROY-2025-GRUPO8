import cv2
from virtual_chess import ChessApp
from gesture_controller import GestureController

import os
print("Working directory:", os.getcwd())

def detect_chessboard(cam_id=0):
    cap = cv2.VideoCapture(cam_id)
    if not cap.isOpened():
        print("No se pudo acceder a la cámara.")
        return False

    print("Buscando patrón de tablero de ajedrez...")
    found = False
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error al capturar imagen.")
            break
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        found, corners = cv2.findChessboardCorners(gray, (7, 7), None)

        display = frame.copy()
        if found:
            cv2.drawChessboardCorners(display, (7, 7), corners, found)
            cv2.putText(display, "Tablero detectado. Presiona ENTER para continuar", (30, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            cv2.putText(display, "Apunta la camara a un tablero de ajedrez", (30, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.imshow("Detección de tablero", display)
        key = cv2.waitKey(1)
        if key == 13 and found:  # ENTER
            break
        elif key == 27:  # ESC
            print("Cancelado por el usuario.")
            cap.release()
            cv2.destroyAllWindows()
            return False

    cap.release()
    cv2.destroyAllWindows()
    return True


if __name__ == "__main__":
    if detect_chessboard():
        print("Tablero detectado. Iniciando juego virtual...")
        controller = GestureController()
        app = ChessApp()
        app.run(controller)
    else:
        print("No se detectó tablero. El juego no se iniciará.")
