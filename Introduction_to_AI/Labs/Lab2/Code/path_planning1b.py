""" Functions for generating 2D grid maps, for AI Lab 2 - path planning.
"""

import random
import numpy as np
import matplotlib.pyplot as plt
import search_algorithm

percentOfObstacle = 0.9  # 30% - 60%, random


def generateMap2d(size_):
    '''Generates a random 2d map with obstacles (small blocks) randomly distributed.
       You can specify any size of this map but your solution has to be independent of map size

    Parameters:
    -----------
    size_ : list
        Width and height of the 2d grid map, e.g. [60, 60]. The height and width of the map shall be greater than 20.

    Returns:
    --------
        map2d : array-like, shape (size_[0], size_[1])
           A 2d grid map, cells with a value of 0: Free cell; 
                                                -1: Obstacle;
                                                -2: Start point;
                                                -3: Goal point;
    '''

    size_x, size_y = size_[0], size_[1]
    # size_x, size_y = 60, 60

    map2d = np.random.rand(size_y, size_x)
    perObstacles_ = percentOfObstacle
    map2d[map2d <= perObstacles_] = 0
    map2d[map2d > perObstacles_] = -1

    yloc, xloc = [np.random.randint(0, size_x - 1, 2), np.random.randint(0, size_y - 1, 2)]
    while (yloc[0] == yloc[1]) and (xloc[0] == xloc[1]):
        yloc, xloc = [np.random.randint(0, size_x - 1, 2), np.random.randint(0, size_y - 1, 2)]

    map2d[xloc[0]][yloc[0]] = -2
    map2d[xloc[1]][yloc[1]] = -3

    start = (xloc[0], yloc[0])
    goal = (xloc[1], yloc[1])

    return map2d, start, goal


# Generate 2d grid map with rotated-H-shape object
def generateMap2d_obstacle(size_):
    size_x, size_y = size_[0], size_[1]

    map2d, start, goal = generateMap2d(size_)

    map2d[map2d == -2] = 0
    map2d[map2d == -3] = 0
    # add special obstacle
    xtop = [np.random.randint(5, 3 * size_x // 10 - 2), np.random.randint(7 * size_x // 10 + 3, size_x - 5)]
    ytop = np.random.randint(7 * size_y // 10 + 3, size_y - 5)
    xbot = np.random.randint(3, 3 * size_x // 10 - 5), np.random.randint(7 * size_x // 10 + 3, size_x - 5)
    ybot = np.random.randint(5, size_y // 5 - 3)

    map2d[ybot, xbot[0]:xbot[1] + 1] = -1
    map2d[ytop, xtop[0]:xtop[1] + 1] = -1
    minx = (xbot[0] + xbot[1]) // 2
    maxx = (xtop[0] + xtop[1]) // 2
    if minx > maxx:
        tempx = minx
        minx = maxx
        maxx = tempx
    if maxx == minx:
        maxx = maxx + 1

    map2d[ybot:ytop, minx:maxx] = -1
    startp = [np.random.randint(0, size_x // 2 - 4), np.random.randint(ybot + 1, ytop - 1)]

    map2d[startp[1], startp[0]] = -2
    goalp = [np.random.randint(size_x // 2 + 4, size_x - 3), np.random.randint(ybot + 1, ytop - 1)]

    map2d[goalp[1], goalp[0]] = -3
    # return map2d, [startp[1], startp[0]], [goalp[1], goalp[0]], [ytop, ybot]
    return map2d, [ytop, ybot, minx]


# helper function for plotting the result
def plotMap(map2d_, path_, title_=''):
    '''Plots a map (image) of a 2d matrix with a path from start point to the goal point.
        cells with a value of 0: Free cell; 
                             -1: Obstacle;
                             -2: Start point;
                             -3: Goal point;
    Parameters:
    -----------
    map2d_ : array-like
        an array with Real Numbers
        
    path_ : array-like
        an array of 2d corrdinates (of the path) in the format of [[x0, y0], [x1, y1], [x2, y2], ..., [x_end, y_end]]
        
    title_ : string
        information/description of the plot

    Returns:
    --------

    '''

    import matplotlib.cm as cm
    plt.interactive(False)

    colors_nn = int(map2d_.max())
    colors = cm.winter(np.linspace(0, 1, colors_nn))

    colorsMap2d = [[[] for x in range(map2d_.shape[1])] for y in range(map2d_.shape[0])]
    # Assign RGB Val for starting point and ending point
    locStart, locEnd = np.where(map2d_ == -2), np.where(map2d_ == -3)

    colorsMap2d[locStart[0][0]][locStart[1][0]] = [.0, .0, .0, 1.0]  # black
    colorsMap2d[locEnd[0][0]][locEnd[1][0]] = [.0, .0, .0, .0]  # white

    # Assign RGB Val for obstacle
    locObstacle = np.where(map2d_ == -1)
    for iposObstacle in range(len(locObstacle[0])):
        colorsMap2d[locObstacle[0][iposObstacle]][locObstacle[1][iposObstacle]] = [1.0, .0, .0, 1.0]
    # Assign 0
    locZero = np.where(map2d_ == 0)

    for iposZero in range(len(locZero[0])):
        colorsMap2d[locZero[0][iposZero]][locZero[1][iposZero]] = [1.0, 1.0, 1.0, 1.0]

    # Assign Expanded nodes
    locExpand = np.where(map2d_ > 0)

    for iposExpand in range(len(locExpand[0])):
        _idx_ = int(map2d_[locExpand[0][iposExpand]][locExpand[1][iposExpand]] - 1)
        colorsMap2d[locExpand[0][iposExpand]][locExpand[1][iposExpand]] = colors[_idx_]

    for irow in range(len(colorsMap2d)):
        for icol in range(len(colorsMap2d[irow])):
            if colorsMap2d[irow][icol] == []:
                colorsMap2d[irow][icol] = [1.0, 0.0, 0.0, 1.0]

    path_ = np.array(path_)
    path = path_.T.tolist()

    plt.figure()
    plt.title(title_)
    plt.imshow(colorsMap2d, interpolation='nearest')
    plt.colorbar()
    plt.plot(path[:][1], path[:][0], color='magenta', linewidth=2.5)
    plt.show()


"""
# map with rotated-H shape obstacle and obstacles randomly distributed
map_h_object, info = generateMap2d_obstacle([60, 60])

# environment information
print("map info: ")
print("y top: ", info[0])
print("t bot: ", info[1])
print("x wall: ", info[2])

plt.clf()
plt.imshow(map_h_object)
plt.show()
"""
'''

#                                                                            COMMENTED CODE IS TO RUN AND ALSO PLOT ALL THE ALGORITHMS. 
map_size = [60, 60]
map_h_object, (ytop, ybot, xwall) = generateMap2d_obstacle(map_size)

# Locate the start and goal positions in the map
locStart, locEnd = np.where(map_h_object == -2), np.where(map_h_object == -3)
start, goal = np.array([locStart[0][0], locStart[1][0]]), np.array([locEnd[0][0], locEnd[1][0]])
start, goal = tuple(start), tuple(goal)

# The search algorithms
algorithm = ['dfs', 'bfs', 'gbfs', 'astar', 'astarh']

for niba in algorithm:
    if niba == "astarh":
        path, cost = search_algorithm.a_star_heuristic(map_h_object, start, goal, (ytop, ybot, xwall))
        if path:
            print(f"Start: {start} -- Goal: {goal}")
            print(f"Path found for astarheuristic, cost of {cost}")
            for value in path:
                print(value)
            plotMap(map_h_object, path)
        else:
            print(f"No path found for astarheuristic.")

    else:
        example_solved_path = search_algorithm.search(map_h_object, start, goal, niba)
        
        # Print and plot the path
        if example_solved_path:
            print("Algorithm is :", niba)
            print(f"Start: {start} -- Goal: {goal}")
            print(f"Path found, cost of {example_solved_path[1]}")
            for value in example_solved_path[0]:
                print(value)
            plotMap(map_h_object, example_solved_path[0])
        else:
            print(f"No path found for {niba}.")

'''

algorithm = ['dfs', 'bfs', 'gbfs', 'astar', 'astarh']


# example fresults = {algo: {'costs': [], 'path_lengths': []} for algo in algorithm}
def run_search_algorithm(algo, map, start, goal, obstacle_info=None):
    if algo == "astarh":
        return search_algorithm.a_star_heuristic(map, start, goal, obstacle_info)
    else:
        return search_algorithm.search(map, start, goal, algo)


# Initialize data collection
results = {algo: {'costs': [], 'path_lengths': []} for algo in algorithm}

num_runs = 20
map_size = [60, 60]

for _ in range(num_runs):
    map_h_object, (ytop, ybot, xwall) = generateMap2d_obstacle(map_size)
    locStart, locEnd = np.where(map_h_object == -2), np.where(map_h_object == -3)
    start, goal = (locStart[0][0], locStart[1][0]), (locEnd[0][0], locEnd[1][0])

    for algo in algorithm:
        result = run_search_algorithm(algo, map_h_object, start, goal, (ytop, ybot, xwall))
        if result:
            path, cost = result
            results[algo]['costs'].append(cost)
            results[algo]['path_lengths'].append(len(path))
        else:
            print(f"No path found for {algo} in run {_}.")

# Analyze the results
for algo, data in results.items():
    avg_cost = np.mean(data['costs'])
    avg_path_length = np.mean(data['path_lengths'])
    print(f"Algorithm: {algo}, Average Cost: {avg_cost}, Average Path Length: {avg_path_length}")
