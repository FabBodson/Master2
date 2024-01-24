import numpy as np
import math
import heapq
import random


# Priority Queue based on heapq
class PriorityQueue:
    def __init__(self):
        self.elements = []

    def isEmpty(self):
        return len(self.elements) == 0

    def add(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def remove(self):
        return heapq.heappop(self.elements)[1]


def get_neighbors(current, map2d, visited):
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
        if valid(map2d, neighbor[1], neighbor[0], visited):
            free_cells.append((neighbor[1], neighbor[0]))
    return free_cells


def get_neighbors_DFS(current, map2d, came_from):
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


# Utility function to check if a move is valid
def valid(map2d, x, y, visited):
    int(x), int(y)
    if 0 <= x < len(map2d[0]) and 0 <= y < len(map2d) and map2d[x][y] != -1 and (x, y) not in visited:
        return True
    else:
        return False


# Random Search Algorithm
def random_search(map2d, start, goal):
    cost = 0
    path = [start]
    while path[-1] != goal:
        x, y = path[-1]
        direction = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        check_move = [(x + dx, y + dy) for dx, dy in direction if valid(map2d, x + dx, y + dy, path)]
        if not check_move:
            return None
        else:
            move = random.choice(check_move)
            path.append(move)
            cost += 1
    return path, cost


# BFS Algorithm
def bfs_search(map2d, start, goal):
    cost = 0
    # path taken
    path = []
    # open list
    frontier = PriorityQueue()
    frontier.add(start, 0)

    # dictionary to keep track of parents
    came_from = {}
    came_from[start] = None

    # if there is still nodes to open
    while not frontier.isEmpty():
        current = frontier.remove()

        # check if the goal is reached
        if current == goal:
            # reconstruct path
            while current != None:
                path.append(current)
                current = came_from[current]
                cost += 1
            path.reverse()  # reverse the path to start->goal
            return path, cost

        for next in get_neighbors(current, map2d, path):
            if next not in came_from:
                # cost[next] = cost_function(moving_cost, cost)

                # add next cell to open list and record its parent
                frontier.add(next, cost)
                came_from[next] = current

    return False


# DFS Algorithm
def dfs_search(map2d, start, goal):
    stack = [start]
    visited = set()
    came_from = {start: None}

    while stack:
        current = stack.pop()

        if current == goal:
            # Reconstruct path
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            path.reverse()  # reverse the path to start->goal
            cost = len(path) - 1
            return path, cost

        if current not in visited:
            visited.add(current)
            for next in get_neighbors_DFS(current, map2d, visited):
                if next not in visited and next not in stack:
                    stack.append(next)
                    came_from[next] = current
    return False


def manhattan_distance(current, goal):
    current_x, current_y = current
    goal_x, goal_y = goal
    return abs(current_x - goal_x) + abs(current_y - goal_y)


def euclidean_distance(current, goal):
    current_x, current_y = current
    goal_x, goal_y = goal
    return math.sqrt((current_x - goal_x) ** 2 + (current_y - goal_y) ** 2)


# Greedy BFS Algorithm


def greedy_bfs_search(map2d, start, goal):
    # The priority queue
    queue = []
    heapq.heappush(queue, (0, [start]))

    # Visited set to keep track of visited nodes
    visited = set()

    while queue:
        _, path = heapq.heappop(queue)
        current = path[-1]

        # Check if this node has been visited
        if current in visited:
            continue

        # Mark the current node as visited
        visited.add(current)

        # Check if the goal is reached
        if current == goal:
            cost = len(path) - 1  # cost is the number of steps in the path
            return path, cost

        # Get neighbors and add them to the queue
        for next in get_neighbors(current, map2d, visited):
            if next not in visited:
                new_path = list(path)
                new_path.append(next)
                # Push to the queue with priority based on manhattan distance
                heapq.heappush(queue, (manhattan_distance(next, goal), new_path))

    return False


def a_star_search(map2d, start, goal):
    frontier = PriorityQueue()
    frontier.add(start, 0)

    # keep track of the path
    came_from = {}
    cost_so_far = {}

    # Initialize with the start point
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.isEmpty():
        current = frontier.remove()

        # Check if the goal has been reached
        if current == goal:
            # Reconstruct path
            path = []
            while current != None:
                path.append(current)
                current = came_from[current]

            path.reverse()  # reverse the path to start->goal
            cost = len(path) - 1
            return path, cost

        for next in get_neighbors(current, map2d, came_from):
            new_cost = cost_so_far[current] + 1  # Assumes a cost of 1 for each step
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + manhattan_distance(next, goal)
                frontier.add(next, priority)
                came_from[next] = current

    return False


def two_phase_heuristic(current, goal, map2d, obstacle_info):
    """
    this one is basically a heuristic that first navigates horizontally to clear the rotated-H-shaped obstacle,
    then switches to manhattan distance towards the goal.
    """
    ytop, ybot, xwall = obstacle_info
    x, y = current

    # Define minx and maxx based on the obstacle information
    minx = xwall
    maxx = xwall  # If the obstacle is a single line; adjust if it's wider

    if x <= minx or x >= maxx:
        # Once past the obstacle, use Manhattan distance
        return manhattan_distance(current, goal)

    # If still in line with the obstacle, prioritize horizontal movement
    horizontal_distance_to_clear_obstacle = min(abs(x - minx), abs(x - maxx))
    vertical_distance_to_goal = abs(y - goal[1])
    return horizontal_distance_to_clear_obstacle + vertical_distance_to_goal


def a_star_heuristic(map2d, start, goal, obstacle_info):
    frontier = PriorityQueue()
    frontier.add(start, 0)

    came_from = {}
    cost_so_far = {}

    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.isEmpty():
        current = frontier.remove()

        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path, len(path) - 1

        for next in get_neighbors(current, map2d, came_from):
            new_cost = cost_so_far[current] + 1
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + two_phase_heuristic(next, goal, map2d, obstacle_info)
                frontier.add(next, priority)
                came_from[next] = current

    return False


# Generic search function
def search(map2d, start, goal, algorithm):
    if algorithm == 'random':
        return random_search(map2d, start, goal)
    elif algorithm == "bfs":
        return bfs_search(map2d, start, goal)
    elif algorithm == "dfs":
        return dfs_search(map2d, start, goal)
    elif algorithm == "gbfs":
        return greedy_bfs_search(map2d, start, goal)
    elif algorithm == "astar":
        return a_star_search(map2d, start, goal)
    else:
        raise ValueError("Unknown algorithm")
