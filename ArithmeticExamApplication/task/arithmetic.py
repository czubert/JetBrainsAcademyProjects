import random
import time


def time_convert(x):
    if x > 60:
        x1 = x // 60
        x2 = x % 60
        return f'{round(x1)} min and {round(x2)} sec'
    else:
        return f'{round(x)} sec'


def print_results():
    try:
        result_file = open('results.txt', 'r')
        for line in result_file:
            print(line[:-1])
    except FileNotFoundError:
        print('No saved results.')


def answer():
    while True:
        t1 = time.time()
        answer_input = input()
        t2 = time.time()
        try:
            answer_int = int(answer_input)
            break
        except ValueError:
            print('Wrong format! Try again.')
    return answer_int, t2 - t1


def level():
    levels = ['1', '2']
    while True:
        check_level = input('''Which level do you want? Enter a number:
1 - simple operations with numbers 2-9
2 - integral squares of 11-29
''')
        if levels.count(check_level):
            return int(check_level)
        else:
            print('Incorrect format.')
            continue


def n_tasks():
    while True:
        n_input = input('How many tasks do you want to solve?\n(Input intiger or "random")\n')
        if n_input == 'random':
            n_random = random.randint(1, 10)
            return n_random
        else:
            try:
                n_int = int(n_input)
                break
            except ValueError:
                print('You must enter an integer or "random"!')
    return n_int


def check_correct(user_answer, real_result, n_correct):
    if user_answer == real_result:
        print('Right!')
        n_correct += 1
    else:
        print('Wrong!')
    return n_correct


def first_level():
    message = '1 - simple operations with numbers 2-9'
    opers = '+-*'
    oper = random.choice(opers)
    x = random.randint(2, 9)
    y = random.randint(2, 9)
    if oper == '+':
        task_result = x + y
    elif oper == '-':
        task_result = x - y
    else:
        task_result = x * y
    print(x, oper, y)
    return task_result, message


def second_level():
    message = '2 - integral squares of 11-29'
    x = random.randint(11, 29)
    task_result = x ** 2
    print(x)
    return task_result, message


print_results()
lev = level()
# n = n_tasks()
n = 5
correct = 0
answer_time = 0

for i in range(n):
    if lev == 1:
        result, msg = first_level()
    elif lev == 2:
        result, msg = second_level()
    ans, t = answer()
    answer_time += t
    correct = check_correct(ans, result, correct)

solve_time = time_convert(answer_time)

print(
    f'You mark is {correct}/{n} in {solve_time}. Your effectiveness is {round(correct / n * 100)}%. Would you like to '
    f'save the result? Enter yes or no.')
save = input()
if save == 'YES' or save == 'Yes' or save == 'yes' or save == 'y':
    name = input('What is your name?\n')
    file = open('results.txt', 'a+')
    file.write(
        f'{name}: {correct}/{n} in level {msg} in {solve_time}. Your effectiveness is {round(correct / n * 100)}%.\n')
    file.close()
    print('The results are saved in "results.txt".')