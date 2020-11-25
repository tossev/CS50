# Project 06 - Reize
Implement a program that resizes BMPs.

```
$ ./resize 4 small.bmp large.bmp
```
## Specification
Implement a program called  `resize`  that resizes (i.e., enlarges) 24-bit uncompressed BMPs by a factor of  `n`.

-   Implement your program in a file called  `resize.c` .
    
-   Your program should accept exactly three command-line arguments, whereby
    
    -   the first (`n`) must be a positive integer less than or equal to  `100`,
        
    -   the second must be the name of a BMP to be resized, and
        
    -   the third must be the name of the resized version to be written.
        
    
    + If your program is not executed with such, it should remind the user of correct usage, as with  `printf`, and  `main`  should return  `1`.
    
-   Your program, if it uses  `malloc`, must not leak any memory. Be sure to call  `free`.
## Usage

Your program should behave per the examples below.

```
$ ./resize
Usage: ./resize n infile outfile
$ echo $?
1
```

```
$ ./resize 2 small.bmp larger.bmp
$ echo $?
0
```
## Background

To reiterate a bit from that lab, recall that a file is just a sequence of bits, arranged in some fashion. A 24-bit BMP file, then, is essentially just a sequence of bits, (almost) every 24 of which happen to represent some pixel’s color. But a BMP file also contains some "metadata," information like an image’s height and width. That metadata is stored at the beginning of the file in the form of two data structures generally referred to as "headers," not to be confused with C’s header files. (Incidentally, these headers have evolved over time. This problem only expects that you support the latest version of Microsoft’s BMP format, 4.0, which debuted with Windows 95.) The first of these headers, called  `BITMAPFILEHEADER`, is 14 bytes long. (Recall that 1 byte equals 8 bits.) The second of these headers, called  `BITMAPINFOHEADER`, is 40 bytes long. Immediately following these headers is the actual bitmap: an array of bytes, triples of which represent a pixel’s color. (In 1-, 4-, and 16-bit BMPs, but not 24- or 32-, there’s an additional header right after  `BITMAPINFOHEADER`  called  `RGBQUAD`, an array that defines "intensity values" for each of the colors in a device’s palette.) However, BMP stores these triples backwards (i.e., as BGR), with 8 bits for blue, followed by 8 bits for green, followed by 8 bits for red. (Some BMPs also store the entire bitmap backwards, with an image’s top row at the end of the BMP file. But we’ve stored this problem set’s BMPs as described herein, with each bitmap’s top row first and bottom row last.) In other words, were we to convert the 1-bit smiley above to a 24-bit smiley, substituting red for black, a 24-bit BMP would store this bitmap as follows, where  `0000ff`  signifies red and  `ffffff`  signifies white.

```
ffffff  ffffff  0000ff  0000ff  0000ff  0000ff  ffffff  ffffff
ffffff  0000ff  ffffff  ffffff  ffffff  ffffff  0000ff  ffffff
0000ff  ffffff  0000ff  ffffff  ffffff  0000ff  ffffff  0000ff
0000ff  ffffff  ffffff  ffffff  ffffff  ffffff  ffffff  0000ff
0000ff  ffffff  0000ff  ffffff  ffffff  0000ff  ffffff  0000ff
0000ff  ffffff  ffffff  0000ff  0000ff  ffffff  ffffff  0000ff
ffffff  0000ff  ffffff  ffffff  ffffff  ffffff  0000ff  ffffff
ffffff  ffffff  0000ff  0000ff  0000ff  0000ff  ffffff  ffffff
```

Because we’ve presented these bits from left to right, top to bottom, in 8 columns, you can actually see the red smiley if you take a step back.

To be clear, recall that a hexadecimal digit represents 4 bits. Accordingly,  `ffffff`  in hexadecimal actually signifies  `111111111111111111111111`  in binary.

Now look at the underlying bytes that compose  `smiley.bmp`. Within CS50 IDE’s file browser, right- or control-click  **smiley.bmp**  and select  **Open as hexadecimal**  in order to view the file’s bytes in hexadecimal (i.e., base-16). In the tab that appears, change  **Start with byte**  to  **54**, change  **Bytes per row**  to  **24**, change  **Bytes per column**  to  **3**. Then click  **Set**.  **If unable to change these values, try clicking View > Night Mode and try again**. You should see the below, byte 54 onward of  `smiley.bmp`. (Recall that a 24-bit BMP’s first 14 + 40 = 54 bytes are filled with metadata, so we’re simply ignoring that for now.)

```
ffffff ffffff 0000ff 0000ff 0000ff 0000ff ffffff ffffff
ffffff 0000ff ffffff ffffff ffffff ffffff 0000ff ffffff
0000ff ffffff 0000ff ffffff ffffff 0000ff ffffff 0000ff
0000ff ffffff ffffff ffffff ffffff ffffff ffffff 0000ff
0000ff ffffff 0000ff ffffff ffffff 0000ff ffffff 0000ff
0000ff ffffff ffffff 0000ff 0000ff ffffff ffffff 0000ff
ffffff 0000ff ffffff ffffff ffffff ffffff 0000ff ffffff
ffffff ffffff 0000ff 0000ff 0000ff 0000ff ffffff ffffff
```

So,  `smiley.bmp`  is 8 pixels wide by 8 pixels tall, and it’s a 24-bit BMP (each of whose pixels is represented with 24 ÷ 8 = 3 bytes). Each row (aka "scanline") thus takes up (8 pixels) × (3 bytes per pixel) = 24 bytes, which happens to be a multiple of 4.

It turns out, though, that BMPs are stored a bit differently if the number of bytes in a scanline is not, in fact, a multiple of 4. In  `small.bmp`, for instance, is another 24-bit BMP, a green box that’s 3 pixels wide by 3 pixels wide. If you view it (as by double-clicking it), you’ll see that it resembles the below, albeit much smaller. (Indeed, you might need to zoom in again to see it.)

![small.png](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAJYAAACWCAYAAAA8AXHiAAAEJGlDQ1BJQ0MgUHJvZmlsZQAAOBGFVd9v21QUPolvUqQWPyBYR4eKxa9VU1u5GxqtxgZJk6XtShal6dgqJOQ6N4mpGwfb6baqT3uBNwb8AUDZAw9IPCENBmJ72fbAtElThyqqSUh76MQPISbtBVXhu3ZiJ1PEXPX6yznfOec7517bRD1fabWaGVWIlquunc8klZOnFpSeTYrSs9RLA9Sr6U4tkcvNEi7BFffO6+EdigjL7ZHu/k72I796i9zRiSJPwG4VHX0Z+AxRzNRrtksUvwf7+Gm3BtzzHPDTNgQCqwKXfZwSeNHHJz1OIT8JjtAq6xWtCLwGPLzYZi+3YV8DGMiT4VVuG7oiZpGzrZJhcs/hL49xtzH/Dy6bdfTsXYNY+5yluWO4D4neK/ZUvok/17X0HPBLsF+vuUlhfwX4j/rSfAJ4H1H0qZJ9dN7nR19frRTeBt4Fe9FwpwtN+2p1MXscGLHR9SXrmMgjONd1ZxKzpBeA71b4tNhj6JGoyFNp4GHgwUp9qplfmnFW5oTdy7NamcwCI49kv6fN5IAHgD+0rbyoBc3SOjczohbyS1drbq6pQdqumllRC/0ymTtej8gpbbuVwpQfyw66dqEZyxZKxtHpJn+tZnpnEdrYBbueF9qQn93S7HQGGHnYP7w6L+YGHNtd1FJitqPAR+hERCNOFi1i1alKO6RQnjKUxL1GNjwlMsiEhcPLYTEiT9ISbN15OY/jx4SMshe9LaJRpTvHr3C/ybFYP1PZAfwfYrPsMBtnE6SwN9ib7AhLwTrBDgUKcm06FSrTfSj187xPdVQWOk5Q8vxAfSiIUc7Z7xr6zY/+hpqwSyv0I0/QMTRb7RMgBxNodTfSPqdraz/sDjzKBrv4zu2+a2t0/HHzjd2Lbcc2sG7GtsL42K+xLfxtUgI7YHqKlqHK8HbCCXgjHT1cAdMlDetv4FnQ2lLasaOl6vmB0CMmwT/IPszSueHQqv6i/qluqF+oF9TfO2qEGTumJH0qfSv9KH0nfS/9TIp0Wboi/SRdlb6RLgU5u++9nyXYe69fYRPdil1o1WufNSdTTsp75BfllPy8/LI8G7AUuV8ek6fkvfDsCfbNDP0dvRh0CrNqTbV7LfEEGDQPJQadBtfGVMWEq3QWWdufk6ZSNsjG2PQjp3ZcnOWWing6noonSInvi0/Ex+IzAreevPhe+CawpgP1/pMTMDo64G0sTCXIM+KdOnFWRfQKdJvQzV1+Bt8OokmrdtY2yhVX2a+qrykJfMq4Ml3VR4cVzTQVz+UoNne4vcKLoyS+gyKO6EHe+75Fdt0Mbe5bRIf/wjvrVmhbqBN97RD1vxrahvBOfOYzoosH9bq94uejSOQGkVM6sN/7HelL4t10t9F4gPdVzydEOx83Gv+uNxo7XyL/FtFl8z9ZAHF4bBsrEwAAA1xJREFUeAHt3cFNQ1EQA8B8RP8tA6KGOLK8A3fnrT3KNc/r5+/fnwbe3MDXm/PEaeC/AbBAiDQAVqRWoWAxEGkArEitQsFiINIAWJFahYLFQKQBsCK1CgWLgUgDYEVqFQoWA5EGwIrUKhQsBiINgBWpVShYDEQaACtSq1CwGIg0AFakVqFgMRBpAKxIrULBYiDSAFiRWoWCxUCkAbAitQoFi4FIA2BFahUKFgORBsCK1CoULAYiDYAVqVUoWAxEGgArUqtQsBiINABWpFahYDEQaQCsSK1CwWIg0gBYkVqFgsVApAGwIrUKBYuBSANgRWoVChYDkQbAitQqFCwGIg2AFalVKFgMRBr4jqR+OHTltzyf1/Ph5nIf5xsr1+3pZLBOz587Hqxct6eTwTo9f+54sHLdnk4G6/T8uePBynV7Ohms0/Pnjgcr1+3pZLBOz587Hqxct6eTwTo9f+54sHLdnk4G6/T8uePBynV7Ohms0/Pnjgcr1+3pZLBOz587Hqxct6eTwTo9f+54sHLdnk4G6/T8uePBynV7Ohms0/Pnjgcr1+3pZLBOz587Hqxct6eTwTo9f+54sHLdnk4G6/T8uePBynV7Ohms0/Pnjgcr1+3pZLBOz587Hqxct6eTwTo9f+54sHLdnk4G6/T8uePBynV7Ohms0/Pnjgcr1+3pZLBOz587Hqxct6eTwTo9f+54sHLdnk4G6/T8uePBynV7Ohms0/Pnjgcr1+3p5Oe18vOkp2fsO943Vt8mEy8Ca2LGviPA6ttk4kVgTczYdwRYfZtMvAisiRn7jgCrb5OJF4E1MWPfEWD1bTLxIrAmZuw7Aqy+TSZeBNbEjH1HgNW3ycSLwJqYse8IsPo2mXgRWBMz9h0BVt8mEy8Ca2LGviPA6ttk4kVgTczYdwRYfZtMvAisiRn7jgCrb5OJF4E1MWPfEWD1bTLxIrAmZuw7Aqy+TSZeBNbEjH1HgNW3ycSLwJqYse8IsPo2mXgRWBMz9h0BVt8mEy8Ca2LGviPA6ttk4kVgTczYdwRYfZtMvAisiRn7jgCrb5OJF4E1MWPfEWD1bTLxIrAmZuw7Aqy+TSZeBNbEjH1HgNW3ycSLwJqYse8IsPo2mXgRWBMz9h0BVt8mEy8Ca2LGviN+ASqtBynn2UvuAAAAAElFTkSuQmCC)

Each scanline in  `small.bmp`  thus takes up (3 pixels) × (3 bytes per pixel) = 9 bytes, which is  **not**  a multiple of 4. And so the scanline is "padded" with as many zeroes as it takes to extend the scanline’s length to a multiple of 4. In other words, between 0 and 3 bytes of padding are needed for each scanline in a 24-bit BMP.  In the case of  `small.bmp`, 3 bytes' worth of zeroes are needed, since (3 pixels) × (3 bytes per pixel) + (3 bytes of padding) = 12 bytes, which is indeed a multiple of 4.

To "see" this padding, right- or control-click  **small.bmp**  in CS50 IDE’s file browser and select  **Open as hexadecimal**. In the tab that appears, change  **Start with byte**  to  **54**, change  **Bytes per row**  to  **12**, and change  **Bytes per column**  to  **3**. Then click  **Set**. You should see output like the below; we’ve highlighted in green all instances of  `00ff00`.

```
00ff00 00ff00 00ff00 000000
00ff00 ffffff 00ff00 000000
00ff00 00ff00 00ff00 000000
```

For contrast, let’s next look at  `large.bmp`, which looks identical to  `small.bmp`  but, at 12 pixels by 12 pixels, is four times as large. Right- or control-click it in CS50 IDE’s file browser, then select  **Open as hexadecimal**. You should see output like the below; we’ve again highlighted in green all instances of  `00ff00`.

```
00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00
00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00
00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00
00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00
00ff00 00ff00 00ff00 00ff00 ffffff ffffff ffffff ffffff 00ff00 00ff00 00ff00 00ff00
00ff00 00ff00 00ff00 00ff00 ffffff ffffff ffffff ffffff 00ff00 00ff00 00ff00 00ff00
00ff00 00ff00 00ff00 00ff00 ffffff ffffff ffffff ffffff 00ff00 00ff00 00ff00 00ff00
00ff00 00ff00 00ff00 00ff00 ffffff ffffff ffffff ffffff 00ff00 00ff00 00ff00 00ff00
00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00
00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00
00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00
00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00 00ff00
```

Worthy of note is that this BMP lacks padding! After all, (12 pixels) × (3 bytes per pixel) = 36 bytes is indeed a multiple of 4.