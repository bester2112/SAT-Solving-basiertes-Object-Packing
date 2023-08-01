def compute_overlap_matrix(board_width, board_height, shape_width, shape_height):
    overlap_matrix = [[0 for _ in range(board_width)] for _ in range(board_height)]

    for i in range(board_height):
        for j in range(board_width):
            for x in range(max(0, i - shape_height + 1), min(board_height - shape_height + 1, i + 1)):
                for y in range(max(0, j - shape_width + 1), min(board_width - shape_width + 1, j + 1)):
                    overlap_matrix[i][j] += 1
    return overlap_matrix

def compute_new_matrix(matrix):
    return [[k * (k - 1) // 2 for k in row] for row in matrix]

def compute_sum(matrix):
    return sum(sum(row) for row in matrix)

def main(n):
    shape_width = shape_height = n
    board_width = 2 * shape_width
    board_height = 2 * shape_height

    overlap_matrix = compute_overlap_matrix(board_width, board_height, shape_width, shape_height)
    new_matrix = compute_new_matrix(overlap_matrix)

    # Auskommentierte Ausgabe
    # print("Variable:")
    # for row in overlap_matrix:
    #     print(row)
    # print("Summe Variablen: ", compute_sum(overlap_matrix))

    # print("\nKlauseln:")
    # for row in new_matrix:
    #     print(row)
    # print("Summe Klauseln: ", compute_sum(new_matrix))

    return shape_width, compute_sum(overlap_matrix), compute_sum(new_matrix)

def print_results(max_n):
    print("[n], [Summe Variablen], [Summe Klauseln]")
    for n in range(1, max_n + 1):
        shape_width, sum_vars, sum_clauses = main(n)
        print(f"{shape_width}, {sum_vars}, {sum_clauses}")

if __name__ == "__main__":
    max_n = 1000  # Hier können Sie die maximale Anzahl der berechneten n-Werte festlegen
    print_results(max_n)
