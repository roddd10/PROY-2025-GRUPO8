import random
import numpy as np
import cv2 as cv
import mediapipe as mp
import time
import platform

# Para sonido simple en Windows
if platform.system() == "Windows":
    import winsound

font = cv.FONT_HERSHEY_DUPLEX

class SnakeGameClass:
    def __init__(self):
        self.backSize = (1280, 1280)
        self.gameSize = (500, 500)
        self.numTile = 25
        self.margin = 5
        self.high_score = 0
        self.lastFinger = [None, None]
        self.points = [(self.numTile // 2, self.numTile // 2)]
        self.length = 1
        self.score = 0
        self.gameOver = False
        self.gameStart = False
        self.previousTime = time.time()
        self.currentTime = time.time()
        self.snakeSpeed = 0.30  # Velocidad inicial más lenta para facilitar
        self.startTime = time.time()
        self.direction = 'r'
        self.high_scores = self.loadHighScores()

        self.foodIcon = cv.imread("assets_food/food_icon.png", cv.IMREAD_UNCHANGED)
        self.foodIcon = cv.resize(self.foodIcon, (20, 20)) 
        self.foodMask = self.foodIcon[:, :, 3]

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils
        self.cap = cv.VideoCapture(0)
        self.cap.set(3, 1280)
        self.cap.set(4, 720)
        self.imgMain = None

        self.hard_mode = False
        self.progressive_speed = False
        self.fruit_count = 0
        self.min_snake_speed = 0.05

        self.obstacles = []
        self.obstacle_speed = 0.5
        self.last_obstacle_move = time.time()
        self.initObstacles()

        self.foodPoint = self.randomFood()
        self.golden_start_time = None

    def loadHighScores(self):
        try:
            with open("highscores.txt", "r") as f:
                return sorted([int(line.strip()) for line in f], reverse=True)[:3]
        except FileNotFoundError:
            return [0, 0, 0]

    def saveHighScores(self):
        all_scores = self.high_scores + [self.score]
        top3 = sorted(all_scores, reverse=True)[:3]
        with open("highscores.txt", "w") as f:
            for score in top3:
                f.write(str(score) + "\n")
        self.high_scores = top3

    def start(self):
        x, y, w, h = 391, 10, 500, 541
        self.startTime = time.time()
        while True:
            success, img = self.cap.read()
            img = cv.flip(img, 1)
            cropped_img = img[y:y+h, x:x+w]
            imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
            results = self.hands.process(imgRGB)

            if results.multi_hand_landmarks:
                for handLMs in results.multi_hand_landmarks:
                    x_finger = int(handLMs.landmark[8].x * img.shape[1])
                    y_finger = int(handLMs.landmark[8].y * img.shape[0])
                    self.lastFinger = [x_finger, y_finger]
                    self.updateDirection()
                    self.gameStart = True

            if self.isTimeToMoveSnake():

                self.update()

            # Manejar fruta dorada
            if self.foodPoint and self.foodPoint['type'] == 'golden':
                if self.golden_start_time is None:
                    self.golden_start_time = time.time()
                elif time.time() - self.golden_start_time > 7:
                    self.foodPoint = self.randomFood()
                    self.golden_start_time = None
            else:
                self.golden_start_time = None

            # Mover obstáculos
            current_time = time.time()
            if current_time - self.last_obstacle_move > self.obstacle_speed:
                self.moveObstacles()
                self.last_obstacle_move = current_time

            self.imgMain = self.displayGUI(img)
            cv.imshow("Snake Game", cropped_img)

            key = cv.waitKey(1)
            if key == ord('r'):
                self.resetGame()
                print('reset')

            elif key == ord('m'):
                self.hard_mode = not self.hard_mode
                print("Modo difícil:", self.hard_mode)

            elif key == ord('v'):
                self.progressive_speed = not self.progressive_speed
                print("Velocidad progresiva:", self.progressive_speed)

            elif key == 27:
                self.saveHighScores()
                cv.destroyAllWindows()
                self.cap.release()
                print('break')
                break

    # Devuelve lista 0/1 si dedo está arriba (pulgar, índice, medio, anular, meñique)
    def getFingersUp(self, handLMs):
        tips = [4, 8, 12, 16, 20]
        fingers = []
        for tip in tips:
            tip_y = handLMs.landmark[tip].y
            pip_y = handLMs.landmark[tip-2].y
            fingers.append(1 if tip_y < pip_y else 0)
        return fingers

    def update(self):
        if self.gameOver or not self.gameStart:
            return

        hx, hy = self.points[-1]

        def check_collision(new_point):
            return (new_point in self.points[:-2]) if self.length >= 3 else False

        if self.direction == 'l':
            new_point = (hx - 1, hy)
        elif self.direction == 'r':
            new_point = (hx + 1, hy)
        elif self.direction == 'u':
            new_point = (hx, hy - 1)
        else:
            new_point = (hx, hy + 1)

        if self.hard_mode and not (0 <= new_point[0] < self.numTile and 0 <= new_point[1] < self.numTile):
            self.gameOver = True
            return

        if check_collision(new_point):
            self.gameOver = True
            return

        if new_point in self.obstacles:
            self.gameOver = True
            return

        if self.foodPoint and new_point == self.foodPoint['pos']:
            self.whenAteFood()
            return

        self.points.append(new_point)
        del self.points[0]

    def whenAteFood(self):
        if not self.foodPoint:
            return

        pos = self.foodPoint['pos']
        ftype = self.foodPoint['type']

        self.points.append(pos)
        self.length += 1

        if ftype == 'normal':
            self.score += 1
            self.fruit_count += 1
            self.playSound('eat')
        elif ftype == 'golden':
            self.score += 5
            self.fruit_count += 5
            self.playSound('golden')
        elif ftype == 'trap':
            self.gameOver = True
            self.playSound('trap')
            return

        self.foodPoint = self.randomFood()
        self.golden_start_time = None

        if self.progressive_speed and self.fruit_count % 5 == 0:
            self.snakeSpeed = max(self.snakeSpeed - 0.02, self.min_snake_speed)
            print(f"Velocidad aumentada! Nuevo intervalo: {self.snakeSpeed:.3f}s")

    def playSound(self, sound_type):
        if platform.system() == "Windows":
            if sound_type == 'eat':
                winsound.Beep(600, 100)
            elif sound_type == 'golden':
                winsound.Beep(1000, 200)
            elif sound_type == 'trap':
                winsound.Beep(400, 400)
        else:
            # No soportado o agregar librería cross-platform
            pass

    def randomFood(self):
        foodSpace = [(i, j) for i in range(self.numTile) for j in range(self.numTile)]
        for item in self.points:
            if item in foodSpace:
                foodSpace.remove(item)
        for obs in self.obstacles:
            if obs in foodSpace:
                foodSpace.remove(obs)

        if not foodSpace:
            return None

        pos = random.choice(foodSpace)
        p = random.random()
        if p < 0.1:
            ftype = 'trap'
        elif p < 0.25:
            ftype = 'golden'
        else:
            ftype = 'normal'

        return {'pos': pos, 'type': ftype}

    def updateDirection(self):
        if self.lastFinger == [None, None]:
            return

        x_finger, y_finger = self.lastFinger
        x_head, y_head = self.indexToPixel(self.points[-1])

        dx = x_finger - x_head
        dy = y_finger - y_head

        threshold = 20  # zona muerta para evitar cambios pequeños
        if abs(dx) < threshold and abs(dy) < threshold:
            return

        if abs(dx) >= abs(dy):
            new_direction = 'r' if dx >= 0 else 'l'
        else:
            new_direction = 'd' if dy >= 0 else 'u'

        opposites = {'r': 'l', 'l': 'r', 'u': 'd', 'd': 'u'}
        if new_direction != opposites.get(self.direction, ''):
            self.direction = new_direction

    def initObstacles(self):
        self.obstacles = []
        for _ in range(5):
            possible_positions = [(i, j) for i in range(self.numTile) for j in range(self.numTile)]
            for p in self.points:
                if p in possible_positions:
                    possible_positions.remove(p)
            pos = random.choice(possible_positions)
            self.obstacles.append(pos)

    def moveObstacles(self):
        new_positions = []
        for (x, y) in self.obstacles:
            moves = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
            valid_moves = [m for m in moves if 0 <= m[0] < self.numTile and 0 <= m[1] < self.numTile and m not in self.points and m not in self.obstacles]
            if valid_moves:
                new_pos = random.choice(valid_moves)
            else:
                new_pos = (x, y)
            new_positions.append(new_pos)
        self.obstacles = new_positions

    def indexToPixel(self, index):
        i, j = index
        n = self.gameSize[0] // self.numTile
        x_new = 390 + n * i + 1
        y_new = 5 + n * j + 1
        return x_new, y_new

    def isTimeToMoveSnake(self):
        self.currentTime = time.time()
        if self.currentTime > self.previousTime + self.snakeSpeed:
            self.previousTime += self.snakeSpeed
            return True
        return False

    def resetGame(self):
        self.saveHighScores()
        self.lastFinger = [None, None]
        self.points = [(self.numTile // 2, self.numTile // 2)]
        self.length = 1
        self.score = 0
        self.fruit_count = 0
        self.gameOver = False
        self.gameStart = False
        self.direction = 'r'
        self.snakeSpeed = 0.30
        self.startTime = time.time()
        self.foodPoint = self.randomFood()
        self.golden_start_time = None
        self.initObstacles()

    def displayGUI(self, imgMain):
        if self.gameOver:
            cv.putText(imgMain, "You Lose Press R for Restart", (400, 200), font, 1, (0, 0, 255), 2, cv.LINE_AA)
            cv.putText(imgMain, "Best Score : " + str(self.high_score), (520, 280), font, 1, (200, 0, 0), 2, cv.LINE_AA)
        else:
            if self.foodPoint:
                x_food, y_food = self.indexToPixel(self.foodPoint['pos'])
                if self.foodPoint['type'] == 'normal':
                    imgMain[y_food:y_food + 20, x_food:x_food + 20] = self.foodIcon[:, :, :3] * (self.foodMask[:, :, None] / 255.0) + imgMain[y_food:y_food + 20, x_food:x_food + 20] * (1.0 - self.foodMask[:, :, None] / 255.0)
                elif self.foodPoint['type'] == 'golden':
                    cv.circle(imgMain, (x_food+10, y_food+10), 10, (0, 215, 255), thickness=-1)
                elif self.foodPoint['type'] == 'trap':
                    cv.circle(imgMain, (x_food+10, y_food+10), 10, (0, 0, 255), thickness=-1)

            imgMain = self.drawSnake(imgMain, self.points, (0, 255, 0))

            # Dibuja obstáculos
            n = self.gameSize[0] // self.numTile
            thickness = n // 2
            for (x, y) in self.obstacles:
                center = (int(390 + n * (x + 0.5)), int(5 + n * (y + 0.5)))
                cv.circle(imgMain, center, thickness, (0, 0, 255), thickness=-1)

            # Dibuja flecha dirección
            self.drawDirectionArrow(imgMain)

        # Texto HUD
        cv.putText(imgMain, f"Score : {self.score}", (560, 540), font, 1, (0, 255, 0), 2, cv.LINE_AA)

        elapsedTime = int(time.time() - self.startTime)
        minutes = elapsedTime // 60
        seconds = elapsedTime % 60
        cv.putText(imgMain, f"Time: {minutes:02}:{seconds:02}", (20, 540), font, 1, (255, 255, 0), 2, cv.LINE_AA)

        for i, hs in enumerate(self.high_scores):
            cv.putText(imgMain, f"Top {i+1}: {hs}", (20, 50 + i * 40), font, 1, (0, 200, 255), 2, cv.LINE_AA)

        # Instrucciones pantalla
        info_lines = [
            "Controles:",
            "- M: Cambiar modo facil/dificil",
            "- V: Cambiar velocidad progresiva",
            "- R: Reiniciar",
        ]
        for i, line in enumerate(info_lines):
            cv.putText(imgMain, line, (20, 480 + i*20), font, 0.6, (255, 255, 255), 1, cv.LINE_AA)

        imgMain = cv.rectangle(imgMain,
            (self.backSize[0] // 2 - self.gameSize[0] // 2, 2 * self.margin),
            (self.backSize[0] // 2 + self.gameSize[0] // 2, 2 * self.margin + self.gameSize[1]),
            (0, 255, 0), 2)

        n = self.gameSize[0] // self.numTile
        for i in range(self.numTile + 1):
            x = 390 + i * n
            y_start = 5
            y_end = 5 + self.gameSize[1]
            cv.line(imgMain, (x, y_start), (x, y_end), (50, 50, 50), 1)

            y = 5 + i * n
            x_start = 390
            x_end = 390 + self.gameSize[0]
            cv.line(imgMain, (x_start, y), (x_end, y), (50, 50, 50), 1)

        return imgMain

    def drawDirectionArrow(self, imgMain):
        n = self.gameSize[0] // self.numTile
        head_pos = self.points[-1]
        center = (int(390 + n * (head_pos[0] + 0.5)), int(5 + n * (head_pos[1] + 0.5)))
        length = n // 2

        if self.direction == 'r':
            tip = (center[0] + length, center[1])
        elif self.direction == 'l':
            tip = (center[0] - length, center[1])
        elif self.direction == 'u':
            tip = (center[0], center[1] - length)
        else:
            tip = (center[0], center[1] + length)

        cv.arrowedLine(imgMain, center, tip, (255, 255, 0), 3, tipLength=0.4)

    def drawSnake(self, imgMain, points, color):
        if self.high_score <= self.score:
            self.high_score = self.score
        n = self.gameSize[0] // self.numTile
        thickness = n // 2
        head_pt = (int(390 + n * (points[-1][0] + 0.5)), int(5 + n * (points[-1][1] + 0.5)))
        cv.circle(imgMain, head_pt, thickness, color, thickness=-1)

        for i in range(len(points) - 1):
            pt1 = (int(390 + n * (points[i][0] + 0.5)), int(5 + n * (points[i][1] + 0.5)))
            pt2 = (int(390 + n * (points[i + 1][0] + 0.5)), int(5 + n * (points[i + 1][1] + 0.5)))
            cv.line(imgMain, pt1, pt2, color, thickness=thickness)

        return imgMain

game = SnakeGameClass()
game.start()
