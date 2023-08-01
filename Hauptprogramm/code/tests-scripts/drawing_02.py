import argparse
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import math


def createImage(xArg: int, yArg: int) -> None:
    if not isinstance(xArg, int) or not isinstance(yArg, int):
        raise TypeError
    if xArg == 0 or yArg == 0:
        raise SyntaxError

    step_count = 5
    # pixel size Y (so a pixel is YxY big)
    size = 100
    fontsize = 30
    height = 600
    width = 600

    #xArg = args.x
    #yArg = args.y
    step_count_x = xArg + 1
    step_count_y = yArg + 1

    width = (xArg + 1) * size
    height = (yArg + 1) * size

    image = Image.new(mode='L', size=(width, height), color=255)
    image = image.convert("RGB")

    # initialize drawing variables
    draw = ImageDraw.Draw(image)
    y_start = 0
    y_end = image.height
    step_size_width = int(image.width / step_count_x)
    step_size_height = int(image.height / step_count_y)

    # font = ImageFont.truetype(<font-file>, <font-size>)
    font = ImageFont.truetype("/usr/share/fonts/truetype/quicksand/Quicksand-Bold.ttf", fontsize)

    # draw rectangles
    xCoord = 100
    yCoord = 100
    shape = [(xCoord, yCoord), (xCoord + size, yCoord + size)]
    draw.rectangle(shape, fill=(255, 0, 0))
    xCoord = 200
    yCoord = 200
    shape = [(xCoord, yCoord), (xCoord + size, yCoord + size)]
    draw.rectangle(shape, fill=(0, 255, 0))

    # draw the grid
    for x in range(0, image.width, step_size_width):
        if (x != 0):
            line = ((x, y_start), (x, y_end))
            draw.line(line, fill=(0,0,0))
            print("v :(" + str(x) + "," + str(y_start) + ")")

            textToDraw = str(int(x / step_size_width) - 1)
            # draw.text((x, y),"Sample Text",(r,g,b))
            halfwidth = (step_size_width - fontsize) / 2
            halfheight = (step_size_height - fontsize) / 2
            draw.text((x + halfwidth, y_start + halfheight), textToDraw, 0, font=font)
            # draw.text((x, y_start ), textToDraw, 0)

    x_start = 0
    x_end = image.width

    for y in range(0, image.height, step_size_height):
        if (y != 0):
            line = ((x_start, y), (x_end, y))
            draw.line(line, fill=(0,0,0))
            print("h :(" + str(x_start) + "," + str(y) + ")")

            textToDraw = str(int(y / step_size_height) - 1)
            # draw.text((x, y),"Sample Text",(r,g,b))
            halfwidth = (step_size_width - fontsize) / 2
            halfheight = (step_size_height - fontsize) / 2
            draw.text((x_start + halfwidth, y + halfheight), textToDraw, 0, font=font)
            # draw.text((x, y_start ), textToDraw, 0)

    del draw


    # create file
    # image.show()
    filename = "grid-{}-{}-{}-{}.png".format(width, height, xArg, yArg)
    print("Saving {}".format(filename))
    image.save(filename)

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("x", help="max x coordinates",
                        type=int)
    parser.add_argument("y", help="max y coordinates",
                        type=int)
    args = parser.parse_args()

    createImage(args.x, args.y)

    #for i in range(1,11):
    #    if i != 0:
    #        for j in range(1,11):
    #            if j != 0:
    #                createImage(xArg=i, yArg=j)






if __name__ == "__main__":
    main()
