from PIL import Image


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

    # Speichern in der Textdatei
    with open("output.txt", "w") as file:
        file.write(output_str)


image_to_text("images_done/9x10OneSided.GIF")
