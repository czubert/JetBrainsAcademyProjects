def calculate(numbers, dct):
    numbers = '**'.join(numbers.split('^'))
    nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    try:
        print(eval(numbers))
    except SyntaxError:
        numbers = numbers.split('=')
        variable = numbers[0].strip(' ')
        expression = numbers[1].strip(' ')
        for num in nums:
            if num in variable:
                print('Invalid identifier')
                return
        if expression in dct.keys():
            dct[variable] = dct[expression]
        else:
            try:
                dct[variable] = int(expression)
            except ValueError:
                print('Invalid assignment')
    except NameError:
        if numbers in dct.keys():
            print(dct[numbers])
        else:
            numbers = numbers.split()
            for n in range(len(numbers)):
                if numbers[n] in dct.keys():
                    numbers[n] = dct[numbers[n]]
            numbers = list(map(str, numbers))
            try:
                result = eval(''.join(numbers))
                if isinstance(result, float) and result.is_integer():
                    print(int(result))
                else:
                    print(result)
            except NameError:
                print('Unknown variable')


def check_symbols(numbers):
    parentheses = 0
    for n in numbers:
        if n == '(':
            parentheses += 1
        elif n == ')':
            parentheses -= 1

    other = 0
    for n in range(len(numbers) - 1):
        x = numbers[n: n + 2]
        if x == '**':
            other += 1
        elif x == '//':
            other += 1
        elif x == '^^':
            other += 1

    if parentheses == 0 and other == 0:
        return True
    else:
        return False


def main():
    dct = {}
    while True:
        numbers = input()
        if numbers == '/exit':
            print("Bye!")
            break
        elif numbers == '/help':
            print('''The calculator is used to calculate expression. It supports writing values to variables and operators:
    + addition; 
    - subtraction; 
    () parentheses 
    * multiplication; 
    / division; 
    ^ multiplication''')
            continue
        elif not numbers:
            continue
        elif numbers[0] == '/':
            print('Unknown command')
            continue

        if not check_symbols(numbers):
            print('Invalid expression')
            continue

        calculate(numbers, dct)


if __name__ == '__main__':
    main()
