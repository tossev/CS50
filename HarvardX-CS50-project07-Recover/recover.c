#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef unsigned char BYTE;

int is_jpeg_start(BYTE buffer[]);

int main(int argc, char *argv[])
{
    // check command-line arguments
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover file.raw\n");
        return 1;
    }

    // remember filename
    char *infile = argv[1];

    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s\n", infile);
        return 2;
    }

    // define block size
    int block_size = 512;

    // initialize buffer
    BYTE buffer[block_size];

    // init name counter
    int name_counter = 0;

    // set flag
    int flag = 0;

    // set array to store img name
    char img_name[20];

    // create outfile for the jpeg
    FILE *img = NULL;


    // repeat until the end of the card
    while (fread(&buffer, block_size, 1, inptr) == 1)
    {
        // if we are at the beginnig of jpeg
        if (is_jpeg_start(buffer))
        {
            // we close current img to read new
            if (flag == 1)
            {
                fclose(img);
            }
            // we found JPEG
            else
            {
                flag = 1;
            }

            // make JPEG
            sprintf(img_name, "%03i.jpg", name_counter);
            img = fopen(img_name, "w");
            name_counter++;
        }

        // if it is jpeg
        if (flag == 1)
        {
            fwrite(buffer, block_size, 1, img);

        }

    }

    // close all files
    fclose(inptr);
    fclose(img);

    // on success
    return 0;
}

int is_jpeg_start(BYTE buffer[])
{
    // check if it is a start of JPEG
    if (buffer[0] == 0xff &&
        buffer[1] == 0xd8 &&
        buffer[2] == 0xff &&
        (buffer[3] & 0xf0) == 0xe0)
    {
        return 1;
    }
    return 0;
}

