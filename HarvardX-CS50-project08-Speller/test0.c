#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "dictionary.h"

// number of buckets in hashtable
#define N 26

typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

void insert_new_node(node **head, char new_word[]);
void display_linked_list(node *head);
void insert_into_table(node **hashtable[], char new_word[]);
void display_table(node *hashtable);

int main(void)
{
    node *head = malloc(sizeof(node));
    insert_new_node(&head,"angel");
    insert_new_node(&head,"tossev");
    insert_new_node(&head,"storytel");

    display_linked_list(head);

    node *hashtable[N];

    insert_into_table(hashtable, "angel");
    insert_into_table(hashtable, "tossev");
    insert_into_table(hashtable, "storytel");
    insert_into_table(hashtable, "srqda");
    insert_into_table(hashtable, "storytel");
    insert_into_table(hashtable, "angel");
    insert_into_table(hashtable, "komp");

    display_table(*hashtable);

    return 0;
}

unsigned int hash(const char *word)
{
    return tolower(word[0]) - 'a';
}

void insert_new_node(node **head, char new_word[])
{
    // Create a new item and set its value
    node *new_node = malloc(sizeof(node*));

    // Link the new item to point to the head of the list
    strcpy(new_node->word, new_word);
    new_node->next = *head;

    // Set the head of the list to be our new item
    *head = new_node;
}

void display_linked_list(node *head)
{
    node *current = head;

    while(current != NULL)
    {
        printf("%s\n", current->word);
        current = current->next;
    }
}

void insert_into_table(node** hashtable, char new_word[])
{
    // get location
    int location = hash(new_word);

    // check if head exists in that location
    // if it is NULL create head
    if (hashtable[location] == NULL)
    {
        // create head
        // allocate the space required for the head
        hashtable[location] = malloc(sizeof(node*));

        // make variable for the head
        node* head = NULL;

        insert_new_node(&head, new_word);

        // set the hashtable location to point to the head
        hashtable[location] = head;
    }
    // if the head was allready there
    else
    {
        node* head = hashtable[location];

        insert_new_node(&head, new_word);

        // set the hashtable location to point to the head
        hashtable[location] = head;
    }
}

void display_table(node *hashtable)
{
    for (int i = 0; i < N; i++)
    {
        node *head = &hashtable[i];
        printf("%d: ", i);

        if(head == NULL)
        {
            printf("NULL");
        }
        else
        {
            node *current = head;

            while (current != NULL)
            {
                printf("%s ", current->word);
                current = current->next;
            }
        }
        printf("\n");
    }
}