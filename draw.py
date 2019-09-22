import pygame
import random
from enum import Enum

# define variables
black = (0,0,0)
white = (255,255,255)

def init(width, height):
    global _game_display
    global _clock
    global _sf

    # init game
    pygame.init()
    _game_display = pygame.display.set_mode((width,height))
    _clock = pygame.time.Clock()

    # init drawing surface
    _sf = pygame.Surface((width, height))
    _sf.fill(white)

def update():
    global _game_display
    _game_display.blit(_sf, (0,0))
    pygame.display.update()

class UserAction(Enum):
    RESET = 0
    PAUSE = 1
    JULIA = 2
    ZOOM_IN = 3
    ZOOM_OUT = 4
    MOVE_UP = 5
    MOVE_DOWN = 6
    MOVE_LEFT = 7
    MOVE_RIGHT = 8
    INCREASE_DEPTH = 9
    DECREASE_DEPTH = 10
    JULIA_MOVE_UP = 11
    JULIA_MOVE_DOWN = 12
    JULIA_MOVE_LEFT = 13
    JULIA_MOVE_RIGHT = 14

def getUserAction():
    "Return pygame events if they are valid user actions"
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_q:
                pygame.quit()
                quit()
            elif e.key == pygame.K_SPACE:
                return UserAction.PAUSE
            elif e.key == pygame.K_j:
                return UserAction.JULIA
            elif e.key == pygame.K_r:
                return UserAction.RESET
            elif e.key == pygame.K_PLUS:
                return UserAction.ZOOM_IN
            elif e.key == pygame.K_MINUS:
                return UserAction.ZOOM_OUT
            elif e.key == pygame.K_UP:
                return UserAction.MOVE_UP
            elif e.key == pygame.K_DOWN:
                return UserAction.MOVE_DOWN
            elif e.key == pygame.K_LEFT:
                return UserAction.MOVE_LEFT
            elif e.key == pygame.K_RIGHT:
                return UserAction.MOVE_RIGHT
            elif e.key == pygame.K_PERIOD:
                return UserAction.INCREASE_DEPTH
            elif e.key == pygame.K_COMMA:
                return UserAction.DECREASE_DEPTH
            elif e.key == pygame.K_w:
                return UserAction.JULIA_MOVE_UP
            elif e.key == pygame.K_s:
                return UserAction.JULIA_MOVE_DOWN
            elif e.key == pygame.K_a:
                return UserAction.JULIA_MOVE_LEFT
            elif e.key == pygame.K_d:
                return UserAction.JULIA_MOVE_RIGHT
    return None

def pixel(pos, color=black, update_display=True):
    global _sf
    _sf.set_at(pos, color)
    if update_display:
        update()

def rectangle(pos_from, pos_to, color=black, update_display=True):
    global _sf
    rect = pygame.Rect(pos_from,
                       (abs(pos_to[0] - pos_from[0]),
                        abs(pos_to[1] - pos_from[1])))
    _sf.fill(color, rect)
    if update_display:
        update()

def partial_square(pos, max_size, shrink_f=1,
                   color=black, update_display=True):
    global _sf
    size = max(max_size / max(shrink_f, 1), 1)
    pos_from = (pos[0] - size / 2, pos[1] - size / 2)
    pos_to = (pos[0] + size / 2, pos[1] + size / 2)
    rectangle(pos_from, pos_to, color=color, update_display=update_display)

def idle():
    "commit surface and idle until next user action"
    global _sf
    global _clock
    _game_display.blit(_sf, (0,0))
    while True:
        user_action = getUserAction()
        if user_action != None:
            return user_action
        pygame.display.update()
        _clock.tick(60)

def randomColor():
    return (random.randint(0,255),
            random.randint(0,255),
            random.randint(0,255))
