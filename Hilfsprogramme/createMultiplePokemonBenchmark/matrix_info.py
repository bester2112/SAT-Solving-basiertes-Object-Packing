class MatrixInfo:
    def __init__(self, matrix, file_name, width, height, trimmed_matrix=None, trimmed_width=None, trimmed_height=None):
        self.matrix = matrix
        self.file_name = file_name
        self.width = width
        self.height = height
        self.trimmed_matrix = trimmed_matrix
        self.trimmed_width = trimmed_width
        self.trimmed_height = trimmed_height

    def __str__(self):
        string_representation = f"Dateiname: {self.file_name}\n" \
               f"Breite: {self.width}\n" \
               f"Höhe: {self.height}\n" \
               f"Matrix: \n{self.matrix}"

        if self.trimmed_matrix is not None:
            string_representation += f"\nGetrimmte Breite: {self.trimmed_width}\n" \
                                    f"Getrimmte Höhe: {self.trimmed_height}\n" \
                                    f"Getrimmte Matrix: \n{self.trimmed_matrix}"
        return string_representation

    def calculate_pixel_percentage(self, percentage_threshold):
        row_counts = []
        col_counts = []

        for row in self.matrix:
            row_counts.append(sum(row) / len(row))

        for col in self.matrix.T:
            col_counts.append(sum(col) / len(col))

        return row_counts, col_counts

    def get_trim_indices(self, percentage_threshold):
        row_counts, col_counts = self.calculate_pixel_percentage(percentage_threshold)

        left = next((i for i, x in enumerate(col_counts) if x > percentage_threshold), None)
        right = next((i for i, x in reversed(list(enumerate(col_counts))) if x > percentage_threshold), None)

        top = next((i for i, x in enumerate(row_counts) if x > percentage_threshold), None)
        bottom = next((i for i, x in reversed(list(enumerate(row_counts))) if x > percentage_threshold), None)

        return top, bottom, left, right

    def trim_sprite(self, percentage_threshold):
        top, bottom, left, right = self.get_trim_indices(percentage_threshold)
        print(top, bottom, left, right)

        if top is not None and bottom is not None and left is not None and right is not None:
            self.trimmed_matrix = self.matrix[top:bottom + 1, left:right + 1]
            self.trimmed_height, self.trimmed_width = self.trimmed_matrix.shape