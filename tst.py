import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
import numpy as np

TF_ENABLE_ONEDNN_OPTS = 0
print("TF version:", tf.__version__)

import chessPY

original_width, original_height = 640, 640
aspect_ratio = original_width / original_height

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

init_pos = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

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

model = tf.keras.models.Sequential([
  tf.keras.layers.Dense(768, activation='relu'),
  tf.keras.layers.Dense(1)
])

while running:
    
    # get moves
    moves = chessPY.get_moves(pos, board)
    
    predictions = [[np.zeros([0,]) for i in range(8)] for j in range(8)]
    for row in range(8):
        for move_set in range(8):
            if moves[row][move_set] != []:

                piece_moves = [chessPY.make_move(
                    pos, (move_set, row), move, board) for move in moves[row][move_set]]
                
                move_input = np.array([chessPY.board_to_neural(
                    future_board, True if future_pos.split(' ')[1] == 'b' else False) 
                                                    for future_pos, future_board in piece_moves])
                print(move_input.shape)
                predictions[row][move_set] = model.predict(move_input)
                print(predictions[row][move_set].tolist())
                print()
            
    # print(move_input[6][7].shape)
            
            # for move in moves[row][move_set]:
            #     future_pos, future_board = chessPY.make_move(pos, (move_set, row), move, board)
            #     a = chessPY.board_to_neural(
            #         future_board, True if future_pos.split(' ')[1] == 'b' else False)
            #     move_input[row][move_set] = np.vstack([move_input[row][move_set], a])
            #     print(a.shape, move_input[row][move_set].shape)
                # move_input[row][move_set].append(
                #     chessPY.board_to_neural(
                #         future_board, True if future_pos.split(' ')[1] == 'b' else False))
    
    # print(move_input[7][6])
                
    # input = chessPY.board_to_neural(board, True if pos.split(' ')[1] == 'w' else False)
    # input = tf.reshape(move_input[7][6],shape=(1,768))
    
    # for row in range(8):
    #     for move_set in range(8):
    #         # print(move_input[row][move_set], end=' ')
    #         if move_input[row][move_set].tolist() != []:
                
    #             predictions[row][move_set] = model.predict(move_input[row][move_set])
            # print(move_input[row][move_set].shape) if move_input[row][move_set].tolist() != [] else print('n')
    
    # print(move_input[6][6].shape)
    # prediction = model.predict(move_input[6][6])
    # print(prediction.shape)
    # print(prediction.tolist())
    
    # print(move_input[7][0])
    # prediction = model.predict(move_input[7][6])
    # print(prediction.shape)
    # print(prediction.tolist())
    
    # print(predictions)
    
    running = False


# while running:

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
        
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             if pygame.mouse.get_pressed()[0]:
#                 x, y = pygame.mouse.get_pos()
#                 new_selected = (int(x/(window_size[0]/8)), int(y/(window_size[1]/8)))
#                 if board_flip and pos.split(' ')[1] == 'b': new_selected = (7 - new_selected[0], 7 - new_selected[1])

#                 if selected:
#                     if new_selected in moves[selected[1]][selected[0]]:
#                         pos, board = chessPY.make_move(pos, selected, new_selected, board)
#                         print(pos)
                        
#                         move_list.append(pos)
#                         moves = chessPY.get_moves(pos, board)
#                         if board_flip and pos.split(' ')[1] == 'b':
#                             flipped_board = flip_board(board)
#                             flipped_moves = flip_moves(moves)
#                         selected = False

#                     elif board[new_selected[1]][new_selected[0]] == '0': selected = False
#                     else: selected = new_selected
#                 else:
#                     if board[new_selected[1]][new_selected[0]] == '0': selected = False
#                     else: selected = new_selected
        
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_LEFT:
#                 if len(move_list) > 1:
#                     move_list.pop()
#                     pos = move_list[-1]
#                     board = FEN_to_board(pos)
#                     moves = chessPY.get_moves(pos, board)
#                     if board_flip and pos.split(' ')[1] == 'b':
#                         flipped_board = flip_board(board)
#                         flipped_moves = flip_moves(moves)
#                     print(pos)
#                     selected = False

#         elif event.type == pygame.VIDEORESIZE:
#             window_size = maintain_aspect_ratio(event.size)
#             print(window_size)

#             pieces = transform_scale(original_pieces, window_size[0], window_size[1])
            
#             capture_screen = pygame.Surface((window_size[0]/8, window_size[1]/8), pygame.SRCALPHA)
#             move_screen = pygame.Surface((window_size[0]/8, window_size[1]/8), pygame.SRCALPHA)
#             pygame.draw.circle(capture_screen,(100, 100, 100, 100), 
#                             ((window_size[0]/16), (window_size[1]/16)), 
#                             window_size[1]//16, window_size[1]//90)
#             pygame.draw.circle(move_screen,(100, 100, 100, 100), 
#                             ((window_size[0]/16), (window_size[1]/16)), 
#                             window_size[1]//50)
            
#             screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)

#     if board_flip and pos.split(' ')[1] == 'b':
#         for i in range(0, 8):
#             for j in range(0, 8):
#                 screen.blit(pieces[flipped_board[j][i]][(i+j)%2], 
#                             (i*window_size[0]/8, j*window_size[1]/8))
#     else:
#         for i in range(0, 8):
#             for j in range(0, 8):
#                 screen.blit(pieces[board[j][i]][(i+j)%2], 
#                             (i*window_size[0]/8, j*window_size[1]/8))
    
#     if selected:
#         if board_flip and pos.split(' ')[1] == 'b':
#             flipped_selected = (7 - selected[0], 7 - selected[1])
#             pygame.draw.rect(screen, (245, 246, 130) if (selected[0] + selected[1]) % 2 == 0 else (185, 202, 67),
#                                 pygame.Rect(flipped_selected[0] * window_size[0]/8, flipped_selected[1] * window_size[1]/8, 
#                                             window_size[0]/8, window_size[1]/8), 
#                                 window_size[0]//128)
#             for move in moves[selected[1]][selected[0]]:
#                 if board[move[1]][move[0]] == '0':
#                     screen.blit(move_screen, ((7-move[0]) * window_size[0]/8, (7-move[1]) * window_size[1]/8))
#                 else:
#                     screen.blit(capture_screen, ((7-move[0]) * window_size[0]/8, (7-move[1]) * window_size[1]/8))
#         else:
#             pygame.draw.rect(screen, (245, 246, 130) if (selected[0] + selected[1]) % 2 == 0 else (185, 202, 67),
#                                 pygame.Rect(selected[0] * window_size[0]/8, selected[1] * window_size[1]/8, 
#                                             window_size[0]/8, window_size[1]/8), 
#                                 window_size[0]//128)
#             for move in moves[selected[1]][selected[0]]:
#                 if board[move[1]][move[0]] == '0':
#                     screen.blit(move_screen, (move[0] * window_size[0]/8, move[1] * window_size[1]/8))
#                 else:
#                     screen.blit(capture_screen, (move[0] * window_size[0]/8, move[1] * window_size[1]/8))
    
#     pygame.display.flip()

# pygame.quit()
# sys.exit()