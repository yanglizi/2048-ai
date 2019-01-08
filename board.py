import random
import copy
import math

board = [
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0],
    [0,0,0,0]
]

# board = [
#     [2, 8, 2, 4],
#     [4, 32, 64, 16],
#     [4, 64, 128, 64],
#     [4, 2048, 1024, 8]
# ]

def print_board(b):
    print '================'
    for row in b:
        print row
    print '================'


def init(b):
    for x in range(0, len(b)):
        for y in range(0, len(b[x])):
            b[x][y] = 0
    # choices = [0,1,2,3]
    choices = range(0,len(b))
    picked = 0
    while picked < 2:
        x = random.choice(choices)
        y = random.choice(choices)
        #print 'picked ('+str(x)+', '+str(y)+')'
        value = 2 if random.random() > 0.2 else 4
        if b[x][y] == 0:
            b[x][y] = value
            picked+=1

def empty_places_count(b):
    count = 0
    # check if board is full
    for x in range(0, len(b)):
        for y in range(0, len(b[x])):
            if b[x][y] == 0:
                count += 1 
    return count
               

def generate(b):
    # choices = [0,1,2,3]
    choices = range(0,len(b))
    picked = 0
    h = empty_places_count(b)
    if h >= 1:
        while picked < 1:
            x = random.choice(choices)
            y = random.choice(choices)
            value = 2 if random.random() > 0.2 else 4
            # print 'picked ('+str(x)+', '+str(y)+') = %d'%(value)
            if b[x][y] == 0:
                b[x][y] = value
                picked+=1
                # print b[x][y]
        return True
    return False

def is_board_changed(before,after):
    for x in range(0, len(before)):
        for y in range(0, len(before[x])):
            if(before[x][y] != after[x][y]):
                return True
    return False

def is_game_over(b):
    if empty_places_count(b) == 0:
        for x in range(0, len(b)):
            for y in range(0, len(b[x])-1):
                if b[x][y] == b[x][y+1]:
                    return False
        for y in range(0,len(b[x])):
            for x in range(0,len(b)-1):
                if b[x][y] == b[x+1][y]:
                    return False
        return True
    else: 
        return False

def is_win(b):
    for x in range(0, len(b)):
            for y in range(0, len(b[x])):
                if b[x][y] == 2048:
                    return True
    return False


def maxvalue(b):
    max = 0
    for x in range(0, len(b)):
            for y in range(0, len(b[x])):
                if b[x][y] >= max:
                    max = b[x][y]
    return max


def smoothness(b):
    smoothvalue = 0 
    for x in range(0,len(b)):
        for y in range(0,len(b[0])-1):
            smoothvalue -= abs((math.log(b[x][y]) if b[x][y] != 0 else 0 )/(math.log(2)) - (math.log(b[x][y+1]) if b[x][y+1] != 0 else 0)/(math.log(2)))
    
    for y in range(0,len(b[0])):
        for x in range(0,len(b)-1):
            smoothvalue -= abs((math.log(b[x][y]) if b[x][y] != 0 else 0 )/(math.log(2)) - (math.log(b[x+1][y]) if b[x+1][y] != 0 else 0)/(math.log(2)))
    return smoothvalue

def smoothness_2(b):
    smoothvalue = 0
    value = 0
    targetvalue = 0
    for x in range(0,len(b)):
        for y in range(0,len(b[0])):
            if b[x][y] != 0:
                value = math.log(b[x][y]) / math.log(2)
                if b[x][3] != 0:
                    targetvalue = math.log(b[x][3]) / math.log(2)
                    smoothvalue -= abs(value - targetvalue)
                if b[3][y] != 0:
                    targetvalue = math.log(b[3][y]) / math.log(2)
                    smoothvalue -= abs(value - targetvalue)
    return smoothvalue




def monotonicity(b):
    total = [0,0,0,0]

    for x in range(0,len(b)):
        current = 0
        thenext = current + 1
        while(thenext < 4):
            while thenext < 4 and b[x][thenext] == 0:
                thenext = thenext + 1
            if thenext >= 4:
                thenext = thenext - 1
            currentvalue = math.log(b[x][current])/math.log(2) if b[x][current] != 0 else 0
            thenextvalue = math.log(b[x][thenext])/math.log(2) if b[x][thenext] != 0 else 0
            if currentvalue > thenextvalue:
                total[0] += thenextvalue - currentvalue
            elif currentvalue < thenextvalue:
                total[1] += currentvalue - thenextvalue
            current = thenext
            thenext = thenext + 1
        
    for y in range(0,len(b[0])):
        current = 0
        thenext = current + 1
        while(thenext < 4):
            while thenext < 4 and b[thenext][y] == 0:
                thenext = thenext + 1
            if thenext >= 4:
                thenext = thenext - 1
            currentvalue = math.log(b[current][y])/math.log(2) if b[current][y] != 0 else 0
            thenextvalue = math.log(b[thenext][y])/math.log(2) if b[thenext][y] != 0 else 0
            if currentvalue > thenextvalue:
                total[2] += thenextvalue - currentvalue
            elif currentvalue < thenextvalue:
                total[3] += currentvalue - thenextvalue
            current = thenext
            thenext = thenext + 1

    return max(total[0], total[1]) + max(total[2], total[3])



def up(b):
    sco = 0
    add_time_of_line = []

    for x in range(0, len(b)):
        for y in range(0, len(b[x])):
            add_time_of_line.append(0)
            if b[x][y] != 0:
                for i in range(x-1,-1,-1):
                    if b[i][y] == b[i+1][y] and add_time_of_line[y] == 0:
                        b[i][y]+=b[i+1][y]
                        b[i+1][y]=0
                        sco = sco + b[i][y]
                        add_time_of_line[y] = 1
                        break
                    elif b[i][y] != b[i+1][y]:                        
                        if b[i][y] == 0:
                            b[i][y]=b[i+1][y]
                            b[i+1][y]=0
                        else:
                            break                        
                    # print 'i='+str(i)+', y='+str(y)
    return sco

def down(b):
    sco = 0
    b.reverse()
    sco = up(b)
    b.reverse()
    return sco

def left(b):
    sco = 0
    turn_right(b)
    sco = up(b)
    turn_left(b)
    return sco

def right(b):
    sco = 0
    turn_left(b)
    sco = up(b)
    turn_right(b)
    return sco

def turn_right(b):
    # b_right = [
    #     [0,0,0,0],
    #     [0,0,0,0],
    #     [0,0,0,0],
    #     [0,0,0,0]
    # ]

    b_right = copy.deepcopy(b)
    for x in range(0, len(b_right)):
        for y in range(0, len(b_right[x])):
            b_right[x][y] = 0

    i=0
    for y in range(0,len(b_right[0])):
        j=0
        for x in range(len(b_right)-1,-1,-1):
            b_right[i][j] = b[x][y]
            #print b[x][y]
            #print_board(b_down)
            j=j+1
        i=i+1
    for x in range(0,len(b_right[0])):
        for y in range(len(b_right)-1,-1,-1):
            b[x][y] = b_right[x][y]

def turn_left(b):
    # b_left = [
    # [0,0,0,0],
    # [0,0,0,0],
    # [0,0,0,0],
    # [0,0,0,0]
    # ]   


    b_left = copy.deepcopy(b)
    for x in range(0, len(b_left)):
        for y in range(0, len(b_left[x])):
            b_left[x][y] = 0

    i=0
    for y in range(len(b_left[0])-1,-1,-1):
        j=0
        for x in range(0,len(b_left)):
            b_left[i][j] = b[x][y]
            #print b[x][y]
            #print_board(b_down)
            j=j+1
        i=i+1
    for x in range(0,len(b_left[0])):
        for y in range(len(b_left)-1,-1,-1):
            b[x][y] = b_left[x][y]


direction = {'up':up , 'down':down , 'left':left , 'right':right}
