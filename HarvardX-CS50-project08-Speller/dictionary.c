// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include "dictionary.h"

// Represents number of buckets in a hash table
#define N 26

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Represents a hash table
node *hashtable[N];

// Represents dictionary size
int dictionary_size = 0;

// Hashes word to a number between 0 and 25, inclusive, based on its first letter
unsigned int hash(const char *word)
{
    return tolower(word[0]) - 'a';
}

// converts string to lowercase
char* to_lower(char* word)
{
    char *tmp = malloc(LENGTH + 1);
    strcpy(tmp, word);

    for(int i = 0; tmp[i] != '\0'; i++)
    {
        if (tmp[i] >= 'A' && tmp[i] <= 'Z')
        {
            tmp[i] += 32;
        }
    }

    return tmp;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialize hash table
    for (int i = 0; i < N; i++)
    {
        hashtable[i] = NULL;
    }

    // Open dictionary
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        unload();
        return false;
    }

    // Buffer for a word
    char word[LENGTH + 1];

    // Insert words into hash table
    while (fscanf(file, "%s", word) != EOF)
    {
        // TODO

        // increment dictionary size
        dictionary_size++;

        // allocate memory for new word
        node *new_word = malloc(sizeof(node));

        // put word in the new node
        strcpy(new_word->word, word);

        // find what index of the array the word should go in
        int location = hash(word);

        // if hashtable is empty at current location - create the head
        if (hashtable[location] == NULL)
        {
            hashtable[location] = new_word;
            new_word-> next = NULL;
        }
        // else - make current node head
        else
        {
            new_word->next = hashtable[location];
            hashtable[location] = new_word;
        }
    }

    // Close dictionary
    fclose(file);

    // Indicate success
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return dictionary_size;
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // TODO

    // create temp string to store and modify input
    char tmp[LENGTH + 1];
    int len = strlen(word);

    // make temp lowercase
    for(int i = 0; i < len; i ++)
    {
        tmp[i] = tolower(word[i]);
    }
    // add "end of string" char
    tmp[len] = '\0' ;

    // get locatio for the node
    int location = hash(tmp);

    //create cursor
    node* cursor = hashtable[location];

    // if hashtable is empty at that location return false
    if(cursor == NULL)
        return false;

    // if hashtable is not empty at index iterate over words and compare
    while (cursor != NULL)
    {
        if (strcmp(tmp, cursor->word) == 0)
        {
            return true;
        }
        // update cursor
        cursor = cursor->next;
    }

    // if word is not found return false
    return false;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // TODO
    // iterate over hashtable
    for (int i = 0; i < N; i++)
    {
        // create node for the current element
        node *current = hashtable[i];

        // till the end if linked-list
        while (current != NULL)
        {
            // create temp node ans swap values
            node *tmp = current;
            // update current elemet
            current = current->next;
            // free memory
            free(tmp);
        }
    }

    return true;
}
