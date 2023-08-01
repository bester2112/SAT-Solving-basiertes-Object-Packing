import cv2
import string
import random

def read_image(file_name):
    img = cv2.imread(file_name, cv2.IMREAD_UNCHANGED)
    alpha_channel = img[:, :, 3]
    binary_alpha = [['.' if pixel == 0 else '#' for pixel in row] for row in alpha_channel]
    return binary_alpha, sum(row.count('#') for row in binary_alpha)

def read_polyomino(file_name):
    polyominos = []
    with open(file_name, 'r') as file:
        polyomino = []
        for line in file:
            if line.strip() == '%%%':
                polyominos.append(polyomino)
                for row in polyomino:
                    print(''.join('#' if cell else '.' for cell in row))
                print()
                polyomino = []
            else:
                polyomino.append([1 if pixel == '#' else 0 for pixel in line.strip()])
        if polyomino:
            polyominos.append(polyomino)
            for row in polyomino:
                print(''.join('#' if cell else '.' for cell in row))
    return polyominos

def print_grid(grid):
    for row in grid:
        print(''.join(row))
    print()

def can_place_polyomino(grid, polyomino, r, c):
    if r + len(polyomino) > len(grid) or c + len(polyomino[0]) > len(grid[0]):
        return False
    for rp, row in enumerate(polyomino):
        for cp, cell in enumerate(row):
            if cell == 1 and grid[r+rp][c+cp] != '.':
                return False
    return True

def place_polyomino(grid, polyomino, symbol):
    rows, cols = len(grid), len(grid[0])
    for r in range(rows):
        for c in range(cols):
            if can_place_polyomino(grid, polyomino, r, c):
                for rp, row in enumerate(polyomino):
                    for cp, cell in enumerate(row):
                        if cell == 1:
                            grid[r+rp][c+cp] = symbol
                return True
    return False

def place_polyominos(grid, polyominos):
    ascii_symbols = list(string.ascii_letters + string.digits + string.punctuation)
    random.shuffle(ascii_symbols)
    used_polyominoes = []
    for polyomino in polyominos:
        symbol = ascii_symbols.pop(0)
        while place_polyomino(grid, polyomino, symbol):
            print_grid(grid)
            used_polyominoes.append(symbol)
    return grid, used_polyominoes

def main():
    polyominos = read_polyomino('polyomino/polyomino-3.txt')
    grid, black_pixel_count = read_image('abra-black/abra.png')
    contiguous_black_pixels = black_pixel_count  # replace this with the actual number of contiguous black pixels
    grid, used_polyominoes = place_polyominos(grid, polyominos)

if __name__ == '__main__':
    main()
