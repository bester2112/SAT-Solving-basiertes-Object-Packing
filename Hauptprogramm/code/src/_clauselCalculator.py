import itertools
import os
import subprocess
import time

from _model import Model
from _profiler import Profiler
from _utilities import Utilities
from _spielstein import Spielstein
from _imagecreator import ImageCreator
from _benchmarkRules import BenchmarkRules
from _timeCalculator import TimeCalculator
from _solutionEvaluator import SolutionEvaluator
import logging
from sathelper import SatHelper


class ClauselCalculator:
    """
    This class represents a clausel calculator.
    Attributes:
        alleSpielteine (list): List of all Spielsteine.
        playfieldWidth (int): Width of the playfield.
        playfieldHeight (int): Height of the playfield.
        image (ImageCreator): ImageCreator object to create images.
        mapPlayfield (dict): Dictionary of all positions in the playfield and their corresponding variables.
        allEquivalentClauselLists (list): List of equivalent Clausel lists for all Spielsteine.
        allFirstPixelLists (list): List of first pixels of all Spielsteine.
        maxTime (int): Maximum time for the calculation.
    """
    alleSpielteine = []
    playfieldWidth: int
    playfieldHeight: int
    image: ImageCreator
    mapPlayfield = {}
    allEquivalentClauselLists = []
    allFirstPixelLists = []
    maxTime: int
    model = None
    utility: Utilities = None
    benchmarkEquivalents = []
    benchmarkExactlyOneForThePixels = []
    benchmarkExactlyOneForThePossiblePlaystone = []

    def _possiblePositions(self, spielsteinTyp) -> None:
        """
        Creates a list of all possible positions where a Spielstein can be placed without getting out of the box/field.

        Args:
            spielsteinTyp (Spielstein): The type of Spielstein.
        """
        #logging.debug("create all possible positions where a Spielstein can be placed without to get out of the box / field")
        endWidth = self.playfieldWidth - spielsteinTyp.width + 1
        endHeight = self.playfieldHeight - spielsteinTyp.height + 1
        for y in range(endHeight):
            for x in range(endWidth):
                spielsteinTyp.moeglichePositionen.append([x, y])

        #logging.debug("spielsteinTyp.moeglichePositionen = " + str(spielsteinTyp.moeglichePositionen))

    def _createClauselForTheAmountOfOneStoneType(self, spielsteinTyp):
        """
        Creates variable names for a specific tetromino type based on the amount of tetrominoes in the game.

        This method creates variable names for a specific tetromino type based on the amount of tetrominoes in the game
        and adds them to the 'mapPlayfield' dictionary.

        Args:
            spielsteinTyp (Spielstein): The tetromino type to create variable names for.
        """
        for spielsteinIndex in range(spielsteinTyp.spielsteineImSpiel):
            self._createVariableName(spielsteinTyp, spielsteinIndex)

        result = self.check_map_playfield(self.mapPlayfield)
        if result == False:
            raise ValueError("mapPlayfield is not valid")

    def check_map_playfield(self, map_dict):
        for k, v in map_dict.items():
            if not self.utility.check_last_chars(map_dict, k):
                return False
        return True

    def _createClauselForOneStoneType(self, spielsteinTyp: Spielstein):
        """
        Creates all possible positions for a specific tetromino type and generates the corresponding clauses.
        This method creates all possible positions for a specific tetromino type, generates the corresponding clauses
        and adds them to the SAT solver.

        Args:
            spielsteinTyp (Spielstein): The tetromino type to create clauses for.
        """
        #logging.debug("methode die alles zusammen baut")
        #logging.debug("bestimme erst alle möglichen Positionen für einen SpielStein Typen - d.h. alle Start positionen bestimmen auf dem globalen Spielfeld")
        self._possiblePositions(spielsteinTyp=spielsteinTyp)
        #logging.debug("da für jeden Spielsteintyp die jeweiligen Plazierungen die gleichen sind, können die auch für alle vorher berechnet werden")
        self.utility._placeStoneOnPossiblePositions(spielsteinTyp=spielsteinTyp)

        # Ausgabe aller möglicher Positionen für den Baustein.
        self.image.createImgForSpielstein(fieldWidth=self.playfieldWidth,
                                          fieldHeight=self.playfieldHeight,
                                          fileName=spielsteinTyp.name + "-moeglichePos.png",
                                          folderName=self.image.folderName,
                                          elemList=spielsteinTyp.moeglichePositionen,
                                          color=(150, 150, 150))

        #logging.debug("nachdem alle möglichen Positionen bestimmt sind, erstelle nun die Klauseln")
        #logging.debug("sehr wahrscheinlich muss man erst einmal Variablen Namen festlegen")
        #logging.debug("ein spielsteintyp kann mehr als 1 mal vorkommen, daher muss hier auch über die Häufigkeit der Spielsteine itteriert werden")
        #logging.debug("der einfachhaltshalber fangen wir jetzt mit 1 an")

    def _checkStoneFitsInPlayfield(self, stoneWidth: int, stoneHeight: int, name: str) -> None:
        """
        Checks if a tetromino fits in the game field.

        This method checks if a tetromino fits in the game field by comparing its width and height to the width and
        height of the game field.

        Args:
            stoneWidth (int): The width of the tetromino.
            stoneHeight (int): The height of the tetromino.
            name (str): The name of the tetromino.

        Raises:
            SyntaxError: If the tetromino is too big for the game field.
        """
        if not isinstance(stoneWidth, int) or not isinstance(stoneHeight, int):
            raise TypeError

        tempHeight = self.playfieldHeight - stoneHeight
        tempWidth = self.playfieldWidth - stoneWidth

        if tempHeight < 0:
            raise SyntaxError("The HEIGHT of your object {" + name + "} is too big for the playing field.\n" +
                              "To fix this modify your specified file")
        if tempWidth < 0:
            raise SyntaxError("The WIDTH of your object {" + name + "} is too big for the playing field.\n" +
                              "To fix this modify your specified file")

    def _collectAllVariables(self, spielsteinTyp: Spielstein) -> None:
        """
        Collects all equivalent clauses and first pixels for each tetromino type.

        This method collects all equivalent clauses and first pixels for each tetromino type and adds them to the
        'allEquivalentClauselLists' and 'allFirstPixelLists' attributes respectively.

        Args:
            spielsteinTyp (Spielstein): The tetromino type to collect clauses and pixels for.
        """
        for spielsteinIndex in range(spielsteinTyp.spielsteineImSpiel):
            self.allFirstPixelLists.append(spielsteinTyp.firstPixelList[spielsteinIndex])
            self.allEquivalentClauselLists.append(spielsteinTyp.equivalentClauselList[spielsteinIndex])
            #logging.debug("final - allFirstPixelLists: " + str(self.allFirstPixelLists))
            #logging.debug("final - allEquivalentClauselLists: " + str(self.allEquivalentClauselLists))

    @Profiler
    def _createLogicOriginalUntouched(self):
        """
        Creates all the clauses necessary for the SAT solver to solve the puzzle.
        """
        logging.info(" - create Variables - ")
        ctvProfiler = self._createTheVariables()
        logging.info(f" cV = {ctvProfiler}")
        logging.info(" - create equivalents - ")
        cteProfiler = self._createTheEquivalents()
        logging.info(f" cte = {cteProfiler}")
        logging.info(" - create Exactly One For The Pixels - ")
        ceoftpProfiler = self._createExactlyOneForThePixels()
        logging.info(f" ceoftpProfiler = {ceoftpProfiler}")
        logging.info(" - create Exactly One For The Possible Play stone - ")
        ceoftppProfiler = self._createExactlyOneForThePossiblePlaystone()
        logging.info(f"ceoftppProfiler = {ceoftppProfiler}")
        logging.info(" - created All Variables successfully - ")

        print("self.allVariableName", self.allVariableName)
        print("sh.addEquivalentList = ", len(self.benchmarkEquivalents))
        print("self.benchmarkEquivalents", self.benchmarkEquivalents)
        print("sh.addAtMostOne = ", len(self.benchmarkExactlyOneForThePixels))
        print("self.benchmarkExactlyOneForThePixels", self.benchmarkExactlyOneForThePixels)
        print("sh.addExactlyOne(firstPixelList) = ", len(self.benchmarkExactlyOneForThePossiblePlaystone))
        print("self.benchmarkExactlyOneForThePossiblePlaystone", self.benchmarkExactlyOneForThePossiblePlaystone)


        ''' save the benchmark Rules '''
        if self.model == Model.Binary:
            self.benchmarkRules = BenchmarkRules(self.allVariableName,
                                                 self.benchmarkEquivalents,
                                                 self.benchmarkExactlyOneForThePixels,
                                                 self.benchmarkExactlyOneForThePossiblePlaystone,
                                                 self.playfieldWidth,
                                                 self.playfieldHeight)
            self.sh.addClauseForAllCnfBinaryData(self.benchmarkRules.allCnfData)
        if self.model == Model.Standard:
            logging.info(" - start printing File - ")
            try:
                pffProfiler = self.sh.printFormulaFile(folder=self.image.folderName, filename="_file_problem.cnf")
                logging.info(f"pffProfiler = {pffProfiler}")
            except Exception as e:
                logging.info(f"Error occurred in {self.fileName}: {e}")
                print(f"Error occurred in {self.fileName}: {e}")
            logging.info(" - start printing finished - ")
            #print("#printed formula")

            #print("started Solving Sat please wait ...")
            logging.info("- started Solving Sat -")

            time_calculator_solving_SAT = TimeCalculator(max_time=self.maxTime)
            try:
                time_calculator_solving_SAT.measure_and_run("#1377# \" _solving_SAT \"", self.sh.solveSatPath, self.image.folderName, "_file_problem", self.maxTime)
                #self.sh.solveSatPath(folder=self.image.folderName, filename="_file_problem")
                #result = time_calculator.measure_and_run(your_function, arg1, arg2)

            #except TimeoutError:
                #print("Timeout of " + str(time_calculator_solving_SAT.max_time) + "s for \"" + str(time_calculator_solving_SAT.task_name) + "\" reached, terminating code. No Solution found in that time")
            except subprocess.TimeoutExpired:
                logging.info(f"Timeout of {self.maxTime} reached while solving SAT in {self.fileName}")
                print(f"Timeout of {self.maxTime} reached while solving SAT in {self.fileName}")
                #return
                quit()
            except Exception as e:
                logging.info(f"Error occurred in {self.fileName}: {e}")
                print(f"Error occurred in {self.fileName}: {e}")
                #return
                quit()
            finally:
                time_calculator_solving_SAT.stop()
                time_duration = time_calculator_solving_SAT.get_duration()
                #print(time_duration)
                logging.info(time_duration)
                #print("Timeout of " + str(self.maxTime) + "s  reached, terminating code. No Solution found in that time")
                #logging.error("Timeout of " + str(self.maxTime) + "s reached, terminating code. No Solution found in that time")

                file_size_cnf_res = -1
                file_size_cnf = -1
                file_size_cnf_res_formated = -1
                file_size_cnf_formated = -1
                folder = self.image.folderName
                filename = "_file_problem"
                file_path = os.path.join(folder, filename)
                file_path_res = file_path + ".cnf.res"
                if os.path.isfile(file_path_res):
                    file_size_cnf_res = os.path.getsize(file_path_res)
                    file_size_cnf_res_formated = self.format_my_size(file_size_cnf_res)
                    os.remove(file_path_res)
                    logging.info(f"- {file_path_res} with {file_size_cnf_res_formated} deleted successfully -")
                file_path_cnf = file_path + ".cnf"
                if os.path.isfile(file_path_cnf):
                    file_size_cnf = os.path.getsize(file_path_cnf)
                    file_size_cnf_formated = self.format_my_size(file_size_cnf)
                    os.remove(file_path_cnf)
                    logging.info(f"- {file_path_cnf} with {file_size_cnf_formated} deleted successfully -")
                if file_size_cnf_res != -1:
                    with open(file_path_res, 'w') as f:
                        f.write(f'file_size: {file_size_cnf_res}\n')
                        f.write(f'file_size_formated: {file_size_cnf_res_formated}')
                if file_size_cnf != -1:
                    with open(file_path_cnf, 'w') as f:
                        f.write(f'file_size: {file_size_cnf}\n')
                        f.write(f'file_size_formated: {file_size_cnf_formated}')
            #print("SAT finished")
            logging.info("-SAT finished-")

            logging.info("self.sh.solution: " + str(self.sh.solution))
            #logging.info("self.sh.trueValues" + str(self.sh.trueValues))
            #print("self.sh.trueValues = " + str(self.sh.trueValues))

            if self.model == Model.Binary:
                result = self.benchmarkRules.backToNormalVariables(self.sh.trueValues, self.sh.falseValues)

            time_calculator_extractInfos = TimeCalculator()
            time_calculator_extractInfos.start_with_task_name("#1376# _extractInfos & img creation")

            try:
                sEval = SolutionEvaluator(playfieldWidth=self.playfieldWidth, playfieldHeight=self.playfieldHeight, img=self.image)
                sEval._extractInfos(self.sh.solution, self.sh.trueValues)
            finally:
                time_calculator_extractInfos.stop()
                time_duration = time_calculator_extractInfos.get_duration()
                logging.info(time_duration)

        #if self.model == Model.Binary:
            #print(" started binary mode ")
            # TODO ...



        #print("Program finished")
        logging.info("Program finished")

    def format_my_size(self, bytes):
        """ Formatiert eine Dateigröße in der passendsten Einheit (KB, MB, GB, TB) """
        for unit in ['Bytes', 'KB', 'MB', 'GB', 'TB']:
            if bytes < 1024.0:
                return f"{bytes:3.0f} {unit}"
            bytes /= 1024.0

    @Profiler
    def _createTheVariables(self):
        """
        Create a list of all variables in the playfield map and declare them with the solver.

        This method populates the 'allVariableName' list with all variables in the 'mapPlayfield'
        dictionary, flattens the list of variables, and declares the variables with the solver by
        calling the 'declareVariableList' method of the 'sh' object.
        """
        self.allVariableName = []
        #logging.debug("alle Variablen sollten in der map gespeichert sein, es werden alle variablen der einfachheit halber in eine liste gespeichert")
        for key in self.mapPlayfield:
            self.allVariableName.append(self.mapPlayfield[key])

        self.allVariableName = list(itertools.chain.from_iterable(self.allVariableName))
        #print(self.allVariableName)

        if self.model == Model.Standard:
            self.sh.declareVariableList(self.allVariableName)

    @Profiler
    def _createTheEquivalents(self):
        """
        Creates all the equivalent clauses for each Spielstein object.
        """
        #logging.debug("Now we are creating the eqivalent clauseln")
        for spielSteinEquivalentList in self.allEquivalentClauselLists:
            for oneEquivalentList in spielSteinEquivalentList:
                canBeAdded = self.sh.addEquivalentList(oneEquivalentList, self.model)
                if canBeAdded:
                    self.benchmarkEquivalents.append(oneEquivalentList)

    @Profiler
    def _createExactlyOneForThePixels(self) -> None:
        """
        Create the 'exactly one' clauses for all the pixels.

        This method iterates through each pixel in the 'mapPlayfield' dictionary
        and creates the 'exactly one' clause for each pixel. The 'exactly one'
        clauses are then added to the formula using the 'addClauseList' method of
        the 'sh' object.
        """
        # #print("Now we are creating the Exactly One OR At Most One for each pixel")
        #logging.debug("Now we are creating the Exactly One OR At Most One for each pixel")
        for key, content in self.mapPlayfield.items():
            if not content == []:

                #print("addAtMostOne added for " + str(content))
                if self.model == Model.Standard:
                    self.sh.addAtMostOne(content)  # TODO or exact one if you just want that it should
                self.benchmarkExactlyOneForThePixels.append(content)
                # TODO solve if everything is filled
                # logging.debug("addExactlyOne added for " + str(content))
                # if self.model == Model.Standard:
                    # self.sh.addExactlyOne(content) #TODO THIS HERE

    @Profiler
    def _createExactlyOneForThePossiblePlaystone(self) -> None:
        """
        Create the 'exactly one' clauses for all the possible play stones.

        This method iterates through each Spielstein object in the 'alleSpielteine' list
        and creates the 'exactly one' clause for all the possible placements of each stone.
        The 'exactly one' clauses are then added to the formula using the 'addClauseList' method of
        the 'sh' object.
        """
        #logging.debug("Für jeden Spielstein, werden alle möglichen Positionen mit exactly one verknüpft. \nd.h. für jeden Spielstein darf nur ein stein plaziert werden.")
        # #print("Für jeden Spielstein, werden alle möglichen Positionen mit exactly one verknüpft."
        #      "\nd.h. für jeden Spielstein darf nur ein stein plaziert werden.")
        for firstPixelList in self.allFirstPixelLists:
            # #print("firstPixelList " + str(firstPixelList))
            #logging.debug("excatlyOne for = " + str(firstPixelList))
            if self.model == Model.Standard:
                self.sh.addExactlyOne(firstPixelList)
            self.benchmarkExactlyOneForThePossiblePlaystone.append(firstPixelList)

    def _createClauselForAllStones(self) -> None:
        """
        Creates all the clauses for each Spielstein object.

        This method first checks if a stone fits in the playfield, then creates the clauses
        for one stone type, creates the clauses for the amount of one stone type, and collects
        all variables for each stone type. Finally, the method calls the '_createLogic' method
        to create the logic for the formula.
        """
        #logging.debug("input alle Spielsteine, weitergabe an weitere funktion, die die aufgabe lösen soll")
        # check if the stone fits in the field
        for spielsteinTyp in self.alleSpielteine:
            #logging.debug("SpielsteinTyp = " + str(spielsteinTyp))
            self._checkStoneFitsInPlayfield(stoneWidth=spielsteinTyp.width, stoneHeight=spielsteinTyp.height,
                                            name=spielsteinTyp.name)

        for spielsteinTyp in self.alleSpielteine:
            self._createClauselForOneStoneType(spielsteinTyp)
            self._createClauselForTheAmountOfOneStoneType(spielsteinTyp)
            self._collectAllVariables(spielsteinTyp)
            #logging.debug("SpielsteinTyp = " + str(spielsteinTyp))
            #logging.debug("self.alleSpielteine = " + str(self.alleSpielteine))
            #logging.debug("spielsteinTyp.alleMoeglichenPlaziertenSteine = " + str(spielsteinTyp.alleMoeglichenPlaziertenSteine))

        #logging.debug("create now from \"allEquivalentClauselLists\", \"allFirstPixelLists\" and \"mapPlayfield\" the clausel:")
        res, cLOUProfiler = self._createLogicOriginalUntouched()
        logging.debug(f"cLOUProfiler {cLOUProfiler}")

    def init_map(self) -> None:
        """
        Initializes the 'mapPlayfield' dictionary with keys and empty lists.

        This method initializes the 'mapPlayfield' dictionary with keys representing each pixel
        in the playfield, and values that are initially empty lists.
        """
        for y in range(self.playfieldHeight):
            for x in range(self.playfieldWidth):
                self.mapPlayfield[self.utility._listToStr([x, y])] = []

    def _createVariableName(self, spielsteinTyp: Spielstein, spielsteinIndex: int) -> None:
        """
        Create a list of all variables in the playfield map and declare them with the solver.
        This method populates the 'allVariableName' list with all variables in the 'mapPlayfield'
            dictionary, flattens the list of variables, and declares the variables with the solver by
            calling the 'declareVariableList' method of the 'sh' object.
        """
        if not isinstance(spielsteinTyp, Spielstein) or not isinstance(spielsteinIndex, int):
            raise TypeError

        #logging.debug("hier wird der Variablenname zusammengebaut")
        for pixelPosition in spielsteinTyp.alleMoeglichenPlaziertenSteine:
            newStringList = []

            firstPixel = True

            for actualPosIndex in range(len(spielsteinTyp.alleMoeglichenPlaziertenSteine[pixelPosition])):
                actualPos = spielsteinTyp.alleMoeglichenPlaziertenSteine[pixelPosition][actualPosIndex]
                actualPosStr = self.utility._listToStr(actualPos)
                pixelPrefix = "p"
                pixelCoordinate = pixelPosition
                pixelString = pixelPrefix + pixelCoordinate

                spielsteinPrefix = "s"
                spielsteinName = spielsteinTyp.name
                spielsteinNummer = spielsteinIndex + 1
                spielString = spielsteinPrefix + spielsteinName + str(spielsteinNummer)

                localSpielsteinPrefix = "l"
                localSpielsteinNummer = self.utility._listToStr(spielsteinTyp.activeBlocks[actualPosIndex])
                localSpielsteinString = localSpielsteinPrefix + localSpielsteinNummer

                globalSpielsteinPrefix = "g"
                globalSpielsteinNummer = actualPosStr
                globalSpielsteinString = globalSpielsteinPrefix + globalSpielsteinNummer

                res = pixelString + spielString + localSpielsteinString + globalSpielsteinString

                newStringList.append(res)
                self.mapPlayfield[actualPosStr].append(res)
                if firstPixel:
                    firstPixel = False
                    spielsteinTyp.firstPixelList[spielsteinIndex].append(res)

            spielsteinTyp.equivalentClauselList[spielsteinIndex].append(newStringList)

    def __init__(self, alleSpielteine, spielFeldBreite, spielFeldHoehe, image, timeToRun, model, fileName):
        """
        Initializes an instance of the ClauselCalculator class.

        This method initializes an instance of the ClauselCalculator class by setting
        the 'alleSpielteine', 'playfieldWidth', 'playfieldHeight', 'maxTime', and 'image'
        instance attributes.

        Args:
            alleSpielteine (list): A list of Spielstein objects.
            spielFeldBreite (int): The width of the playfield.
            spielFeldHoehe (int): The height of the playfield.
            image (ImageCreator): An instance of the ImageCreator class.
            timeToRun (int): The maximum amount of time to run the solver.
        """
        self.alleSpielteine = alleSpielteine
        self.playfieldWidth = spielFeldBreite
        self.playfieldHeight = spielFeldHoehe
        self.maxTime = timeToRun
        self.image = image
        self.model = model
        self.count = 0
        self.utility = Utilities()
        self.fileName = fileName

    @Profiler
    def run(self) -> None:
        """
        Runs the solver.

        This method initializes the SatHelper object, initializes the 'mapPlayfield' dictionary,
        creates all the clauses for each Spielstein object, and runs the solver.
        """
        #logging.info(" Init SatHelper ")
        self.sh = SatHelper()
        #logging.info(" Init Map ")
        self.init_map()
        #logging.info(" Create All Clauses ")
        # start_time = time.time()
        #
        # # Schleife für eine Minute ausführen
        # while time.time() - start_time < 60:
        #     # Führe hier deine Berechnungen aus
        #     pass
        #
        # # Ausgabe, wenn die Schleife abgeschlossen ist
        # print("Die Schleife wurde für eine Minute ausgeführt.")

        self._createClauselForAllStones()

        return None
