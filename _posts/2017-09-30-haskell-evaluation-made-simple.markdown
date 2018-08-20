---
layout: default
title:  Precedence order of evaluation for AST building in Haskell
date:   2017-10-01 19:20:34 +0200
categories: haskell blogging
---

## Introduction

I wanted to write a page of drills for practicing monads in Haskell, and I
wanted to be accessible, so as I started to write things about type annotations,
I noticed that somethings here couldn't be left out and had to be written down.
The result is this article, covering to some extents type annotation and precedence
in Haskell, enough to get started and make the most out of the type system.

The subtility of the evaluation performed on the abstract syntax tree are let
out, we aim just to clarify and illustrate some of the most notable features
of the Haskell syntax.

The style aims to be simple
and understandable by almost anybody who has done a little bit of programming
before. It was written a sunday afternoon after going for another subject 
Actually, the notions covered here are quite important and even fundamental
for at least writing good (working) Haskell code.

## Type system and annotations

### What are type signatures ?

As for many languages, when writing a function, the type of its arguments must be 
known before actually running the program. This is known as static typing.

To tell what are the types of the variables are in an expression, Haskell is using 
type annotation, which are however not mandatory since the compiler may deduce
the type of the variables in an expression through **type inference**, 
whenever it is possible \(sometimes it is not\). 

In any case, it is often encouraged to write annotations as much as possible.

Let us consider a function of two variables, say _x_
and _y_. The mathematical
notation for it is often viewed as:

$$ 
f: \begin{cases} 
        \mathbb{R}^2 &\to \mathbb{R} \\ 
             x,y   &\mapsto f(x,y)
   \end{cases}
$$

Which tells us that the function takes as an input two real numbers and returns
us a real number (we say it is a function from R² to R).

The pure analog for the set of real numbers in computer science is the type
float. So $x$ and $y$ would have respectively type `Float` and `Float`.

You would define the arguments of this function in the GHCi REPL like this:

```
Prelude> let x= 2::Float
Prelude> x
2.0
Prelude> let y= 3::Float
Prelude> y
3.0
Prelude> 
```

or in a text file:

```haskell
x::Float
x=2
y::Float
y=2
```

Now, functions need their type annotations as well. But we will need to bring some
conceptual explanation about _curryfication_. The word itself comes from a mathematician,
whose name is fortuitously [Haskell Curry](https://fr.wikipedia.org/wiki/Haskell_Curry).

If I asked you to tell me
what is the following function:

$$ g:\begin{cases} \mathbb{R}&\to\mathbb{R}\\ y&\mapsto f(3,y)\end{cases} $$

What would be your answer ? 

You would probably tell me that $f$ is a function
of a real number, $y$, into the set of real numbers. Actually, it would simply be the function 
$f$ for a fixed value of $x$. By fixing _x_ to a predefined value, we obtain another function of one single
variable. This is sometimes used when you calculate partial derivatives of a function (remembering
first grade calculus course).

In Haskell, the curryfication is the way everything is working. To tell things plainly, you can 
easily obtain the later function (let us call it `g`) by fixing $x$, that is to say by writing

```haskell
g = f 3  
```

But then, let's go back to the type annotation problem once more. $g$ is a function from the
real set to the real set. We said later that the analog of $\mathbb{R}$ from the point of view
of the computer is `Float` (or `Double` for what matters, but let's keep it straight to the 
_point_).

Well at this point, one can't help but give the type annotation: we would plainly write
with all the ASCII characters at hand:

```haskell
g :: Float -> Float
g = f 3
```

And moreover:

```haskell
f:: Float -> Float -> Float
f x y = x + y
```

## Type annotation for multi-variable function 

What are all this arrows in the previous definition? Well, as it happens, you
can, coming from all I told previously, interprete them quite naively. You must actually read
type definition from the left to the right (like in normal english). Moreover, the precedence
of the arrows may be understood with the highest priority being let to the arrow at the farthest
left (we are leftist by default in Haskell).

So, if you'd happen to rewrite the type definition with parenthesis to illustrate this precedence
rule (I let the function definition outside of it for the sake of conciseness), you would write:

```haskell
f:: Float -> (Float -> Float)
```

Now, what is the type of (Float -> Float) ? Isn't it just the type of the function `g` we 
just defined above ? Bingo. Then, we can reword the definition of `f` as a function that
takes as an input a floating point number, and returns a _function that takes a floating point
number and returns a floating point number_.

Just for the sake of completeness, let us examine this point of view with a function of three 
real numbers (let us call it _h_ this time).

The usual mathematical definition would be:

$$ 
h : \begin{cases} \mathbb{R}^3 &\to \mathbb{R} \\
x, y, z &\mapsto h(x,y,z)\end{cases}
$$

So, we are going to take back our later argument and try to see if, by writing naively the 
parenthetised type annotation, we will find back the precedence rule I told you about previously.

Let us do it.

So, we start by fixing _x_. Then we obtain kind of the function of two variables we previously
had (_f_). We keep the parenthetized version of this later function (since we know it works plain),
and we have so:

```haskell
h :: Float -> ( Float -> (Float -> Float) )
h x y z = x + y + z
```

So yes, it is quite plain evidence that the precedence rule (left arrow as 
the highest precedence) we previously told you about is applying.


## From the type system to evaluation order

We just described at some extent how the Haskell type system is working. This is quite cool.
Furthermore, the type system is really cool. I like it. But let's not get 
ourselves lost in affectionate arguments and, that is the evaluation order (I am not talking
about evaluation of the argument but rather of the priority in building the blocks of the 
abstract syntax tree).

Because of the later precedence rule, the arguments of a function in Haskell are evaluated from
the left to the right. That is, to actually compute `h 1 2 3`, we must first now what `h 1` is.
So, from the precedence system we just talked about, the real way the later program is executed
is by computing (or rather, evaluating), from the innermost parenthesis to the outermost:

`( ( ( h 1 ) 2 ) 3 )`

It is confusing, isn't it ? Quite, huh ? Not usual at least, since from the moment you went to 
school, calculate the result succesively as a successive application of small function has not 
been really natural. Or was it to begin with? Anyway, letting aside the _naturalness_ problem,
we will try to demonstrate some of the dangers with this evaluation system you could be unaware of.

If you try to understand quite well the type system, it will lead you to write Haskell code faster
and with much less error than if you had to put parenthesis around each members of your equations
just for the sake of not having the compiler throwing errors at you constantly.

So, imagine that you want to take the 10 first odd positive integers. Let us write naively that 
thing using `filter` and `take`, then we will carefully proceed to the parenthetization and 
function joining.

Naively, it would read: `take 10 filter odd [1..]`. But this is wrong to let it in such a form, because
of the evaluation rule precedence.

So, what is this all about ?

Let us examine the `take` type:
```
Prelude> :t take
take :: Int -> [a] -> [a]
```

That would actually read, following the precedence rule I just talked you about:
`take :: Int -> ([a] -> [a])`

What it tells you is that take is a function that first take an Int, and returns a function
that takes as its single argument a list and returns a list of the same type of objects.

Now, following the precedence rule for evaluation, we start at the left-most part of our special
equation, that is `take 10`. What is wrong with that ? Nothing. It actually returns the function
we just talked about.

## Building solid expressions in Haskell

At this point, what goes wrong? It is the next evaluation step. If we think about the 
parenthetized version of our equation, it will read `( ( ( ( take 10 ) filter ) odd ) [1..] )`.

Let us examine the type of filter:

```haskell
Prelude> :t filter
filter :: (a -> Bool) -> [a] -> [a]
```

But we just told that the argument of `(take 10)` is of type `[a]` (namely, a list of objects of 
type `a`). Huh-huh. That is not exactly the type of our `filter` object. Nah. They are actually
quite different kind of objects.

### Parenthetization

Let us examine, at this point, the parenthetized version of our filter type annotation:

```
filter :: (a -> Bool) -> ( [a]->[a] )
```

Se we are not even close! We want ultimately have a `[a]`, but this stupid filter is returning a 
`([a] -> [a])` function! And that, if we didn't consider the problem of feeding something as a first
argument to our filter function.

Tough problem it seems. At this point, in the Haskell world, there is three choices I may be aware
of. The first, obvious one is to preempt the default evaluation order by putting parenthesis around
`filter` and its arguments, to force them to be evaluated as a single argument.

This would read:

```
take 10 (filter odd [1..])
```

Simple, isn't it?

### The `$` infix operator

The second option would be to use the `$` infix operator operator:

```
Prelude>:t ($)
(a -> b) -> a -> b
```

Simply put, the application of the `$` operator would read:
```
take 10 $ filter odd [1..]
```

In its infix notation, we would say that `$` is forcing the regroupment of the right most part
of the equation. The more traditionnal notation would be:

```
($) (take 10) (filter odd [1..])
```

This does not save us much parenthesis, but we will do it to explain how `$` works actually.
From its type annotation :

```haskell
($) :: (a -> b) -> a -> b
```
or, using our convenient parenthesizing model:

```haskell
($) :: (a -> b) -> (a -> b)
```
Let us first consider the following truth: the type of 
`a` or `b` may be anything (function _or_ primitive type, it doesn't matter). This 
function will thus apply to any relevant type following the type inference procedure
we talked about earlier. But let us consider the first argument of `($)`. We saw
that `take 10` has type `(take 10) :: [a] -> [a]` yummy yummy. It feets quite neatly
in the definition of `($)`. Then, the first part of the equation does actually that.

When we write the strictly equivalent formulations: `($) (take 10)` or `(take 10 $)`,
the effect is to force the evaluation of the left part, behind the `$` of the equation
(this works because `$` is an infix operator, so there is a bit of magic involved in it.
The firts formulation ($) (take 10) has not much interest, because we could parenthetize
everything and let the `($)` out, it would have the same effect).

Now, another magical effect of the infix operators are that the two arguments are 
evaluated separately. So before the program is trying to know what to do with  
`($) (take 10)` applied to filter (that would let us in the same dire situation as 
at the beginning, it will try to know what (filter odd) is. And it fits ! yes, 
`filter odd` is fitting quite neatly into the type definition, since its type annotation
is `odd :: Integral a => a -> Bool`. The rest is history, as they say. Once the firts 
part has been evaluated, we know that we have at hand an object of type `[a]->[a]` which
is evaluated as an object of type `[a]`, easily fed to our `(take 10 $) :: [a]->[a]` object,
and then evaluated to being:

```haskell
Prelude> take 10 $ filter odd [1..]
[1,3,5,7,9,11,13,15,17,19]	
```

### Function composition, or curryfication

What we would really like, is to use the curryfication at its maximum potential. The
magic you just saw with the infix operator is quite interesting, indeed, and you can
remember its precedence behaviour in other Haskell situations. And God knows, there is
a shitload of operators in Haskell we don't even have notion of.

So what we would like to be is to be genuine Haskellers and use function composition.

A composition of function makes use of a function that take a function and then returns
another function. Rember the definition of `$`, it does just that. Actually, the sole
purpose of `$` is to be an infix operator and to force evaluation precedence, but by
himself, it quite does nothing. We might even say that this is kind of the identity
operators for functions. Indeed, `(($) take 10)` is just `(take 10)`. And we don't even
need to write `(($) take 10)`. Indeed, we have `(($) take)` the same as `take`, and then
evaluation proceeds as usual for the remaining arguments.

You can try with function of 2, 3 or even 15 variables:


The expression `(($) (+) a b)` is merely `( ( ( ($) (+) ) a ) b )`, and since
`$` is the identity for a function, it gives us simply `( (+) a ) b` for the AST.


etc.

Well, in our case we want to compose two function. But the chaining must operate on the 
same type of argument, otherwise it won't work. The fundamental building block of our
equation is the list, so we will need to compose functions that work on lists.
It would actually reads like that:

```haskell
f1 = (take 10) :: [a] -> [a]
f2 = (filter odd) :: [a] -> [a]

res = f1.f2 [1..]
```

where `.` is another infix operator, called _function composition operator_

Let's have a look at his type:

`(.) :: (a -> b) -> (b -> c) -> a -> c`

Or using our special parenthetizing:

`(.) :: (a -> b) -> ((b -> c) -> a -> c)`

Then

`(.) :: (a -> b) -> ((b -> c) -> (a -> c))`

So, simply put, `.` takes two functions and return a third one,
as you would expect from a function composition operator.

Since this is an infix operator, it will force the evaluation of its left
part and right part separately as in Haskell traditional `lefty` fashion.

So then, is evaluated as parenthetized. `take 10 :: [a] -> [a]` is ok.

But remember, because of the infix operator logic, `filter odd [1..]` is going
to have its type evaluated completely before feeding it to `.`. And we will have
something like:

`(filter odd [1..]) :: Integral a => [a]`

Well, this is not exactly the function we were looking for as a second argument.

At this point, we have two choices. We can put parenthesis around the `.` operator to
limit the evaluation to the function we want to, and to apply the joined function to 
a given argument, or we can reuse the `$` infix operator:

`(take 10 . filter odd) [1..] :: Integral a => [a]`

or 

`take 10 . filter odd $ [1..] :: Integral a => [a]`

The evaluation of order of infix operator depends on the
fixity of the operator, and if this is a right infix operator
`infixr` or `infixl`.

Let's invent an operator which would be, say, `(**)`.

Since this in `infixr`, the right most part of the first operator is evaluated
first.

The `a ** b ** c` would actually be 

```haskell
a ** ( b ** ( c ) )
```

And the operator precedence (fixity), the higher it is, the higher the operator
has precedence.

For example, in the previously seen expression:

```haskell
take 10 . filter odd $ [1..9]
```

The `.` (dot) is an `infixr 9` operator, and the `$` (dollar) is an `infixr 0` operator.

This means that the arguments of `$` are always evaluated last, or in the last place.
The right most part of two equivalent operators is evaluated first.

