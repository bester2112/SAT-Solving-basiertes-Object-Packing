import random
from shape import Shape
from benchmark import Benchmark
from collections import defaultdict
from collections import deque


class BenchmarkGenerator:
    @staticmethod
    def generate_benchmark(x, y, z, w, minPixels, maxPixels):
        shapes = defaultdict(int)
        grid = [[1 for _ in range(z)] for _ in range(w)]
        visited = [[False for _ in range(z)] for _ in range(w)]

        num_shapes = random.randint(x, (x * y) // 2)
        for _ in range(num_shapes):
            if not BenchmarkGenerator.has_unvisited(visited):
                break
            row, col = BenchmarkGenerator.select_random_unvisited(visited)
            shape_grid, visited = BenchmarkGenerator.extract_shape(grid, visited, row, col, x, y, minPixels, maxPixels)
            if not shape_grid:  # Wenn keine Form gefunden wurde, die den Pixelanforderungen entspricht, überspringen
                continue
            shape = Shape(shape_grid)
            shapes[shape] += 1

        return Benchmark(z, w, shapes)

    @staticmethod
    def has_unvisited(visited):
        return any(not all(row) for row in visited)

    @staticmethod
    def select_random_unvisited(visited):
        unvisited_cells = [(row, col) for row in range(len(visited)) for col in range(len(visited[row])) if
                           not visited[row][col]]
        return random.choice(unvisited_cells)

    @staticmethod
    def extract_shape(grid, visited, row, col, x, y, minPixels, maxPixels):
        shape_grid = []
        q = deque([(row, col)])
        min_row, max_row = row, row
        min_col, max_col = col, col

        cells_added = 0
        while q:
            r, c = q.popleft()
            if not visited[r][c]:
                shape_grid.append((r, c))
                visited[r][c] = True
                cells_added += 1

                min_row, max_row = min(min_row, r), max(max_row, r)
                min_col, max_col = min(min_col, c), max(max_col, c)

                if cells_added < maxPixels:  # Füge Nachbarzellen nur hinzu, wenn die Anzahl der hinzugefügten Zellen weniger als maxPixels beträgt
                    for dr, dc in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and not visited[nr][nc] and abs(nr - row) < x and abs(nc - col) < y:
                            q.append((nr, nc))

        if cells_added < minPixels:  # Wenn die Anzahl der hinzugefügten Zellen weniger als minPixels beträgt, wird die Form verworfen
            for r, c in shape_grid:
                visited[r][c] = False
            return [], visited

        return [[grid[r][c] for c in range(min_col, max_col + 1)] for r in range(min_row, max_row + 1)], visited