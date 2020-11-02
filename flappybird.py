import pgzrun
import random
from bot import Bot



bot = Bot()

TITLE = 'Flappy Bird'
WIDTH = 288
HEIGHT = 512

# These constants control the difficulty of the game
GAP = 130
GRAVITY = 0.3
FLAP_STRENGTH = 6.5
SPEED = 3

bird = Actor('bird1', (75, 200))
bird.dead = False
bird.score = 0
bird.vy = 0

storage.setdefault('highscore', 0)


def reset_pipes():
    pipe_gap_y = random.randint(200, HEIGHT - 200)
    pipe_top.pos = (WIDTH, pipe_gap_y - GAP // 2)
    pipe_bottom.pos = (WIDTH, pipe_gap_y + GAP // 2)


pipe_top = Actor('top', anchor=('left', 'bottom'))
pipe_bottom = Actor('bottom', anchor=('left', 'top'))
reset_pipes()  # Set initial pipe positions.


def update_pipes():
    pipe_top.left -= SPEED
    pipe_bottom.left -= SPEED
    if pipe_top.right < 0:
        reset_pipes()
        if not bird.dead:
            bird.score += 1
            if bird.score > storage['highscore']:
                storage['highscore'] = bird.score


def update_bird():
    uy = bird.vy
    bird.vy += GRAVITY
    bird.y += (uy + bird.vy) / 2
    bird.x = 75

    if not bird.dead:
        if bird.vy < -3:
            bird.image = 'bird2'
        else:
            bird.image = 'bird1'
        status = bot.act(-bird.x + pipe_top.left,
             -bird.y + pipe_bottom.pos[1],
              bird.vy)
        if status==1: # click button if status==1 
            on_key_down()

    if bird.colliderect(pipe_top) or bird.colliderect(pipe_bottom):
        if not bird.dead:
            bot.update_scores()
            print("Game %d score %d" %  (bot.gameCNT, bird.score))
        bird.dead = True
        bird.image = 'birddead'
        bird.y = 200
        bird.dead = False
        bird.score = 0
        bird.vy = 0
        reset_pipes()


    if not 0 < bird.y < HEIGHT:
        if not bird.dead:
            bot.update_scores()
            print("Game %d score %d" %  (bot.gameCNT, bird.score))
        bird.y = 200
        bird.dead = False
        bird.score = 0
        bird.vy = 0
        reset_pipes()


def update():
    update_pipes()
    update_bird()


def on_key_down():
    if not bird.dead:
        bird.vy = -FLAP_STRENGTH


def draw():
    screen.blit('background', (0, 0))
    pipe_top.draw()
    pipe_bottom.draw()
    bird.draw()
    screen.draw.text(
        str(bird.score),
        color='white',
        midtop=(WIDTH // 2, 10),
        fontsize=70,
        shadow=(1, 1)
    )
    screen.draw.text(
        "Best: {}".format(storage['highscore']),
        color=(200, 170, 0),
        midbottom=(WIDTH // 2, HEIGHT - 10),
        fontsize=30,
        shadow=(1, 1)
    )


pgzrun.go()