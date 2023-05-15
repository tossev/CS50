#include <stdio.h>
#include <cs50.h>
#include <math.h>

int cents;
int total_coins;

void count(int,int);

int main(void)
{
    float change_owed;
    do
    {
        change_owed = get_float("Change owed: ");
    }
    while(change_owed < 0.00);
    
    cents = round(change_owed*100);
    total_coins = 0;

    int quarters = 25;
    int dimes = 10;
    int nickles = 5;
    int pennies = 1;
    int remainder = 0;
    
    
    while(cents > 0)
    {
        while(cents >= quarters)
        {
            count(quarters, remainder);          
        } 
        while(cents >= dimes)
        {
            count(dimes, remainder); 
        }
        while(cents >= nickles)
        {
            count(nickles, remainder); 
        }
        while(cents >= pennies)
        {
            count(pennies, remainder); 
        }
    }
    printf("%i\n", total_coins);
}

void count(int value, int remainder)
{
    remainder =  cents / value;
    total_coins += remainder;
    cents -= value * remainder;
}

