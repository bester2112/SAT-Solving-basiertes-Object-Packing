#from nnf.operators import iff
#from sympy import symbols
#from sympy.logic.boolalg import to_cnf
from nnf import Var, And, Or
import re
from itertools import combinations, product


class SympyTransformer:

    def __init__(self):
        self.last_case_expr = False


    def process_string(self, s):
        pattern = r"bi(?P<index>\d+)b(?P<bool>[01])px(?P<xPos>\d+)y(?P<yPos>\d+)s(?P<name>.+)"
        match = re.match(pattern, s)

        if match:
            index = match.group('index')
            bool_val = match.group('bool')
            xPos = match.group('xPos')
            yPos = match.group('yPos')
            name = match.group('name')

            # Zusammenbau des Strings ohne "b[0/1]" und ohne s$name
            s_text = f"bi{index}px{xPos}y{yPos}"

            # Anwenden der entsprechenden Logik basierend auf 'bool_val'
            if bool_val == '0':
                expr = Var(s_text).negate()  # Negieren des Ausdrucks
            elif bool_val == '1':
                expr = Var(s_text)  # Erzeugen eines Symbols
            else:
                raise ValueError(f"Ungültige Zeichenkette: {s}")
            return expr
        else:
            # Prüfen, ob der String dem Muster "T{Zahl}" entspricht
            pattern_T = r"T(?P<number>\d+)"
            match_T = re.match(pattern_T, s)

            if match_T:
                # Wenn der String dem Muster entspricht, wird er zurückgegeben
                self.last_case_expr = True
                return s

            else:
                raise ValueError(f"Die Eingabe entspricht nicht dem erwarteten Muster: {s}")

    def check_tuple_elements_are_strings(self, tup):
        if not all(isinstance(element, str) for element in tup):
            raise ValueError("All elements in the tuple must be strings.")

    def to_my_cnf(self, var, tup):
        if not isinstance(var, str) or not isinstance(tup, tuple):
            raise ValueError("Both inputs must be either a string or a tuple.")
        if isinstance(tup, tuple):
            self.check_tuple_elements_are_strings(tup)

        cnf = []
        # A -> (B and C)
        for t in tup:
            # Negate var unless it's already negated
            negated_var = ('~' + var if var[0] != '~' else var[1:])
            cnf.append((negated_var, str(t)))

        # (B and C) -> A
        # Negate all elements in tup unless they're already negated
        negated_tup = [('~' + t if t[0] != '~' else t[1:]) for t in tup]
        negated_tup.append(var)
        cnf.append(tuple(negated_tup))

        return cnf

    def implies_cnf(self, tup1, tup2):
        # Prüfen, ob tup1 und tup2 Tupel sind, und wenn nicht, sie in Tupel umwandeln
        tup1 = tup1 if isinstance(tup1, tuple) else (tup1,)
        tup2 = tup2 if isinstance(tup2, tuple) else (tup2,)

        if isinstance(tup1, tuple) or isinstance(tup2, tuple):
            self.check_tuple_elements_are_strings(tup1)
            self.check_tuple_elements_are_strings(tup2)

        cnf = []
        # Negate all elements in tup1 unless they're already negated
        negated_tup1 = [('~' + t if t[0] != '~' else t[1:]) for t in tup1]

        # Loop over each element in tup2 and add it to negated_tup1
        for t in tup2:
            cnf.append(tuple(negated_tup1 + [t]))

        return cnf

    def iff_cnf(self, tup1, tup2):
        # Prüfen, ob tup1 und tup2 Tupel sind, und wenn nicht, sie in Tupel umwandeln
        tup1 = tup1 if isinstance(tup1, tuple) else (tup1,)
        tup2 = tup2 if isinstance(tup2, tuple) else (tup2,)

        # Call implies_cnf twice with reversed arguments and concatenate the lists
        return self.implies_cnf(tup1, tup2) + self.implies_cnf(tup2, tup1)

    def convert_to_iff_cnf(self, input1, input2):
        # Überprüfen, ob die Eingaben korrekt sind
        if not isinstance(input1, (str, tuple)) or not isinstance(input2, (str, tuple)):
            raise ValueError("Both inputs must be either a string or a tuple.")

        if isinstance(input1, str) and isinstance(input2, tuple):
            # Aufruf von to_my_cnf, wenn input1 eine einzelne Variable und input2 ein Tupel ist
            str_tup = tuple(map(str, input2))
            return self.to_my_cnf(input1, str_tup)
        elif isinstance(input1, tuple) and isinstance(input2, str):
            # Aufruf von to_my_cnf, wenn input2 eine einzelne Variable und input1 ein Tupel ist
            str_tup = tuple(map(str, input1))
            return self.to_my_cnf(input2, str_tup)
        elif isinstance(input1, tuple) and isinstance(input2, tuple):
            # Aufruf von iff_cnf, wenn beide Eingaben Tupel sind
            str_tup_1 = tuple(map(str, input1))
            str_tup_2 = tuple(map(str, input2))
            return self.iff_cnf(str_tup_1, str_tup_2)
        else:
            raise ValueError(
                "Invalid input combination. For to_my_cnf, input1 should be a string and input2 should be a tuple. For iff_cnf, both inputs should be tuples.")

    def convert_to_iff_cnf_special_case(self, input1, input2):
        t1, t2 = input2  # Tupel extrahieren
        t3 = input1

        # Erstellen Sie die Liste von Tupeln
        formula = [(t1, t2, t3),
                   (t1, '~' + t2, '~' + t3),
                   ('~' + t1, t2, '~' + t3),
                   ('~' + t1, '~' + t2, t3)]

        return formula

    def equivalent_cnf(self, data):
        output = []
        for group in data:
            for item in group:
                # Erzeugen eines Symbols für den ersten Teil des Elements
                a = item[0]

                # Verarbeiten der Tupel-Elemente
                processed_items = [self.process_string(i) for i in item[1]]
                tupple_processed_items = tuple(processed_items)

                if not self.last_case_expr:
                    #result_str = str(result).replace("{", "").replace("}", "")
                    cnf_result = self.convert_to_iff_cnf(a, tupple_processed_items)
                else:
                    cnf_result = self.convert_to_iff_cnf_special_case(a, tupple_processed_items)
                    self.last_case_expr = False

                output.append(cnf_result)

        return output

    def atMostOne_cnf(self, data, testOnly=False):
        # Überprüfen, ob die Eingabe eine Liste ist
        if not isinstance(data, list):
            raise ValueError("Die Eingabe muss eine Liste sein.")

        if not testOnly:
            # Aufrufen von process_string für jedes Element in jedem Tupel in data
            processed_data = [[self.process_string(i) for i in tup] for sublist in data for tup in sublist]
        else:
            processed_data = data

        new_data = []

        for sublist in processed_data:
            new_sublist = []
            # Überprüfen, ob jedes Element in der Unterliste ein Tupel ist, und wenn nicht, es in ein Tupel umwandeln
            sublist = [item if isinstance(item, tuple) else (item,) for item in sublist]

            # Erzeugen aller möglichen Tupel-Paare innerhalb der Unterliste
            for tup_pair in combinations(sublist, 2):
                for tup1, tup2 in combinations(tup_pair, 2):
                    # Prüfen, ob tup1 ein Var-Objekt ist und es in einen String konvertieren, wenn es so ist
                    tup1 = tuple(str(t) if isinstance(t, Var) else t for t in tup1)
                    # Prüfen, ob tup2 ein Var-Objekt ist und es in einen String konvertieren, wenn es so ist
                    tup2 = tuple(str(t) if isinstance(t, Var) else t for t in tup2)

                    # Negieren der Elemente in tup1 und tup2, sofern sie nicht bereits negiert sind
                    negated_tup1 = tuple('~' + t if t[0] != '~' else t[1:] for t in tup1)
                    negated_tup2 = tuple('~' + t if t[0] != '~' else t[1:] for t in tup2)

                    # Verknüpfen der Elemente in negated_tup1 und negated_tup2
                    new_tup = negated_tup1 + negated_tup2
                    new_sublist.append(new_tup)

            new_data.append(new_sublist)

        return new_data

    def clause_cnf(self, data, testOnly=False):
        # Überprüfen, ob die Eingabe eine Liste ist
        if not isinstance(data, list):
            raise ValueError("Die Eingabe muss eine Liste sein.")

        if not testOnly:
            # Aufrufen von process_string für jedes Element in jedem Tupel in data
            processed_data = [[self.process_string(i) for i in tup] for sublist in data for tup in sublist]
        else:
            processed_data = data

        new_data = []

        for sublist in processed_data:
            new_sublist = []

            # Stellen Sie sicher, dass jedes Element in der Unterliste ein Tupel ist
            sublist = [item if isinstance(item, tuple) else (item,) for item in sublist]

            # Erzeugen des Kreuzprodukts aller Tupel in der Unterliste
            for combined_tup in product(*sublist):
                # Prüfen, ob jedes Element ein Var-Objekt ist und es in einen String konvertieren, wenn es so ist
                combined_tup = tuple(str(t) if isinstance(t, Var) else t for t in combined_tup)

                new_sublist.append(combined_tup)

            new_data.append(new_sublist)

        return new_data

    def exactlyOne_cnf(self, data, testOnly=False):
        # Rufen Sie zuerst die beiden Methoden auf
        at_most_one_cnf_data = self.atMostOne_cnf(data, testOnly)
        clause_cnf_data = self.clause_cnf(data, testOnly)
        combined_data = at_most_one_cnf_data + clause_cnf_data
        return combined_data

    def negateNotAllowedVariables(self, data):
        # Überprüfen, ob die Eingabe eine Liste ist
        if not isinstance(data, list):
            raise ValueError("Die Eingabe muss eine Liste sein.")

        new_data = []

        for tup in data:
            # Aufrufen von process_string für jedes Element in dem Tupel
            processed_tup = [self.process_string(i) for i in tup]

            # Prüfen, ob jedes Element ein Var-Objekt ist und es in einen String konvertieren, wenn es so ist
            processed_tup = [str(t) if isinstance(t, Var) else t for t in processed_tup]

            # Negieren der Elemente, sofern sie nicht bereits negiert sind
            negated_tup = [('~' + t if t[0] != '~' else t[1:]) for t in processed_tup]

            new_data.append(tuple(negated_tup))

        return [new_data]

    def flatten_sublists(self, data):
        return [tup for sublist in data for tup in sublist]

    def flatten_and_combine_sublists(self, *args):
        combined = []
        for data in args:
            combined.extend(self.flatten_sublists(data))
        return combined

    def is______cnf(self, expr):
        if isinstance(expr, And):
            for clause in expr:
                if not isinstance(clause, Or) and not isinstance(clause, Var):
                    return False
            return True
        elif isinstance(expr, Or) or isinstance(expr, Var):
            return True
        else:
            return False
