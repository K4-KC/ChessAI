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

def board_to_FEN(pos, board, move=False):

    pos_part = [pos.split(' ')[i] for i in range(1, 6)]
    if move:
        pos_part[0] = 'w' if pos_part[0] == 'b' else 'b'
        pos_part[2] = '-'
        pos_part[4] = str(int(pos_part[4]) + 1) if pos_part[0] == 'w' else pos_part[4]
    pos_part = " ".join(pos_part)

    fen_rows = []
    
    for row in board:
        fen_row = ""
        empty_count = 0
        
        for cell in row:
            if cell == '0':
                empty_count += 1
            else:
                if empty_count > 0:
                    fen_row += str(empty_count)
                    empty_count = 0
                fen_row += cell
        
        if empty_count > 0:
            fen_row += str(empty_count)
        
        fen_rows.append(fen_row)
    
    fen_position = "/".join(fen_rows)
    
    return fen_position + " " + pos_part

def get_color(piece):
    if piece.isupper():
        return True
    elif piece.islower():
        return False
    else: return None

def get_moves(pos, board):
    color = True if pos.split(' ')[1] == 'w' else False
    return [[get_moves_selected(color, board, i, j) for i in range(8)]for j in range(8)]

def get_moves_selected(color, board, x , y):
    piece = board[y][x]

    if color:
        if piece == 'P': return get_pawn_moves(board, True, x, y)
        elif piece == 'R': return get_rook_moves(board, True, x, y)
        elif piece == 'N': return get_knight_moves(board, True, x, y)
        elif piece == 'B': return get_bishop_moves(board, True, x, y)
        elif piece == 'Q': return get_queen_moves(board, True, x, y)
        elif piece == 'K': return get_king_moves(board, True, x, y)
        else: return []
    
    elif piece == 'p': return get_pawn_moves(board, False, x, y)
    elif piece == 'r': return get_rook_moves(board, False, x, y)
    elif piece == 'n': return get_knight_moves(board, False, x, y)
    elif piece == 'b': return get_bishop_moves(board, False, x, y)
    elif piece == 'q': return get_queen_moves(board, False, x, y)
    elif piece == 'k': return get_king_moves(board, False, x, y)
    
    else: return []

def get_pawn_moves(board, color, x, y):
    moves = []

    if color:
        if y > 0:
            moves.append((x, y-1)) if board[y-1][x] == '0' else None
            if y == 6:
                moves.append((x, y-2)) if board[y-2][x] == '0' else None
            if x > 0 and get_color(board[y-1][x-1]) is False: moves.append((x-1, y-1))
            if x < 7 and get_color(board[y-1][x+1]) is False: moves.append((x+1, y-1))
    else:
        if y < 7:
            moves.append((x, y+1)) if board[y+1][x] == '0' else None
            if y == 1:
                moves.append((x, y+2)) if board[y+2][x] == '0' else None
            if x > 0 and get_color(board[y+1][x-1]): moves.append((x-1, y+1))
            if x < 7 and get_color(board[y+1][x+1]): moves.append((x+1, y+1))
    
    # add en passant and promotion

    return moves

def get_rook_moves(board, color, x, y):
    moves = []

    for i in range(1, x+1):
        if board[y][x-i] != '0':
            if get_color(board[y][x-i]) is not color: moves.append((x-i, y))
            break
        else: moves.append((x-i, y))

    for i in range(x+1, 8):
        if board[y][i] != '0':
            if get_color(board[y][i]) is not color: moves.append((i, y))
            break
        else: moves.append((i, y))
    
    for i in range(1, y+1):
        if board[y-i][x] != '0':
            if get_color(board[y-i][x]) is not color: moves.append((x, y-i))
            break
        else: moves.append((x, y-i))

    for i in range(y+1, 8):
        if board[i][x] != '0':
            if get_color(board[i][x]) is not color: moves.append((x, i))
            break
        else: moves.append((x, i))

    return moves

def get_knight_moves(board, color, x, y):
    moves = []

    if x > 0:
        if x > 1:
            if y > 0: moves.append((x-2, y-1)) if get_color(board[y-1][x-2]) is not color else None
            if y < 7: moves.append((x-2, y+1)) if get_color(board[y+1][x-2]) is not color else None
        if y > 1: moves.append((x-1, y-2)) if get_color(board[y-2][x-1]) is not color else None
        if y < 6: moves.append((x-1, y+2)) if get_color(board[y+2][x-1]) is not color else None
    if x < 7:
        if x < 6:
            if y > 0: moves.append((x+2, y-1)) if get_color(board[y-1][x+2]) is not color else None
            if y < 7: moves.append((x+2, y+1)) if get_color(board[y+1][x+2]) is not color else None
        if y > 1: moves.append((x+1, y-2)) if get_color(board[y-2][x+1]) is not color else None
        if y < 6: moves.append((x+1, y+2)) if get_color(board[y+2][x+1]) is not color else None
    
    return moves

def get_bishop_moves(board, color, x, y):
    moves = []

    diag_bott_rght, diag_bott_left, diag_top_rght, diag_top_left = True, True, True, True
    for i in range(1, 8):
        if diag_bott_rght and x+i < 8 and y+i < 8:
            if board[y+i][x+i] == '0': moves.append((x+i, y+i))
            else:
                if get_color(board[y+i][x+i]) is not color: moves.append((x+i, y+i))
                diag_bott_rght = False        
        if diag_bott_left and x+i < 8 and y-i >= 0:
            if board[y-i][x+i] == '0': moves.append((x+i, y-i))
            else:
                if get_color(board[y-i][x+i]) is not color: moves.append((x+i, y-i))
                diag_bott_left = False

        if diag_top_rght and x-i >= 0 and y+i < 8:
            if board[y+i][x-i] == '0': moves.append((x-i, y+i))
            else:
                if get_color(board[y+i][x-i]) is not color: moves.append((x-i, y+i))
                diag_top_rght = False

        if diag_top_left and x-i >= 0 and y-i >= 0:
            if board[y-i][x-i] == '0': moves.append((x-i, y-i))
            else:
                if get_color(board[y-i][x-i]) is not color: moves.append((x-i, y-i))
                diag_top_left = False

    return moves

def get_queen_moves(board, color, x, y):
    return get_rook_moves(board, color, x, y) + get_bishop_moves(board, color, x, y)

def get_king_moves(board, color, x, y):
    moves = []

    if x > 0: moves.append((x-1, y)) if get_color(board[y][x-1]) is not color else None
    if x < 7: moves.append((x+1, y)) if get_color(board[y][x+1]) is not color else None
    if y > 0: moves.append((x, y-1)) if get_color(board[y-1][x]) is not color else None
    if y < 7: moves.append((x, y+1)) if get_color(board[y+1][x]) is not color else None
    if x > 0 and y > 0: moves.append((x-1, y-1)) if get_color(board[y-1][x-1]) is not color else None
    if x > 0 and y < 7: moves.append((x-1, y+1)) if get_color(board[y+1][x-1]) is not color else None
    if x < 7 and y > 0: moves.append((x+1, y-1)) if get_color(board[y-1][x+1]) is not color else None
    if x < 7 and y < 7: moves.append((x+1, y+1)) if get_color(board[y+1][x+1]) is not color else None

    return moves

def make_move(pos, selected, new_selected, board):
    if board[new_selected[1]][new_selected[0]] == '0':
        board[new_selected[1]][new_selected[0]] = board[selected[1]][selected[0]]
        board[selected[1]][selected[0]] = '0'
    else:
        # capture
        board[new_selected[1]][new_selected[0]] = board[selected[1]][selected[0]]
        board[selected[1]][selected[0]] = '0'
    
    # improve promotion options
    if new_selected[1] == 0:
        if board[new_selected[1]][new_selected[0]] == 'P':
            board[new_selected[1]][new_selected[0]] = 'Q'
    elif new_selected[1] == 7:
        if board[new_selected[1]][new_selected[0]] == 'p':
            board[new_selected[1]][new_selected[0]] = 'q'
    
    pos = board_to_FEN(pos, board, True)
    return (pos, board)