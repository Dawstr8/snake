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
    'speed': 100.0, #frames per second
    'showing': ['score', 'thinking', 'average'], # sratatata
    'size': 10, #dividing 600 and preferably not odd
    'generating cycle time': 10 #selfexplanatory
}

game_options = {
    'AI': 'heuristic',
    'distance': 'taxi',
    'must win': 'yes',
    'map type': 'without walls',
    'speed': 100.0,
    'showing': ['thinking'],
    'size': 30,
    'generating cycle time': 0,
    'lives': 1
}

screen_width = 600
screen_height = 600

gridsize = screen_width/game_options['size']
grid_width = game_options['size']
grid_height = game_options['size']

up = (0,-1)
down = (0,1)
left = (-1,0)
right = (1,0)

directions = [up, down, left, right]

hamiltonian_cycle = []

if game_options['map type'] == 'with walls':
    for i in range(grid_width):
        hamiltonian_cycle.append((0, grid_width - 1 - i))
    for i in range(grid_width):
        if (i + 1) % 2 == 0:
            for j in range(grid_height - 1):
                hamiltonian_cycle.append((grid_width - 1 - j, i))
        else:
            for j in range(grid_height - 1):
                hamiltonian_cycle.append((j + 1, i))
elif game_options['map type'] == 'without walls':
    for i in range(grid_width):
        if i % 2 == 0:
            for j in range(grid_height):
                hamiltonian_cycle.append((grid_width - 1 - j, i))
        else:
            for j in range(grid_height):
                hamiltonian_cycle.append((j, i))

class Point():
    def __init__(self, position):
        self.position = position

    def get_neighbors(self, size):
        array_of_neighbors = []
        for direction in directions:
            if game_options['map type'] == 'without walls':
                array_of_neighbors.append(((self.position[0] + direction[0])%size, (self.position[1] + direction[1])%size))
            else:
                if self.position[0] + direction[0] < size and self.position[0] + direction[0] >= 0 and self.position[1] + direction[1] < size and self.position[1] + direction[1] >= 0:
                    array_of_neighbors.append((self.position[0] + direction[0], self.position[1] + direction[1]))
        return array_of_neighbors

def is_hamiltonian_cycle(temp_hamiltonian_cycle, size):
    are_neighbors = True
    for i in range(len(temp_hamiltonian_cycle) - 1):
        if temp_hamiltonian_cycle[i] not in Point(temp_hamiltonian_cycle[i+1]).get_neighbors(size):
            are_neighbors = False
    if len(temp_hamiltonian_cycle) == size ** 2 and temp_hamiltonian_cycle[0] in Point(temp_hamiltonian_cycle[len(temp_hamiltonian_cycle) - 1]).get_neighbors(size) and are_neighbors:
        return True
    else:
        return False

timeout = time.time() + game_options['generating cycle time']
result_hamiltonian_cycle = []

while time.time() < timeout:
    neighbor_position = 1
    random_point_position = 0
    while abs(neighbor_position - random_point_position) == 1:
        random_point = random.choice(hamiltonian_cycle)
        for neighbor in Point(random_point).get_neighbors(game_options['size']):
            for i in range(game_options['size'] ** 2):
                if hamiltonian_cycle[i] == neighbor:
                    neighbor_position = i
                if hamiltonian_cycle[i] == random_point:
                    random_point_position = i
            if abs(neighbor_position - random_point_position) != 1:
                break

    hamiltonian_small_cycle = []
    hamiltonian_big_cycle = []
    for i in range(game_options['size'] ** 2):
        if i < neighbor_position and i > random_point_position:
            hamiltonian_small_cycle.append(hamiltonian_cycle[i])
        elif i > neighbor_position and i < random_point_position:
            hamiltonian_big_cycle.append(hamiltonian_cycle[i])
        else:
            hamiltonian_small_cycle.append(hamiltonian_cycle[i])

    first_neighbor_position = -1
    second_neighbor_position = -1
    counter = 0
    first_point_position = 0
    second_point_position = 0
    while abs(first_neighbor_position - second_neighbor_position) != 1 or first_neighbor_position == -1 or second_neighbor_position == -1:
        first_point_position = random.randint(0, len(hamiltonian_small_cycle) - 1)
        second_point_position = (first_point_position + 1)%len(hamiltonian_small_cycle)
        for first_neighbor in Point(hamiltonian_small_cycle[first_point_position]).get_neighbors(game_options['size']):
            for second_neighbor in Point(hamiltonian_small_cycle[second_point_position]).get_neighbors(game_options['size']):
                for i in range(len(hamiltonian_big_cycle)):
                    if hamiltonian_big_cycle[i] == first_neighbor:
                        first_neighbor_position = i
                    if hamiltonian_big_cycle[i] == second_neighbor:
                        second_neighbor_position = i
                if abs(first_neighbor_position - second_neighbor_position) == 1 and first_neighbor_position != -1 and second_neighbor_position != -1:
                    break
        counter += 1
        print counter
        if counter > 1000:
            break

    result_hamiltonian_cycle = []
    for i in range(len(hamiltonian_big_cycle)):
        if i == min(first_neighbor_position, second_neighbor_position):
            result_hamiltonian_cycle.append(hamiltonian_big_cycle[i])
            if hamiltonian_small_cycle[first_point_position] in Point(hamiltonian_big_cycle[i]).get_neighbors(game_options['size']):
                for j in range(len(hamiltonian_small_cycle)):
                    result_hamiltonian_cycle.append(hamiltonian_small_cycle[(j + first_point_position)%len(hamiltonian_small_cycle)])
            else:
                for j in range(len(hamiltonian_small_cycle)):
                    result_hamiltonian_cycle.append(hamiltonian_small_cycle[(j + second_point_position)%len(hamiltonian_small_cycle)])
        else:
             result_hamiltonian_cycle.append(hamiltonian_big_cycle[i])
    if is_hamiltonian_cycle(result_hamiltonian_cycle, game_options['size']):
        hamiltonian_cycle = result_hamiltonian_cycle

class Snake():
    def __init__(self):
        self.length = 1
        self.positions = [(grid_width/2, grid_height/2)]
        self.direction = random.choice([up, down, left, right])
        self.color = (13, 250, 144)
        self.lives = game_options['lives']
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
            if (len(self.positions) > 2 and new in self.positions[1:]) or not (new[0] >= 0 and new[1] >= 0 and new[0] < grid_width and new[1] < grid_height):
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
        elif snake.lives > 1:
            self.position = (0, 0)
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

        if distance_to_tail <= 10 and distance_to_tail != 0:
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
        timeout = time.time() + (game_options['speed'] ** -1)

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
            return [self.get_children()[0]]
        if len(open) == 0:
            return [self.get_children()[0]]

    def get_route(self):
        if game_options['AI'] == 'order':
            return self.order()
        if game_options['AI'] == 'heuristic':
            return self.heuristic()
        elif game_options['AI'] == 'best first search' or game_options['AI'] == 'A*':
            return self.best_first_search()

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
        clock.tick(game_options['speed'])
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
            #pygame.mixer.music.load('eating.wav')
            #pygame.mixer.music.play(0)
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
