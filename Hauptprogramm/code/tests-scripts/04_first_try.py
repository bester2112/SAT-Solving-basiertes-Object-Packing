print("Program started")
# First, we import the initialized sat helper class.
from SatHelper import sh
print("SatHelper imported")

#testing variables:
test_row = [
['s111', 's112', 's113', 's114', 's115', 's116', 's117', 's118', 's119'],
['s121', 's122', 's123', 's124', 's125', 's126', 's127', 's128', 's129'],
['s131', 's132', 's133', 's134', 's135', 's136', 's137', 's138', 's139'],
['s141', 's142', 's143', 's144', 's145', 's146', 's147', 's148', 's149'],
['s151', 's152', 's153', 's154', 's155', 's156', 's157', 's158', 's159'],
['s161', 's162', 's163', 's164', 's165', 's166', 's167', 's168', 's169'],
['s171', 's172', 's173', 's174', 's175', 's176', 's177', 's178', 's179'],
['s181', 's182', 's183', 's184', 's185', 's186', 's187', 's188', 's189'],
['s191', 's192', 's193', 's194', 's195', 's196', 's197', 's198', 's199']]

test_column = [
['s111', 's112', 's113', 's114', 's115', 's116', 's117', 's118', 's119'],
['s211', 's212', 's213', 's214', 's215', 's216', 's217', 's218', 's219'],
['s311', 's312', 's313', 's314', 's315', 's316', 's317', 's318', 's319'],
['s411', 's412', 's413', 's414', 's415', 's416', 's417', 's418', 's419'],
['s511', 's512', 's513', 's514', 's515', 's516', 's517', 's518', 's519'],
['s611', 's612', 's613', 's614', 's615', 's616', 's617', 's618', 's619'],
['s711', 's712', 's713', 's714', 's715', 's716', 's717', 's718', 's719'],
['s811', 's812', 's813', 's814', 's815', 's816', 's817', 's818', 's819'],
['s911', 's912', 's913', 's914', 's915', 's916', 's917', 's918', 's919']]
print("test variables created")


cnumber_i=1
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
print("variables created")
# it need to be 9 x 9 x 9 variables to be declared
for x in numbers:
    for y in numbers:
        for z in numbers:
            sh.declareVariable("s"+str(x)+str(y)+str(z))         
            print(cnumber_i, x, y, z)
            cnumber_i += 1

# welt schwerstes sudoku einspeichern
sh.addClause(["s118"])
sh.addClause(["s323"])
sh.addClause(["s237"])
sh.addClause(["s426"])
sh.addClause(["s539"])
sh.addClause(["s732"])
sh.addClause(["s245"])
sh.addClause(["s647"])
sh.addClause(["s554"])
sh.addClause(["s655"])
sh.addClause(["s757"])
sh.addClause(["s461"])
sh.addClause(["s863"])
sh.addClause(["s371"])
sh.addClause(["s876"])
sh.addClause(["s978"])
sh.addClause(["s388"])
sh.addClause(["s485"])
sh.addClause(["s881"])
sh.addClause(["s299"])
sh.addClause(["s794"])
print("world hardest sudoku added")

# in jedem Feld ist mindestens eine Zahl
# in jeder Zelle muss sich eine Zahl befinden
print("there is at least one number in each entry")
allCellUnique = [[f"s{x}{y}{i}" for i in numbers] for y in numbers for x in numbers]
#print(allCellUnique)
#print("---------------------------")
counting_i = 0
while(counting_i < 81):
    print(allCellUnique[counting_i])
    ####### NOT SURE WHICH ONE #######
#    sh.addAtMostOne(allCellUnique[counting_i])
    sh.addClause(allCellUnique[counting_i])
    counting_i+=1
    #print(counting_i)

#sh.printFormula()

print("-----------------------")

# in jeder ZEILE ist mindestens eine Zahl 
print("each number appears at most once in each row")
row = [[f"s1{y}{i}" for i in numbers] for y in numbers]
assert row == test_row, "Assert - rows are not equal"

for z in numbers: 
    print("Zeile AMO:", z, row[z-1])
#    sh.addAtMostOne(row[z-1])

for y in numbers:
    for z in numbers:
        for x in range(1,9):
            for i in range(x+1, 10):
                sh.addClause(["-s"+str(x)+str(y)+str(z), "-s"+str(i)+str(y)+str(z)])

print("-----------------------")

#in jeder SPALTE ist mindestens eine Zahl
print("each number appears at most once in each column")
column = [[f"s{x}1{i}" for i in numbers]for x in numbers]
assert column == test_column, "Assert - rows are not equal"

for z in numbers: 
    #print("Spalt AMO:", z, column[z-1])
    print(column[z-1])
#    sh.addAtMostOne(column[z-1])


for x in numbers:
    for z in numbers:
        for y in range(1,9):
            for i in range(y+1, 10):
                sh.addClause(["-s"+str(x)+str(y)+str(z), "-s"+str(x)+str(i)+str(z)])


# !s(3*i+x)(3*j+y)z v !s(3*i+x)(3*j+k)z
# !s(3*i+x)(3*j+y)z v !s(3*i+k)(3*j+l)z
print("each number appears at most once in each 3x3 sub-grid")
for z in numbers:
    for i in range(0,3):
        for j in range(0,3):
            for x in range(1,4):
                for y in range(1,4):
                    for k in range(y+1, 4): 
                        sh.addClause(["-s"+str(3*i+x)+str(3*j+y)+str(z), 
                                      "-s"+str(3*i+x)+str(3*j+k)+str(z)])
                        #print(["-s"+str(3*i+x)+str(3*j+y)+str(z), 
                        #       "-s"+str(3*i+x)+str(3*j+k)+str(z)])

for z in numbers:
    for i in range(0,3):
        for j in range(0,3):
            for x in range(1,4):
                for y in range(1,4):
                    for k in range(x+1, 4): 
                        for l in range(1,4):
                            sh.addClause(["-s"+str(3*i+x)+str(3*j+y)+str(z), 
                                          "-s"+str(3*i+k)+str(3*j+l)+str(z)])
                            #print(["-s"+str(3*i+x)+str(3*j+y)+str(z), 
                            #       "-s"+str(3*i+k)+str(3*j+l)+str(z)])
print("3x3 grid added")

sh.printFormulaFile()
sh.printFormula()
print("printed formula")

sh.solveSat()
print("SAT solved")

print("Program finished")