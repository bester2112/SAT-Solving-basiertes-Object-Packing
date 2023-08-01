# Declare variables for each node and each color
variables = []
colors = ['red', 'blue', 'green']
for node in ['u', 'v', 'w', 'x', 'y']:
    for color in colors:
        variables.append(f"{node}_{color}")

# Declare clauses for each node
clauses = []
for node in ['u', 'v', 'w', 'x', 'y']:
    # Each node must have exactly one color
    clause = [f"{node}_{color}" for color in colors]
    clauses.append(clause)
    for color1 in colors:
        for color2 in colors:
            if color1 != color2:
                # Two nodes cannot have the same color
                clauses.append([f"-{node}_{color1}", f"-{node}_{color2}"])

# Declare clauses for each edge
edges = [('u', 'w'), ('u', 'v'), ('w', 'x'), ('w', 'y'), ('v', 'y'), ('y', 'x')]
for edge in edges:
    node1, node2 = edge
    for color in colors:
        # Adjacent nodes cannot have the same color
        clauses.append([f"-{node1}_{color}", f"-{node2}_{color}"])

# Write the clauses to the CNF file
with open('../graph_coloring.cnf', 'w') as f:
    f.write(f"p cnf {len(variables)} {len(clauses)}\n")
    for clause in clauses:
        f.write(' '.join(clause) + ' 0\n')