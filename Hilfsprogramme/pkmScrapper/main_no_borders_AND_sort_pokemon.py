import os
from PIL import Image, ImageChops
import numpy as np

def remove_transparency(im: Image.Image) -> Image.Image:
    if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):
        bg = Image.new('RGBA', im.size, (255, 255, 255, 255))
        alpha_composite = Image.alpha_composite(bg, im)
        grey = alpha_composite.convert('L')
        bbox = ImageChops.invert(grey).getbbox()

        if bbox:
            return im.crop(bbox)

    return im

def count_black_pixels(im: Image.Image) -> int:
    return np.sum(np.array(im.convert('L')) == 0)

def process_images(input_directory, output_directory):
    os.makedirs(output_directory, exist_ok=True)

    image_info = []

    for file in os.listdir(input_directory):
        if file.endswith(".png") or file.endswith(".jpg"):
            input_path = os.path.join(input_directory, file)
            output_path = os.path.join(output_directory, file)

            with Image.open(input_path) as img:
                img_no_transparency = remove_transparency(img)
                img_no_transparency.save(output_path)

                width, height = img_no_transparency.size
                black_pixels = count_black_pixels(img_no_transparency)
                image_info.append((file, width, height, black_pixels))

    image_info.sort(key=lambda x: x[3])  # Sortiert nach Anzahl der schwarzen Pixel

    return image_info[:100]  # Gibt die ersten 100 zurück

def main():
    input_directory = "Gen7-withframe-black"  # Ändern Sie dies in den Pfad zu Ihrem Ordner
    output_directory = input_directory + "_without_borders"
    image_info = process_images(input_directory, output_directory)

    for info in image_info:
        print(f"Dateiname: {info[0]}, Breite: {info[1]}, Höhe: {info[2]}, Schwarze Pixel: {info[3]}")

if __name__ == "__main__":
    main()
