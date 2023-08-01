import re
from sympy import sympify
from nnf import Var
from nnf.operators import And, Or, implies

class _ccNNF:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'tseitin_counter'):
            self.tseitin_counter = 1

    def process_output(self, output):
        tseitin_variables = {}

        temp_str_output = str(output)
        # Schritt 1: Ersetzen der Tseitin-Variablen
        for var in re.findall(r'<[0-9a-f]+>', temp_str_output):
            if var not in tseitin_variables.values():
                tseitin_key = f"tseitin_{self.tseitin_counter}"
                tseitin_variables[tseitin_key] = var
                self.tseitin_counter += 1

        processed_output = temp_str_output
        for key, value in tseitin_variables.items():
            processed_output = processed_output.replace(value, key)

        # Schritt 2: Entfernen der geschweiften Klammern
        processed_output = processed_output.replace("{", "").replace("}", "")

        # Schritt 3: Konvertieren der verarbeiteten Ausgabe zurück in SymPy
        processed_output = sympify(processed_output)

        return processed_output

    def transform_input(self, input_str):
        # Regex-Muster, um alle Variablennamen zu erkennen
        pattern = re.compile(r'\b\w+\b')

        # Funktion, die die entsprechenden Transformationen für die gefundenen Variablennamen vornimmt
        def replace_with_var(match):
            var_name = match.group(0)
            if var_name == "Equivalent":
                return "equivalent"
            return f'Var("{var_name}")'

        # Ersetze alle Variablennamen mit dem entsprechenden Var-Ausdruck
        transformed_str = pattern.sub(replace_with_var, input_str)

        if "equivalent" in transformed_str:
            transformed_str = self.transformEquivalent(transformed_str)

            def replace_with_var2(match):
                var_name = match.group(0)
                if var_name == "And":
                    return "And"
                if var_name == "Or":
                    return "Or"
                if var_name == "implicates":
                    return "implicates"
                if var_name == "implies":
                    return "implies"
                return f'Var("{var_name}")'

            #transformed_str = pattern.sub(replace_with_var2, transformed_str)

        return transformed_str

    def transformEquivalent(self, input_str):
        input_str = input_str.replace("equivalent(", "")
        if input_str[-1] == ")":
            input_str = input_str[:-1]

        parts = input_str.split(", ")

        #equivalent = "(A | ~B) & (B | ~A)"
        equivalent = "implies(A, B) & implies(B, A)"
        equivalent = equivalent.replace("A", parts[0])
        equivalent = equivalent.replace("B", parts[1])

        return equivalent

    def execute_transformed_code(self, transformed_str):
        return eval(transformed_str)

    def process_formula(self, input_str):
        transformed_str = self.transform_input(input_str)
        formula = self.execute_transformed_code(transformed_str)
        cnf_formula = formula.to_CNF()
        processed_output_simplified = self.process_output(cnf_formula)
        return processed_output_simplified