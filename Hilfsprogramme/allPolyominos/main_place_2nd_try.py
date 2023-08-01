import numpy as np
import os
import random
import sys
sys.setrecursionlimit(150000000)  # Erhöhen der maximalen Rekursionstiefe
import cv2
import string
import re


def read_image(file_name):
    img = cv2.imread(file_name, cv2.IMREAD_UNCHANGED)
    alpha_channel = img[:, :, 3]
    binary_alpha = [['.' if pixel == 0 else '#' for pixel in row] for row in alpha_channel]

    # Ausgabe in der Konsole
    #for row in binary_alpha:
        # print(''.join(row))

    # Speichern in der Textdatei
    with open('abra.txt', 'w') as file:
        file.write('\n'.join([''.join(row) for row in binary_alpha]))

    return binary_alpha, sum(row.count('#') for row in binary_alpha)


def read_polyominos(file):
    with open(file, 'r') as f:
        lines = [line.strip() for line in f.readlines()]

    # Trennung der Polyominos
    polyominos_str = []
    temp_poly = []
    for line in lines:
        if line != '%%%':
            temp_poly.append(line)
        else:
            polyominos_str.append(temp_poly)
            temp_poly = []
    polyominos_str.append(temp_poly)  # Das letzte Polyomino hinzufügen

    polyominos = []
    for polyomino_str in polyominos_str:
        max_length = max(len(line) for line in polyomino_str)
        polyomino = [[c == '#' for c in line.ljust(max_length, '.')] for line in polyomino_str]
        polyominos.append(np.array(polyomino))

    # Ausgabe jedes Polyominos in der Kommandozeile
    #for i, polyomino in enumerate(polyominos):
    #    if len(polyomino) == 0:
    #        continue
    #    #print(f"Polyomino {i + 1}:")
    #    #for row in polyomino:
    #    #    for cell in row:
    #    #        print('#' if cell else '.', end='')
    #    #    print()
    #    #print()

    polyominos = []
    for polyomino_str in polyominos_str:
        max_length = max(len(line) for line in polyomino_str)
        polyomino = [[c == '#' for c in line.ljust(max_length, '.')] for line in polyomino_str]
        # Umwandlung in Koordinaten
        coords = [(i, j) for i, row in enumerate(polyomino) for j, cell in enumerate(row) if cell]
        polyominos.append(coords)

    # Ausgabe jedes Polyominos in der Kommandozeile
    for i, polyomino in enumerate(polyominos):
        if len(polyomino) == 0:
            continue
        #print(f"Polyomino {i + 1}:")
        max_x = max(coord[0] for coord in polyomino)
        max_y = max(coord[1] for coord in polyomino)
        matrix = [['.' for _ in range(max_y + 1)] for _ in range(max_x + 1)]
        for coord in polyomino:
            matrix[coord[0]][coord[1]] = '#'
        #for row in matrix:
        #    print(''.join(row))
        #print()

    return polyominos




# Funktion um die Matrix aus Datei zu lesen
def read_matrix(file):
    with open(file, 'r') as f:
        lines = f.readlines()
        max_length = max(len(line.strip()) for line in lines)
        matrix = [[c == '#' for c in line.strip().ljust(max_length, '.')] for line in lines]
    return np.array(matrix)

# Funktion um die Matrix aus Datei zu lesen und in zwei Formaten zurückzugeben
def read_matrices(file):
    with open(file, 'r') as f:
        lines = f.readlines()
        max_length = max(len(line.strip()) for line in lines)
        string_matrix = [list(line.strip().ljust(max_length, '.')) for line in lines]
        bool_matrix = [[c == '#' for c in line] for line in string_matrix]
    return np.array(string_matrix), np.array(bool_matrix)


# Funktion um zu überprüfen ob alle "#" zusammenhängend sind
def check_adjacent(matrix):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    visited = np.zeros_like(matrix, dtype=bool)
    stack = [(np.where(matrix)[0][0], np.where(matrix)[1][0])]
    while stack:
        x, y = stack.pop()
        if visited[x, y]:
            continue
        visited[x, y] = True
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < matrix.shape[0] and 0 <= ny < matrix.shape[1] and matrix[nx, ny] and not visited[nx, ny]:
                stack.append((nx, ny))
    return np.array_equal(matrix, visited)

# Funktion um das kleinste Polyomino zu finden
def smallest_polyomino(file):
    polyominos = os.listdir(file)
    smallest = min([int(polyomino.split('-')[1].split('.')[0]) for polyomino in polyominos])
    return smallest

# Hauptalgorithmus
def print_matrix(matrix):  # Funktion zum Drucken der Matrix
    for row in matrix:
        print(''.join('#' if cell else '.' for cell in row))
    print()

# Ausgabefunktionen für beide Matrizen
def print_string_matrix(matrix):
    for row in matrix:
        print(''.join(row))
    print()

def print_bool_matrix(matrix):
    for row in matrix:
        print(''.join('#' if cell else '.' for cell in row))
    print()


def can_place_polyomino(bool_matrix, i, j, polyomino):
    for dx, dy in polyomino: # für alle pixel in dem polyomino
        x = i + dx
        y = j + dy
        if x < 0 or x >= bool_matrix.shape[0]: # wert muss in der matrix sein
            return False
        if y < 0 or y >= bool_matrix.shape[1]: # wert muss in der matrix sein
            return False
        if not bool_matrix[x, y]: # wert muss auf true sein
            return False
    return True

# Hauptalgorithmus
def fit_polyomino_old(string_matrix, bool_matrix, polyominos, counter, counter_black, smallest, symbol_counter):
    if counter_black <= smallest:
        return True
    for i in range(bool_matrix.shape[0]):
        for j in range(bool_matrix.shape[1]):
            if bool_matrix[i, j]:  # Use the boolean matrix for calculations
                for index in range(len(polyominos)):
                    polyomino = polyominos[index]
                    # Check if the polyomino can be placed
                    if can_place_polyomino(bool_matrix, i, j, polyomino):
                        counter[index] += 1
                        counter_black -= len(polyomino)

                        # Generate a random symbol and apply it to the string matrix
                        symbol = random.choice(string.ascii_letters)
                        for dx, dy in polyomino:
                            bool_matrix[i + dx, j + dy] = False
                            string_matrix[i + dx, j + dy] = symbol
                        # print('After adding a polyomino:')
                        # print_string_matrix(string_matrix)  # Print the string matrix
                        # print_bool_matrix(bool_matrix)  # Print the bool matrix
                        # print('counter_black:', counter_black)

                        if fit_polyomino(string_matrix, bool_matrix, polyominos, counter, counter_black, smallest,
                                         symbol_counter):
                            return True
                        counter[index] -= 1
                        counter_black += len(polyomino)

                        # Revert the string matrix back to '#'
                        for dx, dy in polyomino:
                            bool_matrix[i + dx, j + dy] = True
                            string_matrix[i + dx, j + dy] = '#'
                        # print('After removing a polyomino:')
                        # print_string_matrix(string_matrix)  # Print the string matrix
                        # print_bool_matrix(bool_matrix)  # Print the bool matrix
                        # print('counter_black:', counter_black)
                return False
    return False


# Funktion zum Drucken der boolschen Matrix
def print_bool_matrix(bool_matrix):
    for i in range(bool_matrix.shape[0]):
        for j in range(bool_matrix.shape[1]):
            if bool_matrix[i, j]:
                print('.', end='')
            else:
                print('#', end='')
        print()


# Funktion um die Matrix aus Datei zu lesen
def read_matrix(file):
    with open(file, 'r') as f:
        lines = f.readlines()
        max_length = max(len(line.strip()) for line in lines)
        matrix = [[c == '#' for c in line.strip().ljust(max_length, '.')] for line in lines]
    return np.array(matrix)


def main_old():
    # Daten vorbereiten
    binary_alpha, black_pixel_count = read_image('abra-black/abra.png')
    #print(f"black pixel count {black_pixel_count}")
    string_matrix, bool_matrix = read_matrices('abra.txt')
    counter_black = np.sum(bool_matrix)
    if not check_adjacent(bool_matrix):
        #print('Die Matrix aus abra.txt ist nicht zusammenhängend.')
        exit(1)
    polyominos = read_polyominos('polyomino/polyomino-3.txt')
    counter = {i: 0 for i in range(len(polyominos))}

    # Kleinstes Polyomino ermitteln
    #smallest = smallest_polyomino('polyomino')

    # Hauptalgorithmus
    #if not fit_polyomino(string_matrix, bool_matrix, polyominos, counter, counter_black, smallest, 0):
        #print('Das Problem ist nicht lösbar.')


def save_to_files(string_matrix, bool_matrix, suffix):
    np.savetxt(f'string_matrix_{suffix}.txt', string_matrix, fmt='%s')
    np.savetxt(f'bool_matrix_{suffix}.txt', bool_matrix, fmt='%d')


def save_to_files_temp(string_matrix, bool_matrix, symbol_counter):
    # Save string_matrix
    with open(f'string_matrix_{symbol_counter}.txt', 'w') as f:
        f.write('\n'.join([''.join(row) for row in string_matrix]))
    # Save bool_matrix
    with open(f'bool_matrix_{symbol_counter}.txt', 'w') as f:
        f.write('\n'.join([''.join('.' if x == 0 else '#' for x in row) for row in bool_matrix]))


def read_bool_matrix(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    matrix = []
    for line in lines:
        matrix.append([0 if x == '.' else 1 for x in line.strip()])
    return np.array(matrix)

def read_string_matrix(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    matrix = []
    for line in lines:
        matrix.append(list(line.strip()))
    return np.array(matrix)

import unicodedata
import string

def get_next_symbol(string_matrix):
    used_symbols = set()
    for row in string_matrix:
        for symbol in row:
            if symbol != '.' and symbol not in used_symbols:
                used_symbols.add(symbol)

    # Erstellen Sie Sets von Symbolen in der gewünschten Reihenfolge
    all_symbols_ordered = [
        set(string.ascii_lowercase),
        set(string.ascii_uppercase),
        set(string.digits),
        set("!\"$%&'()*+,-/:;<=>?@[]^_`{|}~"),
        set(chr(i) for i in range(0x80, 0x250) if unicodedata.category(chr(i)).startswith('L'))
    ]

    # Durchlaufen Sie die Sets, bis Sie ein verfügbares Symbol finden
    for symbol_set in all_symbols_ordered:
        available_symbols = symbol_set - used_symbols
        if available_symbols:
            return random.choice(list(available_symbols))

    # Wenn wir hier ankommen, bedeutet das, dass wir keine verfügbaren Symbole gefunden haben
    return None



def handle_isolated_pixels(string_matrix, bool_matrix):
    # define the 4 directions to search for neighboring pixels: up, down, left, right
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for i in range(bool_matrix.shape[0]):
        for j in range(bool_matrix.shape[1]):
            if bool_matrix[i][j] == 1:  # if the pixel is set
                # check all 4 neighboring pixels
                if all(bool_matrix[i + di][j + dj] == 0 for di, dj in directions if 0 <= i + di < bool_matrix.shape[0] and 0 <= j + dj < bool_matrix.shape[1]):
                    # if all neighboring pixels are not set, this is an isolated pixel
                    string_matrix[i][j] = get_next_symbol(string_matrix)  # set a symbol in the string matrix
                    bool_matrix[i][j] = 0  # unset the pixel in the bool matrix
    return string_matrix, bool_matrix


def fill_remaining(string_matrix, bool_matrix):
    visited = np.zeros_like(bool_matrix, dtype=bool)

    def dfs(i, j, symbol):
        if 0 <= i < bool_matrix.shape[0] and 0 <= j < bool_matrix.shape[1] and bool_matrix[i, j] and not visited[i, j]:
            visited[i, j] = True
            string_matrix[i, j] = symbol
            bool_matrix[i, j] = False
            dfs(i - 1, j, symbol)
            dfs(i + 1, j, symbol)
            dfs(i, j - 1, symbol)
            dfs(i, j + 1, symbol)

    for i in range(bool_matrix.shape[0]):
        for j in range(bool_matrix.shape[1]):
            if bool_matrix[i, j]:
                symbol = get_next_symbol(string_matrix)
                dfs(i, j, symbol)

    return string_matrix, bool_matrix


def handle_isolated_pixels_and_small_groups(string_matrix, bool_matrix):
    # define the 4 directions to search for neighboring pixels: up, down, left, right
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # height and width of the matrix
    h, w = bool_matrix.shape

    #print('before adding pixels_and_small_groups:')
    #print_string_matrix(string_matrix)  # Print the string matrix
    #print_bool_matrix(bool_matrix)  # Print the bool matrix

    def dfs(i, j, group):
        if i < 0 or j < 0 or i >= h or j >= w or bool_matrix[i][j] == 0 or len(group) >= polyminio_size or (
        i, j) in group:
            return
        group.append((i, j))
        for di, dj in directions:
            dfs(i + di, j + dj, group)

    small_groups = 0
    unset_pixels = 0
    for i in range(h):
        for j in range(w):
            if bool_matrix[i][j] == 1:  # if the pixel is set
                group = []
                dfs(i, j, group)
                if len(group) < polyminio_size:  # if the group is smaller than polymino_size
                    small_groups += 1
                    for gi, gj in group:
                        string_matrix[gi][gj] = get_next_symbol(string_matrix)  # set a symbol in the string matrix
                        bool_matrix[gi][gj] = 0  # unset the pixel in the bool matrix
                        unset_pixels += 1

    #print(f"Number of small groups: {small_groups}")
    #print(f"Number of unset pixels: {unset_pixels}")
    #print('after adding pixels_and_small_groups:')
    #print_string_matrix(string_matrix)  # Print the string matrix
    #print_bool_matrix(bool_matrix)  # Print the bool matrix
    return string_matrix, bool_matrix, unset_pixels


def fit_polyomino(string_matrix, bool_matrix, polyominos, counter, counter_black, symbol_counter=16, counter_black_start=None):
    if counter_black_start is None:  # Initialization for the first run
        counter_black_start = counter_black
    elif counter_black_start - counter_black >= polyminio_size:  # Check if we have placed 30 blocks
        save_to_files_temp(string_matrix, bool_matrix, symbol_counter)
        # reload the matrices and rerun the fit_polyomino function
        string_matrix, bool_matrix = read_matrices(f'bool_matrix_{symbol_counter}.txt')
        #bool_matrix = read_bool_matrix(f'bool_matrix_{symbol_counter}.txt')
        string_matrix = read_string_matrix(f'string_matrix_{symbol_counter}.txt')
        # handle any isolated pixels
        string_matrix, bool_matrix, unset_pixels = handle_isolated_pixels_and_small_groups(string_matrix, bool_matrix)
        counter_black = counter_black - unset_pixels
        return fit_polyomino(string_matrix, bool_matrix, polyominos, counter, counter_black, symbol_counter+1, counter_black)

    if counter_black <= 4 * polyminio_size:
        string_matrix, bool_matrix, unset_pixels = handle_isolated_pixels_and_small_groups(string_matrix, bool_matrix)
        counter_black = np.sum(bool_matrix)

        # print('After adding counter_black <= 4 * polyminio_size:')
        # print_string_matrix(string_matrix)  # Print the string matrix
        # print_bool_matrix(bool_matrix)  # Print the bool matrix
        # print('counter_black:', counter_black)
        save_to_files_temp(string_matrix, bool_matrix, symbol_counter + 1)


    if counter_black <= polyminio_size:
        string_matrix, bool_matrix = fill_remaining(string_matrix, bool_matrix)

        #print('After adding counter_black <= smallest:')
        #print_string_matrix(string_matrix)  # Print the string matrix
        #print_bool_matrix(bool_matrix)  # Print the bool matrix
        #print('counter_black:', counter_black)
        save_to_files_temp(string_matrix, bool_matrix, symbol_counter + 2)
        return True
    for i in range(bool_matrix.shape[0]):
        for j in range(bool_matrix.shape[1]):
            if bool_matrix[i, j]:  # Use the boolean matrix for calculations
                for index in range(len(polyominos)):
                    polyomino = polyominos[index]
                    # Check if the polyomino can be placed
                    if can_place_polyomino(bool_matrix, i, j, polyomino):
                        counter[index] += 1
                        counter_black -= len(polyomino)

                        # Generate a random symbol and apply it to the string matrix
                        symbol = get_next_symbol(string_matrix)
                        for dx, dy in polyomino:
                            bool_matrix[i + dx, j + dy] = False
                            string_matrix[i + dx, j + dy] = symbol
                        #print('After adding a polyomino:')
                        #print_string_matrix(string_matrix)  # Print the string matrix
                        #print_bool_matrix(bool_matrix)  # Print the bool matrix
                        #print('counter_black:', counter_black)

                        if fit_polyomino(string_matrix, bool_matrix, polyominos, counter, counter_black,
                                         symbol_counter, counter_black_start):
                            return True
                        counter[index] -= 1
                        counter_black += len(polyomino)

                        # Revert the string matrix back to '#'
                        for dx, dy in polyomino:
                            bool_matrix[i + dx, j + dy] = True
                            string_matrix[i + dx, j + dy] = '#'
                        #print('After removing a polyomino:')
                        #print_string_matrix(string_matrix)  # Print the string matrix
                        #print_bool_matrix(bool_matrix)  # Print the bool matrix
                        #print('counter_black:', counter_black)
                return False
    return False


def main(polyomino_file, polyomino_size, polyominos):
    # Daten vorbereiten
    global polyminio_size
    polyminio_size = polyomino_size
    binary_alpha, black_pixel_count = read_image('abra.png')
    # print(f"black pixel count {black_pixel_count}")
    string_matrix, bool_matrix = read_matrices('abra.txt')
    counter_black = np.sum(bool_matrix)
    if not check_adjacent(bool_matrix):
        # print('Die Matrix aus abra.txt ist nicht zusammenhängend.')
        string_matrix, bool_matrix, unset_pixels = handle_isolated_pixels_and_small_groups(string_matrix, bool_matrix)
        counter_black = counter_black - unset_pixels
        #return False
        #exit(1)
    #polyominos = read_polyominos('polyomino/' + polyomino_file)
    counter = {i: 0 for i in range(len(polyominos))}

    # Kleinstes Polyomino ermitteln
    #smallest = smallest_polyomino('polyomino')

    # Hauptalgorithmus
    if not fit_polyomino(string_matrix, bool_matrix, polyominos, counter, counter_black, 0):
        #print('Das Problem ist nicht lösbar.')
        return False

    return True


def fit_polyomino_rotated(string_matrix, bool_matrix, polyominos, counter, counter_black, symbol_counter, counter_black_start=None):
    if counter_black_start is None:  # Initialization for the first run
        counter_black_start = counter_black
    elif counter_black_start - counter_black >= 3:  # Check if we have placed 30 blocks
        save_to_files_temp(string_matrix, bool_matrix, symbol_counter)
        # reload the matrices and rerun the fit_polyomino function
        string_matrix, bool_matrix = read_matrices(f'bool_matrix_{symbol_counter}.txt')
        #bool_matrix = read_bool_matrix(f'bool_matrix_{symbol_counter}.txt')
        string_matrix = read_string_matrix(f'string_matrix_{symbol_counter}.txt')
        # handle any isolated pixels
        string_matrix, bool_matrix, unset_pixels = handle_isolated_pixels_and_small_groups(string_matrix, bool_matrix)
        counter_black = counter_black - unset_pixels
        return fit_polyomino_rotated(string_matrix, bool_matrix, polyominos, counter, counter_black, symbol_counter+1, counter_black)

    if counter_black <= 4 * polyminio_size:
        string_matrix, bool_matrix, unset_pixels = handle_isolated_pixels_and_small_groups(string_matrix, bool_matrix)
        counter_black = np.sum(bool_matrix)

        # print('After adding counter_black <= 4 * polyminio_size:')
        # print_string_matrix(string_matrix)  # Print the string matrix
        # print_bool_matrix(bool_matrix)  # Print the bool matrix
        # print('counter_black:', counter_black)
        save_to_files_temp(string_matrix, bool_matrix, symbol_counter + 1)


    if counter_black <= polyminio_size:
        string_matrix, bool_matrix = fill_remaining(string_matrix, bool_matrix)

        # print('After adding counter_black <= smallest:')
        # print_string_matrix(string_matrix)  # Print the string matrix
        # print_bool_matrix(bool_matrix)  # Print the bool matrix
        # print('counter_black:', counter_black)
        save_to_files_temp(string_matrix, bool_matrix, symbol_counter + 2)
        return True
    for i in range(bool_matrix.shape[0]):
        for j in range(bool_matrix.shape[1]):
            if bool_matrix[i, j]:  # Use the boolean matrix for calculations
                for index in range(len(polyominos)):
                    polyomino = polyominos[index]
                    # Check if the polyomino can be placed
                    if can_place_polyomino(bool_matrix, i, j, polyomino):
                        counter[index] += 1
                        counter_black -= len(polyomino)

                        # Generate a random symbol and apply it to the string matrix
                        symbol = get_next_symbol(string_matrix)
                        for dx, dy in polyomino:
                            bool_matrix[i + dx, j + dy] = False
                            string_matrix[i + dx, j + dy] = symbol
                        # print('After adding a polyomino:')
                        # print_string_matrix(string_matrix)  # Print the string matrix
                        # print_bool_matrix(bool_matrix)  # Print the bool matrix
                        # print('counter_black:', counter_black)

                        if fit_polyomino_rotated(string_matrix, bool_matrix, polyominos, counter, counter_black,
                                         symbol_counter, counter_black_start):
                            return True
                        counter[index] -= 1
                        counter_black += len(polyomino)

                        # Revert the string matrix back to '#'
                        for dx, dy in polyomino:
                            bool_matrix[i + dx, j + dy] = True
                            string_matrix[i + dx, j + dy] = '#'
                        # print('After removing a polyomino:')
                        # print_string_matrix(string_matrix)  # Print the string matrix
                        # print_bool_matrix(bool_matrix)  # Print the bool matrix
                        # print('counter_black:', counter_black)
                return False
    return False


def get_image_dimensions(image):
    height = len(image)
    width = len(image[0]) if height > 0 else 0
    return height, width


def rotate_only():
    # Daten vorbereiten
    binary_alpha, black_pixel_count = read_image('abra.png')
    img_height, img_width = get_image_dimensions(binary_alpha)
    # print(f"black pixel count {black_pixel_count}")

    # Dateien sammeln
    files = os.listdir('.')
    # Wir speichern die Nummer aus dem Dateinamen und den Dateityp (bool oder string) in der Liste matrix_files
    matrix_files = [(f, int(re.search(r'(\d+)', f).group(1)), 'bool' if 'bool_matrix' in f else 'string') for f in files
                    if re.search(r'_\d+\.txt$', f)]
    matrix_files.sort(key=lambda x: x[1], reverse=True)

    bool_temp = string_temp = None
    bool_num = string_num = -1

    for file_name, num, file_type in matrix_files:
        if file_type == 'bool':
            bool_temp = read_bool_matrix(file_name)
            bool_num = num
        elif file_type == 'string':
            string_temp = read_string_matrix(file_name)
            string_num = num

        if bool_temp is not None and string_temp is not None and bool_num == string_num and \
                ((bool_temp.shape == (img_height, img_width) and string_temp.shape == (img_height, img_width)) or
                 (bool_temp.shape == (img_width, img_height) and string_temp.shape == (img_width, img_height))):
            string_matrix = string_temp
            bool_matrix = bool_temp
            break

    if string_matrix is None or bool_matrix is None:
        # print('Keine passenden Matrizen gefunden.')
        return

    # Matrix um 90 Grad drehen
    bool_matrix = np.rot90(bool_matrix)
    string_matrix = np.rot90(string_matrix)

    # Dateien speichern
    save_to_files_temp(string_matrix, bool_matrix, bool_num+1)


def rotated_main(polyomino_file, polyomino_size, polyominos):
    # Daten vorbereiten
    global polyminio_size
    polyminio_size = polyomino_size
    binary_alpha, black_pixel_count = read_image('abra.png')
    img_height, img_width = get_image_dimensions(binary_alpha)
    # print(f"black pixel count {black_pixel_count}")

    # Dateien sammeln
    files = os.listdir('.')
    # Wir speichern die Nummer aus dem Dateinamen und den Dateityp (bool oder string) in der Liste matrix_files
    matrix_files = [(f, int(re.search(r'(\d+)', f).group(1)), 'bool' if 'bool_matrix' in f else 'string') for f in files
                    if re.search(r'_\d+\.txt$', f)]
    matrix_files.sort(key=lambda x: x[1], reverse=True)

    bool_temp = string_temp = None
    bool_num = string_num = -1

    for file_name, num, file_type in matrix_files:
        if file_type == 'bool':
            bool_temp = read_bool_matrix(file_name)
            bool_num = num
        elif file_type == 'string':
            string_temp = read_string_matrix(file_name)
            string_num = num

        if bool_temp is not None and string_temp is not None and bool_num == string_num and \
                ((bool_temp.shape == (img_height, img_width) and string_temp.shape == (img_height, img_width)) or
                 (bool_temp.shape == (img_width, img_height) and string_temp.shape == (img_width, img_height))):
            string_matrix = string_temp
            bool_matrix = bool_temp
            break

    if string_matrix is None or bool_matrix is None:
        # print('Keine passenden Matrizen gefunden.')
        return False

    counter_black = np.sum(bool_matrix)
    if not check_adjacent(bool_matrix):
        # print('Die Matrix aus abra.txt ist nicht zusammenhängend.')
        string_matrix, bool_matrix, unset_pixels = handle_isolated_pixels_and_small_groups(string_matrix, bool_matrix)
        counter_black = counter_black - unset_pixels

    #polyominos = read_polyominos('polyomino/' + polyomino_file)
    counter = {i: 0 for i in range(len(polyominos))}

    # Kleinstes Polyomino ermitteln
    #smallest = smallest_polyomino('polyomino')

    #print_bool_matrix(bool_matrix)
    #print_string_matrix(string_matrix)

    # Matrix um 90 Grad drehen
    bool_matrix = np.rot90(bool_matrix)
    string_matrix = np.rot90(string_matrix)

    #print_bool_matrix(bool_matrix)
    #print_string_matrix(string_matrix)

    # Hauptalgorithmus
    if not fit_polyomino_rotated(string_matrix, bool_matrix, polyominos, counter, counter_black, bool_num+1):
        # print('Das Problem ist nicht lösbar.')
        return False

    return True



if __name__ == '__main__':
    main()