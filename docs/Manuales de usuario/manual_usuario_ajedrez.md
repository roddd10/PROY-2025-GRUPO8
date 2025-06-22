# Manual de Usuario – Ajedrez con Control por Gestos

## Juego: Ajedrez Virtual con Detección de Manos

---

## Descripción General

Este módulo permite jugar al ajedrez virtual utilizando gestos con la mano, que son reconocidos mediante una cámara web y procesados con las bibliotecas MediaPipe y OpenCV. El usuario puede mover piezas cerrando la mano sobre una posición del tablero y soltándola al abrirla sobre otra casilla.

---

## Requisitos del Sistema

- Python 3.11 o superior
- Cámara web funcional
- Resolución recomendada: 1280x720

### Dependencias

Instalación de dependencias mediante `pip`:

```bash
pip install -r requirements.txt
```

Contenido sugerido del archivo `requirements.txt`:

```
pygame
opencv-python
mediapipe
numpy
python-chess
```

---

## Instrucciones de Ejecución

1. Clonar el repositorio y navegar a la carpeta del proyecto:

```bash
cd src/ajedrez
```

2. Ejecutar el archivo principal:

```bash
python main.py
```

3. Apuntar la cámara hacia un tablero físico de ajedrez de 7x7 casillas para que el sistema lo detecte.

4. Una vez detectado, presionar la tecla Enter para iniciar el juego.

---

## Controles y Gestos

- Gesto de puño cerrado: permite seleccionar o "agarrar" una pieza.
- Gesto de mano abierta: permite soltar la pieza previamente seleccionada.
- El tablero responde al movimiento de la mano del usuario.
- Presionar la tecla `Z` permite deshacer el último movimiento.
- Para cerrar el juego, se puede presionar `ESC` o cerrar la ventana manualmente.

## Lógica de Funcionamiento Interno

- Se utiliza MediaPipe para detectar la mano del usuario en tiempo real.
- La distancia entre el pulgar y el índice permite distinguir entre dos gestos:
  - Gesto "closed": si la distancia es pequeña.
  - Gesto "open": si la distancia es grande.
- Las imágenes correspondientes a las piezas (ubicadas en `assets/white/` y `assets/black/`) se cargan mediante Pygame.

---

## Problemas Frecuentes

| Problema                            | Solución                                                                    |
| ----------------------------------- | --------------------------------------------------------------------------- |
| "No se pudo acceder a la cámara"    | Verificar que la cámara esté conectada y no esté siendo utilizada por otra aplicación. |
| "Imagen blanca/negra no encontrada" | Asegurarse de que los archivos `.png` estén correctamente ubicados en `assets/white/` y `assets/black/`. |
| No se detecta el tablero            | Asegurarse de tener buena iluminación y que el tablero esté centrado en el encuadre de la cámara. |

---

## Recomendaciones Generales

- Colocar la cámara en una posición estable, enfocando directamente el tablero.
- Jugar en un entorno con iluminación uniforme.
- Ejecutar el juego en pantalla completa para una experiencia más inmersiva.

---

## Créditos

Desarrollado por el Grupo 8 como parte del Proyecto PROY-2025.

