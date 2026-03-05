#Juego de pong en el que el jugador controla la paleta izquierda y la computadora controla la paleta derecha.
# El juego incluye un marcador, sonidos de rebote y puntuación, y aumenta la velocidad de la pelota con cada rebote.
# El juego termina cuando uno de los jugadores llega a 3 puntos.
import turtle
import random
import tkinter as tk
import winsound
import time
wn = turtle.Screen()
game_over = False
game_running = True

# Configuración de la ventana
wn.title("Pong por Lau")
wn.bgcolor("black")
wn.setup(width=800, height=600)
wn.tracer(0)

# Linea divisora
center_line = turtle.Turtle()
center_line.color("white")
center_line.penup()
center_line.goto(0, -300)
center_line.setheading(90)
center_line.pensize(3)

for i in range(30):
    center_line.pendown()
    center_line.forward(10)
    center_line.penup()
    center_line.forward(10)

# Marcador
score_a = 0
score_b = 0
score_display = turtle.Turtle()
score_display.speed(0)
score_display.color("white")
score_display.penup()
score_display.hideturtle()
score_display.goto(0, 260)
def update_score():
    score_display.clear()
    score_display.write(f"Jugador A: {score_a}  Jugador B: {score_b}", align="center", font=("Courier", 24, "normal"))
    
# Paleta A
paddle_a = turtle.Turtle()  
paddle_a.speed(0)
paddle_a.shape("square")
paddle_a.color("white")
paddle_a.shapesize(stretch_wid=5, stretch_len=1)
paddle_a.penup()
paddle_a.goto(-350, 0)
# Paleta B
paddle_b = turtle.Turtle()
paddle_b.speed(0)
paddle_b.shape("square")
paddle_b.color("white")
paddle_b.shapesize(stretch_wid=5, stretch_len=1)
paddle_b.penup()
paddle_b.goto(350, 0)
# Pelota
ball = turtle.Turtle()
ball.speed(100)
ball.shape("square")
ball.color("white")
ball.penup()
ball.goto(0, 0)
start_dx = 1.5  
start_dy = -1.5
ball.dx = start_dx
ball.dy = start_dy
speed_increment = 1.25
max_speed = 5

# Pantalla de inicio
start_screen = turtle.Turtle()
start_screen.color("white")
start_screen.hideturtle()
start_screen.penup()
start_screen.goto(0, 0)
start_screen.write(
    "PONG\n\nPresiona ESPACIO para empezar\nW / S para mover\nPrimero a 3 gana",
    align="center",
    font=("Courier", 20, "normal")
)
game_running = False

# Funciones
def paddle_a_up():
    y = paddle_a.ycor()
    y += 20
    paddle_a.sety(y)
def paddle_a_down():
    y = paddle_a.ycor()
    y -= 20
    paddle_a.sety(y)
def paddle_b_up():
    y = paddle_b.ycor()
    y += 20
    paddle_b.sety(y)
def paddle_b_down():
    y = paddle_b.ycor()
    y -= 20
    paddle_b.sety(y)
    
# Funcion para iniciar el juego
def start_game():
    global game_running
    start_screen.clear()
    game_running = True
    
# Función para mostrar la ventana de fin del juego , que jugador a ganado y si quiere volver a jugar, reiniciando la partida
def ventana_fin(ganador):
    global game_running
    game_running = False
    ventana = tk.Toplevel(wn._root)
    ventana.title("Fin del juego")
    ventana.geometry("250x120")
    label = tk.Label(ventana, text=f"¡Jugador {ganador} ha ganado! ¿Jugar otra vez?")
    label.pack(pady=10)
    def reiniciar():
        reiniciar_juego()
        ventana.destroy()
    boton_reiniciar = tk.Button(ventana, text="Sí", command=reiniciar)
    boton_reiniciar.pack(side="left", padx=20)
    boton_salir = tk.Button(ventana, text="No", command=cerrar_juego)
    boton_salir.pack(side="right", padx=20)
# Función para verificar si el juego ha terminado
def verificar_fin():
    if score_a >= 3:
        winsound.PlaySound("sounds/win.wav", winsound.SND_ASYNC)
        ventana_fin("A")
    elif score_b >= 3:
        winsound.PlaySound("sounds/lose.wav", winsound.SND_ASYNC)
        ventana_fin("B")
# Función para reiniciar el juego
def reiniciar_juego():
    global score_a, score_b, game_over, game_running

    score_a = 0
    score_b = 0

    ball.goto(0,0)
    ball.dx = start_dx
    ball.dy = start_dy
    paddle_a.goto(-350,0)
    paddle_b.goto(350,0)
    game_over = False
    game_running = True
    update_score()
    
def game_loop():
    global game_running
    if not game_running:
        return
    
def cerrar_juego():
    global game_running
    game_running = False
    wn.bye()

#Teclado
wn.listen()
wn.onkeypress(paddle_a_up, "w")
wn.onkeypress(paddle_a_down, "s")
wn.onkeypress(start_game, "space")



#computadora controla la paleta b
ai_speed = 4

# Bucle principal del juego
while True:
    time.sleep(0.01)
    try:
        wn.update()
        if not game_running:
            continue
        
        # Mover la pelota
        ball.setx(ball.xcor() + ball.dx)
        ball.sety(ball.ycor() + ball.dy)
        
        # Hacer menos capaze a la computadora de seguir la pelota perfectamente        
        if ball.dx > 0:
            target = ball.ycor() + random.randint(-25, 25)
            if paddle_b.ycor() < target:
                paddle_b.sety(paddle_b.ycor() + ai_speed)
            elif paddle_b.ycor() > target:
                paddle_b.sety(paddle_b.ycor() - ai_speed)      
                   
        # Colisiones con los bordes
        if ball.ycor() > 290:
            ball.sety(290)
            ball.dy *= -1
            winsound.PlaySound("sounds/bounce.wav", winsound.SND_ASYNC)
        if ball.ycor() < -290:
            ball.sety(-290)
            ball.dy *= -1
            winsound.PlaySound("sounds/bounce.wav", winsound.SND_ASYNC)
            
            # Jugador A anota
        if ball.xcor() > 390:
            score_a += 1
            winsound.PlaySound("sounds/score.wav", winsound.SND_ASYNC)
            ball.goto(0, 0)
            paddle_a.goto(-350, 0)
            paddle_b.goto(350, 0)
            ball.dx = start_dx * random.choice([-1, 1])
            ball.dy = start_dy * random.choice([-1, 1])
            update_score()
            wn.update()
            time.sleep(1)

        # Jugador B anota
        if ball.xcor() < -390:
            score_b += 1
            winsound.PlaySound("sounds/score.wav", winsound.SND_ASYNC)

            ball.goto(0, 0)
            paddle_a.goto(-350, 0)
            paddle_b.goto(350, 0)

            ball.dx = start_dx * random.choice([-1, 1])
            ball.dy = start_dy * random.choice([-1, 1])

            update_score()
            wn.update()
            time.sleep(1)
        # Colisiones con las paletas
        # Colisión con paleta B
        if (340 < ball.xcor() < 350) and (paddle_b.ycor()-50 < ball.ycor() < paddle_b.ycor()+50):
            ball.setx(340)
            ball.dx *= -speed_increment
            ball.dy *= speed_increment
            if abs(ball.dx) > max_speed:
                ball.dx = max_speed if ball.dx > 0 else -max_speed
            if abs(ball.dy) > max_speed:
                ball.dy = max_speed if ball.dy > 0 else -max_speed
            winsound.PlaySound("sounds/bounce.wav", winsound.SND_ASYNC)

        # Colisión con paleta A
        if (-350 < ball.xcor() < -340) and (paddle_a.ycor()-50 < ball.ycor() < paddle_a.ycor()+50):
            ball.setx(-340)
            ball.dx *= -speed_increment
            ball.dy *= speed_increment
            if abs(ball.dx) > max_speed:
                ball.dx = max_speed if ball.dx > 0 else -max_speed
            if abs(ball.dy) > max_speed:
                ball.dy = max_speed if ball.dy > 0 else -max_speed
            winsound.PlaySound("sounds/bounce.wav", winsound.SND_ASYNC)              
        update_score()
        
        # Limitar el movimiento de las paletas
        if paddle_a.ycor() > 250:
            paddle_a.sety(250)
        if paddle_a.ycor() < -250:
            paddle_a.sety(-250)
        if paddle_b.ycor() > 250:
            paddle_b.sety(250)
        if paddle_b.ycor() < -250:
            paddle_b.sety(-250)
            
        # Limitar la velocidad de la pelota
        if ball.dx > max_speed:
            ball.dx = max_speed
        if ball.dx < -max_speed:
            ball.dx = -max_speed
        if ball.dy > max_speed:
            ball.dy = max_speed
        if ball.dy < -max_speed:
            ball.dy = -max_speed
            
        # detener el juego cuando uno de los jugadores llega a 3 puntos y mostrar la ventana de fin del juego
        if not game_over and (score_a >= 3 or score_b >= 3):
            game_running = False
            game_over = True
            verificar_fin()
    except (turtle.Terminator, tk.TclError):
        break




            
            

