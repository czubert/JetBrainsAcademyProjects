msg_0 = "Enter an equation"
msg_1 = "Do you even know what numbers are? Stay focused!"
msg_2 = "Yes ... an interesting math operation. You've slept through all classes, haven't you?"
msg_3 = "Yeah... division by zero. Smart move..."
msg_4 = "Do you want to store the result? (y / n):"
msg_5 = "Do you want to continue calculations? (y / n):"
msg_6 = " ... lazy"
msg_7 = " ... very lazy"
msg_8 = " ... very, very lazy"
msg_9 = "You are"
msg_10 = "Are you sure? It is only one digit! (y / n)"
msg_11 = "Don't be silly! It's just one number! Add to the memory? (y / n)"
msg_12 = "Last chance! Do you really want to embarrass yourself? (y / n)"

msgs = ["Enter an equation", "Do you even know what numbers are? Stay focused!",
        "Yes ... an interesting math operation. You've slept through all classes, haven't you?",
        "Yeah... division by zero. Smart move...",
        "Do you want to store the result? (y / n):",
        "Do you want to continue calculations? (y / n):",
        " ... lazy",
        " ... very lazy",
        " ... very, very lazy",
        "You are",
        "Are you sure? It is only one digit! (y / n)",
        "Don't be silly! It's just one number! Add to the memory? (y / n)",
        "Last chance! Do you really want to embarrass yourself? (y / n)"
        ]

opers = ["/", "*", "+", "-"]

finish = False

memory = 0


def check(v1, v2, v3):
    msg = ""

    if is_one_digit(v1) and is_one_digit(v2):
        msg += msgs[6]

    if (v1 == 1 or v2 == 1) and v3 == '*':
        msg += msgs[7]

    if (v1 == 0 or v2 == 0) and (v3 == '*' or v3 == '+' or v3 == '-'):
        msg += msgs[8]

    if msg != "":
        msg = msgs[9] + msg
        print(msg)


def is_one_digit(v):
    if -10 < v < 10 and float(v).is_integer():
        return True
    else:
        return False


def calc(x, oper, y):
    if oper == '+':
        return x + y
    elif oper == '-':
        return x - y
    elif oper == '*':
        return x * y
    else:
        try:
            return x / y
        except ZeroDivisionError:
            print(msgs[3])


def store_result():
    while True:
        print(msgs[4])
        store_answ = input()
        if store_answ == 'y':
            return store_answ
        elif store_answ == 'n':
            return store_answ
        else:
            continue


def storing_result(score):
    if is_one_digit(score):
        msg_index = 10

        while True:
            print(msgs[msg_index])
            store = input()

            if store == 'y':

                if msg_index < 12:
                    msg_index += 1
                    continue
                else:
                    return score

            elif store == 'n':
                break
            else:
                continue
    else:
        return score


def continue_calc():
    while True:
        print(msgs[5])
        continue_input = input()
        if continue_input == 'y':
            break
        if continue_input == 'n':
            break
        else:
            continue
    return continue_input


while not finish:
    print(msgs[0])
    x, oper, y = input().split()

    if x == "M":
        x = memory
    else:
        try:
            x = float(x)
        except:
            print(msgs[1])
            continue

    if y == "M":
        y = memory
    else:
        try:
            y = float(y)
        except:
            print(msgs[1])
            continue

    if oper not in opers:
        print(msgs[2])
        continue

    check(x, y, oper)

    result = calc(x, oper, y)

    if result is not None:
        print(result)
        answer = store_result()

        if answer == 'y':
            x = storing_result(result)
            if x:
                memory = x

        cont = continue_calc()

        if cont == 'y':
            continue
        elif cont == 'n':
            finish = True
