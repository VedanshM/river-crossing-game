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
        self.no = plno
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
            self.rect.y += WIN_SIZE[1]*(1-PLANK_RATIO)
            self.ylimit = (SB_POS[3], self.rect.y)
        else:
            self.ckeys = {"up": pg.K_w, "down": pg.K_s,
                          "left": pg.K_a, "right": pg.K_d}
            self.name = "PLayer 2"
            self.ylimit = (
                self.rect.y, SB_POS[3] + WIN_SIZE[1]*(1-PLANK_RATIO))
            self.surf = pg.transform.rotozoom(self.surf, 180, 1)
        self.orig_rect = self.rect.copy()

    def update(self, window):
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

    def dist_cover(self):
        d = self.rect.y - self.orig_rect.y
        if d < 0:
            return -d
        return d

    def hit(self):
        pass

    def pos_reset(self):
        self.rect = self.orig_rect.copy()


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

    @classmethod
    def height(self):
        return 2*PLANK_RATIO*WIN_SIZE[1]

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

    @classmethod
    def height(self):
        return 3*PLANK_RATIO*WIN_SIZE[1]

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
        speed = 15 + (player.wins)*6
        print(round_no)
        print(speed)
        no_of_elements = 2
        if round_no == 3 and player.wins == 2:
            no_of_elements += 1
        elem = []
        pos = [0, SB_POS[3] + (5*row-4)*PLANK_RATIO*WIN_SIZE[1]+10]
        for _ in range(no_of_elements):
            pos[0] = random.randint(1, WIN_SIZE[0] - 10)
            elem.append(Ship(pos, speed))
        return elem


def help_page(window):
    pass


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
    player.pos_reset()
    status = True
    score = 0
    check_pt = 0
    next_check_pt = check_pt + Ship.height()
    psec = pg.time.get_ticks()

    while not game_quit:
        clock.tick(FPS)
        draw_bg(window)
        draw_sb(window)
        walls.update(window)
        ships.update(window)
        player.update(window)

        if player.dist_cover() > next_check_pt:
            check_pt = next_check_pt
            if next_check_pt - check_pt == Wall.height():
                score += WALL_POINTS
                next_check_pt = check_pt + Ship.height()
            else:
                score += RIV_POINTS
                next_check_pt = check_pt + Wall.height()

        if pg.time.get_ticks() - psec >= 1000:
            psec = pg.time.get_ticks()
            score -= TM_POINTS
        score_display(score, round_no, player)

        if pg.sprite.spritecollide(player, walls, 0) or pg.sprite.spritecollide(player, ships, 0):
            player.hit()
            status = False
            break
        if player.dist_cover() >= TRACK_LEN:
            break

        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_quit = True
                break
        pg.display.update()
    if status:
        player.score += score
        player.wins += 1
    return status
    # pg.quit()


def round_end(status):
    global game_quit
    if game_quit:
        return
    window.fill(BLACK)
    fontb = pg.font.SysFont('comicsans', 80, True)
    fontm = pg.font.SysFont('comicsans', 40, True)
    heading = fontb.render(WIN_MSG if status else LOSE_MSB,
                           True, WHITE)
    scr_head = fontm.render("Scores", True, WHITE)
    scr1 = fontm.render("Player 1 : {0}".format(player1.score), True, WHITE)
    scr2 = fontm.render("Player 2 : {0}".format(player2.score), True, WHITE)
    hrect = heading.get_rect()
    shrect = scr_head.get_rect()
    srect1 = scr1.get_rect()
    srect2 = scr2.get_rect()
    hrect.center = (WIN_SIZE[0]//2, WIN_SIZE[1]*0.4)
    shrect.center = (WIN_SIZE[0]//2, WIN_SIZE[1]*0.6)
    srect1.center = (WIN_SIZE[0]//2, WIN_SIZE[1]*0.7)
    srect2.center = (WIN_SIZE[0]//2, srect1.bottom + 30)

    window.blit(heading, hrect)
    window.blit(scr_head, shrect)
    window.blit(scr1, srect1)
    window.blit(scr2, srect2)
    pg.display.update()
    ctime = pg.time.get_ticks()
    while pg.time.get_ticks() - ctime < ROUND_RESULT_DELAY:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_quit = True
                return


def score_display(score, round_no, player):
    font = pg.font.SysFont('comicsans', SB_POS[3]*90//100, True)
    rheading = font.render("Round {0}".format(player.no), True, BLACK)
    rheadrect = rheading.get_rect()
    rheadrect.left, rheadrect.centery = (0, SB_POS[3]//2)
    window.blit(rheading, rheadrect)

    pheading = font.render(player.name, True, BLACK)
    pheadrect = pheading.get_rect()
    pheadrect.center = (WIN_SIZE[0]//2, SB_POS[3]//2)
    window.blit(pheading, pheadrect)

    sheading = font.render("Score: {0}".format(score), True, BLACK)
    sheadrect = sheading.get_rect()
    sheadrect.right, sheadrect.centery = (WIN_SIZE[0]-2, SB_POS[3]//2)
    window.blit(sheading, sheadrect)


def round_start(round_no, player):
    global game_quit
    if game_quit:
        return
    window.fill(BLACK)
    fontb = pg.font.SysFont('comicsans', 60, True)
    fontm = pg.font.SysFont('comicsans', 40, True)
    heading = fontb.render("ROUND : {0}".format(round_no), True, WHITE)
    pname = fontm.render("{0}".format(player.name), True, WHITE)
    hrect = heading.get_rect()
    prect = pname.get_rect()
    hrect.center = (WIN_SIZE[0]//2, WIN_SIZE[1]//2)
    prect.center = (WIN_SIZE[0]//2, WIN_SIZE[1]*0.75)
    window.blit(heading, hrect)
    window.blit(pname, prect)
    pg.display.update()
    pg.time.delay(1500)


pg.init()
pg.font.init()
game_quit = False
initialize()
help_page(window)
player1 = Player(1)
player2 = Player(2)
no_of_rounds = 3
for round_no in range(1, no_of_rounds+1):
    round_start(round_no, player1)
    status = round_play(round_no, player1)
    round_end(status)
    round_start(round_no, player2)
    status = round_play(round_no, player2)
    round_end(status)

pg.quit()
