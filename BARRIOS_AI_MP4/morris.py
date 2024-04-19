import sys
import values
import pygame

from ai import ai_moves

def initialize_game():
    pygame.init()
    screen = pygame.display.set_mode((values.WIDTH, values.HEIGHT))
    pygame.display.set_caption("Six Men's Morris")
    font = pygame.font.Font(None, 36)
    return screen

screen = initialize_game()
current_phase = values.MAIN_DISPLAY

def draw_button(screen, x, y, width, height, b_color, b_thickness):
    pygame.draw.rect(screen, b_color, (x, y, width, height), b_thickness)

def display(mouse_x, mouse_y):
    main_background = pygame.image.load(values.home)
    scaled_background = pygame.transform.scale(main_background, (values.WIDTH, values.HEIGHT))
    screen.blit(scaled_background, (0, 0))

    button_width, button_height = 300, 40
    button_x = (values.WIDTH - button_width) // 2
    button_y = 510

    draw_button(screen, button_x, button_y, button_width, button_height, (0, 0, 0), 1)

    if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
        return values.CHOOSE_COLOR_CHAR

    return values.MAIN_DISPLAY

def chooseColor(mouse_x, mouse_y):
    background_image = pygame.image.load(values.choose_color)
    background_image = pygame.transform.scale(background_image, (values.WIDTH, values.HEIGHT))
    screen.blit(background_image, (0, 0))

    button_width = 300
    button_height = 400
    white_button_x = 600
    black_button_x = 100
    button_y = 125

    start_button_width = 300
    start_button_height = 40
    start_button_x = (values.WIDTH - start_button_width) // 2
    start_button_y = 530

    white_piece = pygame.image.load(values.hero_white)
    white_piece = pygame.transform.scale(white_piece, (button_width, button_height))
    black_piece = pygame.image.load(values.hero_black)
    black_piece = pygame.transform.scale(black_piece, (button_width, button_height))

    pygame.draw.rect(screen, (0, 0, 0), (start_button_x, start_button_y, start_button_width, start_button_height), 1)

    if white_button_x <= mouse_x <= white_button_x + button_width and button_y <= mouse_y <= button_y + button_height:
        if values.white_piece_clicked:
            values.white_piece_clicked = False

        elif values.black_piece_clicked: 
            values.black_piece_clicked = False
            values.white_piece_clicked = True

        else:
            values.white_piece_clicked = True

    if black_button_x <= mouse_x <= black_button_x + button_width and button_y <= mouse_y <= button_y + button_height:
        if values.black_piece_clicked:
            values.black_piece_clicked = False

        elif values.white_piece_clicked: 
            values.white_piece_clicked = False
            values.black_piece_clicked = True

        else:
            values.black_piece_clicked = True
        
    if values.white_piece_clicked:
        screen.blit(pygame.transform.scale(white_piece, (button_width + 40, button_height + 40)), (white_button_x - 10, button_y - 10))
    elif not values.white_piece_clicked:
        screen.blit(white_piece, (white_button_x, button_y))

    if values.black_piece_clicked:
        screen.blit(pygame.transform.scale(black_piece, (button_width + 40, button_height + 40)), (black_button_x - 10, button_y - 10))
    elif not values.black_piece_clicked:
        screen.blit(black_piece, (black_button_x, button_y))

    if values.white_piece_clicked or values.black_piece_clicked:
        pygame.draw.rect(screen, (0, 255, 0), (start_button_x, start_button_y, start_button_width, start_button_height), 1)
        if start_button_x <= mouse_x <= start_button_x + start_button_width and start_button_y <= mouse_y <= start_button_y + start_button_height:
            if values.white_piece_clicked:
                values.current_player = values.player_human
                return values.PLAYING_PHASE, values.player_human
            elif values.black_piece_clicked:
                values.current_player = values.player_ai
                return values.PLAYING_PHASE, values.player_ai
    else:
        pygame.draw.rect(screen, (0, 0, 0), (start_button_x, start_button_y, start_button_width, start_button_height), 1)
    return values.CHOOSE_COLOR_CHAR, 0

def start(mouse_x, mouse_y, curr_player, current_phase):
    board(current_phase, curr_player)
    curr_board()
    
    if values.held_pieces_by_player[curr_player] > 0:
        if curr_player == values.current_player:
            available_moves = check_moves()
            availmoves()

            for point in values.intersection_points:
                distance = ((mouse_x - point[0]) ** 2 + (mouse_y - point[1]) ** 2) ** 0.5
                if distance <= values.POINT_RADIUS:
                    if point in available_moves:
                        board(current_phase, curr_player)
                        curr_board()
                        placePieceOnBoard(curr_player, point)

                        if check_points(curr_player):
                            
                            if newmill_formed(curr_player):
                                values.piece_clicked = (0, 0)
                                values.prev_piece_clicked = (0, 0)
                                values.is_piece_selected = False
                                return values.GAMEPLAY_REMOVE_PIECE, curr_player
                        else:
                            values.player_pieces_mills[curr_player] = []
                            values.player_pieces_prev_mills[curr_player] = []
                                
                        winner = check_winner(curr_player)
                        if winner != 0:
                            if winner == values.current_player:
                                return values.GAMEPLAY_PLAYER_WON, winner
                            else:
                                return values.GAMEPLAY_PLAYER_LOSE, curr_player
                        
                        curr_player = values.player_ai if curr_player == values.player_human else values.player_human
                        board(current_phase, curr_player)
                        curr_board()
                        availmoves()

                        if values.held_pieces_by_player[values.player_human] > 0 or values.held_pieces_by_player[values.player_ai] > 0:
                            pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (1000, 1)}))
                            return values.PLAYING_PHASE, curr_player
                        else:
                            pygame.time.wait(1000)
                            board(values.current_game_phase, curr_player)
                            curr_board()
                            return values.MOVEMENT_PHASE, curr_player
                    else:
                        pygame.time.wait(1000)
                        board(current_phase, curr_player)
                        curr_board()
                        availmoves()
                        return values.PLAYING_PHASE, curr_player
        else:

            return_value = ai_moves(values.PLAYING_PHASE, curr_player)
            placePieceOnBoard(curr_player, return_value)

            if check_points(curr_player):
                
                if newmill_formed(curr_player):
                    values.piece_clicked = (0, 0)
                    values.prev_piece_clicked = (0, 0)
                    values.is_piece_selected = False
                    return values.GAMEPLAY_REMOVE_PIECE, curr_player
            else:
                values.player_pieces_mills[curr_player] = []
                values.player_pieces_prev_mills[curr_player] = []
                    

            winner = check_winner(curr_player)
            if winner != 0:
                if winner == values.current_player:
                    return values.GAMEPLAY_PLAYER_WON, winner
                else:
                    return values.GAMEPLAY_PLAYER_LOSE, curr_player
            
            curr_player = values.player_ai if curr_player == values.player_human else values.player_human
            board(current_phase, curr_player)
            curr_board()
            availmoves()

            if values.held_pieces_by_player[values.player_human] > 0 or values.held_pieces_by_player[values.player_ai] > 0:
                return values.PLAYING_PHASE, curr_player
            else:
                pygame.time.wait(1000)
                board(values.current_game_phase, curr_player)
                curr_board()
                return values.MOVEMENT_PHASE, curr_player

        return values.PLAYING_PHASE, curr_player
    else:
        pygame.time.wait(1000)
        board(values.current_game_phase, curr_player)
        curr_board()
        return values.MOVEMENT_PHASE, curr_player

def second_phase(mouse_x, mouse_y, curr_player):
    board(values.current_game_phase, curr_player)

    if curr_player == values.player_human:
        opponent_player = values.player_ai
    elif curr_player == values.player_ai:
        opponent_player = values.player_human     

    if len(values.board_pieces_by_player[curr_player]) == 3 and len(values.board_pieces_by_player[opponent_player]) == 3:
        pygame.time.wait(1000)
        board(values.current_game_phase, curr_player)
        curr_board()
        availmoves()
        return values.GAMEPLAY_FINAL_PHASE, curr_player
    
    else:
        if curr_player == values.current_player:
            curr_player_pieces = set(values.board_pieces_by_player[curr_player])
            for piece in curr_player_pieces:
                piece_distance = ((mouse_x - piece[0]) ** 2 + (mouse_y - piece[1]) ** 2) ** 0.5
                if piece_distance <= values.POINT_RADIUS:
                    values.piece_clicked = piece

                    if values.prev_piece_clicked == values.piece_clicked:
                        values.prev_piece_clicked = (0, 0)
                        values.is_piece_selected = False
                    
                    elif values.is_piece_selected and values.prev_piece_clicked != values.piece_clicked:
                        values.prev_piece_clicked = values.piece_clicked
                        values.is_piece_selected = True
                    
                    else:
                        values.prev_piece_clicked = values.piece_clicked
                        values.is_piece_selected = True

            if not values.is_piece_selected:
                values.current_game_phase = values.GAMEPLAY_SELECT_PIECE_TO_MOVE
                board(values.current_game_phase, curr_player)    
                curr_board()

            if values.is_piece_selected:
                curr_player_valid_moves = checkPieceValidMoves(values.piece_clicked, curr_player, opponent_player)
                if curr_player_valid_moves:
                    values.current_game_phase = values.GAMEPLAY_SELECT_VALID_POINT
                    board(values.current_game_phase, curr_player)

                    for point in curr_player_valid_moves:
                        pygame.draw.circle(screen, values.GREEN, point, 15, width=5) 

                    for curr_player_move in curr_player_valid_moves:
                        player_move_distance = ((mouse_x - curr_player_move[0]) ** 2 + (mouse_y - curr_player_move[1]) ** 2) ** 0.5
                        if player_move_distance <= values.POINT_RADIUS:
                            values.board_pieces_by_player[curr_player][values.board_pieces_by_player[curr_player].index(values.piece_clicked)] = curr_player_move
                            board(values.current_game_phase, curr_player)
                            curr_board()

                            if check_points(curr_player):

                                if newmill_formed(curr_player):
                                    values.piece_clicked = (0, 0)
                                    values.prev_piece_clicked = (0, 0)
                                    values.is_piece_selected = False
                                    return values.GAMEPLAY_REMOVE_PIECE, curr_player
                            else:
                                values.player_pieces_mills[curr_player] = []
                                values.player_pieces_prev_mills[curr_player] = []

                            winner = check_winner(curr_player)
                            if winner != 0:
                                if winner == values.current_player:
                                    return values.GAMEPLAY_PLAYER_WON, winner
                                else:
                                    return values.GAMEPLAY_PLAYER_LOSE, curr_player
        
                            if len(values.board_pieces_by_player[curr_player]) == 3 and len(values.board_pieces_by_player[opponent_player]) == 3:
                                pygame.time.wait(1000)  

                                pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (1000, 1)}))
                                curr_player = values.player_ai if curr_player == values.player_human else values.player_human
                                values.current_game_phase = values.GAMEPLAY_SELECT_PIECE_TO_MOVE
                                values.piece_clicked = (0, 0)
                                values.prev_piece_clicked = (0, 0)
                                values.is_piece_selected = False

                                board(values.current_game_phase, curr_player)
                                curr_board()
                                return values.GAMEPLAY_FINAL_PHASE, curr_player
                            else:
                                pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (1000, 1)}))
                                curr_player = values.player_ai if curr_player == values.player_human else values.player_human
                                values.current_game_phase = values.GAMEPLAY_SELECT_PIECE_TO_MOVE
                                values.piece_clicked = (0, 0)
                                values.prev_piece_clicked = (0, 0)
                                values.is_piece_selected = False
                                
                                board(values.current_game_phase, curr_player)
                                curr_board()
                                return values.MOVEMENT_PHASE, curr_player
                else:
                    values.current_game_phase = values.GAMEPLAY_NO_VALID_MOVES
                    board(values.current_game_phase, curr_player)
        else:
            return_piece, return_move = ai_moves(values.MOVEMENT_PHASE, curr_player)
            values.board_pieces_by_player[curr_player][values.board_pieces_by_player[curr_player].index(return_piece)] = return_move
            board(values.current_game_phase, curr_player)
            curr_board()

            if check_points(curr_player):
                if newmill_formed(curr_player):
                    values.piece_clicked = (0, 0)
                    values.prev_piece_clicked = (0, 0)
                    values.is_piece_selected = False
                    return values.GAMEPLAY_REMOVE_PIECE, curr_player
            else:
                values.player_pieces_mills[curr_player] = []
                values.player_pieces_prev_mills[curr_player] = []

            winner = check_winner(curr_player)
            if winner != 0:
                if winner == values.current_player:
                    return values.GAMEPLAY_PLAYER_WON, winner
                else:
                    return values.GAMEPLAY_PLAYER_LOSE, curr_player

            if len(values.board_pieces_by_player[curr_player]) == 3 and len(values.board_pieces_by_player[opponent_player]) == 3:
                pygame.time.wait(700)  

                pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (1000, 1)}))
                curr_player = values.player_ai if curr_player == values.player_human else values.player_human
                values.current_game_phase = values.GAMEPLAY_SELECT_PIECE_TO_MOVE
                values.piece_clicked = (0, 0)
                values.prev_piece_clicked = (0, 0)
                values.is_piece_selected = False

                board(values.current_game_phase, curr_player)
                curr_board()
                return values.GAMEPLAY_FINAL_PHASE, curr_player
            else:
                pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (1000, 1)}))
                curr_player = values.player_ai if curr_player == values.player_human else values.player_human
                values.current_game_phase = values.GAMEPLAY_SELECT_PIECE_TO_MOVE
                values.piece_clicked = (0, 0)
                values.prev_piece_clicked = (0, 0)
                values.is_piece_selected = False
                
                board(values.current_game_phase, curr_player)
                curr_board()
                return values.MOVEMENT_PHASE, curr_player

        curr_board()
        return values.MOVEMENT_PHASE, curr_player       
    
def final_phase(mouse_x, mouse_y, curr_player):
    board(values.current_game_phase, curr_player)

    if curr_player == values.player_human:
        opponent_player = values.player_ai
    elif curr_player == values.player_ai:
        opponent_player = values.player_human

    if curr_player == values.current_player:
        curr_player_pieces = set(values.board_pieces_by_player[curr_player])
        for piece in curr_player_pieces:
            piece_distance = ((mouse_x - piece[0]) ** 2 + (mouse_y - piece[1]) ** 2) ** 0.5
            if piece_distance <= values.POINT_RADIUS:
                values.piece_clicked = piece

                if values.prev_piece_clicked == values.piece_clicked:
                    values.prev_piece_clicked = (0, 0)
                    values.is_piece_selected = False
                
                elif values.is_piece_selected and values.prev_piece_clicked != values.piece_clicked:
                    values.prev_piece_clicked = values.piece_clicked
                    values.is_piece_selected = True
                
                else:
                    values.prev_piece_clicked = values.piece_clicked
                    values.is_piece_selected = True

        if not values.is_piece_selected:
            values.current_game_phase = values.GAMEPLAY_SELECT_PIECE_TO_MOVE
            board(values.current_game_phase, curr_player)    
            curr_board()

        if values.is_piece_selected:
            curr_player_valid_moves = check_moves()
            if curr_player_valid_moves:
                values.current_game_phase = values.GAMEPLAY_SELECT_VALID_POINT
                board(values.current_game_phase, curr_player)

                for point in curr_player_valid_moves:
                    pygame.draw.circle(screen, values.GREEN, point, 15, width=5) 

                for curr_player_move in curr_player_valid_moves:
                    player_move_distance = ((mouse_x - curr_player_move[0]) ** 2 + (mouse_y - curr_player_move[1]) ** 2) ** 0.5
                    if player_move_distance <= values.POINT_RADIUS:
                        values.board_pieces_by_player[curr_player][values.board_pieces_by_player[curr_player].index(values.piece_clicked)] = curr_player_move
                        board(values.current_game_phase, curr_player)
                        curr_board()

                        if check_points(curr_player):
                 
                            if newmill_formed(curr_player):
                                values.piece_clicked = (0, 0)
                                values.prev_piece_clicked = (0, 0)
                                values.is_piece_selected = False
                                return values.GAMEPLAY_REMOVE_PIECE, curr_player
                        else:
                            values.player_pieces_mills[curr_player] = []
                            values.player_pieces_prev_mills[curr_player] = []

                        winner = check_winner(curr_player)
                        if winner != 0:
                            if winner == values.current_player:
                                return values.GAMEPLAY_PLAYER_WON, winner
                            else:
                                return values.GAMEPLAY_PLAYER_LOSE, curr_player
                        
                        pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (1000, 1)}))
                        curr_player = values.player_ai if curr_player == values.player_human else values.player_human
                        values.current_game_phase = values.GAMEPLAY_SELECT_PIECE_TO_MOVE
                        values.piece_clicked = (0, 0)
                        values.prev_piece_clicked = (0, 0)
                        values.is_piece_selected = False
                        board(values.current_game_phase, curr_player)
                        curr_board()
                        return values.GAMEPLAY_FINAL_PHASE, curr_player
            else:
                values.current_game_phase = values.GAMEPLAY_NO_VALID_MOVES
                board(values.current_game_phase, curr_player)
    else:

        return_piece, return_move = ai_moves(values.GAMEPLAY_FINAL_PHASE, curr_player)
        values.board_pieces_by_player[curr_player][values.board_pieces_by_player[curr_player].index(return_piece)] = return_move
        board(values.current_game_phase, curr_player)
        curr_board()

        if check_points(curr_player):
            
            if newmill_formed(curr_player):
                values.piece_clicked = (0, 0)
                values.prev_piece_clicked = (0, 0)
                values.is_piece_selected = False
                return values.GAMEPLAY_REMOVE_PIECE, curr_player
        else:
            values.player_pieces_mills[curr_player] = []
            values.player_pieces_prev_mills[curr_player] = []

        winner = check_winner(curr_player)
        if winner != 0:
            if winner == values.current_player:
                return values.GAMEPLAY_PLAYER_WON, winner
            else:
                return values.GAMEPLAY_PLAYER_LOSE, curr_player
        
        curr_player = values.player_ai if curr_player == values.player_human else values.player_human
        values.current_game_phase = values.GAMEPLAY_SELECT_PIECE_TO_MOVE
        values.piece_clicked = (0, 0)
        values.prev_piece_clicked = (0, 0)
        values.is_piece_selected = False
        board(values.current_game_phase, curr_player)
        curr_board()
        return values.GAMEPLAY_FINAL_PHASE, curr_player
        
    curr_board()
    return values.GAMEPLAY_FINAL_PHASE, curr_player

def board(curr_phase, curr_user):
    # Mapping of game phases to background images
    phase_to_image = {
        values.PLAYING_PHASE: values.your_turn,
        values.MOVEMENT_PHASE: values.your_turn2,
        values.GAMEPLAY_SELECT_PIECE_TO_MOVE: values.your_turn2,
        values.GAMEPLAY_SELECT_VALID_POINT: values.your_turn2b,
        values.GAMEPLAY_NO_VALID_MOVES: values.your_turn2c,
        values.GAMEPLAY_REMOVE_PIECE: values.form_mill,
        values.GAMEPLAY_PLAYER_WON: values.you_won,
        values.GAMEPLAY_PLAYER_LOSE: values.you_lose,
    }

    # Default background for opponent's turn
    default_background = values.opp_turn if curr_user != values.current_player else values.game_bg

    # Select the appropriate background image based on the current phase and user
    background_image = pygame.image.load(phase_to_image.get(curr_phase, default_background))

    # Scale and blit the background image
    background_image = pygame.transform.scale(background_image, (values.WIDTH, values.HEIGHT))
    screen.blit(background_image, (0, 0))

    # Draw the game board lines
    lines = [
        ((50, 50), (550, 50)), ((50, 50), (50, 550)), ((550, 50), (550, 550)), ((50, 550), (550, 550)),
        ((300, 50), (300, 175)), ((50, 300), (175, 300)), ((425, 300), (550, 300)), ((300, 425), (300, 550)),
        ((175, 175), (425, 175)), ((175, 175), (175, 425)), ((425, 175), (425, 425)), ((175, 425), (425, 425))
    ]
    for start, end in lines:
        pygame.draw.line(screen, values.BLACK, start, end, values.LINE_WIDTH)

    # Draw intersection points
    for point in values.intersection_points:
        pygame.draw.circle(screen, values.BLACK, point, 10)

def curr_board():
    piece_width, piece_height = 100, 100
    clicked_piece_width, clicked_piece_height = 120, 120

    # Load and scale pieces
    white_piece = pygame.image.load(values.white_piece_img)
    white_piece = pygame.transform.scale(white_piece, (piece_width, piece_height))
    black_piece = pygame.image.load(values.black_piece_img)
    black_piece = pygame.transform.scale(black_piece, (piece_width, piece_height))

    # Helper function to draw pieces
    def draw_piece(piece, point, is_clicked):
        if is_clicked:
            scaled_piece = pygame.transform.scale(piece, (clicked_piece_width, clicked_piece_height))
            offset_x = scaled_piece.get_width() // 2
            offset_y = scaled_piece.get_height() // 2
        else:
            scaled_piece = piece
            offset_x = piece.get_width() // 2
            offset_y = piece.get_height() // 2
        screen.blit(scaled_piece, (point[0] - offset_x, point[1] - offset_y))

    # Draw pieces for human player
    for point in values.board_pieces_by_player[values.player_human]:
        draw_piece(white_piece, point, point == values.prev_piece_clicked)

    # Draw pieces for AI player
    for point in values.board_pieces_by_player[values.player_ai]:
        draw_piece(black_piece, point, point == values.prev_piece_clicked)

def check_moves():
    # All possible points on the board
    all_points = set(values.intersection_points)
    
    # Points currently occupied by any player's pieces
    occupied_points = set(values.board_pieces_by_player[values.player_human] + values.board_pieces_by_player[values.player_ai])
    
    # Calculate available moves by subtracting occupied points from all points
    available_moves = all_points - occupied_points
    
    return available_moves

def availmoves():
    # Visualize available moves on the board
    available_moves = check_moves()
    for point in available_moves:
        pygame.draw.circle(screen, values.BLACK, point, 15, width=5)

def check_movesSecondPhase(curr_player, opponent_player):
    # Gather sets of pieces for both players
    curr_player_pieces = set(values.board_pieces_by_player[curr_player])
    opponent_player_pieces = set(values.board_pieces_by_player[opponent_player])

    # Calculate valid moves for the current player
    curr_player_valid_moves = set()
    for piece in curr_player_pieces:
        possible_moves = set(values.point_moves[piece])
        # Exclude moves to points occupied by any player's pieces
        curr_player_valid_moves.update(possible_moves - (curr_player_pieces | opponent_player_pieces))

    return curr_player_valid_moves

def checkPieceValidMoves(piece_clicked, curr_player, opponent_player):
    # Retrieve sets of pieces for both the current player and the opponent
    curr_player_pieces = set(values.board_pieces_by_player[curr_player])
    opponent_player_pieces = set(values.board_pieces_by_player[opponent_player])

    # Get possible moves for the clicked piece
    clicked_piece_moves = set(values.point_moves[piece_clicked])

    # Calculate valid moves by excluding positions occupied by any player's pieces
    clicked_piece_valid_moves = clicked_piece_moves - (curr_player_pieces | opponent_player_pieces)

    return clicked_piece_valid_moves

def placePieceOnBoard(curr_player, point):
    piece_width = 100
    piece_height = 100

    # Determine the piece image based on the current player
    piece_image_path = values.white_piece_img if curr_player == values.player_human else values.black_piece_img
    piece_image = pygame.image.load(piece_image_path)
    piece_image = pygame.transform.scale(piece_image, (piece_width, piece_height))

    # Calculate the position to blit the piece
    piece_position = (point[0] - piece_width // 2, point[1] - piece_height // 2)

    # Blit the piece image to the screen
    screen.blit(piece_image, piece_position)

    # Update game state
    values.board_pieces_by_player[curr_player].append(point)
    values.held_pieces_by_player[curr_player] -= 1

def check_points(curr_player):
    values.player_pieces_mills[curr_player] = []
    found_mill = False

    for group in values.consecutive_points:
        if all(point in values.board_pieces_by_player[curr_player] for point in group):
            values.player_pieces_mills[curr_player].extend(group)
            found_mill = True

    return found_mill

def newmill_formed(curr_player):
    current_mills = set(values.player_pieces_mills[curr_player])
    previous_mills = set(values.player_pieces_prev_mills[curr_player])

    # Update the previous mills to the current mills for future comparison
    values.player_pieces_prev_mills[curr_player] = values.player_pieces_mills[curr_player]

    # Check if a new mill has been formed
    return not current_mills.issubset(previous_mills)


def remove(mouse_x, mouse_y, curr_player, current_phase):
    board(current_phase, curr_player)
    curr_board()

    opponent_player = values.player_ai if curr_player == values.player_human else values.player_human
    opponent_pieces = set(values.board_pieces_by_player[opponent_player])
    opponent_mills = set(values.player_pieces_prev_mills[opponent_player])
    valid_pieces_to_remove = opponent_pieces - opponent_mills

    if curr_player != values.current_player:
        return_value = ai_moves(values.GAMEPLAY_REMOVE_PIECE, curr_player)
        values.board_pieces_by_player[opponent_player].remove(return_value)
        return handle_game_end(curr_player)

    for vpoint in valid_pieces_to_remove:
        pygame.draw.circle(screen, values.GREEN, vpoint, 20, width=5) 

    for piece in valid_pieces_to_remove:
        distance = ((mouse_x - piece[0]) ** 2 + (mouse_y - piece[1]) ** 2) ** 0.5
        if distance <= values.POINT_RADIUS:
            values.board_pieces_by_player[opponent_player].remove(piece)
            return handle_game_end(curr_player)

    return values.GAMEPLAY_REMOVE_PIECE, curr_player

def handle_game_end(curr_player):
    # Determine the opponent player based on the current player
    opponent_player = values.player_ai if curr_player == values.player_human else values.player_human

    # Check for a winner
    winner = check_winner(curr_player)
    if winner != 0:
        return (values.GAMEPLAY_PLAYER_WON if winner == values.current_player else values.GAMEPLAY_PLAYER_LOSE, curr_player)

    # Check if the game should move to the final phase or continue in the movement phase
    if values.held_pieces_by_player[curr_player] > 0:
        return switch_player_and_phase(curr_player, values.PLAYING_PHASE)
    elif len(values.board_pieces_by_player[curr_player]) == 3 and len(values.board_pieces_by_player[opponent_player]) == 3:
        return switch_player_and_phase(curr_player, values.GAMEPLAY_FINAL_PHASE)
    else:
        return switch_player_and_phase(curr_player, values.MOVEMENT_PHASE)

def switch_player_and_phase(curr_player, next_phase):
    pygame.time.wait(1000)
    curr_player = values.player_ai if curr_player == values.player_human else values.player_human
    board(next_phase, curr_player)
    curr_board()
    return next_phase, curr_player

def check_winner(curr_player):
    if curr_player == values.player_human:
        opponent_player = values.player_ai
    elif curr_player == values.player_ai:
        opponent_player = values.player_human
    else:
        return 0  # Early exit on invalid player

    # Check if the current player has no pieces left to place and is reduced to two pieces or has no valid moves
    if check_end_conditions(curr_player, opponent_player):
        return opponent_player

    # Check if the opponent has no pieces left to place and is reduced to two pieces or has no valid moves
    if check_end_conditions(opponent_player, curr_player):
        return curr_player

    return 0

def check_end_conditions(player, opponent):
    if values.held_pieces_by_player[player] == 0:
        player_pieces = set(values.board_pieces_by_player[player])
        if len(player_pieces) <= 2:
            return True
        if not check_movesSecondPhase(player, opponent):
            return True
    return False

def result(mouse_x, mouse_y, curr_player, current_phase):
    board(current_phase, curr_player)
    curr_board()

    # Define button properties
    btn_width = 214
    btn_height = 65
    play_again_btn_x = 573
    play_again_btn_y = 325
    exit_btn_x = play_again_btn_x + btn_width
    exit_btn_y = play_again_btn_y

    # Draw buttons
    pygame.draw.rect(screen, values.PLAY_AGAIN_COLOR, (play_again_btn_x, play_again_btn_y, btn_width, btn_height), 1)
    pygame.draw.rect(screen, values.EXIT_COLOR, (exit_btn_x, exit_btn_y, btn_width, btn_height), 1)

    # Check button clicks
    if play_again_btn_x <= mouse_x <= play_again_btn_x + btn_width and play_again_btn_y <= mouse_y <= play_again_btn_y + btn_height:
        play_again()
        return values.MAIN_DISPLAY, 0
    
    if exit_btn_x <= mouse_x <= exit_btn_x + btn_width and exit_btn_y <= mouse_y <= exit_btn_y + btn_height:
        pygame.quit()
        sys.exit()
    
    return current_phase, curr_player

def play_again():
    # Reset player states
    values.curr_player = 0
    values.current_player = 0
    values.piece_clicked = (0, 0)
    values.prev_piece_clicked = (0, 0)
    values.white_piece_clicked = False
    values.black_piece_clicked = False
    values.is_piece_selected = False
    values.current_game_phase = values.GAMEPLAY_SELECT_PIECE_TO_MOVE

    # Reset game pieces and held pieces
    values.held_pieces_by_player = {values.player_human: 6, values.player_ai: 6}
    values.board_pieces_by_player = {values.player_human: [], values.player_ai: []}

if __name__ == "__main__":
    prev_phase = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if current_phase == values.MAIN_DISPLAY:
                    current_phase = display(mouse_x, mouse_y)
                elif current_phase == values.CHOOSE_COLOR_CHAR:
                    prev_phase = current_phase
                    current_phase, values.current_player = chooseColor(mouse_x, mouse_y)
                    if values.current_player == 1:
                        curr_player = values.current_player
                    else:
                        curr_player = 2 
                elif current_phase == values.PLAYING_PHASE:
                    prev_phase = current_phase
                    current_phase, curr_player = start(mouse_x, mouse_y, curr_player, current_phase)
                elif current_phase == values.MOVEMENT_PHASE:
                    prev_phase = current_phase
                    current_phase, curr_player = second_phase(mouse_x, mouse_y, curr_player)
                elif current_phase == values.GAMEPLAY_FINAL_PHASE:
                    prev_phase = current_phase
                    current_phase, curr_player = final_phase(mouse_x, mouse_y, curr_player)
                elif current_phase == values.GAMEPLAY_REMOVE_PIECE:
                    prev_phase = current_phase
                    current_phase, curr_player = remove(mouse_x, mouse_y, curr_player, current_phase)
                elif current_phase == values.GAMEPLAY_PLAYER_WON or current_phase == values.GAMEPLAY_PLAYER_LOSE or current_phase == values.GAMEPLAY_PLAYER_DRAW:
                    prev_phase = current_phase
                    current_phase, curr_player = result(mouse_x, mouse_y, curr_player, current_phase)
                else:
                    pygame.quit()
                    sys.exit()
        
        if current_phase == values.MAIN_DISPLAY:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            temp = display(mouse_x, mouse_y)

        if prev_phase != current_phase and prev_phase != values.GAMEPLAY_REMOVE_PIECE and prev_phase != values.GAMEPLAY_PLAYER_WON and prev_phase != values.GAMEPLAY_PLAYER_LOSE and prev_phase != values.GAMEPLAY_PLAYER_DRAW:
            pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, {'pos': (1, 1)}))
        
        pygame.display.flip()
        
    pygame.quit()
    sys.exit()
