#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>

int printError(void);
char* cipher(string plaintext, int key);
char cipherAlgorithm(char c, int key, int shift);

int main(int argc, char* argv[])
{
    //asign argument to varialble and convert to int
    //validate input
   if(argc == 2)
   {
       //check if digit
       for(int i = 0; i < strlen(argv[1]); i++)
       {
           if(!isdigit(argv[1][i]))
           {
              printf("Usage: ./caesar key\n");
              return 1;
           }
       }

       //get input
       int key = atoi(argv[1]);
       char* plaintext = get_string("plaintext: ");
       char* ciphertext = cipher(plaintext, key);

       printf("ciphertext: %s\n",ciphertext);
       return 0;
   }
   else
   {
       printf("Usage: ./caesar key\n");
       return 1;
   }


}
char cipherAlgorithm(char c, int key, int shift)
{
    return (c - shift + key) % 26 + shift;
}
char* cipher(string plaintext, int key)
{
    int upperCaseShift = 65;
    int lowerCaseShift = 97;
    for(int i = 0; i < strlen(plaintext); i ++)
       {

           if(isalpha(plaintext[i]))
           {
              if(isupper(plaintext[i]))
              {
                   plaintext[i] = cipherAlgorithm(plaintext[i], key, upperCaseShift);

              }
               else
               {
                  plaintext[i] = cipherAlgorithm(plaintext[i], key, lowerCaseShift);
               }
           }
       }

    return plaintext;
}

