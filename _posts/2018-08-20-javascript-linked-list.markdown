---
layout: default
title:  "JavaScript: a linked list example"
date:   2018-08-20 19:20:34 +0200
categories: javascript datastructures
---

# Why implementing linked lists in JavaScript ?

Before hand, I must recall that I am a total beginner in JavaScript, so I'll do 
my best. Do not hesitate to correct me in the comment section 
for obvious error or small rectifications, really anything that could improve the overall quality.

At least two motivations:

- The first is to learn how to use javascript to implement a simple data structure.
Prototyping objects with javascript is one of the main features that makes this language
very cool, and manipulation of linked list needs a little API so it will be a neat exercise
to learn javascript basics.

- Second interest is that the linked list is ubiquitous in programming (esp. functional
programming). As a [kata](https://en.wikipedia.org/wiki/Kata_(programming)) to relearn fundamental
data structures, it will do :)

# Implementation

I will  be inspired by the Haskell API for linked lists (haa, that lack of
creativity. You often rely on your basic training when struggling to find new ideas, 
that's why the idea of _discipline_ is so dear to me).

We will define elementary operations to apply on lists and also a
standard function (`max` will do).

In Haskell the two operators are ``:`` (`cons`) and ``++`` (`mappend`).

The `cons` operator is already implemented  as the `append` and the 
`mappend` function as the `concat` method (let's keep things simple).

The new prototype is now, after some minutes of debugging and learning how to use the `nod`
interpreter:


```javascript
// Notice how the `append` definition has changed.
// The type of `this.next` is now a LinkedList, and
// the value is stored in a dedicated container (value).

module.exports = {
    LinkedList: function(value) {
        this.next = null;
        this.value = value;
        this.append = function (obj) {
            var newList = new this.constructor(obj);
            newList.next = this;
            return newList;
        }

        this.concat = function (listToAppend) {
            console.log(this.toString())
            if (this.next === null){
                this.next = listToAppend;
            } else {
                this.next.concat(listToAppend)
            }
        }
        // Let's implement a toString() method, because having
        // a textual representation of objects is always nice.
        this.toString = function(){
            if (this.next != null){
                return this.value + "," + this.next.toString();
            }
            return this.value;
        }
        this.max = function(){
            console.log(this.toString());
            if (this.next === null) {
                return this.value;
            } else {
                return Math.max(this.value, this.next.max())
            }
        }
    }
}
```

All of that can be a little tricky. 

Notice that I use only recursive functions.
  
- The `append` method use a recursive call to the constructor
- Also, the `toString` method is implemented recursively
- Same for `max`, etc

## Let's test

Fire the node interpreter and load the above file:

```js

> ll = require('./javascriptLL.js')
> x = (new ll.LinkedList(-2)).append(4).append(2).append(3)
> x.toString()
'3,2,4,-2'
> y = (new ll.LinkedList(8)).append(3))
'3,8'
> x.concat(y)
> x.toString()
'3,2,4,-2,3,8'
> m = x.max()
> m
8
```

Everything seems to work, we could add the `head` and `tail` methods (easy enough).

Some small remarks and warnings: the empty list is not properly defined here because
the constructor returns as a default a list with a single element, whose value is `null`
eventually if no argument is passed as a parameter.

This make things not quite as precise as how it is implement in Haskell. However it was good for fun and practice :)

For you guys really more interested in pure FP, you can check the following links:

- [Mostly adequate guide](https://github.com/MostlyAdequate/mostly-adequate-guide): haskell copy-pasted into a javascript library. Interesting, reuse a lot of Haskell interfaces to implement pure FP in javascript.
- [Awesome FP js](https://github.com/stoeffel/awesome-fp-js): A huge list of libraries that can be used to be full FP style with javascript. Have fun !

