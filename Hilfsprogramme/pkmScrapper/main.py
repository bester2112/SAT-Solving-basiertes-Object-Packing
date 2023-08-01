import os
import string
import random
import requests
import numpy as np
from PIL import Image
from pathlib import Path
from bs4 import BeautifulSoup
from skimage import measure, filters, color
from string import ascii_uppercase
import sys

# Set recursion limit
sys.setrecursionlimit(3000000)  # Set the recursion limit to 3000



def download_sprites(url, folder, img_class):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('img', {'class': img_class})

    urls = [img['src'] for img in img_tags]

    if not os.path.exists(folder):
        os.makedirs(folder)

    for url in urls:
        response = requests.get(url)
        with open(os.path.join(folder, os.path.basename(url)), 'wb') as f:
            f.write(response.content)

    print(f"{folder} download_sprites done")


def download_folders2():
    download_sprites("https://msikma.github.io/pokesprite/overview/dex-gen7.html", "Gen7", 'p')

def download_folders():
    download_sprites("https://msikma.github.io/pokesprite/overview/dex-gen7.html", "Gen7", 'p')
    download_sprites("https://msikma.github.io/pokesprite/overview/dex-gen8.html", "Gen8", 'p')
    download_sprites("https://msikma.github.io/pokesprite/overview/dex-gen8-new.html", "Gen8-new", 'p')
    download_sprites("https://msikma.github.io/pokesprite/overview/inventory.html", "inventory", 'i')
    download_sprites("https://msikma.github.io/pokesprite/overview/misc.html", "misc", 'm')


def crop_transparency(image):
    # Konvertiere das Bild in ein Format mit Alphakanal
    image = image.convert("RGBA")

    # Erstelle eine Maske des Alphakanals
    mask = Image.new('L', image.size, 0)
    for i in range(image.width):
        for j in range(image.height):
            if image.getpixel((i, j))[-1] != 0:
                mask.putpixel((i, j), 255)

    # Schneide das Bild entlang der Maske zurecht
    bounds = mask.getbbox()
    if bounds:
        image = image.crop(bounds)

    return image


def add_border(input_image_path, output_image_path):
    img = Image.open(input_image_path)
    img = crop_transparency(img)

    img_with_border = Image.new('RGBA', (img.width + 2, img.height + 2), (0, 0, 0, 0))
    img_with_border.paste(img, (1, 1))

    img_with_border.save(output_image_path)


def process_images(original_folder, new_folder):
    if not os.path.exists(new_folder):
        os.makedirs(new_folder)

    for filename in os.listdir(original_folder):
        if filename.endswith('.png'):
            add_border(os.path.join(original_folder, filename), os.path.join(new_folder, filename))

    print(f"{original_folder} {new_folder} process images done")


def modify_images():
    process_images('Gen7', 'Gen7-withframe')
    process_images('Gen8', 'Gen8-withframe')
    process_images('Gen8-new', 'Gen8-new-withframe')
    process_images('inventory', 'inventory-withframe')
    process_images('misc', 'misc-withframe')


def process_image_color(input_image_path, output_colored_path):
    # Lade das Bild
    img = Image.open(input_image_path).convert('RGBA')
    data = np.array(img)

    # Konvertiere das Bild in Graustufen und finde die Regionen
    gray = color.rgb2gray(data[..., :3])
    threshold = filters.threshold_otsu(gray)
    labels = measure.label(gray < threshold)

    # Erstelle Farbkarten für die farbigen Bilder
    colored_data = data.copy()
    used_colors = set([(0, 0, 0)])  # Add black to used colors

    for region in measure.regionprops(labels):
        # Wähle eine neue Farbe für die Region
        while True:
            new_color = np.random.randint(0, 256, 3)
            if tuple(new_color) not in used_colors:
                used_colors.add(tuple(new_color))
                break

        # Färbe die Region ein
        for coord in region.coords:
            # Check if pixel is not black (frame)
            if not np.array_equal(data[coord[0], coord[1], :3], [0, 0, 0]):
                colored_data[coord[0], coord[1], :3] = new_color

    # Speichere die bearbeiteten Bilder
    Image.fromarray(colored_data).save(output_colored_path)


def process_image_black(input_image_path, output_black_path):
    # Lade das Bild
    img = Image.open(input_image_path).convert('RGBA')
    data = np.array(img)

    # Erstelle die schwarzen Bilder
    black_data = data.copy()

    # Setze alle nicht-transparenten Pixel auf schwarz
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            if data[i, j, 3] > 0:  # Nicht transparent
                black_data[i, j, :3] = 0  # Schwarz

    # Speichere die bearbeiteten Bilder
    Image.fromarray(black_data).save(output_black_path)


def process_images_region(original_folder):
    colored_folder = original_folder + '-colored'
    black_folder = original_folder + '-black'

    if not os.path.exists(colored_folder):
        os.makedirs(colored_folder)
    if not os.path.exists(black_folder):
        os.makedirs(black_folder)

    for filename in os.listdir(original_folder):
        if filename.endswith('.png'):
            process_image_color(
                os.path.join(original_folder, filename),
                os.path.join(colored_folder, filename)
            )
            process_image_black(
                os.path.join(original_folder, filename),
                os.path.join(black_folder, filename)
            )

    print(f"{original_folder} {black_folder} {colored_folder} process images region done")

def modify_color2():
    process_images_region('Gen7-withframe')

def modify_color3(folderprefix):
    process_images_region(folderprefix+'-withframe')
def modify_color():
    process_images_region('Gen7-withframe')
    process_images_region('Gen8-withframe')
    process_images_region('Gen8-new-withframe')
    process_images_region('inventory-withframe')
    process_images_region('misc-withframe')


def process_images_txt3(folder_name):
    # Set alphabet letters
    alphabet = [char for char in ascii_uppercase if char != 'B']
    # Generate identifiers
    identifiers = [f'{letter}{num}' for letter in alphabet for num in range(1, 10000)]

    # Check if destination folder exists, if not create it
    if not os.path.exists(f'{folder_name}-txt-tmp'):
        os.makedirs(f'{folder_name}-txt-tmp')

    # Loop over every file in the directory
    for filename in os.listdir(folder_name):
        if filename.endswith('.png'):
            try:
                image_path = os.path.join(folder_name, filename)
                image = Image.open(image_path)
                pixels = image.load()

                width, height = image.size

                color_letter_dict = {}
                color_letter_dict[(0, 0, 0, 255)] = 'C'  # Black
                color_letter_dict[(0, 0, 0, 0)] = 'B'  # Transparent

                # First pass: count unique colors and assign letters/identifiers
                unique_colors = set()
                for y in range(height):
                    for x in range(width):
                        pixel_color = pixels[x, y]
                        unique_colors.add(pixel_color)

                # Check if unique colors exceed alphabet length
                if len(unique_colors) - 1 > len(alphabet):
                    available_identifiers = identifiers[:]
                else:
                    available_identifiers = alphabet[:]

                for color in unique_colors:
                    if color not in color_letter_dict:
                        if len(available_identifiers) == 0:
                            raise ValueError('Ran out of unique identifiers for colors')
                        assigned_identifier = available_identifiers.pop(0)
                        color_letter_dict[color] = assigned_identifier

                # Second pass: replace colors with letters/identifiers
                text_repr = []
                for y in range(height):
                    row = []
                    for x in range(width):
                        pixel_color = pixels[x, y]
                        row.append(color_letter_dict[pixel_color])
                    text_repr.append(''.join(row))


                # Write to txt file
                filname_without_ending = filename.replace(".png", "")
                with open(f'{folder_name}-txt-tmp/{filname_without_ending}.txt', 'w') as f:
                    f.write('\n'.join(text_repr))
            except Exception as e:
                print(f"Error processing file {filname_without_ending}: {e}")

    print(f"{folder_name} process images region done")

def process_images_txt(folder_name):
    # Set alphabet letters
    alphabet = [char for char in ascii_uppercase if char != 'B']
    # Generate identifiers
    identifiers = [f'{letter}{num}' for letter in alphabet for num in range(1, 10000)]

    # Check if destination folder exists, if not create it
    if not os.path.exists(f'{folder_name}-txt-tmp'):
        os.makedirs(f'{folder_name}-txt-tmp')

    # Loop over every file in the directory
    for filename in os.listdir(folder_name):
        if filename.endswith('.png'):
            try:
                image_path = os.path.join(folder_name, filename)
                image = Image.open(image_path)
                pixels = image.load()

                width, height = image.size

                color_letter_dict = {}
                color_letter_dict[(0, 0, 0, 255)] = 'B'  # Black
                color_letter_dict[(0, 0, 0, 0)] = 'B'  # Transparent

                # First pass: count unique colors and assign letters/identifiers
                unique_colors = set()
                for y in range(height):
                    for x in range(width):
                        pixel_color = pixels[x, y]
                        unique_colors.add(pixel_color)

                # Check if unique colors exceed alphabet length
                if len(unique_colors) - 1 > len(alphabet):
                    available_identifiers = identifiers[:]
                else:
                    available_identifiers = alphabet[:]

                for color in unique_colors:
                    if color not in color_letter_dict:
                        if len(available_identifiers) == 0:
                            raise ValueError('Ran out of unique identifiers for colors')
                        assigned_identifier = available_identifiers.pop(0)
                        color_letter_dict[color] = assigned_identifier

                # Second pass: replace colors with letters/identifiers
                text_repr = []
                for y in range(height):
                    row = []
                    for x in range(width):
                        pixel_color = pixels[x, y]
                        row.append(color_letter_dict[pixel_color])
                    text_repr.append(''.join(row))


                # Write to txt file
                filname_without_ending = filename.replace(".png", "")
                with open(f'{folder_name}-txt-tmp/{filname_without_ending}.txt', 'w') as f:
                    f.write('\n'.join(text_repr))
            except Exception as e:
                print(f"Error processing file {filname_without_ending}: {e}")

    print(f"{folder_name} process images region done")


def create_text_files2():
    process_images_txt('Gen7-withframe-colored')

def create_text_files3(folderprefix):
    process_images_txt3(folderprefix + '-withframe-colored')

def create_text_files():
    process_images_txt('Gen7-withframe-colored')
    process_images_txt('Gen8-withframe-colored')
    process_images_txt('Gen8-new-withframe-colored')
    process_images_txt('inventory-withframe-colored')
    process_images_txt('misc-withframe-colored')


def generate_random_name():
    return ''.join(random.choices(string.ascii_uppercase, k=4))


def identify_and_print_areas3(text):
    # Convertiere Text in 2D-Array
    lines = text.split('\n')
    grid = [list(line) for line in lines]

    # Definiere Größe der Karte
    m = len(grid)
    n = len(grid[0])

    # Definiere Richtungen für die Tiefensuche (oben, unten, links, rechts)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def dfs(x, y, letter, area):
        if x < 0 or y < 0 or x >= m or y >= n or grid[x][y] != letter or (x, y) in area:
            return
        area.append((x, y))
        for dx, dy in directions:
            dfs(x + dx, y + dy, letter, area)

    areas = []

    for i in range(m):
        for j in range(n):
            if grid[i][j] != 'B' and not any((i, j) in area for area in areas):
                area = []
                dfs(i, j, grid[i][j], area)
                areas.append(area)

    # Erzeuge die Hintergrundfläche
    area_strings = []

    background = []
    for i in range(m):
        background.append([])
        for j in range(n):
            if grid[i][j] == 'B':
                background[i].append('#')
            else:
                background[i].append('.')
    area_strings.append('\n'.join(''.join(line) for line in background))

    # Speichere die Flächen als Zeichenketten
    for area in areas:
        min_x = min(x for x, y in area)
        min_y = min(y for x, y in area)
        area_grid = [['.'] * (max(y for x, y in area) - min_y + 1) for _ in range(max(x for x, y in area) - min_x + 1)]
        for (x, y) in area:
            area_grid[x - min_x][y - min_y] = '#'
        area_strings.append('\n'.join(''.join(line) for line in area_grid))

    # Erstelle einen Zähler für jede Form und weise jeder Form einen eindeutigen Namen zu
    area_counter = {}
    area_names = {}
    for area in area_strings:
        if area not in area_counter:
            area_counter[area] = 1
            area_names[area] = generate_random_name()
        else:
            area_counter[area] += 1

    # Drucke die Häufigkeit, den Namen und die Form jeder Fläche
    for area in area_counter:
        print("-" * 30)
        print('Häufigkeit:', area_counter[area])
        print('Name:', area_names[area])
        print(area)
        print("-" * 30)

    # Erstelle den gewünschten Ausgabestring
    output = 'p pack\n' + str(n) + ' ' + str(m) + '\n'
    for area in area_counter:
        output += str(area_counter[area]) + ' ' + area_names[area] + '\n'
        output += area + '\n%%%\n'

    #print(output)

    return output


def identify_and_print_areas(text):
    # Convertiere Text in 2D-Array
    lines = text.split('\n')
    grid = [list(line) for line in lines]

    # Definiere Größe der Karte
    m = len(grid)
    n = len(grid[0])

    # Definiere Richtungen für die Tiefensuche (oben, unten, links, rechts)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def dfs(x, y, letter, area):
        if x < 0 or y < 0 or x >= m or y >= n or grid[x][y] != letter or (x, y) in area:
            return
        area.append((x, y))
        for dx, dy in directions:
            dfs(x + dx, y + dy, letter, area)

    areas = []

    for i in range(m):
        for j in range(n):
            if grid[i][j] != 'B' and not any((i, j) in area for area in areas):
                area = []
                dfs(i, j, grid[i][j], area)
                areas.append(area)

    # Erzeuge die Hintergrundfläche
    area_strings = []

    background = []
    for i in range(m):
        background.append([])
        for j in range(n):
            if grid[i][j] == 'B':
                background[i].append('#')
            else:
                background[i].append('.')
    area_strings.append('\n'.join(''.join(line) for line in background))

    # Speichere die Flächen als Zeichenketten
    for area in areas:
        min_x = min(x for x, y in area)
        min_y = min(y for x, y in area)
        area_grid = [['.'] * (max(y for x, y in area) - min_y + 1) for _ in range(max(x for x, y in area) - min_x + 1)]
        for (x, y) in area:
            area_grid[x - min_x][y - min_y] = '#'
        area_strings.append('\n'.join(''.join(line) for line in area_grid))

    # Erstelle einen Zähler für jede Form und weise jeder Form einen eindeutigen Namen zu
    area_counter = {}
    area_names = {}
    for area in area_strings:
        if area not in area_counter:
            area_counter[area] = 1
            area_names[area] = generate_random_name()
        else:
            area_counter[area] += 1

    # Drucke die Häufigkeit, den Namen und die Form jeder Fläche
    for area in area_counter:
        print("-" * 30)
        print('Häufigkeit:', area_counter[area])
        print('Name:', area_names[area])
        print(area)
        print("-" * 30)

    # Erstelle den gewünschten Ausgabestring
    output = 'p pack\n' + str(n) + ' ' + str(m) + '\n'
    for area in area_counter:
        output += str(area_counter[area]) + ' ' + area_names[area] + '\n'
        output += area + '\n%%%\n'

    #print(output)

    return output

def process_img_bench_files3(input_directory):
    # Erstelle den Ausgabeverzeichnisnamen, indem du '-benchmark' an den Verzeichnisnamen anhängst
    output_directory = input_directory + '-benchmark'

    # Erstelle das Ausgabeverzeichnis, falls es noch nicht existiert
    os.makedirs(output_directory, exist_ok=True)

    # Durchlaufe alle Dateien im Eingabeverzeichnis
    for filename in os.listdir(input_directory):
        # Stelle sicher, dass es sich um eine Textdatei handelt
        if filename.endswith('.txt'):
            # Öffne die Datei und lese den Text ein
            with open(os.path.join(input_directory, filename), 'r') as file:
                text = file.read()

            # Rufe die identify_and_print_areas Funktion auf und erhalte den Ausgabestring
            output = identify_and_print_areas3(text)

            # Speichere den Ausgabestring in der Ausgabedatei
            with open(os.path.join(output_directory, filename), 'w') as output_file:
                output_file.write(output)
    print(f"{output_directory} bench done")

def process_img_bench_files(input_directory):
    # Erstelle den Ausgabeverzeichnisnamen, indem du '-benchmark' an den Verzeichnisnamen anhängst
    output_directory = input_directory + '-benchmark'

    # Erstelle das Ausgabeverzeichnis, falls es noch nicht existiert
    os.makedirs(output_directory, exist_ok=True)

    # Durchlaufe alle Dateien im Eingabeverzeichnis
    for filename in os.listdir(input_directory):
        # Stelle sicher, dass es sich um eine Textdatei handelt
        if filename.endswith('.txt'):
            # Öffne die Datei und lese den Text ein
            with open(os.path.join(input_directory, filename), 'r') as file:
                text = file.read()

            # Rufe die identify_and_print_areas Funktion auf und erhalte den Ausgabestring
            output = identify_and_print_areas(text)

            # Speichere den Ausgabestring in der Ausgabedatei
            with open(os.path.join(output_directory, filename), 'w') as output_file:
                output_file.write(output)
    print(f"{output_directory} bench done")


def create_text_bench2():
    process_img_bench_files('Gen7-withframe-colored-txt-tmp')

def create_text_bench3(folderprefix):
    process_img_bench_files3(folderprefix+'-withframe-colored-txt-tmp')

def create_text_bench():
    process_img_bench_files('Gen7-withframe-colored-txt-tmp')
    process_img_bench_files('Gen8-withframe-colored-txt-tmp')
    process_img_bench_files('Gen8-new-withframe-colored-txt-tmp')
    process_img_bench_files('inventory-withframe-colored-txt-tmp')
    process_img_bench_files('misc-withframe-colored-txt-tmp')


def check_file_existence(source_folder, target_folder):
    # Get list of file names (without extension) in source folder
    source_files = [Path(file).stem for file in os.listdir(source_folder) if file.endswith('.png')]
    # Get list of file names (without extension) in target folder
    target_files = [Path(file).stem for file in os.listdir(target_folder) if file.endswith('.txt')]

    # Check which files are missing in the target folder
    missing_files = set(source_files) - set(target_files)

    if missing_files:
        print(f"Missing files in {target_folder}:\n")
        for file in missing_files:
            print(f"{file}.png")
    else:
        print(f"All files in {source_folder} have a corresponding text file in {target_folder}.")


def test_benchmark_creation():
    # Teste die Funktion mit Ihrem Eingabetext
    text = """AAB
    ADC
    AAA"""

    identify_and_print_areas(text)

    text = """BBBBBBBBBBBBBBBBBBBBBBBBBBBBB
BBBBBBBBBBBBBBBBBBBBBBBBBBBBB
BBBBBBBBJBBBBBBBBBBBBBBBBBBBB
BBBBBBBBJJIIIBBBBBBBBBBBBPBBB
BBBBBBBJJJJJIBBBBBBBBBBBDDBBB
BBBBBBJJJNJNNBBBBBIIBBKKDIBBB
BBBBBBBJINNNPBBPJBIPHKHHKKIBB
BBBBBBBBPINNPJJPJPPPLLLHKHKBB
BBBBBBBIPJIPPJPPPCCJPPLHHNBBB
BBBBBKKBPPIPPPPBBPCPPJPPIHBBB
BBBBBIKBKPJPPCCJPJJCPPPIHIHBB
BBBBBBIIBMKPJPPPPPPCPJIIHHBBB
BBBBBBKKBMPPPPJPPKJPPPPPIBBBB
BBBBBBBBPJPPJBMPPPGBPPJIHHBBB
BBBBBBPJPPPPMMMPFJPKPPPPIBBBB
BBBBBBIPKPJKPPPPPPPPIKKJBBBBB
BBBBBBBPJJOAPPKPKPIPPIKKKBBBB
BBBBBPPIIKOOAPJPJPPIIKKJIBBBB
BBBPKPPPIKKKAAKJKIIPPIKKBBBBB
BBBBJPJPIKJKJKKKKKJPPIIBBBBBB
BBBEIIEIJIJJJKJKJKJPPPBBBBBBB
BBBEEEEINNIKJJKJJKJPPPBBBBBBB
BBEIHEEBBNNIBKKKKIPPPPPBBBBBB
BBBIEBBBBBBBBBBBKIPJPJPBBBBBB
BBBBBBBBBBBBBBBBBIEEEEBBBBBBB
BBBBBBBBBBBBBBBBBBIHEHEBBBBBB
BBBBBBBBBBBBBBBBBBBEBBEBBBBBB
BBBBBBBBBBBBBBBBBBBBBBBBBBBBB
BBBBBBBBBBBBBBBBBBBBBBBBBBBBB"""
    identify_and_print_areas(text)


def add_border2(input_image_path, output_image_path):
    img = Image.open(input_image_path)
    img = crop_transparency(img)

    img_with_border = Image.new('RGBA', (img.width + 2, img.height + 2), (0, 0, 0, 0))
    img_with_border.paste(img, (1, 1))

    img_with_border.save(output_image_path)
    img.save(output_image_path)


def process_images2(original_folder, new_folder):
    if not os.path.exists(new_folder):
        os.makedirs(new_folder)

    for filename in os.listdir(original_folder):
        if filename.endswith('.png'):
            add_border2(os.path.join(original_folder, filename), os.path.join(new_folder, filename))

    print(f"{original_folder} {new_folder} process images done")


def modify_images2():
    process_images2('Gen7', 'Gen7-withframe')

def modify_images3(folderprefix):
    process_images2(folderprefix, folderprefix + '-withframe')

def run2():
    #download_folders2()
    modify_images2()
    modify_color2()
    create_text_files2()
    create_text_bench2()

def run3():
    folderprefix = "mixed-6"
    #download_folders2()
    modify_images3(folderprefix)
    modify_color3(folderprefix)
    create_text_files3(folderprefix)
    create_text_bench3(folderprefix)

def run():


    download_folders()
    modify_images()
    modify_color()
    create_text_files()
    create_text_bench()


    # Use the function
    source_folder = 'Gen7-withframe-colored-txt-tmp'
    target_folder = 'Gen7-withframe-colored-txt-tmp-benchmark'
    #check_file_existence(source_folder, target_folder)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    run3()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
