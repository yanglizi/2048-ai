from board import *

playerTurn = True


def evaluate(b):
    smoothWeight = 0.1
    monoWeight  = 1.0
    emptyWeight  = 2.7
    maxWeight    = 1.0
    return smoothness_2(b)*smoothWeight + monotonicity(b)*monoWeight + (math.log(empty_places_count(b)) if empty_places_count(b) != 0 else 0)*emptyWeight + maxvalue(b)*maxWeight

def alphabeta_minimax(b , alpha , beta , depth , maxdepth):
    newb = copy.deepcopy(b)
    this_alpha = alpha
    this_beta  = beta
    this_value = 0
    return_value = 0 

    bestdirc = ' '

    result = {0:this_value,1:bestdirc}

    
    if depth == maxdepth:
        this_value = evaluate(newb)
        return {0:this_value}
    
    elif depth < maxdepth:
        if depth & 1 == 0:
            for dirc in direction:
                # print 'dirc=%s'%(dirc)
                b_before = copy.deepcopy(newb)
                b_after = copy.deepcopy(newb)
                direction[dirc](b_after)
                # result = copy.deepcopy(alphabeta_minimax(newb , this_alpha , this_beta , depth+1 , maxdepth))
                # print depth,dirc,is_board_changed(b_before,b_after)
                if is_board_changed(b_before,b_after):
                    result[0] = (alphabeta_minimax(b_after , this_alpha , this_beta , depth+1 , maxdepth))[0]
                    # print result
                    return_value = result[0]
                    if this_alpha <  return_value:
                        this_alpha = return_value
                        bestdirc = dirc
                        # print this_alpha,return_value,bestdirc
                    if this_alpha >=  this_beta:
                        return {0:this_beta,1:bestdirc}
            this_value = this_alpha
            return {0:this_value,1:bestdirc}

        elif depth & 1 == 1:
            for x in range(len(newb)):
                for y in range(len(newb[0])):
                    if newb[x][y] == 0:
                        for i in range(2 , 5 , 2):
                            # print 'x=%d'%(x)
                            newb[x][y] = i
                            # result = copy.deepcopy(alphabeta_minimax(newb , this_alpha , this_beta , depth+1 , maxdepth))
                            result[0] = (alphabeta_minimax(newb , this_alpha , this_beta , depth+1 , maxdepth))[0]
                            return_value = result[0]
                            if this_beta > return_value:
                                this_beta = return_value
                            if this_alpha >=  this_beta:
                                return {0:this_alpha}           
                        newb[x][y] = 0
            this_value = this_beta
            return {0:this_value}

    

# def alphabeta_minimax2(b , alpha , beta , depth , positions , cutoffs):
#     newb = copy.deepcopy(b)

#     this_alpha = alpha
#     this_beta  = beta
#     this_value = 0

#     bestmove = 'null'

#     result = { }

#     b_before = copy.deepcopy(newb)

#     global playerTurn 
    

#     if playerTurn == True:
#         for move in direction:
#             print move
#             b_after = copy.deepcopy(newb)
#             direction[move](b_after)
            
#             print_board(b_after)
#             if is_board_changed(b_before,b_after):
#                 positions += 1
#                 # if is_win(newb):
#                 #     return { 'move': move, 'value': 10000 , 'positions': positions, 'cutoffs': cutoffs }
#                 if depth == 0:
#                     result = {'move':move,'value':evaluate(newb)}
#                 else:
#                     result = alphabeta_minimax2(b_after , this_alpha , this_beta  , depth-1 , positions , cutoffs)
#                     # print result
#                     if result['value'] > 9900:
#                         result['value'] -= 1

#                     positions = result['positions']
#                     cutoffs = result['cutoffs']

#                 # print this_alpha,result['value']

#                 if this_alpha <  result['value']:
#                     this_alpha = result['value']
#                     bestmove = move
#                     this_value = this_alpha
#                 if this_alpha >= beta:
#                     cutoffs += 1
#                     print bestmove
#                     return { 'move': bestmove, 'value': beta , 'positions': positions, 'cutoffs': cutoffs }
#         playerTurn = False

    
#     elif playerTurn == False:
#         for x in range(len(newb)):
#                 for y in range(len(newb[0])):
#                     # print x
#                     if newb[x][y] == 0:
#                         for i in range(2 , 5 , 2):
#                             newb[x][y] = i
#                             result = alphabeta_minimax2(newb , this_alpha , this_beta  , depth-1 , positions , cutoffs)                            
#                             if this_beta > result['value']:
#                                 this_beta = result['value']
#                                 this_value = this_alpha
#                             if this_alpha >= beta:
#                                 cutoffs += 1
#                                 return { 'move': 'null', 'value': alpha , 'positions': positions, 'cutoffs': cutoffs }
#                         newb[x][y] = 0
#         playerTurn == True
#     # print bestmove
#     return { 'move': bestmove, 'value': alpha , 'positions': positions, 'cutoffs': cutoffs }






# def alphabeta_minimax3(b , alpha , beta , depth , positions , cutoffs):
#     newb = copy.deepcopy(b)

#     this_alpha = alpha
#     this_beta  = beta
#     this_value = 0

#     bestmove = 'null'

#     result = { }

#     b_before = copy.deepcopy(newb)

#     global playerTurn 
    
#     if depth == 0:
#         result = {'value':evaluate(newb)}

#     elif playerTurn == True:
#         for move in direction:
#             # print move
#             b_after = copy.deepcopy(newb)
#             direction[move](b_after)
            
#             print_board(b_after)
#             if is_board_changed(b_before,b_after):
#                 positions += 1
#                 # if is_win(newb):
#                 #     return { 'move': move, 'value': 10000 , 'positions': positions, 'cutoffs': cutoffs }
#                 result = alphabeta_minimax2(b_after , this_alpha , this_beta  , depth-1 , positions , cutoffs)
#                 # print result
#                 if result['value'] > 9900:
#                     result['value'] -= 1

#                 positions = result['positions']
#                 cutoffs = result['cutoffs']

#                 # print this_alpha,result['value']

#                 if this_alpha <  result['value']:
#                     this_alpha = result['value']
#                     bestmove = move
#                     this_value = this_alpha
#                 if this_alpha >= beta:
#                     cutoffs += 1
#                     # print bestmove
#                     return { 'move': bestmove, 'value': beta , 'positions': positions, 'cutoffs': cutoffs }
#         playerTurn = False

    
#     elif playerTurn == False:
#         for x in range(len(newb)):
#                 for y in range(len(newb[0])):
#                     # print x
#                     if newb[x][y] == 0:
#                         for i in range(2 , 5 , 2):
#                             newb[x][y] = i
#                             result = alphabeta_minimax2(newb , this_alpha , this_beta  , depth-1 , positions , cutoffs)                            
#                             if this_beta > result['value']:
#                                 this_beta = result['value']
#                                 this_value = this_alpha
#                             if this_alpha >= beta:
#                                 cutoffs += 1
#                                 return { 'move': 'null', 'value': alpha , 'positions': positions, 'cutoffs': cutoffs }
#                         newb[x][y] = 0
    
#         playerTurn == True
#     # print bestmove
#     return { 'move': bestmove, 'value': alpha , 'positions': positions, 'cutoffs': cutoffs }
