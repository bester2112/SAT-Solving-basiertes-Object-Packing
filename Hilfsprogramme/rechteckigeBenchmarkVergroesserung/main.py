import os
import glob
import shutil


def transform_file(file_path, multiplier, output_dir):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    # Ensure the file has at least two lines
    if len(lines) < 2:
        print(f"Skipping file {file_path} as it has less than 2 lines")
        return

    new_lines = []

    # handle the special first two lines
    new_lines.append(lines[0].strip() + "\n")  # "p pack"

    # For the 2nd line multiply each number by the multiplier
    parts = lines[1].strip().split(" ")
    parts[0] = str(int(parts[0]) * multiplier)  # width
    parts[1] = str(int(parts[1]) * multiplier)  # height
    new_lines.append(" ".join(parts) + "\n")

    for line in lines[2:]:
        if line.startswith("#") or line.startswith("."):
            new_lines.append(line)
        elif line.startswith("%%"):
            new_lines.append(line.strip() + "\n")
        else:
            parts = line.strip().split(" ")
            if parts[0].isdigit():
                # Multiply form count by square of multiplier
                parts[0] = str(int(parts[0]) * multiplier * multiplier)
            new_line = " ".join(parts)
            new_lines.append(new_line + "\n")

    file_name_parts = file_path.split('/')[-1].split('_')
    file_name_parts[1] = str(int(file_name_parts[1]) * multiplier)
    file_name_parts[2] = str(int(file_name_parts[2].split('-')[0]) * multiplier) + '-' + file_name_parts[2].split('-')[
        1]
    new_filename = '_'.join(file_name_parts)

    with open(os.path.join(output_dir, new_filename + ".txt"), 'w') as f:
        f.writelines(new_lines)


def process_directory(input_dir, multipliers):
    for multiplier in multipliers:
        output_dir = input_dir + "-" + str(multiplier) + "X"
        # Remove the output directory if it already exists
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)
        os.makedirs(output_dir, exist_ok=True)

        for file_path in glob.glob(input_dir + "/*.txt"):
            transform_file(file_path, multiplier, output_dir)


def main():
    base_dir = "/Users/mama/Documents/GitHub/runs/"
    directories = ["dekamino", "pentomino", "pentadekamino", "oktamino", "oktadekamino",
                   "nonamino", "icosamino", "hexomino", "hexadekamino", "heptamino",
                   "heptadekamino", "hendekamino", "ennedekamino", "dodekamino",
                   "dekamino", "tetradekamino", "tetromino", "tridekamino", "tromino"]
    multipliers = [2, 4]

    for directory in directories:
        input_dir = base_dir + directory
        process_directory(input_dir, multipliers)


if __name__ == "__main__":
    main()
