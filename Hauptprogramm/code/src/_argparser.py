import sys
import argparse
from _model import Model

class ArgParser:
    """
    Parses command-line arguments and stores them as instance attributes.

    Args:
        None

    Attributes:
        fileName (str): The name of the file to be executed.
        timeLimit (str): The time limit after which the program should break up.
        debugMode (bool): Whether or not debug mode is enabled.

    Methods:
        parse_args(argv): Parses command-line arguments and stores them as instance attributes.

    Raises:
        None

    Returns:
        None
    """

    def __init__(self) -> None:
        """
        Initializes instance attributes with default values.

        Args:
            None

        Raises:
            None

        Returns:
            None
        """

        self.model = None
        self.fileName = ""
        self.timeLimit = ""
        self.debugMode = False

        self.parse_args(sys.argv[1:])

    def parse_args(self, argv):
        """
        Parses command-line arguments and stores them as instance attributes.

        Args:
            argv (list): A list of command-line arguments.

        Raises:
            None

        Returns:
            args: The parsed arguments.
        """
        
        parser = argparse.ArgumentParser()

        # positionals arguments (always required)
        parser.add_argument("filename", type=str, help="file which should be executed")

        # optional arguments (not necessary)
        parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1, 2], help="increase output verbosity")
        parser.add_argument("-d", "--debug", type=int, choices=[0, 1], help="debug mode 0 = off, 1 = on")
        #parser.add_argument("-f", "--filename", type=str, required=True, help="file which should be executed")
        parser.add_argument("-s", "--seconds", type=int, default=60 * 60, required=False,
                            help="time limit after the programm should break up (units: s = (second))")
        parser.add_argument("-m", "--model", type=str, required=False, choices=["standard", "binary"], help="used model to run the program")

        args = parser.parse_args(argv)

        if args.model == "standard":
            self.model = Model.Standard
        elif args.model == "binary":
            self.model = Model.Binary
        elif args.model == None:
            self.model = Model.Standard
        else:
            raise Exception("Invalid model")

        self.fileName = args.filename
        self.timeLimit = args.seconds
        if args.debug == 0:
            self.debugMode = False
        else:
            self.debugMode = True


        # answer = 0

        # if args.verbosity == 2:
        #     print(f"the square of {args.square} equals {answer}")
        # elif args.verbosity == 1:
        #     print(f"{args.square}^2 == {answer}")
        # else:
            # answer = 0
            # print(answer)
            # print(self.fileName)
            # print(self.timeLimit)

        return args
