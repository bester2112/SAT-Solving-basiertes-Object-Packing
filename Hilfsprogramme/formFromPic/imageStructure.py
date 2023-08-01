import os
import random
import string
from collections import Counter

class ImageStructure:
    def __init__(self, filepath):
        with open(filepath, 'r') as f:
            self.data = [list(line.strip()) for line in f.readlines()]
        self.width = len(self.data[0])
        self.height = len(self.data)
        self.blocks_in_width = (self.width - 1) // 4
        self.blocks_in_height = (self.height - 1) // 4
        self.midpoints = self.calculate_midpoints()
        self.new_coord_system = self.build_new_coord_system()
        self.figures = self.calculate_figures()
        self.alphabet = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
        self.new_data = None
        self.border_blocks = False

    def calculate_midpoints(self):
        midpoints = []
        for y in range(self.blocks_in_height):
            for x in range(self.blocks_in_width):
                mid_x = x * 4 + 2
                mid_y = y * 4 + 2
                midpoints.append({
                    'pos': (mid_x, mid_y),
                    'value': self.data[mid_y][mid_x],
                    'N': self.data[mid_y-2][mid_x],
                    'E': self.data[mid_y][mid_x+2],
                    'S': self.data[mid_y+2][mid_x],
                    'W': self.data[mid_y][mid_x-2],
                })
        return midpoints

    def build_new_coord_system(self):
        new_coord_system = [[' ']*self.blocks_in_width for _ in range(self.blocks_in_height)]
        for y in range(self.blocks_in_height):
            for x in range(self.blocks_in_width):
                new_coord_system[y][x] = self.midpoints[y*self.blocks_in_width + x]['value']
        return new_coord_system

    def print_new_coord_system(self):
        for line in self.new_coord_system:
            print(''.join(line))

    def get_block(self, x, y):
        if 0 <= x < self.blocks_in_width and 0 <= y < self.blocks_in_height:
            return self.midpoints[y*self.blocks_in_width + x]
        return None

    def dfs(self, x, y, figure_value, visited):
        block = self.get_block(x, y)
        if not block or (x, y) in visited or block['value'] != figure_value:
            return []
        visited.add((x, y))
        figure = [block]
        directions = [('N', 0, -1), ('E', 1, 0), ('S', 0, 1), ('W', -1, 0)]
        for direction, dx, dy in directions:
            if block[direction] == figure_value:
                figure += self.dfs(x + dx, y + dy, figure_value, visited)
        return figure

    def calculate_figures(self):
        visited = set()
        figures = []
        for y in range(self.blocks_in_height):
            for x in range(self.blocks_in_width):
                if (x, y) not in visited:
                    block = self.get_block(x, y)
                    figure = self.dfs(x, y, block['value'], visited)
                    if figure:
                        figures.append(figure)
        return figures

    def assign_letters_to_figures(self):
        for i, figure in enumerate(self.figures):
            letter = self.alphabet[i % len(self.alphabet)]  # wrap around if more than 26 figures
            for block in figure:
                u, v = block['pos']
                # We have to adjust the positions to match with the indices of self.new_data
                x = u // 4
                y = v // 4
                self.new_data[y][x] = letter

    def calculate_new_data_size(self):
        max_x_neu = max(block['pos'][0] // 4 for figure in self.figures for block in figure)
        max_y_neu = max(block['pos'][1] // 4 for figure in self.figures for block in figure)
        self.new_data = [[None for _ in range(max_x_neu + 1)] for _ in range(max_y_neu + 1)]

    def print_new_coord_system_with_figures(self):
        self.calculate_new_data_size()
        self.assign_letters_to_figures()
        for row in self.new_data:
            print(''.join(cell if cell is not None else '?' for cell in row))

    def are_same_shape(self, figure1, figure2):
        if len(figure1) != len(figure2):
            return False
        dx = figure1[0]['pos'][0] - figure2[0]['pos'][0]
        dy = figure1[0]['pos'][1] - figure2[0]['pos'][1]
        return all(
            block1['pos'][0] - dx == block2['pos'][0] and block1['pos'][1] - dy == block2['pos'][1] for block1, block2
            in zip(figure1, figure2))

    def encode_figure(self, figure):
        min_x = min(block['pos'][0] for block in figure) // 4
        min_y = min(block['pos'][1] for block in figure) // 4
        max_x = max(block['pos'][0] for block in figure) // 4
        max_y = max(block['pos'][1] for block in figure) // 4
        encoded = [['.' for _ in range(min_x, max_x + 1)] for _ in range(min_y, max_y + 1)]
        for block in figure:
            encoded[(block['pos'][1] // 4) - min_y][(block['pos'][0] // 4) - min_x] = '#'
        return [''.join(line) for line in encoded]

    def generate_unique_name(self, existing_names):
        while True:
            name = ''.join(random.choice(string.ascii_letters) for _ in range(4))
            if name not in existing_names:
                return name

    def count_figures(self):
        count = Counter()
        for figure in self.figures:
            for unique_figure in self.unique_figures:
                if self.are_same_shape(figure, unique_figure):
                    count[tuple(frozenset(block.items()) for block in unique_figure)] += 1
        return count

    def identify_border_blocks(self):
        border_blocks = []
        border_value = self.data[0][0]  # Das ist der Wert an der Position (0,0)
        for y in range(self.blocks_in_height):
            for x in range(self.blocks_in_width):
                block = self.get_block(x, y)
                if block and block['value'] == border_value:
                    border_blocks.append(block)
                    self.border_block = True
        self.border_blocks = border_blocks

    def write_to_file(self, filepath):
        self.unique_figures = []
        for figure in self.figures:
            if not any(self.are_same_shape(figure, unique_figure) for unique_figure in self.unique_figures):
                self.unique_figures.append(figure)

        # Identifizieren Sie die Randblöcke
        self.identify_border_blocks()

        existing_names = set()
        name_to_figure = {}
        border_name = None
        border_figure = None
        for figure in self.unique_figures:
            if figure[0] in self.border_blocks:  # Der erste Block jeder Figur ist der "Hauptblock"
                border_name = self.generate_unique_name(existing_names)
                existing_names.add(border_name)
                border_figure = figure
                break  # Da wir nur eine einzige Randdarstellung wollen, brechen wir die Schleife nach der ersten Übereinstimmung ab.

        figure_to_count = self.count_figures()

        # Ersetzen Sie alle "B"s mit "#" und alles andere mit "."
        self.new_coord_system = [['#' if cell == 'B' else '.' for cell in row] for row in self.new_coord_system]

        with open(filepath, 'w') as f:
            f.write('p pack\n')
            print("p pack")
            f.write(f'{len(self.new_data[0])} {len(self.new_data)}\n')
            print(f'{len(self.new_data[0])} {len(self.new_data)}')
            # Geben Sie zuerst die manipulierte Randform aus
            if self.border_blocks:
                if border_name and border_figure:
                    count = figure_to_count[tuple(frozenset(block.items()) for block in border_figure)]
                    f.write(f'{count} {border_name}\n')
                    print(f'{count} {border_name}')
                    for line in self.new_coord_system:  # Verwenden Sie new_coord_system für die Randdarstellung
                        f.write(''.join(line) + '\n')
                        print(''.join(line))
                    f.write('%%%\n')
            # Geben Sie dann die restlichen eindeutigen Figuren aus
            for figure in self.unique_figures:
                if figure[0] not in self.border_blocks:  # Überspringen Sie die Ausgabe für Randblöcke
                    name = self.generate_unique_name(existing_names)
                    existing_names.add(name)
                    name_to_figure[name] = figure
                    count = figure_to_count[tuple(frozenset(block.items()) for block in figure)]
                    f.write(f'{count} {name}\n')
                    print(f'{count} {name}')
                    for line in self.encode_figure(figure):
                        f.write(line + '\n')
                        print(line)
                    f.write('%%%\n')


