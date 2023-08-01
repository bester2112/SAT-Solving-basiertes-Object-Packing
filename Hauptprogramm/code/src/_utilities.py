import re


class Utilities(object):
    def _listToStr(self, listToTransform: list) -> str:
        """
       Converts a list to a string.

       Args:
           listToTransform (list): The list to convert.

       Raises:
           TypeError: If the input is not a list.
           SyntaxError: If the list is not of length 2.

       Returns:
           A string.
       """
        if not isinstance(listToTransform, list):
            raise TypeError

        if len(listToTransform) != 2:
            raise SyntaxError

        res = "["
        res += str(listToTransform[0])
        res += ","
        res += str(listToTransform[1])
        res += "]"

        return res

    def _strToList(self, textToTransform: str) -> []:
        """
        Converts a string to a list.

        Args:
            textToTransform (str): The string to convert.

        Raises:
            TypeError: If the input is not a string.

        Returns:
            A list.
        """
        if not isinstance(textToTransform, str):
            raise TypeError

        textToTransform = textToTransform.strip("[]")
        x, y = textToTransform.split(",")
        return [int(x), int(y)]

    def _placeStoneOnPossiblePositions(self, spielsteinTyp):
        """
        Places the Spielstein on all possible positions.

        Args:
            spielsteinTyp (Spielstein): The type of Spielstein.

        Returns:
            None
        """
        for [x, y] in spielsteinTyp.moeglichePositionen:
            key = "[" + str(x) + "," + str(y) + "]"
            content = []
            for [activeX, activeY] in spielsteinTyp.activeBlocks:
                content.append([x + activeX, y + activeY])
            spielsteinTyp.alleMoeglichenPlaziertenSteine[key] = content

    def check_last_chars(self, map_dict, key):
        if map_dict.get(key) == []:
            return True
        for k, v in map_dict.items():
            if k == key:
                for s in v:
                    if s.endswith(k[-5:]):
                        return True
                return False
        return False

    def getNegated(self, arg):
        if arg.startswith('~'):
            return arg[1:]
        else:
            return '~' + arg

    def addAtMostOneNested(self, args):
        result = []
        for i in range(len(args) - 1):
            for j in range(i + 1, len(args)):
                result.append([self.getNegated(args[i]), self.getNegated(args[j])])
        return result

    def joinElementsWithOr(self, input_list):
        result = []
        for sub_list in input_list:
            joined_sub_list = " | ".join([f"({expr})" for expr in sub_list])
            result.append(joined_sub_list)
        return result

    def countUniqueSympyVariables(self, expressions):
        unique_variable_counts = []

        for expression in expressions:
            # Entferne alle Klammern und Tilden
            clean_expression = re.sub(r'[()~]', '', expression)

            # Ersetze ' & ' und ' | ' durch ', '
            elements_str = re.sub(r' [&|] ', ', ', clean_expression)

            # Teile den Ausdruck in einzelne Variablen auf
            variables = elements_str.split(', ')

            # Erstelle ein Set, um die einzigartigen Variablen zu speichern
            unique_variables = set(variables)

            # Zähle die einzigartigen Variablen und füge sie zur Liste hinzu
            unique_variable_counts.append(len(unique_variables))

        return unique_variable_counts

    def sympyListToStrList(self, lst):
        str_lst = []
        for expr in lst:
            str_lst.append(str(expr))
        return str_lst

    def joinWithOrStr(self, input_list):
        return " | ".join([expr for expr in input_list])

    def cnf_conversion(self, expr):
        return sp.to_cnf(expr)

    def process_list_again(self, input_list):
        output_list = []
        for group in input_list:
            new_group = []
            for item in group:
                new_item = " ".join([element.replace('~', '-') for element in item])
                new_group.append(new_item)
            output_list.append(new_group)
        return output_list

    def prepareEquivalentExprForClauses(self, expr_components):
        # Step 1: Split the string by '&', and remove leading/trailing spaces
        clauses_separated = [[clause.strip() for clause in group.split('&')] for group in expr_components]

        # Step 2: Remove '(' and ')' and replace ' | ' with ' '
        clauses_no_parentheses = [
            [[clause.replace('(', '').replace(')', '').replace(' | ', ' ').replace('~', '-')] for clause in group] for
            group in clauses_separated]
        # clauses_no_parentheses = [[[clause.replace('(', '').replace(')', '')] for clause in group] for group in clauses_separated]

        # splitted_no_parentheses = [[[clause.strip() for clause in group_clause.split('|')] for group_clause in clause_group] for clauses_group
        #    in clauses_no_parentheses for clause_group in clauses_group]

        # cnf_list_splitted = self.process_this_list(splitted_no_parentheses)

        # cnf_list = self.process_list_again(cnf_list_splitted)

        # Step 3: Split each clause into a list of individual literals
        literals_separated = [[clause[0].split(' ') for clause in group] for group in clauses_no_parentheses]

        return literals_separated

    def prepareExprForClauses(self, expr_components):
        # Step 1: Split the string by '&', and remove leading/trailing spaces
        clauses_separated = [[clause.strip() for clause in group.split('&')] for group in expr_components]

        # Step 2: Remove '(' and ')' and replace ' | ' with ' '
        clauses_no_parentheses = [[[clause.replace('(', '').replace(')', '').replace(' | ', ' ').replace('~', '-')] for clause in group]
                                  for group in clauses_separated]

        # Step 3: Split each clause into a list of individual literals
        literals_separated = [[clause[0].split(' ') for clause in group] for group in clauses_no_parentheses]

        return literals_separated

    def tseitin_vars(self, list_data):
        tseitin_vars = set()
        for sublist in list_data:
            for pair in sublist:
                for item in pair:
                    if item.startswith("tseitin") and item not in self.sh.variableIntMap:
                        tseitin_vars.add(item)

        tseitin_list = sorted(tseitin_vars, key=lambda x: int(x.split("_")[1]))
        return tseitin_list

    def process_this_list(self, input_list):
        output_list = []
        for group in input_list:
            new_group = []
            for item in group:
                new_item = []
                for element in item:
                    new_item.append(str(self.cnf_conversion(element)))
                new_group.append(new_item)
            output_list.append(new_group)
        return output_list

    def translateAddClauseForThePossiblePlaystone(self, input_list):
        combined_expressions = []

        # Schritt 1: Verbinden Sie geschachtelte Elemente mit &
        for sublist in input_list:
            combined_sublist = [self.combine_expression_list(expr_list) for expr_list in sublist]
            combined_expressions.append(combined_sublist)

        # Schritt 2: Verbinden Sie jedes Element in der Liste mit |
        reordered_expressions = []

        for combined_sublist in combined_expressions:
            reordered_sublist = self.joinWithOrStr(combined_sublist)
            reordered_expressions.append(reordered_sublist)

        return reordered_expressions

    def simplifyExpressions(self, expr_list):
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

            if count <= 8:
                cnf_expr = sp.to_cnf(expr)
            else :
                nnf = ccNNF._ccNNF()
                cnf_expr = nnf.process_formula(expr)
                #cnf_expr = sp.to_cnf(expr)

            simplified_list.append(cnf_expr)
            logging.info("simplified_list " + str(self.count) + " = " + str(simplified_list))
            self.count += 1
        return simplified_list

    def replaceVarFromExactlyOneForThePixels(self, output_list, variable_map):
        new_output_list = []
        for pair in output_list:
            temp_pair = []
            for element in pair:
                negated = element.startswith('~')
                var_name = element[1:] if negated else element
                if var_name in variable_map:
                    combined_expr = self.combine_expression_list(variable_map[var_name])
                    if negated:
                        combined_expr = f"~({combined_expr})"
                    temp_pair.append(combined_expr)
                else:
                    temp_pair.append(element)
            new_output_list.append(temp_pair)
        return new_output_list