import simplegui
import random

WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_pos = [WIDTH / 2, HEIGHT / 2]
vel = [-50.0 / 90.0, 50.0 / 90.0]
speed_increment = 0.0001

def spawn_ball(direction):
    global ball_pos, ball_vel  
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    if direction == RIGHT:
        ball_vel = [random.randrange(2, 4), -random.randrange(1, 3)]
    else:
        ball_vel = [-random.randrange(2, 4), -random.randrange(1, 3)]

def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel 
    global score1, score2 
    score1 = 0
    score2 = 0
    paddle1_pos = HEIGHT / 2 - HALF_PAD_HEIGHT
    paddle2_pos = HEIGHT / 2 - HALF_PAD_HEIGHT
    paddle1_vel = 0
    paddle2_vel = 0
    spawn_ball(random.choice([LEFT, RIGHT]))

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
    global paddle1_vel, paddle2_vel

    ball_pos[0] += vel[0] * 3
    ball_pos[1] += vel[1] * 3
    
    if ball_pos[0] <= BALL_RADIUS:
        vel[0] = - vel[0]
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT - BALL_RADIUS:
        vel[1] = - vel[1]
        
    vel[0] *= (1 + speed_increment)
    vel[1] *= (1 + speed_increment)
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")

    canvas.draw_line([HALF_PAD_WIDTH, paddle1_pos],
                     [HALF_PAD_WIDTH, paddle1_pos + PAD_HEIGHT], PAD_WIDTH, "White")
    canvas.draw_line([WIDTH - HALF_PAD_WIDTH, paddle2_pos],
                     [WIDTH - HALF_PAD_WIDTH, paddle2_pos + PAD_HEIGHT], PAD_WIDTH, "White")

    if paddle1_pos + paddle1_vel >= 0 and paddle1_pos + paddle1_vel <= HEIGHT - PAD_HEIGHT:
        paddle1_pos += paddle1_vel
    if paddle2_pos + paddle2_vel >= 0 and paddle2_pos + paddle2_vel <= HEIGHT - PAD_HEIGHT:
        paddle2_pos += paddle2_vel

    if (ball_pos[0] - BALL_RADIUS <= PAD_WIDTH and
            paddle1_pos <= ball_pos[1] <= paddle1_pos + PAD_HEIGHT):
        vel[0] = -vel[0]
    elif (ball_pos[0] + BALL_RADIUS >= WIDTH - PAD_WIDTH and
            paddle2_pos <= ball_pos[1] <= paddle2_pos + PAD_HEIGHT):
        vel[0] = -vel[0]
    
    if ball_pos[0] - BALL_RADIUS <= 0:
        score2 += 1
        spawn_ball(RIGHT)
    elif ball_pos[0] + BALL_RADIUS >= WIDTH:
        score1 += 1
        spawn_ball(LEFT)

    canvas.draw_text(str(score1), [WIDTH / 4, 50], 36, "White")
    canvas.draw_text(str(score2), [3 * WIDTH / 4, 50], 36, "White")

def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 3
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -3
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 3
    elif key == simplegui.KEY_MAP["w"]:
        paddle1_vel = -3

def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["down"] or key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["s"] or key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0

frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

new_game()
frame.start()
