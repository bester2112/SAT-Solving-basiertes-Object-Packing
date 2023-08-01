print("Program started")

# First, we import the initialized sat helper class.
from src.sathelper import SatHelper
print("SatHelper imported")

#variables
sh = SatHelper()

#initialize variables
width = 2
height = 5

numberOfIs = 2
pieces = []
listOfIs = []
numberOfPixelsForOneI = 4
for indexI in range(numberOfIs):
    for indexPixelI in range(1, numberOfPixelsForOneI + 1):
        listOfIs.append("I" + str(indexI+1) + "P" + str(indexPixelI))

pieces += listOfIs

print("list of Is " , listOfIs)
#pieces = ["I", "IB1", "IB2", "IB3", "IB4", "IB5" 
#          "T", "TB",
#          "L", "LB",
#          "S", "SB",
#          "O", "OB",
#          "NaN"] # begin I, begin T, etc. 
# begin O2, Begin O2, Begin O3, Begin I1.
#add variables for field
for x in range(width):
    for y in range(height):
        for piece in pieces:
            print("p"+str(x)+str(y)+str(piece))
            sh.declareVariable(name="p"+str(x)+str(y)+str(piece))
print("field variables added")

for x in range(width):
    for y in range(height):
        piecesArray = [f"p"+str(x)+str(y)+str(i) for i in pieces]
        i = 0
        for piece in piecesArray:
            for letter in pieces:
                piece += letter

        print(piecesArray)
        sh.addAtMostOne(piecesArray) # maximum eins
        sh.addClause(piecesArray) # clausel minimum eins stelle sicher das genau 1 da ist
print("field atMostOne & addClause clausel added")

#I = 1 x 4 
#   0
# 0 X
# 1 X
# 2 X
# 3 X
# needed variables = 4
# I = [0,0], [0,1], [0,2], [0,3] // [X,Y] = [right, bottom]
# you don't need to add variables for the I 
# you just need to add implications
i_height = 4
i_width = 1

# add Klausel for I
for x in range(width):
    for y in range(height):
        for beginIndex in range(1,numberOfIs+1):
            if x + i_width <= width:
                if y + i_height <= height:
                    #sh.addImplies("p"+str(x)+str(y)+"IB"+str(beginIndex),
                    #              "p"+str(x)+str(y)+"IB")
                    sh.addEquivalent("p"+str(x)+str(y)+"I"+str(beginIndex)+"P1",
                                     "p"+str(x)+str(y+1)+"I"+str(beginIndex)+"P2")
                    sh.addEquivalent("p"+str(x)+str(y)+"I"+str(beginIndex)+"P1",
                                     "p"+str(x)+str(y+2)+"I"+str(beginIndex)+"P3")
                    sh.addEquivalent("p"+str(x)+str(y)+"I"+str(beginIndex)+"P1",
                                     "p"+str(x)+str(y+3)+"I"+str(beginIndex)+"P4")
                    print("p"+str(x)+str(y)+"I"+str(beginIndex)+"P1", " <=> ",
                          "p"+str(x)+str(y+1)+"I"+str(beginIndex)+"P2")
                    print("p"+str(x)+str(y)+"I"+str(beginIndex)+"P1", " <=> ",
                          "p"+str(x)+str(y+2)+"I"+str(beginIndex)+"P3")
                    print("p"+str(x)+str(y)+"I"+str(beginIndex)+"P1", " <=> ",
                          "p"+str(x)+str(y+3)+"I"+str(beginIndex)+"P4")
                        
for indexI in range(1, numberOfIs+1):
    listForI = []
    for x in range(width): 
        for y in range(height):
            if x + i_width <= width:
                if y + i_height <= height:
                    listForI.append("p"+str(x)+str(y)+"I"+str(indexI)+"P1")
    print("listForI " , listForI)
    sh.addClause(listForI)

print("I clausel added")




#O = 2 x 2
#   01
# 0 XX
# 1 XX
# needed variables = 4 // [X,Y] = [right, bottom]
# O = [0,0], [1,0], [0,1], [1,1]
# o_height = 2
# o_width = 2
# for x in range(o_width):
#     for y in range(o_height):
#         print("O"+str(x)+str(y))
#         sh.declareVariable("O"+str(x)+str(y))
# print("O variable added")

# # add Klausel for O
# for x in range(width):
#     for y in range(height):
#         if x + o_width <= width: 
#             if y + o_height <= height:
#                 sh.addClause(["p"+str(x)+str(y)+"O", 
#                               "p"+str(x+1)+str(y)+"O", 
#                               "p"+str(x)+str(y+1)+"O", 
#                               "p"+str(x+1)+str(y+1)+"O"])
#                 print(["p"+str(x)+str(y)+"O", 
#                        "p"+str(x+1)+str(y)+"O", 
#                        "p"+str(x)+str(y+1)+"O", 
#                        "p"+str(x+1)+str(y+1)+"O"])
# print("O clausel added")


# #T = 1x3 verknüpfung mit 1x1 an position [1,1]
# #   012
# # 0 XXX
# # 1  X
# # needed variables = 4 // [X,Y] = [right, bottom]
# # T = [0,0], [1,0], [2,0], [1,1]
# t_height = 2
# t_width = 3
# for x in range(t_width):
#     print("T"+str(x)+"0")
#     sh.declareVariable("T"+str(x)+"0")
# print("T11")
# sh.declareVariable("T11")

# print("T variable added")

# # add Klausel for T
# for x in range(width):
#     for y in range(height):
#         if x + t_width <= width:  
#             if y + t_height <= height:
#                 sh.addClause(["p"+str(x)+str(y)+"T", 
#                               "p"+str(x+1)+str(y)+"T", 
#                               "p"+str(x+2)+str(y)+"T", 
#                               "p"+str(x+1)+str(y+1)+"T"])
#                 print(["p"+str(x)+str(y)+"T", 
#                         "p"+str(x+1)+str(y)+"T", 
#                         "p"+str(x+2)+str(y)+"T", 
#                         "p"+str(x+1)+str(y+1)+"T"])
# print("T clausel added")


# #S = 2 x 1 verknüpfungmit 2x1 (um 1 nach rechts & 1 nach oben verschoben)
# #   012
# # 0  XX
# # 1 XX
# # needed variables = 4 // [X,Y] = [right, bottom]
# # S = [0,1], [1,1], [1,0], [2,0]
# s_height = 2
# s_width = 3
# for x in range(2):
#     print("S"+str(x)+"1")
#     sh.declareVariable("S"+str(x)+"1")

# for x in range(1,3):
#     print("S"+str(x)+"0")
#     sh.declareVariable("S"+str(x)+"0")
# print("S variable added")

# # add Klausel for S
# for x in range(width):
#     for y in range(height):
#         if x + s_width <= width:  
#             if y + s_height <= height:
#                 sh.addClause(["p"+str(x)+str(y+1)+"S", 
#                               "p"+str(x+1)+str(y+1)+"S", 
#                               "p"+str(x+1)+str(y)+"S", 
#                               "p"+str(x+2)+str(y)+"S"])
#                 print(["p"+str(x)+str(y+1)+"S", 
#                         "p"+str(x+1)+str(y+1)+"S", 
#                         "p"+str(x+1)+str(y)+"S", 
#                         "p"+str(x+2)+str(y)+"S"])
# print("S clausel added")

# #L = 3 x 2
# #   012
# # 0 X
# # 1 XXX
# # needed variables = 4
# # L = [0,0], [0,1], [1,1], [2,1]
# l_height = 2
# l_width = 3
# for x in range(l_width):
#     print("L"+str(x)+"1")
#     sh.declareVariable("L"+str(x)+"1")

# print("L00")
# sh.declareVariable("L00")
# print("L variable added")


# # add Klausel for L
# for x in range(width):
#     for y in range(height):
#         if x + l_width <= width:  
#             if y + l_height <= height:
#                 sh.addClause(["p"+str(x)+str(y)+"L", 
#                               "p"+str(x)+str(y+1)+"L", 
#                               "p"+str(x+1)+str(y+1)+"L", 
#                               "p"+str(x+2)+str(y+1)+"L"])
#                 print(["p"+str(x)+str(y)+"L", 
#                         "p"+str(x)+str(y+1)+"L", 
#                         "p"+str(x+1)+str(y+1)+"L", 
#                         "p"+str(x+2)+str(y+1)+"L"])
# print("L clausel added")

#sh.printFormulaFile()
sh.printFormula()
#print("printed formula")

sh.solveSat()
print("SAT solved")

print("Program finished")