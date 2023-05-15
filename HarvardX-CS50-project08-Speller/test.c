#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

// Represents number of buckets in a hash table
#define N 26

typedef struct node{
    char word[100];
    struct node* next;
}
node;

void insert_new_node(node** head, char new_value[]);
node** get_hashtable();
void insert_into_table(node** hashtable, char new_word[]);
void display_table(node** hashtable);
unsigned int hash(const char *word);

int main()
{
    node** table = get_hashtable();

    insert_into_table(table, "angel");
    insert_into_table(table, "tossev");
    insert_into_table(table, "storytel");
    insert_into_table(table, "tuesday");
    insert_into_table(table, "weekday");
    insert_into_table(table, "cs50");

    insert_into_table(table, "angel");
    insert_into_table(table, "tossev");
    insert_into_table(table, "storytell");
    insert_into_table(table, "tuesdayy");
    insert_into_table(table, "weekday");
    insert_into_table(table, "cs500");

    display_table(table);


    return 0;
}
unsigned int hash(const char *word)
{
    return tolower(word[0]) - 'a';
}

// create/insert new node
void insert_new_node(node** head, char new_word[])
{
    // allocate space
    node* new_node = malloc(sizeof(node*));
    // asign value
    strcpy(new_node->word, new_word);
    // assign the address to the next node
    new_node->next = NULL;

    // check if head exists (is NULL)
    if (*head == NULL)
    {
        // then new_node is head
        *head = new_node;
    }
    // if head allready eists
    else
    {
        node* current = *head;

        // find the tail
        while (current->next != NULL)
        {
            current = current->next;
        }

        // when we find the end we put new_node at the end
        current->next = new_node;
    }
}

node** get_hashtable()
{
    node** hashtable = calloc(N, sizeof(node*));
    return hashtable;
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

void display_table(node* hashtable)
{
    for (int i = 0; i < N; i++)
    {
        node *head = &hashtable[i];

        printf("%d: ", i);

        if (head == NULL)
        {
            printf("NULL");
        }
        else
        {
            node *current = head;

            while(current != NULL)
            {
                printf("%s ", current->word);
                current = current->next;
            }
        }
        printf("\n");
    }
}