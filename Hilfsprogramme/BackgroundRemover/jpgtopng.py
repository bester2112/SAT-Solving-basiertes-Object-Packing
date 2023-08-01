import os
from PIL import Image
import concurrent.futures


class JPGToPNG:
    def __init__(self, input_folder, output_folder):
        self.input_folder = input_folder
        self.output_folder = output_folder

    def save_as_png(self, input_path, output_path):
        img = Image.open(input_path)
        img.save(output_path, "PNG")

    def process_images(self):
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        sorted_files = sorted(os.listdir(self.input_folder))

        for file in sorted_files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                print(f"JPG To PNG Bild: {file}")
                input_path = os.path.join(self.input_folder, file)
                output_path = os.path.join(self.output_folder, file.split('.')[0] + '.png')
                self.save_as_png(input_path, output_path)

    def process_images_parallel(self):
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        sorted_files = sorted(os.listdir(self.input_folder))

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for file in sorted_files:
                if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    print(f"JPG To PNG Bild: {file}")
                    input_path = os.path.join(self.input_folder, file)
                    output_path = os.path.join(self.output_folder, file.split('.')[0] + '.png')
                    futures.append(executor.submit(self.save_as_png, input_path, output_path))

            for future in concurrent.futures.as_completed(futures):
                future.result()