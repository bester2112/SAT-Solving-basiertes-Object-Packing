import re
#from boolean.boolean import BooleanAlgebra


class CNFTransformer:
    def __init__(self):
        self.variable_counter = 0

    def transform_wrong(self, input_data):
        result = []
        result_separate = []
        for sub_list in input_data:
            new_variables = []
            transformed_data = []
            transformed_data_separate = []

            for tupel in sub_list:
                new_variable = f"A{self.variable_counter}"
                new_variables.append(new_variable)
                equivalence = f"({new_variable} <-> {tupel})"
                transformed_data.append(equivalence)
                transformed_data_separate.append(equivalence)
                self.variable_counter += 1

            logical_or_expression = f"({' | '.join(new_variables)})"
            final_expression = f"{logical_or_expression} & {' & '.join(transformed_data)}"
            result.append(final_expression)
            result_separate.append([logical_or_expression] + transformed_data_separate)

        return result, result_separate

    def transform_OLD(self, input_data):
        result = []
        result_separate = []
        result_new = []
        result_separate_new = []

        for sub_list in input_data:
            sub_result = []
            sub_result_separate = []
            sub_result_new = []
            sub_result_separate_new = []

            first_tuple = sub_list[0]
            for i in range(1, len(sub_list)):
                next_tuple = sub_list[i]
                sub_result.append(f"{first_tuple} <-> {next_tuple}")
                sub_result_separate.append(first_tuple)
                sub_result_separate.append(next_tuple)

                new_variable_first = f"T{self.variable_counter}"
                self.variable_counter += 1

                new_variable_next = f"T{self.variable_counter}"
                self.variable_counter += 1

                sub_result_new.append([f"{new_variable_first} <-> {first_tuple}"])
                sub_result_new.append([f"{new_variable_next} <-> {next_tuple}"])

                sub_result_separate_new.append([new_variable_first, first_tuple])
                sub_result_separate_new.append([new_variable_next, next_tuple])

                new_variable_final = f"T{self.variable_counter}"
                self.variable_counter += 1

                sub_result_new.append([f"{new_variable_final} <-> ({new_variable_first} <-> {new_variable_next})"])
                sub_result_separate_new.append([new_variable_final, (new_variable_first, new_variable_next)])

            result.append(sub_result)
            result_separate.append(sub_result_separate)
            result_new.append(sub_result_new)
            result_separate_new.append(sub_result_separate_new)

        return result, result_separate, result_new, result_separate_new

    def transform(self, input_data):
        result = []
        result_separate = []
        result_new = []
        result_separate_new = []

        for sub_list in input_data:
            sub_result = []
            sub_result_separate = []
            sub_result_new = []
            sub_result_separate_new = []
            result_all_Vars_Needs_to_be_True = []

            firstTime = True

            first_tuple = sub_list[0]
            for i in range(1, len(sub_list)):
                next_tuple = sub_list[i]
                sub_result.append(f"{first_tuple} <-> {next_tuple}")
                sub_result_separate.append(first_tuple)
                sub_result_separate.append(next_tuple)

                if firstTime:
                    firstTime = False
                    new_variable_first = f"T{self.variable_counter}"
                    self.variable_counter += 1

                    new_variable_next = f"T{self.variable_counter}"
                    self.variable_counter += 1

                    sub_result_new.append([f"{new_variable_first} <-> {first_tuple}"])
                    sub_result_new.append([f"{new_variable_next} <-> {next_tuple}"])

                    sub_result_separate_new.append([new_variable_first, first_tuple])

                    sub_result_separate_new.append([new_variable_next, next_tuple])

                    new_variable_final = f"T{self.variable_counter}"
                    self.variable_counter += 1

                    sub_result_new.append([f"{new_variable_final} <-> ({new_variable_first} <-> {new_variable_next})"])
                    sub_result_separate_new.append([new_variable_final, (new_variable_first, new_variable_next)])
                else:
                    new_variable_first = f"T0"
                    self.variable_counter += 1

                    new_variable_next = f"T{self.variable_counter}"
                    self.variable_counter += 1

                    #sub_result_new.append([f"{new_variable_first} <-> {first_tuple}"])
                    sub_result_new.append([f"{new_variable_next} <-> {next_tuple}"])

                    sub_result_separate_new.append([new_variable_next, next_tuple])

                    new_variable_final = f"T{self.variable_counter}"
                    self.variable_counter += 1

                    sub_result_new.append([f"{new_variable_final} <-> ({new_variable_first} <-> {new_variable_next})"])
                    sub_result_separate_new.append([new_variable_final, (new_variable_first, new_variable_next)])
                result_all_Vars_Needs_to_be_True.append(new_variable_final)

            result.append(sub_result)
            result_separate.append(sub_result_separate)
            result_new.append(sub_result_new)
            result_separate_new.append(sub_result_separate_new)

        return result, result_separate, result_new, result_separate_new, result_all_Vars_Needs_to_be_True

    def process_data(self, input_data):
        edited_data = []
        for sublist in input_data:
            edited_sublist = []
            for item in sublist:
                # Entferne äußere Klammern, wenn sie vorhanden sind
                if item.startswith('(') and item.endswith(')'):
                    item = item[1:-1]

                # Teile die Zeichenkette bei "<->"
                if "<->" in item:
                    split_item = item.split(" <-> ")

                    # Transformiere das zweite Element in ein Tupel, falls es ein String ist
                    second_element = eval(split_item[1])
                    edited_sublist.append([split_item[0], second_element])
                else:
                    edited_sublist.append(item)

            edited_data.append(edited_sublist)
        return edited_data

    @staticmethod
    def transform_name(name):
        match = re.search("bi[0-9]+b([01])px[0-9]+y[0-9]+s[\w\d]*$", name)
        if match is None:
            return name

        # Suche das Muster "b[0-1]" und extrahiere die Zahl
        match = re.search("b([01])", name)
        if match is None:
            return name  # Wenn das Muster nicht gefunden wird, geben wir den ursprünglichen Namen zurück

        number = match.group(1)

        # Füge ein "~" hinzu, wenn die Zahl 0 ist
        prefix = "~" if number == "0" else ""

        # Entferne das "b[0-1]" Muster und das "s" gefolgt von Buchstaben/Zahlen am Ende
        new_name = re.sub("b[01]", "", name)
        new_name = re.sub("s[\w\d]*$", "", new_name)

        return prefix + new_name

    @staticmethod
    def process_data_bool(data):
        new_data = []
        for sublist in data:
            new_sublist = [sublist[0]]  # Kopiere den ersten Eintrag (z.B. 'A0 | A1 | A2')
            for item in sublist[1:]:
                if isinstance(item, list):
                    new_item = [item[0]]  # Kopiere den ersten Eintrag (z.B. 'A0')
                    for subitem in item[1:]:
                        if isinstance(subitem, tuple):
                            new_subitem = tuple(CNFTransformer.transform_name(name) for name in subitem)
                            new_item.append(new_subitem)
                    new_sublist.append(new_item)
            new_data.append(new_sublist)
        return new_data

    @staticmethod
    def transform_name(name):
        match = re.search("bi[0-9]+b([01])px[0-9]+y[0-9]+s[\w\d]*$", name)
        if match is None:
            return name

        match = re.search("b([01])", name)
        if match is None:
            return name

        number = match.group(1)
        prefix = "~" if number == "0" else ""

        new_name = re.sub("b[01]", "", name)
        new_name = re.sub("s[\w\d]*$", "", new_name)

        return prefix + new_name

    @staticmethod
    def transform_data(data):
        new_data = []
        for sublist in data:
            new_sublist = [sublist[0]]
            for item in sublist[1:]:
                if isinstance(item, list):
                    new_item = [item[0]]
                    for subitem in item[1:]:
                        if isinstance(subitem, tuple):
                            new_subitem = tuple(CNFTransformer.transform_name(name) for name in subitem)
                            new_item.append(new_subitem)
                    new_sublist.append(new_item)
            new_data.append(new_sublist)
        return new_data

    # def iff(self, a, b):
    #     boolean = BooleanAlgebra()
    #     return boolean.OR(boolean.AND(a, b), boolean.AND(boolean.NOT(a), boolean.NOT(b)))
    #
    # def generate_cnf(self, data):
    #     boolean = BooleanAlgebra()
    #
    #     first_part = boolean.Symbol(data[0])
    #     second_part = [boolean.Symbol(element) for element in data[1]]
    #
    #     expr = ((first_part & boolean.AND(*second_part)) | (
    #                 ~first_part & boolean.AND(*[~element for element in second_part])))
    #     # expr = self.iff(first_part, *second_part) # TODO
    #     cnf = boolean.cnf(expr)
    #
    #     return cnf

    # def transform_and_generate(self, data):
    #     transformed_data = CNFTransformer.transform_data(data)
    #     cnfs = []
    #     for sublist in transformed_data:
    #         for item in sublist[1:]:
    #             if isinstance(item, list):
    #                 cnf = self.generate_cnf(item)
    #                 cnfs.append(cnf)
    #     return cnfs
