import itertools
import os
import numpy as np
from shape import Shape
from benchmark import Benchmark


class PuzzleGenerator:
    def __init__(self, min_size, max_size):
        self.min_size = min_size
        self.max_size = max_size

    def _generate_neighbors(self, position):
        x, y = position
        return [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]

    def _valid_position(self, position, width, height):
        x, y = position
        return 0 <= x < width and 0 <= y < height

    def _remove_empty_rows_and_columns(self, grid):
        non_empty_rows = [row for row in grid if any(cell == 1 for cell in row)]
        non_empty_columns = list(zip(*[row for row in zip(*non_empty_rows) if any(cell == 1 for cell in row)]))
        return [list(row) for row in non_empty_columns]

    def _generate_shape(self, width, height, available_area):
        visited = np.zeros((width, height), dtype=bool)
        start_position = (np.random.randint(0, width), np.random.randint(0, height))
        size = min(np.random.randint(self.min_size, self.max_size + 1), available_area)
        stack = [start_position]

        while stack:
            current_position = stack.pop()
            if not visited[current_position]:
                visited[current_position] = True
                size -= 1
                available_area -= 1

                if size == 0:
                    break

                neighbors = [neighbor for neighbor in self._generate_neighbors(current_position) if self._valid_position(neighbor, width, height)]
                np.random.shuffle(neighbors)
                stack.extend(neighbors)

        grid = self._remove_empty_rows_and_columns(visited.astype(int).tolist())
        return Shape(grid), available_area

    def generate_puzzle_pieces(self, width, height, area):
        remaining_area = area
        shapes = []
        while remaining_area > 0:
            shape, remaining_area = self._generate_shape(width, height, remaining_area)
            shape_size = sum(sum(row) for row in shape.grid)

            if self.min_size <= shape_size <= self.max_size:
                shapes.append(shape)

        return shapes

