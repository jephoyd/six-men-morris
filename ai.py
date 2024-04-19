import values
curr_phase = None

def ai_moves(phase, curr_player):
    opponent_player = values.player_ai if curr_player == values.player_human else values.player_human
    ai_pieces_onboard = set(values.board_pieces_by_player[curr_player])
    opp_pieces_onboard = set(values.board_pieces_by_player[opponent_player])
    available_moves = ai_checkmoves(ai_pieces_onboard, opp_pieces_onboard, 1)
    depth = 3
    global curr_phase 
    curr_phase = phase

    # Ensure all handler functions receive the correct number of arguments
    if phase == values.PLAYING_PHASE:
        result = handle_playing_phase(ai_pieces_onboard, opp_pieces_onboard, available_moves, curr_player, depth)
    elif phase == values.MOVEMENT_PHASE:
        result = handle_movement_phase(ai_pieces_onboard, opp_pieces_onboard, curr_player, depth)
    elif phase == values.GAMEPLAY_FINAL_PHASE:
        result = handle_final_phase(ai_pieces_onboard, opp_pieces_onboard, curr_player, depth)
    elif phase == values.GAMEPLAY_REMOVE_PIECE:
        result = handle_remove_piece_phase(opp_pieces_onboard, curr_player)

    if result is None:
        return (None, None)  # Ensure a tuple is returned
    return result

def handle_playing_phase(ai_pieces_onboard, opp_pieces_onboard, available_moves, curr_player, depth):
    best_move = None
    max_eval = float('-inf')
    for move in available_moves:
        new_ai_pieces = ai_pieces_onboard.copy()
        new_ai_pieces.add(move)
        new_ai_pieces_onhold = values.held_pieces_by_player[curr_player] - 1
        
        eval = minimax(new_ai_pieces, depth, new_ai_pieces_onhold, opp_pieces_onboard, values.held_pieces_by_player[curr_player])
        eval += block_opp_mill(opp_pieces_onboard, move)
        eval += make_mill(ai_pieces_onboard, move)

        if eval > max_eval:
            max_eval = eval
            best_move = move
    return best_move

def handle_movement_phase(ai_pieces_onboard, opp_pieces_onboard, curr_player, depth):
    best_move = None
    best_piece = None
    max_eval = float('-inf')
    for piece in ai_pieces_onboard:
        for move in ai_checkpiecemoves(piece, ai_pieces_onboard, opp_pieces_onboard):
            new_ai_pieces = ai_pieces_onboard.copy()
            new_ai_pieces.add(move)
            
            eval = minimax(new_ai_pieces, depth, 0, opp_pieces_onboard, 0)
            eval += block_opp_mill(opp_pieces_onboard, move)
            eval += make_mill(ai_pieces_onboard, move)

            if eval > max_eval:
                max_eval = eval
                best_move = move
                best_piece = piece
    return best_piece, best_move

def handle_final_phase(ai_pieces_onboard, opp_pieces_onboard, curr_player, depth):
    best_move = None
    best_piece = None
    max_eval = float('-inf')
    for piece in ai_pieces_onboard:
        for move in ai_checkmoves(ai_pieces_onboard, opp_pieces_onboard, 1):
            new_ai_pieces = ai_pieces_onboard.copy()
            new_ai_pieces.add(move)
            
            eval = minimax(new_ai_pieces, depth, 0, opp_pieces_onboard, 0)
            eval += block_opp_mill(opp_pieces_onboard, move)
            eval += make_mill(ai_pieces_onboard, move)

            if eval > max_eval:
                max_eval = eval
                best_move = move
                best_piece = piece
    return best_piece, best_move

def handle_remove_piece_phase(opp_pieces_onboard, curr_player):
    opponent_player = values.player_ai if curr_player == values.player_human else values.player_human
    opponent_mills = set(values.player_pieces_prev_mills[opponent_player])
    opponent_valid_pieces = opp_pieces_onboard - opponent_mills
    player_pieces = set(values.board_pieces_by_player[curr_player])

    best_piece = None
    best_value = float('-inf')
    for piece in opponent_valid_pieces:
        piece_value = remove_pieceval(piece, opponent_valid_pieces, player_pieces)
        if piece_value > best_value:
            best_piece = piece
            best_value = piece_value
    return best_piece

def ai_checkmoves(ai_pieces, opp_pieces, mode):
    if mode == 1:
        return calculate_free_moves(ai_pieces, opp_pieces)
    elif mode == 2:
        return calculate_valid_moves(ai_pieces, opp_pieces)

def calculate_free_moves(ai_pieces, opp_pieces):
    inter_points = set(values.intersection_points)
    points_occupied = ai_pieces | opp_pieces
    return inter_points - points_occupied

def calculate_valid_moves(ai_pieces, opp_pieces):
    your_moves = get_possible_moves(ai_pieces)
    opponent_moves = get_possible_moves(opp_pieces)
    return your_moves - (opponent_moves | ai_pieces)

def get_possible_moves(pieces):
    moves = set()
    for piece in pieces:
        moves.update(values.point_moves[piece])
    return moves

def ai_checkpiecemoves(piece_clicked, ai_pieces, opp_pieces):
    # Get all potential moves for the clicked piece
    potential_moves = set(values.point_moves[piece_clicked])

    # Exclude moves that would land on any occupied positions
    valid_moves = potential_moves - (ai_pieces | opp_pieces)
    return valid_moves

def minimax(ai_pieces, depth, ai_pieces_onhold, opp_pieces, opp_pieces_onhold):
    if depth == 0 or ai_checkplayerwon(ai_pieces, opp_pieces_onhold, opp_pieces):
        return evaluate(ai_pieces, opp_pieces)

    max_eval = float('-inf')
    if curr_phase == values.PLAYING_PHASE:
        return handle_playing_phase_minimax(ai_pieces, depth, ai_pieces_onhold, opp_pieces, opp_pieces_onhold, max_eval)
    elif curr_phase == values.MOVEMENT_PHASE:
        return handle_movement_phase_minimax(ai_pieces, depth, opp_pieces, max_eval)
    elif curr_phase == values.GAMEPLAY_FINAL_PHASE:
        return handle_final_phase_minimax(ai_pieces, depth, opp_pieces, max_eval)

def handle_playing_phase_minimax(ai_pieces, depth, ai_pieces_onhold, opp_pieces, opp_pieces_onhold, max_eval):
    for move in ai_checkmoves(ai_pieces, opp_pieces, 1):
        new_ai_pieces = set(ai_pieces.copy())
        new_ai_pieces.add(move)
        new_ai_pieces_onhold = ai_pieces_onhold - 1
        eval = minimax(new_ai_pieces, depth - 1, new_ai_pieces_onhold, opp_pieces, opp_pieces_onhold)
        max_eval = max(max_eval, eval)
    return max_eval

def handle_movement_phase_minimax(ai_pieces, depth, opp_pieces, max_eval):
    for piece in ai_pieces:
        for move in ai_checkpiecemoves(piece, ai_pieces, opp_pieces):
            new_ai_pieces = set(ai_pieces.copy())
            new_ai_pieces.add(move)
            eval = minimax(new_ai_pieces, depth - 1, 0, opp_pieces, 0)
            max_eval = max(max_eval, eval)
    return max_eval

def handle_final_phase_minimax(ai_pieces, depth, opp_pieces, max_eval):
    for piece in ai_pieces:
        for move in ai_checkmoves(ai_pieces, opp_pieces, 1):
            new_ai_pieces = set(ai_pieces.copy())
            new_ai_pieces.add(move)
            eval = minimax(new_ai_pieces, depth - 1, 0, opp_pieces, 0)
            max_eval = max(max_eval, eval)
    return max_eval
    

def ai_checkplayerwon(ai_pieces, opp_pieces_onhold, opp_pieces):
    # Opponent cannot move if they have 2 or fewer pieces on the board or no valid moves left
    if opp_pieces_onhold == 0 and (len(opp_pieces) <= 2 or not ai_checkmoves(opp_pieces, ai_pieces, 2)):
        return True
    return False

def evaluate(ai_pieces, opp_pieces):
    piece_count_weight, mill_count_weight, mobility_weight, mode = get_phase_weights()

    ai_piece_count = len(ai_pieces)
    ai_mills = count_mill(ai_pieces, 1)
    ai_mobility = len(ai_checkmoves(ai_pieces, opp_pieces, mode))
    
    ai_score = (piece_count_weight * ai_piece_count) + (mill_count_weight * ai_mills) + (mobility_weight * ai_mobility)
    return ai_score

def get_phase_weights():
    if curr_phase == values.PLAYING_PHASE:
        return (2, 10, 2, 1)
    elif curr_phase == values.MOVEMENT_PHASE:
        return (7, 10, 8, 2)
    elif curr_phase == values.GAMEPLAY_FINAL_PHASE:
        return (4, 10, 8, 1)

def count_mill(pieces, cmode):
    if cmode == 1:
        return count_complete_mills(pieces)
    elif cmode == 2:
        return count_two_piece_configurations(pieces)
    elif cmode == 3:
        return count_groups_with_two_pieces(pieces)

def count_complete_mills(pieces):
    mill_count = 0
    for group in values.consecutive_points:
        if all(point in pieces for point in group):
            mill_count += 1
    return mill_count

def count_two_piece_configurations(pieces):
    mill_pieces = set()
    for group in values.consecutive_points:
        count = sum(1 for point in group if point in pieces)
        if count == 2:
            mill_pieces.update(group)
    return mill_pieces

def make_mill(ai_pieces, ai_move):
    for group in values.consecutive_points:
        if ai_move in group and sum(point in ai_pieces for point in group) == 2:
            return 200
    return 0

def count_groups_with_two_pieces(pieces):
    mill_groups = set()
    for group in values.consecutive_points:
        count = sum(1 for point in group if point in pieces)
        if count == 2:
            mill_groups.add(tuple(group))
    return mill_groups

def remove_pieceval(piece, opp_pieces, player_pieces):
    value = len(ai_checkpiecemoves(piece, player_pieces, opp_pieces))

    if piece in count_mill(opp_pieces, 2):
        value += 1

    for group in count_mill(player_pieces, 3):
        if piece in group:
            value += 1

    return value

def block_opp_mill(opp_pieces, ai_move):
    for group in values.consecutive_points:
        if ai_move in group and sum(point in opp_pieces for point in group) == 2:
            return 100
    return 0

