from board import *
from collections import deque
from Pacman import *
directions = [[0, -1], [0, 1], [1, 0], [-1, 0]]

class Ghost:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y 
        self.speed = speed * 2
        self.direction = [0, 0]
        self.powerup_image = pygame.transform.scale(pygame.image.load(f'ASSETS/GHOST/powerup.png'), (24, 24))
        self.x2 = 2
        self.y2 = 2
        self.scatter_targets = []
        self.exit_home = False
        self.og_x = 0
        self.og_y = 0
        self.in_cage = False
    
    def move(self):
        if not self.check_collision(board):
            self.x += self.direction[0] * self.speed
            self.y += self.direction[1] * self.speed
        
        if self.y >= len(board[0]) * BLOCK_SIZE:
            self.y = 0
        elif self.y <= 0:
            self.y = (len(board[0]) - 1) * BLOCK_SIZE
        
        if self.x >= len(board) * BLOCK_SIZE:
            self.x = 0
        elif self.x <= 0:
            self.x = (len(board) - 1) * BLOCK_SIZE

    def check_collision(self, board):
        if self.x % BLOCK_SIZE != 0 or self.y % BLOCK_SIZE != 0:
            return False
        
        next_board_x = self.get_board_x() + self.direction[0]
        next_board_y = self.get_board_y() + self.direction[1]

        if next_board_y == len(board[0]):
            next_board_y = 0

        if next_board_x == len(board):
            next_board_x = 0

        if board[next_board_x][next_board_y] in (3, 4, 5, 6, 7, 8):
            return True
        
        return False 
  
    def update_direction(self):
        if self.next_direction == self.direction:
            return
        
        if (self.direction[0] == 0 and self.next_direction[0] == 0) or (self.direction[1] == 0 and self.next_direction[1] == 0):
            self.direction[0] = self.next_direction[0]
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

    def get_board_x(self):
        return int(self.x // BLOCK_SIZE)
    
    def get_board_y(self):
        return int(self.y // BLOCK_SIZE)

    def draw(self, screen, pacman):
        if pacman.is_chase_mode():
            screen.blit((self.powerup_image), (self.y, self.x))
        else:
            screen.blit((self.image), (self.y, self.x))

    def think(self, pacman):
        if not pacman.is_chase_mode():
            self.in_cage = False
            if not pacman.is_chase_mode():
                (self.x2, self.y2) = (pacman.get_board_x(), pacman.get_board_y())
                self.exit_home = True
            else:
                if (self.get_board_x(), self.get_board_y()) == (15, 14):
                    return
                if self.exit_home:
                    self.x2, self.y2 = self.scatter_targets[0][0], self.scatter_targets[0][1]
                    self.exit_home = False

                self.update_target()
            self.next_direction[0], self.next_direction[1] = self.find_path_ghost_target(board, directions)
            self.update_direction()
            self.move()
        elif self.in_cage == True:
            return
        else:
            if not pacman.is_chase_mode():
                (self.x2, self.y2) = (pacman.get_board_x(), pacman.get_board_y())
                self.exit_home = True
            else:
                if (self.get_board_x(), self.get_board_y()) == (15, 14):
                    return
                if self.exit_home:
                    self.x2, self.y2 = self.scatter_targets[0][0], self.scatter_targets[0][1]
                    self.exit_home = False

                self.update_target()
            self.next_direction[0], self.next_direction[1] = self.find_path_ghost_target(board, directions)
            self.update_direction()
            self.move()
        
    def find_path_ghost_target(self, board, directions):
        N = len(board)
        M = len(board[0])
        q = deque([(self.get_board_x(), self.get_board_y(), [])])
        visit = set((self.get_board_x(), self.get_board_y()))
        if (self.get_board_x(), self.get_board_y()) == (self.x2, self.y2):
            return self.direction
        while q:
            r, c, path = q.popleft()
            if r == self.x2 and c == self.y2:
                return path[0]
            
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if min(nr, nc) >= 0 and nc < M and nr < N and board[nr][nc] not in (3, 4, 5, 6, 7, 8) and (nr, nc) not in visit:
                    q.append((nr, nc, path + [(dr, dc)]))
                    visit.add((nr, nc))

        return (0, 0)
    
    def eat_pacman(self, pacman):
        if (pacman.get_board_x(), pacman.get_board_y()) == (self.get_board_x(), self.get_board_y()):
            return True
        return False
    
    def update_target(self):
        if (self.get_board_x(), self.get_board_y()) == (self.x2, self.y2) == (self.scatter_targets[0][0], self.scatter_targets[0][1]):
            self.x2 = self.scatter_targets[1][0]
            self.y2 = self.scatter_targets[1][1]
        if (self.get_board_x(), self.get_board_y()) == (self.x2, self.y2) == (self.scatter_targets[1][0], self.scatter_targets[1][1]):
            self.x2 = self.scatter_targets[0][0]
            self.y2 = self.scatter_targets[0][1]
    
    def spawn(self):
        self.x = self.og_x 
        self.y = self.og_y
        self.in_cage = True

class Clyde(Ghost):
    def __init__(self, x, y, speed):
        super().__init__(x, y, speed)
        self.image = pygame.transform.scale(pygame.image.load(f'ASSETS/GHOST/orange.png'), (24, 24))
        self.next_direction = [-1, 0]
        self.x2 = 2
        self.y2 = 2
        self.scatter_targets = [(2, 2), (6, 13)]
        self.og_x = x
        self.og_y = y
class Inky(Ghost):
    def __init__(self, x, y, speed):
        super().__init__(x, y, speed)
        self.image = pygame.transform.scale(pygame.image.load(f'ASSETS/GHOST/blue.png'), (24, 24))
        self.next_direction = [-1, 0]
        self.x2 = 2
        self.y2 = 27
        self.scatter_targets = [(2, 27), (6, 16)]
        self.og_x = x
        self.og_y = y
class Blinky(Ghost):
    def __init__(self, x, y, speed):
        super().__init__(x, y, speed)
        self.image = pygame.transform.scale(pygame.image.load(f'ASSETS/GHOST/red.png'), (24, 24))
        self.next_direction = [-1, 0]
        self.x2 = 30
        self.y2 = 2
        self.scatter_targets = [(30, 2), (27, 13), (24, 7)]
        self.og_x = x
        self.og_y = y
    
    def update_target(self):
        for i in range(len(self.scatter_targets)):
            if (self.get_board_x(), self.get_board_y()) == (self.x2, self.y2) == (self.scatter_targets[i][0], self.scatter_targets[i][1]):
                self.x2 = self.scatter_targets[i + 1][0]
                self.y2 = self.scatter_targets[i + 1][1]
                break
            if (self.get_board_x(), self.get_board_y()) == (self.x2, self.y2) == (self.scatter_targets[2][0], self.scatter_targets[2][1]):
                self.x2 = self.scatter_targets[0][0]
                self.y2 = self.scatter_targets[0][1]
                i = 0
class Pinky(Ghost):
    def __init__(self, x, y, speed):
        super().__init__(x, y, speed)
        self.image = pygame.transform.scale(pygame.image.load(f'ASSETS/GHOST/pink.png'), (24, 24))
        self.next_direction = [-1, 0]
        self.x2 = 30
        self.y2 = 27
        self.scatter_targets = [(30, 27), (24, 19), (27, 16)]
        self.og_x = x
        self.og_y = y
    
    def update_target(self):
        for i in range(len(self.scatter_targets)):
            if (self.get_board_x(), self.get_board_y()) == (self.x2, self.y2) == (self.scatter_targets[i][0], self.scatter_targets[i][1]):
                self.x2 = self.scatter_targets[i + 1][0]
                self.y2 = self.scatter_targets[i + 1][1]
                break
            if (self.get_board_x(), self.get_board_y()) == (self.x2, self.y2) == (self.scatter_targets[2][0], self.scatter_targets[2][1]):
                self.x2 = self.scatter_targets[0][0]
                self.y2 = self.scatter_targets[0][1]
                i = 0
                break

