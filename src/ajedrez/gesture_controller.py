import cv2
import mediapipe as mp
import numpy as np


class GestureController:
    def __init__(self):
        self.hands = mp.solutions.hands.Hands(static_image_mode=False,
                                              max_num_hands=1,
                                              min_detection_confidence=0.7,
                                              min_tracking_confidence=0.4)

    def detect(self, frame,screen_size=(700, 700)):
        frame =   cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb)


        if result.multi_hand_landmarks:
            hand = result.multi_hand_landmarks[0]
            landmarks = [(lm.x, lm.y) for lm in hand.landmark]

            h, w, _ = frame.shape
            coords = [(int(lm.x * w), int(lm.y * h)) for lm in hand.landmark]

            # Centro aproximado de la palma (landmark 0)
            cx, cy = coords[9]
            screen_w, screen_h = screen_size
            scaled_x = int(cx * screen_w / w)
            scaled_y = int(cy * screen_h / h)
            # Distancia entre pulgar (4) y dedo índice (8)
            d = np.linalg.norm(np.array(coords[4]) - np.array(coords[8]))

            gesture = "closed" if d < 40 else "open"

            return gesture, (scaled_x, scaled_y)

        return None, None
