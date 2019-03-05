import signal
import time

def isStateSafe(row, column):
    
    row_multiplier = [-1, 1, 0, 0, 1, 1, -1, -1]
    column_multiplier = [0, 0, -1, 1, 1, -1, 1, -1]

    for k in range(0, 8):
        iterator = 1
        try:
            while True:
                if grid_state[row + iterator * row_multiplier[k]][column + iterator * column_multiplier[k]] == 1: 
                    return False
                iterator += 1
        except IndexError as e:
            pass
    return True

def placePolice(row, pol):
    if (pol == police):
        currSumofState = 0
        sumOfStateTranspose = 0
        sumofLRFlippedState = 0
        sumOfUDFlippedState = 0
        global max_path_sum
        for iterator_x in range(N):
            for iterator_y in range(N):
                if grid_state[iterator_x][iterator_y] == 1:
                    currSumofState += path_cost_matrix[iterator_x][iterator_y]
                    sumOfStateTranspose += path_cost_matrix[iterator_y][iterator_x]
                    sumofLRFlippedState += path_cost_matrix[iterator_x][N - iterator_y - 1]
                    sumOfUDFlippedState += path_cost_matrix[N - iterator_x - 1][iterator_y]
        max_path_sum = max(max_path_sum, currSumofState, sumOfStateTranspose, sumofLRFlippedState, sumOfUDFlippedState)
        return
    if police - pol <= N - row:
        col_iterator = 0
        while col_iterator < N:
        #for col_iterator in range(N):
            if isStateSafe(row, col_iterator):
                grid_state[row][col_iterator] = 1
                if pol == police:
                    col_iterator+=1
                else:
                    placePolice(row + 1, pol + 1)
                    grid_state[row][col_iterator] = 0
            col_iterator +=1
        placePolice(row + 1, pol)

def TimePeriodHandler(signum, frame):
    global f_out
    f_out.write(str(max_path_sum))
    exit()

def getInput():

    f = open('input.txt', 'r')
    lines = f.readlines()
    N = int(lines[0])
    police = int(lines[1])
    scooter = int(lines[2])
    

    path_cost_matrix = [[0 for x in range(N)] for x in range(N)]

    for line in lines[3:]:
        coords = line.split(",")
        xcoords = int(coords[0])
        ycoords = int(coords[1])
        path_cost_matrix[xcoords][ycoords] = path_cost_matrix[xcoords][ycoords] + 1
    return N, police, path_cost_matrix


signal.signal(signal.SIGALRM, TimePeriodHandler)
signal.alarm(174)
f_out = open("output.txt", "w")
N,police,path_cost_matrix = getInput()
max_path_sum = -999999
grid_state = [[0 for x in range(N)] for x in range(N)]
placePolice(0, 0)

f_out.write(str(max_path_sum))
f_out.close()