import os

def polyomino_generator(n, polyomino=None):
    if polyomino is None:
        polyomino = [(0, 0)]

    if len(polyomino) == n:
        yield polyomino
    else:
        for neighbor in neighbors(polyomino):
            new_polyomino = polyomino.copy()
            new_polyomino.append(neighbor)
            new_polyomino.sort()
            new_canonical_form = canonical_form(new_polyomino)
            if tuple(new_canonical_form) not in visited:
                visited.add(tuple(new_canonical_form))
                yield from polyomino_generator(n, new_polyomino)

def neighbors(polyomino):
    candidate_neighbors = [(x + dx, y + dy) for x, y in polyomino for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]]
    return [point for point in candidate_neighbors if candidate_neighbors.count(point) == 1 and point not in polyomino]

def print_polyomino(polyomino):
    x_coords = [x for x, y in polyomino]
    y_coords = [y for x, y in polyomino]
    grid = [['.' for _ in range(min(y_coords), max(y_coords)+1)] for _ in range(min(x_coords), max(x_coords)+1)]
    for x, y in polyomino:
        grid[x-min(x_coords)][y-min(y_coords)] = '#'
    return "\n".join("".join(row) for row in grid)

def canonical_form(polyomino):
    min_x = min(x for x, y in polyomino)
    min_y = min(y for x, y in polyomino)
    canonical_polyomino = sorted((x - min_x, y - min_y) for x, y in polyomino)
    return canonical_polyomino

def main():
    for n in range(1, 31):  # Generate polyominoes of size 1 to 20
        global visited
        visited = set()
        polyominoes = [print_polyomino(polyomino) for polyomino in polyomino_generator(n)]
        with open(f"polyomino-{n}.txt", "w") as f:
            f.write("\n%%%\n".join(polyominoes))
        print(f"polyomino-{n}.txt done")


if __name__ == "__main__":
    main()