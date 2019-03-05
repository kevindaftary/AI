import numpy as np
import copy
from collections import defaultdict
import math


def read_input():
    global file
    global fout
    file = open("input.txt","r")
    fout = open("output.txt","w")
    lines = file.readlines()
    grid_size = int(lines[0].rstrip())
    num_cars = int(lines[1].rstrip())
    num_obstacles = int(lines[2].rstrip())
    loc_of_obstacles = []
    start_loc_of_cars = []
    end_loc_of_cars = []
    grid = -1*np.ones(shape=(grid_size,grid_size))
    
    for i in range(3,3+num_obstacles):
        lin = lines[i].rstrip().split(",")
        loc_of_obstacles.append([int(lin[1]),int(lin[0])])
        grid[int(lin[1])][int(lin[0])]-=100
    for j in range(i+1, i+1+num_cars):
        lin = lines[j].rstrip().split(",")
        start_loc_of_cars.append([int(lin[1]), int(lin[0])])
    for k in range(j+1, j+1+num_cars):
        lin = lines[k].rstrip().split(",")
        end_loc_of_cars.append([int(lin[1]), int(lin[0])])
    return start_loc_of_cars,end_loc_of_cars, grid, num_cars, grid_size, num_obstacles, loc_of_obstacles


def generate_new_car_grid(grid, end_loc_of_car):
    grid[end_loc_of_car[0]][end_loc_of_car[1]] += 100
    return grid



def calculate_utility(grid, start, end, size, obstacle):
    GAMMA = 0.9
    EPSILON = 0.1
    
    util = map(list, grid)
    util_prime = map(list, grid)
    policy = defaultdict()
    temp = defaultdict()
    while True:
        DELTA = 0
        util = copy.deepcopy(util_prime)
        temp = copy.deepcopy(policy)
        for x_coord in range(size):
            for y_coord in range(size):
                if [x_coord,y_coord]==end:
                    util_prime[x_coord][y_coord] = np.float64(grid[x_coord][y_coord])
                else:
                    up_val = np.float64(util[x_coord-1 if x_coord>0 else x_coord][y_coord])
                    left_val = np.float64(util[x_coord][y_coord-1 if y_coord>0 else y_coord])
                    right_val = np.float64(util[x_coord][y_coord+1 if y_coord<size-1 else y_coord])
                    down_val = np.float64(util[x_coord+1 if x_coord<size-1 else x_coord][y_coord])
                    dec_up = (0.7*up_val)+0.1*(left_val+right_val+down_val)
                    dec_left = (0.7*left_val)+0.1*(up_val+right_val+down_val)
                    dec_right = (0.7*right_val)+0.1*(up_val+left_val+down_val)
                    dec_down = (0.7*down_val)+0.1*(up_val+left_val+right_val)
                    choice_val = max(dec_up,dec_left,dec_right,dec_down)
                    if choice_val == dec_left:
                        temp_dec = "left"
                    if choice_val == dec_right:
                        temp_dec = "right"
                    if choice_val == dec_down:
                        temp_dec = "down"
                    if choice_val == dec_up:
                        temp_dec = "up"
                    util_prime[x_coord][y_coord] = np.float64(grid[x_coord][y_coord]) + (GAMMA*choice_val)
                    policy[x_coord,y_coord] = temp_dec
                    DELTA = max(abs(util[x_coord][y_coord]-util_prime[x_coord][y_coord]),DELTA)
        if DELTA < EPSILON*(1-GAMMA)/GAMMA:
            break
    return util,temp    


def turn_left(move):
    if move=="left":
        return "down"
    elif move=="right":
        return "up"
    elif move == "up":
        return "left"
    return "right"


def turn_right(move):
    if move=="left":
        return "up"
    elif move=="right":
        return "down"
    elif move == "up":
        return "right"
    return "left"    


def simulation(grid,policy,start, end):
    if start == end:
        return 100
    pos_x = start[0]
    pos_y = start[1]
    end_pos_x = end[0]
    end_pos_y = end[1]
    final_val = 0
    for j in range(10):
        np.random.seed(j)
        point = 0
        swerve = np.random.random_sample(1000000)
        k=0
        while pos_x != end_pos_x or pos_y!=end_pos_y:
            move = policy[pos_x,pos_y]
            if swerve[k]>0.7:
                if swerve[k]>0.8:
                    if swerve[k]>0.9:
                        move = turn_right(turn_right(move))
                    else:
                        move = turn_right(move)
                else:
                    move = turn_left(move)
            if move == "left":
                pos_y = pos_y-1 if pos_y>0 else pos_y
            elif move == "right":
                pos_y = pos_y + 1 if pos_y<len(grid)-1 else pos_y
            elif move =="up":
                pos_x = pos_x-1 if pos_x>0 else pos_x
            else:
                pos_x = pos_x+1 if pos_x<len(grid)-1 else pos_x
            point += grid[pos_x][pos_y]
            k=k+1
        pos_x = start[0]
        pos_y = start[1]
        final_val += point
    final_val = (math.floor(np.float64(final_val/10.0)))
    return int(final_val)


start_loc_of_cars, end_loc_of_cars, grid, num_cars, grid_size, num_obstacles, loc_of_obstacles = read_input()
global fout
for i in range(num_cars):
    grid = generate_new_car_grid(grid, end_loc_of_cars[i])
    util_values, policy = calculate_utility(grid, start_loc_of_cars[i],end_loc_of_cars[i],grid_size, num_obstacles)
    total = simulation(grid, policy, start_loc_of_cars[i], end_loc_of_cars[i])
    fout.write(str(total))
    fout.write("\n")
    grid[end_loc_of_cars[i][0]][end_loc_of_cars[i][1]] -= 100