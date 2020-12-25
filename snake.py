import pygame
import sys
import random
import math
import copy
import time

INFINITY = 10000000

options = {
    'AI': ['order', 'heuristic', 'best first search', 'A*'],
    'distance': ['taxi', 'euclides', 'hamilton'],
    'map type': ['with walls', 'without walls'],
    'time': 0.001, #1.0 equals to 1 sec per move (pretty slow)
    'showing': ['score', 'thinking', 'average'], # sratatata
    'safety': 1 # 1 - 10
}

game_options = {
    'AI': 'heuristic',
    'distance': 'euclides',
    'must win': 'yes',
    'map type': 'with walls',
    'time': 0.1,
    'showing': ['thinking'],
    'safety': 1
}

class Snake():
    def __init__(self):
        self.length = 1
        self.positions = [(grid_width/2, grid_height/2)]
        self.direction = random.choice([up, down, left, right])
        self.color = (13, 250, 144)
        self.lives = 1
        self.route = []
        self.state = 'found'
        self.ended = False
        self.data = {'average': 0, 'from last': 0, 'moves': 0, 'score': 0, 'sum_score': 0}

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0]*-1, point[1]*-1) == self.direction:
            return
        else:
            self.direction = point

    def change_color(self):
        if self.state == "found":
            self.color = (13, 250, 144)
        elif self.state == "not found":
            self.color = (237, 163, 12)
        elif self.state == "die":
            self.color = (255, 0, 0)


    def new_move(self, cur, x, y):
        if game_options['map type'] == "without walls":
            new = (((cur[0]+x)%grid_width), (cur[1]+y)%grid_height)
        elif game_options['map type'] == "with walls":
            new = ((cur[0]+x), (cur[1]+y))
        return new

    def move(self, direction):
        if not self.ended:
            cur = self.get_head_position()
            x,y = direction
            new = self.new_move(cur, x, y)
            if (len(self.positions) > 2 and new in self.positions[2:]) or not (new[0] >= 0 and new[1] >= 0 and new[0] < grid_width and new[1] < grid_height):
                    self.ended = True
                    self.reset()
            else:
                self.positions.insert(0, new)
                if len(self.positions) > self.length:
                    self.positions.pop()

    def reset(self):
        if self.lives > 1:
            self.lives -= 1
            self.length = 1
            self.positions = [(grid_width/2, grid_height/2)]
            self.direction = random.choice([up, down, left, right])
            self.ended = False
            self.state = "not found"
            self.data = {'average': 0, 'from last': 0, 'moves': 0, 'score': 0, 'sum_score': 0}

    def draw(self,surface):
        if len(self.positions) == 1:
            p = self.positions[0]
            rr = pygame.Rect((p[0]*gridsize + 1, p[1]*gridsize + 1), (gridsize - 2,gridsize - 2))
            pygame.draw.rect(surface, self.color, rr)
        else:
            for i in range(len(self.positions)):
                p = self.positions[i]
                if i != len(self.positions) - 1:
                    if (self.positions[i + 1][0] - p[0], self.positions[i + 1][1] - p[1]) == (1, 0):
                        rr = pygame.Rect((p[0]*gridsize + 2, p[1]*gridsize + 2), (gridsize - 2,gridsize - 4))
                        pygame.draw.rect(surface, self.color, rr)
                    elif (self.positions[i + 1][0] - p[0], self.positions[i + 1][1] - p[1]) == (-1, 0):
                        rr = pygame.Rect((p[0]*gridsize, p[1]*gridsize + 2), (gridsize - 2,gridsize - 4))
                        pygame.draw.rect(surface, self.color, rr)
                    elif (self.positions[i + 1][0] - p[0], self.positions[i + 1][1] - p[1]) == (0, 1):
                        rr = pygame.Rect((p[0]*gridsize + 2, p[1]*gridsize + 2), (gridsize - 4,gridsize - 2))
                        pygame.draw.rect(surface, self.color, rr)
                    elif (self.positions[i + 1][0] - p[0], self.positions[i + 1][1] - p[1]) == (0, -1):
                        rr = pygame.Rect((p[0]*gridsize + 2, p[1]*gridsize), (gridsize - 4,gridsize - 2))
                        pygame.draw.rect(surface, self.color, rr)
                if i != 0:
                    if (p[0] - self.positions[i - 1][0], p[1] - self.positions[i - 1][1]) == (1, 0):
                        rr = pygame.Rect((p[0]*gridsize, p[1]*gridsize + 2), (gridsize - 2,gridsize - 4))
                        pygame.draw.rect(surface, self.color, rr)
                    elif (p[0] - self.positions[i - 1][0], p[1] - self.positions[i - 1][1]) == (-1, 0):
                        rr = pygame.Rect((p[0]*gridsize + 2, p[1]*gridsize + 2), (gridsize - 2,gridsize - 4))
                        pygame.draw.rect(surface, self.color, rr)
                    elif (p[0] - self.positions[i - 1][0], p[1] - self.positions[i - 1][1]) == (0, 1):
                        rr = pygame.Rect((p[0]*gridsize + 2, p[1]*gridsize), (gridsize - 4,gridsize - 2))
                        pygame.draw.rect(surface, self.color, rr)
                    elif (p[0] - self.positions[i - 1][0], p[1] - self.positions[i - 1][1]) == (0, -1):
                        rr = pygame.Rect((p[0]*gridsize + 2, p[1]*gridsize + 2), (gridsize - 4,gridsize - 2))
                        pygame.draw.rect(surface, self.color, rr)
            #pygame.draw.rect(surface, self.color, r)
            #pygame.draw.rect(surface, (0,0,0), r, 1)

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
        if len(self.get_possible_moves()) != 0:
            if len(self.route) == 0:
                self.route = node.get_route()
            if self.route[-1].snake.get_head_position() == food.position or game_options['must win'] == 'yes':
                self.state = "found"
            elif len(self.route[-1].snake.get_possible_moves()) == 0:
                self.state = "die"
            else:
                self.state = "not found"
            self.move(self.route.pop(0).direction)
        else:
            self.move(random.choice(directions))

class Food():
    def __init__(self, snake):
        self.position = (0,0)
        self.color = (255, 0, 0)
        self.randomize_position(snake)

    def randomize_position(self, snake):
        if len(snake.positions) != (grid_width * grid_height):
            self.position = (random.randint(0, grid_width-1), random.randint(0, grid_height-1))
            while self.position in snake.positions:
                self.position = (random.randint(0, grid_width-1), random.randint(0, grid_height-1))
        else:
            self.position = None

    def draw(self, surface):
        if not self.position is None:
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
        self.first_direction = first_direction
        self.f = 0

    def get_snake(self):
        return copy.deepcopy(self.snake)

        # Compare nodes
    def __eq__(self, other):
        return self.snake.positions == other.snake.positions
    # Sort nodes
    def __lt__(self, other):
         return self.f < other.f

    def get_children(self):
        directions = self.snake.get_possible_moves()
        array_of_children = []
        for direction in directions:
            new_snake = self.get_snake()
            new_snake.move(direction)
            if game_options['must win'] == 'yes' and not self.parent is None:
                for i in range(len(hamiltonian_cycle)):
                    if hamiltonian_cycle[i] == self.snake.get_head_position():
                        head_position = i
                    if hamiltonian_cycle[i] == self.food.position:
                        food_position = i
                    if hamiltonian_cycle[i] == self.parent.snake.get_head_position():
                        parent_head_position = i
                array_of_children.append(Node(self.food, new_snake, self, direction, self.from_start + (head_position - parent_head_position)%(grid_width*grid_height)))
            else:
                array_of_children.append(Node(self.food, new_snake, self, direction, self.from_start + 1))
        return array_of_children

    def taxi(self):
        node_head = self.snake.get_head_position()
        node_food = self.food.position
        if game_options['map type'] == "without walls":
            return min(abs(node_head[0] - node_food[0] - grid_width), abs(node_head[0] - node_food[0]), abs(node_head[0] - node_food[0] + grid_width)) + min(abs(node_head[1] - node_food[1] - grid_height), abs(node_head[1] - node_food[1]), abs(node_head[1] - node_food[1] + grid_height))
        elif game_options['map type'] == "with walls":
            return abs(node_head[0] - node_food[0])+ abs(node_head[1] - node_food[1])

    def euclides(self):
        node_head = self.snake.get_head_position()
        node_food = self.food.position
        if game_options['map type'] == "without walls":
            return math.sqrt(min((node_head[0] - node_food[0] - grid_width)**2, (node_head[0] - node_food[0])**2, (node_head[0] - node_food[0] + grid_width)**2) + min((node_head[1] - node_food[1] - grid_height)**2, (node_head[1] - node_food[1])**2, (node_head[1] - node_food[1] + grid_height)**2))
        elif game_options['map type'] == "with walls":
            return math.sqrt((node_head[0] - node_food[0])**2 + (node_head[1] - node_food[1])**2)

    def hamilton(self):
        for i in range(len(hamiltonian_cycle)):
            if hamiltonian_cycle[i] == self.snake.get_head_position():
                head_position = i
            if hamiltonian_cycle[i] == self.food.position:
                food_position = i
            if hamiltonian_cycle[i] == self.parent.snake.get_head_position():
                parent_head_position = i
        return (food_position - head_position)%(grid_width*grid_height)

    def check_cycle(self):
        for i in range(len(hamiltonian_cycle)):
            if hamiltonian_cycle[i] == self.snake.get_head_position():
                head_position = i
            if hamiltonian_cycle[i] == self.food.position:
                food_position = i
            if hamiltonian_cycle[i] == self.snake.positions[-1]:
                tail_position = i
            if not self.parent is None and hamiltonian_cycle[i] == self.parent.snake.get_head_position():
                parent_head_position = i

        distance_to_tail = (tail_position - head_position)%(grid_width*grid_height)

        if not self.parent is None:
            distance_from_parent_head_position = (head_position - parent_head_position - 1)%(grid_width*grid_height)
            for i in range(distance_from_parent_head_position):
                if hamiltonian_cycle[(i + parent_head_position + 1)%(grid_width*grid_height)] in self.snake.positions:
                    return False
            if (food_position - head_position)%(grid_width*grid_height) > (parent_head_position - head_position)%(grid_width*grid_height):
                return False

        if distance_to_tail <= 5 and distance_to_tail != 0:
            return False

        return True

    def distance_to_food(self):
        if game_options['must win'] == 'yes':
            if self.check_cycle():
                if game_options['distance'] == 'euclides':
                    self.to_food = self.euclides()
                elif game_options['distance'] == 'taxi':
                    self.to_food = self.taxi()
                elif game_options['distance'] == 'hamilton':
                    self.to_food = self.hamilton()
            else:
                self.to_food = INFINITY
        else:
            if game_options['distance'] == 'euclides':
                self.to_food = self.euclides()
            elif game_options['distance'] == 'taxi':
                self.to_food = self.taxi()

    def function_value(self):
        if game_options['AI'] == "best first search":
            self.f = self.to_food
        elif game_options['AI'] == "A*":
            self.f = self.to_food + self.from_start

    def order(self):
        for i in range(len(hamiltonian_cycle)):
            if hamiltonian_cycle[i] == self.snake.get_head_position():
                head_position = i
        for child in self.get_children():
            if child.snake.get_head_position() == hamiltonian_cycle[(head_position+1)%(grid_width*grid_height)]:
                best_child = child
        return [best_child]

    def heuristic(self):
        distance = INFINITY
        best_child = random.choice(self.get_children())
        for child in self.get_children():
            child.distance_to_food()
            if child.to_food < distance:
                distance = child.to_food
                best_child = child
        if distance == INFINITY:
            return self.order()
        return [best_child]

    def best_first_search(self):
        route = []
        timeout = time.time() + game_options['time']

        self.distance_to_food()
        self.function_value()
        open = [self]
        closed = []

        while len(open) != 0 and time.time() < timeout:
            open.sort()
            current_node = open.pop(0)
            closed.append(current_node)
            if current_node.to_food == 0:
                path = []
                while current_node != self:
                    path.append(current_node)
                    current_node = current_node.parent
                return path[::-1]
            for child in current_node.get_children():
                if child in closed:
                    continue
                if child not in open:
                    child.distance_to_food()
                    child.function_value()
                    open.append(child)

        if len(open) != 0:
            return self.heuristic()
        if len(open) == 0:
            return self.heuristic()

    def get_route(self):
        if game_options['AI'] == 'order':
            return self.order()
        if game_options['AI'] == 'heuristic':
            return self.heuristic()
        elif game_options['AI'] == 'best first search' or game_options['AI'] == 'A*':
            return self.best_first_search()


screen_width = 600
screen_height = 600

gridsize = 30
grid_width = screen_width/gridsize
grid_height = screen_height/gridsize

up = (0,-1)
down = (0,1)
left = (-1,0)
right = (1,0)

directions = [up, down, left, right]

hamiltonian_cycle = [(18, 18), (18, 17), (18, 16), (18, 15), (17, 15), (17, 14), (18, 14), (18, 13), (18, 12), (18, 11), (17, 11), (17, 12), (17, 13), (16, 13), (16, 14), (16, 15), (16, 16), (17, 16), (17, 17), (16, 17), (15, 17), (14, 17), (14, 18), (15, 18), (16, 18), (17, 18), (17, 19), (16, 19), (15, 19), (14, 19), (13, 19), (13, 18), (12, 18), (12, 19), (11, 19), (11, 18), (10, 18), (10, 19), (9, 19), (9, 18), (9, 17), (8, 17), (8, 16), (8, 15), (8, 14), (9, 14), (10, 14), (10, 15), (9, 15), (9, 16), (10, 16), (10, 17), (11, 17), (11, 16), (11, 15), (11, 14), (11, 13), (11, 12), (10, 12), (10, 13), (9, 13), (9, 12), (9, 11), (9, 10), (9, 9), (9, 8), (8, 8), (8, 9), (8, 10), (8, 11), (8, 12), (8, 13), (7, 13), (7, 14), (7, 15), (7, 16), (7, 17), (7, 18), (8, 18), (8, 19), (7, 19), (6, 19), (5, 19), (4, 19), (4, 18), (4, 17), (4, 16), (4, 15), (4, 14), (4, 13), (5, 13), (5, 14), (5, 15), (5, 16), (5, 17), (5, 18), (6, 18), (6, 17), (6, 16), (6, 15), (6, 14), (6, 13), (6, 12), (7, 12), (7, 11), (6, 11), (6, 10), (7, 10), (7, 9), (6, 9), (6, 8), (7, 8), (7, 7), (6, 7), (5, 7), (5, 8), (4, 8), (4, 7), (4, 6), (5, 6), (5, 5), (4, 5), (3, 5), (3, 6), (3, 7), (3, 8), (2, 8), (1, 8), (1, 9), (2, 9), (3, 9), (4, 9), (5, 9), (5, 10), (5, 11), (5, 12), (4, 12), (4, 11), (4, 10), (3, 10), (3, 11), (3, 12), (3, 13), (3, 14), (3, 15), (3, 16), (3, 17), (3, 18), (3, 19), (2, 19), (2, 18), (2, 17), (2, 16), (1, 16), (1, 17), (1, 18), (1, 19), (0, 19), (0, 18), (0, 17), (0, 16), (0, 15), (0, 14), (1, 14), (1, 15), (2, 15), (2, 14), (2, 13), (1, 13), (0, 13), (0, 12), (1, 12), (2, 12), (2, 11), (2, 10), (1, 10), (1, 11), (0, 11), (0, 10), (0, 9), (0, 8), (0, 7), (0, 6), (1, 6), (1, 7), (2, 7), (2, 6), (2, 5), (2, 4), (2, 3), (2, 2), (3, 2), (3, 1), (2, 1), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (0, 5), (0, 4), (0, 3), (0, 2), (0, 1), (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (6, 1), (5, 1), (4, 1), (4, 2), (4, 3), (3, 3), (3, 4), (4, 4), (5, 4), (5, 3), (5, 2), (6, 2), (7, 2), (7, 1), (7, 0), (8, 0), (8, 1), (8, 2), (8, 3), (9, 3), (10, 3), (10, 4), (10, 5), (11, 5), (11, 4), (12, 4), (12, 3), (11, 3), (11, 2), (10, 2), (9, 2), (9, 1), (9, 0), (10, 0), (10, 1), (11, 1), (11, 0), (12, 0), (12, 1), (12, 2), (13, 2), (13, 3), (13, 4), (14, 4), (14, 3), (15, 3), (15, 4), (15, 5), (14, 5), (14, 6), (15, 6), (16, 6), (16, 7), (15, 7), (14, 7), (13, 7), (13, 6), (13, 5), (12, 5), (12, 6), (12, 7), (11, 7), (11, 6), (10, 6), (9, 6), (9, 5), (9, 4), (8, 4), (8, 5), (7, 5), (7, 4), (7, 3), (6, 3), (6, 4), (6, 5), (6, 6), (7, 6), (8, 6), (8, 7), (9, 7), (10, 7), (10, 8), (10, 9), (10, 10), (10, 11), (11, 11), (12, 11), (13, 11), (13, 10), (12, 10), (11, 10), (11, 9), (11, 8), (12, 8), (12, 9), (13, 9), (13, 8), (14, 8), (14, 9), (14, 10), (14, 11), (14, 12), (14, 13), (13, 13), (13, 12), (12, 12), (12, 13), (12, 14), (13, 14), (13, 15), (12, 15), (12, 16), (12, 17), (13, 17), (13, 16), (14, 16), (15, 16), (15, 15), (14, 15), (14, 14), (15, 14), (15, 13), (15, 12), (16, 12), (16, 11), (15, 11), (15, 10), (15, 9), (15, 8), (16, 8), (16, 9), (16, 10), (17, 10), (17, 9), (17, 8), (18, 8), (18, 7), (17, 7), (17, 6), (18, 6), (18, 5), (17, 5), (16, 5), (16, 4), (17, 4), (18, 4), (18, 3), (17, 3), (16, 3), (16, 2), (17, 2), (17, 1), (16, 1), (15, 1), (15, 2), (14, 2), (14, 1), (13, 1), (13, 0), (14, 0), (15, 0), (16, 0), (17, 0), (18, 0), (19, 0), (19, 1), (18, 1), (18, 2), (19, 2), (19, 3), (19, 4), (19, 5), (19, 6), (19, 7), (19, 8), (19, 9), (18, 9), (18, 10), (19, 10), (19, 11), (19, 12), (19, 13), (19, 14), (19, 15), (19, 16), (19, 17), (19, 18), (19, 19), (18, 19)]

def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    drawGrid(surface)

    snake = Snake()
    food = Food(snake)

    myfont = pygame.font.SysFont("monospace",16)

    while True:
        clock.tick(game_options['time'] ** -1)
        snake.handle_keys()
        drawGrid(surface)
        if not snake.ended:
            if game_options['AI'] == 'human':
                snake.move(snake.direction)
            else:
                snake.heuristic_move(food)
        else:
            snake.reset()
        snake.data['moves'] += 1
        snake.data['from last'] += 1
        if snake.get_head_position() == food.position:
            pygame.mixer.music.load('eating.wav')
            pygame.mixer.music.play(0)
            snake.length += 1
            food.randomize_position(snake)
            snake.data['score'] += 1
            snake.data['sum_score'] += 1
            snake.data['average'] = snake.data['moves']/snake.data['score']
            snake.from_last = 0
            print snake.data['score'], snake.data['average']
        if 'thinking' in game_options['showing']:
            snake.change_color()
        snake.draw(surface)
        food.draw(surface)
        screen.blit(surface, (0,0))
        if 'score' in game_options['showing']:
            show_score = myfont.render("Score {0}".format(snake.data['score']), 1, (255,255,255))
            screen.blit(show_score, (5,10))
        if 'average' in game_options['showing']:
            show_average = myfont.render("Average {0}".format(snake.data['average']), 1, (255,255,255))
            screen.blit(show_average, (5, 30))
        pygame.display.update()

main()
