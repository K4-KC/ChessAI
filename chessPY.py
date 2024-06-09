def FEN_to_board(pos):
    board_part = pos.split(' ')[0]
    rows = board_part.split('/')
    
    board = []
    
    for row in rows:
        board_row = []
        for char in row:
            if char.isdigit():
                board_row.extend(['0'] * int(char))
            else:
                board_row.append(char)
        board.append(board_row)
    
    return board

def get_color(piece):
    if piece.isupper():
        return True
    else:
        return False

def get_moves(pos):
    board = FEN_to_board(pos)
    return [[get_moves_selected(board, i, j) for i in range(8)]for j in range(8)]

def get_moves_selected(board, x , y):
    piece = board[y][x]
    if piece == 'P':
        return get_pawn_moves(board, True, x, y)
    elif piece == 'R':
        return get_rook_moves(board, True, x, y)
    elif piece == 'N':
        return get_knight_moves(board, True, x, y)
    elif piece == 'B':
        return get_bishop_moves(board, True, x, y)
    elif piece == 'Q':
        return get_queen_moves(board, True, x, y)
    elif piece == 'K':
        return get_king_moves(board, True, x, y)
    
    elif piece == 'p':
        return get_pawn_moves(board, False, x, y)
    elif piece == 'r':
        return get_rook_moves(board, False, x, y)
    elif piece == 'n':
        return get_knight_moves(board, False, x, y)
    elif piece == 'b':
        return get_bishop_moves(board, False, x, y)
    elif piece == 'q':
        return get_queen_moves(board, False, x, y)
    elif piece == 'k':
        return get_king_moves(board, False, x, y)
    
    else:
        return []

def get_pawn_moves(board, color, x, y):
    moves = []
    if color:
        if y > 0:
            moves.append((x, y-1)) if board[y-1][x] == '0' else None
            if y == 6:
                moves.append((x, y-2)) if board[y-2][x] == '0' else None
            if x > 0 and board[y-1][x-1] is not '0' and (not get_color(board[y-1][x-1])): moves.append((x-1, y-1))
            if x < 7 and board[y-1][x+1] is not '0' and (not get_color(board[y-1][x+1])): moves.append((x+1, y-1))
    else:
        if y < 7:
            moves.append((x, y+1)) if board[y+1][x] == '0' else None
            if y == 1:
                moves.append((x, y+2)) if board[y+2][x] == '0' else None
            # can be improved with the true/false
            if x > 0 and board[y+1][x-1] is not '0' and get_color(board[y+1][x-1]): moves.append((x-1, y+1))
            if x < 7 and board[y+1][x+1] is not '0' and get_color(board[y+1][x+1]): moves.append((x+1, y+1))

    return moves

def get_rook_moves(board, color, x, y):
    moves = []
    for i in range(8):
        if i != x: moves.append((i, y))
        if i != y: moves.append((x, i))
    return moves

def get_knight_moves(board, color, x, y):
    moves = []
    if x > 1 and y > 0: moves.append((x-2, y-1))
    if x > 1 and y < 7: moves.append((x-2, y+1))
    if x < 6 and y > 0: moves.append((x+2, y-1))
    if x < 6 and y < 7: moves.append((x+2, y+1))
    if x > 0 and y > 1: moves.append((x-1, y-2))
    if x > 0 and y < 6: moves.append((x-1, y+2))
    if x < 7 and y > 1: moves.append((x+1, y-2))
    if x < 7 and y < 6: moves.append((x+1, y+2))
    return moves

def get_bishop_moves(board, color, x, y):
    moves = []
    for i in range(1, 8):
        if x+i < 8 and y+i < 8: moves.append((x+i, y+i))
        if x+i < 8 and y-i >= 0: moves.append((x+i, y-i))
        if x-i >= 0 and y+i < 8: moves.append((x-i, y+i))
        if x-i >= 0 and y-i >= 0: moves.append((x-i, y-i))
    return moves

def get_queen_moves(board, color, x, y):
    return get_rook_moves(board, color, x, y) + get_bishop_moves(board, color, x, y)

def get_king_moves(board, color, x, y):
    moves = []
    if x > 0: moves.append((x-1, y))
    if x < 7: moves.append((x+1, y))
    if y > 0: moves.append((x, y-1))
    if y < 7: moves.append((x, y+1))
    if x > 0 and y > 0: moves.append((x-1, y-1))
    if x > 0 and y < 7: moves.append((x-1, y+1))
    if x < 7 and y > 0: moves.append((x+1, y-1))
    if x < 7 and y < 7: moves.append((x+1, y+1))
    return moves

def make_move(selected, new_selected, board):
    if board[new_selected[1]][new_selected[0]] == '0':
        board[new_selected[1]][new_selected[0]] = board[selected[1]][selected[0]]
        board[selected[1]][selected[0]] = '0'
    else:
        # capture
        board[new_selected[1]][new_selected[0]] = board[selected[1]][selected[0]]
        board[selected[1]][selected[0]] = '0'
    return board