import os
import shutil

def find_and_copy_files(src_dir):
    if not os.path.exists(src_dir):
        print(f"Quellverzeichnis {src_dir} existiert nicht.")
        return

    dst_dir = os.path.join(src_dir, '_NO_DOUBLE')
    os.makedirs(dst_dir, exist_ok=True)

    for filename in os.listdir(src_dir):
        if filename.endswith("-0.txt"):
            src_file_path = os.path.join(src_dir, filename)
            shutil.copy2(src_file_path, dst_dir)
            print(f"Datei {filename} wurde kopiert.")

def main(folderpPath):
    # Aufrufen der Funktion mit dem Pfad zum Quellverzeichnis
    # Bitte ändern Sie 'path_to_your_directory' zu Ihrem gewünschten Pfad
    find_and_copy_files(folderpPath)

if __name__ == "__main__":
    path ="/Volumes/MasterArbeit 3/GitHub/polyomino-benchmarks Kopie/group3/"
    path = "/Volumes/MasterArbeit 3/all runs/runRemainingBenchmarkGenerator/random-benchmark-generator/benchmarks/"
    folderName = "hexadekamino"
    main(path + folderName)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
