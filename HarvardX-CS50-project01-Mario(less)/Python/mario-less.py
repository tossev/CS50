height = 0
symbol = '#'
offset_symbol = ' '

while True:
    height = input("Height: ")

    if height.isdigit():
        height = int(height)

        if height > 0 and height < 9:
            break

for i in range(height):
    for m in range(height-1, i, -1):
        print(f"{offset_symbol}", end="")
    for k in range(i + 1):
        print(f"{symbol}", end="")
    print()