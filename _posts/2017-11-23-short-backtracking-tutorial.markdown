---
layout: default
title:  "Backtracking Tutorial (Backtracking Made Simple)"
date:   2017-11-23 19:20:34 +0200
categories: backtracking blogging algorithm
---

## Introduction

_Backtracking_ is one of those fancy word to describe an algorithm
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
def is_winning_move((x,y), grid):
    
    

