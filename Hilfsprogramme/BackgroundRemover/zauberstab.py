import os
import cv2
import numpy as np
from glob import glob
import concurrent.futures


class Zauberstab:
    def __init__(self, toleranz, kontinuierlich, muster, anti_aliasing):
        self.toleranz = toleranz
        self.kontinuierlich = kontinuierlich
        self.muster = muster
        self.anti_aliasing = anti_aliasing

    def loesche_ausgewaehlte_pixel(self, image, x, y):
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        clicked_pixel = hsv_image[y, x]

        lower_bound = np.array(
            [clicked_pixel[0] - self.toleranz, clicked_pixel[1] - self.toleranz, clicked_pixel[2] - self.toleranz])
        upper_bound = np.array(
            [clicked_pixel[0] + self.toleranz, clicked_pixel[1] + self.toleranz, clicked_pixel[2] + self.toleranz])

        mask = cv2.inRange(hsv_image, lower_bound, upper_bound)

        if self.kontinuierlich:
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2:]
            for i, contour in enumerate(contours):
                if cv2.pointPolygonTest(contour, (x, y), False) >= 0:
                    cv2.drawContours(mask, contours, i, 255, -1)  # Use the current contour index instead of 0
                    break
            else:
                return image

        if self.anti_aliasing:
            mask = cv2.GaussianBlur(mask, (5, 5), 0)

        result = cv2.bitwise_and(image, image, mask=cv2.bitwise_not(mask))

        # Update alpha channel based on the mask to make the black areas transparent
        b, g, r, _ = cv2.split(result)  # Change this line
        alpha = cv2.bitwise_not(mask)
        result = cv2.merge((b, g, r, alpha))

        return result

    def bearbeite_bilder(self, input_folder, output_folder, x, y):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        image_files = sorted(glob(os.path.join(input_folder, "*.png")) + glob(os.path.join(input_folder, "*.jpg")))

        for image_file in image_files:
            print(f"Zauberstab Bild: {image_file}")
            output_file = os.path.join(output_folder, os.path.basename(image_file))
            image = cv2.imread(image_file, cv2.IMREAD_UNCHANGED)  # Read image with alpha channel
            cv2.imwrite(output_file, image)
            if len(image.shape) == 2 or image.shape[2] != 4:  # Add alpha channel if not present
                image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
            result = self.loesche_ausgewaehlte_pixel(image, x, y)
            output_file = os.path.join(output_folder, os.path.basename(image_file))
            cv2.imwrite(output_file, result)