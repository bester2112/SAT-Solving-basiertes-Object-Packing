import os
from benchmarkGenerator import BenchmarkGenerator
from puzzleGenerator import PuzzleGenerator
from shape import Shape
from benchmark import Benchmark
from areaPlacer import AreaPlacer

def are_benchmarks_equal(benchmark1, benchmark2):
    if benchmark1.width != benchmark2.width or benchmark1.height != benchmark2.height:
        return False

    shapes1 = benchmark1.shapes
    shapes2 = benchmark2.shapes

    if len(shapes1) != len(shapes2):
        return False

    for shape1, count1 in shapes1.items():
        found = False
        for shape2, count2 in shapes2.items():
            if shape1 == shape2 and count1 == count2:
                found = True
                break
        if not found:
            return False
    return True

class Main:
    @staticmethod
    def shapes_with_less_hashes(benchmark, threshold):
        for shape, _ in benchmark.shapes.items():
            if shape.number_of_hashes < threshold:
                return True
        return False

    @staticmethod
    def count_shapes_with_one_hash(benchmark):
        count = 0
        for shape, _ in benchmark.shapes.items():
            if shape.number_of_hashes == 1:
                count += 1
        return count

    @staticmethod
    def shapes_within_hash_range(benchmark, min_threshold, max_threshold):
        for shape, _ in benchmark.shapes.items():
            if min_threshold <= shape.number_of_hashes <= max_threshold:
                return True
        return False

    @staticmethod
    def generate_benchmarks(x, y, z, w, num_files, minPixels, maxPixels):
        if not os.path.exists("benchmarks"):
            os.mkdir("benchmarks")

        for n in range(num_files):
            for i in range(max(x, z) - 1, max(x, z) + 1):
                for j in range(max(y, w) - 1, max(y, w) + 1):
                    benchmark = BenchmarkGenerator.generate_benchmark(x, y, i, j, minPixels, maxPixels)
                    with open(f"benchmarks/benchmark_{i}_{j}-{n}.txt", "w") as file:
                        file.write(str(benchmark))

    def generate_benchmarks2(x, y, z, w, num_files, minPixels, maxPixels):
        if not os.path.exists("benchmarks"):
            os.mkdir("benchmarks")

        puzzle_generator = PuzzleGenerator(minPixels, maxPixels)
        generated_benchmarks = set()

        for n in range(num_files):
            for i in range(max(x, z) - 1, max(x, z) + 1):
                for j in range(max(y, w) - 1, max(y, w) + 1):
                    area = i * j
                    shapes = puzzle_generator.generate_puzzle_pieces(x, y, area)
                    shape_counts = {shape: shapes.count(shape) for shape in set(shapes)}
                    benchmark = Benchmark(i, j, shape_counts)

                    # Prüfen, ob der Benchmark bereits erstellt wurde
                    is_duplicate = any(are_benchmarks_equal(benchmark, existing_benchmark) for existing_benchmark in
                                       generated_benchmarks)

                    # Wenn der Benchmark ein Duplikat ist, überspringen
                    if is_duplicate:
                        continue

                    generated_benchmarks.add(benchmark)

                    with open(f"benchmarks/benchmark_{i}_{j}-{n}.txt", "w") as file:
                        file.write(str(benchmark))

    @staticmethod
    def text_to_benchmark(text):
        lines = text.strip().split("\n")
        height = len(lines)
        width = len(lines[0])

        grid = [[ord(char) - ord('A') + 1 for char in line] for line in lines]
        shape_dict = {}
        for y in range(height):
            for x in range(width):
                shape_id = grid[y][x]
                if shape_id not in shape_dict:
                    shape_dict[shape_id] = []
                shape_dict[shape_id].append((x, y))

        shapes = {}
        for shape_id, coordinates in shape_dict.items():
            shape_grid = [[1 if (x, y) in coordinates else 0 for x in range(width)] for y in range(height)]
            shape = Shape(shape_grid)
            shapes[shape] = shapes.get(shape, 0) + 1

        benchmark = Benchmark(width, height, shapes)
        return benchmark

    @staticmethod
    def run():
        minX, maxX = 2, 20
        minY, maxY = 2, 20
        min_pixel = 5
        max_pixel = 5
        threshold = 4
        minThreshold = 2
        maxThreshold = 4
        maxOneHash = 1
        countPerBenchmark = 100
        maxFailsLimitReached = 0
        maxFailsLimitCount = 0
        maxFailsLimit = 50000
        maxFailsCount = 0
        generated_benchmarks = set()

        # Beispiel: Verwenden der text_to_benchmark Methode
        text = "UUXIIIIIZWWTTTFLLLLV\nUXXXPPZZZYWWTFFFNNLV\nUUXPPPZYYYYWTFNNNVVV"
        text = "FFIIIIIL\nVFFWLLLL\nVFAWWBZZ\nVVVXWWZN\nPPXXXZZN\nPPCXTDNN\nPYTTTUNU\nYYYYTUUU"
        text = "UUXPPPLLLLFTTTACCCCWWZZDDDEVVV\nUXXXPPLNNFFFTAAABBCYWWZDDGEEEV\nUUXIIIIINNNFTABBBYYYYWZZGGGGEV"
        benchmark = Main.text_to_benchmark(text)

        # Speichern des Benchmarks
        area_placer = AreaPlacer(benchmark.width, benchmark.height, 1, 1)
        area_placer.save_benchmark(benchmark.width, benchmark.height, benchmark.shapes, 1, "text_based", 1)



if __name__ == "__main__":
    Main.run()