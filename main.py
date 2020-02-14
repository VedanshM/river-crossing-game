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


draw_bg(window)
pg.display.update()

game_quit = False
# pg.time.delay(10000)

while not game_quit:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            game_quit = True
            break
