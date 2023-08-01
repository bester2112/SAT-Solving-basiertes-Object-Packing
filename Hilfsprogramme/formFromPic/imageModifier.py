import os
import glob


class ImageModifier:
    def __init__(self, filepath):
        with open(filepath, 'r') as f:
            self.data = [list(line.strip()) for line in f.readlines()]
        self.width = len(self.data[0])
        self.height = len(self.data)

    def extend_edges(self):
        # Add rows on top and bottom
        self.data.insert(0, ['B'] * self.width)
        self.data.append(['B'] * self.width)
        # Add columns on left and right
        for row in self.data:
            row.insert(0, 'B')
            row.append('B')
        self.width += 2
        self.height += 2

    def replace_A_with_B(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.data[i][j] == 'A':
                    self.data[i][j] = 'B'

    def write_to_file(self, filepath):
        with open(filepath, 'w') as f:
            for row in self.data:
                f.write(''.join(row) + '\n')


def extend_all_files_in_directory(dirpath):
    # Create the output directory if it doesn't exist
    out_dir = os.path.join(dirpath, 'special_txt_out')
    os.makedirs(out_dir, exist_ok=True)

    print(f'Current working directory: {os.getcwd()}')  # Print current directory
    print(f'Directory listing: {os.listdir(dirpath)}')  # Print directory listing

    # Process each file in the directory
    for filepath in glob.glob(os.path.join(dirpath, 'special-txt', '*.txt')):
        print(f'Processing file: {filepath}')
        img_mod = ImageModifier(filepath)

        # Extend edges four times
        for _ in range(4):
            img_mod.extend_edges()

        # Replace all "A"s with "B"s
        img_mod.replace_A_with_B()

        # Write output to a new filename in the output directory
        filename = os.path.basename(filepath)
        output_path = os.path.join(out_dir, 'special-' + filename)
        img_mod.write_to_file(output_path)
        print(f'Finished processing file: {output_path}')



if __name__ == '__main__':
    extend_all_files_in_directory('.')
