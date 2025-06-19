import cv2
import mediapipe as mp
import numpy as np


class GestureController:
    def __init__(self):
        self.hands = mp.solutions.hands.Hands(static_image_mode=False,
                                              max_num_hands=1,
                                              min_detection_confidence=0.5,
                                              min_tracking_confidence=0.5)

    def detect(self, frame):
        frame =   cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb)


        if result.multi_hand_landmarks:
            hand = result.multi_hand_landmarks[0]
            landmarks = [(lm.x, lm.y) for lm in hand.landmark]

            h, w, _ = frame.shape
            coords = [(int(x * w), int(y * h)) for x, y in landmarks]

            # Centro aproximado de la palma (landmark 0)
            cx, cy = coords[0]

            # Distancia entre pulgar (4) y dedo índice (8)
            d = np.linalg.norm(np.array(coords[4]) - np.array(coords[8]))

            gesture = "closed" if d < 40 else "open"

            return gesture, (cx, cy)

        return None, None
