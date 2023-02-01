import random


def get_the_number():
    number = 0

    while True:
        try:
            number = int(input("How many pencils would you like to use: "))
        except ValueError:
            print("The number of pencils should be numeric.")
            continue

        if number == 0:
            print("The number of pencils should be positive")
            continue

        elif number <= 0:
            print("The number of pencils should be numeric (\"minus sign is not numeric\"")

        else:
            break
    return number


def get_the_name():
    list_of_names = ["Jack", "John"]
    name = input("Who will be the first (John, Jack): ")
    while name not in list_of_names:
        print("Choose between *John* and *Jack*")
        name = input("Who will be the first (John, Jack): ")

    return name


def bot(number):
    if number == 1:
        turn = 1
    elif (number - 1) % 4 != 0:
        pattern = (number - 1) // 4

        turn = number - (pattern * 4 + 1)
    else:
        turn = random.randint(1, 3)

    print(f'Jack\'s turn:')
    print(f'{turn}')

    return turn


def game(number, name):
    print(number * "|")

    while number > 0:

        if name == "Jack":
            turn = bot(number)
        else:
            try:
                turn = int(input(f"{name}'s turn (you can go 1,2 or 3): "))
            except ValueError:
                print("Possible values: '1', '2', '3'")
                continue

            if turn not in [1, 2, 3]:
                print("Possible values: '1', '2' or '3'")
                continue
            elif turn > number:
                print("Too many pencils were taken")
                continue

        number = number - turn

        if name == "John":
            name = "Jack"
        else:
            name = "John"

        if number == 0:
            print(f'{name} won!')
        else:
            print(number * "|")


number_of_pens = get_the_number()
players_name = get_the_name()

game(number_of_pens, players_name)
