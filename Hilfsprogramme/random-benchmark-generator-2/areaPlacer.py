import os
import random
from shape import Shape
from benchmark import Benchmark

class AreaPlacer:

    def __init__(self, width, height, min_pixel, max_pixel):
        self.X = width
        self.Y = height
        self.minPixel = min_pixel
        self.maxPixel = max_pixel
        self.currentArea = 1
        self.grid = [[-1 for _ in range(self.X)] for _ in range(self.Y)]

    def free_place_old(self):
        for y in range(self.Y):
            for x in range(self.X):
                if self.grid[y][x] == -1:
                    return x, y
        return None

    def free_place(self):
        free_places = [(x, y) for y in range(self.Y) for x in range(self.X) if self.grid[y][x] == -1]
        if not free_places:
            return None
        return random.choice(free_places)

    def possible_places(self, x, y):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        possible_positions = []

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < self.X and 0 <= new_y < self.Y and self.grid[new_y][new_x] == -1:
                if (new_x, new_y) not in possible_positions:
                    possible_positions.append((new_x, new_y))

        return possible_positions

    def place_areas(self):
        while self.currentArea <= self.X * self.Y:
            random_pixel = random.randint(self.minPixel, self.maxPixel)
            coord = self.free_place()

            if coord is None:
                break

            x, y = coord
            self.grid[y][x] = self.currentArea
            placed_pixels = 1

            while placed_pixels < random_pixel:
                possible_positions = self.possible_places(x, y)
                if not possible_positions:
                    break

                x, y = random.choice(possible_positions)
                self.grid[y][x] = self.currentArea
                placed_pixels += 1

            self.currentArea += 1

        return self.grid

    def generate_shapes(self, grid):
        shape_dict = {}
        for y in range(len(grid)):
            for x in range(len(grid[0])):
                shape_id = grid[y][x]
                if shape_id not in shape_dict:
                    shape_dict[shape_id] = []
                shape_dict[shape_id].append((x, y))

        shapes = {}
        for shape_id, coordinates in shape_dict.items():
            shape_grid = [[1 if (x, y) in coordinates else 0 for x in range(self.X)] for y in range(self.Y)]
            shape = Shape(shape_grid)
            shapes[shape] = shapes.get(shape, 0) + 1

        return shapes

    def save_benchmark(self, width, height, shapes, num_files, text, maxOneHash):
        if not os.path.exists("benchmarks"):
            os.mkdir("benchmarks")

        benchmark = Benchmark(width, height, shapes)
        with open(f"benchmarks/benchmark_{width}_{height}-{text}-mOH={maxOneHash}-{num_files}.txt", "w") as file:
            file.write(str(benchmark))
