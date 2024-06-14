from chess import system
import pygame
import chessPY

system("echo ChessAI")

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
pygame.draw.circle(capture_screen,(100, 100, 100, 100), 
                   ((original_width/16), (original_height/16)), original_height//16, original_height//90)
pygame.draw.circle(move_screen,(100, 100, 100, 100), 
                   ((original_width/16), (original_height/16)), original_height//50)

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

init_pos = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
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
pos = init_pos
print(pos)

move_list = [pos]
selected = False

window_size = (original_width, original_height)
running = True
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
                        pos, board = chessPY.make_move(pos, selected, new_selected, board)
                        print(pos)
                        
                        move_list.append(pos)
                        moves = chessPY.get_moves(pos, board)
                        if board_flip and pos.split(' ')[1] == 'b':
                            flipped_board = flip_board(board)
                            flipped_moves = flip_moves(moves)
                        selected = False

                    elif board[new_selected[1]][new_selected[0]] == '0': selected = False
                    else: selected = new_selected
                else:
                    if board[new_selected[1]][new_selected[0]] == '0': selected = False
                    else: selected = new_selected
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if len(move_list) > 1:
                    move_list.pop()
                    pos = move_list[-1]
                    board = FEN_to_board(pos)
                    moves = chessPY.get_moves(pos, board)
                    if board_flip and pos.split(' ')[1] == 'b':
                        flipped_board = flip_board(board)
                        flipped_moves = flip_moves(moves)
                    print(pos)
                    selected = False

        elif event.type == pygame.VIDEORESIZE:
            window_size = maintain_aspect_ratio(event.size)
            print(window_size)

            pieces = transform_scale(original_pieces, window_size[0], window_size[1])
            
            capture_screen = pygame.Surface((window_size[0]/8, window_size[1]/8), pygame.SRCALPHA)
            move_screen = pygame.Surface((window_size[0]/8, window_size[1]/8), pygame.SRCALPHA)
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
    
    pygame.display.flip()

pygame.quit()
sys.exit()