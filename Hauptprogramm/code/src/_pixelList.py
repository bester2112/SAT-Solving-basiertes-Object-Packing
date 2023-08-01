import math

class PixelList:
    def __init__(self):
        self.forward_dict = {}
        self.reverse_dict = {}
        self.extra_binaries = []
        self.transform_dict = {}
        self.reverse_dict = {}

    def add_empty_entries(self, benchmarkExactlyOneForThePixels, playfieldWidth, playfieldHeight):
        # Erstellen Sie eine neue Liste, um die Ergebnisse zu speichern
        new_benchmark = []

        # Erstellen Sie ein Set, um alle Koordinaten zu speichern, die bereits in der Liste vorhanden sind
        existing_coords = set()

        # Füge 'EMPTY' Einträge in bestehenden Listen hinzu und speichere existierende Koordinaten
        for sub_list in benchmarkExactlyOneForThePixels:
            # Extrahiere die Koordinaten aus der letzten 'g' Klammer des ersten Elements der sub_list
            x, y = map(int, sub_list[0].split('g[')[1].split(']')[0].split(','))
            existing_coords.add((x, y))

            # Überprüfe, ob ein 'EMPTY' Element bereits existiert
            empty_exists = any('EMPTY' in element for element in sub_list)

            # Wenn es kein 'EMPTY' Element gibt, füge es hinzu
            if not empty_exists:
                sub_list.append('p[0,0]sEMPTYl[{},{}]g[{},{}]'.format(x, y, x, y))

            new_benchmark.append(sub_list)

        # Füge neue Listen mit 'EMPTY' Einträgen hinzu, wenn die Koordinaten noch nicht existieren
        for x in range(playfieldWidth):
            for y in range(playfieldHeight):
                if (x, y) not in existing_coords:
                    new_benchmark.append(['p[0,0]sEMPTYl[{},{}]g[{},{}]'.format(x, y, x, y)])

        return new_benchmark

    def create_name(self, input_str, idx):
        # Find the index of the first occurrence of 'g['
        start = input_str.find('g[') + 2
        substring = input_str[start:]

        # Find the index of ']' in the substring
        end = substring.find(']')

        # Extract the content between 'g[' and ']' and split by ','
        try:
            x, y = substring[:end].split(',')
            # Try to convert x, y to integers to ensure they are numbers
            x, y = int(x), int(y)
        except ValueError:
            raise ValueError(f"x = {x} and y = {y} must be numbers")

        # Find the index of the first 's' and the first 'l['
        start_s = input_str.find(']s') + 2
        end_s = input_str.find('l[')

        # Extract s from the string
        s = input_str[start_s:end_s]

        bin_idx = format(idx, "02b")
        new_name = 'b' + bin_idx + 'px' + str(x) + 'y' + str(y) + 's' + s
        return new_name

    def calculate_max_binary(self, length):
        return 2 ** math.ceil(math.log(length, 2))

    def generate_extra_binaries(self, input_str, length, s='EXTRA'):
        x, y = input_str.split('g')[1][1:-1].split(',')
        max_binary = self.calculate_max_binary(length)
        for i in range(length, max_binary):
            new_name = 'b' + format(i, "02b") + 'px' + x + 'y' + y + 's' + s
            self.extra_binaries.append(new_name)

    def transform_list(self, input_list, createExtraBinaries = False):
        output_list = []
        for idx, input_str in enumerate(input_list):
            if input_str in self.forward_dict:
                output_list.append(self.forward_dict[input_str])
            else:
                new_name = self.create_name(input_str, idx)
                self.forward_dict[input_str] = new_name
                self.reverse_dict[new_name] = input_str
                output_list.append(new_name)
        if createExtraBinaries:
            self.generate_extra_binaries(input_list[-1], len(input_list))
        return output_list

    def reverse_list(self, input_list):
        output_list = []
        for input_str in input_list:
            if input_str in self.reverse_dict:
                output_list.append(self.reverse_dict[input_str])
            else:
                output_list.append(None)
        return output_list

    def process_nested_list(self, input_list_of_lists, createExtraBinaries=False):
        output_list_of_lists = []
        for lst in input_list_of_lists:
            output_list_of_lists.append(self.transform_list(lst, createExtraBinaries))
        return output_list_of_lists

    def reverse_nested_list(self, input_list_of_lists):
        output_list_of_lists = []
        for lst in input_list_of_lists:
            if not lst == None:
                output_list_of_lists.append(self.reverse_list(lst))
        return output_list_of_lists

    # -----------------------------------------------------
    # split binaries
    # -----------------------------------------------------

    def split_binary(self, input_str):
        # Extract binary part
        binary_part = input_str.split('px')[0][1:]
        binary_split = []
        for i, binary_digit in enumerate(binary_part):
            binary_split.append('bi' + str(i) + 'b' + binary_digit + input_str.split(binary_part)[1])
        return tuple(binary_split)

    #def split_binary_list(self, input_list):
    #    return [self.split_binary(input_str) for input_str in input_list]

    def split_binary_list(self, input_list):
        output_list = [self.split_binary(input_str) for input_str in input_list]

        for input_str, transformed in zip(input_list, output_list):
            self.transform_dict[input_str] = transformed
            self.reverse_dict[transformed] = input_str

        return output_list

    def split_binary_nested_list(self, input_list_of_lists):
        return [self.split_binary_list(lst) for lst in input_list_of_lists]

    def join_binary(self, split_binary_tuple):
        binary_part = ''.join([part[3] for part in split_binary_tuple])
        rest_of_str = split_binary_tuple[0][4:]
        return 'b' + binary_part + rest_of_str

    def join_binary_list(self, split_binary_list):
        return [self.join_binary(split_binary_tuple) for split_binary_tuple in split_binary_list]

    def join_binary_nested_list(self, split_binary_nested_list):
        return [self.join_binary_list(lst) for lst in split_binary_nested_list]