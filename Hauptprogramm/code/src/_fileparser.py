import random
import string
from dataclasses import dataclass, field
from os.path import exists as file_exists
from pathlib import Path
import os
from copy import deepcopy
from _spielstein import Spielstein
import logging
from _profiler import Profiler

# def generate_id() -> str:
#     """
#     Generate a random string.
#
#     This method generates a random string with uppercase letters and a length of 12 characters.
#
#     Args:
#         None.
#
#     Returns:
#         str: A random string.
#     """
#     return "".join(random.choices(string.ascii_uppercase, k=12))

#@dataclass(kw_only=True, slots=True)  # kw_only bedeutet beim aufrufen muss man filname= hinschreiben und slots macht das Programm schneller
@dataclass
class FileParser:
    """
    A class that parses a text file containing game data.

    Attributes:
        fileName (str): The name of the text file.
        timeLimit (str): A string representation of the time limit for solving the game.
        debugMode (bool): A boolean value indicating whether or not to enable debugging.
        allSpielsteine (list): A list of Spielstein objects representing all game pieces in the game.
        height (int): The height of the game field.
        width (int): The width of the game field.
    """

    fileName: str = ""
    timeLimit: str = ""
    debugMode: bool = False
    allSpielsteine = []
    height = -1
    width = -1

    # active: bool = True # boolean
    # email_addresses: list[str] = field(default_factory=list) # list of string
    # id: str = field(init=False, default_factory=generate_id)
    # _search_string: str = field(init=False, repr=False) # repr = false bedeutet es wird nicht ausgegeben
    # def __post_init__(self) -> None: 
    #     self._search_string = f"{self.filename} {self.timelimit}"

    def _check_File_exists(self) -> None:
        """
        Check if the file exists.

        This method checks if the file exists at the given location and logs appropriate messages.

        Args:
            None.

        Returns:
            None.
        """

        b_file_exists = file_exists(self.fileName)

        #logging.debug("b_file_exists" + str(b_file_exists))
        #if b_file_exists:
        #    if self.debugMode:
        #       logging.debug("> File exists: " + str(self.fileName))
        #else:
        #    logging.debug("> Program-Error: File " + str(self.fileName) + " does not exists")

        path = Path(self.fileName)

        b_path = path.is_file()
        #logging.debug("b_path" + str(b_path))
        if b_path:
            if self.debugMode:
                logging.debug("> File exists: " + str(self.fileName))
        else:
            logging.debug("> Program-Error: File " + str(self.fileName) + " does not exists")

        if b_path != b_file_exists:
            logging.debug("> Program-Fatal-Error: The file " + str(self.fileName) + " exists for the one but not for the other"
                                                                       " checking method")

    def _logFile(self):
        """
        Log the files in the current directory.

        This method logs the current path and all files in the current directory.

        Args:
            None.

        Returns:
            None.
        """

        aktuellerPfad = os.getcwd()
        inhalteAktuellerOrdner = os.listdir()
        logging.debug("your current path to the project is : \n " + str(aktuellerPfad))
        logging.debug("your folder contains these files: \n" + str(inhalteAktuellerOrdner))
        for datei in os.listdir():
            dateiendung = os.path.splitext(datei)[1]
            #if dateiendung.lower() == ".txt":
                #logging.debug("Textfile: \t" + str(datei))


    def _transform_text_to_array(self, textToTransform) -> []:
        """
        Transform a text string to a 1D list.

        This method transforms a text string to a 1D list of integers, where each integer represents an active or
        inactive pixel.

        Args:
            textToTransform (str): The text string to transform.

        Returns
            list: A 1D list of integers representing active or inactive pixels.
        """

        stringExistsInMap = False
        list = []
        map = {
            "#": 1,
            ".": 0
        }

        for s in textToTransform:
            if s in map:
                list.append(map.get(s))
                stringExistsInMap = True

        if not stringExistsInMap:
            logging.debug("Unknown-Symbols-Error: " + str(textToTransform))


        return list

    def _checkWidthAndHeight(self, sHeight, sWidth):
        """
        Check if the dimensions of the Spielstein object are smaller than the dimensions of the game field.

        This method checks if the dimensions of a Spielstein object are smaller than the dimensions of the game field.

        Args:
            sHeight (int): The height of the Spielstein object.
            sWidth (int): The width of the Spielstein object.

        Returns:
            bool: True if the dimensions of the Spielstein object are smaller than the dimensions of the game field,
                  False otherwise.
        """

        if sHeight <= self.height and sWidth <= self.width:
            return True
        else:
            return False


    def _readFile(self):
        """
        Read the text file and create Spielstein objects.

        This method reads the text file, creates Spielstein objects, and appends them to the allSpielsteine list.

        Args:
            None.

        Returns:
            None.
        """

        with open(self.fileName, "r") as self.file:
            # print(self.file.read()) # print complete file

            counter = 1
            newObjectCounter = -1

            numberObjects = -1
            objectName = ""
            objectList = []
            for line in self.file:
                line = line.rstrip("\n") # remove the \n (bc every line ends with "\n")

                #logging.debug("line " + str(counter) + " " + str(line))

                #if "p pack" == line and counter == 1:
                    # first line
                    #logging.debug("First Line is correct : " + str(line))
                #elif counter == 1:
                    #logging.debug("Text-File-Error: First line should be \"p pack\"")

                if counter == 2:
                    # second line
                    widthHeight = line.split(" ")
                    self.width = int(widthHeight[0])
                    self.height = int(widthHeight[1])

                    #logging.debug("width: \t\t" + str(self.width))
                    #logging.debug("height: \t" + str(self.height))
                    newObjectCounter = 0


                if newObjectCounter == 1 and counter > 2:
                    #anzahl an bausteinen die erstellt werden sollen
                    tempLine = line.split(" ")
                    numberObjects = int(tempLine[0])
                    objectName = tempLine[1]
                    #logging.debug("numberObjects" + str(numberObjects))
                    #logging.debug("SpielsteinName: " + str(objectName))

                if newObjectCounter > 1 and counter > 2 and not "%%%" == line:
                    objectList.append(self._transform_text_to_array(line))

                if "%%%" == line and counter > 2:
                    #speichere den Baustein & die Anzahl an Objekten die erstellt werden sollen
                    tempObjectList = deepcopy(objectList)
                    tempSpielStein = Spielstein(blocks=tempObjectList)
                    tempSpielStein._setSpielsteineImSpiel(anzahl=numberObjects, name=objectName)

                    #logging.debug("prüfe ob das spielstein kleiner ist ob das Spiel Feld")
                    if not self._checkWidthAndHeight(sHeight=tempSpielStein.height, sWidth=tempSpielStein.width):
                        logging.debug("Error-Spielstein-Bigger-then-Playfield")

                    #logging.debug("tempSpielStein " + str(tempSpielStein))
                    self.allSpielsteine.append(tempSpielStein)

                    #logging.debug("tempObjectList " + str(numberObjects))
                    #logging.debug("tempObjectList " + str(tempObjectList))

                    #setze counter zurück
                    newObjectCounter = 0
                    objectList = []

                counter += 1
                if counter > 2:
                    newObjectCounter += 1
            #print()

#    def _createObjectsOutOfFile(self):

    def _checkAllPixelCount(self):
        """
        Checks if the sum of all active pixels in all Spielsteine objects exceeds the total number of pixels in the playfield.

        Raises:
            None

        Returns:
            None
        """

        totalPixel = self.width * self.height
        tempObjectList = deepcopy(self.allSpielsteine)

        allPixels = 0
        for spielStein in tempObjectList:
            numberStone = spielStein.spielsteineImSpiel
            numberActiveBlocks = len(spielStein.activeBlocks)
            allPixels += numberStone * numberActiveBlocks

        logging.debug("allPixels  = " + str(allPixels))
        logging.debug("totalPixel = " + str(totalPixel))

        if allPixels > totalPixel:
            print("No Solution possible. \nYou try to fit " + str(allPixels) + " Pixels in " + str(totalPixel) + " Pixels" + " filename : " + str(self.fileName))
            logging.info("No Solution possible. \nYou try to fit " + str(allPixels) + " Pixels in " + str(totalPixel) + " Pixels")
            quit()


    @Profiler
    def _check_all(self) -> None:
        """
        Calls all the necessary functions to check the validity of the file and its contents.

        Raises:
            None

        Returns:
            None
        """

        self._check_File_exists()
        self._logFile()
        self._readFile()
        self._checkAllPixelCount()
        #self._createObjectsOutOfFile()