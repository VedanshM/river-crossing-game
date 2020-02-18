FPS = 25
ROUNDS_CNT = 3


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LBLUE = (18, 218, 224)
BROWN = (209, 84, 6)

MAIN_FONT = 'comicsans'
HG_FILE = 'hg_score.txt'
SB_POS = (0, 0, 1500, 50)
WIN_SIZE = (1500, 800)
WIN_CAPTION = "The Game"
PLANK_RATIO = 0.05
HEAD_POS = (0, SB_POS[3]+0,
            WIN_SIZE[0], WIN_SIZE[1]*PLANK_RATIO)
FOOT_POS = (0, SB_POS[3]+WIN_SIZE[1]*(1-PLANK_RATIO),
            WIN_SIZE[0], WIN_SIZE[1]*PLANK_RATIO)
RIV_CNT = 4
LAND_CNT = 3
LAND_POS = [
    (0, SB_POS[3] + WIN_SIZE[1]*PLANK_RATIO*(4),
     WIN_SIZE[0], WIN_SIZE[1]*PLANK_RATIO*2),
    (0, SB_POS[3]+WIN_SIZE[1]*PLANK_RATIO*(9),
     WIN_SIZE[0], WIN_SIZE[1]*PLANK_RATIO*2),
    (0, SB_POS[3]+WIN_SIZE[1]*PLANK_RATIO*(14),
     WIN_SIZE[0], WIN_SIZE[1]*PLANK_RATIO*2),
]

WALL_POINTS = 5
RIV_POINTS = 10
TM_POINTS = 1
DIFF_INC = 6
BASE_SPEED_SHIP = 15
PLAYER_SPEED = 10
TRACK_LEN = int((1-PLANK_RATIO)*WIN_SIZE[1])


WIN_MSG = "ROUND CLEARED!!"
LOSE_MSB = "ROUND FAILED!"
ROUND_RESULT_DELAY = 2500

HELP_HEAD = "Welcome to {0}".format(WIN_CAPTION)
HELP_MSG = [
    "Instructions",
    "Cross the river and the lands escaping all the obstacles",
    "Player 1 control keys: Arrow Keys",
    "Player 2 control keys: WASD",
    "",
    "Finish as fast as you can",
    "Note: If you win difficulty increases in next round",
    "Press ENTER to continue..."
]
