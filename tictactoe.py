"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # xSum and oSum tracks number of x and o on the board
    xSum = 0
    oSum = 0
    # loop through the board
    for i in range(3):
        for j in range(3):
            # update xSum and oSum
            if board[i][j] == X:
                xSum = xSum + 1
            elif board[i][j] == O:
                oSum = oSum + 1
    # X's turn if xSum == oSum
    if xSum == oSum:
        return X
    # O's turn if xSum > oSum
    elif xSum > oSum:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # initialize list that will store all possible actions
    actions = []
    # loop through board
    for i in range(3):
        for j in range(3):
            # if cell is empty, it is a possible action
            if board[i][j] == EMPTY:
                actions.append((i, j))
    # return list of actions
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # initialize new board as a deep copy of board
    newBoard = copy.deepcopy(board)
    # check if action is valid
    if newBoard[action[0]][action[1]] == EMPTY:
        # make move
        newBoard[action[0]][action[1]] = player(board)
    else:
        # raise exception if action is invalid
        raise ValueError
    return newBoard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # if it is O's turn next, that means we only need to check X's (X just made their move)
    if player(board) == O:
        check = X
    # similarly, we only need to check O's if it is X's turn next
    else:
        check = O

    # initialize win to True, will turn to False if there is no winner
    win = True
    # check diagonal case 1
    for i in range(3):
        if board[i][i] != check:
            win = False
            break
    # return winner if there is a winner
    if win:
        return check
    # do the same for diagonal case 2
    win = True
    for i in range(3):
        if board[2-i][i] != check:
            win = False
            break
    if win:
        return check

    # horizontal cases
    for i in range(3):
        win = True
        for j in range(3):
            if board[i][j] != check:
                win = False
                break
        if win:
            return check

    # vertical cases
    for i in range(3):
        win = True
        for j in range(3):
            if board[j][i] != check:
                win = False
                break
        if win:
            return check

    # return None if there is no winner
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # return True if there is a winner
    if winner(board) != None:
        return True

    # loop through board
    for i in range(3):
        for j in range(3):
            # return False if a cell is still empty
            if board[i][j] == EMPTY:
                return False

    # return True if all cells are full
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # return 1 if winner is X
    if winner(board) == X:
        return 1
    # return -1 if winner is O
    elif winner(board) == O:
        return -1
    # return 0 otherwise
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # return None if board is a terminal board
    if terminal(board):
        return None

    # get list of all available actions
    currActions = actions(board)
    # if current player is O
    if player(board) == O:
        # initialize val to positive infinity (we want to minimize val)
        val = math.inf
        # loop through all possible actions
        for action in currActions:
            # get the max value of the action
            v = max_value(result(board, action), -math.inf, math.inf)
            # update val and store action if new max value is less than the current val
            if v < val:
                val = v
                move = action

    # if current player is X
    elif player(board) == X:
        # initialize val to negative infinity (we want to maximize val)
        val = -math.inf
        # loop through all possible actions
        for action in currActions:
            # get the min value of the action
            v = min_value(result(board, action), -math.inf, math.inf)
            # update val and store action if new min value is greater than the current val
            if v > val:
                val = v
                move = action

    return move


# recursive function that calculates the max value of a given board
def max_value(board, alpha, beta):
    # return utility value if board is a terminal state
    if terminal(board):
        return utility(board)
    # initialize v to negative infinity (we want to maximize v)
    v = -math.inf
    # loop through all possible actions
    for action in actions(board):
        # calculate the min value of each action and update v if new min value is greater than the current v
        v = max(v, min_value(result(board, action), alpha, beta))
        # update alpha
        alpha = max(alpha, v)
        # prune if alpha >= beta
        if alpha >= beta:
            break

    return v


# recursive function that calculates the min value of a given board
def min_value(board, alpha, beta):
    # return utility value if board is a terminal state
    if terminal(board):
        return utility(board)
    # initialize v to positive infinity (we want to minimize v)
    v = math.inf
    # loop through all possible actions
    for action in actions(board):
        # calculate the max value of each action and update v if new max value is less than the current v
        v = min(v, max_value(result(board, action), alpha, beta))
        # update beta
        beta = min(beta, v)
        # prune if alpha >= beta
        if alpha >= beta:
            break

    return v
