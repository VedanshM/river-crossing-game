import pygame as pg
from config import *

window = pg.display.set_mode(WIN_SIZE)
pg.display.set_caption(WIN_CAPTION)
clock = pg.time.Clock()


def draw_bg(window):
    window.fill(LBLUE)
    pg.draw.rect(window, BLACK, HEAD_POS)
    pg.draw.rect(window, BLACK, FOOT_POS)

    for i in LAND_POS:
        pg.draw.rect(window, BROWN, i)


class Wall(pg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.x = pos[0]
        self.y = pos[1]
        self.surf = pg.image.load("wall.png").convert_alpha()
        self.rect = self.surf.get_rect()

    def update(self, window):
        window.blit(self.surf, (self.x, self.y))


draw_bg(window)
walls = pg.sprite.Group()
for i in WALL_POS:
    walls.add(Wall(i))
for i in walls:
    i.update(window)
pg.display.update()

game_quit = False
# pg.time.delay(10000)

while not game_quit:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            game_quit = True
            break
