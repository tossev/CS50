# Questions

## What's `stdint.h`?

**stdint.h** is a header file in the[ C standard library](https://en.wikibooks.org/wiki/C_Programming/Standard_libraries) introduced in the [C99 standard library](https://en.wikibooks.org/wiki/C_Programming/Standard_library_reference) section 7.18 to allow programmers to write more portable code by providing a set of typedefs that specify exact-width integer types, together with the defined minimum and maximum allowable values for each type, using macros. This header is particularly useful for embedded programming which often involves considerable manipulation of hardware specific I/O registers requiring integer data of fixed widths, specific locations and exact alignments.

## What's the point of using `uint8_t`, `uint32_t`, `int32_t`, and `uint16_t` in a program?

We use them for type declarations. The ``_t`` stands for ``typedef``.
C type | stdint.h type | Bits | Sign | Range
------ | ------------- | ---- | ---- | -----
char | uint8_t | 8 | Unsigned | 0..255
unsigned int | uint32_t | 32 | Unsigned | 0..4,294,967,295
int | int32_t | 32 | Signed | -2,147,483,648..2,147,483,647
unsigned short | uint16_t | 16 | Unsigned | 0..65,535

## How many bytes is a `BYTE`, a `DWORD`, a `LONG`, and a `WORD`, respectively?

TYPE | SIZE in bytes
---- | -------------
BYTE | 1
DWORD | 4
LONG | 4
WORD | 2

## What (in ASCII, decimal, or hexadecimal) must the first two bytes of any BMP file be? Leading bytes used to identify file formats (with high probability) are generally called "magic numbers."

``bfType`` (the file type) must be ``0x4d42`` ("BM").

## What's the difference between `bfSize` and `biSize`?

bfSize | biSize
------ | ------
The size, in bytes, of the bitmap file | The number of bytes required by the structure

## What does it mean if `biHeight` is negative?

If ``biHeight`` is negative , the bitmap is top-down DIP, and it origin is the top-left corner.

## What field in `BITMAPINFOHEADER` specifies the BMP's color depth (i.e., bits per pixel)?

``biBitCount`` specifies the BMP's color depth.

## Why might `fopen` return `NULL` in `copy.c`?

In ``copy.c`` ``fopen()`` might return ``NULL`` because the file could not be created or opened.

## Why is the third argument to `fread` always `1` in our code?

Because this is the number of elements whit size of ``size`` bytes, we want to read.

## What value does `copy.c` assign to `padding` if `bi.biWidth` is `3`?

3

## What does `fseek` do?

`fseek()` sets the file position of the **stream** to the given **offset**.

## What is `SEEK_CUR`?

`SEEK_CUR` is the current position of the file p0inter.
