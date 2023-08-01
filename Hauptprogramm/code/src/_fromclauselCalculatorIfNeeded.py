def _createVariableName(self, spielsteinTyp: Spielstein, spielsteinIndex: int) -> None:
    """
    Create a list of all variables in the playfield map and declare them with the solver.
    This method populates the 'allVariableName' list with all variables in the 'mapPlayfield'
        dictionary, flattens the list of variables, and declares the variables with the solver by
        calling the 'declareVariableList' method of the 'sh' object.

    Args:
        None

    Raises:
        None

    Returns:
        None
    """
    if not isinstance(spielsteinTyp, Spielstein) or not isinstance(spielsteinIndex, int):
        raise TypeError

    logging.debug("hier wird der Variablenname zusammengebaut")
    # p steht für Pixelposition
    # X Y sind die Koordinaten von den Pixelpositionen
    # s = Spielstein
    # "Name" = Name des Spielsteins
    # "Nummer" = Nummer des Spielsteins, es können ja mehrere Spielsteine existieren
    # l = lokale Pixelnummerierung
    # "lokale Nummerierung" = durch Nummerierung der aktiven Blöcke
    # pXYs"Name""Nummer"l"lokale Nummerierung."
    for pixelPosition in spielsteinTyp.alleMoeglichenPlaziertenSteine:
        newStringList = []
        # logging.debug("Position vom Spielstein " + str(pixelPosition))
        # logging.debug(spielsteinTyp.alleMoeglichenPlaziertenSteine[pixelPosition])

        firstPixel = True

        for actualPosIndex in range(len(spielsteinTyp.alleMoeglichenPlaziertenSteine[pixelPosition])):
            actualPos = spielsteinTyp.alleMoeglichenPlaziertenSteine[pixelPosition][actualPosIndex]
            actualPosStr = self._listToStr(actualPos)
            # print(actualPosStr)
            # print(actualPos)
            pixelPrefix = "p"
            pixelCoordinate = pixelPosition
            pixelString = pixelPrefix + pixelCoordinate

            spielsteinPrefix = "s"
            spielsteinName = spielsteinTyp.name
            spielsteinNummer = spielsteinIndex + 1
            spielString = spielsteinPrefix + spielsteinName + str(spielsteinNummer)

            localSpielsteinPrefix = "l"
            localSpielsteinNummer = self._listToStr(spielsteinTyp.activeBlocks[actualPosIndex])
            localSpielsteinString = localSpielsteinPrefix + localSpielsteinNummer

            globalSpielsteinPrefix = "g"
            globalSpielsteinNummer = actualPosStr
            globalSpielsteinString = globalSpielsteinPrefix + globalSpielsteinNummer

            res = pixelString + spielString + localSpielsteinString + globalSpielsteinString

            # logging.debug("result variable: " + res)
            # print("result variable: " + res)

            newStringList.append(res)
            self.mapPlayfield[actualPosStr].append(res)
            # print("mapPlayfield"+ actualPosStr +" : " + str(self.mapPlayfield[actualPosStr]))
            # logging.debug("mapPlayfield"+ actualPosStr +" : " + str(self.mapPlayfield[actualPosStr]))
            if firstPixel:
                firstPixel = False
                spielsteinTyp.firstPixelList[spielsteinIndex].append(res)

        # logging.debug("newStringList " + str(newStringList))
        # print("newStringList " + str(newStringList))
        spielsteinTyp.equivalentClauselList[spielsteinIndex].append(newStringList)
        # logging.debug("equivalentClauselList: " + str(spielsteinTyp.equivalentClauselList[spielsteinIndex]))
        # print("equivalentClauselList: " + str(spielsteinTyp.equivalentClauselList[spielsteinIndex]))
        # print("firstPixelList: " + str(spielsteinTyp.firstPixelList[spielsteinIndex]))
        # print("mapPlayfield : " + str(self.mapPlayfield))
        # logging.debug("mapPlayfield : " + str(self.mapPlayfield))

        # print image for the Spielstein
        # img = ImageCreator("-")
        # self.image.createImgForSpielstein(fieldWidth=self.playfieldWidth,
        #                           fieldHeight=self.playfieldHeight,
        #                           fileName=res+".png",
        #                           folderName=self.image.folderName,
        #                           elemList=spielsteinTyp.alleMoeglichenPlaziertenSteine[pixelPosition],
        #                           color=(255, 0, 0))


# def translateToExpression2(self, mapBinaryForAllUsedVariables, mapBinaryForNotUsedVariables):
    #     new_map = {}
    #     #count = 0
    #     for key, value in mapBinaryForAllUsedVariables.items():
    #         #if count <= 3:
    #         combined_value = self.combine_expression_list(value)
    #         new_map[key] = sp.sympify(combined_value)
    #         #count += 1
    #
    #     #count = 0
    #     # negiere die variable
    #     for key, value in mapBinaryForNotUsedVariables.items():
    #         #if count <= 3:
    #         combined_value = self.combine_expression_list(value)
    #         new_map[key] = self.negate_expression(combined_value)
    #         #count += 1
    #
    #     return new_map

    # def get_atom(self, expression):
    #     return expression.atom()
    #
    # def get_Symbol(self, singleVariable: str):
    #     return sp.symbols(singleVariable)
    #
    # def expression_equals(self, expr1, expr2):
    #     return expr1.equals(expr2)

    # def get_equivalent(self, expr1, expr2):
    #     return sp.Equivalent(expr1, expr2)

    # def get_truth_table2(self, expression):
    #     variables = sorted(list(expression.free_symbols), key=lambda x: x.name, reverse=True)
    #     return variables, list(truth_table(expression, variables))
    #
    # def print_truth_table(self, table, variables, expression):
    #     print(f"[{', '.join(str(var) for var in variables)}] -> {expression}")
    #     self.print_truth_table_only(table)
    #     # for row in table:
    #     #    assignments, result = row[:-1], row[-1]
    #     #    print(f"{assignments} -> {result}")
    #
    # def print_truth_table_only(self, table):
    #     for t in table:
    #         print("{0} -> {1}".format(*t))
    #
    # def get_truth_table_reverse(self, expression, reverse=False):
    #     variables = sorted(list(expression.free_symbols), key=lambda x: x.name, reverse=reverse)
    #     return variables, list(truth_table(expression, variables))
    #
    # def print_truth_table_reverse(self, table, variables, expression, reverse=False):
    #     print(f"[{', '.join(str(var) for var in variables)}] -> {expression}")
    #     self.print_truth_table_only_reverse(table, reverse)
    #
    # def print_truth_table_only_reverse(self, table, reverse=False):
    #     for t in table:
    #         if reverse:
    #             t = (t[0][::-1], t[1])  # Reverse the variable assignments in each row
    #         print("{0} -> {1}".format(*t))

    # def generate_truth_table_parallel(self, expression, variables):
    #     num_variables = len(variables)
    #     truth_table = []
    #     all_combinations = list(itertools.product([0, 1], repeat=num_variables))
    #
    #     with concurrent.futures.ThreadPoolExecutor() as executor:
    #         futures = [executor.submit(self.evaluate_expression, expression, variables, values)
    #                    for values in all_combinations]
    #
    #         for future in concurrent.futures.as_completed(futures):
    #             truth_table.append(future.result())
    #
    #     return truth_table
    #
    # def evaluate_expression(self, expression, variables, values):
    #     expr_val = expression.subs(dict(zip(variables, values)))
    #     return tuple(map(int, values)) + (int(expr_val == sp.true),)

    # def get_truth_table(self, expression):
    #     variables = sorted(list(expression.free_symbols), key=lambda x: x.name, reverse=True)
    #     return variables, self.generate_truth_table_parallel(expression, variables)

    def generate_expression_from_true_rows(self, table, variables):
        expressions = []

        for row in table:
            assignments, result = row[:-1], row[-1]
            # assignmentsList = assignments[0]
            if not result:
                expr_parts = []
                for value, var in zip(assignments[0], variables):
                    if value:
                        expr_parts.append(f"Not({var})")
                    else:
                        expr_parts.append(str(var))
                expression = " | ".join(expr_parts)
                expressions.append(expression)

        return expressions


    def expression_replace_sign_in_list(self, expressionList, sign_should_be_replaced, replacement_sign):
        ### This function replaces all the sign (signShouldBeReplaced) from each element of the list with the replacementSign.
        new_list = []
        for expression in expressionList:
            new_expression = expression.replace(sign_should_be_replaced, replacement_sign)
            new_list.append(new_expression)
        return new_list

    def compare_truth_tables(self, tt1, tt2):
        if len(tt1) != len(tt2):
            return False

        for row1, row2 in zip(tt1, tt2):
            if row1 != row2:
                return False

        return True

# def string_to_sympy_logic(self, input_str):
    #     # Define symbols
    #     variables = sorted(list(set(re.findall(r'\b[A-Z]\b', input_str))))
    #     sym_vars = symbols(' '.join(variables))
    #     sym_dict = dict(zip(variables, sym_vars))
    #
    #     # Replace symbols and operators
    #     input_str = input_str.replace('~', 'Not(')
    #     input_str = input_str.replace('&', ', ')
    #     input_str = input_str.replace('|', ', ')
    #     input_str = input_str.replace('(', ' ( ')
    #     input_str = input_str.replace(')', ' ) ')
    #
    #     for var in variables:
    #         input_str = input_str.replace(var, f"{sym_dict[var]}")
    #
    #     # Convert to SymPy logical expression
    #     tokens = input_str.split()
    #     stack = []
    #     for token in tokens:
    #         if token == '(':
    #             stack.append(token)
    #         elif token == ')':
    #             while stack and stack[-1] != '(':
    #                 stack.pop()
    #             if stack and stack[-1] == '(':
    #                 stack.pop()
    #         elif token == 'Not(':
    #             stack.append(Not)
    #         elif token == ',':
    #             if stack and (stack[-1] == And or stack[-1] == Or):
    #                 stack.pop()
    #                 stack.append(Or)
    #             else:
    #                 stack.append(And)
    #         else:
    #             stack.append(sym_dict[token])
    #
    #     # Evaluate expression and return
    #     expr = stack.pop(0)
    #     for item in stack:
    #         if isinstance(item, Not):
    #             expr = item(expr)
    #         else:
    #             expr = Or(expr, item)
    #     return expr

    # def get_cnf2(self, expr):
    #     # Convert the input list to a string
    #     expr_str = ' & '.join(expr)
    #
    #     # Replace invalid characters and negation symbol
    #     expr_str = expr_str.replace('[', '_').replace(']', '_').replace(',', '_').replace('!', '~')
    #
    #     # Define the symbols in the expression
    #     symbols = {str(symb): symb for symb in sp.symbols(expr_str) if str(symb).startswith('g')}
    #
    #     # Parse the expression
    #     expr_parsed = sp.sympify(expr_str, locals=symbols)
    #
    #     # Convert the expression to CNF
    #     return sp.to_cnf(expr_parsed)

    # def is_equivalent(self, expr1, expr2):
    #     cnf_expr1 = sp.sympify(expr1)
    #     cnf_expr2 = sp.sympify(expr2)
    #
    #     # Get CNFs of the expressions
    #     cnf_expr1 = self.get_cnf(cnf_expr1)
    #     cnf_expr2 = self.get_cnf(cnf_expr2)
    #
    #     # Check if the CNFs are equivalent
    #     return cnf_expr1 == cnf_expr2

    # def compare_expressions(self, expr1, expr2):
    #     # Convert the expressions to SymPy format
    #     sym_expr1 = sp.sympify(expr1)
    #     sym_expr2 = sp.sympify(expr2)
    #
    #     # Simplify the expressions
    #     simplified_expr1 = sp.simplify(sym_expr1)
    #     simplified_expr2 = sp.simplify(sym_expr2)
    #
    #     # Compare if the simplified expressions are the same
    #     return simplified_expr1 == simplified_expr2

    # def truth_table(self, expression):
    #     variables = set(
    #         expression.replace('(', '').replace(')', '').replace('&', '').replace('|', '').replace('!', '').replace(' ',
    #                                                                                                                 ''))
    #     variables = sorted(variables, reverse=True)
    #     values = list(itertools.product([0, 1], repeat=len(variables)))
    #     table = []
    #     for value in values:
    #         row = list(value)
    #         for variable, v in zip(variables, value):
    #             expression = expression.replace(variable, str(v))
    #         expression = expression.replace('!', 'not ')
    #         row.append(int(eval(expression)))
    #         table.append(row)
    #     return (variables, table)
    #
    # def print_truth_table2(self, variables, table, expression):
    #     header = ' '.join(variables) + ' || ' + expression
    #     divider = '-' * len(header)
    #     print(header)
    #     print(divider)
    #     for row in table:
    #         values = ' '.join(str(v) for v in row[:-1])
    #         result = row[-1]
    #         print(f'{values} || {result}')
    #
    # def get_truth_table2(self, expr):
    #     symbols = list(set(''.join(expr).replace('!', '').replace('|', '').replace('&', '').replace(' ', '')))
    #     truth_table = {}
    #
    #     for values in itertools.product([False, True], repeat=len(symbols)):
    #         assignments = {symbols[i]: values[i] for i in range(len(symbols))}
    #         expr_values = [
    #             eval(term.replace('!', ' not ').replace('|', ' or ').replace('&', ' and '), None, assignments) for term
    #             in expr]
    #         truth_table[tuple(values)] = all(expr_values)
    #
    #     return truth_table
    #
    # def print_truth_table3(self, expr):
    #     if isinstance(expr, str):
    #         expr = [expr]
    #
    #     truth_table = self.get_truth_table(expr)
    #     symbols = sorted(list(
    #         set(''.join(expr).replace('!', '').replace('|', '').replace('&', '').replace('(', '').replace(')',
    #                                                                                                       '').replace(
    #             ' ', ''))), reverse=True)
    #
    #     header = " | ".join(symbols) + " | " + " | ".join(expr)
    #     print("Truth table for expr:")
    #     print(header)
    #     print('-' * len(header))
    #
    #     for values, results in truth_table.items():
    #         row = " | ".join(str(int(v)) for v in values) + " | " + " | ".join(str(int(r)) for r in results)
    #         print(row)

    # def is_equivalent2(self, expr1, expr2):
    #     truth_table1 = self.get_truth_table(expr1)
    #     truth_table2 = self.get_truth_table(expr2)
    #     return truth_table1 == truth_table2

    # def implies(self, expr1, expr2):
    #     # Define the string expression
    #     expr_str = f"Implies({expr1}, {expr2})"
    #
    #     # Convert the string to a SymPy expression
    #     implies_expr = sp.sympify(expr_str)
    #     return self.get_cnf(implies_expr)
    #
    #     # negated_expr1 = self.negate_expression(expr1)
    #     # combined_expr = negated_expr1 + expr2
    #     # return self.get_cnf(combined_expr)

    # def equivalent(self, expr1, expr2):
    #     expr1 = sp.sympify(expr1)
    #     expr2 = sp.sympify(expr2)
    #     result = Equivalent(expr1, expr2)
    #     return self.get_cnf(result)
    #     # implied_forward = self.implies(expr1, expr2)
    #     # implied_backward = self.implies(expr2, expr1)
    #     # combined_expr = list(implied_forward.args) + list(implied_backward.args)
    #     # return sp.to_cnf(sp.And(*combined_expr))

    # def string_to_sympy_bool_expr(self, input_str):
    #     input_str = input_str.replace("Not", "~").replace("Or", "|").replace("And", "&")
    #     sym_set = set(filter(str.isalpha, input_str))
    #     sym_dict = {sym: symbols(sym) for sym in sym_set}
    #
    #     sympy_expr = eval(input_str, {"__builtins__": None}, sym_dict)
    #
    #     return sympy_expr