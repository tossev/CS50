
from sys import argv


def main():

    # TODO
    file_name = ""
    max_arguments = 2

    if len(argv) is not max_arguments:
        print("Usage: python bleep.py dictionary")
        exit(1)
    else:
        file_name = argv[1]

    message = input("What message would you like to censor?\n").split()

    dict_file = open(file_name, 'r')
    dictionary = set(remove_newlines(dict_file))
    dict_file.close()
    output = ''

    for word in message:
        check = word.lower()
        if check in dictionary:
            output += '*' * len(word) + ' '
        else:
            output += word + ' '

    print(output.strip())


def remove_newlines(dict_file):
    flist = dict_file.readlines()
    return [s.rstrip('\n') for s in flist]


if __name__ == "__main__":
    main()