from dataclasses import dataclass, field
from copy import deepcopy
from itertools import groupby
#from _clauselStone import ClauselStone
import logging

# max = 1

@dataclass
class Spielstein:
    """
    Represents a game piece in a block-based puzzle game.

    Attributes:
        name (str): The name of the game piece.
        width (int): The width of the game piece in blocks.
        height (int): The height of the game piece in blocks.
        spielsteineImSpiel (int): The number of game pieces of this type in the game.
        alleMoeglichenPlaziertenSteine (dict): A dictionary of all possible positions where the game piece
            can be placed on the game board, with the position as the key and the active blocks and position as
            the value.
        moeglichePositionen (list): A list of all possible positions where the game piece can be placed on the
            game board.
        list2D (list): A 2D list representing the shape of the game piece, with 1s indicating active blocks and
            0s indicating inactive blocks.
        activeBlocks (list): A list of the active blocks in the game piece.
        equivalentClauselList (list): A list of ClauselStone objects representing the game piece's clauses.
        firstPixelList (list): A list of the first pixel in each row of the game piece's shape.
    """

    name: str
    width: int
    height: int
    spielsteineImSpiel: int
    alleMoeglichenPlaziertenSteine: {} # map key ist die Position [0,0] und ergebnis ist die activeBlocks + key
    moeglichePositionen: list = field(default_factory=list)
    list2D: list = field(default_factory=list)
    activeBlocks: list = field(default_factory=list)
    equivalentClauselList: list = field(default_factory=list)
    firstPixelList: list = field(default_factory=list)


    def _calculateOnlyActiveBlocks(self):
        """
        Calculate the list of active blocks in the game piece.

        This method iterates over the 2D list 'list2D' and adds the coordinates of all active blocks to
        the 'activeBlocks' attribute.

        Args:
            self (object): The instance of the class calling this method.

        Returns:
            None.
        """

        activeList = []
        for y in range(len(self.list2D)):
            for x in range(len(self.list2D[y])):
                if self.list2D[y][x] == 1:
                    activeList.append([x, y])
                #logging.debug("self.list2D[y][x] " + str(self.list2D[y][x]))

        self.activeBlocks = deepcopy(activeList)
        #logging.debug("activeList: " + str(self.activeBlocks))

    def all_equal(self, iterable):
        """
        Check if all elements in an iterable are equal.

        This method uses the 'groupby' function from the 'itertools' module to group elements in the iterable
        and checks if there is only one group (i.e. all elements are equal).

        Args:
            iterable (iterable): An iterable to check for equality.

        Returns:
            bool: True if all elements are equal, False otherwise.
        """

        g = groupby(iterable)
        return next(g, True) and not next(g, False)

    def _calculate_width_height(self):
        """
        Calculate the width and height of the game piece.

        This method iterates over the 2D list 'list2D' and calculates the width and height of the game piece.
        It raises a ValueError if the width of the game piece is not the same for all rows.

        Args:
            self (object): The instance of the class calling this method.

        Returns:
            None.
        """

        widthList = []
        for i in range(len(self.list2D)):
            widthList.append(len(self.list2D[i]))
            # for j in range(len(self.list2D[i])):
            #     print(self.list2D[i][j])

        if self.all_equal(widthList):
            #logging.debug("all the same")
            self.width = widthList[0]
            self.height = len(self.list2D)
            #logging.debug("width:  " + str(self.width))
            #logging.debug("height: " + str(self.height))
        else:
            logging.error("Error not all the same: " + str(widthList))
            raise ValueError("Error not all the same: " + str(widthList))

    def _setSpielsteineImSpiel(self, anzahl, name):
        """
        Set the number of game pieces of this type in the game.

        This method sets the 'spielsteineImSpiel' and 'name' attributes to the given values, and initializes
        the 'firstPixelList' and 'equivalentClauselList' attributes for each game piece.

        Args:
            self (object): The instance of the class calling this method.
            anzahl (int): The number of game pieces of this type in the game.
            name (str): The name of the game piece.

        Returns:
            None.
        """

        self.spielsteineImSpiel = anzahl
        self.name = name
        for index in range(self.spielsteineImSpiel):
            #empty = ClauselStone(index)
            #self.equivalentClauselList.append(empty)
            self.firstPixelList.append([])
            self.equivalentClauselList.append([])
    def __init__(self, blocks):
        """
        Initialize a Spielstein object.

        This method initializes a Spielstein object with the given 2D list 'blocks', and calls the
        '_calculate_width_height', '_calculateOnlyActiveBlocks', and '_setSpielsteineImSpiel' methods to
        calculate the game piece's width and height, active blocks, and number of game pieces in the game.

        Args:
            self (object): The instance of the class calling this method.
            blocks (list): A 2D list representing the shape of the game piece, with 1s indicating active blocks
                and 0s indicating inactive blocks.

        Returns:
            None.
        """

        self.list2D = deepcopy(blocks)
        self._calculate_width_height()
        self._calculateOnlyActiveBlocks()
        self.spielsteineImSpiel = -1
        self.moeglichePositionen = []
        self.alleMoeglichenPlaziertenSteine = {}
        self.equivalentClauselList = []
        self.firstPixelList = []


