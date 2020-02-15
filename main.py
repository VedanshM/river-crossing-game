import pygame as pg
import random
from config import *

window = None
clock = None


def initialize():
    global window
    global clock
    window = pg.display.set_mode((WIN_SIZE[0], WIN_SIZE[1]+SB_POS[3]))
    pg.display.set_caption(WIN_CAPTION)
    clock = pg.time.Clock()


def draw_sb(window):
    pg.draw.rect(window, WHITE, SB_POS)


def draw_bg(window):
    window.fill(LBLUE)
    pg.draw.rect(window, BLACK, HEAD_POS)
    pg.draw.rect(window, BLACK, FOOT_POS)

    for i in LAND_POS:
        pg.draw.rect(window, BROWN, i)


class Player(pg.sprite.Sprite):
    def __init__(self):
        pass

    pass


class Wall(pg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.x = pos[0]
        self.y = pos[1]
        self.surf = pg.image.load("wall.png").convert_alpha()
        self.surf = pg.transform.scale(self.surf,
                                       (int(LAND_POS[0][3]), int(LAND_POS[0][3])))
        self.rect = self.surf.get_rect()

    def update(self, window):
        window.blit(self.surf, (self.x, self.y))

    @staticmethod
    def walls_gen(row, round_no):
        if round_no == 1:
            no_of_walls = random.randint(3, 4)
        elif round_no == 2:
            no_of_walls = random.randint(3, 5)
        else:
            no_of_walls = random.randint(4, 5)
        walls = []
        poss = list(range(5, 95, 10))

        pos = []
        while len(pos) < no_of_walls:
            pos.append(poss[random.randint(0, len(poss) - 1)]
                       * WIN_SIZE[0]//100)
            pos = list(set(pos))
        # print(row)
        # print(pos)
        for i in pos:
            walls.append(
                Wall((i, SB_POS[3] + (PLANK_RATIO*(5*row-1))*WIN_SIZE[1])))
        return walls


class Ship(pg.sprite.Sprite):
    def __init__(self, pos, speed):
        super().__init__()
        self.x = pos[0]
        self.y = pos[1]
        self.speed = speed
        self.dir = 1 if random.randint(0, 1) == 1 else -1
        self.surf = pg.image.load("ship.png").convert_alpha()
        self.surf = pg.transform.rotozoom(self.surf, 0, 0.8 *
                                          3*PLANK_RATIO*WIN_SIZE[1] / self.surf.get_height())
        self.rect = self.surf.get_rect()

    @property
    def velocity(self):
        return self.dir * self.speed

    def update(self, window):
        self.x += self.velocity
        if self.x <= 0:
            self.x = 0
            self.dir = 1
            self.surf = pg.transform.flip(self.surf, True, False)
        elif self.x + self.surf.get_width() >= WIN_SIZE[0]:
            self.x = WIN_SIZE[0] - self.surf.get_width()
            self.dir = -1
            self.surf = pg.transform.flip(self.surf, True, False)
        # print(self.x)
        # print(self.velocity)
        window.blit(self.surf, (self.x, self.y))

    @staticmethod
    def ships_gen(row, round_no):

        pass


def round_setup(round_no, turn):
    draw_bg(window)
    draw_sb(window)
    walls = pg.sprite.Group()

    for i in range(LAND_CNT):
        tmp = Wall.walls_gen(i+1, round_no)
        for j in tmp:
            walls.add(j)
    for i in walls:
        i.update(window)
    pg.display.update()
    game_quit = False
    ship1 = Ship((900, 300), 15)

    while not game_quit:
        clock.tick(FPS)
        draw_bg(window)
        draw_sb(window)
        for i in walls:
            i.update(window)
        ship1.update(window)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_quit = True
                break
        pg.display.update()
    pg.quit()


initialize()
round_setup(1, 0)
