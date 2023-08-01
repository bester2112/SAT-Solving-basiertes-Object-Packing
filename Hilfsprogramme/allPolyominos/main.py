import random
import copy
import string


class Polyomino:
    def __init__(self, size, points=None, grid=None):
        self.size = size
        if points is None and grid is None:
            self.start_point = (random.randint(0, size - 1), random.randint(0, size - 1))
            self.grid = [['.' for _ in range(size)] for _ in range(size)]
            self.grid[self.start_point[0]][self.start_point[1]] = '#'
            self.points = [self.start_point]
        else:
            self.points = points
            self.grid = grid

    def neighbours(self):
        neighbours = set()
        for point in self.points:
            x, y = point
            directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.size and 0 <= ny < self.size and self.grid[nx][ny] == '.':
                    neighbours.add((nx, ny))
        return list(neighbours)

    def generate(self):
        while len(self.points) < self.size:
            ns = self.neighbours()
            if ns:
                n = random.choice(ns)
                self.grid[n[0]][n[1]] = '#'
                self.points.append(n)
        self.trim()

    def trim(self):
        min_x = min([point[0] for point in self.points])
        min_y = min([point[1] for point in self.points])
        self.points = [(x - min_x, y - min_y) for (x, y) in self.points]
        max_x = max([point[0] for point in self.points])
        max_y = max([point[1] for point in self.points])
        self.grid = [['.' for _ in range(max_y + 1)] for _ in range(max_x + 1)]
        for point in self.points:
            self.grid[point[0]][point[1]] = '#'

    def flip(self):
        max_y = max([point[1] for point in self.points])
        flipped_points = [(x, max_y - y) for (x, y) in self.points]
        flipped_grid = copy.deepcopy(self.grid)
        for point in flipped_points:
            flipped_grid[point[0]][point[1]] = '#'
        return Polyomino(self.size, flipped_points, flipped_grid)

    def rotate(self):
        rotated_points = [(y, -x) for (x, y) in self.points]
        min_x = min([point[0] for point in rotated_points])
        min_y = min([point[1] for point in rotated_points])
        rotated_points = [(x - min_x, y - min_y) for (x, y) in rotated_points]
        max_x = max([point[0] for point in rotated_points])
        max_y = max([point[1] for point in rotated_points])
        rotated_grid = [['.' for _ in range(max_y + 1)] for _ in range(max_x + 1)]
        for point in rotated_points:
            rotated_grid[point[0]][point[1]] = '#'
        return Polyomino(self.size, rotated_points, rotated_grid)

    def flip(self):
        max_x = max([point[0] for point in self.points])
        max_y = max([point[1] for point in self.points])
        flipped_points = [(x, max_y - y) for (x, y) in self.points]
        flipped_grid = [['.' for _ in range(max_y + 1)] for _ in range(max_x + 1)]
        for point in flipped_points:
            flipped_grid[point[0]][point[1]] = '#'
        return Polyomino(self.size, flipped_points, flipped_grid)

    def display(self):
        for row in self.grid:
            print(''.join(row))


def run():
    size = 6
    polyomino = Polyomino(size)
    polyomino.generate()
    polyomino.display()
    print("\nRotated:\n")
    rotated = polyomino.rotate()
    rotated.display()
    print("\nFlipped:\n")
    flipped = polyomino.flip()
    flipped.display()


# Importieren der string-Bibliotheksfunktion
import string
def run_test():
    # Storing the sets of punctuation,
    # digits, ascii_letters and whitespace
    # in variable result
    result = string.printable

    # Durchlaufen jedes Zeichens in result und Ausgeben
    for char in result:
        print(f"\"{char}\"")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
