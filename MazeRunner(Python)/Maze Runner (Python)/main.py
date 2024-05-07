import json
import sys
import random
from queue import Queue
import numpy as np


class Maze:
    def __init__(self, recursion_limit: int = 1000):
        self.menu_options = None
        self.width = None
        self.height = None
        self.maze = dict()

        sys.setrecursionlimit(recursion_limit)

    def _generate_maze(self) -> None:
        self._init_maze()
        random.seed()
        self.maze[1][1] = 0
        try:
            self._carve_maze(1, 1)
        except RecursionError:
            print("Set bigger Maze(recursion_limit=3000) parameter")
            raise
        self.maze[1][0] = 0
        self.maze[self.width - 2][self.height - 1] = 0

    def _init_maze(self) -> None:
        for i in range(0, self.width):
            self.maze[i] = dict()
            for y in range(0, self.height):
                self.maze[i][y] = 1

    def _carve_maze(self, x: int, y: int) -> None:
        direction = random.randint(0, 3)
        step_count = 0
        while step_count < 4:
            dx = 0
            dy = 0
            if direction == 0:
                dx = 1
            elif direction == 1:
                dy = 1
            elif direction == 2:
                dx = -1
            else:
                dy = -1

            x1 = x + dx
            y1 = y + dy
            x2 = x1 + dx
            y2 = y1 + dy
            if 0 < x2 < self.width and 0 < y2 < self.height:
                if self.maze[x1][y1] == 1 and self.maze[x2][y2] == 1:
                    self.maze[x1][y1] = 0
                    self.maze[x2][y2] = 0
                    self._carve_maze(x2, y2)
            step_count += 1
            direction = (direction + 1) % 4

    def create_maze(
            self, wall_str: str = '\u2588\u2588'
    ) -> None:
        self._generate_maze()

        for y in range(self.height - 1, -1, -1):
            for x in range(self.width - 1, -1, -1):
                if self.maze[x][y] == 0:
                    sys.stdout.write("  ")
                elif self.maze[x][y] == 1:
                    sys.stdout.write(wall_str)
                else:
                    sys.stdout.write(self.maze[x][y])
            sys.stdout.write("\n")

    def print_menu_list(self):
        self.menu_options = {1: 'Generate a new maze', 2: 'Load a maze', 3: 'Save the maze', 4: 'Display  the maze',
                             5: 'Find the escape', 0: 'Exit'}
        print('=== Menu ===')
        for key, val in self.menu_options.items():
            if not self.maze and key in [3, 4, 5]:
                continue
            print(f'{key} - {val}')

        option = int(input())

        return option

    def find_path(self):
        # BFS algorithm to find the shortest path
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        start = (0, 0)
        end = (self.width - 2, self.height - 1)
        visited = np.zeros((self.width, self.height), dtype=bool)
        visited[start[0]][start[1]] = True
        queue = Queue()
        queue.put((start, []))
        while not queue.empty():
            (node, path) = queue.get()
            for dx, dy in directions:
                next_node = (node[0] + dx, node[1] + dy)
                if next_node == end:
                    return path + [next_node]
                if (0 <= next_node[0] < self.width and 0 <= next_node[1] < self.height and
                        self.maze[next_node[0]][next_node[1]] == 0 and not visited[next_node[0]][next_node[1]]):
                    visited[next_node[0]][next_node[1]] = True
                    queue.put((next_node, path + [next_node]))

        return None

    def draw_path(self, path=None, wall_str: str = '\u2588\u2588'):
        if path is not None:
            for key, val in path:
                self.maze[key][val] = 2

            for y in range(self.height - 1, -1, -1):
                for x in range(self.width - 1, -1, -1):
                    if self.maze[x][y] == 0:
                        sys.stdout.write("  ")
                    elif self.maze[x][y] == 1:
                        sys.stdout.write(wall_str)
                    elif self.maze[x][y] == 2:
                        sys.stdout.write(r'//')
                    else:
                        sys.stdout.write(self.maze[x][y])
                sys.stdout.write("\n")

        else:
            print('Something went wrong')

    def menu(self) -> None:
        end = False
        while not end:
            option = self.print_menu_list()
            if option not in self.menu_options.keys():
                print('Incorrect option. Please try again.\n')
                continue

            if option == 1:
                size = int(input('Enter the size of a new maze\n'))
                self.width = size
                self.height = size

                # # Width and height must be odd numbers.
                self.width = self.width + 1 if self.width % 2 == 0 else self.width
                self.height = self.height + 1 if self.height % 2 == 0 else self.height

                # Generate new maze
                self.create_maze()

            elif option == 2:
                filename = input('Enter the filename with .json\n')
                try:
                    with open(filename, 'r') as json_file:
                        self.maze = json.load(json_file)
                    if self.width is None:
                        self.width = len(self.maze.keys())
                        self.height = len(self.maze['0'].keys())

                except FileExistsError:
                    print(f'The file {filename} does not exist')
                except FileNotFoundError:
                    print(f'The file {filename} does not exist')
                except json.JSONDecodeError:
                    print("Cannot load the maze. It has an invalid format")

            elif option == 3:
                filename = input('Enter the filename with .json\n')
                try:
                    with open(filename, 'w') as json_file:
                        json.dump(self.maze, json_file)
                except json.JSONDecodeError:
                    print("Cannot read the maze. It has an invalid format")
                except FileNotFoundError:
                    print(f'The file {filename} does not exist')

            elif option == 4:
                self.create_maze()

            elif option == 5:
                found_path = self.find_path()

                if found_path:
                    print("Path found!")
                    self.draw_path(found_path)
                else:
                    print("No path found from start to end.")

            elif option == 0:
                print("Bye!")
                end = True


if __name__ == "__main__":
    maze = Maze()
    maze.menu()
