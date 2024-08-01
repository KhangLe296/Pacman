from board import BLOCK_SIZE, board
import pygame
from Ghost import *
import time

class Pacman:
    def __init__(self, x, y, speed): # create all the materials needed for pacman
        self.x = x # position on window
        self.y = y # position on window
        self.speed = speed * 2 
        self.direction = [0, 1]
        self.next_direction = self.direction # next direction is the input from user
        self.pacman_images = []
        self.cur_frame = 0
        self.auto_run = False
        self.timer = 0
        for i in range(1, 5):
            self.pacman_images.append(pygame.transform.scale(pygame.image.load(f'ASSETS/{i}.png'), (24, 24)))

    def check_collision(self, board): # check collision between pacman and wall
        if self.x % BLOCK_SIZE != 0 or self.y % BLOCK_SIZE != 0: # check if pacman is in the middle of the pixel - if not return false
            return False

        next_board_x = self.get_board_x() + self.direction[0] # check in front of pacman to see if there is any walls
        next_board_y = self.get_board_y() + self.direction[1]

        if next_board_y == len(board[0]): # set back position of pacman when it moves through the tunnel
            next_board_y = 0

        if next_board_x == len(board):
            next_board_x = 0

        if board[next_board_x][next_board_y] in (3, 4, 5, 6, 7, 8, 9): # check collision with walls
            return True # return true so game knows there is obsticle ahead
        
        return False  # if not thing is detectdd return False so the game knows there is not obsticle ahead
    
    def eat(self):
        if self.x % BLOCK_SIZE != 0 or self.y % BLOCK_SIZE != 0: # also check if pacman is in middle of the pixel
            return False
        
        board_x = self.get_board_x() # get position of pacman on the board because using position of pacman on the window in pixel would make errors when calculating
        board_y = self.get_board_y()

        flag = False # flag to let game knows when a pellet is eaten or not 
        if board[board_x][board_y] == 2:
            self.Power_up()
        if board[board_x][board_y] in (1, 2): # set that position to 0 so in the next loop it does not draw that pellet on the window
            board[board_x][board_y] = 0
            flag = True
        
        return flag 

    def move(self):
        if self.auto_run == False: # this to check if pacman is currently moving or standing in one position 
            return

        self.update_direction() # to plug in the direction from input from user

        if not self.check_collision(board): # there is not obsticle ahead so the move is allowed # parameter is board since I need to use it for calculating 
            self.x += self.direction[0] * self.speed
            self.y += self.direction[1] * self.speed
        
        if self.y >= len(board[0]) * BLOCK_SIZE:      # set back position of pacman when it moves through tunnel
            self.y = 0
        elif self.y <= 0:
            self.y = (len(board[0]) - 1) * BLOCK_SIZE
        
        if self.x >= len(board) * BLOCK_SIZE:         # set back position of pacman when it moves through tunnel
            self.x = 0
        elif self.x <= 0:
            self.x = (len(board) - 1) * BLOCK_SIZE

    def update_direction(self):
        if self.next_direction == self.direction: # update direction is the direction from user input and if it is the same it the current direction there will be no changes     
            return
        
        if (self.direction[0] == 0 and self.next_direction[0] == 0) or (self.direction[1] == 0 and self.next_direction[1] == 0):
            self.direction[0] = self.next_direction[0]                                                          # check to match the input direction with the direction of pacman
            self.direction[1] = self.next_direction[1]
            return
        
        if self.direction[0] == 0 and self.next_direction[0] != 0 and self.y % BLOCK_SIZE == 0:
            self.direction[0] = self.next_direction[0]
            self.direction[1] = self.next_direction[1]
            return
        
        if self.direction[1] == 0 and self.next_direction[1] != 0 and self.x % BLOCK_SIZE == 0:
            self.direction[0] = self.next_direction[0]
            self.direction[1] = self.next_direction[1]
            return

    def get_board_x(self): # transfer the position of pacman on window to board
        return self.x // BLOCK_SIZE 
    
    def get_board_y(self): # transfer the position of pacman on window to board
        return self.y // BLOCK_SIZE
    
    def change_animation(self): # calculate the current frame for choosing one pictures in one of four for pacman
        self.cur_frame = (self.cur_frame + 1) % len(self.pacman_images)  # The modulus operation % len(self.pacman_images) resets the index to 0 after the last frame, so with 4 frames, self.cur_frame + 1 becomes 4, and 4 % 4 is 0, wrapping to the first frame
    
    def draw(self, screen): # draw base on direction of pacman
        self.change_animation()
        if self.direction [0] == 0 and self.direction[1] == 1:
            screen.blit(self.pacman_images[self.cur_frame], (self.y, self.x)) # Draw the current frame image on the screen at (self.y, self.x)
        elif self.direction [0] == 0 and self.direction[1] == -1:
            screen.blit(pygame.transform.flip(self.pacman_images[self.cur_frame], True, False), (self.y, self.x)) # Flip the current frame image horizontally and draw it on the screen at (self.y, self.x)
        elif self.direction [0] == -1 and self.direction[1] == 0:
            screen.blit(pygame.transform.rotate(self.pacman_images[self.cur_frame], 90), (self.y, self.x)) # Rotate the current frame image by 90 degrees and draw it on the screen at (self.y, self.x)
        elif self.direction [0] == 1 and self.direction[1] == 0:
            screen.blit(pygame.transform.rotate(self.pacman_images[self.cur_frame], 270), (self.y, self.x)) # Rotate the current frame image by 270 degrees and draw it on the screen at (self.y, self.x)


    def Power_up(self): 
        x = self.get_board_x()
        y = self.get_board_y()
        if board[x][y] == 2: # if pacman lands on the power-up than it activates set_chase_mode()
            self.set_chase_mode()
            return True
        return False

    def set_chase_mode(self):
        self.timer = time.time() + 15 # activates a timer of 15 seconds

    def is_chase_mode(self):
        if time.time() < self.timer: # check if the power-up is ended yet
            return True
        return False
    
    
