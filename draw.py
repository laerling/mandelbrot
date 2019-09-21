import pygame
import random

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
    maybeQuit()
    pygame.display.update()

def maybeQuit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

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
    "commit surface and idle until program is quit"
    global _sf
    global _clock
    _game_display.blit(_sf, (0,0))
    while True:
        maybeQuit()
        pygame.display.update()
        _clock.tick(60)

def randomColor():
    return (random.randint(0,255),
            random.randint(0,255),
            random.randint(0,255))
