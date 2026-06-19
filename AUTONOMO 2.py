import turtle
import time
import random

# Configuración
ventana = turtle.Screen()
ventana.title("Juego de la Serpiente - Paso 2")
ventana.bgcolor("black")
ventana.setup(width=600, height=600)
ventana.tracer(0)

# Cabeza
cabeza = turtle.Turtle()
cabeza.speed(0)
cabeza.shape("square")
cabeza.color("green")
cabeza.penup()
cabeza.goto(0,0)
cabeza.direccion = "stop"

# Comida
comida = turtle.Turtle()
comida.speed(0)
comida.shape("circle")
comida.color("red")
comida.penup()
comida.goto(0,100)

# Funciones de movimiento
def ir_arriba(): cabeza.direccion = "up"
def ir_abajo(): cabeza.direccion = "down"
def ir_izq(): cabeza.direccion = "left"
def ir_der(): cabeza.direccion = "right"

ventana.listen()
ventana.onkeypress(ir_arriba, "w")
ventana.onkeypress(ir_abajo, "s")
ventana.onkeypress(ir_izq, "a")
ventana.onkeypress(ir_der, "d")

while True:
    ventana.update()

    # Lógica de colisión con paredes
    if cabeza.xcor() > 290 or cabeza.xcor() < -290 or cabeza.ycor() > 290 or cabeza.ycor() < -290:
        time.sleep(1)
        cabeza.goto(0,0)
        cabeza.direccion = "stop"

    # Lógica de consumo de comida
    if cabeza.distance(comida) < 20:
        x = random.randint(-280, 280)
        y = random.randint(-280, 280)
        comida.goto(x,y)

    # Movimiento
    if cabeza.direccion == "up": cabeza.sety(cabeza.ycor() + 20)
    if cabeza.direccion == "down": cabeza.sety(cabeza.ycor() - 20)
    if cabeza.direccion == "left": cabeza.setx(cabeza.xcor() - 20)
    if cabeza.direccion == "right": cabeza.setx(cabeza.xcor() + 20)

    time.sleep(0.1)