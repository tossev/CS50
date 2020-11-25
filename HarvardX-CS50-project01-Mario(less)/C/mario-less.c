#include <cs50.h>
#include <stdio.h>

int main(void)
{
    int height;
    char symbol = '#';
    char offset_symbol = ' ';
    
    do
    {
        height = get_int("Height: ");
    }
    while(height < 1 || height > 8);
    
    
    for(int i = 0; i < height; i++)
    {
        for(int m = height-1; m > i; m--)
        {
            printf("%c", offset_symbol);
        }
        for(int k = 0; k <(i+1); k++)
        {
           
            printf("%c",symbol);
        }
        printf("\n");
    }
    
    
    
}
