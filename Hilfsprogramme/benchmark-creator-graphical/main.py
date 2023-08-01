import random
import string
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_matrix', methods=['POST'])
def get_matrix():
    matrix = request.get_json()
    result = process_matrix(matrix)
    return jsonify(result)

def process_matrix(matrix):
    # Find the bounds of the object
    min_x, max_x, min_y, max_y = find_bounds(matrix)

    output = ""
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            output += "#" if matrix[x][y] else "."
        output += "\n"
    return output.strip()

def find_bounds(matrix):
    min_x, max_x, min_y, max_y = len(matrix[0]), 0, len(matrix), 0

    for y in range(len(matrix)):
        for x in range(len(matrix[y])):
            if matrix[x][y]:
                min_x = min(min_x, x)
                max_x = max(max_x, x)
                min_y = min(min_y, y)
                max_y = max(max_y, y)

    return min_x, max_x, min_y, max_y

def process_matrix(matrix):
    # Find the bounds of the object
    min_x, max_x, min_y, max_y = find_bounds(matrix)

    output = f"1 {random_name()}\n"
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            output += "#" if matrix[x][y] else "."
        output += "\n"
    output += "%%%"
    return output.strip()

def random_name(length=4):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))


if __name__ == '__main__':
    app.run(debug=True, port=5004)
