# Manual de Usuario - Pong con Control por Gestos

## 1. Descripción General

Este juego es una versión del clásico "Pong" implementada en Python. A diferencia del original, este juego permite controlar las paletas usando gestos de las manos detectados por una cámara web, utilizando la biblioteca MediaPipe de Google. El sistema reconoce la posición y orientación de las manos para mover las paletas de los jugadores en tiempo real.

## 2. Requisitos del Sistema

- Python 3.x
- Librerías instaladas:
  - `opencv-python`
  - `mediapipe`
  - `numpy`
- Una cámara web funcional

## 3. Ejecución del Juego

Para iniciar el juego, asegúrese de tener las dependencias instaladas y ejecute el script principal desde su terminal o entorno de desarrollo:

```bash
python pong_gestos.py
```

## 4. Instrucciones de Uso

### 4.1. Interfaz del Juego

El juego se abre en una ventana que muestra:

- La pelota en movimiento
- Las paletas controladas por las manos
- El marcador actualizado en tiempo real

### 4.2. Control por Gestos

- El sistema detecta hasta **dos manos** simultáneamente.
- Cada paleta es controlada por una mano:
  - **Paleta izquierda:** se mueve con la mano izquierda.
  - **Paleta derecha:** se mueve con la mano derecha.
- La paleta se posiciona automáticamente en base al **landmark 9** (centro de la palma) y su dirección se calcula desde la base de la mano (landmark 0).
- Se dibuja una paleta en forma de línea verde sobre la imagen de la cámara.

### 4.3. Objetivo del Juego

- Cada jugador debe evitar que la pelota toque su borde de la pantalla.
- Si la pelota toca el borde izquierdo, el jugador derecho gana un punto.
- Si la pelota toca el borde derecho, el jugador izquierdo gana un punto.
- La pelota rebota contra los bordes superior e inferior y contra las paletas.
- La velocidad de la pelota aumenta progresivamente con el tiempo.

### 4.4. Finalización del Juego

- Para salir del juego presione la tecla `ESC`.

## 5. Consejos de Uso

- Mantenga las manos visibles frente a la cámara para un seguimiento preciso.
- Juegue en un entorno bien iluminado para mejorar la detección de los gestos.
- Evite obstrucciones o movimientos bruscos que dificulten el reconocimiento.

## 6. Posibles Errores

- Si no se detecta la cámara, revise las configuraciones del sistema o permisos.
- Si la detección de manos es inconsistente, intente ajustar la iluminación o reiniciar el juego.

## 7. Autoría

Este juego fue desarrollado como parte de un proyecto universitario en la asignatura de Programación con Visión Artificial. Utiliza técnicas de detección de poses de manos y cálculos vectoriales para recrear una experiencia de juego tradicional con interacción moderna sin contacto físico.