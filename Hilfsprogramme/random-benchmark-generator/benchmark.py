import random
import string


class Benchmark:
    def __init__(self, width, height, shapes):
        self.width = width
        self.height = height
        self.shapes = shapes

    def __str__(self):
        result = ["p pack", f"{self.width} {self.height}"]
        for shape, count in self.shapes.items():
            uid = "".join(random.choices(string.ascii_letters, k=4))
            result.append(f"{count} {uid}")
            result.append(str(shape))
            result.append("%%%")
        return "\n".join(result)