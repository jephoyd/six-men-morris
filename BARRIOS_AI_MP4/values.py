MAIN_DISPLAY = 0
CHOOSE_COLOR_CHAR = 1
PLAYING_PHASE = 2
MOVEMENT_PHASE = 3
GAMEPLAY_REMOVE_PIECE = 4
GAMEPLAY_PLAYER_WON = 5
GAMEPLAY_PLAYER_LOSE = 6
GAMEPLAY_PLAYER_DRAW = 7

GAMEPLAY_SELECT_PIECE_TO_MOVE = 8
GAMEPLAY_SELECT_VALID_POINT = 9
GAMEPLAY_NO_VALID_MOVES = 10
GAMEPLAY_FINAL_PHASE = 11

player_human = 1
player_ai = 2
curr_player = 0
current_player = 0
piece_clicked = (0, 0)
prev_piece_clicked = (0, 0)
white_piece_clicked = False
black_piece_clicked = False
is_piece_selected = False
current_game_phase = GAMEPLAY_SELECT_PIECE_TO_MOVE
isFinal_phase = False

home = "./resources/home.png"
choose_color = "./resources/choose_color.png"
white_piece_img = "./resources/white_piece1.png"
black_piece_img = "./resources/black_piece1.png"
game_bg = "./resources/game_bg.png"
hero_black = "./resources/black_hero.png"
hero_white = "./resources/white_hero.png"

your_turn = "./resources/your_turn1.png"
opp_turn = "./resources/opp_turn.png"
your_turn2 = "./resources/your_turn2.png"
your_turn2b = "./resources/your_turn2b.png"
your_turn2c = "./resources/your_turn2c.png"
form_mill = "./resources/form_mill.png"
you_won = "./resources/you_won.png"
you_lose = "./resources/you_lose.png"


BLACK = (0, 0, 0)
LINE_WIDTH = 5
POINT_RADIUS = 20
WIDTH, HEIGHT = 1000, 600
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PLAY_AGAIN_COLOR = (64, 64, 64)
EXIT_COLOR = (32, 32, 32)

intersection_points = [
    (50, 50), (300, 50), (550, 50),                       
    (175, 175), (300, 175), (425, 175),                  
    (50, 300), (175, 300), (425, 300), (550, 300),       
    (175, 425), (300, 425), (425, 425),                   
    (50, 550), (300, 550), (550, 550)                     
]
consecutive_points = {
    ((50, 50), (300, 50), (550, 50)): None,
    ((175, 175), (300, 175), (425, 175)): None,
    ((175, 425), (300, 425), (425, 425)): None,
    ((50, 550), (300, 550), (550, 550)): None,

    ((50, 50), (50, 300), (50, 550)): None,
    ((175, 175), (175, 300), (175, 425)): None,
    ((425, 175), (425, 300), (425, 425)): None,
    ((550, 50), (550, 300), (550, 550)): None
}
point_moves = {
    (50, 50): [(300, 50), (50, 300)],
    (300, 50): [(50, 50), (300, 175), (550, 50)],
    (550, 50): [(300, 50), (550, 300)],

    (175, 175): [(300, 175), (175, 300)],
    (300, 175): [(175, 175), (300, 50), (425, 175)], 
    (425, 175): [(300, 175), (425, 300)],

    (50, 300): [(50, 50), (175, 300), (50, 550)],
    (175, 300): [(50, 300), (175, 175), (175, 425)],
    (425, 300): [(425, 175), (550, 300), (425, 425)],
    (550, 300): [(550, 50), (425, 300), (550, 550)],

    (175, 425): [(175, 300), (300, 425)],
    (300, 425): [(175, 425), (300, 550), (425, 425)],
    (425, 425): [(300, 425), (425, 300)],

    (50, 550): [(50, 300), (300, 550)],
    (300, 550): [(50, 550), (300, 425), (550, 550)],
    (550, 550): [(550, 300), (300, 550)]
}

held_pieces_by_player = {player_human: 6, player_ai: 6}
board_pieces_by_player = {
    player_human: [],
    player_ai: []
}
player_pieces_mills = {
    player_human: [],
    player_ai: []
}
player_pieces_prev_mills = {
    player_human: [],
    player_ai: []
}