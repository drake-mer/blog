---
layout: default
title:  "Backtracking Tutorial (Backtracking Made Simple)"
date:   2017-11-23 19:20:34 +0200
categories: backtracking blogging algorithm
---

## Introduction

### What is backtracking.

Backtracking etymology is straightforward. It means to keep track
of an already taken path, like the breadcrumbs in _Little Thumb_.

In computer science, more specifically.

is one of those fancy word to describe an algorithm
very much used in artificial intelligence. What is interesting about
backtracking is the fact that it allows many variants and improvemnts
according to the situation.

This article will focus on a simple implementation of backtracking
for a simple problem, with implementation in Python and Haskell.
To finish with, we will talk of the possible refinments of the backtracking
algorithm, which are need in most practical cases, especially in gaming.

## Problem

To start with, we want a good problem to work on. There is many problems out
there that can be solved by backtracking, but to keep the matter simple and
the implementation also simplistic, we will talk about the infamous tic-tac-toe
game.

First of all, let us say that the backtracking algorithm is really efficient
when you have a knowledge of all the possible future states of the
problem you are attempting to solve.

### Description of the game

Everybody knows tic-tac-toe, so it is not a big deal to present it simply.
The game takes place on a 3x3 board. The game is a 2 player game, each player
putting a mark of him on the board. The first player having 3 consecutive marks,
either diagonally or horizontally or vertically wins the game.

### Prediction of the opponent moves

The difficulty in applying the backtracking to the tic-tac-toe algorithm comes
from the fact that the opponent is able to make several possible moves, and so
the backtracking algorithm must evaluate each of them before returning

## Implementation

The board will be represented by a list of list, ie a 3x3 matrix. If a case is
empty, the value is 0. For player 1 mark, the value is 1, and for player 2 mark,
the value is 2.

The game starts like that:

```python
init_state = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]
```

### Short evaluation of the game tree

We are going to evaluate, with player 1 starting, the complexity of the
game tree evaluation.

To start with, player 1 has 9 possibilities. Then player 2 has 8, and
after player 2 played, it remains 7 possibilities to player1, and so on.
So the extent of possible games is exactly 9!. This remains quite a tractable
number but it still has 362880 possibilities, and that is huge for
such a trivial game.

### Description of the algorithm

The backtracking algorithm is trying to find all the paths leading to
a winning move. To do so, it must evaluate all the possible move and
discard all moves that lead to an eventual disaster. The problem comes
from the fact that we cannot predice the opponent's choices.

But in the possible moves we have, there is very certainly a path
that will give us victory. The backtracking algorithm here may let us
play until it finds out that we don't have any valid move remaining.
To find the first winning move (move the faster), we are going to
use breadth first search.

```
import itertools as iter
from pprint import pprint


def log(*args, **kwars):
    def wrapper(*args, **kwargs):
        grid, = args
        turn = kwargs['turn']
        print("game state -- turn={}, grid=\n{}".format(turn, pprint.pformat(g, width=15)))

    return wrapper

def is_winning_move(move, grid):
   x, y = move  # coordinates of the move
   grid[y][x] = 1  # set the grid

   if win(1, grid) == 1:
       return True

   for board in possible_boards(grid):               # list of player 2 possible moves
       for move in possible_moves(board):            # list of player 1 possible moves
           if is_winning_move(move, board, 1):          # recursion depth-first
               return True

   return False


def possible_boards(board):
    for x in range(3):
        for y in range(3):
             if board[y][x] == 0:
                 new = [row[:] for row in board]
                 new[y][x] = 2
                 yield new



def possible_moves(board):                           # list of player 1 possible moves
    for x in range(3):                               # iter over the whole 3x3 board
        for y in range(3):                           #
            if board[y][x] == 0:                     # if the space is unoccupied
                yield (x, y)                         # possible_moves is an iterator


def play(move, board, player):
    b = [ r[:] for r in board ]
    x, y = move
    b[y][x] = player
    return b

def win(player, grid):
    def w( y):                                     # inner function to tell if all
         for case in y:                              # the positions on the row, col,
             if case != player:                           # or diagonal are belonging to
                 return False                        # player (x).
         return True

    diag1 = (grid[x][x] for x in range(3))           # first diagonal
    diag2 = (grid[x][2-x] for x in range(3))         # second diagonal
    rows = (row for row in grid)
    cols = (col for col in zip(*grid))
    chain = iter.chain((diag1, diag2), rows, cols)
    for ch in chain:
        if w(chain):
            return True

    return False


def play_game(grid, turn=0):
    for move in possible_moves(grid):
        if is_winning_move(move, grid, 1):
            grid = play(move, grid, 1)
            for move in possible_moves(grid):
                grid = play(move, grid, 2)
    print("turn = {}, grid = \n {}".format(turn, pprint.pformat(grid)))
    play_game(grid, turn=turn+1)

if __name__ == '__main__':
    grid = [[0]*3 * for _ in range(3)]
    play_game(grid)

```
