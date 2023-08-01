import os
import glob
import numpy as np
import random
import string
from matrix_info import MatrixInfo


def convert_to_matrix(lines, width, height):
    matrix = np.zeros((height, width), dtype=int)
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == '#':
                matrix[i][j] = 1
    return matrix


def print_matrix(matrix):
    return '\n'.join([''.join(['.' if element == 0 else '#' for element in row]) for row in matrix])


def reduce_matrix(matrix):
    while np.all(matrix[0] == 1):
        matrix = matrix[1:]
    while np.all(matrix[-1] == 1):
        matrix = matrix[:-1]
    while np.all(matrix[:,0] == 1):
        matrix = np.delete(matrix, 0, 1)
    while np.all(matrix[:,-1] == 1):
        matrix = np.delete(matrix, -1, 1)
    matrix = np.logical_not(matrix).astype(int)  # Invertiert alle Werte in der Matrix
    return matrix


def read_file(file):
    with open(file, 'r') as f:
        lines = f.readlines()
    width, height = map(int, lines[1].split())
    shape_lines = [list(line.strip()) for line in lines[3:3+height]]
    matrix = convert_to_matrix(shape_lines, width, height)
    reduced_matrix = reduce_matrix(matrix)
    file_name = os.path.splitext(os.path.basename(file))[0]
    matrix_info = MatrixInfo(reduced_matrix, file_name, reduced_matrix.shape[1], reduced_matrix.shape[0])
    return matrix_info


def read_files_from_folder(folder):
    files = glob.glob(os.path.join(folder, "*.txt"))
    if len(files) < 2:
        print("Nicht genügend Dateien im Ordner.")
        return []
    random.shuffle(files)
    matrix_infos = []
    while files:
        if len(files) <= 8:
            num_files = len(files)
        else:
            num_files = random.randint(2, len(files) - 1)  # So bleibt immer mindestens eine Datei übrig
        selected_files = files[:num_files]
        files = files[num_files:]
        matrix_infos.extend([read_file(file) for file in selected_files])
    return matrix_infos


def create_files_from_matrix_infos(matrix_infos):
    if not os.path.exists("multiple_pokemon"):
        os.makedirs("multiple_pokemon")

    files_group = []
    while matrix_infos:
        total_width = 0
        total_height = 0
        total_width_original = 0
        total_height_original = 0

        num_files = random.randint(2, min(8, len(matrix_infos)))
        num_files = 5
        selected_infos = matrix_infos[:num_files]
        matrix_infos = matrix_infos[num_files:]
        files_group.append(selected_infos)

        total_width_original += sum(info.width for info in selected_infos)
        total_height_original += sum(info.height for info in selected_infos)
        #total_width += sum(info.trimmed_width for info in selected_infos)
        #total_height += sum(info.trimmed_height for info in selected_infos)
        total_width += sum(info.trimmed_width if info.trimmed_width is not None else 0 for info in selected_infos)
        total_height += sum(info.trimmed_height if info.trimmed_height is not None else 0 for info in selected_infos)

        file_names = '_'.join(info.file_name for info in selected_infos)
        with open(os.path.join("multiple_pokemon", f"{file_names}.txt"), 'w') as f:
            f.write("p pack\n")
            f.write(f"{total_width} {total_height}\n")
            for info in selected_infos:
                f.write(f"1 {''.join(random.choices(string.ascii_letters, k=4))}\n")
                f.write(print_matrix(info.matrix))
                f.write("\n%%%\n")



def main():
    matrix_infos = read_files_from_folder('/Users/mama/Documents/GitHub/Tetromino-Puzzle-SAT/pkmScrapper/mixed-6-withframe-colored-txt-tmp-benchmark')
    for info in matrix_infos:
        print("Vor dem Trimmen:")
        print(info)
        info.trim_sprite(0.85)  # 0.2 als der Prozentsatz (20%)
        print("Nach dem Trimmen:")
        print(info)

    create_files_from_matrix_infos(matrix_infos)


if __name__ == "__main__":
    main()
