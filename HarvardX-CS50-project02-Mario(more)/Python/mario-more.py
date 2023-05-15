def main():
    height = 0
    symbol = '#'
    offset_symbol = ' '
    separator = "  "

# validate input
    while True:
        height = input("Height: ")

        if height.isdigit():
            height = int(height)

            if height > 0 and height < 9:
                break

    # print pyramid
    for i in range(height):
        for j in range(height - 1, i, -1):
            print(f"{offset_symbol}", end="")

        print_symbol(symbol, i)
        print(f"{separator}", end="")
        print_symbol(symbol, i)
        print()

# functions declarations
def print_symbol(symbol, right_margin):
    for i in range(right_margin + 1):
        print(f"{symbol}", end="")

if __name__ == "__main__":
    main()
