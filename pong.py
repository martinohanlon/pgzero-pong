import pgzrun
from math import sin, cos, radians
from time import sleep

#setup the constants
TITLE = "Pygame Zero Pong"
WIDTH = 1000
HEIGHT = 800
BALLSPEED = 10
PADDLESPEED = 5
MAXBOUNCEANGLE = 75
gamemode = 1
hold = False

def reset_game(angle):
    global hold
    #setup ball properties
    ball.pos = WIDTH / 2, HEIGHT / 2
    ball.x_float = float(ball.x)
    ball.y_float = float(ball.y)
    ball.angle = angle
    ball.x_vel = BALLSPEED * cos(radians(ball.angle))
    ball.y_vel = BALLSPEED * sin(radians(ball.angle))

    #position the paddles
    pad1.pos = 30, HEIGHT / 2
    pad2.pos = WIDTH - 30, HEIGHT / 2

    # Tells the game to pause in update()
    hold = True

#create a rectangle of the playing area
screenRect = Rect(20, 60, WIDTH - 40, HEIGHT - 120)

#create ball
ball = Actor('ball')

#create paddles
pad1 = Actor('paddle')
pad2 = Actor('paddle')

#reset the game
reset_game(180)

#setup the goals
goals = [0, 0]

def draw():
    screen.clear()
    screen.draw.filled_rect(Rect((20, 32),(WIDTH-40, 16)), (255,255,255))
    screen.draw.filled_rect(Rect((20, HEIGHT-48),(WIDTH-40, 16)), (255,255,255))
    screen.blit('middots', (500-8, 48))
    screen.draw.text(str(goals[0]), midtop=(250, 80), fontname="lcd", fontsize=72)
    screen.draw.text(str(goals[1]), midtop=(750, 80), fontname="lcd", fontsize=72)
    if not hold:
        ball.draw()
    pad1.draw()
    pad2.draw()

def computer_move():
    if ball.x_vel >= 0:
    #If ball is moving away from paddle, center bat
        if pad1.y < (HEIGHT/2):
            pad1.y += 2
        elif pad1.y > (HEIGHT/2):
            pad1.y -= 2
    #if ball is moving towards bat, track its movement.
    elif ball.x_vel < 0:
        if pad1.y < ball.y:
            pad1.y += 3
        else:
            pad1.y -= 3

def update():
    global gamemode, hold
    # pause to let player(s) prepare
    if hold:
        sleep(2)
        hold = False
    #move the paddles
    if gamemode == 1:
    #in 1-player mode, let the computer operate paddle 1
        computer_move()
    if gamemode == 2:
    #in 2-player mode, let the player operate paddle 1
        if keyboard.q and pad1.top > 48:
            pad1.top -= PADDLESPEED
        if keyboard.a and pad1.bottom < HEIGHT-48:
            pad1.top += PADDLESPEED
    #in all modes, let the player operate paddle 2
    if keyboard.k and pad2.top > 48:
        pad2.top -= PADDLESPEED
    if keyboard.m and pad2.bottom < HEIGHT-48:
        pad2.top += PADDLESPEED

    #move the ball
    ball_old_x = ball.x_float
    ball_old_y = ball.y_float
    
    ball.x_float = ball.x_float + ball.x_vel
    ball.y_float = ball.y_float + ball.y_vel
    ball.x = int(round(ball.x_float))
    ball.y = int(round(ball.y_float))

    #move the ball back to where it was?
    reset_ball = False

    #has the ball left the screen?  
    if not screenRect.contains(ball._rect):
        
        #did it hit the top or bottom?
        if ball.top < 32 or ball.bottom > HEIGHT-32:
            ball.y_vel *= -1
            reset_ball = True
            
        #it must have hit the side
        else:
            if ball.left < 10:
                print("Player 2 goal")
                goals[1] += 1
                reset_game(180)
                print("Score {} : {}".format(goals[0], goals[1]))

            elif ball.right > WIDTH - 10:
                print("player 1 goal")
                goals[0] += 1
                reset_game(0)
                print("Score {} : {}".format(goals[0], goals[1]))
    
    #has the ball hit a paddle
    if pad1.colliderect(ball):
        #work out the bounce angle
        bounce_angle = ((ball.y - pad1.y) / (pad1.height / 2)) * MAXBOUNCEANGLE
        ball.angle = max(0 - MAXBOUNCEANGLE, min(MAXBOUNCEANGLE, bounce_angle))
        #work out the ball velocity
        ball.x_vel = BALLSPEED * cos(radians(ball.angle))
        ball.y_vel = BALLSPEED * sin(radians(ball.angle))

        reset_ball = True

    elif pad2.colliderect(ball):
        bounce_angle = 180 - (((ball.y - pad2.y) / (pad2.height / 2)) * MAXBOUNCEANGLE)
        ball.angle = max(180 - MAXBOUNCEANGLE, min(180 + MAXBOUNCEANGLE, bounce_angle))
        ball.x_vel = BALLSPEED * cos(radians(ball.angle))
        ball.y_vel = BALLSPEED * sin(radians(ball.angle))

        reset_ball = True

    if reset_ball:
        ball.x_float = ball_old_x + ball.x_vel  # The second term prevents the ball from sticking to the paddle
        ball.y_float = ball_old_y + ball.y_vel  # The second term prevents the ball from sticking to the paddle
        ball.x = int(round(ball.x_float))
        ball.y = int(round(ball.y_float))
            
pgzrun.go()
