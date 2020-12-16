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

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0]*-1, point[1]*-1) == self.direction:
            return
        else:
            self.direction = point

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
                if self.length < 60 * (grid_width * grid_height) / 100:
                    for child in children:
                        snake = node.get_snake()
                        snake.move_to((hamiltonian_cycle[child[1]][0]-hamiltonian_cycle[head_position][0], hamiltonian_cycle[child[1]][1] - hamiltonian_cycle[head_position][1]))
                        child_node = Node(food, snake, None, None)
                        child_node.distance_to_food()
                        distance_to_food = (food_position - child[1])%(grid_width*grid_height)
                        #distance_to_food = child_node.to_food*100 +
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
                print "hey"
        else:
            #self.reset()
            print "hey"

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

hamiltonian_cycle = [(1, 27), (1, 28), (2, 28), (2, 27), (2, 26), (2, 25), (2, 24), (2, 23), (2, 22), (2, 21), (2, 20), (2, 19), (2, 18), (2, 17), (2, 16), (2, 15), (2, 14), (2, 13), (2, 12), (2, 11), (2, 10), (2, 9), (2, 8), (2, 7), (2, 6), (2, 5), (2, 4), (2, 3), (2, 2), (2, 1), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0), (10, 0), (11, 0), (12, 0), (13, 0), (14, 0), (15, 0), (16, 0), (17, 0), (18, 0), (19, 0), (20, 0), (21, 0), (22, 0), (23, 0), (24, 0), (25, 0), (26, 0), (27, 0), (28, 0), (29, 0), (29, 1), (28, 1), (27, 1), (26, 1), (25, 1), (24, 1), (23, 1), (22, 1), (21, 1), (20, 1), (19, 1), (18, 1), (17, 1), (16, 1), (15, 1), (14, 1), (13, 1), (12, 1), (11, 1), (10, 1), (9, 1), (8, 1), (7, 1), (6, 1), (5, 1), (4, 1), (3, 1), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2), (9, 2), (10, 2), (11, 2), (12, 2), (13, 2), (14, 2), (15, 2), (16, 2), (17, 2), (18, 2), (19, 2), (20, 2), (21, 2), (22, 2), (23, 2), (24, 2), (25, 2), (26, 2), (27, 2), (28, 2), (29, 2), (29, 3), (28, 3), (27, 3), (26, 3), (25, 3), (24, 3), (23, 3), (22, 3), (21, 3), (20, 3), (19, 3), (18, 3), (17, 3), (16, 3), (15, 3), (14, 3), (13, 3), (12, 3), (11, 3), (10, 3), (9, 3), (8, 3), (7, 3), (6, 3), (5, 3), (4, 3), (3, 3), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 4), (9, 4), (10, 4), (11, 4), (12, 4), (13, 4), (14, 4), (15, 4), (16, 4), (17, 4), (18, 4), (19, 4), (20, 4), (21, 4), (22, 4), (23, 4), (24, 4), (25, 4), (26, 4), (27, 4), (28, 4), (29, 4), (29, 5), (28, 5), (27, 5), (26, 5), (25, 5), (24, 5), (23, 5), (22, 5), (21, 5), (20, 5), (19, 5), (18, 5), (17, 5), (16, 5), (15, 5), (14, 5), (13, 5), (12, 5), (11, 5), (10, 5), (9, 5), (8, 5), (7, 5), (6, 5), (5, 5), (4, 5), (3, 5), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6), (8, 6), (9, 6), (10, 6), (11, 6), (12, 6), (13, 6), (14, 6), (15, 6), (16, 6), (17, 6), (18, 6), (19, 6), (20, 6), (21, 6), (22, 6), (23, 6), (24, 6), (25, 6), (26, 6), (27, 6), (28, 6), (29, 6), (29, 7), (28, 7), (27, 7), (26, 7), (25, 7), (24, 7), (23, 7), (22, 7), (21, 7), (20, 7), (19, 7), (18, 7), (17, 7), (16, 7), (15, 7), (14, 7), (13, 7), (12, 7), (11, 7), (10, 7), (9, 7), (8, 7), (7, 7), (6, 7), (5, 7), (4, 7), (3, 7), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8), (8, 8), (9, 8), (10, 8), (11, 8), (12, 8), (13, 8), (14, 8), (15, 8), (16, 8), (17, 8), (18, 8), (19, 8), (20, 8), (21, 8), (22, 8), (23, 8), (24, 8), (25, 8), (26, 8), (27, 8), (28, 8), (29, 8), (29, 9), (28, 9), (27, 9), (26, 9), (25, 9), (24, 9), (23, 9), (22, 9), (21, 9), (20, 9), (19, 9), (18, 9), (17, 9), (16, 9), (15, 9), (14, 9), (13, 9), (12, 9), (11, 9), (10, 9), (9, 9), (8, 9), (7, 9), (6, 9), (5, 9), (4, 9), (3, 9), (3, 10), (4, 10), (5, 10), (6, 10), (7, 10), (8, 10), (9, 10), (10, 10), (11, 10), (12, 10), (13, 10), (14, 10), (15, 10), (16, 10), (17, 10), (18, 10), (19, 10), (20, 10), (21, 10), (22, 10), (23, 10), (24, 10), (25, 10), (26, 10), (27, 10), (28, 10), (29, 10), (29, 11), (28, 11), (27, 11), (26, 11), (25, 11), (24, 11), (23, 11), (22, 11), (21, 11), (20, 11), (19, 11), (18, 11), (17, 11), (16, 11), (15, 11), (14, 11), (13, 11), (12, 11), (11, 11), (10, 11), (9, 11), (8, 11), (7, 11), (6, 11), (5, 11), (4, 11), (3, 11), (3, 12), (4, 12), (5, 12), (6, 12), (7, 12), (8, 12), (9, 12), (10, 12), (11, 12), (12, 12), (13, 12), (14, 12), (15, 12), (16, 12), (17, 12), (18, 12), (19, 12), (20, 12), (21, 12), (22, 12), (23, 12), (24, 12), (25, 12), (26, 12), (27, 12), (28, 12), (29, 12), (29, 13), (28, 13), (27, 13), (26, 13), (25, 13), (24, 13), (23, 13), (22, 13), (21, 13), (20, 13), (19, 13), (18, 13), (17, 13), (16, 13), (15, 13), (14, 13), (13, 13), (12, 13), (11, 13), (10, 13), (9, 13), (8, 13), (7, 13), (6, 13), (5, 13), (4, 13), (3, 13), (3, 14), (4, 14), (5, 14), (6, 14), (7, 14), (8, 14), (9, 14), (10, 14), (11, 14), (12, 14), (13, 14), (14, 14), (15, 14), (16, 14), (17, 14), (18, 14), (19, 14), (20, 14), (21, 14), (22, 14), (23, 14), (24, 14), (25, 14), (26, 14), (27, 14), (28, 14), (29, 14), (29, 15), (28, 15), (27, 15), (26, 15), (25, 15), (24, 15), (23, 15), (22, 15), (21, 15), (20, 15), (19, 15), (18, 15), (17, 15), (16, 15), (15, 15), (14, 15), (13, 15), (12, 15), (11, 15), (10, 15), (9, 15), (8, 15), (7, 15), (6, 15), (5, 15), (4, 15), (3, 15), (3, 16), (4, 16), (5, 16), (6, 16), (7, 16), (8, 16), (9, 16), (10, 16), (11, 16), (12, 16), (13, 16), (14, 16), (15, 16), (16, 16), (17, 16), (18, 16), (19, 16), (20, 16), (21, 16), (22, 16), (23, 16), (24, 16), (25, 16), (26, 16), (27, 16), (28, 16), (29, 16), (29, 17), (28, 17), (27, 17), (26, 17), (25, 17), (24, 17), (23, 17), (22, 17), (21, 17), (20, 17), (19, 17), (18, 17), (17, 17), (16, 17), (15, 17), (14, 17), (13, 17), (12, 17), (11, 17), (10, 17), (9, 17), (8, 17), (7, 17), (6, 17), (5, 17), (4, 17), (3, 17), (3, 18), (4, 18), (5, 18), (6, 18), (7, 18), (8, 18), (9, 18), (10, 18), (11, 18), (12, 18), (13, 18), (14, 18), (15, 18), (16, 18), (17, 18), (18, 18), (19, 18), (20, 18), (21, 18), (22, 18), (23, 18), (24, 18), (25, 18), (26, 18), (27, 18), (28, 18), (29, 18), (29, 19), (28, 19), (27, 19), (26, 19), (25, 19), (24, 19), (23, 19), (22, 19), (21, 19), (20, 19), (19, 19), (18, 19), (17, 19), (16, 19), (15, 19), (14, 19), (13, 19), (12, 19), (11, 19), (10, 19), (9, 19), (8, 19), (7, 19), (6, 19), (5, 19), (4, 19), (3, 19), (3, 20), (4, 20), (5, 20), (6, 20), (7, 20), (8, 20), (9, 20), (10, 20), (11, 20), (12, 20), (13, 20), (14, 20), (15, 20), (16, 20), (17, 20), (18, 20), (19, 20), (20, 20), (21, 20), (22, 20), (23, 20), (24, 20), (25, 20), (26, 20), (27, 20), (28, 20), (29, 20), (29, 21), (28, 21), (27, 21), (26, 21), (25, 21), (24, 21), (23, 21), (22, 21), (21, 21), (20, 21), (19, 21), (18, 21), (17, 21), (16, 21), (15, 21), (14, 21), (13, 21), (12, 21), (11, 21), (10, 21), (9, 21), (8, 21), (7, 21), (6, 21), (5, 21), (4, 21), (3, 21), (3, 22), (4, 22), (5, 22), (6, 22), (7, 22), (8, 22), (9, 22), (10, 22), (11, 22), (12, 22), (13, 22), (14, 22), (15, 22), (16, 22), (17, 22), (18, 22), (19, 22), (20, 22), (21, 22), (22, 22), (23, 22), (24, 22), (25, 22), (26, 22), (27, 22), (28, 22), (29, 22), (29, 23), (28, 23), (27, 23), (26, 23), (25, 23), (24, 23), (23, 23), (22, 23), (21, 23), (20, 23), (19, 23), (18, 23), (17, 23), (16, 23), (15, 23), (14, 23), (13, 23), (12, 23), (11, 23), (10, 23), (9, 23), (8, 23), (7, 23), (6, 23), (5, 23), (4, 23), (3, 23), (3, 24), (4, 24), (5, 24), (6, 24), (7, 24), (8, 24), (9, 24), (10, 24), (11, 24), (12, 24), (13, 24), (14, 24), (15, 24), (16, 24), (17, 24), (18, 24), (19, 24), (20, 24), (21, 24), (22, 24), (23, 24), (24, 24), (25, 24), (26, 24), (27, 24), (28, 24), (29, 24), (29, 25), (28, 25), (27, 25), (26, 25), (25, 25), (24, 25), (23, 25), (22, 25), (21, 25), (20, 25), (19, 25), (18, 25), (17, 25), (16, 25), (15, 25), (14, 25), (13, 25), (12, 25), (11, 25), (10, 25), (9, 25), (8, 25), (7, 25), (6, 25), (5, 25), (4, 25), (3, 25), (3, 26), (4, 26), (5, 26), (6, 26), (7, 26), (8, 26), (9, 26), (10, 26), (11, 26), (12, 26), (13, 26), (14, 26), (15, 26), (16, 26), (17, 26), (18, 26), (19, 26), (20, 26), (21, 26), (22, 26), (23, 26), (24, 26), (25, 26), (26, 26), (27, 26), (28, 26), (29, 26), (29, 27), (28, 27), (27, 27), (26, 27), (25, 27), (24, 27), (23, 27), (22, 27), (21, 27), (20, 27), (19, 27), (18, 27), (17, 27), (16, 27), (15, 27), (14, 27), (13, 27), (12, 27), (11, 27), (10, 27), (9, 27), (8, 27), (7, 27), (6, 27), (5, 27), (4, 27), (3, 27), (3, 28), (4, 28), (5, 28), (6, 28), (7, 28), (8, 28), (9, 28), (10, 28), (11, 28), (12, 28), (13, 28), (14, 28), (15, 28), (16, 28), (17, 28), (18, 28), (19, 28), (20, 28), (21, 28), (22, 28), (23, 28), (24, 28), (25, 28), (26, 28), (27, 28), (28, 28), (29, 28), (29, 29), (28, 29), (27, 29), (26, 29), (25, 29), (24, 29), (23, 29), (22, 29), (21, 29), (20, 29), (19, 29), (18, 29), (17, 29), (16, 29), (15, 29), (14, 29), (13, 29), (12, 29), (11, 29), (10, 29), (9, 29), (8, 29), (7, 29), (6, 29), (5, 29), (4, 29), (3, 29), (2, 29), (1, 29), (0, 29), (0, 28), (0, 27), (0, 26), (0, 25), (0, 24), (0, 23), (0, 22), (0, 21), (0, 20), (0, 19), (0, 18), (0, 17), (0, 16), (0, 15), (0, 14), (0, 13), (0, 12), (0, 11), (0, 10), (0, 9), (0, 8), (0, 7), (0, 6), (0, 5), (0, 4), (0, 3), (0, 2), (0, 1), (0, 0), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10), (1, 11), (1, 12), (1, 13), (1, 14), (1, 15), (1, 16), (1, 17), (1, 18), (1, 19), (1, 20), (1, 21), (1, 22), (1, 23), (1, 24), (1, 25), (1, 26)]

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

    snake = Snake("walls", "hamilton with cut")
    food = Food(snake)
    #snake.heuristic_move(food)

    myfont = pygame.font.SysFont("monospace",16)

    while (True):
        clock.tick(150)
        snake.handle_keys()
        drawGrid(surface)
        snake.heuristic_move(food)
        #snake.move()
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
        score = myfont.render("Score {0}".format(snake.score), 1, (255,255,255))
        screen.blit(score, (5,10))
        #lives = myfont.render("Lives {0}".format(snake.lives), 1, (255,255,255))
        #screen.blit(lives, (screen_width - 100,10))
        #time = myfont.render("Time {0}".format(snake.time), 1, (255,255,255))
        #screen.blit(time, (5,screen_height - 30))
        pygame.display.update()

main()
