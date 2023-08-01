import os
import sys
import random
import colorsys
import logging

from PIL import Image, ImageDraw, ImageFont

class ImageCreator:
    """
    ImageCreator

    The ImageCreator class is responsible for creating and saving images of empty grids and game boards for the game Pentominoes.

    Methods:
    - init(self, folderName:str)
    - createFolder(self, folder:str)
    - createSessionFolder(self, folder:str)
    - createImageFolder(self, defaultFolder:str, sessionName:str)
    - createEmptyFieldWithFilename(self, fieldWidth:int, fieldHeight:int, fileName:str)
    - createEmptyField(self, fieldWidth:int, fieldHeight:int)
    - createImgForSpielstein(self, fieldWidth:int, fieldHeight:int, fileName:str, folderName:str, elemList:[], color)
    - randomColor(self)
    - createImgForAllSpielsteine(self, fieldWidth:int, fieldHeight:int, fileName:str, folderName:str, elemMap)

    Attributes:
    - changeFileName (bool)
    - fileName (str)
    - folderName (str)

    """

    changeFileName: bool
    fileName: str

    def __init__(self, folderName:str):
        """
        Initializes an ImageCreator object.

        Args:
            folderName (str): The name of the folder where the image files will be saved.

        Raises:
            TypeError: If folderName is not a string.
            SyntaxError: If folderName is an empty string.

        Returns:
            None
        """

        if not isinstance(folderName, str):
            raise TypeError
        if folderName == "":
            raise SyntaxError

        self.folderName = folderName
        self.changeFileName = False
        self.fileName = ""

    def createFolder(self, folder):
        """
        Checks if a directory exists, and creates it if it doesn't.

        Args:
            folder (str): The name of the folder to check/create.

        Raises:
            None

        Returns:
            None
        """

        check_folder = os.path.isdir(folder)

        # If folder doesn't exists, then create it
        if not check_folder:
            os.makedirs(folder)
            logging.debug("created folder : " + str(folder))
        #else:
        #    logging.debug(str(folder) + " folder already exists.")

    def createSessionFolder(self, folder):
        """
       Creates a new folder within the specified folder to store image files.

       Args:
           folder (str): The name of the folder to create.

       Raises:
           None

       Returns:
           None
       """
        self.createFolder(folder)
        self.folderName = folder

    def createImageFolder(self, defaultFolder, sessionName):
        """
        Creates a new folder within a default folder to store image files.

        Args:
            defaultFolder (str): The name of the default folder.
            sessionName (str): The name of the session folder to create.

        Raises:
            None

        Returns:
            None
        """
        self.createFolder(defaultFolder)
        self.createSessionFolder(defaultFolder + sessionName + "/")

    def createEmptyFieldWithFilename(self, fieldWidth: int, fieldHeight: int, fileName:str):
        """
        Creates an empty grid image with a specified file name.

        Args:
            fieldWidth (int): The width of the grid.
            fieldHeight (int): The height of the grid.
            fileName (str): The name of the file to be created.

        Raises:
            TypeError: If fileName is not a string.
            SyntaxError: If fileName is an empty string.
            TypeError: If fieldWidth or fieldHeight is not an integer.
            SyntaxError: If fieldWidth or fieldHeight is equal to 0.

        Returns:
            None
        """
        if not isinstance(fileName, str):
            raise TypeError
        if fileName == "":
            raise SyntaxError
        self.changeFileName = True
        self.fileName = fileName
        self.createEmptyField(fieldWidth=fieldWidth, fieldHeight=fieldHeight)
        self.changeFileName = False
        self.fileName = ""

    def createEmptyField(self, fieldWidth: int, fieldHeight: int):
        """
        Creates an empty grid image.

        Args:
            fieldWidth (int): The width of the grid.
            fieldHeight (int): The height of the grid.

        Raises:
            TypeError: If fieldWidth or fieldHeight is not an integer.
            SyntaxError: If fieldWidth or fieldHeight is equal to 0.

        Returns:
            None
        """
        if not isinstance(fieldWidth, int) or not isinstance(fieldHeight, int):
            raise TypeError
        if fieldWidth == 0 or fieldHeight == 0:
            raise SyntaxError

        # pixel size Y (so a pixel is YxY big)
        size = 100
        fontsize = 30

        step_count_x = fieldWidth + 1
        step_count_y = fieldHeight + 1

        width = step_count_x * size
        height = step_count_y * size

        image = Image.new(mode="L", size=(width, height), color=255)
        image = image.convert("RGB")

        # initialize drawing variables
        draw = ImageDraw.Draw(image)
        y_start = 0
        y_end = image.height
        step_size_width = int(image.width / step_count_x)
        step_size_height = int(image.height / step_count_y)

        font = ImageFont.truetype("quicksand/Quicksand-Bold.ttf", fontsize)

        # draw the grid
        for x in range(0, image.width, step_size_width):
            if (x != 0):
                line = ((x, y_start), (x, y_end))
                draw.line(line, fill=(0, 0, 0))
                #logging.debug("v :(" + str(x) + "," + str(y_start) + ")")

                textToDraw = str(int(x / step_size_width) - 1)
                halfwidth = (step_size_width - fontsize) / 2
                halfheight = (step_size_height - fontsize) / 2
                draw.text((x + halfwidth, y_start + halfheight), textToDraw, 0, font=font)

        x_start = 0
        x_end = image.width

        for y in range(0, image.height, step_size_height):
            if (y != 0):
                line = ((x_start, y), (x_end, y))
                draw.line(line, fill=(0, 0, 0))
                #logging.debug("h :(" + str(x_start) + "," + str(y) + ")")

                textToDraw = str(int(y / step_size_height) - 1)
                # draw.text((x, y),"Sample Text",(r,g,b))
                halfwidth = (step_size_width - fontsize) / 2
                halfheight = (step_size_height - fontsize) / 2
                draw.text((x_start + halfwidth, y + halfheight), textToDraw, 0, font=font)
                # draw.text((x, y_start ), textToDraw, 0)

        del draw

        # create file
        # image.show()
        actualFilename = ""
        if self.changeFileName:
            actualFilename = self.folderName + self.fileName
        else:
            actualFilename = self.folderName + "grid-empty-field-{}-{}-{}-{}.png".format(width, height, fieldWidth, fieldHeight)

        logging.debug("Saving {" + str(format(actualFilename)) + "}")
        image.save(actualFilename)

    def createImgForSpielstein(self, fieldWidth:int ,fieldHeight:int, fileName:str, folderName:str, elemList:[], color):
        """
        Creates an image file containing the given Spielstein elements.

        Args:
            fieldWidth (int): The width of the field.
            fieldHeight (int): The height of the field.
            fileName (str): The name of the output file.
            folderName (str): The name of the folder to save the output file in.
            elemMap (dict): A dictionary containing the Spielstein elements.

        Raises:
            TypeError: If fieldWidth or fieldHeight are not integers.
            SyntaxError: If fieldWidth or fieldHeight are 0.
            None

        Returns:
            None
        """

        #logging.debug("fieldWidth: " + str(fieldWidth))
        #logging.debug("fieldHeight: " + str(fieldHeight))
        #logging.debug("fileName: " + str(fileName))
        #logging.debug("folderName: " + str(folderName))
        #logging.debug("elemList: " + str(elemList))

        if not isinstance(fieldWidth, int) or not isinstance(fieldHeight, int):
            raise TypeError
        if fieldWidth == 0 or fieldHeight == 0:
            raise SyntaxError

        # pixel size Y (so a pixel is YxY big)
        size = 100
        fontsize = 30

        step_count_x = fieldWidth + 1
        step_count_y = fieldHeight + 1

        width = step_count_x * size
        height = step_count_y * size

        image = Image.new(mode="L", size=(width, height), color=255)
        image = image.convert("RGB")

        # initialize drawing variables
        draw = ImageDraw.Draw(image)
        y_start = 0
        y_end = image.height
        step_size_width = int(image.width / step_count_x)
        step_size_height = int(image.height / step_count_y)

        font = None
        #ImageFont.truetype("quicksand/Quicksand-Bold.ttf", fontsize)
        if sys.platform == "win32":
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)
            font_path = os.path.join(parent_dir, "quicksand", "Quicksand-Bold.ttf")
            font = ImageFont.truetype(font_path, fontsize)
        else:
            font = ImageFont.truetype("quicksand/Quicksand-Bold.ttf", fontsize)


        # draw the array
        for index in range(len(elemList)):
            array = elemList[index]
            positionX = (array[0] + 1) * size
            positionY = (array[1] + 1) * size
            #logging.debug("positionX: " + str(positionX))
            #logging.debug("positionY: " + str(positionY))

            shape = [(positionX, positionY), (positionX + size, positionY + size)]
            draw.rectangle(shape, fill=color)

        # draw the grid
        for x in range(0, image.width, step_size_width):
            if (x != 0):
                line = ((x, y_start), (x, y_end))
                draw.line(line, fill=(0, 0, 0))
                #logging.debug("v :(" + str(x) + "," + str(y_start) + ")")

                textToDraw = str(int(x / step_size_width) - 1)
                halfwidth = (step_size_width - fontsize) / 2
                halfheight = (step_size_height - fontsize) / 2
                draw.text((x + halfwidth, y_start + halfheight), textToDraw, 0, font=font)

        x_start = 0
        x_end = image.width

        for y in range(0, image.height, step_size_height):
            if (y != 0):
                line = ((x_start, y), (x_end, y))
                draw.line(line, fill=(0, 0, 0))
                #logging.debug("h :(" + str(x_start) + "," + str(y) + ")")

                textToDraw = str(int(y / step_size_height) - 1)
                # draw.text((x, y),"Sample Text",(r,g,b))
                halfwidth = (step_size_width - fontsize) / 2
                halfheight = (step_size_height - fontsize) / 2
                draw.text((x_start + halfwidth, y + halfheight), textToDraw, 0, font=font)
                # draw.text((x, y_start ), textToDraw, 0)

        del draw

        # create file
        # image.show()
        actualFilename = folderName + fileName

        logging.debug("Saving {" + str(format(actualFilename)) + "}")
        image.save(actualFilename)

    def randomColor(self):
        """
        Generate a random RGB color tuple.

        Args:
            None

        Raises:
            None

        Returns:
            tuple: A tuple containing the RGB color values.
        """

        red = random.randint(0, 255)
        green = random.randint(0, 255)
        blue = random.randint(0, 255)
        return (red, green, blue)

    def createImgForAllSpielsteine(self, fieldWidth: int, fieldHeight: int, fileName: str, folderName: str, elemMap):
        """
        Create an image for all Spielstein game pieces.

        Args:
            fieldWidth (int): The width of the game board.
            fieldHeight (int): The height of the game board.
            fileName (str): The name of the output image file.
            folderName (str): The name of the folder in which to save the output image file.
            elemMap (list): A list of the game board's elements.

        Raises:
            TypeError: If fieldWidth or fieldHeight are not integers.
            SyntaxError: If fieldWidth or fieldHeight are equal to 0.

        Returns:
            None
        """

        #logging.debug("fieldWidth: " + str(fieldWidth))
        #logging.debug("fieldHeight: " + str(fieldHeight))
        #logging.debug("fileName: " + str(fileName))
        #logging.debug("folderName: " + str(folderName))
        #logging.debug("elemList: " + str(elemMap))

        if not isinstance(fieldWidth, int) or not isinstance(fieldHeight, int):
            raise TypeError
        if fieldWidth == 0 or fieldHeight == 0:
            raise SyntaxError

        # pixel size Y (so a pixel is YxY big)
        size = 100
        fontsize = 30

        step_count_x = fieldWidth + 1
        step_count_y = fieldHeight + 1

        width = step_count_x * size
        height = step_count_y * size

        image = Image.new(mode="L", size=(width, height), color=255)
        image = image.convert("RGB")

        # initialize drawing variables
        draw = ImageDraw.Draw(image)
        y_start = 0
        y_end = image.height
        step_size_width = int(image.width / step_count_x)
        step_size_height = int(image.height / step_count_y)

        font = ImageFont.truetype("quicksand/Quicksand-Bold.ttf", fontsize)

        # TODO
        # Anzahl der Elemente im Wörterbuch ermitteln
        num_elements = len(elemMap)

        # Generiere visuell unterschiedliche Farben für jedes Element im Wörterbuch
        distinct_colors = self.get_combined_colors(num_elements)


        randColor = {}
        # draw the array
        for i, key in enumerate(elemMap):
            randColor__ = self.randomColor()
            randColor[key] = tuple(distinct_colors[i])
            #print("Stein " + str(key) + " has the color " + str(randColor))
            #logging.debug("Stein " + str(key) + " has the color " + str(randColor[key]))
            pixelList = elemMap[key]
            for pixel in pixelList:
                positionX = (pixel[0] + 1) * size
                positionY = (pixel[1] + 1) * size
                #logging.debug("positionX: " + str(positionX))
                #logging.debug("positionY: " + str(positionY))

                shape = [(positionX, positionY), (positionX + size, positionY + size)]
                draw.rectangle(shape, fill=randColor[key])

        # draw the grid
        for x in range(0, image.width, step_size_width):
            if (x != 0):
                line = ((x, y_start), (x, y_end))
                draw.line(line, fill=(0, 0, 0))
                #logging.debug("v :(" + str(x) + "," + str(y_start) + ")")

                textToDraw = str(int(x / step_size_width) - 1)
                halfwidth = (step_size_width - fontsize) / 2
                halfheight = (step_size_height - fontsize) / 2
                draw.text((x + halfwidth, y_start + halfheight), textToDraw, 0, font=font)

        x_start = 0
        x_end = image.width

        for y in range(0, image.height, step_size_height):
            if (y != 0):
                line = ((x_start, y), (x_end, y))
                draw.line(line, fill=(0, 0, 0))
                #logging.debug("h :(" + str(x_start) + "," + str(y) + ")")

                textToDraw = str(int(y / step_size_height) - 1)
                # draw.text((x, y),"Sample Text",(r,g,b))
                halfwidth = (step_size_width - fontsize) / 2
                halfheight = (step_size_height - fontsize) / 2
                draw.text((x_start + halfwidth, y + halfheight), textToDraw, 0, font=font)
                # draw.text((x, y_start ), textToDraw, 0)

        del draw

        # create file
        # image.show()
        actualFilename = folderName + fileName

        logging.debug("Saving {" + str(format(actualFilename)) + "}")
        image.save(actualFilename)

    def get_combined_colors(self, n, s=0.5, l=0.5):
        """
        Generiere n visuell unterschiedliche Farben im RGB-Format.
        Verwendet Kelly-Farben, wenn n <= 20, andernfalls werden Farben aus dem HSL-Farbraum generiert.
        Parameter:
            n (int): Anzahl der Farben, die generiert werden sollen.
            s (float): Sättigung der Farben. Standardwert ist 0.5. Wird nur verwendet, wenn n > 20.
            l (float): Helligkeit der Farben. Standardwert ist 0.5. Wird nur verwendet, wenn n > 20.
        Rückgabe:
            colors (Liste von Tupeln): Liste der generierten RGB-Farben.
        """
        light_grey = (200, 200, 200)
        kelly_colors = self.get_kelly_colors()
        if n <= len(kelly_colors):
            colors = random.sample(kelly_colors, n)
        else:
            extra_colors_needed = n - len(kelly_colors)
            colors = random.sample(kelly_colors, len(kelly_colors))
            colors += self.generate_visually_distinct_colors_2(extra_colors_needed, s, l)
        # Randomly shuffle the colors (excluding light grey)
        random.shuffle(colors)
        # Add light grey at the beginning and move other colors one position back.
        colors.insert(0, light_grey)
        colors = colors[:n + 1]
        return colors

    def get_kelly_colors(self):
        kelly_colors_hex = [
            "#F0F0F1",  # Light Gray
            "#181818",  # Dark Gray
            "#F7C100",  # Vivid Yellowish Orange
            "#875392",  # Strong Purplish Pink
            "#F78000",  # Vivid Orange
            "#9EC9EF",  # Very Light Blue
            "#C0002D",  # Vivid Red
            "#C2B280",  # Grayish Yellow
            "#838382",  # Medium Gray
            "#008D4B",  # Vivid Green
            "#E68DAB",  # Strong Purplish Pink
            "#0067A8",  # Strong Blue
            "#F99178",  # Strong Yellowish Pink
            "#5E4B97",  # Strong Violet
            "#FBA200",  # Vivid Orange Yellow
            "#B43E6B",  # Strong Purplish Red
            "#DDD200",  # Vivid Greenish Yellow
            "#892610",  # Strong Reddish Brown
            "#8DB600",  # Vivid Yellowish Green
            "#65421B",  # Deep Yellowish Brown
            "#E4531B",  # Vivid Reddish Orange
            "#263A21",  # Dark Olive Green
        ]

        # if n > len(kelly_colors_hex):
        #    raise ValueError("The maximum number of colors supported is {}.".format(len(kelly_colors_hex)))

        kelly_colors_rgb = [tuple(int(hex_color[i:i + 2], 16) for i in (1, 3, 5)) for hex_color in kelly_colors_hex]
        return kelly_colors_rgb

    def generate_visually_distinct_colors_2(self, n, s=0.5, l=0.5):
        """
        Generiere n visuell unterschiedliche Farben im RGB-Format.
        Parameter:
            n (int): Anzahl der Farben, die generiert werden sollen.
            s (float): Sättigung der Farben. Standardwert ist 0.5.
            l (float): Helligkeit der Farben. Standardwert ist 0.5.
        Rückgabe:
            colors (Liste von Tupeln): Liste der generierten RGB-Farben.
        """
        colors = []
        for i in range(n):
            h = i / n
            r, g, b = colorsys.hls_to_rgb(h, l, s)
            colors.append((int(r * 255), int(g * 255), int(b * 255)))
        return colors
