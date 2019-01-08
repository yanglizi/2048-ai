import random
import pygame
import time
import copy

from board import *

from ai_2048 import *

screen_width = 640
screen_height = 640
block_width = 640
block_height = 640


def rectangle(scr, x, y, size):
    pygame.draw.rect(scr, (0,0,0), (x,y,x+size,y+size), 3)

def draw_board(screen, b):
    size = int(block_width / 4)

    screen.fill((255, 255, 255))
    # screen.blit(screen, (0, 200))
    font1 = pygame.font.SysFont('arial', 28)

    for x in range(0,block_width ,size):
        for y in range(0,block_height,size):
            val = b[int(y/size)][int(x/size)]
            rectangle(scr, x, y+screen_height-block_height, size)
            # print x, y+screen_height-block_height
            if val != 0:
                color = (255,255,255)
                text = font1.render(str(val),True,(0,0,255), color)
                screen.blit(text, (x+size/2, y+screen_height-block_height+size/2))
    pygame.display.flip()

def init_graphics():
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    return screen




# main loop
def main_loop(scr, b):
    try:
        init(board)
        print_board(board)
        TotalScore = 0
        # pygame.display.flip()
        while 1:
            score = 0
            b_before = copy.deepcopy(b)
            event = pygame.event.wait()
            # print event
            if event.type == pygame.QUIT:
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.unicode == 'q':
                    break
                if event.key == pygame.K_UP:
                    score = up(b)
                    # print score
                if event.key == pygame.K_LEFT:
                    score = left(b)
                if event.key == pygame.K_DOWN:
                    score = down(b)
                if event.key == pygame.K_RIGHT:
                    score = right(b)
                b_after = copy.deepcopy(b)
                if is_board_changed(b_before,b_after) == False:
                    # print is_board_changed(b_before,b_after)
                    if is_game_over(b):
                        print 'Game Over'
                    continue
                TotalScore = TotalScore + score
                print TotalScore
                # print maxvalue(b)
                if is_win(b):
                    print 'You win!'               
                generate(b)
                print_board(b)            
            draw_board(scr, b)
            time.sleep(0.05)
    finally:
        pygame.quit()


# ai do
def ai_do(scr, b):
    try:
        init(board)
        while 1:
            result = alphabeta_minimax(b , -100000 , 100000 , 0 , 4)

            dirc = result[1]

            # print result

            if dirc == ' ':
                print 'You lost!'
                time.sleep(2)
                return 0

            direction[dirc](b)
            generate(b)

            print_board(b)
            draw_board(scr, b)

            if is_win(b):
                print 'You win!'
                time.sleep(2)
                return 1
            

    finally:
        pygame.quit()

def winning_rate(b):
    total_time = 0
    win_time = 0
    while 1:
        win_time += ai_do(scr, b)
        total_time += 1
        print win_time,total_time
        if total_time == 50:
            break



# # ai do_2
# def ai_do_2(scr, b):
#     try:
#         depth = 0
#         while depth < 5:
#             print depth
#             newBest = alphabeta_minimax2(b, -10000, 10000, depth, 0 ,0)
#             # print newBest
#             if newBest['move'] == 'null':
#                 print 'null'
#                 break
#             else:
#                 best = newBest
#             depth += 1
#         direction[best['move']](b)
#         generate(b)
#         print_board(b)

#     finally:
#         pass






# winning_rate(board)


if __name__ == '__main__':

    scr = init_graphics()

    # main_loop(scr,board)
    # winning_rate(board)
    ai_do(scr,board)