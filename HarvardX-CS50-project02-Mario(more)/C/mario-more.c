#include <cs50.h>
#include <stdio.h>

void print_symbol(char symbol, int right_margin);
int main(void)
{
    int height;
    char symbol = '#';
    char offset_symbol = ' ';
    string separator = "  ";
    
    do
    {
        height = get_int("Height: ");
    }
    while(height < 1 || height > 8);
    
     for(int i = 0; i < height; i++)
    {
        for(int m = height - 1; m > i; m--)
        {
            printf("%c", offset_symbol);
        }
        print_symbol(symbol, i);
         
        printf("%s", separator);
         
        print_symbol(symbol, i);
         
        printf("\n");
        
    }
    
   
    
}

void print_symbol(char symbol, int right_margin)
{
    for(int k = 0; k < (right_margin+1); k++)
        {
            printf("%c", symbol);
        }
}
