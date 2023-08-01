class Shape:
    def __init__(self, grid):
        self.grid = grid
        self.number_of_hashes = sum(row.count(1) for row in self.grid)
        self.remove_empty_rows_and_columns()

    def remove_empty_rows_and_columns(self):
        # Leere Zeilen entfernen
        self.grid = [row for row in self.grid if any(cell == 1 for cell in row)]

        # Leere Spalten entfernen
        if self.grid:
            empty_columns = {i for i in range(len(self.grid[0])) if all(row[i] == 0 for row in self.grid)}
            self.grid = [[cell for j, cell in enumerate(row) if j not in empty_columns] for row in self.grid]

    def __str__(self):
        result = []
        for row in self.grid:
            result.append("".join(["#" if cell == 1 else "." for cell in row]))
        return "\n".join(result)

    def __eq__(self, other):
        if isinstance(other, Shape):
            return self.grid == other.grid
        return False

    def __hash__(self):
        return hash(tuple(map(tuple, self.grid)))