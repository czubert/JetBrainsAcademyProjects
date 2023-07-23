# write your code here
path = input()

with open(path, 'r') as f:
    out = f.readlines()
    for i, el in enumerate(out):
        if i < 4:
            print(el[:-1])