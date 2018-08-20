---
layout: default
title:  "Insights on Backtracking and DFS Algorithm"
date:   2017-11-23 19:20:34 +0200
categories: backtracking blogging algorithm
---

## Introduction

### About this Article

In this article, I will outline a very personal study of the backtracking 
algorithm. At the moment of writing this introduction, the orientation 
taken is to come from a concrete description of the problem and then to
derive an algorithmic implementing a solution to this problem.

### What is Backtracking

Backtracking etymology is straightforward. It means to keep track
of an already taken path, like the breadcrumbs in _Little Thumb_.

In computer science, more specifically, _backtracking_ relates to
a family of algorithms where one of the sequence of operations can 
be played back.

The need for backtracking comes from the fact that, sometimes, a sequence
of evaluations leads to a dead-end. You need then, to continue the search
for the appropriate result, to get back to one of the previous state of the 
calculation.

### Datastructure

The term _Backtracking_ really let us think to a two way data structure.

If we are investigating a linear data-structure, there really is two
possibility I can think of: 

  - an array, with an index _i_ keeping track of the
  position. This way, one can move up by incrementing _i_, or down by
  decrementing _i_.

  - A doubly linked list, which allows to get the _next_ or the _previous_
  element simply by construction of what is a doubly linked list.

Trying to transpose one of this two data structures to a tree, I think
that the _doubly linked list_ model is more accurate.

A single schema to illustrate our need:

```mermaid
graph LR
A(Round edge) --> B (Round edge)
A(Round edge) --> C (Round edge)
B(Round edge) --> D (Round edge)
B(Round edge) --> E (Round edge)
B(Round edge) --> F (Round edge)
```

In this case, let us assume we are on `F` and we need to actually get on `C`.
The path would be actually:

```
F -> B -> A -> C
```

Then, the classic tree which allow to have only descendent 
references would be useless. Each node must contains a reference
to its parent, which is unique because we are working with a tree.

There is two possibilities here to consider:
  - keep working in the _tree_ fashion
  - start thinking that we are working with a bidirectional acyclic graph instead

Each node has at max three neighbours:
  - one parent
  - two children

The representation of a graph we are used to is 
the adjacency list. So basically, the tree above would read:

```haskell
data BiDiGraph a = EmptyNode | Node a (BiDiGraph a) (BiDiGraph a) (BiDiGraph a)
```

From this point, the look for a good path is quite the same as a well known algorithm,
_Depth First Search_.

And then we have the backtracking algorithm that comes with at no cost.

