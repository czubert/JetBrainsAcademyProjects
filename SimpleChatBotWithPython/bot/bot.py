def greet(bot_name, birth_year):
    print("Heed me, mortal, for I am " + bot_name + "!")
    print("I have existed since time immemorial, but I have last manifested in the mortal realm in year " + birth_year + ".")


def remind_name():
    print("What is your name, mortal?")
    name = input()
    print("Hah! " + name + " is a fitting name for a mortal.")


def guess_age():
    print("My wisdom is beyond comprehension. I can easily guess the age of one such as yourself.")
    print("Tell me, mortal, what are the remainders of dividing your age by 3, 5 and 7?")

    rem3 = int(input())
    rem5 = int(input())
    rem7 = int(input())
    age = (rem3 * 70 + rem5 * 21 + rem7 * 15) % 105

    print("Then you have lived for " + str(age) + " years, mortal. To me, a mere blink of an eye.")


def count():
    print("Pick a number, and I shall count to it faster than your mortal life slips through your fingers.")

    number = int(input())
    counter = 0
    while counter <= number:
        print(str(counter) + "!")
        counter += 1


def test():
    print("Enough of these games. The time has come for you to face the ultimate test.")

    # write your code here
    print("Answer me, mortal. How mighty am I? How powerful?")
    print("1. Not mighty at all.")
    print("2. Decently mighty.")
    print("3. Slightly mighty.")
    print("4. My might knows no bounds, my power is immeasurable.")

    answer = int(input())
    while answer != 4:
        print("Blasphemy! But I am merciful. You may try again.")
        answer = int(input())

    print("Yes. Do not ever forget this, mortal... But we must stop here. "
          "And as we part ways, the Ancient Pledge compels me to say this out-of-character phrase:")


def end():
    print("Congratulations, have a nice day!")


greet("Thunderbane the Dreadful, Destroyer of Worlds and Devourer of Souls", "2020")  # change it as you need
remind_name()
guess_age()
count()
test()
end()
