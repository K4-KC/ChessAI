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

def board_to_FEN(pos, board, move=False, castle_rights='KQkq', en_passant='-'):

    pos_part = [pos.split(' ')[i] for i in range(1, 6)]
    if move:
        pos_part[0] = 'w' if pos_part[0] == 'b' else 'b'
        pos_part[1] = castle_rights
        pos_part[2] = en_passant
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

def get_territory(pos, board, color):
    territory = [[False for i in range(8)] for j in range(8)]

    for i in range(8):
        for j in range(8):
            piece = board[j][i]
            if not color:
                if piece == 'P':
                    for square in get_pawn_territory(board, True, i, j):
                        territory[square[1]][square[0]] = True
                elif piece == 'R':
                    for square in get_rook_territory(board, True, i, j):
                        territory[square[1]][square[0]] = True
                elif piece == 'N':
                    for square in get_knight_territory(board, True, i, j):
                        territory[square[1]][square[0]] = True
                elif piece == 'B':
                    for square in get_bishop_territory(board, True, i, j):
                        territory[square[1]][square[0]] = True
                elif piece == 'Q':
                    for square in get_queen_territory(board, True, i, j):
                        territory[square[1]][square[0]] = True
                elif piece == 'K':
                    for square in get_king_territory(board, True, i, j):
                        territory[square[1]][square[0]] = True
            
            elif piece == 'p':
                for square in get_pawn_territory(board, False, i, j):
                    territory[square[1]][square[0]] = True
            elif piece == 'r':
                for square in get_rook_territory(board, False, i, j):
                    territory[square[1]][square[0]] = True
            elif piece == 'n':
                for square in get_knight_territory(board, False, i, j):
                    territory[square[1]][square[0]] = True
            elif piece == 'b':
                for square in get_bishop_territory(board, False, i, j):
                    territory[square[1]][square[0]] = True
            elif piece == 'q':
                for square in get_queen_territory(board, False, i, j):
                    territory[square[1]][square[0]] = True
            elif piece == 'k':
                for square in get_king_territory(board, False, i, j):
                    territory[square[1]][square[0]] = True

    return territory

def get_pawn_territory(board, color, x, y):
    territory = []

    if color:
        if y > 0:
            if x > 0: territory.append((x-1, y-1))
            if x < 7: territory.append((x+1, y-1))
    else:
        if y < 7:
            if x > 0: territory.append((x-1, y+1))
            if x < 7: territory.append((x+1, y+1))

    return territory

def get_rook_territory(board, color, x, y):
    territory = []

    for i in range(1, x+1):
        territory.append((x-i, y))
        if board[y][x-i] != '0':
            territory.append((x-i, y))
            break

    for i in range(x+1, 8):
        territory.append((i, y))
        if board[y][i] != '0':
            territory.append((i, y))
            break
    
    for i in range(1, y+1):
        territory.append((x, y-i))
        if board[y-i][x] != '0':
            territory.append((x, y-i))
            break

    for i in range(y+1, 8):
        territory.append((x, i))
        if board[i][x] != '0':
            territory.append((x, i))
            break

    return territory

def get_knight_territory(board, color, x, y):
    territory = []

    if x > 0:
        if x > 1:
            if y > 0: territory.append((x-2, y-1))
            if y < 7: territory.append((x-2, y+1))
        if y > 1: territory.append((x-1, y-2))
        if y < 6: territory.append((x-1, y+2))
    if x < 7:
        if x < 6:
            if y > 0: territory.append((x+2, y-1))
            if y < 7: territory.append((x+2, y+1))
        if y > 1: territory.append((x+1, y-2))
        if y < 6: territory.append((x+1, y+2))
    
    return territory

def get_bishop_territory(board, color, x, y):
    territory = []

    diag_bott_rght, diag_bott_left, diag_top_rght, diag_top_left = True, True, True, True
    for i in range(1, 8):
        if diag_bott_rght and x+i < 8 and y+i < 8:
            territory.append((x+i, y+i))
            if board[y+i][x+i] != '0': diag_bott_rght = False    

        if diag_bott_left and x+i < 8 and y-i >= 0:
            territory.append((x+i, y-i))
            if board[y-i][x+i] != '0': diag_bott_left = False

        if diag_top_rght and x-i >= 0 and y+i < 8:
            territory.append((x-i, y+i))
            if board[y+i][x-i] != '0': diag_top_rght = False

        if diag_top_left and x-i >= 0 and y-i >= 0:
            territory.append((x-i, y-i))
            if board[y-i][x-i] != '0': diag_top_left = False

    return territory

def get_queen_territory(board, color, x, y):
    return get_rook_territory(board, color, x, y) + get_bishop_territory(board, color, x, y)

def get_king_territory(board, color, x, y):
    territory = []

    if x > 0: territory.append((x-1, y))
    if x < 7: territory.append((x+1, y))
    if y > 0: territory.append((x, y-1))
    if y < 7: territory.append((x, y+1))
    if x > 0 and y > 0: territory.append((x-1, y-1))
    if x > 0 and y < 7: territory.append((x-1, y+1))
    if x < 7 and y > 0: territory.append((x+1, y-1))
    if x < 7 and y < 7: territory.append((x+1, y+1))

    return territory

def get_moves(pos, board):
    color = True if pos.split(' ')[1] == 'w' else False
    castle_rights, en_passant = pos.split(' ')[2:4]
    territory = get_territory(pos, board, color)
    return [[get_moves_selected(color, board, territory, castle_rights, en_passant, i, j) for i in range(8)]for j in range(8)]

def get_moves_selected(color, board, territory, castle_rights, en_passant, x , y):
    piece = board[y][x]

    if color:
        if piece == 'P': return get_pawn_moves(en_passant, board, True, x, y)
        elif piece == 'R': return get_rook_moves(board, True, x, y)
        elif piece == 'N': return get_knight_moves(board, True, x, y)
        elif piece == 'B': return get_bishop_moves(board, True, x, y)
        elif piece == 'Q': return get_queen_moves(board, True, x, y)
        elif piece == 'K': return get_king_moves(castle_rights, board, territory, True, x, y)
        else: return []
    
    elif piece == 'p': return get_pawn_moves(en_passant, board, False, x, y)
    elif piece == 'r': return get_rook_moves(board, False, x, y)
    elif piece == 'n': return get_knight_moves(board, False, x, y)
    elif piece == 'b': return get_bishop_moves(board, False, x, y)
    elif piece == 'q': return get_queen_moves(board, False, x, y)
    elif piece == 'k': return get_king_moves(castle_rights, board, territory, False, x, y)
    
    else: return []

def get_pawn_moves(en_passant, board, color, x, y):
    moves = []

    if color:
        if y > 0:
            moves.append((x, y-1)) if board[y-1][x] == '0' else None
            if y == 6:
                moves.append((x, y-2)) if board[y-2][x] == '0' else None
            # en passant
            elif en_passant != '-':
                if y == 3:
                    en_passant_pos = ord(en_passant[0])-97
                    if en_passant_pos == x+1:
                        moves.append((x+1, y-1))
                    elif en_passant_pos == x-1:
                        moves.append((x-1, y-1))
            if x > 0 and get_color(board[y-1][x-1]) is False: moves.append((x-1, y-1))
            if x < 7 and get_color(board[y-1][x+1]) is False: moves.append((x+1, y-1))
    else:
        if y < 7:
            moves.append((x, y+1)) if board[y+1][x] == '0' else None
            if y == 1:
                moves.append((x, y+2)) if board[y+2][x] == '0' else None
            # en passant
            elif en_passant != '-':
                if y == 4:
                    en_passant_pos = ord(en_passant[0])-97
                    if en_passant_pos == x+1:
                        moves.append((x+1, y+1))
                    elif en_passant_pos == x-1:
                        moves.append((x-1, y+1))
            if x > 0 and get_color(board[y+1][x-1]): moves.append((x-1, y+1))
            if x < 7 and get_color(board[y+1][x+1]): moves.append((x+1, y+1))

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

def get_king_moves(castle_rights, board, territory, color, x, y):
    moves = []

    if x > 0: moves.append((x-1, y)) if get_color(board[y][x-1]) is not color and not territory[y][x-1] else None
    if x < 7: moves.append((x+1, y)) if get_color(board[y][x+1]) is not color and not territory[y][x+1] else None
    if y > 0: moves.append((x, y-1)) if get_color(board[y-1][x]) is not color and not territory[y-1][x] else None
    if y < 7: moves.append((x, y+1)) if get_color(board[y+1][x]) is not color and not territory[y+1][x] else None
    if x > 0 and y > 0: moves.append((x-1, y-1)) if get_color(board[y-1][x-1]) is not color and not territory[y-1][x-1] else None
    if x > 0 and y < 7: moves.append((x-1, y+1)) if get_color(board[y+1][x-1]) is not color and not territory[y+1][x-1] else None
    if x < 7 and y > 0: moves.append((x+1, y-1)) if get_color(board[y-1][x+1]) is not color and not territory[y-1][x+1] else None
    if x < 7 and y < 7: moves.append((x+1, y+1)) if get_color(board[y+1][x+1]) is not color and not territory[y+1][x+1] else None

    # castle
    if color:
        if 'K' in castle_rights:
            if board[7][5] == '0' and board[7][6] == '0':
                moves.append((6, 7))
        if 'Q' in castle_rights:
            if board[7][1] == '0' and board[7][2] == '0' and board[7][3] == '0':
                moves.append((2, 7))
    else:
        if 'k' in castle_rights:
            if board[0][5] == '0' and board[0][6] == '0':
                moves.append((6, 0))
        if 'q' in castle_rights:
            if board[0][1] == '0' and board[0][2] == '0' and board[0][3] == '0':
                moves.append((2, 0))

    return moves

def make_move(pos, selected, new_selected, board):

    castle_rights = pos.split(' ')[2]
    en_passant = '-'
    if board[new_selected[1]][new_selected[0]] == '0':

        # check en passant
        if selected[1] == 6:
            if new_selected[1] == 4 and board[selected[1]][selected[0]] == 'P':
                if new_selected[0] < 7:
                    if board[new_selected[1]][new_selected[0]+1] == 'p':
                        en_passant = chr(selected[0]+97) + '3'
                if new_selected[0] > 0:
                    if board[new_selected[1]][new_selected[0]-1] == 'p':
                        en_passant = chr(selected[0]+97) + '3'
        elif selected[1] == 1:
            if new_selected[1] == 3 and board[selected[1]][selected[0]] == 'p':
                if new_selected[0] < 7:
                    if board[new_selected[1]][new_selected[0]+1] == 'P':
                        en_passant = chr(selected[0]+97) + '6'
                if new_selected[0] > 0:
                    if board[new_selected[1]][new_selected[0]-1] == 'P':
                        en_passant = chr(selected[0]+97) + '6'

        en_passant_move = pos.split(' ')[3]

        # make en passant move
        if en_passant_move != '-':
            if new_selected == (ord(en_passant_move[0])-97, 8 - int(en_passant_move[1])):
                if board[selected[1]][selected[0]] == 'P':
                    board[new_selected[1]+1][new_selected[0]] = '0'
                elif board[selected[1]][selected[0]] == 'p':
                    board[new_selected[1]-1][new_selected[0]] = '0'

        # castling
        if board[selected[1]][selected[0]] == 'K':
            castle_rights = castle_rights.replace('K', '')
            castle_rights = castle_rights.replace('Q', '')
            if selected == (4, 7) and new_selected == (6, 7):
                board[7][5] = 'R'
                board[7][7] = '0'
            elif selected == (4, 7) and new_selected == (2, 7):
                board[7][3] = 'R'
                board[7][0] = '0'
        elif board[selected[1]][selected[0]] == 'k':
            castle_rights = castle_rights.replace('k', '')
            castle_rights = castle_rights.replace('q', '')
            if selected == (4, 0) and new_selected == (6, 0):
                board[0][5] = 'r'
                board[0][7] = '0'
            elif selected == (4, 0) and new_selected == (2, 0):
                board[0][3] = 'r'
                board[0][0] = '0'
        elif board[selected[1]][selected[0]] == 'R':
            if selected == (0, 7):
                castle_rights = castle_rights.replace('Q', '')
            elif selected == (7, 7):
                castle_rights = castle_rights.replace('K', '')
        elif board[selected[1]][selected[0]] == 'r':
            if selected == (0, 0):
                castle_rights = castle_rights.replace('q', '')
            elif selected == (7, 0):
                castle_rights = castle_rights.replace('k', '')

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
    
    pos = board_to_FEN(pos, board, True, castle_rights, en_passant)
    return (pos, board)