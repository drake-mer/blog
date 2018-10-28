---
layout: default
title:  Random Number Generation With Haskell
date:   2018-10-28 10:20:34 +0200
categories: haskell blogging
---

# Random Number Generation in Programming

Usually, the random number generators are « pseudo random », which means
that numbers are distributed uniformally by mean of a deterministic algorithm,
of which plenty of versions exist.

The property of a good random generator are such to have a very big period
(Mersenne-Twister random number 
[generator](https://en.wikipedia.org/wiki/Pseudorandom_number_generator)
has a periodicity of 2 at the exponent 19937 minus 1) and a quasi-uniform curve.

Each pseudo random number generator must be initialized with a _seed_ that will 
guarantee that the sequence for the current thread or program starts at an 
undeterministic value.

All this properties of random generators make them not very intuitive to use 
in a language like `C` (because we need to manually initialize the random number
generator) or in purely functional languages (Haskell as the primary one).

The aim of this article is to provide a quick way to get through random 
number generation with the _Standard_ `System.Random` implementation 
in the `random` (>= 1.1 library).

We try to save the future readers to get through a lot of function signatures
and providing an overview as well as most common examples on how to perform
random number generation with Haskell.

The primary motivation of this text is to serve as an helper for the author himself,
it is published with the hope that it can be useful to others.

# Quick Overview of The Implement TypeClasses

## The `RandomGen` TypeClass

The typeclass `RandomGen` specify an interface for common random number generators.
For non-haskellers, a _typeclass_ is the rough equivalent of an `interface` in Java Code:
a specification of some properties that an object must have in order to implement correctly
this interface.

A correct `RandomGen` object must then have a definition for the following
functions:

### The `next` Function

Given a random generator object implementing the `RandomGen` interface,
the `next` function takes an instance of this PRNG and returns an integer coupled
with the same PRNG, but one step further in its sequence.

```haskell
next :: g -> (Int, g)
```

### The `genRange` Function

The `genRange` function returns the range of values that can be returned
by the random number generator.

For instance, a correct implementation of a PRNG returning a random integer
in the set `{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}` will have its `genRange` function
returning the following value:

```haskell
Prelude> genRange myGenerator
(1,10)
```

### The `split` Function

Its definition is:
```haskell
split :: g -> (g, g)
```
Given an instance of a PRNG, it returns two distincts and independant PRNGS from the first.
It is useful if you need to not have the same random number generator used in recursive
call stacks (from the [documentation](http://hackage.haskell.org/package/random-1.1/docs/System-Random.html)).

## The Random TypeClass

As its name indicates, the `Random` TypeClass is concerning random values.
As Haskell is a pure language, a pure function can never be a random number
generator, as the next random value depends on the internal state of the generator.

```haskell

class Random a where
  randomR :: RandomGen g => (a, a) -> g -> (a, g)
  random  :: RandomGen g => g -> (a, g)

```
### The randomR Function

Here, let us give an example. Say `a` is in fact `Int`, then 
`randomR` (short-cut for `randomRange`) type signature is:

```haskell
randomR :: RandomGen g => (Int, Int) -> g -> (Int, g)
```

It is correct, you read well, that indeed, a call to 
`randomR` consumes a pair of `Int` as the range in which
we are going to generate the number and a PRNG `g`.

The state of the generator is passed around as a value.

### The random Function

If we keep our `Int` exemple, then the `random` function
is just a function that will return the next possible value
of the PRNG passed as argument, alongside with the PRNG
in its ulterior state.

### Variants: `randomRs` and `randoms`

The type signature of those functions are the same than for 
`random` and `randomR`, except the type of the returned value, which
is in fact an infinite list of values. 

This can save a lot of book-keeping since the main advantage
is that you don't need to carry around the PRNG between 
each call.

### Global (aka System-Wide) PRNG

Two other functions may be used in the same fashion.

```haskell
randomRIO :: (a, a) -> IO a
randomIO :: IO a
```

The return value is encapsulated into the IO Monad, and that is comprehensible
since we typically issue a random value from a global state (I would guess
that what is under the hood is typically to read a random integer
from `/dev/urandom`, at least that would be my view of it. For non-linux system,
a similar mechanism must be in play.


## Standard PRNG in the `random` Library

The documentation of the `random` library doesn't say which algorithm is used
for this instance of `RandomGen` but it says that it should be at least 
as statistically robust as the minimal standard random number generator
defined in [ref 1: Two fast implementations of the minimal standard random number generator](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.94.3416&rep=rep1&type=pdf)
and [ref 2: Random number generators - good ones are hard to find](https://dl.acm.org/citation.cfm?id=63042).

Here are some demonstration of how to instanciate 
and use that pseudo number generator:

```haskell
import Control.Monad
import System.Random
import Data.Time.Clock.POSIX (getPOSIXTime)

-- genRandomNumbers x: generate a list of x random numbers
genRandomNumbers :: (Random a, Integral a) => Int -> Int -> [a]
genRandomNumbers n seed = take n $ (randoms myGenerator) where
    myGenerator = mkStdGen seed

genRandomNumbersBetween :: Int -> Int -> (Int, Int) -> [Int]
genRandomNumbersBetween n seed (a, b) = take n $ (randomRs (a, b) myGenerator) where
    myGenerator = mkStdGen seed

main :: IO ()
main = do 
    seed <- (round . (* 1000)) <$> getPOSIXTime 
    -- Generate 10 random numbers with a millisecond timestamp
    -- as the seed and display them to the console.
    putStrLn "Print 10 random numbers"
    let numbers = genRandomNumbers 10 seed :: [Int]
    putStrLn (show numbers)
    seed <- (round .(* 1000)) <$> getPOSIXTime
    putStrLn "Print 10 random numbers between 1 and 10"
    let numbers = genRandomNumbersBetween 10 seed (1, 10) :: [Int]
    putStrLn (show numbers)
    return ()
```

## System Random Generator

If you don't want to instanciate the PRNG with a state, you can use directly the system random
number generator. But, it is stuck in the IO monad.

Nevertheless, here are some examples of use:

```haskell
import Control.Monad
import System.Random

main :: IO ()
main = do
    tenRandomNumbers <- replicateM 10 randomIO :: IO [Int]
    putStrLn (show tenRandomNumbers)

    tenRandomNumbersBetween1and10 <- replicateM 10 (randomRIO (1, 10)) :: IO [Int]
    putStrLn (show tenRandomNumbersBetween1and10)
    return ()
```

# Remarks and Other References on the Topic

This [post](https://www.schoolofhaskell.com/school/starting-with-haskell/libraries-and-frameworks/randoms)
is of high quality on the topic. It precises (and it is important to do so) that the PRNG
implemented in `random` is not of cryptographic quality, as such non-suitable for cryptographic
applications.

As for its use in simulations (EG Monte-Carlo), I could not say at the moment of writing.

This user's [question](https://stackoverflow.com/questions/19594655/random-number-in-haskell) on 
stack overflow and the accompanying responses are also quite interesting.

People in the irc channel on #freenode were kind enough to indicate me of the
[Monad.Random](https://hackage.haskell.org/package/MonadRandom-0.1.3/docs/Control-Monad-Random.html)
module, useful for carrying computations with carrying the generator around.
