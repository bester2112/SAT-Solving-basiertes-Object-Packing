import os
import cv2
import numpy as np
from glob import glob
import concurrent.futures


class MaskApplier:
    def __init__(self):
        pass

    def apply_mask(self, image, mask_image):
        height, width = mask_image.shape[:2]

        if len(mask_image.shape) < 3 or mask_image.shape[2] != 4:
            mask_b, mask_g, mask_r = cv2.split(mask_image)
            mask_alpha = 255 * np.ones_like(mask_b)
            mask_image = cv2.merge((mask_b, mask_g, mask_r, mask_alpha))

        if len(image.shape) < 3 or image.shape[2] != 4:  # Add alpha channel if not present
            if len(image.shape) == 2:
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGBA)
            else:
                b, g, r = cv2.split(image)
                alpha = 255 * np.ones_like(b)
                image = cv2.merge((b, g, r, alpha))

        result = image.copy()

        for y in range(height):
            for x in range(width):
                if mask_image[y, x, 3] == 0:  # Check if the mask_image pixel is transparent
                    result[y, x, 3] = 0  # Make the result image pixel transparent

        return result

    def process_images(self, input_folder, mask_folder, output_folder):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        image_files = sorted(glob(os.path.join(input_folder, "*.png")) + glob(os.path.join(input_folder, "*.jpg")))
        mask_files = sorted(glob(os.path.join(mask_folder, "*.png")) + glob(os.path.join(mask_folder, "*.jpg")))

        for image_file, mask_file in zip(image_files, mask_files):
            print(f"Mask Applier Bild: {image_file}")
            image = cv2.imread(image_file, cv2.IMREAD_UNCHANGED)
            mask_image = cv2.imread(mask_file, cv2.IMREAD_UNCHANGED)
            result = self.apply_mask(image, mask_image)
            output_file = os.path.join(output_folder, os.path.basename(image_file))
            cv2.imwrite(output_file, result)

    def process_images_parallel(self, input_folder, mask_folder, output_folder):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        image_files = sorted(glob(os.path.join(input_folder, "*.png")) + glob(os.path.join(input_folder, "*.jpg")))
        mask_files = sorted(glob(os.path.join(mask_folder, "*.png")) + glob(os.path.join(mask_folder, "*.jpg")))

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for image_file, mask_file in zip(image_files, mask_files):
                print(f"Mask Applier Bild: {image_file}")
                image = cv2.imread(image_file, cv2.IMREAD_UNCHANGED)
                mask_image = cv2.imread(mask_file, cv2.IMREAD_UNCHANGED)
                futures.append(executor.submit(self.apply_mask, image, mask_image))

            for future, image_file in zip(concurrent.futures.as_completed(futures), image_files):
                result = future.result()
                output_file = os.path.join(output_folder, os.path.basename(image_file))
                cv2.imwrite(output_file, result)