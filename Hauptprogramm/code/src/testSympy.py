from sympy import symbols, Implies, And, Or, to_cnf
from _sympyTransformer import SympyTransformer

class TestSympy:
    def __init__(self):
        # Symbole definieren
        A, B1, B2, B3 = symbols('A B1 B2 B3')

        # Ausdruck erstellen
        expr = Implies(A, And(B1, B2, B3))

        # Ausdruck in KNF umwandeln
        knf_expr = to_cnf(expr)

        print("A implies (B1 & B2 & B3)")
        # KNF-Ausdruck anzeigen
        print(knf_expr)



        # Symbole definieren
        A, B1, B2, B3 = symbols('A B1 B2 B3')

        # Ausdruck erstellen
        expr = Implies(And(B1, B2, B3), A)

        # Ausdruck in KNF umwandeln
        knf_expr = to_cnf(expr)

        print("(B1 & B2 & B3) implies A")
        # KNF-Ausdruck anzeigen
        print(knf_expr)



        # Symbole definieren
        A1, A2, A3, B1, B2, B3 = symbols('A1 A2 A3 B1 B2 B3')

        # Ausdruck erstellen
        expr = Implies(And(A1, A2, A3), And(B1, B2, B3))

        # Ausdruck in KNF umwandeln
        knf_expr = to_cnf(expr)

        print("(A1 & A2 & A3) implies (B1 & B2 & B3)")
        # KNF-Ausdruck anzeigen
        print(knf_expr)




        # Symbole definieren
        A1, A2, A3, B1, B2, B3 = symbols('A1 A2 A3 B1 B2 B3')

        # Ausdruck erstellen
        expr = Implies(And(~A1, ~A2, A3), And(B1, B2, B3))

        # Ausdruck in KNF umwandeln
        knf_expr = to_cnf(expr)

        print("(!A1 & !A2 & A3) implies (B1 & B2 & B3)")
        # KNF-Ausdruck anzeigen
        print(knf_expr)




        # Symbole definieren
        A1, A2, A3, B1, B2, B3 = symbols('A1 A2 A3 B1 B2 B3')

        # Ausdruck erstellen
        expr = Implies(And(B1, B2, B3), And(A1, A2, A3))

        # Ausdruck in KNF umwandeln
        knf_expr = to_cnf(expr)

        print("(B1, B2, B3) implies (A1 & A2 & A3)")
        # KNF-Ausdruck anzeigen
        print(knf_expr)




        # Symbole definieren
        A, B1, B2, B3, B4, B5, B6, B7 = symbols('A B1 B2 B3 B4 B5 B6 B7')

        # Ausdruck erstellen
        expr2 = Implies(And(B1, B2, B3, B4, B5, B6, B7), A)

        # Ausdruck in KNF umwandeln
        knf_expr2 = to_cnf(expr2)

        print("((B1 & B2 & B3 & B4 & B5 & B6 & B7) implies A)")
        # KNF-Ausdruck anzeigen
        print(knf_expr2)




        # Symbole definieren
        A, B1, B2, B3, B4, B5, B6, B7 = symbols('A B1 B2 B3 B4 B5 B6 B7')

        # Ausdruck erstellen
        expr1 = Implies(A, And(B1, B2, B3, B4, B5, B6, B7))

        # Ausdruck in KNF umwandeln
        knf_expr1 = to_cnf(expr1)

        print("(A implies (B1 & B2 & B3 & B4 & B5 & B6 & B7))")
        # KNF-Ausdruck anzeigen
        print(knf_expr1)




        # Symbole definieren
        A1, A2, B1, B2, C1, C2, D1, D2 = symbols('A1 A2 B1 B2 C1 C2 D1 D2')

        # Ausdruck erstellen
        expr = Or(And(A1, A2), And(B1, B2), And(C1, C2), And(D1, D2))

        # Ausdruck in KNF umwandeln
        knf_expr = to_cnf(expr)

        print("(A1 And A2) OR (B1 And B2) OR (C1 And C2) OR (D1 And D2)")

        # KNF-Ausdruck anzeigen
        print(knf_expr)



        # Symbole definieren
        A1, A2, B1, B2, C1, C2 = symbols('A1 A2 B1 B2 C1 C2')

        # Ausdrücke erstellen
        expr1 = Or(~(And(A1, A2)), ~(And(B1, B2)))
        expr2 = Or(~(And(A1, A2)), ~(And(C1, C2)))
        expr3 = Or(~(And(B1, B2)), ~(And(C1, C2)))

        # Gesamtausdruck erstellen
        expr = And(expr1, expr2, expr3)

        print("(NOT(A1 AND A2) OR NOT(B1 AND B2)) AND (NOT(A1 AND A2) OR NOT(C1 AND C2)) AND (NOT(B1 AND B2) OR NOT(C1 AND C2))")
        # Ausdruck in KNF umwandeln
        knf_expr = to_cnf(expr)

        # KNF-Ausdruck anzeigen
        print(knf_expr)

        X, Y, Z, C = symbols('X Y Z C')

        #(x∧¬y)∨(z∨(x∧¬w))
        # Ausdrücke erstellen
        expr1 = Or(And(X, ~Y), Or(Z, C))
        print("(x ∧ ¬ y) ∨ (z ∨ c)")
        knf_expr = to_cnf(expr1)
        print(knf_expr)

        tup1 = ('A1', 'A2')
        tup2 = ('B1', 'B2')
        sympyTransformer = SympyTransformer()
        result = sympyTransformer.iff_cnf(tup1, tup2)
        print(tup1, tup2)
        print(result)







        # Symbole definieren
        A1, A2, B1, B2, B3, C1, C2 = symbols('A1 A2 B1 B2 B3 C1 C2')

        # Ausdrücke erstellen
        expr1 = Or(~(And(A1, A2)), ~(And(B1, B2, B3)))
        expr2 = Or(~(And(A1, A2)), ~(And(C1, C2)))
        expr3 = Or(~(And(B1, B2, B3)), ~(And(C1, C2)))

        # Gesamtausdruck erstellen
        expr = And(expr1, expr2, expr3)

        print("(NOT(A1 AND A2) OR NOT(B1 AND B2 And B3)) AND (NOT(A1 AND A2) OR NOT(C1 AND C2)) AND (NOT(B1 AND B2 AND B3) OR NOT(C1 AND C2))")
        # Ausdruck in KNF umwandeln
        knf_expr = to_cnf(expr)

        # KNF-Ausdruck anzeigen
        print(knf_expr)


        data = [
            [('A1', 'A2'), ('B1', 'B2')],
            [('A1', 'A2'), ('B1', 'B2'), ('C1', 'C2')],
            [('A1', 'A2'), ('B1'), ('C1', 'C2')],
            [('A1', 'A2', 'A3'), ('B1', 'B2')],
            [('~A1', '~A2', '~A3'), ('~B1', '~B2')],
            [('A1', 'A2', 'A3'), ('B1', 'B2', 'B3')],
            [('A1', 'A2', 'A3', 'A4'), ('B1', 'B2', 'B3'), ('C1', 'C2', 'C3')],
            [('A1', 'A2', 'A3', 'A4'), ('B1', 'B2', 'B3', 'B4'), ('C1', 'C2', 'C3'), ('D1', 'D2', 'D3')],
            [('A1', 'A2', 'A3', 'A4', 'A5'), ('B1', 'B2', 'B3', 'B4', 'B5'), ('C1', 'C2', 'C3'), ('D1', 'D2', 'D3'),
             ('E1', 'E2', 'E3')]
        ]
        sympyTransformer = SympyTransformer()
        output_knf = sympyTransformer.atMostOne_cnf(data, testOnly=True)

        print("output_knf _ atMosteOne Test")
        print(data)
        print(output_knf)

        data2 = [[('A1', 'A2'), ('B1', 'B2')],
             [('~A1', '~A2'), ('~B1', '~B2')],
             [('A1', 'A2'), ('B1'), ('C1', 'C2')],
             [('A1', 'A2'), ('B1', 'B2'), ('C1', 'C2', 'C3')],
             [('A1', 'A2'), ('B1', 'B2'), ('C1', 'C2', 'C3'), ('D1', 'D2')],
        ]

        output_knf = sympyTransformer.clause_cnf(data2, testOnly=True)

        print("output_knf _ clause_cnf Test")
        print(data2)
        print(output_knf)

        data = [
            [('A1', 'A2'), ('B1', 'B2')],
            [('A1', 'A2'), ('B1', 'B2'), ('C1', 'C2')]
        ]
        sympyTransformer = SympyTransformer()
        output_knf = sympyTransformer.exactlyOne_cnf(data, testOnly=True)

        print("output_knf")
        print(output_knf)

        input2 = [
            [('bi0b0px0y0sI1', 'bi1b0px0y0sI1'), ('bi0b0px1y0sI1', 'bi1b0px1y0sI1')],
            [('bi0b0px0y1sI1', 'bi1b0px0y1sI1'), ('bi0b0px1y1sI1', 'bi1b0px1y1sI1')],
            [('bi0b0px2y0sI1', 'bi1b0px2y0sI1'), ('bi0b0px0y2sI1', 'bi1b0px0y2sI1')]
        ]

        output2 = sympyTransformer.atMostOne_cnf(input2)

        print("output2n")
        print(output2)

        input3 = [
            [('bi0b0px0y0sI1', 'bi1b0px0y0sI1', 'bi2b0px0y0sI1'), ('bi0b0px1y0sI1', 'bi1b0px1y0sI1', 'bi2b0px1y0sI1')],
            [('bi0b0px0y1sI1', 'bi1b0px0y1sI1', 'bi2b0px0y1sI1'), ('bi0b0px1y1sI1', 'bi1b0px1y1sI1', 'bi2b0px1y1sI1')],
            [('bi0b0px2y0sI1', 'bi1b0px2y0sI1', 'bi2b0px2y0sI1'), ('bi0b0px0y2sI1', 'bi1b0px0y2sI1', 'bi2b0px0y2sI1')],
        ]

        output3 = sympyTransformer.atMostOne_cnf(input3)

        print("output3s")
        print(output3)

        input4 = [
            [('bi0b0px0y0sI1', 'bi1b0px0y0sI1', 'bi2b0px0y0sI1', 'bi3b0px0y0sI1'),
             ('bi0b0px1y0sI1', 'bi1b0px1y0sI1', 'bi2b0px1y0sI1', 'bi3b0px1y0sI1')],
            [('bi0b0px0y1sI1', 'bi1b0px0y1sI1', 'bi2b0px0y1sI1', 'bi3b0px0y1sI1'),
             ('bi0b0px1y1sI1', 'bi1b0px1y1sI1', 'bi2b0px1y1sI1', 'bi3b0px1y1sI1')],
            [('bi0b0px2y0sI1', 'bi1b0px2y0sI1', 'bi2b0px2y0sI1', 'bi3b0px2y0sI1'),
             ('bi0b0px0y2sI1', 'bi1b0px0y2sI1', 'bi2b0px0y2sI1', 'bi3b0px0y2sI1')],
        ]

        output4 = sympyTransformer.atMostOne_cnf(input4)

        print("output4s")
        print(output4)

        input5 = [
            [('bi0b0px0y0sI1', 'bi1b0px0y0sI1', 'bi2b0px0y0sI1', 'bi3b0px0y0sI1', 'bi4b0px0y0sI1'),
             ('bi0b0px1y0sI1', 'bi1b0px1y0sI1', 'bi2b0px1y0sI1', 'bi3b0px1y0sI1', 'bi4b0px1y0sI1')],
            [('bi0b0px0y1sI1', 'bi1b0px0y1sI1', 'bi2b0px0y1sI1', 'bi3b0px0y1sI1', 'bi4b0px0y1sI1'),
             ('bi0b0px1y1sI1', 'bi1b0px1y1sI1', 'bi2b0px1y1sI1', 'bi3b0px1y1sI1', 'bi4b0px1y1sI1')],
            [('bi0b0px2y0sI1', 'bi1b0px2y0sI1', 'bi2b0px2y0sI1', 'bi3b0px2y0sI1', 'bi4b0px2y0sI1'),
             ('bi0b0px0y2sI1', 'bi1b0px0y2sI1', 'bi2b0px0y2sI1', 'bi3b0px0y2sI1', 'bi4b0px0y2sI1')],
        ]

        output5 = sympyTransformer.atMostOne_cnf(input5)

        print("output5s")
        print(output5)

