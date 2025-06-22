# Informe Técnico del Proyecto: Juegos Interactivos Controlados por Mano

## 1. Introducción

El presente proyecto surge como iniciativa de un grupo de estudiantes motivados por trasladar la experiencia de los juegos de mesa clásicos a un entorno digital más interactivo y didáctico. El objetivo principal fue rediseñar juegos tradicionales utilizando tecnologías de visión por computadora, para que puedan ser controlados mediante gestos de la mano, sin contacto físico.

Cada integrante del grupo desarrolló un juego distinto (por ejemplo, Snake, Pong, etc.), pero el desarrollo fue colaborativo: los aprendizajes y soluciones de cada uno fueron compartidos con los demás, facilitando el avance técnico colectivo del grupo.

## 2. Tecnologías Utilizadas

- **Python 3.x**: Lenguaje principal de programación.
- **OpenCV**: Procesamiento de imagen en tiempo real.
- **MediaPipe (Hands)**: Detección y seguimiento de las manos y dedos.
- **NumPy**: Manipulación eficiente de arreglos y coordenadas.
- **Winsound (Windows)**: Para efectos de sonido en eventos del juego.

## 3. Arquitectura General del Sistema

Cada juego comparte una arquitectura similar basada en los siguientes módulos:

- **Captura de cámara**: Inicialización de la webcam con configuración personalizada.
- **Detección de manos**: Uso de MediaPipe Hands para identificar landmarks en tiempo real.
- **Procesamiento de gestos**: Análisis de la posición de los dedos (típicamente el índice) para controlar direcciones o colisiones.
- **Lógica del juego**: Incluye el estado, reglas, colisiones, reinicio y actualización de puntuaciones.
- **Renderizado gráfico**: Dibujo de tablero, jugadores, objetos y HUD mediante OpenCV.

## 4. Análisis Técnico por Juego

### 4.1 Snake con Seguimiento de Mano

- **Control**: Se rastrea el dedo índice (landmark 8) para cambiar la dirección de la serpiente, considerando umbrales de distancia para evitar cambios involuntarios.
- **Frutas**: Hay tres tipos de frutas (normal, dorada, trampa), cada una con efectos diferentes en la puntuación y estado del juego.
- **Obstáculos**: Son dinámicos y se mueven de forma autónoma cada cierto tiempo.
- **Dificultades**: Modo difícil (colisiones con bordes), velocidad progresiva según frutas comidas.
- **Persistencia**: Se almacenan los 3 mejores puntajes en archivo `highscores.txt`.

### 4.2 Pong con Control de Paletas por Mano

- **Paletas**: Se usan los landmarks 0 y 9 para calcular la posición y orientación de la paleta del jugador.
- **Pelota**: Tiene velocidad y dirección iniciales, las cuales se aceleran gradualmente hasta un máximo.
- **Colisiones**: Se detectan usando vectores normales a las paletas. Si la pelota está próxima y alineada con la paleta, se refleja.
- **Marcador**: Se actualiza al pasar la pelota por los bordes y se reinicia la posición.

## 5. Colaboración y Trabajo en Equipo

El desarrollo de este proyecto fue altamente colaborativo. Si bien cada miembro del grupo se enfocó en un juego distinto, se compartieron constantemente avances, códigos, estrategias de detección de colisiones, representación visual y manejo de gestos. Por ejemplo:

- El sistema de detección de colisiones del juego Pong fue reutilizado en parte para el manejo de colisiones con obstáculos en Snake.
- El enfoque de dirección mediante gestos del Snake sirvió como base para otros sistemas de control manual.
- Las optimizaciones de velocidad progresiva y reinicio de juego se intercambiaron entre integrantes.

## 6. Resultados y Conclusiones

El proyecto demostró que es posible transformar juegos clásicos en experiencias modernas sin contacto físico, aprovechando tecnologías accesibles como la cámara web y librerías gratuitas.

- Se cumplió el objetivo de crear juegos interactivos, intuitivos y accesibles.
- El uso de la visión por computadora agregó un componente educativo y tecnológico valioso.
- El trabajo colaborativo aceleró el aprendizaje y la resolución de problemas comunes.

## 7. Futuras Mejoras

- Agregar detección de múltiples gestos para más comandos (pausa, turbo, etc.).
- Incluir reconocimiento de manos para identificar jugadores.
- Integrar una interfaz gráfica externa (Tkinter, PyQt) para configuración previa.
- Soporte multijugador en juegos como Pong.