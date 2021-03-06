# Python implementation of Minimax and simple user-interface on the terminal
def calculateWinner(board):
    lines = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6]
    ]
    draw = 'D'

    for item in lines:
        index1, index2, index3 = item
        if board[index1] == board[index2] == board[index3]:
            return board[index1]

    for item in board:
        if item == '':
            return None

    return draw


def minmax(board, maximizingPlayer):
    empty = []
    for i in range(len(board)):
        if board[i] == '':
            empty.append(i)

    result = calculateWinner(board)
    if result == "X":
        return {'index': 'leaf', 'value': -10, 'depth': 1}
    elif result == "O":
        return {'index': 'leaf', 'value': 10, 'depth': 1}
    elif result == 'D':
        return {'index': 'leaf', 'value': 0, 'depth': 1}

    storage = []
    for i in range(len(empty)):
        tempSquare = board.copy()
        if maximizingPlayer:
            tempSquare[empty[i]] = 'O'
            score = minmax(tempSquare, False)
            storage.append(score)
        else:
            tempSquare[empty[i]] = 'X'
            score = minmax(tempSquare, True)
            storage.append(score)

    bestIdea = {}
    if maximizingPlayer:
        bestScore = -9999999
        bestMove = None
        bestDepth = 999999
        for i in range(len(storage)):
            if storage[i]['value'] == bestScore and storage[i]['depth'] < bestDepth:
                bestScore = storage[i]['value']
                bestMove = empty[i]
                bestDepth = storage[i]['depth'] + 1
            if storage[i]['value'] > bestScore:
                bestScore = storage[i]['value']
                bestMove = empty[i]
                bestDepth = storage[i]['depth'] + 1
        bestIdea['index'] = bestMove
        bestIdea['value'] = bestScore
        bestIdea['depth'] = bestDepth
    else:
        bestScore = 9999999
        bestMove = None
        bestDepth = -999999
        for i in range(len(storage)):
            if storage[i]['value'] == bestScore and storage[i]['depth'] > bestDepth:
                bestScore = storage[i]['value']
                bestMove = empty[i]
                bestDepth = storage[i]['depth'] + 1
            if storage[i]['value'] < bestScore:
                bestScore = storage[i]['value']
                bestMove = empty[i]
                bestDepth = storage[i]['depth'] + 1
        bestIdea['index'] = bestMove
        bestIdea['value'] = bestScore
        bestIdea['depth'] = bestDepth

    return bestIdea

def alphaBeta(board, alpha=-999999999, beta=999999999, maximizingPlayer=True):
    empty = []
    for i in range(len(board)):
        if board[i] == '':
            empty.append(i)

    if calculateWinner(board) == 'X':
        return {'index': 'leaf', 'value': -10}
    elif calculateWinner(board) == 'O':
        return {'index': 'leaf', 'value': 10}
    elif calculateWinner(board) == 'D':
        return {'index':'leaf', 'value': 0}

    if maximizingPlayer:
        bestScore = -999999999
        bestMove = None
        for i in range(len(empty)):
            squareCopy = board.copy()
            squareCopy[empty[i]] = 'O'
            result = alphaBeta(squareCopy, alpha, beta, False)
            temp = max(bestScore, result['value'])
            if temp > bestScore:
                bestScore = temp
                bestMove = empty[i]
            alpha = max(alpha, bestScore)
            if alpha >= beta:
                break
        return {'index':bestMove, 'value':bestScore}
    else:
        bestScore = 999999999
        bestMove = None
        for i in range(len(empty)):
            squareCopy = board.copy()
            squareCopy[empty[i]] = 'X'
            result = alphaBeta(squareCopy, alpha, beta, True)
            temp = min(bestScore, result['value'])
            if temp < bestScore:
                bestScore = temp
                bestMove = empty[i]
            beta = min(beta, bestScore)
            if alpha >= beta:
                break
        return {'index':bestMove, 'value':bestScore}


board = ['O', 'O', 'X', '', 'X', '', '', '', '']
turn = 'Human'
while True:
    if turn == 'Human':
        index = input('Enter where you want to play (0-8): ')
        board[int(index)] = 'X'
    else:
        index = alphaBeta(board,-999999999,999999999, True)['index']
        board[index] = 'O'
    if turn == 'Human':
        print('--------------Human plays--------------')
        print(str(board[0])+' | '+str(board[1])+' | '+str(board[2]))
        print(str(board[3])+' | '+str(board[4])+' | '+str(board[5]))
        print(str(board[6])+' | '+str(board[7])+' | '+str(board[8]))
    else:
        print('--------------AI plays--------------')
        print(str(board[0])+' | '+str(board[1])+' | '+str(board[2]))
        print(str(board[3])+' | '+str(board[4])+' | '+str(board[5]))
        print(str(board[6])+' | '+str(board[7])+' | '+str(board[8]))

    state = calculateWinner(board)
    if state == 'X':
        print('Human wins')
        break
    elif state == 'O':
        print('AI wins')
        break
    elif state == 'D':
        print('This is a draw')
        break

    if turn == 'Human':
        turn = 'AI'
    else:
        turn = 'Human'
