# from chess import system
import pygame
import chessPY

# system("echo 5.0")

import sys

pygame.init()

original_pieces = {
    'P' :[pygame.image.load('data/png/pieces/White/P' + str(P) +'.png') for P in range(2)],
    'K' :[pygame.image.load('data/png/pieces/White/K' + str(K) +'.png') for K in range(2)],
    'Q' :[pygame.image.load('data/png/pieces/White/Q' + str(Q) +'.png') for Q in range(2)],
    'R' :[pygame.image.load('data/png/pieces/White/R' + str(R) +'.png') for R in range(2)],
    'B' :[pygame.image.load('data/png/pieces/White/B' + str(B) +'.png') for B in range(2)],
    'N' :[pygame.image.load('data/png/pieces/White/N' + str(N) +'.png') for N in range(2)],

    'p' :[pygame.image.load('data/png/pieces/Black/p' + str(p) +'.png') for p in range(2)],
    'k' :[pygame.image.load('data/png/pieces/Black/k' + str(k) +'.png') for k in range(2)],
    'q' :[pygame.image.load('data/png/pieces/Black/q' + str(q) +'.png') for q in range(2)],
    'r' :[pygame.image.load('data/png/pieces/Black/r' + str(r) +'.png') for r in range(2)],
    'b' :[pygame.image.load('data/png/pieces/Black/b' + str(b) +'.png') for b in range(2)],
    'n' :[pygame.image.load('data/png/pieces/Black/n' + str(n) +'.png') for n in range(2)],

    '0' :[pygame.image.load('data/png/pieces/0' + str(i) +'.png') for i in range(2)]
    }

original_width, original_height = 640, 640
aspect_ratio = original_width / original_height

def transform_scale(original_pieces, width, height):
    return {
        'P' :[pygame.transform.scale(original_pieces['P'][i], (width//8, height//8)) for i in range(2)],
        'K' :[pygame.transform.scale(original_pieces['K'][i], (width//8, height//8)) for i in range(2)],
        'Q' :[pygame.transform.scale(original_pieces['Q'][i], (width//8, height//8)) for i in range(2)],
        'R' :[pygame.transform.scale(original_pieces['R'][i], (width//8, height//8)) for i in range(2)],
        'B' :[pygame.transform.scale(original_pieces['B'][i], (width//8, height//8)) for i in range(2)],
        'N' :[pygame.transform.scale(original_pieces['N'][i], (width//8, height//8)) for i in range(2)],

        'p' :[pygame.transform.scale(original_pieces['p'][i], (width//8, height//8)) for i in range(2)],
        'k' :[pygame.transform.scale(original_pieces['k'][i], (width//8, height//8)) for i in range(2)],
        'q' :[pygame.transform.scale(original_pieces['q'][i], (width//8, height//8)) for i in range(2)],
        'r' :[pygame.transform.scale(original_pieces['r'][i], (width//8, height//8)) for i in range(2)],
        'b' :[pygame.transform.scale(original_pieces['b'][i], (width//8, height//8)) for i in range(2)],
        'n' :[pygame.transform.scale(original_pieces['n'][i], (width//8, height//8)) for i in range(2)],

        '0' :[pygame.transform.scale(original_pieces['0'][i], (width//8, height//8)) for i in range(2)]
        }

pieces = transform_scale(original_pieces, original_width, original_height)

screen = pygame.display.set_mode((original_width, original_height), pygame.RESIZABLE)
capture_screen = pygame.Surface((original_width/8, original_height/8), pygame.SRCALPHA)
move_screen = pygame.Surface((original_width/8, original_height/8), pygame.SRCALPHA)
off_track_screen = pygame.Surface((original_width, original_height), pygame.SRCALPHA)
pygame.draw.circle(capture_screen,(100, 100, 100, 100), 
                   ((original_width/16), (original_height/16)), original_height//16, original_height//90)
pygame.draw.circle(move_screen,(100, 100, 100, 100), 
                   ((original_width/16), (original_height/16)), original_height//50)

off_track_screen.fill((255, 255, 255, 100))

pygame.display.set_caption("ChessAI")

def maintain_aspect_ratio(event_size):
    new_width, new_height = event_size
    new_width = 8 * (new_width//8)
    new_height = 8 * (new_height//8)
    if new_width / new_height > aspect_ratio:
        new_width = 8 * (int(new_height * aspect_ratio)//8)
    else:
        new_height = 8 * (int(new_width / aspect_ratio)//8)
    return new_width, new_height

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

def board_to_FEN(board):
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
    
    return fen_position + " w KQkq - 0 1"

def flip_board(board):
    return [row[::-1] for row in board[::-1]]

def flip_moves(moves):
    moves = flip_board(moves)
    return [[[(7 - move[0], 7 - move[1]) for move in piece] for piece in row] for row in moves]

pre_move_list = []
    # 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', 'rnbqkbnr/pppppppp/8/8/8/P7/1PPPPPPP/RNBQKBNR b KQkq - 0 1', 'rnbqkbnr/p1pppppp/8/1p6/8/P7/1PPPPPPP/RNBQKBNR w KQkq - 0 2', 'rnbqkbnr/p1pppppp/8/1p6/8/P7/RPPPPPPP/1NBQKBNR b Kkq - 1 2', 'rnbqkb1r/p1pppppp/5n2/1p6/8/P7/RPPPPPPP/1NBQKBNR w Kkq - 2 3', 'rnbqkb1r/p1pppppp/5n2/1p6/7P/P7/RPPPPPP1/1NBQKBNR b Kkq - 0 3', 'rnbqkb1r/2pppppp/p4n2/1p6/7P/P7/RPPPPPP1/1NBQKBNR w Kkq - 0 4', 'rnbqkb1r/2pppppp/p4n2/1p6/7P/P3P3/RPPP1PP1/1NBQKBNR b Kkq - 0 4', 'rnbqkb1r/2pppppp/p7/1p6/4n2P/P3P3/RPPP1PP1/1NBQKBNR w Kkq - 1 5', 'rnbqkb1r/2pppppp/p7/1p5P/4n3/P3P3/RPPP1PP1/1NBQKBNR b Kkq - 0 5', 'rnbqkb1r/2p1pppp/p2p4/1p5P/4n3/P3P3/RPPP1PP1/1NBQKBNR w Kkq - 0 6', 'rnbqkb1r/2p1pppp/p2p4/1p5P/4n3/P3P2N/RPPP1PP1/1NBQKB1R b Kkq - 1 6', 'rn1qkb1r/2p1pppp/p2p4/1p5P/4n3/P3P2b/RPPP1PP1/1NBQKB1R w Kkq - 2 7', 'rn1qkb1r/2p1pppp/p2p4/1p5P/4n3/P3P2b/RPPP1PP1/1NBQKBR1 b kq - 3 7', 'r2qkb1r/2pnpppp/p2p4/1p5P/4n3/P3P2b/RPPP1PP1/1NBQKBR1 w kq - 4 8', 'r2qkb1r/2pnpppp/p2p4/1p5P/4nP2/P3P2b/RPPP2P1/1NBQKBR1 b kq - 0 8', 'r2qkb1r/2pnp1pp/p2p1p2/1p5P/4nP2/P3P2b/RPPP2P1/1NBQKBR1 w kq - 0 9', 'r2qkb1r/2pnp1pp/p2p1p2/1p5P/4nP2/P3P2b/RPPPK1P1/1NBQ1BR1 b kq - 1 9', 'r1q1kb1r/2pnp1pp/p2p1p2/1p5P/4nP2/P3P2b/RPPPK1P1/1NBQ1BR1 w kq - 2 10', 'r1q1kb1r/2pnp1pp/p2p1p2/1p5P/P3nP2/4P2b/RPPPK1P1/1NBQ1BR1 b kq - 0 10', 'r3kb1r/1qpnp1pp/p2p1p2/1p5P/P3nP2/4P2b/RPPPK1P1/1NBQ1BR1 w kq - 1 11', 'r3kb1r/1qpnp1pp/p2p1p2/1P5P/4nP2/4P2b/RPPPK1P1/1NBQ1BR1 b kq - 0 11', '2kr1b1r/1qpnp1pp/p2p1p2/1P5P/4nP2/4P2b/RPPPK1P1/1NBQ1BR1 w - - 1 12', '2kr1b1r/1qpnp1pp/p2p1p2/1P5P/4nP2/4P2b/RPPP2P1/1NBQKBR1 b - - 2 12', '2kr1b1r/2pnp1pp/p1qp1p2/1P5P/4nP2/4P2b/RPPP2P1/1NBQKBR1 w - - 3 13', '2kr1b1r/2pnp1pp/p1qp1p2/1P5P/4nP2/4P2b/RPPPK1P1/1NBQ1BR1 b - - 4 13', '2kr1b1r/2pnp1pp/p2p1p2/1P5P/4nP2/2q1P2b/RPPPK1P1/1NBQ1BR1 w - - 5 14', '2kr1b1r/2pnp1pp/p2p1p2/1P5P/4nP2/2q1P2b/RPPP2P1/1NBQKBR1 b - - 6 14', '2kr1b1r/2pnp2p/p2p1p2/1P4pP/4nP2/2q1P2b/RPPP2P1/1NBQKBR1 w - g6 0 15', '2kr1b1r/2pnp2p/p2p1p2/1P4PP/4n3/2q1P2b/RPPP2P1/1NBQKBR1 b - - 0 15', '2kr3r/2pnp1bp/p2p1p2/1P4PP/4n3/2q1P2b/RPPP2P1/1NBQKBR1 w - - 1 16', '2kr3r/2pnp1bp/p2p1P2/1P5P/4n3/2q1P2b/RPPP2P1/1NBQKBR1 b - - 0 16', '2kr3r/2pn2bp/p2p1p2/1P5P/4n3/2q1P2b/RPPP2P1/1NBQKBR1 w - - 0 17', '2kr3r/2pn2bp/p2p1p2/1P5P/4n3/2q1P2b/RPPPK1P1/1NBQ1BR1 b - - 1 17', '3r3r/1kpn2bp/p2p1p2/1P5P/4n3/2q1P2b/RPPPK1P1/1NBQ1BR1 w - - 2 18', '3r3r/1kpn2bp/p2p1p2/1P5P/4n3/2q1P2b/RPPP2P1/1NBQKBR1 b - - 3 18', 'k2r3r/2pn2bp/p2p1p2/1P5P/4n3/2q1P2b/RPPP2P1/1NBQKBR1 w - - 4 19', 'k2r3r/2pn2bp/p2p1p2/1P5P/4n3/2q1P2b/RPPPK1P1/1NBQ1BR1 b - - 5 19', 'k5rr/2pn2bp/p2p1p2/1P5P/4n3/2q1P2b/RPPPK1P1/1NBQ1BR1 w - - 6 20', 'k5rr/2pn2bp/p2p1p2/1P5P/4n3/2q1P2b/RPPP2P1/1NBQKBR1 b - - 7 20', 'k2r3r/2pn2bp/p2p1p2/1P5P/4n3/2q1P2b/RPPP2P1/1NBQKBR1 w - - 8 21', 'k2r3r/2pn2bp/p2p1p2/1P5P/4n3/2q1P2b/RPPPK1P1/1NBQ1BR1 b - - 9 21', 'k5rr/2pn2bp/p2p1p2/1P5P/4n3/2q1P2b/RPPPK1P1/1NBQ1BR1 w - - 10 22', 'k5rr/2pn2bp/p2p1p2/1P5P/4n3/2q1P2b/RPPP2P1/1NBQKBR1 b - - 11 22', 'k2r3r/2pn2bp/p2p1p2/1P5P/4n3/2q1P2b/RPPP2P1/1NBQKBR1 w - - 12 23']

    # 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', 'rnbqkbnr/pppppppp/8/8/8/1P6/P1PPPPPP/RNBQKBNR b KQkq - 0 1', 'rnbqkbnr/pppp1ppp/8/4p3/8/1P6/P1PPPPPP/RNBQKBNR w KQkq - 0 2', 'rnbqkbnr/pppp1ppp/8/4p3/8/1P6/PBPPPPPP/RN1QKBNR b KQkq - 1b KQkq - 1 2', 'rnbqkb1r/ppppnppp/8/4p3/8/1P6/PBPPPPPP/RN1QKBNR w KQkq - 2 3', 'rnbqkb1r/ppppnppp/8/4p3/8/1P3N2/PBPPPPPP/RN1QKB1R b KQkq - 3 3', 'r1bqkb1r/ppppnppp/2n5/4p3/8/1P3N2/PBPPPPPP/RN1QKB1R w KQkq - 4 4', 'r1bqkb1r/ppppnppp/2n5/4p3/3P4/1P3N2/PBP1PPPP/RN1QKB1R b KQkq - 0 4', 'r1bqkb1r/1pppnppp/p1n5/4p3/3P4/1P3N2/PBP1PPPP/RN1QKB1R w KQkq - 0 5', 'r1bqkb1r/1pppnppp/p1n5/4P3/8/1P3N2/PBP1PPPP/RN1QKB1R b KQkq - 0 5', 'r1bqkb1r/1pppnppp/p7/4P3/1n6/1P3N2/PBP1PPPP/RN1QKB1R w KQkq - 1 6', 'r1bqkb1r/1pppnppp/p7/4P3/1n6/1P3N2/PBPKPPPP/RN1Q1B1R b kq - 2 6', 'r1bqkb1r/1p1pnppp/p1p5/4P3/1n6/1P3N2/PBPKPPPP/RN1Q1B1R w kq - 0 7', 'r1bqkb1r/1p1pnppp/p1p5/4P3/1n5N/1P6/PBPKPPPP/RN1Q1B1R b kq - 1 7', 'r1bqkb1r/1p1p1ppp/p1p5/4Pn2/1n5N/1P6/PBPKPPPP/RN1Q1B1R w kq - 2 8', 'r1bqkb1r/1p1p1ppp/p1p5/4PN2/1n6/1P6/PBPKPPPP/RN1Q1B1R b kq - 3 8', 'r1bqk2r/1p1p1ppp/p1p5/2b1PN2/1n6/1P6/PBPKPPPP/RN1Q1B1R w kq - 4 9', 'r1bqk2r/1p1p1ppp/p1p5/2b1PN2/Pn6/1P6/1BPKPPPP/RN1Q1B1R b kq - 0 9', 'r1b1k2r/1p1p1ppp/p1p5/2b1PN2/Pn5q/1P6/1BPKPPPP/RN1Q1B1R w kq - 1 10', 'r1b1k2r/1p1p1ppp/p1p5/2b1PN2/Pn5q/1P6/RBPKPPPP/1N1Q1B1R b kq - 2 10', 'r1b1k2r/1p1p1ppp/p1p5/2b1PN2/Pn2q3/1P6/RBPKPPPP/1N1Q1B1R w kq - 3 11', 'r1b1k2r/1p1p1ppp/p1p5/P1b1PN2/1n2q3/1P6/RBPKPPPP/1N1Q1B1R b kq - 0 11', 'r1b1k2r/3p1ppp/p1p5/Ppb1PN2/1n2q3/1P6/RBPKPPPP/1N1Q1B1R w kq b6 0 12', 'r1b1k2r/3p1ppp/p1p5/Ppb1PN2/1n2q3/1PN5/RBPKPPPP/3Q1B1R b kq - 1 12', 'r1b1k2r/3p1ppp/p1p5/Ppb1qN2/1n6/1PN5/RBPKPPPP/3Q1B1R w kq - 2 13', 'r1b1k2r/3p1ppp/p1p5/Ppb1qN2/1n2N3/1P6/RBPKPPPP/3Q1B1R b kq - 3 13', 'r1b1k2r/3p1ppp/p1pq4/Ppb2N2/1n2N3/1P6/RBPKPPPP/3Q1B1R w kq - 4 14', 'r1b1k2r/3p1ppp/p1pq4/Ppb2N2/1n2N3/1PK5/RBP1PPPP/3Q1B1R b kq - 5 14', 'r1b1k2r/3p1ppp/p1p5/Ppb2N2/1n2N3/1PK5/RBP1PPPP/3q1B1R w kq - 6 15', 'r1b1k2r/3p1ppp/p1p5/Ppb2N2/Rn2N3/1PK5/1BP1PPPP/3q1B1R b kq - 7 15', 'r1b1k2r/3p1ppp/p1p5/Ppbn1N2/R3N3/1PK5/1BP1PPPP/3q1B1R w kq - 8 16']
if pre_move_list:
    init_pos = pre_move_list[0]
else:
    init_pos = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

# init_pos = '1n2kbn1/rp2ppp1/1q5r/p6p/2p2PP1/1P2P2P/PR2K1B1/1b2q1NR w KQkq - 0 1'
# init_pos = 'R7/8/8/4R3/8/8/8/8 w KQkq - 0 1'

board_flip = False
board = FEN_to_board(init_pos)
# board = [['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
#          ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
#          ['0', '0', '0', '0', '0', '0', '0', '0'],
#          ['0', '0', '0', '0', '0', '0', '0', '0'],
#          ['0', '0', '0', '0', '0', '0', '0', '0'],
#          ['0', '0', '0', '0', '0', '0', '0', '0'],
#          ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
#          ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']]

moves = chessPY.get_moves(init_pos, board)

if board_flip:
    flipped_board = flip_board(board)
    flipped_moves = flip_moves(moves)

pos = init_pos
print(pos)

move_list, draw_move_list = [pos], [pos]
selected = False

window_size = (original_width, original_height)
running, off_track = True, False
while running:

    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                x, y = pygame.mouse.get_pos()
                new_selected = (int(x/(window_size[0]/8)), int(y/(window_size[1]/8)))
                if board_flip and pos.split(' ')[1] == 'b': new_selected = (7 - new_selected[0], 7 - new_selected[1])

                if selected:
                    if new_selected in moves[selected[1]][selected[0]]:
                        if board[selected[1]][selected[0]] == 'P' or board[selected[1]][selected[0]] == 'p':
                            draw_move_list = []
                        pos, board = chessPY.make_move(pos, selected, new_selected, board)
                        if pre_move_list:
                            if len(move_list) < len(pre_move_list):
                                if pos != pre_move_list[len(move_list)]: off_track = True
                            else: off_track = True
                        print(pos)
                        
                        move_list.append(pos)
                        draw_move_list.append(pos)
                        moves = chessPY.get_moves(pos, board)
                        if board_flip and pos.split(' ')[1] == 'b':
                            flipped_board = flip_board(board)
                            flipped_moves = flip_moves(moves)
                        selected = False
                        
                        if moves == [[[] for i in range(8)] for j in range(8)]:
                            print('White won' if pos.split(' ')[1] == 'b' else 'Black won')
                            if not pre_move_list:
                                running = False
                                break
                        if pos.split(' ')[4] == '50':
                            print('Draw by 50 move rule')
                            if not pre_move_list:
                                running = False
                                break
                        if [i.split(' ')[0] for i in draw_move_list].count(pos.split(' ')[0]) >= 3:
                            print('Draw by repetition')
                            if not pre_move_list:
                                running = False
                                break

                    elif board[new_selected[1]][new_selected[0]] == '0': selected = False
                    else: selected = new_selected
                else:
                    if board[new_selected[1]][new_selected[0]] == '0': selected = False
                    else: selected = new_selected
        
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_LEFT:
                if len(move_list) > 1:
                    move_list.pop()
                    if draw_move_list != []: draw_move_list.pop()
                    pos = move_list[-1]
                    board = FEN_to_board(pos)
                    moves = chessPY.get_moves(pos, board)
                    if board_flip and pos.split(' ')[1] == 'b':
                        flipped_board = flip_board(board)
                        flipped_moves = flip_moves(moves)
                    print(pos)
                    selected = False
                    if pre_move_list and len(move_list) <= len(pre_move_list):
                        if pos == pre_move_list[len(move_list)-1]: off_track = False
                    
            elif event.key == pygame.K_RIGHT:
                if not off_track and len(move_list) < len(pre_move_list):
                    pos = pre_move_list[len(move_list)]
                    board = FEN_to_board(pos)
                    moves = chessPY.get_moves(pos, board)
                    if board_flip and pos.split(' ')[1] == 'b':
                        flipped_board = flip_board(board)
                        flipped_moves = flip_moves(moves)
                    print(pos)
                    move_list.append(pos)
                    draw_move_list.append(pos)
                    selected = False
                    
                    # if moves == [[[] for i in range(8)] for j in range(8)]:
                    #     print('White won' if pos.split(' ')[1] == 'b' else 'Black won')
                    #     running = False
                    #     break
                    # if pos.split(' ')[4] == '50':
                    #     print('Draw by 50 move rule')
                    #     running = False
                    #     break
                    # if [i.split(' ')[0] for i in draw_move_list].count(pos.split(' ')[0]) >= 3:
                    #     print('Draw by repetition')
                    #     running = False
                    #     break

        elif event.type == pygame.VIDEORESIZE:
            window_size = maintain_aspect_ratio(event.size)
            print(window_size)

            pieces = transform_scale(original_pieces, window_size[0], window_size[1])
            
            capture_screen = pygame.Surface((window_size[0]/8, window_size[1]/8), pygame.SRCALPHA)
            move_screen = pygame.Surface((window_size[0]/8, window_size[1]/8), pygame.SRCALPHA)
            off_track_screen = pygame.Surface((window_size[0], window_size[1]), pygame.SRCALPHA)
            pygame.draw.circle(capture_screen,(100, 100, 100, 100), 
                            ((window_size[0]/16), (window_size[1]/16)), 
                            window_size[1]//16, window_size[1]//90)
            pygame.draw.circle(move_screen,(100, 100, 100, 100), 
                            ((window_size[0]/16), (window_size[1]/16)), 
                            window_size[1]//50)
            
            screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)

    if board_flip and pos.split(' ')[1] == 'b':
        for i in range(0, 8):
            for j in range(0, 8):
                screen.blit(pieces[flipped_board[j][i]][(i+j)%2], 
                            (i*window_size[0]/8, j*window_size[1]/8))
    else:
        for i in range(0, 8):
            for j in range(0, 8):
                screen.blit(pieces[board[j][i]][(i+j)%2], 
                            (i*window_size[0]/8, j*window_size[1]/8))
    
    if selected:
        if board_flip and pos.split(' ')[1] == 'b':
            flipped_selected = (7 - selected[0], 7 - selected[1])
            pygame.draw.rect(screen, (245, 246, 130) if (selected[0] + selected[1]) % 2 == 0 else (185, 202, 67),
                                pygame.Rect(flipped_selected[0] * window_size[0]/8, flipped_selected[1] * window_size[1]/8, 
                                            window_size[0]/8, window_size[1]/8), 
                                window_size[0]//128)
            for move in moves[selected[1]][selected[0]]:
                if board[move[1]][move[0]] == '0':
                    screen.blit(move_screen, ((7-move[0]) * window_size[0]/8, (7-move[1]) * window_size[1]/8))
                else:
                    screen.blit(capture_screen, ((7-move[0]) * window_size[0]/8, (7-move[1]) * window_size[1]/8))
        else:
            pygame.draw.rect(screen, (245, 246, 130) if (selected[0] + selected[1]) % 2 == 0 else (185, 202, 67),
                                pygame.Rect(selected[0] * window_size[0]/8, selected[1] * window_size[1]/8, 
                                            window_size[0]/8, window_size[1]/8), 
                                window_size[0]//128)
            for move in moves[selected[1]][selected[0]]:
                if board[move[1]][move[0]] == '0':
                    screen.blit(move_screen, (move[0] * window_size[0]/8, move[1] * window_size[1]/8))
                else:
                    screen.blit(capture_screen, (move[0] * window_size[0]/8, move[1] * window_size[1]/8))
    
    if off_track: screen.blit(off_track_screen, (0, 0))
    
    pygame.display.flip()

pygame.quit()
sys.exit()