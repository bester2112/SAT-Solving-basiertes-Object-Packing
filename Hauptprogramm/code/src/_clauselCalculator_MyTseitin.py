from sympy import Symbol, And, Or, Not
from sympy.logic import to_cnf


class _Tseitin:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'tseitin_counter'):
            self.tseitin_counter = 0


    '''
    
    input example: 
    (~g_0_0_b1) & (~g_0_0_b2) & (~g_0_0_b3) & (~g_0_0_b4) | (~g_1_0_b1) & (~g_1_0_b2) & (~g_1_0_b3) & (~g_1_0_b4) | 
    (~g_2_0_b1) & (~g_2_0_b2) & (~g_2_0_b3) & (~g_2_0_b4) | (~g_0_1_b1) & (~g_0_1_b2) & (~g_0_1_b3) & (~g_0_1_b4) | 
    (~g_1_1_b1) & (~g_1_1_b2) & (~g_1_1_b3) & (~g_1_1_b4) | (~g_2_1_b1) & (~g_2_1_b2) & (~g_2_1_b3) & (~g_2_1_b4) | 
    (~g_0_2_b1) & (~g_0_2_b2) & (~g_0_2_b3) & (~g_0_2_b4) | (~g_1_2_b1) & (~g_1_2_b2) & (~g_1_2_b3) & (~g_1_2_b4) | 
    (~g_2_2_b1) & (~g_2_2_b2) & (~g_2_2_b3) & (~g_2_2_b4) 
    '''

    def tseitin_calculator(self, expr_str):
        # Schritt 1: Aufteilen nach einer Liste von Expressions, diese sind dann nur mit &. D.h. nach | gesplittet
        clauses = [clause.strip() for clause in expr_str.split('|')]

        new_vars = []
        equivalences = []
        transformed_clauses = []
        last_index = 0

        # Schritt 2: Nun definieren wir Äquivalenzen, die diese neuen Variablen mit ihren jeweiligen Teil-Ausdrücken verknüpfen:
        for i, clause in enumerate(clauses):
            new_var = Symbol(f'T{i + 1 + self.tseitin_counter}')
            new_vars.append(new_var)

            sub_expr = And(*(Symbol(literal.strip()) for literal in clause.split('&')))
            equivalence = (new_var | ~sub_expr) & (sub_expr | ~new_var)
            equivalences.append(equivalence)
            transformed_clauses.append(new_var)
            last_index = i
        self.tseitin_counter = self.tseitin_counter + last_index + 1

        # Schritt 3: Als nächstes setzen wir die neuen Variablen in den ursprünglichen Ausdruck ein und erhalten:
        combined_expr = Or(*transformed_clauses)

        # Schritt 4: Jetzt müssen wir die Äquivalenzen aus Schritt 2 in CNF umwandeln. Dafür benutzen wir die folgende Regel:
        cnf_equivalences = [to_cnf(eq) for eq in equivalences]

        # Schritt 5: Da der Ausdruck aus Schritt 3 bereits in CNF ist, können wir ihn unverändert lassen:
        final_cnf = And(*cnf_equivalences, combined_expr)
        return final_cnf
