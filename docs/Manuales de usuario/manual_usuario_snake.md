# Manual de Usuario - Snake con Seguimiento de Manos

## 1. Descripción General

Este juego es una versión moderna del clásico "Snake", desarrollada en Python. El jugador controla a la serpiente mediante gestos detectados por una cámara web, utilizando la biblioteca MediaPipe. Además del control sin contacto, el juego incorpora obstáculos, frutas especiales (normales, doradas y trampa), velocidad progresiva, modo difícil y sistema de puntajes altos.

## 2. Requisitos del Sistema

- Python 3.x
- Librerías instaladas:
  - `opencv-python`
  - `mediapipe`
  - `numpy`
  - (opcional para Windows) `winsound`
- Una cámara web funcional
- Imagen `food_icon.png` (icono de la fruta) en el mismo directorio del script

## 3. Ejecución del Juego

Ejecute el archivo principal en su terminal o entorno de desarrollo:

```bash
python snake_game.py
```

## 4. Instrucciones de Juego

### 4.1. Control por Gestos

- El juego rastrea el **dedo índice (landmark 8)** para dirigir la serpiente.
- El movimiento se basa en la posición relativa entre el dedo y la cabeza de la serpiente.
- La dirección no puede invertirse directamente para evitar colisiones autoinfligidas.

### 4.2. Tipos de Frutas

- **Normal:** Incrementa en 1 el puntaje y la longitud.
- **Dorada:** Vale 5 puntos y aparece por tiempo limitado.
- **Trampa:** Termina el juego al ser consumida.

### 4.3. Obstáculos

- Obstáculos dinámicos que cambian de posición cada cierto tiempo.
- Si la serpiente colisiona con uno, el juego finaliza.

### 4.4. Modos Especiales

- `M`: Alternar modo difícil (colisiones con paredes).
- `V`: Activar/desactivar velocidad progresiva (aumenta con cada 5 frutas).
- `R`: Reiniciar el juego.
- `ESC`: Salir del juego.

### 4.5. Sistema de Puntajes

- Se muestra el puntaje actual, los mejores tres puntajes, y el tiempo transcurrido.
- El archivo `highscores.txt` se actualiza automáticamente al terminar una partida.

## 5. Interfaz Gráfica

La interfaz incluye:

- Tablero central de 25x25 celdas con cuadrícula visible.
- Serpiente dibujada con cabeza redonda y cuerpo continuo.
- Obstáculos representados como círculos rojos.
- Frutas mostradas como:
  - Imagen `food_icon.png` para frutas normales.
  - Círculo dorado para frutas doradas.
  - Círculo rojo para trampas.
- Flecha amarilla indicando la dirección de movimiento.

## 6. Consejos de Uso

- Mantenga el dedo visible y centrado dentro del área de juego.
- Juegue en un entorno bien iluminado para mejor detección.
- Si usa Windows, el sistema incluye sonidos para eventos (comer fruta, trampa, etc.).

## 7. Archivos del Proyecto

- `snake_game.py`: Script principal del juego.
- `food_icon.png`: Imagen de la fruta normal (debe estar en el mismo directorio).
- `highscores.txt`: Archivo donde se almacenan los tres mejores puntajes.

## 8. Autoría

Este proyecto relaciona visión artificial y utiliza técnicas de seguimiento de mano y procesamiento de imagen para ofrecer una experiencia de juego sin contacto físico.

---
