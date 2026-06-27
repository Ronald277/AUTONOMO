import turtle
import time
import random

# Configuración de la ventana
ventana = turtle.Screen()
ventana.title("Juego de la Serpiente - Completo")
ventana.bgcolor("black")
ventana.setup(width=600, height=600)
ventana.tracer(0)

# ------------------ CUADRÍCULA (celdas visibles) ------------------
dibujo = turtle.Turtle()
dibujo.hideturtle()
dibujo.speed(0)
dibujo.color("gray20")
dibujo.pensize(1)

for x in range(-290, 291, 20):
    dibujo.penup()
    dibujo.goto(x, 290)
    dibujo.pendown()
    dibujo.goto(x, -290)

for y in range(-290, 291, 20):
    dibujo.penup()
    dibujo.goto(-290, y)
    dibujo.pendown()
    dibujo.goto(290, y)
# ---------------------------------------------------------------

# Cabeza
cabeza = turtle.Turtle()
cabeza.speed(0)
cabeza.shape("square")
cabeza.color("green")
cabeza.penup()
cabeza.goto(0, 0)
cabeza.direccion = "stop"

# Nueva variable para encolar la dirección solicitada
nueva_direccion = "stop"

# Comida
comida = turtle.Turtle()
comida.speed(0)
comida.shape("circle")
comida.color("red")
comida.penup()
comida.goto(0, 100)

# Sistema de puntaje
puntaje = 0
marcador = turtle.Turtle()
marcador.speed(0)
marcador.color("white")
marcador.penup()
marcador.hideturtle()
marcador.goto(0, 260)
marcador.write(f"Puntaje: {puntaje}", align="center", font=("Courier", 24, "normal"))

# Turtle para mensajes (reutilizable)
mensaje_turtle = turtle.Turtle()
mensaje_turtle.speed(0)
mensaje_turtle.color("yellow")
mensaje_turtle.penup()
mensaje_turtle.hideturtle()
mensaje_turtle.goto(0, 0)

# Cuerpo de la serpiente
segmentos = []
ocupadas = set()
ocupadas.add((0, 0))
crecer = False

def agregar_segmento(x, y):
    nuevo = turtle.Turtle()
    nuevo.speed(0)
    nuevo.shape("square")
    nuevo.color("dark green")
    nuevo.penup()
    if segmentos:
        ultimo = segmentos[-1]
        nuevo.goto(ultimo.xcor(), ultimo.ycor())
    else:
        nuevo.goto(x, y)
    segmentos.append(nuevo)

# Funciones de movimiento: ahora solo guardan la nueva dirección solicitada
def ir_arriba():
    global nueva_direccion
    if cabeza.direccion != "down":  # validación contra dirección real actual
        nueva_direccion = "up"

def ir_abajo():
    global nueva_direccion
    if cabeza.direccion != "up":
        nueva_direccion = "down"

def ir_izq():
    global nueva_direccion
    if cabeza.direccion != "right":
        nueva_direccion = "left"

def ir_der():
    global nueva_direccion
    if cabeza.direccion != "left":
        nueva_direccion = "right"

ventana.listen()
ventana.onkeypress(ir_arriba, "w")
ventana.onkeypress(ir_abajo, "s")
ventana.onkeypress(ir_izq, "a")
ventana.onkeypress(ir_der, "d")

def mostrar_mensaje(texto, duracion=2):
    mensaje_turtle.clear()
    mensaje_turtle.write(texto, align="center", font=("Courier", 30, "bold"))
    ventana.update()
    time.sleep(duracion)
    mensaje_turtle.clear()

def nueva_comida():
    for _ in range(1000):
        x = random.randint(-14, 14) * 20
        y = random.randint(-14, 14) * 20
        if (x, y) not in ocupadas:
            comida.goto(x, y)
            return True
    return False

def reiniciar_juego():
    global puntaje, crecer, nueva_direccion
    cabeza.goto(0, 0)
    cabeza.direccion = "stop"
    nueva_direccion = "stop"
    for seg in segmentos:
        seg.reset()
        seg.hideturtle()
    segmentos.clear()
    puntaje = 0
    marcador.clear()
    marcador.write(f"Puntaje: {puntaje}", align="center", font=("Courier", 24, "normal"))
    ocupadas.clear()
    ocupadas.add((0, 0))
    crecer = False

# Bucle principal
jugando = True
while jugando:
    ventana.update()

    # Colisión con paredes
    if cabeza.xcor() > 290 or cabeza.xcor() < -290 or cabeza.ycor() > 290 or cabeza.ycor() < -290:
        mostrar_mensaje(f"¡Has perdido!\nPuntaje: {puntaje}")
        reiniciar_juego()
        continue

    # ---- GESTIÓN DE DIRECCIÓN (buffer de un solo cambio) ----
    if nueva_direccion != "stop":
        # Solo aplicar el cambio si no es opuesto a la dirección real actual
        if (nueva_direccion == "up" and cabeza.direccion != "down") or \
           (nueva_direccion == "down" and cabeza.direccion != "up") or \
           (nueva_direccion == "left" and cabeza.direccion != "right") or \
           (nueva_direccion == "right" and cabeza.direccion != "left"):
            cabeza.direccion = nueva_direccion
        # Si no, se ignora y se mantiene la anterior

    # Movimiento
    if cabeza.direccion != "stop":
        ant_x = cabeza.xcor()
        ant_y = cabeza.ycor()

        if cabeza.direccion == "up":
            cabeza.sety(cabeza.ycor() + 20)
        elif cabeza.direccion == "down":
            cabeza.sety(cabeza.ycor() - 20)
        elif cabeza.direccion == "left":
            cabeza.setx(cabeza.xcor() - 20)
        elif cabeza.direccion == "right":
            cabeza.setx(cabeza.xcor() + 20)

        if crecer:
            agregar_segmento(ant_x, ant_y)
            crecer = False
        else:
            if segmentos:
                cola_x = segmentos[-1].xcor()
                cola_y = segmentos[-1].ycor()
                ocupadas.discard((cola_x, cola_y))
            else:
                ocupadas.discard((ant_x, ant_y))

        ocupadas.add((cabeza.xcor(), cabeza.ycor()))

        for i in range(len(segmentos) - 1, 0, -1):
            x = segmentos[i - 1].xcor()
            y = segmentos[i - 1].ycor()
            segmentos[i].goto(x, y)
        if segmentos:
            segmentos[0].goto(ant_x, ant_y)

    # Comer
    if cabeza.distance(comida) < 20:
        exito = nueva_comida()
        if not exito:
            puntaje += 10
            marcador.clear()
            marcador.write(f"Puntaje: {puntaje}", align="center", font=("Courier", 24, "normal"))
            mostrar_mensaje(f"¡Has ganado!\nLlenaste el tablero.\nPuntaje: {puntaje}", 3)
            jugando = False
            break
        else:
            puntaje += 10
            marcador.clear()
            marcador.write(f"Puntaje: {puntaje}", align="center", font=("Courier", 24, "normal"))
            crecer = True

    # Colisión con cuerpo
    for seg in segmentos:
        if cabeza.distance(seg) < 20:
            mostrar_mensaje(f"¡Has perdido!\nPuntaje: {puntaje}")
            reiniciar_juego()
            break

    time.sleep(0.15)

ventana.mainloop()
