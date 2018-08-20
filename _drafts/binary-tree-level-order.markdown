---
layout: default
title:  "Transform a Binary Tree Into a Generic Graph"
date:   2018-05-01 19:20:34 +0200
categories: graphe tree dfs bfs haskell
---

# Introduction

In this article, we focus on how to convert a binary tree into a graph. We start
by writing little basics about binary trees and recursive definitions in Haskell.

I used various sources for this article, also 
- https://www.cs.cmu.edu/~adamchik/15-121/lectures/Trees/trees.html

Problem statement
Binary Trees are falling in the category of one way directed acyclic graphes. If we wanted
to convert it to a basic graph, we would need to track the ancestor node for each node.

# First properties and basic data types of binary trees

## Basic types definitions for binary trees

```haskell
data BinaryTree a = EmptyT | Node a (BinaryTree a) (BinaryTree a)
     deriving (Show, Eq)

type Ancestor a = BinaryTree a
type Current a = BinaryTree a
type Left a = BinaryTree a
type Right a = BinaryTree a
type BinGraph a = [(Current a, Ancestor a, Left a, Right a)]
```

In the `BinGraph a` definition, the first element of the tuple is the current node
and the three other elements are respectively ancestor, left and right nodes.

## Helper functions

When working with binary trees, it is very convenient to have 
the usual helper function to help us structure our algorithm.

The basic functions are acting on a binary tree.

The `val` function is for getting the value of the current Node.
The `left` and `right` functions are respectively to get the left
and right tree from the current Node.

```haskell
val :: BinaryTree a -> Maybe a
val EmptyT = Nothing
val (Node x left right) = Just x

left :: BinaryTree a -> BinaryTree a
left EmptyT = EmptyT
left (Node _ l _) = l

right :: BinaryTree a -> BinaryTree a
right EmptyT = EmptyT
right (Node _ _ r) = r
```

With this basic helper functions, one can easily perform the basic algorithm
on binary tree: 

### Maximum tree depth

```haskell
maxDepth :: BinaryTree -> Int
maxDepth EmptyT = 0
maxDepth (Node _ left right) = 1 + (max (maxDepth left) (maxDepth right))
```

With the following tree:

```haskell
basicTree :: BinaryTree Int
basicTree = (Node 1
              (Node 2
                (Node 3
                  (Node 4 EmptyT EmptyT)
                   EmptyT)
                (Node 8 EmptyT EmptyT))
              EmptyT)
```
we can easily check that the depth is 4:

```ghci
*Main> maxDepth basicTree
4
```

###  Binary tree reversal
  
There has been a really controversial post on the internet about algorithm competency and knowledge
in recruiting developers and tech experts:

http://thecodebarbarian.com/i-dont-want-to-hire-you-if-you-cant-reverse-a-binary-tree

Well, I am not going to give opinionated comments on this :p but at least in Haskell, I think
the basic algorithm can be written easily in a declarative fashion.

So basically, in a tree reversal, the left part becomes the right part and vice-et-versa.

```haskell
reverseTree :: BinaryTree a -> BinaryTree a
reverseTree EmptyT = EmptyT
reverseTree (Node nodeValue leftTree rightTree) =
  (Node nodeValue (reverseTree rightTree) (reverseTree leftTree))
```

Should do the trick :p

# Traversal of trees

## PreOrder traversal

Pre-Order traversal is a synonym for depth-first traversal, with a given
directional preference (either left or right). So basically, the idea would
be to go left as much as possible, then to go back on the right node
if LeftNode is empty, then continue on the left, and so on.

A recursive definition is quite possible and natural for this kind of traversal, but 
we need to keep a stack of the right nodes to visit in case we have to backtrack.

The algorithm is as follow:


```haskell
{- Type definition for the preorder traversal function -}
preOrderTraversal :: (Eq a) => BinaryTree a -> [BinaryTree a] -> [a]

{- end of traversal case: the stack is empty and the tree is a null Node -}
preOrderTraversal EmptyT [] = []

{- The tree is a null Node, but the stack is not empty yet, so we pop
 - from the stack the next node to examine. -}
preOrderTraversal EmptyT ((Node value leftTree rightTree):xs) =
    (value:(preOrderTraversal leftTree newStack))
    where newStack = if (rightTree == EmptyT) then xs else (rightTree:xs)

{- We put the current node value on our result list. 
 - We put the right node on the stack if it is not an empty tree.-}
preOrderTraversal (Node value leftTree rightTree) stack =
    (value:(preOrderTraversal leftTree newStack)) where
    newStack = if (rightTree == EmptyT) then stack else (rightTree:stack)
```

The name _preorder traversal_ comes from the fact that binary tree
are often used to keep a total ordering on nodes' values. For a sorted
binary tree, a preorder traversal would issue all the node in a pre-sorted
list.


## In-Order Traversal

In order traversal can also be recursively programmed.

The idea is similar to the pre-order traversal, but instead of listing the left node 
along the traversal, we go as deep as possible on the left
before issuing a node value on the final list.

A final node can be put on the list if:
  - It has already been traversed (it is the head on the stack)
  - The node has no left Node to continue the recursion

In Haskell, it will then be expressed as the following code:

```haskell
-- inOrderTraversal type definition is identical to the one for the preOrderTraversal
inOrderTraversal :: (Eq a) => BinaryTree a -> [BinaryTree a] -> [a]

-- End of traversal case
inOrderTraversal EmptyT [] = []

-- If the current left node is an empty node, we need to continue
-- with the stack
inOrderTraversal EmptyT (stackHead:stackTail) = inOrderTraversal stackHead stackTail

-- Continue on the left as a default
inOrderTraversal (Node value leftTree rightTree) ((Node headValue headLeftTree headRightTree):stack)
    | leftTree == EmptyT = (headValue:value:(inOrderTraversal headRightTree stack))
    | otherwise = (inOrderTraversal leftTree ((Node value leftTree rightTree):(Node headValue headLeftTree headRightTree):stack))
```


# Example with the simplest possible binary tree

Let us imagine we are working with a binary tree containing three nodes:

```
   a
  / \
 /   \
b     c
```

This tree may be written like:

```haskell
myTree = (Node 'a' (Node 'b' EmptyT EmptyT) (Node 'c' EmptyT EmptyT))
```

How can we compute the binary graph associated with this function ?

The type signature of this function would naively be:

```haskell
binToGraph :: BinaryTree a -> BinGraph a
```

Now, it is very likely that we will need an accumulator for the 
function actually doing the job, because we need a way to keep 
track of the ancestor node when parsing the tree.

So the real function would be

```haskell
binToGraph_ :: BinaryTree a -> BinaryTree a -> BinGraph a
```
Since we return a list and that the function 
If we attempt a generalization, this stuff would read:

Indeed, we would need to go on the left and on the right of the root node,
each one of them having `node` as an ancestor.

```haskell
binToGraph_ ancestor node = curNod ++ leftNode ++ rightNode
    where leftNode = (binToGraph_ node (left node)) 
          rightNode = (binToGraph_ node (right node)) 
	  curNode = [(node, ancestor, left node, right node)]
```

# Deducing the adjacency list

Building the adjacency list is now absolutely easy. We can do it using a hashmap.

Here is the result:

```ghci
*Main> adjacencyList (binToGraph myTree )
fromList [('a',"cb"),('b',"a"),('c',"a")]
```

The whole program in Haskell is written here:

