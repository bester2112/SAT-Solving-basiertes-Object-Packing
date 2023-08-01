import re
import logging
from _utilities import Utilities


class SolutionEvaluator():
    utility: Utilities = None

    def __init__(self, playfieldWidth, playfieldHeight, img):
        self.utility = Utilities()
        self.playfieldWidth = playfieldWidth
        self.playfieldHeight = playfieldHeight
        self.image = img
        self.fileName = "_finalSolution.png"


    def _extractInfos(self, solution, data_list: list):
        """
        Extracts information from a list of data.

        This method extracts information from a list of data, converts the data to a dictionary and uses it to create
        an image of the game field with all tetrominos in their final positions.

        Args:
            data_list (list): The list of data to extract information from.

        Returns:
            None.
        """
        if not solution == "SATISFIABLE":
            return

        result = {}
        mapSpielsteine = {}
        p_pattern = r'p\[(.*?)\]'
        s_pattern = r's(.*?)l\['
        l_pattern = r'l\[(.*?)\]'
        g_pattern = r'g\[(.*?)\]'
        for data in data_list:
            p = re.search(p_pattern, data).group(1)
            s = re.search(s_pattern, data).group(1)
            l = re.search(l_pattern, data).group(1)
            g = re.search(g_pattern, data).group(1)

            globalVal = "[" + g + "]"
            if globalVal in result:
                logging.debug("ERROR : " + str(globalVal) + " is part of " + str(result) + ". But should not.")

            result[globalVal] = [p, s, l, g]

            globalContent = self.utility._strToList(globalVal)
            if s in mapSpielsteine:
                list = mapSpielsteine[s]
                list.append(globalContent)
                mapSpielsteine[s] = list
            else:
                mapSpielsteine[s] = [globalContent]

            # result.append([p, s, l, g])

        self.image.createImgForAllSpielsteine(fieldWidth=self.playfieldWidth,
                                              fieldHeight=self.playfieldHeight,
                                              fileName="_finalSolution.png",
                                              folderName=self.image.folderName,
                                              elemMap=mapSpielsteine)
