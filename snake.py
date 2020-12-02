import pygame
import sys
import random
import math

class Snake():
    def __init__(self, type="walls"):
        self.length = 1
        self.positions = [((screen_width/2), (screen_height/2))]
        self.direction = random.choice([up, down, left, right])
        self.color = (13, 250, 144)
        # Special thanks to YouTubers Mini - Cafetos and Knivens Beast for raising this issue!
        # Code adjustment courtesy of YouTuber Elija de Hoog
        self.score = 0
        self.lives = 10000
        self.sum_score = 0
        self.time = 0
        self.sum_time = 0
        self.type = type

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0]*-1, point[1]*-1) == self.direction:
            return
        else:
            self.direction = point

    def new_move(self, cur, x, y):
        if self.type == "no walls":
            new = (((cur[0]+(x*gridsize))%screen_width), (cur[1]+(y*gridsize))%screen_height)
        elif self.type == "walls":
            new = (((cur[0]+(x*gridsize))), (cur[1]+(y*gridsize)))
        return new

    def move(self):
        cur = self.get_head_position()
        x,y = self.direction
        new = self.new_move(cur, x, y)
        if (len(self.positions) > 2 and new in self.positions[2:]) or not (new[0] >= 0 and new[1] >= 0 and new[0] <= screen_width - gridsize and new[1] <= screen_height - gridsize):
            self.lives -= 1
            if self.lives > 0:
                self.reset()
            print("LOST")
        else:
            self.positions.insert(0,new)
            if len(self.positions) > self.length:
                self.positions.pop()


    def reset(self):
        self.length = 1
        self.positions = [((screen_width/2), (screen_height/2))]
        self.direction = random.choice([up, down, left, right])
        self.score = 0
        self.time = 0

    def draw(self,surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (gridsize,gridsize))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, (0,0, 0), r, 1)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(up)
                elif event.key == pygame.K_DOWN:
                    self.turn(down)
                elif event.key == pygame.K_LEFT:
                    self.turn(left)
                elif event.key == pygame.K_RIGHT:
                    self.turn(right)

    def get_possible_moves(self):
        moves = []
        head = self.get_head_position()
        #print(self.positions)
        x,y = up
        new = self.new_move(head, x, y)
        if new not in self.positions and new[0] >= 0 and new[1] >= 0 and new[0] <= screen_width - gridsize and new[1] <= screen_height - gridsize:
            #print("UP")
            moves.append(up)
        x,y = down
        new = self.new_move(head, x, y)
        if new not in self.positions and new[0] >= 0 and new[1] >= 0 and new[0] <= screen_width - gridsize and new[1] <= screen_height - gridsize:
            #print("DOWN")
            moves.append(down)
        x,y = left
        new = self.new_move(head, x, y)
        if new not in self.positions and new[0] >= 0 and new[1] >= 0 and new[0] <= screen_width - gridsize and new[1] <= screen_height - gridsize:
            #print("LEFT")
            moves.append(left)
        x,y = right
        new = self.new_move(head, x, y)
        if new not in self.positions and new[0] >= 0 and new[1] >= 0 and new[0] <= screen_width - gridsize and new[1] <= screen_height - gridsize:
            #print("RIGHT")
            moves.append(right)
        return moves

    def heuristic_move(self, food, mode):
        moves = self.get_possible_moves()
        head = self.get_head_position()
        bestMove = 0
        distance = 10000000
        #print(moves)
        if len(moves) != 0:
            if mode == "random":
                bestMoves = moves
            if self.type == "walls":
                if mode == "euclides":
                    for move in moves:
                        x, y = move
                        new = self.new_move(head, x, y)
                        if math.sqrt((new[0] - food.position[0])**2 + (new[1] - food.position[1])**2) < distance:
                            distance = math.sqrt((new[0] - food.position[0])**2 + (new[1] - food.position[1])**2)
                            bestMoves = [move]
                if mode == "taxi":
                    for move in moves:
                        x, y = move
                        new = self.new_move(head, x, y)
                        if abs(new[0] - food.position[0]) + abs(new[1] - food.position[1]) < distance:
                            distance = abs(new[0] - food.position[0]) + abs(new[1] - food.position[1])
                            bestMoves = [move]
                if mode == "taxirandom":
                    for move in moves:
                        x, y = move
                        new = self.new_move(head, x, y)
                        if abs(new[0] - food.position[0]) + abs(new[1] - food.position[1]) < distance:
                            distance = abs(new[0] - food.position[0]) + abs(new[1] - food.position[1])
                            bestMoves = [move]
                        if abs(new[0] - food.position[0]) + abs(new[1] - food.position[1]) == distance:
                            bestMoves.append(move)

            elif self.type == "no walls":
                if mode == "euclides":
                    for move in moves:
                        x, y = move
                        new = self.new_move(head, x, y)
                        if math.sqrt(min((new[0] - food.position[0] - screen_width)**2, (new[0] - food.position[0])**2, (new[0] - food.position[0] + screen_width)**2) + min((new[1] - food.position[1] - screen_height)**2, (new[1] - food.position[1])**2, (new[1] - food.position[1] + screen_height)**2)) < distance:
                            distance = math.sqrt(min((new[0] - food.position[0] - screen_width)**2, (new[0] - food.position[0])**2, (new[0] - food.position[0] + screen_width)**2) + min((new[1] - food.position[1] - screen_height)**2, (new[1] - food.position[1])**2, (new[1] - food.position[1] + screen_height)**2))
                            bestMoves = [move]
                if mode == "taxi":
                    for move in moves:
                        x, y = move
                        new = self.new_move(head, x, y)
                        if min(abs(new[0] - food.position[0] - screen_width), abs(new[0] - food.position[0]), abs(new[0] - food.position[0] + screen_width)) + min(abs(new[1] - food.position[1] - screen_height), abs(new[1] - food.position[1]), abs(new[1] - food.position[1] + screen_height)) < distance:
                            distance = min(abs(new[0] - food.position[0] - screen_width), abs(new[0] - food.position[0]), abs(new[0] - food.position[0] + screen_width)) + min(abs(new[1] - food.position[1] - screen_height), abs(new[1] - food.position[1]), abs(new[1] - food.position[1] + screen_height))
                            bestMoves = [move]
                if mode == "taxirandom":
                    for move in moves:
                        x, y = move
                        new = self.new_move(head, x, y)
                        if min(abs(new[0] - food.position[0] - screen_width), abs(new[0] - food.position[0]), abs(new[0] - food.position[0] + screen_width)) + min(abs(new[1] - food.position[1] - screen_height), abs(new[1] - food.position[1]), abs(new[1] - food.position[1] + screen_height)) < distance:
                            distance = min(abs(new[0] - food.position[0] - screen_width), abs(new[0] - food.position[0]), abs(new[0] - food.position[0] + screen_width)) + min(abs(new[1] - food.position[1] - screen_height), abs(new[1] - food.position[1]), abs(new[1] - food.position[1] + screen_height))
                            bestMoves = [move]
                        if min(abs(new[0] - food.position[0] - screen_width), abs(new[0] - food.position[0]), abs(new[0] - food.position[0] + screen_width)) + min(abs(new[1] - food.position[1] - screen_height), abs(new[1] - food.position[1]), abs(new[1] - food.position[1] + screen_height)) == distance:
                            bestMoves.append(move)

            self.turn(random.choice(bestMoves))

class Food():
    def __init__(self, snake):
        self.position = (0,0)
        self.color = (255, 0, 0)
        self.randomize_position(snake)

    def randomize_position(self, snake):
        self.position = (random.randint(0, grid_width-1)*gridsize, random.randint(0, grid_height-1)*gridsize)
        while self.position in snake.positions:
            self.position = (random.randint(0, grid_width-1)*gridsize, random.randint(0, grid_height-1)*gridsize)

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (gridsize, gridsize))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (0, 0, 0), r, 1)

def drawGrid(surface):
    for y in range(0, int(grid_height)):
        for x in range(0, int(grid_width)):
            if (x+y)%2 == 0:
                r = pygame.Rect((x*gridsize, y*gridsize), (gridsize,gridsize))
                pygame.draw.rect(surface,(0,0,0), r)
            else:
                rr = pygame.Rect((x*gridsize, y*gridsize), (gridsize,gridsize))
                pygame.draw.rect(surface, (0,0,0), rr)

screen_width = 800
screen_height = 800

gridsize = 10
grid_width = screen_width/gridsize
grid_height = screen_height/gridsize

up = (0,-1)
down = (0,1)
left = (-1,0)
right = (1,0)

def main():
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    drawGrid(surface)

    snake = Snake("no walls")
    food = Food(snake)

    myfont = pygame.font.SysFont("monospace",16)

    while (True):
        clock.tick(50)
        snake.handle_keys()
        drawGrid(surface)
        snake.heuristic_move(food, "taxi")
        snake.move()
        if snake.get_head_position() == food.position:
            snake.length += 1
            snake.score += 1
            snake.sum_score += 1
            food.randomize_position(snake)
        snake.time += 0.02
        snake.sum_time += 0.02
        snake.draw(surface)
        food.draw(surface)
        screen.blit(surface, (0,0))
        #score = myfont.render("Score {0}".format(snake.score), 1, (255,255,255))
        #screen.blit(score, (5,10))
        #lives = myfont.render("Lives {0}".format(snake.lives), 1, (255,255,255))
        #screen.blit(lives, (screen_width - 100,10))
        #time = myfont.render("Time {0}".format(snake.time), 1, (255,255,255))
        #screen.blit(time, (5,screen_height - 30))
        pygame.display.update()

main()
