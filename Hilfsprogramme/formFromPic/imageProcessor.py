import os
from PIL import Image

from imageStructure import ImageStructure


def image_to_text(image_path):
    img = Image.open(image_path)
    width, height = img.size
    pixels = img.load()

    # Liste aller einzigartigen Farben
    unique_colors = list(set([pixels[x, y] for x in range(width) for y in range(height)]))

    # Die Farben müssen weniger als die Länge des Alphabets sein
    assert len(unique_colors) <= 26, "Es gibt mehr Farben als Buchstaben im Alphabet"

    # Erstellt eine Zuordnung von Farben zu Buchstaben
    color_to_letter = {color: chr(65 + i) for i, color in enumerate(unique_colors)}

    # Erstellt die endgültige Zeichenkette
    output_str = ""
    for y in range(height):
        for x in range(width):
            output_str += color_to_letter[pixels[x, y]]
        output_str += "\n"

    # Rückgabe der generierten Zeichenkette
    return output_str


def convert_all_images():
    # Geht durch alle Bilder im Ordner "images"
    for image_file in os.listdir("images"):
        lowercase_name = image_file.lower()
        if lowercase_name.endswith(('.png', '.jpg', '.gif')):
            image_path = os.path.join("images", image_file)
            # Konvertiert das Bild in Text
            text = image_to_text(image_path)
            # Speichert die Textdatei im Ordner "text-img"
            filename = os.path.splitext(image_file)[0]  # Name der Datei ohne Endung
            with open(f"text-img/{filename}.txt", "w") as file:
                file.write(text)


def apply_algorithm_to_all_text_files():
    # Erstellt den Ordner "benchmark", falls er nicht existiert
    os.makedirs("benchmark", exist_ok=True)

    # Geht durch alle Textdateien im Ordner "text-img"
    for text_file in os.listdir("text-img"):
        if text_file.endswith('.txt'):
            text_path = os.path.join("text-img", text_file)
            # Erstellt eine Instanz von ImageStructure und wendet den Algorithmus an
            img_struct = ImageStructure(text_path)

            # Diese Methoden werden in der richtigen Reihenfolge aufgerufen, um die Daten zu initialisieren
            for index, midpoint in enumerate(img_struct.midpoints):
                print(f'Mittelpunkt bei {midpoint["pos"]} enthält: {midpoint["value"]}')
                print(f'Nord: {midpoint["N"]}, East: {midpoint["E"]}, Sout: {midpoint["S"]}, West: {midpoint["W"]}')
                print(
                    f'Neue Koordinaten: ({index % img_struct.blocks_in_width}, {index // img_struct.blocks_in_width})')
                print('-' * 50)
            img_struct.print_new_coord_system()
            for i, figure in enumerate(img_struct.figures):
                print(f'Figur {i + 1}:')
                for block in figure:
                    print(f'Block bei {block["pos"]}')
            img_struct.print_new_coord_system_with_figures()

            # Speichert die resultierende Datei im Ordner "benchmark"
            filename = os.path.splitext(text_file)[0]  # Name der Datei ohne Endung
            img_struct.write_to_file(f"benchmark/benchmark-{filename}.txt")
def apply_algorithm_to_all_text_files_new():
    os.makedirs("benchmark", exist_ok=True)
    for text_file in os.listdir("text-img"):
        if text_file.endswith('.txt'):
            text_path = os.path.join("text-img", text_file)
            img_struct = ImageStructure(text_path)

            for index, midpoint in enumerate(img_struct.midpoints):
                pass  # replace this line with whatever operations you need to perform on midpoints

            img_struct.print_new_coord_system()

            for i, figure in enumerate(img_struct.figures):
                pass  # replace this line with whatever operations you need to perform on figures

            img_struct.print_new_coord_system_with_figures()

            output_path = os.path.join("benchmark", text_file)
            img_struct.write_to_file(output_path)



def main():
    # Erstellt die Ordner "images" und "text-img", falls sie nicht existieren
    os.makedirs("images", exist_ok=True)
    os.makedirs("text-img", exist_ok=True)

    #convert_all_images()
    apply_algorithm_to_all_text_files_new()


if __name__ == '__main__':
    main()
