def main():
    change_owed = 0

    # validate input
    while True:
        change_owed = input("Change owed: ")
        if is_float(change_owed):
            change_owed = float(change_owed)
            if change_owed > 0:
                break

    # init variables
    cents = round(change_owed * 100)
    coin = (25, 10, 5, 1)

    print(count(cents, coin))

# functions definitions


def count(cents, coin):
    current_coin = 0
    total_coins = 0
    reminder = 0

    while current_coin < len(coin):

        reminder = cents % coin[current_coin]

        if reminder >= 0:
            cents -= reminder
            total_coins += (cents // coin[current_coin])
            cents = reminder
        current_coin += 1

    return total_coins


def is_float(num):
    try:
        num = float(num)
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    main()