---
layout: default
title:  "Haskell Cheat Sheet"
date:   2018-03-22 19:20:34 +0200
categories: haskell datastructures
---

# Defining a data type

## Algebraic datatype: a Traffic-light modelization

A simple traffic light enumeration-like model:

```haskell
data TrafficLight = Red | Yellow | Green deriving (Show, Eq)
```

The Traffic light can have three states only: 

- `Red`: all cars must stop
- `Yellow`: all cars must stop
- `Green`: cars may pass


A _transition_ function could be defined that will give the next 
state of the traffic light according to its present state.


```haskell
nextState :: TrafficLight -> TrafficLight -- type annotation
nextState Red = Green
nextState Yellow = Red
nextState Green = Yellow
```

## Binary Tree Data Structure and Depth of a Binary Tree

A simple binary tree structure:

```haskell
data BinaryTree a = EmptyBinaryTree | Node a (BinaryTree a) (BinaryTree a) deriving (Show, Eq)
```

This is called a recursive algebraic datatype.

The depth of this binary tree can be computed using
this function:

```haskell
depth :: (BinaryTree a) -> Int
depth EmptyBinaryTree = 0
depth (Node _ left right) = 1 + (max (depth left) (depth right))
```
