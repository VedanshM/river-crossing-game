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
    def __init__(self, plno):
        self.speed = 10
        self.score = 0
        self.wins = 0
        self.surf = pg.image.load("turtle.png").convert_alpha()
        self.surf = pg.transform.rotozoom(self.surf, 0,
                                          PLANK_RATIO*WIN_SIZE[1] / self.surf.get_height())
        self.rect = self.surf.get_rect()
        self.rect.centerx, self.rect.y = (WIN_SIZE[0]//2, SB_POS[3])
        # self.x = (WIN_SIZE[0]-self.surf.get_height())//2
        # self.y = SB_POS[3]
        if plno == 1:
            self.ckeys = {"up": pg.K_UP, "down": pg.K_DOWN,
                          "left": pg.K_LEFT, "right": pg.K_RIGHT}
            self.name = "Player 1"
            self.visible = True
            self.rect.y += WIN_SIZE[1]*(1-PLANK_RATIO)
            self.ylimit = (SB_POS[3], self.rect.y)
        else:
            self.ckeys = {"up": pg.K_w, "down": pg.K_s,
                          "left": pg.K_a, "right": pg.K_d}
            self.name = "PLayer 2"
            self.visible = False
            self.ylimit = (
                self.rect.y, SB_POS[3] + WIN_SIZE[1]*(1-PLANK_RATIO))
            self.surf = pg.transform.scale(self.surf, 180, 1)

    def update(self, window):
        if not self.visible:
            return
        keys = pg.key.get_pressed()

        if keys[self.ckeys["up"]]:
            self.rect.y -= self.speed
        if keys[self.ckeys["down"]]:
            self.rect.y += self.speed
        if keys[self.ckeys["left"]]:
            self.rect.x -= self.speed
        if keys[self.ckeys["right"]]:
            self.rect.x += self.speed

        if(self.rect.left < 0):
            self.rect.left = 0
        if self.rect.right > WIN_SIZE[0]:
            self.rect.right = WIN_SIZE[0]
        if(self.rect.y < self.ylimit[0]):
            self.rect.y = self.ylimit[0]
        if self.rect.y > self.ylimit[1]:
            self.rect.y = self.ylimit[1]
        window.blit(self.surf, self.rect)

    def hit(self):
        pass


class Wall(pg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.surf = pg.image.load("wall.png").convert_alpha()
        self.surf = pg.transform.scale(self.surf,
                                       (int(LAND_POS[0][3]), int(LAND_POS[0][3])))
        self.rect = self.surf.get_rect()
        self.rect.topleft = pos

    def update(self, window):
        window.blit(self.surf, self.rect)

    @staticmethod
    def gen(row, round_no):
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
        # self.x = pos[0]
        # self.y = pos[1]
        self.speed = speed
        self.dir = 1
        self.surf = pg.image.load("ship.png").convert_alpha()
        self.surf = pg.transform.rotozoom(self.surf, 0, 0.8 *
                                          3*PLANK_RATIO*WIN_SIZE[1] / self.surf.get_height())
        self.rect = self.surf.get_rect()
        self.rect.topleft = pos
        if random.randint(0, 1) == 1:
            self.dir = -1
            self.surf = pg.transform.flip(self.surf, True, False)

    @property
    def velocity(self):
        return self.dir * self.speed

    def update(self, window):
        self.rect.x += self.velocity
        if self.rect.left < 0:
            self.rect.left = 0
            self.dir = 1
            self.surf = pg.transform.flip(self.surf, True, False)
        elif self.rect.right > WIN_SIZE[0]:
            self.rect.right = WIN_SIZE[0]
            self.dir = -1
            self.surf = pg.transform.flip(self.surf, True, False)
        window.blit(self.surf, self.rect)

    @staticmethod
    def gen(row, round_no, player):
        speed = 15 + (player.wins)*6 - round_no
        if speed < 5:
            speed = 5
        no_of_elements = 2
        if round_no == 3 and player.wins == 2:
            no_of_elements += 1
        elem = []
        pos = [0, SB_POS[3] + (5*row-4)*PLANK_RATIO*WIN_SIZE[1]+10]
        for i in range(no_of_elements):
            pos[0] = random.randint(1, WIN_SIZE[0] - 10)
            elem.append(Ship(pos, speed))
        return elem


def round_play(round_no, player):
    global game_quit
    if(game_quit):
        return
    walls = pg.sprite.Group()
    ships = pg.sprite.Group()

    for i in range(LAND_CNT):
        tmp = Wall.gen(i+1, round_no)
        for j in tmp:
            walls.add(j)
    for i in range(RIV_CNT):
        tmp = Ship.gen(i+1, round_no, player)
        for j in tmp:
            ships.add(j)

    while not game_quit:
        clock.tick(FPS)
        draw_bg(window)
        draw_sb(window)
        walls.update(window)
        ships.update(window)
        player.update(window)

        if pg.sprite.spritecollide(player, walls, 0) or pg.sprite.spritecollide(player, ships, 0):
            player.hit()
            return False

        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_quit = True
                break
        pg.display.update()
    return True
    # pg.quit()


def round_end(status):
    global game_quit
    if game_quit:
        return
    window.fill(BLACK)
    font1 = pg.font.SysFont('comicsans', 60, True)
    if status:
        heading = font1.render(WIN_MSG, True, WHITE)
    else:
        heading = font1.render(LOSE_MSB, True, WHITE)
    headrect = heading.get_rect()
    headrect.center = (WIN_SIZE[0]//2, WIN_SIZE[1]//2)
    window.blit(heading, headrect)
    pg.display.update()
    ctime = pg.time.get_ticks()
    while pg.time.get_ticks() - ctime < ROUND_RESULT_DELAY:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_quit = True
                return


def help_page(window):
    pass


pg.init()
pg.font.init()
game_quit = False
initialize()
help_page(window)
player1 = Player(1)
no_of_rounds = 1
for round_no in range(1, no_of_rounds+1):
    status = round_play(round_no, player1)
    round_end(status)
pg.quit()
