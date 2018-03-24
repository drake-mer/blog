---
layout: default
title:  "Haskell Cheat Sheet"
date:   2018-03-22 19:20:34 +0200
categories: haskell datastructures
---

# Defining a data type

## Traffic-light 

A simple traffic light enumeration-like model:

```haskell
data TrafficLight = Red | Yellow | Green deriving (Show, Eq)
```

The Traffic light can have three states only: 

- `Red`: all cars must stop
- `Yellow`: all cars must stop
- `Green`: cars may pass

Each one of this state is a value _per se_, they are all separated
by a `|` character.

Let us define a _transition_ function that will illustrate 
two features of Haskell: _type annotation_ and _pattern matching_

```haskell
nextState :: TrafficLight -> TrafficLight -- type annotation
nextState Red = Green
nextState Yellow = Red
nextState Green = Yellow
```

## Binary Tree

A simple binary tree structure:

```haskell
data BinaryTree a = EmptyBinaryTree | Node a (BinaryTree a) (BinaryTree a) deriving (Show, Eq)
```

This example is slightly more complex in that it can have only two _states_
or _values_. This data structure is considered recursive because the
_algebraic data type_ `BinaryTree` is at the left hand side of the 
statement and also at the right hand side.

We will demonstrate how to compute the maximum depth of this binary
tree. Recursion is key in the way we can study the maximum depth:

```haskell
depth :: (BinaryTree a) -> Int
depth EmptyBinaryTree = 0
depth (Node _ left right) = 1 + (max (depth left) (depth right))
```
