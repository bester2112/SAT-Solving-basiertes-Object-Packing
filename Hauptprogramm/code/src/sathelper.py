import logging
import subprocess
import sys
import time
import os
import signal
from sys import platform
from collections import Counter
from _model import Model
from _profiler import Profiler


class SatHelper:
    """
    A helper class for creating and manipulating Boolean formulas in conjunctive normal form (CNF).
    Attributes:
        nextIntId (int): The integer ID to assign to the next variable.
        variableIntMap (dict): A dictionary mapping variable names to integer IDs.
        intVariableMap (dict): A dictionary mapping integer IDs to variable names.
        clauses (list): A list of clauses in the CNF formula.
        softClauses (list): A list of soft clauses in the CNF formula.
        softClauseTotalWeight (int): The total weight of all soft clauses.
        trueValues (list): A list of variables assigned true in the most recent solution.
        solution (str): A string representation of the most recent solution found by a SAT solver.
    """
    nextIntId = 1
    variableIntMap = {}
    intVariableMap = {}
    clauses = []
    softClauses = []
    softClauseTotalWeight = 0
    trueValues = []
    falseValues = []
    solution = "-NONE-"

    def declareVariable(self, name):
        """
        Declares a new variable and assigns it an integer ID.

        Args:
            name (str): The name of the new variable.

        Raises:
            None

        Returns:
            None
        """

        self.variableIntMap.update({name:self.nextIntId})
        self.intVariableMap.update({self.nextIntId:name})
        self.nextIntId = self.nextIntId+1

    def declareVariableList(self, varList:list):
        """
        Declares a list of variables and assigns them integer IDs.

        Args:
            varList (list): A list of variable names.

        Raises:
            None

        Returns:
            None
        """

        for index in range(len(varList)):
            #print("Variable Declared : " + varList[index])
            #logging.debug("Variable Declared : " + varList[index])
            self.declareVariable(name=varList[index])

        #print()

    def variableToInt(self, name):
        """
        Maps a variable name to its integer ID.

        Args:
            name (str): The name of the variable.

        Raises:
            ValueError: If the variable name is not found.

        Returns:
            int: The integer ID of the variable.
        """

        if (name in self.variableIntMap):
            return self.variableIntMap[name]
        else:
            raise ValueError("unknown variable with name: " + name)

    def intToVariable(self, id):
        """
        Maps an integer ID to a variable name.

        Args:
            id (int): The integer ID of the variable.

        Raises:
            ValueError: If the integer ID is not found.

        Returns:
            str: The name of the variable.
        """

        if (id in self.intVariableMap):
            return self.intVariableMap[id]
        else:
            raise ValueError("unknown variable with id: " + id)

    def literalToInt(self, literal):
        """
        Maps a literal (i.e., a variable or its negation) to its integer ID.

        Args:
            literal (str): The name of the literal.

        Raises:
            ValueError: If the literal is not found.

        Returns:
            int: The integer ID of the literal.
        """

        intCode = self.variableToInt(self.getVariableName(literal))
        if (self.isNegated(literal)):
            return -intCode
        else:
            return intCode
    
    @staticmethod
    def isNegated(name):
        """
        Determines if a literal is negated.

        Args:
            name (str): The name of the literal.

        Raises:
            None

        Returns:
            bool: True if the literal is negated; otherwise, False.
        """
        return name.startswith("-")
        
    @staticmethod
    def getNegated(name):
        """
        Gets the negation of a literal.

        Args:
            name (str): The name of the literal.

        Raises:
            None

        Returns:
            str: The negated literal.
        """
        if SatHelper.isNegated(name):
            return SatHelper.getVariableName(name)
        else:
            return "-"+name

    @staticmethod
    def getVariableName(name):
        """
        Gets the variable name by removing the negation symbol if it exists.

        Args:
            name (str): A string representing the variable.

        Returns:
            str: The variable name.
        """
        if SatHelper.isNegated(name):
            return name[1:]
        else:
            return name

    def literalsToIntString(self, args):
        """
        Converts a list of literals to a string of integer values.

        Args:
            args (list): A list of literals.

        Returns:
            str: A string of integer values.
        """
        clause = ""
        for arg in args:
            clause += str(self.literalToInt(arg))+" "
        clause += "0"
        return clause

    def addClause(self, literals):
        """
        Adds a new clause to the formula.

        Args:
            literals (list): A list of literals.

        Returns:
            None
        """
        self.clauses.append(self.literalsToIntString(literals))

    def addSoftClause(self, literals):
        """
        Adds a new soft clause to the formula with a weight of 1.

        Args:
            literals (list): A list of literals.

        Returns:
            None
        """
        self.addWeightedSoftClause(1, literals)
        
    def addWeightedSoftClause(self, weight, literals):
        """
        Adds a new soft clause to the formula with a specified weight.

        Args:
            weight (int): The weight of the soft clause.
            literals (list): A list of literals.

        Returns:
            None
        """
        self.softClauseTotalWeight += weight
        self.softClauses.append(str(weight) + " " + self.literalsToIntString(literals))
           
    def addImplies(self, arg1, arg2):
        """
        Adds a new implication to the formula.

        Args:
            arg1 (str): A string representing the first variable.
            arg2 (str): A string representing the second variable.

        Returns:
            None
        """
        self.addClause([self.getNegated(arg1), arg2])

    def addEquivalent(self, arg1, arg2):
        """
        Adds a new equivalence to the formula.

        Args:
            arg1 (str): A string representing the first variable.
            arg2 (str): A string representing the second variable.

        Returns:
            None
        """
        self.addImplies(arg1, arg2)
        self.addImplies(arg2, arg1)

    def addEquivalentList(self, equivalentList:list, model:Model):
        """
        Adds multiple equivalences to the formula.

        Args:
            equivalentList (list): A list of variables.

        Returns:
            True if equivalent was added; otherwise, False.
        """

        if len(equivalentList) == 0:
            #logging.debug("> addEquivalent : the list is empty.")
            #print("> addEquivalent : the list is empty.")
            return False
        elif len(equivalentList) == 1:
            #logging.warning("> addEquivalent : only one Entry in the List " + str(equivalentList))
            #print("> addEquivalent : only one Entry in the List " + str(equivalentList))
            return False

        firstElement = equivalentList[0]
        for index in range(1, len(equivalentList)):
            if model == Model.Standard:
                #logging.debug("add Äquivalenz " + str(firstElement) + " <==> " + str(equivalentList[index]))
                # print("add Äquivalenz " + str(firstElement) + " <==> " + str(equivalentList[index]))
                self.addEquivalent(firstElement, equivalentList[index])

        return True

    def generateEquivalentsOutOfSympy(self, resultExpression):
        """
        example resultExpression =
        [
         [['g_0_0_b1', 'g_0_0_b2', '-g_0_1_b1'], ['g_0_0_b1', 'g_0_0_b2', '-g_0_1_b2'],
          ['g_0_1_b1', 'g_0_1_b2', '-g_0_0_b1'], ['g_0_1_b1', 'g_0_1_b2', '-g_0_0_b2']],
         [['g_1_0_b1', 'g_1_0_b2', '-g_1_1_b1'], ['g_1_0_b1', 'g_1_0_b2', '-g_1_1_b2'],
          ['g_1_1_b1', 'g_1_1_b2', '-g_1_0_b1'], ['g_1_1_b1', 'g_1_1_b2', '-g_1_0_b2']]
        ]
        """
        for expression in resultExpression:
            # Schritt 1: Teilen Sie den Ausdruck in Komponenten
            #exprComponents = str(expression).split(" & ")

            # Schritt 2: Entfernen Sie die Klammern
            #exprComponentsNoBrackets = [component.strip("()") for component in exprComponents]

            # Schritt 3: Entfernen Sie die ODER-Zeichen
            #exprComponentsWithoutOR = [component.replace(" | ", " ") for component in exprComponentsNoBrackets]

            # Schritt 4: Ersetzen Sie die Tilde durch Minus
            #exprComponentsReplacedNegation = [component.replace("~", "-") for component in exprComponentsWithoutOR]

            # Schritt 5: Teilen Sie die Zeichenfolgen in Listen von Literalen
            #exprComponentsList = [component.split(" ") for component in exprComponentsReplacedNegation]

            # Schritt 6: Fügen Sie die Klauseln zur CNF-Formel hinzu
            for literals in expression:
                self.addClause(literals)

    # Funktion zum Umwandeln der Sympy-Ausdrücke in Strings und Trennen der Elemente
    def sympyToStringList(self, sympy_expression_list):
        string_list = []
        for expr in sympy_expression_list:
            string_list.append(str(expr).split(" | "))
        return string_list


    def addClauseForThePossiblePlaystone(self, resultExpression):
        #exprComponentsReplacedNegation = [component.replace("~", "-") for component in resultExpression]
        #exprComponentsList = [component.split(" | ") for component in exprComponentsReplacedNegation]

        for expList in resultExpression:
            for expr in expList:
                self.addClause(literals=expr)

    def addClauseForAllCnfBinaryData(self, data):
        variable_counter = Counter()
        for clause in data:
            for variable in clause:
                variable_name = variable.strip('~')  # remove "~" if present
                variable_counter[variable_name] += 1

        # Create list of unique variable names
        unique_variables = list(variable_counter.keys())

        # Call declareVariableList method
        self.declareVariableList(unique_variables)

        # Now, add clause for all CNF binary data
        for clause in data:
            clause_list = list(map(str, clause))  # Convert tuple to list
            clause_list = [var.replace("~", "-") for var in clause_list]  # Replace "~" with "-"
            self.addClause(clause_list)

        return variable_counter

    def addatMostOneForThePossiblePlaystone(self, resultExpression):
        """
        example resultExpression =
        [[g_0_0_b1 | g_0_0_b2 | g_1_0_b1 | g_1_0_b2],
        [g_0_0_b1 | g_1_0_b1 | ~g_0_0_b2 | ~g_1_0_b2, g_0_0_b1 | g_0_1_b1 | ~g_0_0_b2 | ~g_0_1_b2,
         g_0_0_b1 | g_1_1_b1 | ~g_0_0_b2 | ~g_1_1_b2, g_0_1_b1 | g_1_0_b1 | ~g_0_1_b2 | ~g_1_0_b2,
         g_1_0_b1 | g_1_1_b1 | ~g_1_0_b2 | ~g_1_1_b2, g_0_1_b1 | g_1_1_b1 | ~g_0_1_b2 | ~g_1_1_b2]]
        """
        # Umwandlung der Sympy-Ausdrücke in Strings und Speichern in neuen Variablen

        exprComponentsReplacedNegation = [component.replace("~", "-") for component in resultExpression]
        exprComponentsList = [component.split(" | ") for component in exprComponentsReplacedNegation]

        for expList in exprComponentsList:
            self.addClause(literals=expList)

        #for expression in resultExpression:

            # Umwandlung der Sympy-Ausdrücke in Strings und Speichern in neuen Variablen
            #result_as_strings = [self.sympyToStringList(expr_list) for expr_list in expression]

            #self.addClause(literals=result_as_strings)

            # Schritt 1: Teilen Sie den Ausdruck in Komponenten
            ####### exprComponents = str(expression).split(" & ")

            # Schritt 2: Entfernen Sie die Klammern
            ####### exprComponentsNoBrackets = [component.strip("()") for component in exprComponents]

            # Schritt 3: Entfernen Sie die ODER-Zeichen
            #exprComponentsWithoutOR = [component.replace(" | ", " ") for component in exprComponentsNoBrackets]

            # Schritt 4: Ersetzen Sie die Tilde durch Minus
            #exprComponentsReplacedNegation = [component.replace("~", "-") for component in exprComponentsWithoutOR]

            # Schritt 5: Teilen Sie die Zeichenfolgen in Listen von Literalen
            #exprComponentsList = [component.split(" ") for component in exprComponentsReplacedNegation]

            # Schritt 6: Fügen Sie die Klauseln zur CNF-Formel hinzu
            #for literals in exprComponentsList:
                #self.addClause(literals)

    def addBinaryEquivalent(self, resultCNFexpression):
        """
        resultCNF is the CNF formula of a List of clauses represented in SymPy format.
        example how the formula is represented in SymPy format:
        result (cnf) =
            (g_0_0_b1 | g_0_0_b2 | g_0_0_b3 | g_0_0_b4 | g_0_0_b5 | ~g_0_1_b1) &
            (g_0_0_b1 | g_0_0_b2 | g_0_0_b3 | g_0_0_b4 | g_0_0_b5 | ~g_0_1_b2) &
            (g_0_0_b1 | g_0_0_b2 | g_0_0_b3 | g_0_0_b4 | g_0_0_b5 | ~g_0_1_b3) &
            (g_0_0_b1 | g_0_0_b2 | g_0_0_b3 | g_0_0_b4 | g_0_0_b5 | ~g_0_1_b4) &
            (g_0_1_b1 | g_0_1_b2 | g_0_1_b3 | g_0_1_b4 | g_0_1_b5 | g_0_1_b6 | ~g_0_0_b1)
        Task of this method is to translate the CNF formula into SAT Helper format.
        The variable names at this point already declared.
        """
        # TODO überlege, welche inputs existieren können & erstelle fehlermeldungen, wenn die leer oder nur 1 Element haben sollten
        # TODO siehe addEquivalentList (eine Methode oben drüber) für jetzt erst einmal übersprungen
        # TODO könnte fehlerquelle sein, später schwer zu finden
        # TODO check noch einmal, ob die NewVariablen auch drinnen sind!!!!!!

        # Schritt 1: Teilen Sie den Ausdruck in Komponenten
        exprComponents = str(resultCNFexpression).split(" & ")

        # Schritt 2: Entfernen Sie die Klammern
        exprComponentsNoBrackets = [component.strip("()") for component in exprComponents]

        # Schritt 3: Entfernen Sie die ODER-Zeichen
        exprComponentsWithoutOR = [component.replace(" | ", " ") for component in exprComponentsNoBrackets]

        # Schritt 4: Ersetzen Sie die Tilde durch Minus
        exprComponentsReplacedNegation = [component.replace("~", "-") for component in exprComponentsWithoutOR]

        # Schritt 5: Teilen Sie die Zeichenfolgen in Listen von Literalen
        exprComponentsList = [component.split(" ") for component in exprComponentsReplacedNegation]

        # Schritt 6: Fügen Sie die Klauseln zur CNF-Formel hinzu
        for literals in exprComponentsList:
            self.addClause(literals)

        #print()




    def addAtMostOne(self, args):
        """
       Adds a constraint to the formula such that at most one of the given variables can be true.

       Args:
           args (list): A list of variables.

       Returns:
           None
       """
        for i in range(len(args)-1):
            for j in range(i+1, len(args)):
                self.addClause([self.getNegated(args[i]), self.getNegated(args[j])])

    def addExactlyOne(self, args):
        """
        Adds a constraint to the formula such that exactly one of the given variables must be true.

        Args:
            args (list): A list of variables.

        Returns:
            None
        """
        self.addClause(args)
        self.addAtMostOne(args)
        
    def printFormula(self):
        """
        Prints the formula in the CNF format to standard output.

        Args:
            None

        Returns:
            None
        """
        print("p cnf", self.nextIntId-1, len(self.clauses))
        for clause in self.clauses:
            print(clause)

    @Profiler
    def printFormulaFile(self, folder, filename):
        """
        Writes the formula in the CNF format to a file.

        Args:
            folder (str): The name of the folder to write the file to.
            filename (str): The name of the file.

        Returns:
            None
        """
        file = open(folder + filename, "w")
        pcnfString = "p cnf " + str(self.nextIntId-1) + " " + str(len(self.clauses)) + "\n"
        file.write(pcnfString)
        for clause in self.clauses:
            file.write(clause+"\n")
        file.close()

        new_clauses = []

        for clause in self.clauses:
            transformed_clause = []
            for element in clause.split():
                if element.lstrip('-').isdigit():
                    num = int(element)
                    if num != 0:
                        transformed_element = self.intVariableMap[abs(num)]
                        if num < 0:
                            transformed_element = '-' + transformed_element
                    else:
                        transformed_element = str(num)
                    transformed_clause.append(transformed_element)
            new_clauses.append(' '.join(transformed_clause))

        #print(new_clauses)

        #file = open(folder + "ko" + filename, "w")
        #pcnfString = "p cnf " + str(self.nextIntId - 1) + " " + str(len(self.clauses)) + "\n"
        #file.write(pcnfString)
        #for clause in new_clauses:
        #    file.write(clause + "\n")
        #file.close()

    def printMaxSatFormula(self):
        """
        Prints the formula in the MaxSAT format to standard output.

        Args:
            None

        Returns:
            None
        """
        hardClauseWeight = self.softClauseTotalWeight + 1
        print("p wcnf", self.nextIntId-1, len(self.clauses)+len(self.softClauses), hardClauseWeight)
        for clause in self.clauses:
            print(hardClauseWeight, clause)
        for softClause in self.softClauses:
            print(softClause)
            
    def solveSat(self):
        """
        Solves the formula using the glucose SAT solver and prints the result to standard output.

        Args:
            None

        Returns:
            None
        """
        original_stdout = sys.stdout
        with open('formula.cnf', 'w') as f:
            sys.stdout = f
            self.printFormula()
            sys.stdout = original_stdout # Reset the standard output to its original value
            
        p = subprocess.run(["./glucose", "-model", "formula.cnf"], stdout=subprocess.PIPE, universal_newlines=True)
        solution = list(filter(lambda line: line.startswith("s "), p.stdout.splitlines()))[0][2:]
        print("The formula is", solution)
        self.solution = solution
        if solution == "SATISFIABLE":
            values = list(filter(lambda line: line.startswith("v "), p.stdout.splitlines()))[0][2:]
            self.printTrueVariables(values)

    def solveSatPath(self, folder, filename, maxTime):
        """
        Solves the SAT problem defined in a CNF file.

        Args:
            folder (str): The folder path where the CNF file is located.
            filename (str): The name of the CNF file.

        Raises:
            None

        Returns:
            None
        """
        original_stdout = sys.stdout
        file_path = os.path.join(folder, filename)
        with open(file_path + ".cnf.res", 'w') as f:
            sys.stdout = f
            self.printFormula()
            sys.stdout = original_stdout  # Reset the standard output to its original value

        
        #print("Platform: " + platform)
        logging.debug("Platform: " + platform)
        if platform == "darwin":
            # OS X
            path = folder + filename + ".cnf.res"
            #p = subprocess.run(["./glucose_mac", "-model", folder + filename + ".cnf.res"], stdout=subprocess.PIPE, universal_newlines=True)
            p = subprocess.run(["./kissat_mac", folder + filename + ".cnf.res"], stdout=subprocess.PIPE,
                               universal_newlines=True, timeout=maxTime)
            #p = subprocess.Popen(["./kissat_mac", folder + filename + ".cnf.res"], stdout=subprocess.PIPE,
            #                           universal_newlines=True)
            #p = subprocess.run(["./glucose_mac", "-model", folder + filename + ".cnf.res"], stdout=subprocess.PIPE, universal_newlines=True)
        elif platform == "linux" or platform == "linux2":
            # linux
            p = subprocess.run(["./kissat_linux", folder + filename + ".cnf.res"], stdout=subprocess.PIPE,
                               universal_newlines=True, timeout=maxTime)
            # p = subprocess.Popen(["./kissat_linux", folder + filename + ".cnf.res"], stdout=subprocess.PIPE,
            #                            universal_newlines=True)

        elif platform == "win32":
            # Windows...
            return None # TODO cant execute on windows
            #p = subprocess.run(["./glucose", "-model", folder + filename + ".cnf.res"], stdout=subprocess.PIPE, universal_newlines=True)
        else:
            #Other
            print("Error unknown plattform: " + str(platform))
            logging.error("Error unknown plattform: " + str(platform))

        # # starte den subprocess
        #
        # start_time = time.time()  # Speichert den Startzeitpunkt
        #
        # while True:
        #     # Warte eine Minute
        #     time.sleep(5)
        #
        #     # Überprüfe, ob eine Datei namens "terminate.txt" existiert
        #     if os.path.exists("terminate.txt"):
        #         # Wenn die Datei existiert, beende den subprocess
        #         p.send_signal(signal.SIGTERM)
        #         raise Exception("Subprocess wurde wegen Existenz von 'terminate.txt' beendet.")
        #         #break
        #
        #     # Überprüfe, ob der subprocess beendet wurde
        #     if p.poll() is not None:
        #         break
        #
        #     # Überprüfe, ob die maximale Zeit überschritten wurde
        #     if time.time() - start_time > maxTime:
        #         p.send_signal(signal.SIGTERM)
        #         raise Exception("Subprocess wurde wegen Überschreitung der maximalen Zeit beendet.")
        #         #break
        #
        # # Erhalte das Ergebnis des Subprozesses
        # stdout, stderr = p.communicate()
        #
        # # Speichern der stdout Daten in einer Datei
        # with open(folder + filename + "-stdout.cnf.res", 'w') as f:
        #     f.write(stdout)
        #
        # # Nur für Popen, bei Fehlern:
        # if stderr:
        #     print("STDERR:")
        #     print(stderr)
        # DO NOT DELETE:
        # für run()
        solution = list(filter(lambda line: line.startswith("s "), p.stdout.splitlines()))[0][2:]
        # für Popen()
        #solution = list(filter(lambda line: line.startswith("s "), stdout.splitlines()))[0][2:]
        #print("The formula is", solution)
        self.solution = solution
        if solution == "SATISFIABLE":
            #values = list(filter(lambda line: line.startswith("v "), p.stdout.splitlines()))[0][2:]
            values = ""
            # für run()
            for line in p.stdout.splitlines():
            # für Popen()
            #for line in stdout.splitlines():
                temp = line[0:2]
                if line[0:2] == "v ":
                    temp2 = line[-2:]
                    if line[-2:] == " 0":
                        values += line[2:]
                    else:
                        values += line[2:] + " "
            self.printTrueVariables(values)
    def solveMaxSat(self):
        """
        Solves the MAX-SAT problem defined in a CNF file.

        Args:
            None

        Raises:
            None

        Returns:
            None
        """
        original_stdout = sys.stdout
        with open('formula.cnf', 'w') as f:
            sys.stdout = f
            self.printMaxSatFormula()
            sys.stdout = original_stdout # Reset the standard output to its original value
            
        p = subprocess.run(["./open-wbo", "formula.cnf"], stdout=subprocess.PIPE, universal_newlines=True)
        solution = list(filter(lambda line: line.startswith("s "), p.stdout.splitlines()))[0][2:]
        print("The result is", solution)
        if solution == "OPTIMUM FOUND":
            values = list(filter(lambda line: line.startswith("v "), p.stdout.splitlines()))[0][2:]
            self.printTrueVariablesCompact(values)
            
    def printClauseToForceDifferentSolution(self, solution):
        """
        Prints a clause to force a different solution in the SAT problem.

        Args:
            solution (str): A string representing the current solution of the SAT problem.

        Raises:
            None

        Returns:
            None
        """
        otherSolClause = ""
        for svalue in solution.split(" "):
            value = int(svalue)
            if (value > 0):
                otherSolClause+=str(-value)+" "
        print(otherSolClause + "0")

    def printTrueVariables(self, solution):
        """
        Prints the variables that are assigned the value True in the solution of the SAT problem.

        Args:
            solution (str): A string representing the current solution of the SAT problem.

        Raises:
            None

        Returns:
            None
        """
        #print("The following variables are assigned the value True:")
        #logging.info("The following variables are assigned the value True:")
        for svalue in solution.split(" "):
            value = int(svalue)
            if (value > 0):
                trueVal = self.intToVariable(value)
                #logging.info(trueVal)
                #print(trueVal)
                self.trueValues.append(trueVal)
            elif (value < 0):
                falseValue = self.intToVariable(int(-value))
                self.falseValues.append(falseValue)
        for svalue in solution.split(" "):
            value = int(svalue)
            if (value > 0):
                #logging.info(value)
                pass

                
    def printTrueVariablesCompact(self, solution):
        """
        Prints the variables that are assigned the value True in the solution of the MAX-SAT problem.

        Args:
            solution (str): A string representing the current solution of the MAX-SAT problem.

        Raises:
            None

        Returns:
            None
        """
        print("The following variables are assigned the value True:")
        for index in range(len(solution)):
            if (solution[index] == "1"):
                print(self.intToVariable(index+1))
