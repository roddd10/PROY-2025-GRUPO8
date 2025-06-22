# Manual de Usuario – Gato con Control por Gestos

## Juego: Gato Virtual Interactivo mediante Reconocimiento de Gestos

---

## Descripción General

Este juego de Gato (también conocido como "Tres en Raya") ha sido implementado en Python utilizando las bibliotecas OpenCV, MediaPipe y Pygame. Permite a dos jugadores interactuar con el tablero mediante gestos captados por la cámara web. Cada jugador utiliza un gesto distinto con la mano para colocar su marca en el tablero.

---

## Requisitos del Sistema

- Python 3.11 o superior
- Cámara web funcional
- Resolución recomendada: 640x480

### Dependencias

Instalación de dependencias mediante `pip`:

```bash
pip install opencv-python mediapipe pygame numpy
```

---

## Instrucciones de Ejecución

1. Clonar el repositorio y navegar a la carpeta del proyecto:

```bash
cd src/gato
```

2. Ejecutar el archivo principal:

```bash
python main.py
```

3. El sistema abrirá una ventana de Pygame con el tablero y una ventana de la cámara con la detección de gestos.

---

## Controles y Gestos

- Jugador 1 (Círculo): debe juntar el pulgar e índice para formar un gesto de círculo.
- Jugador 2 (Cruz): debe cerrar la mano completamente, formando un puño.

### Acciones:

- Para marcar una celda, el jugador debe realizar su gesto correspondiente frente a la cámara.
- El sistema identifica en qué parte del tablero está la mano y coloca la marca.
- Presionar `R` permite reiniciar el juego.
- Presionar `Q` o cerrar la ventana termina el programa.

---

## Lógica de Funcionamiento

- El juego funciona en turnos alternados entre los jugadores.
- El gesto detectado debe coincidir con el turno actual para que sea considerado válido.
- El sistema localiza la región de la mano y asigna la jugada a la celda correspondiente.
- Se verifica automáticamente si un jugador ha ganado o si hay empate.

---

## Interfaz y Visualización

- La ventana de Pygame muestra el tablero de Gato con las marcas realizadas.
- La ventana de la cámara muestra:
  - El gesto detectado
  - Las líneas guía del tablero
  - El turno actual

---

## Problemas Frecuentes

| Problema                             | Solución                                                                     |
| ------------------------------------ | --------------------------------------------------------------------------- |
| "La cámara no responde"              | Verificar que no esté siendo usada por otra aplicación.                      |
| "No se detecta el gesto correctamente" | Asegurarse de que la mano esté centrada y bien iluminada.                  |
| "Las marcas aparecen en celdas incorrectas" | Ajustar la posición de la mano y realizar el gesto con claridad.     |

---

## Recomendaciones Generales

- Jugar en un ambiente con buena iluminación.
- Mantener la mano dentro del encuadre y evitar movimientos rápidos.
- Evitar usar prendas o fondos que dificulten la detección de la mano.

---

## Créditos

Desarrollado por el Grupo 8 como parte del Proyecto PROY-2025.

