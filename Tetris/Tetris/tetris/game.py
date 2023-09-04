import numpy as np
import random


class Tetris:
    map = np.array([])
    figures = {'O': [[4, 14, 15, 5]],
               'I': [[4, 14, 24, 34], [3, 4, 5, 6]],
               'S': [[5, 4, 14, 13], [4, 14, 15, 25]],
               'Z': [[4, 5, 15, 16], [5, 15, 14, 24]],
               'L': [[4, 14, 24, 25], [5, 15, 14, 13], [4, 5, 15, 25], [6, 5, 4, 14]],
               'J': [[5, 15, 25, 24], [15, 5, 4, 3], [5, 4, 14, 24], [4, 14, 15, 16]],
               'T': [[4, 14, 24, 15], [4, 13, 14, 15], [5, 15, 25, 14], [4, 5, 6, 15]]}
    arr = None
    block = None
    size_x = None
    size_y = None
    figure = None
    position = None

    def __init__(self):
        self.ground = None

    def game(self):
        # self.size_x, self.size_y = 10, 20
        self.size_x, self.size_y = [int(x) for x in input().split()]
        print('\n' + self.size_y * ((self.size_x - 1) * '- ' + '-' + '\n'))
        self.ground = True

        while True:

            user_input = input('\n')
            if user_input == 'exit':
                return

            elif user_input == 'piece':
                # self.figure = random.choice(list(self.figures.keys()))
                self.figure = input().upper()
                self.figure = self.figures[self.figure]
                self.arr = np.array(self.figure)
                self.position = 0
                self.block = self.arr[self.position]
                self.ground = False
                self.print_map()
                continue

            elif user_input == 'break':
                self.check_line()

            if not self.ground:
                if user_input == 'rotate':
                    self.rotate()
                elif user_input == 'left':
                    self.move_block_left()
                elif user_input == 'right':
                    self.move_block_right()
                self.arr += self.size_x
                self.ground = self.check_hold_block()
            self.print_map()
            if self.check_game_over():
                return

    def print_map(self):
        n = 0
        for row in range(self.size_y):
            line = []
            for column in range(self.size_x):
                if n in self.block or n in self.map:
                    line.append('0')
                else:
                    line.append('-')
                n += 1
            print(' '.join(line))

    def move_block_left(self):
        check_left_side = self.block % self.size_x
        if check_left_side.min() > 0:
            self.arr -= 1

    def move_block_right(self):
        check_right_side = self.block % self.size_x + 1
        if check_right_side.max() < self.size_x:
            self.arr += 1

    def rotate(self):
        check_left1 = self.block % self.size_x
        check_right1 = self.block % self.size_x + 1
        self.position = (self.position + 1) % len(self.figure)
        self.block = self.arr[self.position]
        check_left2 = self.block % self.size_x
        check_right2 = self.block % self.size_x + 1
        check_under_map = self.block // self.size_y
        if check_left1.min() == 0 and check_right2.max() == self.size_x:
            self.arr += 1
        elif check_right1.max() == self.size_x and check_left2.min() == 0:
            self.arr -= 1
        elif check_under_map.max() > self.size_y:
            self.arr -= 10

    def check_hold_block(self):
        check_next_block = False
        for element in self.block:
            if element in self.map:
                self.block -= self.size_x
                check_next_block = True
            elif element + 10 in self.map:
                check_next_block = True
        if self.size_x * (self.size_y - 1) - 1 < self.block.max() < self.size_x * self.size_y or check_next_block:
            self.map = np.append(self.map, self.block)
            return True
        return False

    def check_line(self):
        lines = [[] for _ in range(self.size_y)]
        n = -1
        full_line = False
        for el in sorted(self.map):
            m = int(el % self.size_x)
            if m == 0:
                n += 1
            lines[n].append(el)
        for n, line in enumerate(lines):
            if len(line) == self.size_x:
                full_line = True
                for number in line:
                    self.map = np.delete(self.map, np.where(self.map == number))
        if full_line:
            self.map += self.size_x
            self.block = []

    def check_game_over(self):
        game_over = []
        n_rows = self.size_y
        check_go = self.map // self.size_x
        for n in range(n_rows):
            if n in check_go:
                game_over.append(n)
        if len(game_over) == n_rows:
            print('\nGame Over!')
            return True


if __name__ == '__main__':
    tetris = Tetris()
    tetris.game()
