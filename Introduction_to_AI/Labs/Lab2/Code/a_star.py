import math


class Node:
    def __init__(self, node):
        self.g = 0
        self.h = 0
        self.f = 0
        self.node = node


# Utility function to check if a move is valid
def valid(map2d, x, y, visited):
    int(x), int(y)
    if 0 <= x < len(map2d[0]) and 0 <= y < len(map2d) and map2d[x][y] != -1 and (x, y) not in visited:
        return True
    else:
        return False


def get_neighbors(current, map2d, came_from):
    # Get x and y for the current position
    x_pos, y_pos = current

    # Get the neighbors
    # ! X and Y had to be inverted !
    left = [y_pos, x_pos - 1]
    top = [y_pos - 1, x_pos]
    right = [y_pos, x_pos + 1]
    bottom = [y_pos + 1, x_pos]

    neighbors = [left, top, right, bottom]

    free_cells = []

    for neighbor in neighbors:
        # Checking if the neighbors are valid (value of 0, -3 and inside the matrix)
        # ! X and Y had to be inverted !
        if valid(map2d, neighbor[1], neighbor[0], came_from):
            free_cells.append((neighbor[1], neighbor[0]))
        else:
            # Removed if not valid
            neighbors.remove(neighbor)

    return free_cells


def euclidean_distance(current, goal):
    current_x, current_y = current
    goal_x, goal_y = goal
    return math.sqrt((current_x - goal_x) ** 2 + (current_y - goal_y) ** 2)


# Return the distance between the current node and the goal using the Manhattan distance formula
def manhattan_distance(current, goal):
    current_x, current_y = current
    goal_x, goal_y = goal
    return abs(current_x - goal_x) + abs(current_y - goal_y)


def a_star_search(map2d, start, goal):
    # cost moving to another cell
    moving_cost = 1

    # Init of the stack
    queue = [Node(start)]

    visited = []

    while queue:
        # Get the cell with the lowest f-value from the open list
        current = min(queue, key=lambda p: p.f)
        queue.remove(current)
        visited.append(current.node)

        # check if the goal is reached
        if current.node == goal:
            return visited, current.g + moving_cost

        for next in get_neighbors(current.node, map2d, visited):
            next_cell = Node(next)
            next_cell.g = current.g + moving_cost
            next_cell.h = manhattan_distance(next_cell.node, goal)
            # next_cell.h = euclidean_distance(next_cell.node, goal)
            next_cell.f = next_cell.g + next_cell.h

            queue.append(next_cell)

    return False
