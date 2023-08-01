from flask import Flask, render_template, request, jsonify
from PIL import Image, ImageDraw
import svgwrite
import time
import os

app = Flask(__name__)
grid_data = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update_grid', methods=['POST'])
def update_grid():
    global grid_data
    grid_data = request.json['grid']
    return 'Success', 200

@app.route('/save_image', methods=['GET'])
def save_image():
    global grid_data
    cell_size = 40

    rows = len(grid_data)
    cols = len(grid_data[0]) if rows > 0 else 0

    min_row = min((row for row in range(rows) if any(grid_data[row])), default=0)
    max_row = max((row for row in range(rows) if any(grid_data[row])), default=0)
    min_col = min((col for col in range(cols) if any(grid_data[row][col] for row in range(rows))), default=0)
    max_col = max((col for col in range(cols) if any(grid_data[row][col] for row in range(rows))), default=0)

    # For PNG Image
    width = (max_col - min_col + 1) * cell_size + 1
    height = (max_row - min_row + 1) * cell_size + 1
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    for row in range(min_row, max_row+1):
        for col in range(min_col, max_col+1):
            if grid_data[row][col] == 1:
                x1 = (col - min_col) * cell_size
                y1 = (row - min_row) * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                draw.rectangle([(x1, y1), (x2, y2)], outline="black")
    image.save(f'output_{int(time.time()*1000)}.png')

    # For SVG Image
    svg_width = (max_col - min_col + 1) * cell_size + 1
    svg_height = (max_row - min_row + 1) * cell_size + 1
    dwg = svgwrite.Drawing(f'output_{int(time.time()*1000)}.svg', profile='tiny', size=(svg_width, svg_height))
    for row in range(min_row, max_row+1):
        for col in range(min_col, max_col+1):
            if grid_data[row][col] == 1:
                x1 = (col - min_col) * cell_size
                y1 = (row - min_row) * cell_size
                dwg.add(dwg.rect((x1, y1), (cell_size, cell_size), stroke='black', fill='none'))
    dwg.save()

    return jsonify({'filename': 'Files saved'})


@app.route('/update_grid_with_border', methods=['POST'])
def update_grid_with_border():
    global grid_data
    grid_data = request.json['grid']
    return 'Success', 200


@app.route('/save_image_with_border', methods=['GET'])
def save_image_with_border():
    global grid_data
    cell_size = 40

    # Remove empty rows at the bottom
    while not any(grid_data[-1]):
        grid_data.pop()

    # Remove empty columns at the right
    while not any(row[-1] for row in grid_data):
        for row in grid_data:
            row.pop()

    rows = len(grid_data)
    cols = len(grid_data[0]) if rows > 0 else 0

    # Hier setzen wir min_row und min_col auf 0, um den Rand links und oben zu behalten
    min_row = 0
    min_col = 0
    max_row = rows - 1
    max_col = cols - 1

    # For PNG Image
    width = (max_col - min_col + 1) * cell_size + 1
    height = (max_row - min_row + 1) * cell_size + 1
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    for row in range(min_row, max_row + 1):
        for col in range(min_col, max_col + 1):
            if grid_data[row][col] == 1:
                x1 = (col - min_col) * cell_size
                y1 = (row - min_row) * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                draw.rectangle([(x1, y1), (x2, y2)], outline="black")
    image.save(f'output_{int(time.time() * 1000)}.png')

    # For SVG Image
    svg_width = (max_col - min_col + 1) * cell_size + 1
    svg_height = (max_row - min_row + 1) * cell_size + 1
    dwg = svgwrite.Drawing(f'output_{int(time.time() * 1000)}.svg', profile='tiny', size=(svg_width, svg_height))
    for row in range(min_row, max_row + 1):
        for col in range(min_col, max_col + 1):
            if grid_data[row][col] == 1:
                x1 = (col - min_col) * cell_size
                y1 = (row - min_row) * cell_size
                dwg.add(dwg.rect((x1, y1), (cell_size, cell_size), stroke='black', fill='none'))
    dwg.save()

    return jsonify({'filename': 'Files saved with border'})


if __name__ == '__main__':
    app.run(debug=True, port=5002)
