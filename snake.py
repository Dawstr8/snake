import pygame
import sys
import random
import math
import copy
import time

class Snake():
    def __init__(self, type="walls", mode="taxi"):
        self.length = 1
        self.positions = [(grid_width/2, grid_height/2)]
        self.direction = random.choice([up, down, left, right])
        self.color = (13, 250, 144)
        self.score = 0
        self.lives = 1
        self.sum_score = 0
        self.time = 0
        self.sum_time = 0
        self.type = type
        self.mode = mode
        self.next_moves = []
        self.moves = 0
        self.from_last = 0

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0]*-1, point[1]*-1) == self.direction:
            return
        else:
            self.direction = point

    def change_color(self):
        if len(self.next_moves) == 0:
            self.color = (255, 255, 255)
        else:
            self.color = (13, 250, 144)

    def new_move(self, cur, x, y):
        if self.type == "no walls":
            new = (((cur[0]+x)%grid_width), (cur[1]+y)%grid_height)
            #new = (((cur[0]+(x*gridsize))%screen_width), (cur[1]+(y*gridsize))%screen_height)
        elif self.type == "walls":
            new = ((cur[0]+x), (cur[1]+y))
            #new = (((cur[0]+(x*gridsize))), (cur[1]+(y*gridsize)))
        return new

    def move(self):
        cur = self.get_head_position()
        x,y = self.direction
        new = self.new_move(cur, x, y)
        if (len(self.positions) > 2 and new in self.positions[2:]) or not (new[0] >= 0 and new[1] >= 0 and new[0] < grid_width and new[1] < grid_height):
            self.lives -= 1
            if self.lives > 0:
                self.reset()
            print("LOST")
        else:
            self.positions.insert(0,new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def move_to(self, direction):
        cur = self.get_head_position()
        x,y = direction
        new = self.new_move(cur, x, y)
        if (len(self.positions) > 2 and new in self.positions[2:]) or not (new[0] >= 0 and new[1] >= 0 and new[0] < grid_width and new[1] < grid_height):
            self.lives -= 1
            if self.lives > 0:
                #self.reset()
                print("LOST")
        else:
            self.positions.insert(0,new)
            if len(self.positions) > self.length:
                self.positions.pop()


    def reset(self):
        self.length = 1
        self.positions = [(grid_width/2, grid_height/2)]
        self.direction = random.choice([up, down, left, right])
        self.score = 0
        self.time = 0

    def draw(self,surface):
        for p in self.positions:
            r = pygame.Rect((p[0]*gridsize, p[1]*gridsize), (gridsize,gridsize))
            #r = pygame.Rect((p[0], p[1]), (gridsize,gridsize))
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
        x,y = up
        new = self.new_move(head, x, y)
        if new not in self.positions and new[0] >= 0 and new[1] >= 0 and new[0] < grid_width and new[1] < grid_height:
            moves.append(up)
        x,y = down
        new = self.new_move(head, x, y)
        if new not in self.positions and new[0] >= 0 and new[1] >= 0 and new[0] < grid_width and new[1] < grid_height:
            moves.append(down)
        x,y = left
        new = self.new_move(head, x, y)
        if new not in self.positions and new[0] >= 0 and new[1] >= 0 and new[0] < grid_width and new[1] < grid_height:
            moves.append(left)
        x,y = right
        new = self.new_move(head, x, y)
        if new not in self.positions and new[0] >= 0 and new[1] >= 0 and new[0] < grid_width and new[1] < grid_height:
            moves.append(right)
        return moves

    def heuristic_move(self, food):
        node = Node(food, self, None, None)
        best_children = []
        distance = 10000000
        if len(node.get_children()) != 0:
            if self.mode == "taxi":
                for child in node.get_children():
                    child.distance_to_food()
                    if child.to_food < distance:
                        distance = child.to_food
                        best_children = [child]
            elif self.mode == "euclides":
                for child in node.get_children():
                    child.distance_to_food()
                    if child.to_food < distance:
                        distance = child.to_food
                        best_children = [child]
            elif self.mode == "taxirandom":
                for child in node.get_children():
                    child.distance_to_food()
                    if child.to_food < distance:
                        distance = child.to_food
                        best_children = [child]
                    if child.to_food == distance:
                        best_children.append(child)
            elif self.mode == "hamilton":
                for i in range(len(hamiltonian_cycle)):
                    if hamiltonian_cycle[i] == self.get_head_position():
                        head = i
                    if hamiltonian_cycle[i] == food.position:
                        food_position = i
                child = Node(food, self, None, (hamiltonian_cycle[(head+1)%(grid_width*grid_height)][0]-hamiltonian_cycle[head][0], hamiltonian_cycle[(head+1)%(grid_width*grid_height)][1] - hamiltonian_cycle[head][1]))
                best_children.append(child)
            elif self.mode == "hamilton with cut":
                head = self.get_head_position()
                children = []
                for move in self.get_possible_moves():
                    children.append([(head[0] + move[0], head[1] + move[1]), None])
                for i in range(len(hamiltonian_cycle)):
                    if hamiltonian_cycle[i] == self.get_head_position():
                        head_position = i
                    if hamiltonian_cycle[i] == food.position:
                        food_position = i
                    for child in children:
                        if hamiltonian_cycle[i] == child[0]:
                            child[1] = i
                #if food_position < head_position:
                #    best_child = Node(food, self, None, (hamiltonian_cycle[(head_position+1)%(grid_width*grid_height)][0]-hamiltonian_cycle[head_position][0], hamiltonian_cycle[(head_position+1)%(grid_width*grid_height)][1] - hamiltonian_cycle[head_position][1]))
                best_child = Node(food, self, None, (hamiltonian_cycle[(head_position+1)%(grid_width*grid_height)][0]-hamiltonian_cycle[head_position][0], hamiltonian_cycle[(head_position+1)%(grid_width*grid_height)][1] - hamiltonian_cycle[head_position][1]))
                best = (food_position - head_position - 1)%(grid_width*grid_height)
                if self.length < 0.5 * (grid_width * grid_height):
                    for child in children:
                        snake = node.get_snake()
                        snake.move_to((hamiltonian_cycle[child[1]][0]-hamiltonian_cycle[head_position][0], hamiltonian_cycle[child[1]][1] - hamiltonian_cycle[head_position][1]))
                        child_node = Node(food, snake, None, None)
                        child_node.distance_to_food()
                        distance_to_food = (food_position - child[1])%(grid_width*grid_height)
                        #distance_to_food =  +
                        distance_to_head = (head_position - child[1])%(grid_width*grid_height)
                        if distance_to_food < best:
                            can_go = True
                            for i in range((child[1] - head_position)%(grid_width*grid_height)):
                                if hamiltonian_cycle[(i + child[1])%(grid_width*grid_height)] in self.positions:
                                    can_go = False
                                    break
                            if can_go:
                                best = distance_to_food
                                best_child = Node(food, self, None, (hamiltonian_cycle[child[1]][0]-hamiltonian_cycle[head_position][0], hamiltonian_cycle[child[1]][1] - hamiltonian_cycle[head_position][1]))
                best_children.append(best_child)

            elif self.mode == "euclides best first search" or self.mode == "taxi best first search":
                new_directions = [[(0,-1), 0], [(0,1), 0], [(-1,0), 0], [(1,0), 0]]
                if len(self.next_moves) == 0:
                    for first_child in node.get_children():
                        start_node = first_child
                        open = [start_node]
                        closed = []
                        timeout = time.time() + 0.05 / len(node.get_children())
                        while len(open) != 0 and time.time() < timeout:
                            open.sort()
                            current_node = open.pop(0)
                            closed.append(current_node)
                            current_node.distance_to_food()
                            if current_node.to_food == 0:
                                path = []
                                while current_node != node:
                                    path.append(current_node)
                                    current_node = current_node.parent
                                # Return reversed path
                                self.next_moves =  path[::-1]
                                break
                            for child in current_node.get_children():
                                if child in closed:
                                    continue
                                if child not in open:
                                    child.distance_to_food()
                                    open.append(child)
                                    for new_direction in new_directions:
                                        if new_direction[0] == first_child.direction:
                                            if child.from_start > new_direction[1]:
                                                new_direction[1] = child.from_start

#                    if len(self.next_moves) == 0:
#                        for first_child in node.get_children():
#                            start_node = first_child
#                            open = [first_child]
#                            closed = []
#                            timeout = time.time() + 0.025
#                            while len(open) != 0 and time.time() < timeout:
#                                current_node = open.pop(0)
#                                closed.append(current_node)
#                                for child in current_node.get_children():
#                                    if child in closed:
#                                        continue
#                                    if child not in open:
#                                        for new_direction in new_directions:
#                                            if new_direction[0] == first_child.direction:
#                                                if child.from_start > new_direction[1]:
#                                                    new_direction[1] = child.from_start
#                                        open.append(child)
                    if len(self.next_moves) == 0:
                        best = 0
                        for new_direction in new_directions:
                            if best < new_direction[1]:
                                best = new_direction[1]
                                best_children = [Node(food, self, None, new_direction[0])]

            if len(self.next_moves) == 0 and len(best_children) != 0:
                best_child = random.choice(best_children)
                self.move_to(best_child.direction)
            elif len(self.next_moves) != 0:
                self.move_to(self.next_moves[0].direction)
                self.next_moves.pop(0)
            elif len(best_children) == 0:
                #self.reset()
                xd = "hey"
        else:
            #self.reset()
            xd = "hey"

class Food():
    def __init__(self, snake):
        self.position = (0,0)
        self.color = (255, 0, 0)
        self.randomize_position(snake)

    def randomize_position(self, snake):
        if snake.length != (grid_width * grid_height):
            self.position = (random.randint(0, grid_width-1), random.randint(0, grid_height-1))
            while self.position in snake.positions:
                self.position = (random.randint(0, grid_width-1), random.randint(0, grid_height-1))
                #self.position = (random.randint(0, grid_width-1)*gridsize, random.randint(0, grid_height-1)*gridsize)

    def draw(self, surface):
        r = pygame.Rect((self.position[0]*gridsize, self.position[1]*gridsize), (gridsize, gridsize))
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

class Node():
    def __init__(self, food, snake, parent, direction, from_start=0, first_direction=None):
        self.parent = parent
        self.snake = snake
        self.food = food
        self.direction = direction
        self.from_start = from_start
        self.to_food = None
        self.deaths = 0
        self.first_direction = first_direction

    def get_snake(self):
        return copy.deepcopy(self.snake)

        # Compare nodes
    def __eq__(self, other):
        return self.snake.positions == other.snake.positions
    # Sort nodes
    def __lt__(self, other):
         return self.f < other.f

    def taxi(self):
        node_head = self.snake.get_head_position()
        node_food = self.food.position
        if self.snake.type == "no walls":
            return min(abs(node_head[0] - node_food[0] - grid_width), abs(node_head[0] - node_food[0]), abs(node_head[0] - node_food[0] + grid_width)) + min(abs(node_head[1] - node_food[1] - grid_height), abs(node_head[1] - node_food[1]), abs(node_head[1] - node_food[1] + grid_height))
        elif self.snake.type == "walls":
            return abs(node_head[0] - node_food[0])+ abs(node_head[1] - node_food[1])

    def euclides(self):
        node_head = self.snake.get_head_position()
        node_food = self.food.position
        if self.snake.type == "no walls":
            return math.sqrt(min((node_head[0] - node_food[0] - grid_width)**2, (node_head[0] - node_food[0])**2, (node_head[0] - node_food[0] + grid_width)**2) + min((node_head[1] - node_food[1] - grid_height)**2, (node_head[1] - node_food[1])**2, (node_head[1] - node_food[1] + grid_height)**2))
        elif self.snake.type == "walls":
            return math.sqrt((node_head[0] - node_food[0])**2 + (node_head[1] - node_food[1])**2)

    def distance_to_food(self):
        if self.snake.mode == "euclides" or self.snake.mode == "euclides best first search" or self.snake.mode == "hamilton with cut":
            self.to_food = self.euclides()
        elif self.snake.mode == "taxi" or self.snake.mode == "taxirandom" or self.snake.mode == "taxi best first search":
            self.to_food = self.taxi()
        self.f = self.to_food

    def get_children(self):
        directions = self.snake.get_possible_moves()
        array_of_children = []
        for direction in directions:
            new_snake = self.get_snake()
            new_snake.move_to(direction)
            array_of_children.append(Node(self.food, new_snake, self, direction, self.from_start + 1))
        return array_of_children



screen_width = 600
screen_height = 600

gridsize = 20
grid_width = screen_width/gridsize
grid_height = screen_height/gridsize

hamiltonian_cycle = []

for i in range(grid_width):
    hamiltonian_cycle.append((0, grid_width - 1 - i))
for i in range(grid_width):
    if (i + 1) % 2 == 0:
        for j in range(grid_height - 1):
            hamiltonian_cycle.append((grid_width - 1 - j, i))
    else:
        for j in range(grid_height - 1):
            hamiltonian_cycle.append((j + 1, i))

hamiltonian_cycle = [(0, 0), (0, 1), (1, 1), (1, 2), (0, 2), (0, 3), (0, 4), (0, 5), (1, 5), (1, 4), (1, 3), (2, 3), (3, 3), (3, 2), (2, 2), (2, 1), (3, 1), (4, 1), (4, 2), (4, 3), (4, 4), (3, 4), (2, 4), (2, 5), (3, 5), (4, 5), (5, 5), (5, 4), (5, 3), (5, 2), (5, 1), (5, 0), (4, 0), (3, 0), (2, 0), (1, 0)]

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

    snake = Snake("walls", "euclides best first search")
    food = Food(snake)
    #snake.heuristic_move(food)

    myfont = pygame.font.SysFont("monospace",16)

    while (True):
        clock.tick(100)
        snake.handle_keys()
        drawGrid(surface)
        snake.heuristic_move(food)
        #snake.move()
        snake.moves += 1
        snake.from_last += 1
        if snake.get_head_position() == food.position:
            snake.length += 1
            snake.score += 1
            snake.sum_score += 1
            food.randomize_position(snake)
            print snake.moves/snake.score, snake.from_last
            snake.from_last = 0
        snake.time += 0.02
        snake.sum_time += 0.02
        snake.change_color()
        snake.draw(surface)
        food.draw(surface)
        screen.blit(surface, (0,0))
        score = myfont.render("Score {0}".format(snake.score), 1, (255,255,255))
        screen.blit(score, (5,10))
        #lives = myfont.render("Lives {0}".format(snake.lives), 1, (255,255,255))
        #screen.blit(lives, (screen_width - 100,10))
        #time = myfont.render("Time {0}".format(snake.time), 1, (255,255,255))
        #screen.blit(time, (5,screen_height - 30))
        pygame.display.update()

main()
