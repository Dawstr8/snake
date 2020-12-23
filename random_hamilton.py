import random
import time
import sys
import copy
import math

sys.setrecursionlimit(1000000)

best_all_time = 0
best = 0
go_back = False
operations = 0
tries = 1
#timeout = time.time() + 10

class Node():
    def __init__(self, position):
        self.position = position

    def get_neighbors(self, size):
        array_of_neighbors = []
        for direction in directions:
            if self.position[0] + direction[0] < size and self.position[0] + direction[0] >= 0 and self.position[1] + direction[1] < size and self.position[1] + direction[1] >= 0:
                array_of_neighbors.append((self.position[0] + direction[0], self.position[1] + direction[1]))
        return array_of_neighbors

def is_hamiltonian_cycle(temp_hamiltonian_cycle, size):
    are_neighbors = True
    for i in range(len(temp_hamiltonian_cycle) - 1):
        if temp_hamiltonian_cycle[i] not in Node(temp_hamiltonian_cycle[i+1]).get_neighbors(size):
            are_neighbors = False
    if len(temp_hamiltonian_cycle) == size ** 2 and temp_hamiltonian_cycle[0] in Node(temp_hamiltonian_cycle[len(temp_hamiltonian_cycle) - 1]).get_neighbors(size) and are_neighbors:
        return True
    else:
        return False


with open('answer.txt', 'w') as file:

    up = (0,-1)
    down = (0,1)
    left = (-1,0)
    right = (1,0)
    directions = [up, down, left, right]

    ultimate_size = 30
    grid_width = ultimate_size
    grid_height = ultimate_size

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

    timeout = time.time() + 600
    result_hamiltonian_cycle = []

    while time.time() < timeout:
        neighbor_position = 1
        random_point_position = 0
        while abs(neighbor_position - random_point_position) == 1:
            random_point = random.choice(hamiltonian_cycle)
            for neighbor in Node(random_point).get_neighbors(ultimate_size):
                for i in range(ultimate_size ** 2):
                    if hamiltonian_cycle[i] == neighbor:
                        neighbor_position = i
                    if hamiltonian_cycle[i] == random_point:
                        random_point_position = i
                if abs(neighbor_position - random_point_position) != 1:
                    break

        hamiltonian_small_cycle = []
        hamiltonian_big_cycle = []
        for i in range(ultimate_size ** 2):
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
            for first_neighbor in Node(hamiltonian_small_cycle[first_point_position]).get_neighbors(ultimate_size):
                for second_neighbor in Node(hamiltonian_small_cycle[second_point_position]).get_neighbors(ultimate_size):
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
            #print first_neighbor_position, second_neighbor_position

        result_hamiltonian_cycle = []
        for i in range(len(hamiltonian_big_cycle)):
            if i == min(first_neighbor_position, second_neighbor_position):
                result_hamiltonian_cycle.append(hamiltonian_big_cycle[i])
                if hamiltonian_small_cycle[first_point_position] in Node(hamiltonian_big_cycle[i]).get_neighbors(ultimate_size):
                    for j in range(len(hamiltonian_small_cycle)):
                        result_hamiltonian_cycle.append(hamiltonian_small_cycle[(j + first_point_position)%len(hamiltonian_small_cycle)])
                else:
                    for j in range(len(hamiltonian_small_cycle)):
                        result_hamiltonian_cycle.append(hamiltonian_small_cycle[(j + second_point_position)%len(hamiltonian_small_cycle)])
            else:
                 result_hamiltonian_cycle.append(hamiltonian_big_cycle[i])
        if is_hamiltonian_cycle(result_hamiltonian_cycle, ultimate_size):
            hamiltonian_cycle = result_hamiltonian_cycle

    cycle = str(hamiltonian_cycle)
    file.write(cycle)
    exit()
