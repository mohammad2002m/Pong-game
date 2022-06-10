from turtle import circle
import pygame, math, time

pygame.font.init()

WHITE = (255 , 255 , 255)
BLACK = (0 , 0 , 0)
RED = (255 , 0 , 0)

WIDTH , HEIGHT = (900, 500)
FRAME_RATE = 60

PLAYER_WIDTH = 5
PLAYER_HEIGHT = 100
BALL_RADUIS = 10

SPEED = 4

WINDOW = pygame.display.set_mode((WIDTH , HEIGHT))
pygame.display.set_caption("Pong Game By Mohammad Alshareef")

PLAYER1 = pygame.Rect(30 , HEIGHT / 2 - PLAYER_HEIGHT / 2 , PLAYER_WIDTH , PLAYER_HEIGHT)
PLAYER2 = pygame.Rect(WIDTH - PLAYER_WIDTH - 30 , HEIGHT / 2 - PLAYER_HEIGHT / 2 , PLAYER_WIDTH , PLAYER_HEIGHT)

BORDER_UP = pygame.Rect(0 , 0 , WIDTH , 4)
BORDER_BOTTOM = pygame.Rect(0 , HEIGHT - 4 , WIDTH , 4)
BORDER_LEFT = pygame.Rect(0 , 0 , 4 , HEIGHT)
BORDER_RIGHT = pygame.Rect(WIDTH - 4 , 0 , 4 , HEIGHT)

BALL = pygame.draw.circle(WINDOW, BLACK , (WIDTH / 2 - BALL_RADUIS / 2 , HEIGHT / 2 - BALL_RADUIS / 2) , BALL_RADUIS , 0)

BALL_SPEED = 9 
MAX_ANGLE = 45

BallXVel = 7
BallYVel = 0

player1_score = 0
player2_score = 0

last_collide_with = -1


SCORE_FONT = pygame.font.SysFont('comicsans', 30)

def DrawAndRender():
    global PLAYER1 , PLAYER2
    WINDOW.fill(WHITE)
    pygame.draw.rect(WINDOW , BLACK , PLAYER1)
    pygame.draw.rect(WINDOW , BLACK , PLAYER2)

    pygame.draw.rect(WINDOW , BLACK , BORDER_UP)
    pygame.draw.rect(WINDOW , BLACK , BORDER_BOTTOM)
    pygame.draw.rect(WINDOW , BLACK , BORDER_LEFT)
    pygame.draw.rect(WINDOW , BLACK , BORDER_RIGHT)

    pygame.draw.circle(WINDOW, BLACK , (BALL.x , BALL.y) , BALL_RADUIS , 0)
    PLAYER1_SCORE_TEXT = SCORE_FONT.render(str(player1_score) , 1 ,  BLACK)
    PLAYER2_SCORE_TEXT = SCORE_FONT.render(str(player2_score) , 1 , BLACK)

    WINDOW.blit(PLAYER1_SCORE_TEXT , (10 , 10))
    WINDOW.blit(PLAYER2_SCORE_TEXT , (WIDTH - PLAYER1_SCORE_TEXT.get_width() - 10 , 10))
    pygame.display.update()

def ColisionDetect(BALL , OBJECT):
    def clamp(val , min , max):
        if val < min:
            return min
        elif val > max:
            return max
        else:
            return val

    ClosestX = clamp(BALL.x , OBJECT.x , OBJECT.x + OBJECT.width)
    ClosestY = clamp(BALL.y , OBJECT.y , OBJECT.y + OBJECT.height)

    return (ClosestX - BALL.x) * (ClosestX - BALL.x) + (ClosestY - BALL.y) * (ClosestY - BALL.y) <= BALL_RADUIS * BALL_RADUIS

def hitfactor(PLAYER):
    global BALL
    factor =  (PLAYER.y + PLAYER_HEIGHT / 2) - BALL.y
    factor /= (PLAYER_HEIGHT / 2)
    factor *= MAX_ANGLE
    return factor

def BallMovement(BALL):
    global PLAYER1 , PLAYER2 , BallXVel , BallYVel  , player1_score , player2_score , last_collide_with

    if ColisionDetect(BALL , PLAYER1) and last_collide_with != 1:
        last_collide_with = 1
        factor = hitfactor(PLAYER1)
        BallXVel = math.cos(math.radians(factor)) * BALL_SPEED
        BallYVel = -math.sin(math.radians(factor)) * BALL_SPEED

    elif ColisionDetect(BALL , PLAYER2) and last_collide_with != 2:
        last_collide_with = 2
        factor = hitfactor(PLAYER2)
        BallXVel = -math.cos(math.radians(factor)) * BALL_SPEED
        BallYVel = -math.sin(math.radians(factor)) * BALL_SPEED

    elif ColisionDetect(BALL , BORDER_BOTTOM) and last_collide_with != 3:
        last_collide_with = 3
        BallYVel *= -1

    elif ColisionDetect(BALL , BORDER_UP) and last_collide_with != 4:
        last_collide_with = 4
        BallYVel *= -1

    if BALL.x < 0:
        last_collide_with = -1
        player2_score += 1
        BALL.x , BALL.y = (WIDTH / 2 - BALL_RADUIS / 2 , HEIGHT / 2 - BALL_RADUIS / 2)
        PLAYER1.x , PLAYER1.y = (30 , HEIGHT / 2 - PLAYER_HEIGHT / 2)
        PLAYER2.x , PLAYER2.y = (WIDTH - PLAYER_WIDTH - 30 , HEIGHT / 2 - PLAYER_HEIGHT / 2)
        BallXVel , BallYVel = (10 , 0)
        time.sleep(1)

    if BALL.x + BALL_RADUIS > WIDTH:
        last_collide_with = -1
        player1_score += 1
        BALL.x , BALL.y = (WIDTH / 2 - BALL_RADUIS / 2 , HEIGHT / 2 - BALL_RADUIS / 2)
        PLAYER1.x , PLAYER1.y = (30 , HEIGHT / 2 - PLAYER_HEIGHT / 2)
        PLAYER2.x , PLAYER2.y = (WIDTH - PLAYER_WIDTH - 30 , HEIGHT / 2 - PLAYER_HEIGHT / 2)
        BallXVel , BallYVel = (10 , 0)
        time.sleep(1)

    if BallXVel > 0: BALL.x += math.ceil(BallXVel)
    else: BALL.x += math.floor(BallXVel)

    if BallYVel > 0: BALL.y += math.ceil(BallYVel)
    else: BALL.y += math.floor(BallYVel)



def Movement():
    KeyPressed = pygame.key.get_pressed()
    if KeyPressed[pygame.K_w] and PLAYER1.y - SPEED >= 0:
        PLAYER1.y -= SPEED
    if KeyPressed[pygame.K_s] and PLAYER1.y + SPEED + PLAYER_HEIGHT <= HEIGHT:
        PLAYER1.y += SPEED

    if KeyPressed[pygame.K_UP] and PLAYER2.y - SPEED >= 0:
        PLAYER2.y -= SPEED
    if KeyPressed[pygame.K_DOWN] and PLAYER2.y + SPEED + PLAYER_HEIGHT <= HEIGHT:
        PLAYER2.y += SPEED


def RunTheGame():

    clock = pygame.time.Clock()

    Running = True
    while (Running):
        clock.tick(FRAME_RATE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Running = False
                break

        
        #print(math.ceil(BallXVel) , math.ceil(BallYVel))
        BallMovement(BALL)
        Movement()
        DrawAndRender()


RunTheGame()
