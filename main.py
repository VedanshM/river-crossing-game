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
        self.speed = PLAYER_SPEED
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
        speed = BASE_SPEED_SHIP + (player.wins)*DIFF_INC
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
    global game_quit
    if game_quit:
        return
    enter_pressed = False
    fontb = pg.font.SysFont(MAIN_FONT, 60, True)
    font = pg.font.SysFont(MAIN_FONT, 40, False)
    head = fontb.render(HELP_HEAD, True, WHITE)
    hrect = head.get_rect()
    hrect.center = (WIN_SIZE[0]//2, WIN_SIZE[1]//6)
    lines_surf = []
    lines_rect = []
    prect = hrect.copy()
    prect.y += 20
    for line in HELP_MSG:
        lines_surf.append(font.render(line, False, WHITE))
        lines_rect.append(lines_surf[-1].get_rect())
        lines_rect[-1].centerx = prect.centerx
        lines_rect[-1].top = prect.bottom + 50
        prect = lines_rect[-1].copy()
    window.fill(BLACK)
    window.blit(head, hrect)
    for i in range(len(lines_rect)):
        window.blit(lines_surf[i], lines_rect[i])
    pg.display.update()

    while not(game_quit) and not(enter_pressed):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_quit = True
                return
        if pg.key.get_pressed()[pg.K_RETURN]:
            enter_pressed = True


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
    bsurf = window.copy()
    brect = window.get_rect()
    fontb = pg.font.SysFont(MAIN_FONT, 80, True)
    fontm = pg.font.SysFont(MAIN_FONT, 40, True)
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

    bsurf.blit(heading, hrect)
    bsurf.blit(scr_head, shrect)
    bsurf.blit(scr1, srect1)
    bsurf.blit(scr2, srect2)
    brect.topleft = (0, -200)

    psec = pg.time.get_ticks()
    while pg.time.get_ticks() - psec < 500:
        clock.tick(FPS)
        brect.y += 15
        window.fill(BLACK)
        window.blit(bsurf, brect)
        pg.display.update()

    while pg.time.get_ticks() - psec < ROUND_RESULT_DELAY:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_quit = True
                return


def score_display(score, round_no, player):
    font = pg.font.SysFont(MAIN_FONT, SB_POS[3]*90//100, True)
    rheading = font.render("Round {0}".format(round_no), True, BLACK)
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
    bsurf = window.copy()
    fontb = pg.font.SysFont(MAIN_FONT, 60, True)
    fontm = pg.font.SysFont(MAIN_FONT, 40, True)
    heading = fontb.render("ROUND : {0}".format(round_no), True, WHITE)
    pname = fontm.render("{0}".format(player.name), True, WHITE)
    hrect = heading.get_rect()
    prect = pname.get_rect()
    hrect.center = (WIN_SIZE[0]//2, WIN_SIZE[1]//2)
    prect.center = (WIN_SIZE[0]//2, WIN_SIZE[1]*3/4)
    bsurf.blit(heading, hrect)
    bsurf.blit(pname, prect)
    brect = bsurf.get_rect()
    brect.topleft = (0, -250)
    psec = pg.time.get_ticks()
    while pg.time.get_ticks() - psec <= 400:
        clock.tick(FPS)
        brect.y += 17
        window.fill(BLACK)
        window.blit(bsurf, brect)
        pg.display.update()
    psec = pg.time.get_ticks()
    while pg.time.get_ticks() - psec <= 1100:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_quit = True
                return


def final_standings():
    global game_quit
    if game_quit:
        return
    fontb = pg.font.SysFont(MAIN_FONT, 60, True)
    font = pg.font.SysFont(MAIN_FONT, 40, True)

    head = fontb.render("FINAL STANDINGS", True, WHITE)
    scr1 = font.render("Player 1 : {0}".format(player1.score), True, WHITE)
    scr2 = font.render("Player 2 : {0}".format(player2.score), True, WHITE)
    hscr_surf = font.render("HIGH SCORE: {0}".format(high_score), True, WHITE)
    hrect = head.get_rect()
    srect1 = scr1.get_rect()
    srect2 = scr2.get_rect()
    hscr_rect = hscr_surf.get_rect()
    hrect.center = (WIN_SIZE[0]//2, WIN_SIZE[1]//6)
    srect1.center = (WIN_SIZE[0]//2, WIN_SIZE[1]*0.5)
    srect2.center = (WIN_SIZE[0]//2, srect1.bottom + 30)
    hscr_rect.center = (WIN_SIZE[0]//2, WIN_SIZE[1]*0.95)
    winner = player1.name if player1.score > player2.score else player2.name
    if player1.score == player2.score == 0:
        msg = "No One Won !!"
    elif player1.score == player2.score:
        msg = "It's a Tie !!"
    else:
        msg = "{0} Won !!".format(winner)
    msg_surf = font.render(msg, True, WHITE)
    msg_rect = msg_surf.get_rect()
    msg_rect.center = (WIN_SIZE[0]//2, WIN_SIZE[1]*0.8)
    window.fill(BLACK)
    window.blit(head, hrect)
    window.blit(scr1, srect1)
    window.blit(scr2, srect2)
    window.blit(hscr_surf, hscr_rect)
    bsurf = window.copy()
    brect = bsurf.get_rect()
    brect.topleft = (0, 0)
    window.blit(msg_surf, msg_rect)
    pg.display.update()
    psec = pg.time.get_ticks()
    msg_vis = True
    enter_pressed = False
    while not(game_quit) and not(enter_pressed):
        clock.tick(FPS)
        if pg.time.get_ticks() - psec >= 350:
            psec = pg.time.get_ticks()
            if msg_vis:
                window.blit(bsurf, brect)
                msg_vis = False
            else:
                window.blit(msg_surf, msg_rect)
                msg_vis = True
        pg.display.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_quit = True
                return
        if pg.key.get_pressed()[pg.K_RETURN]:
            enter_pressed = True


try:
    high_score_file = open(HG_FILE, 'r')
except FileNotFoundError:
    high_score_file = open(HG_FILE, 'w')
    high_score_file.write("0")
    high_score_file.close()
    high_score_file = open(HG_FILE, 'r')

finally:
    high_score = int(high_score_file.readline())
    high_score_file.close()

pg.init()
pg.font.init()
game_quit = False
initialize()
help_page(window)
player1 = Player(1)
player2 = Player(2)
for round_no in range(1, ROUNDS_CNT+1):
    round_start(round_no, player1)
    status = round_play(round_no, player1)
    round_end(status)
    round_start(round_no, player2)
    status = round_play(round_no, player2)
    round_end(status)
    if game_quit:
        break

if player1.score > high_score:
    high_score = player1.score
if player2.score > high_score:
    high_score = player2.score

final_standings()

high_score_file = open(HG_FILE, 'w')
high_score_file.write(str(high_score))
high_score_file.close()
pg.quit()
