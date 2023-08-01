import os
import shutil


def copy_and_rename_files(folder_path, pokemon_list):
    # Create mixed folder
    mixed_folder = os.path.join(folder_path, "polyomino-mixed")

    # If mixed folder exists, delete it
    if os.path.exists(mixed_folder):
        shutil.rmtree(mixed_folder)

    # Create a new mixed folder
    os.makedirs(mixed_folder)

    # Get list of all directories in the folder_path
    directories = [d for d in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, d))]

    # Iterate through all directories
    for dir in directories:
        # Check if the directory matches the pattern "polyomino-XY"
        if "polyomino-" in dir:
            # Get the number after "polyomino-"
            num = dir.split("-")[-1]

            # Get all the files in the directory
            files = os.listdir(os.path.join(folder_path, dir))

            # Iterate through all the files
            for file in files:
                # Check if the file (without .txt) is in the pokemon_list
                if file[:-4] in pokemon_list:
                    # Construct the new file name
                    new_file_name = file[:-4] + "-" + num + ".txt"

                    # Construct the source file path
                    source_path = os.path.join(folder_path, dir, file)

                    # Construct the destination file path
                    dest_path = os.path.join(mixed_folder, new_file_name)

                    # Copy the file to the destination
                    shutil.copy2(source_path, dest_path)

    print("Dateien wurden erfolgreich kopiert und umbenannt.")


def main():
    # Set path to folders
    folder_path = "/Users/mama/Documents/GitHub/all_benchmarks"

    # Pokemon list
    pokemon_list = ["pikachu", "charizard", "charizard-mega-x", "eevee", "bulbasaur",
                    "squirtle", "jigglypuff", "gengar", "mewtwo", "snorlax",
                    "psyduck", "gastly", "bellsprout"]

    # Call the function to copy and rename files
    copy_and_rename_files(folder_path, pokemon_list)


if __name__ == "__main__":
    main()
