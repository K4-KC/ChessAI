from chess import system
import pygame

system("echo ChessAI")

import sys

pygame.init()

original_pieces = [[[pygame.image.load('E:/Projects/ChessAI/data/png/pieces/' + str(i) + str(j) + str(k) +'.png')
            for k in range(2)] 
           for j in range(6)] 
           for i in range(2)]

original_width, original_height = 640, 640
aspect_ratio = original_width / original_height

pieces = [[[pygame.transform.scale(original_pieces[i][j][k], (original_width//8, original_height//8))
            for k in range(2)] 
           for j in range(6)] 
           for i in range(2)]

screen = pygame.display.set_mode((original_width, original_height), pygame.RESIZABLE)

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

# board = [['00' for i in range(8)] for j in range(8)]
board = [['13', '10', 0, 0, 0, 0, '00', '03'],
         ['15', '10', 0, 0, 0, 0, '00', '05'],
         ['14', '10', 0, 0, 0, 0, '00', '04'],
         ['12', '10', 0, 0, 0, 0, '00', '02'],
         ['11', '10', 0, 0, 0, 0, '00', '01'],
         ['14', '10', 0, 0, 0, 0, '00', '04'],
         ['15', '10', 0, 0, 0, 0, '00', '05'],
         ['13', '10', 0, 0, 0, 0, '00', '03']]

window_size = (original_width, original_height)
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            window_size = maintain_aspect_ratio(event.size)

            pieces = [[[pygame.transform.scale(original_pieces[i][j][k], (window_size[0]//8, window_size[1]//8)) 
                        for k in range(2)] 
                        for j in range(6)] 
                        for i in range(2)]

            print(window_size)
            
            screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)

    for i in range(0, 8):
        for j in range(0, 8):
            if board[i][j] == 0:
                pygame.draw.rect(screen, (235 if (i+j)%2 == 0 else 118,
                                        236 if (i+j)%2 == 0 else 150,
                                        208 if (i+j)%2 == 0 else 86),
                                        pygame.Rect(i*window_size[0]/8, j*window_size[1]/8, window_size[0]/8, window_size[1]/8))
            else:
                screen.blit(pieces[int(board[i][j][0])][int(board[i][j][1])][(i+j)%2], 
                            (i*window_size[0]/8, j*window_size[1]/8))
    
    pygame.display.flip()

pygame.quit()
sys.exit()