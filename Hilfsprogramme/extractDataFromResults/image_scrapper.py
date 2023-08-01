import re


class Image:
    def __init__(self, image_folder=None, all_pixels=None, total_pixels=None, result_CC_termination=None):
        self.image_folder = image_folder
        self.all_pixels = all_pixels
        self.total_pixels = total_pixels
        self.result_CC_termination = result_CC_termination

    def __str__(self):
        return f"Image: image_folder={self.image_folder}, all_pixels={self.all_pixels}, total_pixels={self.total_pixels}, result_CC_termination={self.result_CC_termination}"

    @staticmethod
    def process(filepath):
        image_folder = None
        all_pixels = None
        total_pixels = None
        result_CC_termination = None
        with open(filepath, 'r') as f:
            for line in f:
                if "DEBUG: created folder" in line:
                    match = re.search(r"DEBUG: created folder : (?P<image_folder>.+)", line)
                    if match:
                        image_folder = match.group('image_folder')
                elif "DEBUG: allPixels" in line:
                    match = re.search(r"DEBUG: allPixels\s+=\s+(?P<all_pixels>\d+)", line)
                    if match:
                        all_pixels = int(match.group('all_pixels'))
                elif "DEBUG: totalPixel" in line:
                    match = re.search(r"DEBUG: totalPixel\s+=\s+(?P<total_pixels>\d+)", line)
                    if match:
                        total_pixels = int(match.group('total_pixels'))
                elif "DEBUG: p_res" in line:
                    match = re.search(r"DEBUG: p_res\s+(?P<result_CC_termination>-?\d+)", line)
                    if match:
                        result_CC_termination = int(match.group('result_CC_termination'))

        if image_folder is not None:
            return Image(image_folder, all_pixels, total_pixels, result_CC_termination)

