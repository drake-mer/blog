import itertools as iter
import pprint
import random


def log_game_turn(f, *args, **kwargs):

    def wrapper(*args, **kwargs):
        grid, = args
        turn = kwargs.pop('turn', 0)
        print("turn={}, grid=\n{}".format(turn, pprint.pformat(grid, width=15)))
        return f(grid, turn=turn)

    return wrapper


def log_check_winning_move(f, *args, **kwargs):

    def wrapper(*args, **kwargs):
        grid, player, opponent = args
        print("checking grid state =\n{}".format(pprint.pformat(grid, width=15)))
        return f(*args, **kwargs)

    return wrapper


class NoMoreAvailableMoves(Exception):
    pass


# @log_check_winning_move
def is_winning_board(grid, player, opponent):
    if win(opponent, grid):
        return False
    if win(player, grid):
        return True
    for board in possible_boards(grid, opponent):         # list of player 2 possible moves
        for new_board in possible_boards(board, player):
            return is_winning_board(new_board, player, opponent)  # recursion depth-first

    return False

def possible_boards(board, player):
    """list of possible boards after player 2 played"""
    for mov in possible_moves(board):
        yield play(mov, board, player)

def play_random_move(board, player):
    moves = list(possible_moves(board))
    if moves:
        return play(random.choice(moves), board, player)
    else:
        raise NoMoreAvailableMoves()

def possible_moves(board):                           # list of player 1 possible moves
    for x in range(3):                               # iter over the whole 3x3 board
        for y in range(3):                           #
            if board[y][x] is None:                  # if the space is unoccupied
                yield (x, y)                         # possible_moves is an iterator

def play(move, board, player):
    b = [ r[:] for r in board ]
    x, y = move
    b[y][x] = player
    return b

def win(player, grid):

    diag1 = (grid[x][x] for x in range(3))           # first diagonal
    diag2 = (grid[x][2-x] for x in range(3))         # second diagonal
    rows = (row for row in grid)
    cols = (col for col in zip(*grid))
    chain = iter.chain((diag1, diag2), rows, cols)
    def w(y):                                        # inner function to tell if all
         for case in y:                              # the positions on the row, col,
             if case != player:                      # or diagonal are belonging to
                 return False                        # player (x).
         return True

    for ch in chain:
        if w(ch):
            return True

    return False

@log_game_turn
def play_game(grid, turn=0):
    g = [ r[:] for r in grid ]
    if win(2, g):
        return False
    elif win(1, g):
        return True
    else:
        try:
            for gr in possible_boards(g, player=1):
                if is_winning_board(gr, 1, 2):
                    gr2 = play_random_move(gr, 2)
                    return play_game(gr2, turn=turn+1)
        except NoMoreAvailableMoves:
            return None

if __name__ == '__main__':
    grid = [[0]*3 for _ in range(3)]
    print(
        "opponent 1: backtracking\n"
        "opponent 2: random moves")
    result = play_game(grid)
    if result is None:
        print("this is a draw")
    elif result:
        print("opponent 1 wins")
    else:
        print("opponent 2 wins")
