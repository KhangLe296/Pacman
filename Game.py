import pygame 
from sys import exit
from board import board
import math
from board import WIDTH, HEIGHT, BLOCK_SIZE, WALL_THICKNESS
from Pacman import Pacman
from Ghost import *
pi = math.pi
SPEED = 3
pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('PACMAN')
clock = pygame.time.Clock()
score = 0
directions = [[0, -1], [0, 1], [1, 0], [-1, 0]]
lives = 3
count = 4
paused = True
new_board = []
lives_image = pygame.transform.scale(pygame.image.load(f'ASSETS/1.png'), (24, 24))
win = False

for i in range(len(board)):
    list_board = []
    for j in range(len(board[0])):
        list_board.append(board[i][j])
    new_board.append(list_board)

def draw_board(board, screen):
    n = len(board)
    m = len(board[0])
    center_point = (BLOCK_SIZE - WALL_THICKNESS)/2
    for i in range(n):
        for j in range(m):
            if board[i][j] == 1: # SMALL DOT
                pygame.draw.circle(screen, 'white', (BLOCK_SIZE * j + BLOCK_SIZE / 2, BLOCK_SIZE * i + BLOCK_SIZE / 2), WALL_THICKNESS)
            if board[i][j] == 2: # POWERUP DOT
                pygame.draw.circle(screen, 'red', (BLOCK_SIZE * j + BLOCK_SIZE / 2, BLOCK_SIZE * i + BLOCK_SIZE / 2), WALL_THICKNESS + 3)
            if board[i][j] == 3: # VERTICAL WALL
                pygame.draw.rect(screen, 'blue', pygame.Rect(BLOCK_SIZE * j + center_point, BLOCK_SIZE * i, WALL_THICKNESS, BLOCK_SIZE))
            if board[i][j] == 4: # HORIZONTAL WALL
                pygame.draw.rect(screen, 'blue', pygame.Rect(BLOCK_SIZE * j, BLOCK_SIZE * i + center_point, BLOCK_SIZE, WALL_THICKNESS))
            if board[i][j] == 5:
                pygame.draw.arc(screen, 'blue', [BLOCK_SIZE * j - center_point - WALL_THICKNESS, BLOCK_SIZE * i + center_point, BLOCK_SIZE + WALL_THICKNESS, BLOCK_SIZE + WALL_THICKNESS], 0, pi / 2, WALL_THICKNESS)
            if board[i][j] == 6:
                pygame.draw.arc(screen, 'blue', [BLOCK_SIZE * j + center_point, BLOCK_SIZE * i + center_point, BLOCK_SIZE + WALL_THICKNESS, BLOCK_SIZE + WALL_THICKNESS], pi/2,pi,WALL_THICKNESS)
            if board[i][j] == 7:
                pygame.draw.arc(screen, 'blue', [BLOCK_SIZE * j + center_point, BLOCK_SIZE * i - center_point - WALL_THICKNESS, BLOCK_SIZE + WALL_THICKNESS, BLOCK_SIZE + WALL_THICKNESS], pi,3*pi/2,WALL_THICKNESS)
            if board[i][j] == 8:
                pygame.draw.arc(screen, 'blue', [BLOCK_SIZE * j - center_point - WALL_THICKNESS, BLOCK_SIZE * i - center_point - WALL_THICKNESS, BLOCK_SIZE + WALL_THICKNESS, BLOCK_SIZE + WALL_THICKNESS], 3*pi/2, 2*pi, WALL_THICKNESS)
            if board[i][j] == 9: # GATE
                pygame.draw.rect(screen, 'white', pygame.Rect(BLOCK_SIZE * j, BLOCK_SIZE * i + center_point, BLOCK_SIZE, WALL_THICKNESS))

def draw_score(screen):
    font = pygame.font.Font('freesansbold.ttf', 32)

    text = font.render(f'Score: {score}', True, 'white')

    textRect = text.get_rect()

    textRect.topleft = (len(board) * 24, 100)

    screen.blit(text, textRect)

def draw_lives(screen):
    for i in range(lives):
        screen.blit((lives_image), (len(board) * 24 + (i * 26), 50))

def draw_resart(screen):
    font = pygame.font.Font('freesansbold.ttf', 32)

    text = font.render(f'PRESS SPACE BAR TO RESTART', True, 'yellow')

    textRect = text.get_rect()

    textRect.center = (WIDTH // 2, HEIGHT // 2 + 30)

    screen.blit(text, textRect)

def draw_win(screen):
    font = pygame.font.Font('freesansbold.ttf', 32)

    text = font.render(f'YOU WON', True, 'yellow')

    textRect = text.get_rect()

    textRect.center = (WIDTH // 2, HEIGHT // 2)

    screen.blit(text, textRect)

def draw_game_over(screen):
    font = pygame.font.Font('freesansbold.ttf', 32)

    text = font.render(f'GAME OVER', True, 'yellow')

    textRect = text.get_rect()

    textRect.center = (WIDTH // 2, HEIGHT // 2)

    screen.blit(text, textRect)

def draw_pause(screen):
    font = pygame.font.Font('freesansbold.ttf', 32)

    text = font.render(f'PRESS SPACE BAR TO PLAY', True, 'yellow')

    textRect = text.get_rect()

    textRect.center = (WIDTH // 2, HEIGHT // 2)

    screen.blit(text, textRect)

def draw_keep_going(screen):
    font = pygame.font.Font('freesansbold.ttf', 32)

    text = font.render(f'YOUR LIVES LEFT: {lives}', True, 'yellow')

    textRect = text.get_rect()

    textRect.center = (WIDTH // 2, HEIGHT // 2)

    screen.blit(text, textRect)

    font = pygame.font.Font('freesansbold.ttf', 32)

    text2 = font.render(f'PRESS SPACE BAR TO KEEP PLAYING', True, 'yellow')

    textRect2 = text2.get_rect()

    textRect2.center = (WIDTH // 2, HEIGHT // 2 + 30)

    screen.blit(text2, textRect2)

def restart_game():
    global pacman, blinky, clyde, inky, pinky, ghosts, score, lives
    pacman = Pacman(18 * BLOCK_SIZE, 15 * BLOCK_SIZE, SPEED)
    blinky = Blinky(12 * BLOCK_SIZE, 14 * BLOCK_SIZE, SPEED)
    clyde = Clyde(15 * BLOCK_SIZE, 16 * BLOCK_SIZE, SPEED)
    inky = Inky(15 * BLOCK_SIZE, 12 * BLOCK_SIZE, SPEED)
    pinky = Pinky(15 * BLOCK_SIZE, 14 * BLOCK_SIZE, SPEED)
    ghosts = [blinky, clyde, inky, pinky]
    score = 0
    lives =  3
    flag = False
    board.clear()
    for i in range(len(new_board)):
        list_board = []
        for j in range(len(new_board[0])):
            list_board.append(new_board[i][j])
        board.append(list_board)

def keep_going_game():
    global pacman, blinky, clyde, inky, pinky, ghosts, score, lives
    pacman = Pacman(18 * BLOCK_SIZE, 15 * BLOCK_SIZE, SPEED)
    blinky = Blinky(12 * BLOCK_SIZE, 14 * BLOCK_SIZE, SPEED)
    clyde = Clyde(15 * BLOCK_SIZE, 16 * BLOCK_SIZE, SPEED)
    inky = Inky(15 * BLOCK_SIZE, 12 * BLOCK_SIZE, SPEED)
    pinky = Pinky(15 * BLOCK_SIZE, 14 * BLOCK_SIZE, SPEED)
    ghosts = [blinky, clyde, inky, pinky]
    flag = False

pacman = Pacman(18 * BLOCK_SIZE, 15 * BLOCK_SIZE, SPEED)
blinky = Blinky(12 * BLOCK_SIZE, 14 * BLOCK_SIZE, SPEED)
clyde = Clyde(15 * BLOCK_SIZE, 16 * BLOCK_SIZE, SPEED)
inky = Inky(15 * BLOCK_SIZE, 12 * BLOCK_SIZE, SPEED) 
pinky = Pinky(15 * BLOCK_SIZE, 14 * BLOCK_SIZE, SPEED)
ghosts = []
ghosts.append(blinky)
ghosts.append(clyde)
ghosts.append(inky)
ghosts.append(pinky)

while True:
    clock.tick(30)
    flag = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_LEFT:
                pacman.auto_run = True
                pacman.next_direction = [0, -1]
            if event.key == pygame.K_RIGHT:
                pacman.auto_run = True
                pacman.next_direction = [0, 1]
            if event.key == pygame.K_UP:
                pacman.auto_run = True
                pacman.next_direction = [-1, 0]
            if event.key == pygame.K_DOWN:
                pacman.auto_run = True
                pacman.next_direction = [1, 0]
            if event.key == pygame.K_SPACE and (lives == 0 or win == True):
                restart_game()
                count = 4
            if event.key == pygame.K_SPACE and lives > 0:
                keep_going_game()
                count -= 1
            if event.key == pygame.K_SPACE and paused:
                paused = False

    if score == 246:
        screen.fill('black')
        draw_win(screen)
        draw_resart(screen)
        pygame.display.flip()
        win = True
        continue

    if paused:
        screen.fill('black')
        draw_pause(screen)
        pygame.display.flip()
        continue

    for ghost in ghosts:
        if ghost.eat_pacman(pacman):
            if pacman.is_chase_mode():
                ghost.spawn()
            else:
                flag = True
                lives = count - 1
                break
            
    if flag == True and lives > 0:
        pygame.display.flip()
        screen.fill('black')
        draw_keep_going(screen)
        continue
    elif flag == True and lives == 0:
        pygame.display.flip()
        screen.fill('black')
        draw_resart(screen)
        draw_game_over(screen)
        continue

    pacman.move()

    for ghost in ghosts:
        ghost.think(pacman)

    if pacman.eat():
        score += 1

    screen.fill((0, 0, 0))

    draw_board(board, screen)
    draw_lives(screen)
    draw_score(screen)

    pacman.draw(screen)  
    for ghost in ghosts:
        ghost.draw(screen, pacman)      

    pygame.display.flip()








