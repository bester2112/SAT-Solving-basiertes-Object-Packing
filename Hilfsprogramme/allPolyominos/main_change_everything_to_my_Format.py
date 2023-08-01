import fnmatch
import os
import shutil
import sys
import traceback

import numpy as np
from collections import defaultdict
import string
import random

# Funktion zum Finden der Dateien, die mit einem bestimmten Muster beginnen
def find_files(directory, pattern):
    for dirpath, dirs, files in os.walk(directory):
        for filename in fnmatch.filter(files, pattern):
            yield os.path.join(dirpath, filename)

class Formen:
    def __init__(self):
        self.formen_dict = defaultdict(int)
        self.formen_names = set()

    def generate_name(self):
        while True:
            name = ''.join(random.choices(string.ascii_letters, k=4))
            if name not in self.formen_names:
                self.formen_names.add(name)
                return name

    def dfs(self, matrix, i, j, shape, char):
        if i < 0 or i >= matrix.shape[0] or j < 0 or j >= matrix.shape[1] or matrix[i][j] != char or (i, j) in shape:
            return
        shape.append((i, j))
        self.dfs(matrix, i - 1, j, shape, char)
        self.dfs(matrix, i + 1, j, shape, char)
        self.dfs(matrix, i, j - 1, shape, char)
        self.dfs(matrix, i, j + 1, shape, char)

    def process(self, matrix):
        visited = np.zeros(matrix.shape, dtype=bool)
        for i in range(matrix.shape[0]):
            for j in range(matrix.shape[1]):
                if not visited[i][j]:
                    char = matrix[i][j]
                    shape = []
                    self.dfs(matrix, i, j, shape, char)
                    for coord in shape:
                        visited[coord] = True
                    min_i = min(coord[0] for coord in shape)
                    min_j = min(coord[1] for coord in shape)
                    normalized_shape = [[coord[0] - min_i, coord[1] - min_j] for coord in shape]
                    max_i = max(coord[0] for coord in normalized_shape)
                    max_j = max(coord[1] for coord in normalized_shape)
                    # Create a graphical representation of the shape
                    shape_repr = [["." for _ in range(max_j + 1)] for __ in range(max_i + 1)]
                    for coord in normalized_shape:
                        shape_repr[coord[0]][coord[1]] = "#"
                    self.formen_dict["\n".join("".join(line) for line in shape_repr)] += 1

    def print_formen(self):
        for form, count in self.formen_dict.items():
            name = self.generate_name()
            print(f"{count} {name}\n{form}\n%%%")

class FileOrganizer:
    def __init__(self, source_folder):
        self.source_folder = source_folder
        self._create_directories()

    def _create_directories(self):
        os.makedirs(os.path.join(self.source_folder, '_benchmarks_OK'), exist_ok=True)
        os.makedirs(os.path.join(self.source_folder, '_benchmarks_NO'), exist_ok=True)
        with open(os.path.join(self.source_folder, '_OK_list.txt'), 'w') as f:
            pass
        with open(os.path.join(self.source_folder, '_NO_list.txt'), 'w') as f:
            pass

    def organize_files(self):
        total_folders = len(list(os.walk(self.source_folder)))
        processed_folders = 0
        for root_name in os.listdir(self.source_folder):
            root_path = os.path.join(self.source_folder, root_name)
            if os.path.isdir(root_path):
                self._handle_folder(root_path, root_name)
                processed_folders += 1
                print(f"Processing folder: {root_name} ({processed_folders})")

    def _handle_folder(self, root_path, root_name):
        for dir_name in os.listdir(root_path):
            subdir_path = os.path.join(root_path, dir_name)
            if os.path.isdir(subdir_path):
                for subfolder in os.listdir(subdir_path):
                    subfolder_path = os.path.join(subdir_path, subfolder)
                    if os.path.isdir(subfolder_path):
                        self._process_files_in_folder(subfolder_path, root_name, dir_name, subfolder)

    def _process_files_in_folder(self, subfolder_path, root_name, dir_name, subfolder):
        for file in os.listdir(subfolder_path):
            if file in ['_OK.txt', '_NO.txt']:
                self._handle_file(file, subfolder_path, root_name, dir_name, subfolder)

    def _process_matrix_file(self, file_path, destination_folder):
        # Erstelle das Ausgabedateiformat basierend auf dem Eingabedatei-Pfad
        file_name = os.path.basename(file_path)
        output_file_path = os.path.join(destination_folder, f'processed_{file_name}')

        # Öffne die Datei und lese die Daten
        with open(file_path, 'r') as file:
            data = file.read().splitlines()

        # Erstelle ein numpy-Array aus den Daten
        matrix = np.array([list(line) for line in data])

        # Erstelle eine Instanz der Formen-Klasse und verarbeite die Matrix
        formen = Formen()
        formen.process(matrix)

        # Leite die Standardausgabe in die Ausgabedatei um und drucke die Formen
        original_stdout = sys.stdout
        with open(output_file_path, 'w') as file:
            sys.stdout = file
            print("p pack")
            print(matrix.shape[1], matrix.shape[0])
            formen.print_formen()
        sys.stdout = original_stdout

    def _handle_file(self, file, subfolder_path, root_name, dir_name, subfolder):
        file_path = os.path.join(subfolder_path, file)
        if file == '_NO.txt':
            new_path = os.path.join(self.source_folder, '_benchmarks_NO', root_name, dir_name, subfolder)
            counter = 0
            while os.path.exists(new_path + f'_{counter}') and (
                    os.path.exists(os.path.join(new_path + f'_{counter}', '_OK.txt')) or os.path.exists(
                    os.path.join(new_path + f'_{counter}', '_NO.txt'))):
                counter += 1
                if counter > 1000:
                    counter = 0
            new_path = new_path + f'_{counter}'
            os.makedirs(new_path, exist_ok=True)
            # Verschieben Sie jede Datei einzeln in das neue Verzeichnis
            for filename in os.listdir(subfolder_path):
                src_file = os.path.join(subfolder_path, filename)
                shutil.move(src_file, new_path)
            with open(os.path.join(self.source_folder, '_NO_list.txt'), 'a') as f:
                f.write(f"{file}, {new_path}, {subfolder_path}\n")
            # Prüfen Sie, ob das Verzeichnis leer ist, und löschen Sie es, wenn es so ist
            if not os.listdir(subfolder_path):
                os.rmdir(subfolder_path)
        elif file == '_OK.txt':
            new_path = os.path.join(self.source_folder, '_benchmarks_OK', root_name, dir_name, subfolder)
            counter = 0
            while os.path.exists(new_path + f'_{counter}') and (
                    os.path.exists(os.path.join(new_path + f'_{counter}', '_OK.txt')) or os.path.exists(
                    os.path.join(new_path + f'_{counter}', '_NO.txt'))):
                counter += 1
                if counter > 1000:
                    counter = 0
            new_path = new_path + f'_{counter}'
            os.makedirs(new_path, exist_ok=True)
            # Verschieben Sie jede Datei einzeln in das neue Verzeichnis
            for filename in os.listdir(subfolder_path):
                src_file = os.path.join(subfolder_path, filename)
                shutil.move(src_file, new_path)
            with open(os.path.join(self.source_folder, '_OK_list.txt'), 'a') as f:
                f.write(f"{file}, {new_path}, {subfolder_path}\n")
            # Wenn _OK.txt existiert, verarbeiten Sie alle Matrix-Dateien in diesem Ordner:
            for subfile in os.listdir(
                    new_path):  # Verwenden Sie hier 'new_path', da 'subfolder_path' jetzt leer sein könnte
                if subfile.startswith('string_matrix_'):
                    self._process_matrix_file(os.path.join(new_path, subfile), new_path)
            # Prüfen Sie, ob das Verzeichnis leer ist, und löschen Sie es, wenn es so ist
            if not os.listdir(subfolder_path):
                os.rmdir(subfolder_path)
    @staticmethod
    def find_deepest_dirs(root):
        dirs_with_subdirs = set()
        deepest_dirs = set()

        for dirpath, dirnames, filenames in os.walk(root):
            if dirnames:
                dirs_with_subdirs.add(dirpath)
            else:
                deepest_dirs.add(dirpath)

        return deepest_dirs - dirs_with_subdirs

    def rename_and_move_files(self):
        root = os.path.join(self.source_folder, '_benchmarks_OK')
        total_folders = len(list(self.find_deepest_dirs(root)))
        processed_folders = 0
        for dir in self.find_deepest_dirs(root):
            processed_folders += 1
            print(f"Renaming and moving files in folder: {dir} ({processed_folders}/{total_folders})")
            for file in os.listdir(dir):
                if file.startswith('processed_string_matrix_'):
                    # Extrahiere den neuen Dateinamen aus dem Ordnernamen
                    new_file_name = os.path.basename(dir).split('.')[0] + '.txt'
                    new_dir = os.path.dirname(dir)
                    # Benenne die Datei um und verschiebe sie in eine Ebene höher
                    old_file_path = os.path.join(dir, file)
                    new_file_path = os.path.join(new_dir, new_file_name)
                    os.rename(old_file_path, new_file_path)

    def move_files_to_done(self):
        ok_path = os.path.join(self.source_folder, '_benchmarks_OK')
        for root, dirs, _ in os.walk(ok_path):
            for dir in dirs:
                if 'polyomino-' in dir:
                    poly_path = os.path.join(root, dir)
                    subdirs = ['Gen8-new-withframe-black-ben2', 'Gen7-withframe-black-ben2',
                               'Gen8-withframe-black-ben2', 'inventory-withframe-black-ben2',
                               'misc-withframe-black-ben2']
                    for subdir in subdirs:
                        subdir_path = os.path.join(poly_path, subdir)
                        if os.path.exists(subdir_path):
                            # check for the folders
                            for item in os.listdir(subdir_path):
                                item_path = os.path.join(subdir_path, item)
                                if os.path.isdir(item_path):
                                    source_folder = subdir.split('-ben2')[0]
                                    source_file_path = os.path.join(source_folder, item)
                                    if os.path.exists(source_file_path):
                                        dest_folder = os.path.join('_done_' + source_folder)
                                        os.makedirs(dest_folder, exist_ok=True)
                                        shutil.move(source_file_path, dest_folder)



if __name__ == "__main__":

    sys.setrecursionlimit(2000000)

    try:
        organizer = FileOrganizer('done')
        organizer.organize_files()
        organizer.rename_and_move_files()
        organizer.move_files_to_done()
        # Bei erfolgreichem Abschluss, erstelle die _finish.txt Datei
        with open('done/_finish.txt', 'w') as f:
            f.write("Successfully finished processing.")
    except Exception as e:
        # Bei einem Fehler, erstelle die _error_occured.txt Datei und schreibe die Fehlermeldung hinein
        with open('done/_error_occured.txt', 'w') as f:
            f.write("An error occurred:\n")
            f.write(str(e))
            f.write(traceback.format_exc())
