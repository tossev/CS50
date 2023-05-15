
# Project 01 - Mario(less)
Implement a program that prints out a half-pyramid of a specified height, per the below.

Implement a program that prints out a half-pyramid of a specified height, per the below.

```
$ python mario-less.py
Height: 5
    #
   ##
  ###
 ####
#####

$ python mario.py
Height: 3
  #
 ##
###
```
## Background

Toward the end of World 1-1 in Nintendo’s Super Mario Brothers, Mario must ascend a "half-pyramid" of blocks before leaping (if he wants to maximize his score) toward a flag pole.
## Specification
-   Write, in a file called  `mario-less.py`  in  `~/workspace/pset6/mario/less/`, a program that recreates this half-pyramid using hashes (`#`) for blocks.
    
-   To make things more interesting, first prompt the user for the half-pyramid’s height, a positive integer between  `1`  and  `8`, inclusive.
    
-   If the user fails to provide a positive integer no greater than  `8`, you should re-prompt for the same again.
    
-   Then, generate (with the help of  `print`  and one or more loops) the desired half-pyramid.
    
-   Take care to align the bottom-left corner of your half-pyramid with the left-hand edge of your terminal window.
## Usage

Your program should behave per the example below.
```
$ ./mario-less.py
Height: 4
   #
  ##
 ###
####
```

```
$ ./mario-less.py
Height: 0
```

```
$ ./mario-less.py
Height: -5
Height: 4
   #
  ##
 ###
####
```

```
$ ./mario-less.py
Height: -5
Height: five
Retry: 40
Height: 24
Height: 4
   #
  ##
 ###
####
```
