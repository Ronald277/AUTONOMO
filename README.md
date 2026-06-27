# Trabajo final - Juego Snake en Python
**Nombre del proyecto:** Snake Game

**Nombre:** Ronald Andrade

**Fecha:** 28 de junio de 2026

## Objetivo del sistema
Desarrollar un videojuego clásico de la serpiente (Snake) utilizando el lenguaje Python.  
El proyecto busca integrar los conocimientos adquiridos en programación estructurada, manejo de eventos, estructuras de datos y control de flujo, al mismo tiempo que se enfrentan y resuelven problemas reales de desarrollo de software como la detección de colisiones, la generación aleatoria condicionada y la gestión de entradas asíncronas.

## ¿De qué trata el juego?

Controlas una serpiente que se mueve sin parar por un espacio cerrado. En el tablero aparece una pieza de comida (la manzana roja). Cuando la serpiente pasa por encima de ella, se la come, el jugador suma puntos y el cuerpo de la serpiente se alarga una casilla.

El desafío está en que no puedes chocar contra las paredes ni contra tu propio cuerpo. Cuanto más comes, más larga se vuelve la serpiente y más difícil resulta esquivarte a ti mismo. El objetivo es conseguir la máxima puntuación posible... o, si eres muy hábil, **llenar por completo el tablero con tu cuerpo**, lo que te dará la victoria definitiva.

## Funcionalidades principales

- **Movimiento fluido en cuadrícula**  
  La serpiente avanza de 20 en 20 píxeles por el centro de las celdas.

- **Buffer de dirección antiglitch**  
  Un sistema de "dirección pendiente" impide los giros de 180° aunque pulses varias teclas muy rápido.

- **Generación segura de comida**  
  La manzana aparece en posiciones alineadas con la cuadrícula y nunca sobre el cuerpo de la serpiente.

- **Crecimiento sin bugs**  
  Al comer, el nuevo segmento se coloca en la cola sin aparecer en el centro ni causar autocolisión.

- **Puntuación en tiempo real**  
  El marcador se actualiza en la parte superior tras cada comida.

- **Colisiones con paredes y cuerpo**  
  Al chocar se muestra un mensaje con el puntaje y la partida se reinicia automáticamente.

- **Condición de victoria**  
  Si el tablero queda completamente lleno, el jugador gana, se muestra un mensaje y el juego termina.

- **Mensajes visibles**  
  Los textos de derrota o victoria se muestran correctamente gracias al refresco forzado de pantalla.

- **Cuadrícula de fondo**  
  Líneas grises que delimitan visualmente las celdas y facilitan la orientación.

- **Velocidad ajustable**  
  El ritmo del juego se controla con `time.sleep(0.15)` y se puede modificar fácilmente en el código.

## Cómo jugar

1. Ejecuta el programa. Aparecerá una ventana negra con una cuadrícula gris.
2. La serpiente (cuadrado verde) empieza quieta en el centro.
3. Usa las teclas para moverla:
   - `W` → Arriba
   - `S` → Abajo
   - `A` → Izquierda
   - `D` → Derecha
4. Conduce la serpiente hasta la manzana roja para comerla.
5. Cada manzana suma 10 puntos y alarga el cuerpo.
6. Evita chocar con los bordes o con tu propio cuerpo.
7. Si llenas todo el tablero, ¡ganas la partida!

## Problemas que encontramos durante el desarrollo

Mientras se programaba el juego aparecieron varios errores que me obligaron a repensar partes del código. Estos fueron los tres más importantes:

### 1. La serpiente moría al comer la primera manzana

**Qué pasaba:**  
Nada más empezar, si la serpiente comía la primera manzana, el juego terminaba sin mostrar ningún mensaje.

**Por qué ocurría:**  
Al comer, se activaba una orden para añadir un segmento al cuerpo. Pero ese nuevo segmento se creaba justo encima de la cabeza, por lo que el juego detectaba una colisión contra el cuerpo y mataba a la serpiente al instante. Además, el mensaje de "Has perdido" no se veía porque la pantalla no se refrescaba antes de la pausa.

**Solución dada:**  
Se cambió la función de crecimiento para que el nuevo segmento se coloque en la celda que la cabeza **acaba de abandonar** y no encima de ella. También añadimos un refresco de pantalla (`ventana.update()`) justo antes de mostrar los mensajes.

### 2. La serpiente iba por las líneas, no dentro de las celdas

**Qué pasaba:**  
El fondo tenía líneas dibujadas para marcar la cuadrícula, pero la serpiente avanzaba justo sobre esas líneas, dando la sensación de ir por los bordes de las baldosas.

**Por qué ocurría:**  
Las líneas de la cuadrícula estaban dibujadas en las mismas coordenadas por las que se mueve la serpiente (múltiplos de 20: -280, -260...). Coincidían exactamente.

**Solución dada:**  
Desplacé todas las líneas 10 píxeles hacia fuera (ahora están en -290, -270...). Así la serpiente se mueve por el centro de cada celda y la cuadrícula funciona como borde visual.

### 3. Bug del giro rápido (autocolisión por pulsar dos teclas seguidas)

**Qué pasaba:**  
Si ibas hacia abajo y pulsabas muy rápido izquierda y luego arriba, la serpiente giraba 180° de golpe y chocaba contra su cuerpo, aunque el jugador no pretendiera hacer ese movimiento.

**Por qué ocurría:**  
Las teclas cambiaban directamente la dirección actual. Al pulsar "izquierda", la dirección pasaba de "abajo" a "izquierda". Inmediatamente después, al pulsar "arriba", el código comparaba "arriba" con "izquierda" (el nuevo valor). Como no son direcciones opuestas, permitía el cambio. El resultado era un giro de 180° en un solo fotograma.

**Solución dada:**  
Se creó una variable intermedia (`nueva_direccion`) que guarda la última tecla pulsada sin aplicarla todavía. En cada fotograma del juego, **solo una vez**, se comprueba si esa nueva dirección es válida respecto a la dirección real con la que se movió la serpiente en el fotograma anterior. Si no lo es, simplemente se ignora. De esta forma, las pulsaciones rápidas no rompen el juego.

## Versión de Python que utilicé: 3.14.5

