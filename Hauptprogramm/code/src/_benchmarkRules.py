import re

from _pixelList import PixelList
from _cnfTransformer import CNFTransformer
from _sympyTransformer import SympyTransformer
#from boolean.boolean import BooleanAlgebra
from testSympy import TestSympy

class BenchmarkRules():
    def __init__(self, allVariableName, benchmarkEquivalents, benchmarkExactlyOneForThePixels, benchmarkExactlyOneForThePossiblePlaystone, playfieldWidth, playfieldHeight):
        #testSympy = TestSympy()# TODO DELETE AFTER TESTING
        self.allVariableName = allVariableName
        self.benchmarkEquivalents = benchmarkEquivalents
        self.benchmarkExactlyOneForThePixels = benchmarkExactlyOneForThePixels
        self.benchmarkExactlyOneForThePossiblePlaystone = benchmarkExactlyOneForThePossiblePlaystone
        self.playfieldWidth = playfieldWidth
        self.playfieldHeight = playfieldHeight + 1

        self.pixelList = PixelList()

        #add an empty field into self.benchmarkExactlyOneForThePixels
        self.benchmarkExactlyOneForThePixelsWEmpty = self.pixelList.add_empty_entries(self.benchmarkExactlyOneForThePixels, self.playfieldWidth, self.playfieldHeight)

        self.benchmarkExactlyOneForThePixelsBinary = self.pixelList.process_nested_list(self.benchmarkExactlyOneForThePixelsWEmpty, createExtraBinaries=True)
        self.allVariableNameBinary = self.pixelList.transform_list(self.allVariableName)
        self.benchmarkEquivalentsBinary = self.pixelList.process_nested_list(self.benchmarkEquivalents)
        self.benchmarkExactlyOneForThePossiblePlaystoneBinary = self.pixelList.process_nested_list(self.benchmarkExactlyOneForThePossiblePlaystone)
        self.allVariableNameAdditionalBinary = self.pixelList.extra_binaries

        self.allVariableNameBinSplitted = self.pixelList.split_binary_list(self.allVariableNameBinary)
        self.allVariableNameAdditionalBinSplitted = self.pixelList.split_binary_list(self.allVariableNameAdditionalBinary)
        self.benchmarkExactlyOneForThePixelsBinSplitted = self.pixelList.split_binary_nested_list(self.benchmarkExactlyOneForThePixelsBinary)
        self.benchmarkEquivalentsBinSplitted = self.pixelList.split_binary_nested_list(self.benchmarkEquivalentsBinary)
        self.benchmarkExactlyOneForThePossiblePlaystoneBinSplitted = self.pixelList.split_binary_nested_list(self.benchmarkExactlyOneForThePossiblePlaystoneBinary)

        cnfTransformer = CNFTransformer()
        #self.benchmarkExactlyOneForThePixelsBSCNF, self.benchmarkExactlyOneForThePixelsBSCNF2 = cnfTransformer.transform(self.benchmarkExactlyOneForThePixelsBinSplitted)
        #self.benchmarkExactlyOneForThePixelsBSCNF2SPLITTED = cnfTransformer.process_data(self.benchmarkExactlyOneForThePixelsBSCNF2)

        self.benRes, self.benResSep, self.benchmarkEquivalentsBSCNF, self.benchmarkEquivalentsBSCNF2, self.benchmarkEquivalentsBSCNF2_all_Vars_Needs_to_be_True= cnfTransformer.transform(self.benchmarkEquivalentsBinSplitted)
        #self.benchmarkEquivalentsBSCNF2SPLITTED = cnfTransformer.process_data(self.benchmarkEquivalentsBSCNF2)

        print("benchmarkRules")
        print(self.allVariableName)
        print("benchmarkEquivalents")
        print(self.benchmarkEquivalents)
        print("benchmarkExactlyOneForThePixels")
        print(self.benchmarkExactlyOneForThePixels)
        print("benchmarkExactlyOneForThePossiblePlaystone")
        print(self.benchmarkExactlyOneForThePossiblePlaystone)
        print()
        print("benchmarkRulesBinary")
        print(self.allVariableNameBinary)
        print("allVariableNameAdditionalBinary")
        print(self.allVariableNameAdditionalBinary)
        print("benchmarkEquivalentsBinary")
        print(self.benchmarkEquivalentsBinary)
        print("benchmarkExactlyOneForThePixelsBinary")
        print(self.benchmarkExactlyOneForThePixelsBinary)
        print("benchmarkExactlyOneForThePossiblePlaystoneBinary")
        print(self.benchmarkExactlyOneForThePossiblePlaystoneBinary)
        print()
        print("benchmarkRulesBinary")
        print(self.allVariableNameBinSplitted)
        print("allVariableNameAdditionalBinSplitted")
        print(self.allVariableNameAdditionalBinSplitted)
        print("benchmarkEquivalentsBinSplitted")
        print(self.benchmarkEquivalentsBinSplitted)
        print("benchmarkExactlyOneForThePixelsBinSplitted")
        print(self.benchmarkExactlyOneForThePixelsBinSplitted)
        print("benchmarkExactlyOneForThePossiblePlaystoneBinSplitted")
        print(self.benchmarkExactlyOneForThePossiblePlaystoneBinSplitted)
        print()
        print("benchmarkEquivalentsBSCNF2")
        print(self.benchmarkEquivalentsBSCNF2)

        #print()

        # boolean = BooleanAlgebra()
        # def generate_cnf(data):
        #     boolean = BooleanAlgebra()
        #
        #     # Definiere die boolesche Variable für den ersten Teil
        #     first_part = boolean.Symbol(data[0])
        #
        #     # Definiere boolesche Variablen für jedes Element im Tupel
        #     second_part = [boolean.Symbol(element) for element in data[1]]
        #
        #     # Forme die Äquivalenz als "and" und "or" Operationen
        #     expr = ((first_part & boolean.AND(*second_part)) | (
        #                 ~first_part & ~boolean.AND(*[element for element in second_part])))
        #
        #     # Konvertiere in CNF
        #     cnf = boolean.cnf(expr)
        #
        #     return cnf
        #
        # data = ['A0', ('bi0b0px0y0sI1', 'bi1b0px0y0sI1')]
        # #print(generate_cnf(data))

        # def iff(a, b):
        #     return boolean.OR(boolean.AND(a, b), boolean.AND(boolean.NOT(a), boolean.NOT(b)))
        #
        # # Beispielverwendung
        # p = boolean.Symbol('p')
        # q = boolean.Symbol('q')
        #
        # result = iff(p, q)
        # #print(result.simplify())
        # #print(boolean.cnf(result.simplify()))
        #
        # A0 = boolean.Symbol('A0')
        # bi0b0px0y0sI1 = boolean.Symbol('bi0b0px0y0sI1')
        # bi1b0px0y0sI1 = boolean.Symbol('bi1b0px0y0sI1')
        # bi0b0px0y0sI0 = boolean.Symbol('bi0b0')
        # B = boolean.AND(bi1b0px0y0sI1, bi0b0px0y0sI1)
        # result = iff(A0, B)
        # #print(result.simplify())
        # #print(boolean.cnf(result.simplify()))
        # #print("...")

        data = [['A0 | A1 | A2', ['A0', ('bi0b0px0y0sI1', 'bi1b0px0y0sI1')], ['A1', ('bi0b0px0y0sP1', 'bi1b1px0y0sP1')],
                 ['A2', ('bi0b1px0y0sP2', 'bi1b0px0y0sP2')]],
                ['A3 | A4 | A5', ['A3', ('bi0b0px1y0sI1', 'bi1b0px1y0sI1')], ['A4', ('bi0b0px1y0sP1', 'bi1b1px1y0sP1')],
                 ['A5', ('bi0b1px1y0sP2', 'bi1b0px1y0sP2')]],
                ['A6 | A7 | A8', ['A6', ('bi0b0px0y1sI1', 'bi1b0px0y1sI1')], ['A7', ('bi0b0px0y1sP1', 'bi1b1px0y1sP1')],
                 ['A8', ('bi0b1px0y1sP2', 'bi1b0px0y1sP2')]],
                ['A9 | A10 | A11', ['A9', ('bi0b0px1y1sI1', 'bi1b0px1y1sI1')],
                 ['A10', ('bi0b0px1y1sP1', 'bi1b1px1y1sP1')], ['A11', ('bi0b1px1y1sP2', 'bi1b0px1y1sP2')]]]

        #cnfTransformer = CNFTransformer()
        #cnfs = cnfTransformer.transform_and_generate(data)
        #for cnf in cnfs:
        #    #print(cnf)

        #print()

        sympyTransformer = SympyTransformer()
        #output1 = sympyTransformer.equivalent_cnf(self.benchmarkExactlyOneForThePixelsBSCNF2SPLITTED)
        output2_equivalent_cnf = sympyTransformer.equivalent_cnf(self.benchmarkEquivalentsBSCNF2)
        output3_atMostOne_cnf = sympyTransformer.atMostOne_cnf(self.benchmarkExactlyOneForThePixelsBinSplitted)
        output4_exactlyOne_cnf = sympyTransformer.exactlyOne_cnf(self.benchmarkExactlyOneForThePossiblePlaystoneBinSplitted)
        output5_negateNotAllowedVariables = sympyTransformer.negateNotAllowedVariables(self.allVariableNameAdditionalBinSplitted)

        #print("output 1")
        #print(output1)
        print("output 2")
        print(output2_equivalent_cnf)
        print("output 3")
        print(output3_atMostOne_cnf)
        print("output 4")
        print(output4_exactlyOne_cnf)
        print("output 5")
        print(output5_negateNotAllowedVariables)

        self.allCnfData = sympyTransformer.flatten_and_combine_sublists(output2_equivalent_cnf,
                                                                        #output3_atMostOne_cnf,
                                                                        #output4_exactlyOne_cnf,
                                                                        output5_negateNotAllowedVariables)
        print("allCnfData")
        print(self.allCnfData)
        print()

    def backToNormalVariables(self, trueVariables, falseVariables):

        result = self.backToNormalVariables(trueVariables, falseVariables)
        return result


    def matchVariable(self, variable, all_true_values = False):
        pattern = r"bi(?P<index>\d+)px(?P<xPos>\d+)y(?P<yPos>\d+)"
        match = re.match(pattern, variable)

        if match:
            index = match.group('index')
            xPos = match.group('xPos')
            yPos = match.group('yPos')

            if all_true_values:
                bool_val = "1"
            elif not all_true_values:
                bool_val = "0"

            # Zusammenbau des Strings ohne "b[0/1]" und ohne s$name
            varName = f"bi{index}b{bool_val}px{xPos}y{yPos}"

            return varName
        else:
            # Prüfen, ob der String dem Muster "T{Zahl}" entspricht
            pattern_T = r"T(?P<number>\d+)"
            match_T = re.match(pattern_T, variable)

            if match_T:
                return variable
    def backToNormalVariables(self, trueVariavles, falseVariables):
        newTrueVars = []
        for content in trueVariavles:
            newTrueVars.append(self.matchVariable(content, all_true_values=True))

        for content in falseVariables:
            newTrueVars.append(self.matchVariable(content, all_true_values=False))

        result_middle = []
        for content in newTrueVars:
            for key in self.pixelList.transform_dict.keys():
                if content in key:
                    result_middle.append(key)

        table = ['bi0b1px0y0', 'bi1b1px0y0', 'bi0b1px1y0', 'bi1b1px1y0', 'T2', 'bi0b1px0y1', 'bi1b1px0y1', 'T5']
        transform_dict = {'b00px0y0sr1': ('bi0b0px0y0sr1', 'bi1b0px0y0sr1'),
                          'b01px0y0sP1': ('bi0b0px0y0sP1', 'bi1b1px0y0sP1'),
                          'b00px1y0sr1': ('bi0b0px1y0sr1', 'bi1b0px1y0sr1'),
                          'b01px1y0sP1': ('bi0b0px1y0sP1', 'bi1b1px1y0sP1'),
                          'b00px0y1sr1': ('bi0b0px0y1sr1', 'bi1b0px0y1sr1'),
                          'b01px0y1sP1': ('bi0b0px0y1sP1', 'bi1b1px0y1sP1'),
                          'b00px1y1sP1': ('bi0b0px1y1sP1', 'bi1b0px1y1sP1')}

        found_list = []

        for item in table:
            for key, value in transform_dict.items():
                if any(item in v for v in value):
                    found_list.append((item, key, value))

        #print(found_list)




        result = []
        for content in newTrueVars:
            for key in self.pixelList.reverse_dict.keys():
                if content in key:
                    result.append(key)
        return result