
# Project 02 - Mario(more)


Implement a program that prints out a double half-pyramid of a specified height, per the below.

```
$ python mario.py
Height: 4
   #  #
  ##  ##
 ###  ###
####  ####
```
  

## Background

  

Toward the beginning of World 1-1 in Nintendo’s Super Mario Brothers, Mario must hop over two "half-pyramids" of blocks as he heads toward a flag pole.

  

## Specification

  
-   Write, in a file called  `mario-more.py`, a program that recreates these half-pyramids using hashes (`#`) for blocks.
    
-   To make things more interesting, first prompt the user for the half-pyramids' heights, a positive integer between  `1`  and  `8`, inclusive. (The height of the half-pyramids pictured above happens to be  `4`, the width of each half-pyramid  `4`, with a gap of size  `2`  separating them.)
    
-   If the user fails to provide a positive integer no greater than  `8`, you should re-prompt for the same again.
    
-   Then, generate (with the help of  `print`  and one or more loops) the desired half-pyramids.
    
-   Take care to left-align the bottom-left corner of the left-hand half-pyramid with the left-hand edge of your terminal window.

## Usage

Your program should behave per the example below. Assume that the underlined text is what some user has typed.

```
$ python mario-more.py
Height: 4
   #  #
  ##  ##
 ###  ###
####  ####
```

```
$ python mario-more.py
Height: 0
Height: 4
   #  #
  ##  ##
 ###  ###
####  ####
```

```
$ python mario-more.py
Height: -5
Height: 4
   #  #
  ##  ##
 ###  ###
####  ####
```

```
$ python mario-more.py
Height: -5
Height: five
Height: 40
Height: 24
Height: 4
   #  #
  ##  ##
 ###  ###
####  ####
```
