from PIL import Image
import math
import os
from PIL import ImageFilter


def is_power_of_two(n):
    return (n != 0) and (n & (n-1) == 0)


def next_power_of_two(n):
    return 2 ** math.ceil(math.log2(n))


def extend_image_to_power_of_two(img):
    width, height = img.size
    max_dimension = max(width, height)

    if not is_power_of_two(max_dimension):
        max_dimension = next_power_of_two(max_dimension)

    print(f"Max dimension: {max_dimension}")

    new_img = Image.new("RGBA", (max_dimension, max_dimension), (0, 0, 0, 0))
    new_img.paste(img, (0, 0))

    return new_img


def add_border2(input_image):
    img = crop_transparency(input_image)

    img_with_border = Image.new('RGBA', (img.width + 2, img.height + 2), (0, 0, 0, 0))
    img_with_border.paste(img, (1, 1))

    return img_with_border


def crop_transparency(image):
    image = image.convert("RGBA")

    mask = Image.new('L', image.size, 0)
    for i in range(image.width):
        for j in range(image.height):
            if image.getpixel((i, j))[-1] != 0:
                mask.putpixel((i, j), 255)

    bounds = mask.getbbox()
    if bounds:
        image = image.crop(bounds)

    return image


def create_black_version(image, path):
    img = image
    output_path = f"{path}-b.png"  # Fügen Sie '.png' zum Pfad hinzu

    data = list(img.getdata())
    new_data = []

    for pixel in data:
        r, g, b, a = pixel  # Hier ändern wir, um auch den Alpha-Wert zu berücksichtigen

        if r == 0 and g == 0 and b == 0 and a == 0:
            new_data.append((0, 0, 0, a))  # Hier fügen wir den Alpha-Wert zum neuen Pixel hinzu
        elif a < (255 / 2):
            new_data.append((r, g, b, 0))
        else:
            new_data.append((0, 0, 0, 255))  # Hier fügen wir den Alpha-Wert zum neuen Pixel hinzu

    new_img = Image.new(img.mode, img.size)
    new_img.putdata(new_data)
    new_img.save(output_path)


def create_mipmaps(img, path):
    base_name = os.path.splitext(os.path.basename(path))[0]
    directory = base_name

    if not os.path.exists(directory):
        os.makedirs(directory)

    size = img.size[0]
    while size > 1:
        img = add_border2(img)
        img.save(f"{directory}/{base_name}-{size}x{size}.png")
        create_black_version(img, f"{directory}/{base_name}-{size}x{size}")
        size = size // 2
        img = img.resize((max(size, 1), max(size, 1)), Image.LANCZOS)


def main(path_to_image):
    img = Image.open(path_to_image)
    img = extend_image_to_power_of_two(img)
    create_mipmaps(img, path_to_image)


if __name__ == "__main__":
    main("bellsprout.png")
