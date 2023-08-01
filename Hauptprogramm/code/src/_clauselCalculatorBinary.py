
class ClauselCalculateBinary:
    def __init__(self):
        self.clauses = []
        "(d | !a | !b) & (!a | !b | !e) & (!a | !b | !f)"
        "((~ a) | (~ b) | d) & ((~ a) | (~ b) | (~ e)) & ((~ a) | (~ b) | (~ f))"
        test = "((~ a) | (~ b) | d) & ((~ a) | (~ b) | (~ e)) & ((~ a) | (~ b) | (~ f)) & (a | (~ d) | e | f) & (b | (~ d) | e | f)"

    def _createTheBinaryVariables(self, declareVariablesInSATHelper):
        """
        Create a list of all binary variables in the playfield map and declare them with the solver.

        This method populates the 'allBinaryVariableName' list with all binary variables in the'mapPlayfield'
        dictionary, flattens the list of variables, and declares the variables with the solver by
        calling the 'declareVariableList' method of the'sh' object.

        Args:
            None.

        Raises:
            None.

        Returns:
            None.
        """
        self.allBinaryVariableName = []
        self.mapTemporaryVarToBinary = {}
        self.mapTemporaryVarToBinaryNotUsed = {}

        self.mapBinaryForAllUsedVariables = {}
        self.mapBinaryForNotUsedVariables = {}

        self.mapBinaryToExpression = {}
        self.allContentFromAllPixels = []

        logging.debug(
            "alle Variablen sollten in der map gespeichert sein, es werden alle variablen der einfachheit halber in eine liste gespeichert")
        for key in self.mapPlayfield:
            listOfElementsOfAnPixel = list(self.mapPlayfield[key])
            self.allContentFromAllPixels = self.allContentFromAllPixels + listOfElementsOfAnPixel
            numberOfAllElementsOfThatPixel = len(listOfElementsOfAnPixel)
            nextPowerOfTwo = self.next_power_of_two(numberOfAllElementsOfThatPixel)

            for number in range(0, numberOfAllElementsOfThatPixel):
                # bauen der binären Variablen
                binVar = "g" + key
                binVar += "b[" + self.create_binary_encoding(nextPowerOfTwo, number) + "]"
                binVar += "o{" + listOfElementsOfAnPixel[number] + "}"
                binVar = binVar.replace("[", "_").replace(",", "_").replace("]", "_").replace("}", "_").replace("{",
                                                                                                                "_")

                self.mapTemporaryVarToBinary[listOfElementsOfAnPixel[number]] = binVar

            tempList = []
            for number in range(numberOfAllElementsOfThatPixel, nextPowerOfTwo):
                binVar = "g" + key
                binVar += "b[" + self.create_binary_encoding(nextPowerOfTwo, number) + "]"
                binVar += "newVariable"
                binVar = binVar.replace("[", "_").replace(",", "_").replace("]", "_")
                tempList.append(binVar)

            self.mapTemporaryVarToBinaryNotUsed[key] = tempList

        # MAP FROM BINARY VARIABLES ARE FILLED AND NEEDED TO BE TRANSFORMED TO SIMPLE BINARY VARIABLES

        self.mapBinaryForAllUsedVariables = self.process_map(self.mapTemporaryVarToBinary)

        # TODO VARIABLEN VERBIETEN, DIE NICHT AUFGERUFEN WERDEN
        # wenn der Raum von bspw 128 nicht erreicht wurde, müssen die variablen blockiert werden:
        # neue variable hinzufügen und in binäre Variablen transformiert

        self.mapBinaryForNotUsedVariables = self.process_map_with_list(self.mapTemporaryVarToBinaryNotUsed)

        # variable muss negiert werden, um anschließend mit DeMorgan Variablen aufgelöst zu werden
        # d.h. klausel-liste sieht dann nur so aus ~g[X,Y]b[binary]newVariable

        self.mapBinaryToExpression = self.translateToExpression(self.mapBinaryForAllUsedVariables,
                                                                self.mapBinaryForNotUsedVariables)

        self.allBinaryVariableName = self.getAllUniqueVariableNames(self.mapBinaryForNotUsedVariables,
                                                                    self.mapBinaryForAllUsedVariables)
        self.allBinaryVariableName = sorted(self.allBinaryVariableName)

        if declareVariablesInSATHelper:
            self.sh.declareVariableList(self.allBinaryVariableName)

        duplicates = []
        for item in self.allContentFromAllPixels:
            if self.allContentFromAllPixels.count(item) > 1 and item not in duplicates:
                duplicates.append(item)

    def _createNewVarClauses(self):
        """
         sinn der Methode ist folgendes :
         die newVariablen die erstellt wurden, müssen nun in die Klauseln hinzugefügt werden.
         ein Beispiel :
          -newVariable => -( -p00b1 & -p00b2) => -(-p00b1) v -(-p00b2) => p00b1 v p00b2
         Länger als die Anzahl an Bytes also faktor 2^x (d.h. länger als x) wird das nicht für createNewVarClauses
        """

        combined_list = []
        for key in self.mapBinaryForNotUsedVariables:
            elements = self.mapBinaryForNotUsedVariables[key]
            content = " & ".join(f"({element})" for element in elements)
            combined_expression = f"~({content})"
            combined_list.append(combined_expression)

        simplified = self.simplifyExpressions(combined_list)
        exprResultStr = self.sympyListToStrList(simplified)
        clauselList = self.prepareExprForClauses(expr_components=exprResultStr)

        self.sh.addClauseForThePossiblePlaystone(clauselList)
        # self.mapBinaryForNotUsedVariables

    def _createBinaryClauses(self, declareVariablesInSATHelper):
        # alle Regeln werden hier jetzt in binäre Variablen umgewandelt
        logging.debug("Now we are creating the eqivalent clauseln")

        self.allBinaryEquivalentClauselLists = copy.deepcopy(self.allEquivalentClauselLists)

        # doppelt verschachtelte Elemente werden in eine einfache Liste gespeichert
        # bsp [[A],[B, C]] -> [A, B, C]
        new_list = []
        for item in self.allBinaryEquivalentClauselLists:
            if isinstance(item, list):
                for subitem in item:
                    new_list.extend(subitem)
            else:
                new_list.append(item)

        self.compare_lists(new_list, self.allContentFromAllPixels)

        self.allBinaryEquivalentClauselLists = self.replaceElementsWithDictValues(self.allBinaryEquivalentClauselLists,
                                                                                  self.mapBinaryToExpression)

        for spielSteinBinaryEquivalentList in self.allBinaryEquivalentClauselLists:
            for oneBinaryEquivalentList in spielSteinBinaryEquivalentList:
                if declareVariablesInSATHelper:
                    result = self.equivalentListElements(oneBinaryEquivalentList)

                    resultCNF = sp.to_cnf(result)

                    # TODO save the equivalent output from self.equivalentListElements(oneEquivalentList) in a datastructure
                    # self.sh.addEquivalentList(oneEquivalentList)
                    # TODO TAKE OUT OF COMMENT IF NEEDED !!!!
                    # self.sh.addBinaryEquivalent(resultCNF)
                    # print(resultCNF)


    def compare_lists(self, list1, list2):
        # Check if all elements in list1 are in list2
        for elem in list1:
            if elem not in list2:
                print(f"list2 is missing element {elem}")

        # Check if all elements in list2 are in list1
        for elem in list2:
            if elem not in list1:
                print(f"list1 is missing element {elem}")

    def replaceElementsWithDictValues(self, allBinaryEquivalentClauselLists, value_dict):

        #result = value_dict['p[0,0]s4er1l[1,0]g[1,0]']

        for i in range(0, len(allBinaryEquivalentClauselLists)):
            for j in range(0, len(allBinaryEquivalentClauselLists[i])):
                for k in range(0, len(allBinaryEquivalentClauselLists[i][j])):
                    result = value_dict[allBinaryEquivalentClauselLists[i][j][k]]
                    allBinaryEquivalentClauselLists[i][j][k] = value_dict[allBinaryEquivalentClauselLists[i][j][k]]

        #for i, outer_list in enumerate(allBinaryEquivalentClauselLists):
        #    for j, inner_list in enumerate(outer_list):
        #        if isinstance(inner_list, list):
        #            for k, element in enumerate(inner_list):
        #                if element in value_dict:
        #                    allBinaryEquivalentClauselLists[i][j][k] = value_dict[element]
        #        else:
        #            if inner_list in value_dict:
        #                allBinaryEquivalentClauselLists[i][j] = value_dict[inner_list]
        return allBinaryEquivalentClauselLists

    def translateToExpression(self, mapBinaryForAllUsedVariables, mapBinaryForNotUsedVariables):
        new_map = {}

        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Prepare data for all used variables
            used_var_futures = {executor.submit(self.combine_expression_list, value): key
                                for key, value in mapBinaryForAllUsedVariables.items()}
            # Prepare data for not used variables
            not_used_var_futures = {executor.submit(self.negate_combined_expression_list, value): key
                                    for key, value in mapBinaryForNotUsedVariables.items()}

            # Process all used variables
            for future in concurrent.futures.as_completed(used_var_futures):
                key = used_var_futures[future]
                new_map[key] = sp.sympify(future.result())

            # Process not used variables
            for future in concurrent.futures.as_completed(not_used_var_futures):
                key = not_used_var_futures[future]
                new_map[key] = future.result()

        return new_map

    def negate_combined_expression_list(self, expression_List):
        combined_expr = self.combine_expression_list(expression_List)
        return self.negate_expression(combined_expr)

    def getAllUniqueVariableNames(self, mapBinaryForNotUsedVariables, mapBinaryForAllUsedVariables):
        all_vars = set()

        any_key_exists = any(key in mapBinaryForAllUsedVariables for key in mapBinaryForNotUsedVariables)
        print(any_key_exists)
        if any_key_exists:
            raise ValueError("mapBinaryForAllUsedVariables and mapBinaryForNotUsedVariables are not compatible",
                             mapBinaryForAllUsedVariables, " ", mapBinaryForNotUsedVariables)
        merged_dict = {**mapBinaryForNotUsedVariables, **mapBinaryForAllUsedVariables}

        # Iterate through the values in both dictionaries
        for key, value in merged_dict.items():
            for var in value:
                # Remove the '~' symbol and add the variable to the set
                all_vars.add(var.replace('~', ''))

        return all_vars

    def equivalentListElements(self, equivalentList):
        result = []
        firstElement = equivalentList[0]
        for index in range(1, len(equivalentList)):
            logging.debug("add Äquivalenz " + str(firstElement) + " <==> " + str(equivalentList[index]))
            result.append(Equivalent(firstElement, equivalentList[index]))

        if len(result) == 0 and len(equivalentList) == 1:
            return equivalentList[0]

        finalExpression = result[0]
        for index in range(1, len(result)):
            logging.debug("add Äquivalenz " + str(finalExpression) + " <==> " + str(result[index]))
            finalExpression = And(finalExpression, result[index])

        return finalExpression

    def get_cnf(self, expression):
        return sp.to_cnf(expression)

    def combine_expression_list(self, expression_List):
        combined_expr = " & ".join([f"({expr})" for expr in expression_List])
        return combined_expr

    def negate_expression(self, expr):
        expr = expr.replace("[", "_").replace(",", "_").replace("]", "_")

        sym_expr = sp.sympify(expr)

        # Negate the expression
        negated_expr = ~sym_expr

        # Return the negated expression as a string
        return negated_expr

    def negate_expression_list(self, expr_list):
        # Negate every expression in the list using the negate_expression method
        negated_expr_list = [self.negate_expression(expr) for expr in expr_list]

        # Return the list of negated expressions
        return negated_expr_list

    def extract_values(self, item):
        """
        Extracts three values (x, y, binary) from a string argument that matches a certain pattern.

        Parameters:
            item (str): A string that should match the pattern 'g[x,y]b[0-1]+'.

        Returns:
            Tuple[str, str, str] or None: If the input string matches the pattern, returns a tuple containing three strings: x, y, and binary. Otherwise, returns None.
        """

        pattern = r'g_(\d+)_(\d+)_b_([01]+)_'
        match = re.match(pattern, item)
        if match:
            x, y, binary = match.groups()
            return x, y, binary
        return None

    def binary_string_mapping(self, binary_string, prefix):
        """
        Maps each digit in a binary string to a corresponding string containing a prefix and the index of the digit.

        Parameters:
            binary_string (str): A string of 0's and 1's.
            prefix (str): A prefix string to be used in the resulting strings.

        Returns:
            List[str]: A list of strings, where each string is formed by concatenating the prefix with an index and a 'b' or '!b', depending on the corresponding digit in the binary string.
        """
        mapped = []
        for i, bit in enumerate(binary_string, start=1):
            if bit == '0':
                mapped.append('~{}b{}'.format(prefix, i))
            elif bit == '1':
                mapped.append('{}b{}'.format(prefix, i))
        return mapped

    def process_map_with_list(self, input_map):
        new_map = {}
        for key, values in input_map.items():
            for value in values:
                tempList = [value]
                new_value = self.process_items(tempList)
                new_map[value] = new_value[value]
        return new_map

    def process_map(self, input_map):
        new_map = {}
        for key, value in input_map.items():
            tempList = [value]
            new_value = self.process_items(tempList)
            new_map[key] = new_value[value]
        return new_map

    def process_items(self, tempList):
        """
        Iterates through a list of strings, extracts values using the extract_values function, maps the binary values using the binary_string_mapping function, and returns a dictionary of mappings.

        Parameters:
            tempList (List[str]): A list of strings to be processed.

        Returns:
            Dict[str, List[str]]: A dictionary where each key is a string from tempList and each value is a list of strings resulting from mapping the binary value in the corresponding string.
        """
        map = {}
        for item in tempList:
            values = self.extract_values(item)
            if values:
                x, y, binary = values
                prefix = 'g_{}_{}_'.format(x, y)
                mapped_binary = self.binary_string_mapping(binary, prefix)
                map[item] = mapped_binary
        return map

    def create_binary_encoding(self, power, num):
        """
        Create binary encoding of a given decimal number for a given power of 2.
        Args:
            power (int): The power of 2 to which the number must be encoded.
            num (int): The decimal number to be encoded.

        Returns:
            str: The binary encoding of the given decimal number for the given power of 2.
        """

        num_bits = power.bit_length() - 1
        binary_encoding = format(num, f'0{num_bits}b')
        return binary_encoding

    def next_power_of_two(self, n):
        """
        next_power_of_two(n)

        Computes the next power of 2 that is greater than or equal to the input integer.

        Args:
        n (int): The input integer.

        Returns:
        int: The next power of 2 that is greater than or equal to n.

        Examples:
        >>> next_power_of_two(10)
        16
        >>> next_power_of_two(17)
        32
        >>> next_power_of_two(1)
        1
        """
        p = 1
        while p < n:
            p <<= 1
        return p

    def transformSymPyExpressionForNewData(self, data_structure):
        result = []
        for outer_list in data_structure:
            new_outer_list = []
            for inner_list in outer_list:
                new_inner_list = f"({') & ('.join(inner_list)})"
                new_outer_list.append(new_inner_list)
            result.append(new_outer_list)
        return result

    def combineSymPyExpressionForNewData(self, expression_list):
        result = []
        for inner_list in expression_list:
            combined_expression = f"Equivalent(({inner_list[0]}), ({inner_list[1]}))"
            #combined_expression = "((~A) | C) & (A | (~C))"
            #temp1 = str(sp.to_cnf("~(" + inner_list[0] + ")"))
            #temp2 = str(sp.to_cnf("~(" + inner_list[1] + ")"))
            #temp3 = str(sp.to_cnf("(" + inner_list[0] + ")"))
            #temp4 = str(sp.to_cnf("(" + inner_list[1] + ")"))
            #combined_expression = combined_expression.replace("(~A)", "(" + temp1 + ")")
            #combined_expression = combined_expression.replace("(~C)", "(" + temp2 + ")")
            #combined_expression = combined_expression.replace("A", "(" + temp3 + ")")
            #combined_expression = combined_expression.replace("C", "(" + temp4 + ")")
            #cnf_sp = sp.sympify(combined_expression)
            #cnf_sp = sp.to_cnf(cnf_sp)
            #cnf_sp = str(cnf_sp)
            result.append(combined_expression)
        return result

    def simplifyEquivalentExpressions(self, expr_list):
        simplified_list = []
        counts = self.countUniqueSympyVariables(expr_list)
        if self.count > 700:
            logging.info("simplified_list " + str(self.count) + " = " + str(expr_list))

        for index in range(len(expr_list)):
            #simplified_expr = sp.simplify(expr)
            #simplified_cnf_expr = sp.simplify(sp.to_cnf(expr))
            expr = expr_list[index]
            count = counts[index]
            cnf_expr = None


            if count <= 3:
                cnf_expr = sp.to_cnf(expr)
            else :
                nnf = ccNNF._ccNNF()
                cnf_expr = nnf.process_formula(expr)
                #tseitin = _Tseitin()
                #cnf_expr = tseitin.tseitin_calculator(expr)

            simplified_list.append(cnf_expr)
            logging.info("simplified_list " + str(self.count) + " = " + str(simplified_list))
            self.count += 1
        return simplified_list

    def generate_equivalent_sympy_expression(self, new_data_structure):
        # Erstellen einer Liste von kombinierten Ausdrücken für jede verschachtelte Liste in new_data_structure
        transformed_expression_list = self.transformSymPyExpressionForNewData(new_data_structure)
        equivalent_expressions = self.combineSymPyExpressionForNewData(transformed_expression_list)
        simplifyed = self.simplifyEquivalentExpressions(equivalent_expressions)
        exprResultStr = self.sympyListToStrList(simplifyed)
        clauselList = self.prepareEquivalentExprForClauses(expr_components=exprResultStr)

        return clauselList

    def _createTheEquivalentsBinaryEdition(self):
        logging.debug("Now we are creating the eqivalent clauseln")
        for spielSteinEquivalentList in self.allEquivalentClauselLists:
            new_data_structure = []
            for oneEquivalentList in spielSteinEquivalentList:
                if len(oneEquivalentList) <= 1:
                    continue

                oneElement = []
                for key in oneEquivalentList:
                    if key in self.mapBinaryForAllUsedVariables:
                        oneElement.append(self.mapBinaryForAllUsedVariables[key])

                new_data_structure.append(oneElement)

            result = self.generate_equivalent_sympy_expression(new_data_structure)
            if len(result) > 0:
                tseitin_var_list = self.tseitin_vars(result)
                self.sh.declareVariableList(tseitin_var_list)
                self.sh.generateEquivalentsOutOfSympy(result)
    #self.sh.addEquivalentList(oneEquivalentList)

    def _createExactlyOneForThePixelsBinaryEdition(self):
        # print("Now we are creating the Exactly One OR At Most One for each pixel")
        logging.debug("Now we are creating the Exactly One OR At Most One for each pixel")
        extractedResult = []
        for key in self.mapPlayfield:
            content = self.mapPlayfield[key]
            if not content == []:

                output_list = self.addAtMostOneNested(content)

                result = self.replaceVarFromExactlyOneForThePixels(output_list, self.mapBinaryForAllUsedVariables)

                expressionList = self.joinElementsWithOr(result)
                extractedResult.append(self.simplifyExpressions(expressionList))

                logging.debug("addAtMostOne added for " + str(content))
                #self.sh.addAtMostOne(content)  # TODO or exact one if you just want that it should
                # TODO solve if everything is filled
                # logging.debug("addExactlyOne added for " + str(content))
                # self.sh.addExactlyOne(content) #TODO THIS HERE

    def _createExactlyOneForThePossiblePlaystoneBinaryEdition(self):
        logging.debug("Für jeden Spielstein, werden alle möglichen Positionen mit exactly one verknüpft."
                      "\nd.h. für jeden Spielstein darf nur ein stein plaziert werden.")
        # print("Für jeden Spielstein, werden alle möglichen Positionen mit exactly one verknüpft."
        #      "\nd.h. für jeden Spielstein darf nur ein stein plaziert werden.")
        extractedResult = []
        for firstPixelList in self.allFirstPixelLists:
            # print("firstPixelList " + str(firstPixelList))
            logging.debug("excatlyOne for = " + str(firstPixelList))

            # Exactly One ist eine AtMostOne und hinzufüden der Klausel
            # d.h. zuerst muss AtMostOne hinzugefügt werden und addClausel

            # atMostOne Functionality
            output_list = self.addAtMostOneNested(firstPixelList)
            # print(output_list)

            result = self.replaceVarFromExactlyOneForThePixels(output_list, self.mapBinaryForAllUsedVariables)

            expressionList = self.joinElementsWithOr(result)
            expressionResult = self.simplifyExpressions(expressionList)
            expressionResultStr = self.sympyListToStrList(expressionResult)
            #expressionResult = expressionResult.replace("[", "").replace("]", "")
            extractedResult.append(expressionResultStr)
            # print("extractedResult " + str(expressionResultStr))
            # TODO das ergebnis muss in sh gespeichert werden !!!! TODO!!!!
            self.sh.addatMostOneForThePossiblePlaystone(expressionResultStr)

        # add clause
        # Ersetzen der Werte in allFirstPixelLists mit den zugehörigen Werten aus dem dict
        replaced_lists = [[self.mapBinaryForAllUsedVariables[key] for key in sublist] for sublist in self.allFirstPixelLists]

        translated = self.translateAddClauseForThePossiblePlaystone(replaced_lists)
        simplifyed = self.simplifyExpressions(translated)
        exprResultStr = self.sympyListToStrList(simplifyed)
        clauselList = self.prepareExprForClauses(expr_components=exprResultStr)

        tseitin_variables = self.tseitin_vars(clauselList)
        self.sh.declareVariableList(tseitin_variables)
        self.sh.addClauseForThePossiblePlaystone(clauselList)

        # Funktion zum Ersetzen der binären Variablen in den Listen mit Sympy "True" oder "False"
        def replace_with_sympy_true_false(self, binary_var_list, true_values):
            replaced_list = []

            for var in binary_var_list:
                if var.startswith("~"):
                    original_var = var[1:]
                    if original_var in true_values:
                        replaced_list.append(symbols('False'))
                    else:
                        replaced_list.append(symbols('True'))
                else:
                    if var in true_values:
                        replaced_list.append(symbols('True'))
                    else:
                        replaced_list.append(symbols('False'))

            return replaced_list

        def _extractBinaryInfos(self, trueValues: list):
            """
            Extracts information from a list of data.

            This method extracts information from a list of data, converts the data to a dictionary and uses it to create
            an image of the game field with all tetrominos in their final positions.

            Args:
                data_list (list): The list of data to extract information from.

            Returns:
                None.
            """
            if not self.sh.solution == "SATISFIABLE":
                return

            # Erstellen Sie Kopien der benötigten Dictionaries und Listen
            map_binary_for_all_used_variables_copy = dict(self.mapBinaryForAllUsedVariables)
            map_binary_for_not_used_variables_copy = dict(self.mapBinaryForNotUsedVariables)

            # Ersetzen der Variablen in den Kopien der Dictionaries
            for key in map_binary_for_all_used_variables_copy.keys():
                map_binary_for_all_used_variables_copy[key] = self.replace_with_sympy_true_false(
                    map_binary_for_all_used_variables_copy[key], self.sh.trueValues)

            for key in map_binary_for_not_used_variables_copy.keys():
                if key == "g_0_0_b_11111_newVariable":
                    print()
                map_binary_for_not_used_variables_copy[key] = self.replace_with_sympy_true_false(
                    map_binary_for_not_used_variables_copy[key], self.sh.trueValues)

            # Finden Sie die Maps, die nur aus Sympy True-Elementen bestehen, und speichern Sie sie in neuen Listen
            only_true_maps_for_all_used_variables = []
            only_true_maps_for_not_used_variables = []

            for key, values in map_binary_for_all_used_variables_copy.items():
                result = self.combine_expression_list(values)
                result = sp.sympify(result)
                if result == sp.true:
                    only_true_maps_for_all_used_variables.append(key)

            for key, values in map_binary_for_not_used_variables_copy.items():
                if key == "g_0_0_b_11111_newVariable":
                    print()
                result = self.combine_expression_list(values)
                result = sp.sympify(result)
                if result == sp.true:
                    only_true_maps_for_not_used_variables.append(key)

            result = {}
            mapSpielsteine = {}
            p_pattern = r'p\[(.*?)\]'
            s_pattern = r's(.*?)l\['
            l_pattern = r'l\[(.*?)\]'
            g_pattern = r'g\[(.*?)\]'
            for data in only_true_maps_for_all_used_variables:
                p = re.search(p_pattern, data).group(1)
                s = re.search(s_pattern, data).group(1)
                l = re.search(l_pattern, data).group(1)
                g = re.search(g_pattern, data).group(1)

                globalVal = "[" + g + "]"
                if globalVal in result:
                    logging.debug("ERROR : " + str(globalVal) + " is part of " + str(result) + ". But should not.")

                result[globalVal] = [p, s, l, g]

                globalContent = self._strToList(globalVal)
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

    def _createLogic(self):
        """
        Creates all the clauses necessary for the SAT solver to solve the puzzle.
        """
        logging.info(" - create Variables - ")
        self.binaryMode = True
        "this call is only neccesary to create the normal variable names"

        time_calculator_createTheVariables = TimeCalculator()
        time_calculator_createTheVariables.start_with_task_name("#1570# \" _createTheVariables \"")
        try:
            self._createTheVariables(declareVariablesInSATHelper=not self.binaryMode)
        except TimeoutError:
            print("Timeout of " + str(time_calculator_createTheVariables.max_time) + "s for \"" + str(
                time_calculator_createTheVariables.task_name) + "\" reached, terminating code. No Solution found in that time")
        finally:
            time_calculator_createTheVariables.stop()
            time_duration = time_calculator_createTheVariables.get_duration()
            print(time_duration)
            logging.info(time_duration)

        "this call is creating the binary variable names out of the call before"
        time_calculator_createTheBinaryVariables = TimeCalculator()
        time_calculator_createTheBinaryVariables.start_with_task_name("#1571# \" _createTheBinaryVariables \"")
        try:
            self._createTheBinaryVariables(declareVariablesInSATHelper=self.binaryMode)
        except TimeoutError:
            print("Timeout of " + str(time_calculator_createTheBinaryVariables.max_time) + "s for \"" + str(
                time_calculator_createTheBinaryVariables.task_name) + "\" reached, terminating code. No Solution found in that time")
        finally:
            time_calculator_createTheBinaryVariables.stop()
            time_duration = time_calculator_createTheBinaryVariables.get_duration()
            print(time_duration)
            logging.info(time_duration)

        time_calculator_createNewVarClauses = TimeCalculator()
        time_calculator_createNewVarClauses.start_with_task_name("#1572# \" _createNewVarClauses \"")
        try:
            self._createNewVarClauses()
        except TimeoutError:
            print("Timeout of " + str(time_calculator_createNewVarClauses.max_time) + "s for \"" + str(
                time_calculator_createNewVarClauses.task_name) + "\" reached, terminating code. No Solution found in that time")
        finally:
            time_calculator_createNewVarClauses.stop()
            time_duration = time_calculator_createNewVarClauses.get_duration()
            print(time_duration)
            logging.info(time_duration)

        time_calculator_createBinaryClauses = TimeCalculator()
        time_calculator_createBinaryClauses.start_with_task_name("#1573# \" _createBinaryClauses \"")
        try:
            self._createBinaryClauses(declareVariablesInSATHelper=self.binaryMode)
        except TimeoutError:
            print("Timeout of " + str(time_calculator_createBinaryClauses.max_time) + "s for \"" + str(
                time_calculator_createBinaryClauses.task_name) + "\" reached, terminating code. No Solution found in that time")
        finally:
            time_calculator_createBinaryClauses.stop()
            time_duration = time_calculator_createBinaryClauses.get_duration()
            print(time_duration)
            logging.info(time_duration)

        time_calculator_createTheEquivalentsBinaryEdition = TimeCalculator()
        time_calculator_createTheEquivalentsBinaryEdition.start_with_task_name("#1574# \" _createTheEquivalentsBinaryEdition \"")
        try:
            self._createTheEquivalentsBinaryEdition()
            print("ok")
        except TimeoutError:
            print("Timeout of " + str(time_calculator_createTheEquivalentsBinaryEdition.max_time) + "s for \"" + str(
                time_calculator_createTheEquivalentsBinaryEdition.task_name) + "\" reached, terminating code. No Solution found in that time")
        finally:
            time_calculator_createTheEquivalentsBinaryEdition.stop()
            time_duration = time_calculator_createTheEquivalentsBinaryEdition.get_duration()
            print(time_duration)
            logging.info(time_duration)

        time_calculator_createExactlyOneForThePixelsBinaryEdition = TimeCalculator()
        time_calculator_createExactlyOneForThePixelsBinaryEdition.start_with_task_name("#1575# \" _createExactlyOneForThePixelsBinaryEdition \"")
        try:
            self._createExactlyOneForThePixelsBinaryEdition()
            print("ok")
        except TimeoutError:
            print("Timeout of " + str(time_calculator_createExactlyOneForThePixelsBinaryEdition.max_time) + "s for \"" + str(
                time_calculator_createExactlyOneForThePixelsBinaryEdition.task_name) + "\" reached, terminating code. No Solution found in that time")
        finally:
            time_calculator_createExactlyOneForThePixelsBinaryEdition.stop()
            time_duration = time_calculator_createExactlyOneForThePixelsBinaryEdition.get_duration()
            print(time_duration)
            logging.info(time_duration)

        time_calculator_createExactlyOneForThePossiblePlaystoneBinaryEdition = TimeCalculator()
        time_calculator_createExactlyOneForThePossiblePlaystoneBinaryEdition.start_with_task_name("#1576# \" _createExactlyOneForThePossiblePlaystoneBinaryEdition \"")
        try:
            self._createExactlyOneForThePossiblePlaystoneBinaryEdition()
            print()
        except TimeoutError:
            print("Timeout of " + str(time_calculator_createExactlyOneForThePossiblePlaystoneBinaryEdition.max_time) + "s for \"" + str(
                time_calculator_createExactlyOneForThePossiblePlaystoneBinaryEdition.task_name) + "\" reached, terminating code. No Solution found in that time")
        finally:
            time_calculator_createExactlyOneForThePossiblePlaystoneBinaryEdition.stop()
            time_duration = time_calculator_createExactlyOneForThePossiblePlaystoneBinaryEdition.get_duration()
            print(time_duration)
            logging.info(time_duration)

        self.sh.printFormulaFile(folder=self.image.folderName, filename="_file_problem.cnf")
        print("printed formula")

        print("started Solving Sat please wait ...")
        logging.info("started Solving Sat please wait ...")

        time_calculator_SAT_Solver = TimeCalculator(max_time=self.maxTime)
        time_calculator_SAT_Solver.start_with_task_name("CNF NNF")

        try:
            self.sh.solveSatPath(folder=self.image.folderName, filename="_file_problem")

        except TimeoutError:
            print("Timeout of " + str(time_calculator_SAT_Solver.max_time) + "s for \"" + str(
                time_calculator_SAT_Solver.task_name) + "\" reached, terminating code. No Solution found in that time")

        finally:
            time_calculator_SAT_Solver.stop()
            time_duration = time_calculator_SAT_Solver.get_duration()
            print(time_duration)
            logging.info(time_duration)

        print("SAT finished")
        logging.info("SAT finished")

        logging.info("self.sh.trueValues" + str(self.sh.trueValues))
        self._extractBinaryInfos(self.sh.trueValues)

        print("Program finished")
        logging.info("Program finished")