import argparse
from PIL import Image, ImageDraw, ImageFont

def main() -> None:
    step_count = 25
    height = 600
    width = 600

    parser = argparse.ArgumentParser()
    parser.add_argument("width", help="width of image in pixels",
                        type=int)
    parser.add_argument("height", help="height of image in pixels",
                        type=int)
    parser.add_argument("step_count", help="how many steps across the grid",
                        type=int)
    args = parser.parse_args()

    step_count = args.step_count
    height = args.height
    width = args.width

    image = Image.new(mode='L', size=(width, height), color=255)

    # Draw a grid
    draw = ImageDraw.Draw(image)
    y_start = 0
    y_end = image.height
    step_size = int(image.width / step_count)

    # font = ImageFont.truetype(<font-file>, <font-size>)
    fontsize = 10
    font = ImageFont.truetype("/usr/share/fonts/truetype/quicksand/Quicksand-Light.ttf", fontsize)


    for x in range(0, image.width, step_size):
        if (x != 0):
            line = ((x, y_start), (x, y_end))
            draw.line(line, fill=128)
            print("v :(" + str(x) + "," + str(y_start) + ")")

            textToDraw = str(int(x / step_size) - 1)
            # draw.text((x, y),"Sample Text",(r,g,b))
            halfwidth = (step_size - fontsize) / 2
            halfheight = (step_size - fontsize) / 2
            draw.text((x + halfwidth, y_start + halfheight), textToDraw, 0, font=font)
            #draw.text((x, y_start ), textToDraw, 0)

    x_start = 0
    x_end = image.width

    for y in range(0, image.height, step_size):
        if (y != 0):
            line = ((x_start, y), (x_end,y))
            draw.line(line, fill=128)
            print("h :(" + str(x_start) + "," + str(y) + ")")


            textToDraw = str(int(y / step_size) - 1)
            # draw.text((x, y),"Sample Text",(r,g,b))
            halfwidth = (step_size - fontsize) / 2
            halfheight = (step_size - fontsize) / 2
            draw.text((x_start + halfwidth, y + halfheight), textToDraw, 0, font=font)
            #draw.text((x, y_start ), textToDraw, 0)


    del draw

    #image.show()
    filename = "grid-{}-{}-{}.png".format(width, height, step_count)
    print("Saving {}".format(filename))
    image.save(filename)



if __name__ == "__main__":
    main()
