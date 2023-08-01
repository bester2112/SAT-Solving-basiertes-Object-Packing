import src._clauselCalculator as clauselC

import sympy as sp
from sympy.logic.boolalg import Not, Or, And, truth_table, Implies, Equivalent
from sympy import symbols, And, Or, Not, simplify
def test_binary_Clausel_Calculator_get_Symbol():
    clauselCalculator = clauselC.ClauselCalculator("", "", "", "", "")

    # Example usage
    input_str = "~(A | B) | D"
    input_string = "OR(Not(OR(A,B), D)"
    a1, b1, c1, d1 = sp.symbols("a, b, c, d")
    atoms = (a1 & b1).atoms()
    a = clauselCalculator.get_Symbol("a")
    b = clauselCalculator.get_Symbol("b")
    c = clauselCalculator.get_Symbol("c")
    d = clauselCalculator.get_Symbol("d")
    assert a1 == a
    assert b1 == b
    assert c1 == c
    assert d1 == d

def test_binary_Clausel_Calculator_Implies_and_Equals():
    print()
    clauselCalculator = clauselC.ClauselCalculator("", "", "", "", "")
    a = clauselCalculator.get_Symbol("a")
    b = clauselCalculator.get_Symbol("b")
    c = clauselCalculator.get_Symbol("c")
    d = clauselCalculator.get_Symbol("d")
    assert (a >> b) == Implies(a, b)
    print(a >> b)
    assert (~b >> ~a) == Implies(~b, ~a)
    print(~b >> ~a)
    assert clauselCalculator.expression_equals((a >> b), (~b >> ~a))
    print(clauselCalculator.expression_equals((a >> b), (~b >> ~a)))
    assert clauselCalculator.expression_equals((a >> b), (Not(b) >> Not(a)))
    print(clauselCalculator.expression_equals((a >> b), (Not(b) >> Not(a))))

def test_binary_Clausel_Calculator_Equivalent():
    print()
    clauselCalculator = clauselC.ClauselCalculator("", "", "", "", "")
    a = clauselCalculator.get_Symbol("a")
    b = clauselCalculator.get_Symbol("b")
    c = clauselCalculator.get_Symbol("c")
    d = clauselCalculator.get_Symbol("d")
    print(sp.simplify((a >> b), (Not(b) >> Not(a))))
    print(clauselCalculator.get_cnf(clauselCalculator.get_equivalent((a >> b), (Not(b) >> Not(a)))))
    assert clauselCalculator.expression_equals(clauselCalculator.get_equivalent((a >> b), (Not(b) >> Not(a))), ((a | b | ~a) & (b | ~a | ~b)))

def test_binary_Clausel_Calculator_Truthtable():
    print()
    clauselCalculator = clauselC.ClauselCalculator("", "", "", "", "")
    a = clauselCalculator.get_Symbol("a")
    b = clauselCalculator.get_Symbol("b")
    c = clauselCalculator.get_Symbol("c")
    d = clauselCalculator.get_Symbol("d")
    expr1 = clauselCalculator.get_equivalent((a & b), (c & d))
    expr2 = (Not(a) | Not(b) | c) & (Not(a) | Not(b) | d) & (a | Not(c) | Not(d)) & (b | Not(c) | Not(d))
    expr3 = Not(a | b) | d
    temp1 = clauselCalculator.get_cnf(expr1)
    print(temp1)
    temp2 = clauselCalculator.get_cnf(expr2)
    print(temp2)
    print(clauselCalculator.expression_equals(temp1, temp2))
    #assert clauselCalculator.expression_equals(temp1, temp2)
    variables1, truth_table1 = clauselCalculator.get_truth_table(expr1)
    variables2, truth_table2 = clauselCalculator.get_truth_table(expr2)
    print("table1")
    clauselCalculator.print_truth_table(truth_table1, variables1, expr1)
    print("table2")
    clauselCalculator.print_truth_table(truth_table2, variables2, expr2)
    print("table1 == table2 ?")
    print(clauselCalculator.compare_truth_tables(truth_table1, truth_table2))
    #assert clauselCalculator.compare_truth_tables(truth_table1, truth_table2)

    variables, tt = clauselCalculator.get_truth_table(expr3)

    #true_expressions = clauselCalculator.generate_expression_from_true_rows(tt, variables)
    #for expression in true_expressions:
    #    print(expression)

    #combined_expression = clauselCalculator.combine_expression_list(true_expressions)
    #print(combined_expression)
    expr4 = (d | b | a) & (Not(d) | b | a) & (Not(d) | b | Not(a)) & (Not(d) | Not(b) | a) & (Not(d) | Not(b) | Not(a))

    variables3, truth_table3 = clauselCalculator.get_truth_table(expr3)
    variables4, truth_table4 = clauselCalculator.get_truth_table(expr4)
    print("table3")
    clauselCalculator.print_truth_table(truth_table3, variables3, expr3)
    print("table4")
    clauselCalculator.print_truth_table(truth_table4, variables4, expr4)
    print("table3 == table4 ?")
    print(clauselCalculator.compare_truth_tables(truth_table3, truth_table4))
    #assert not clauselCalculator.compare_truth_tables(truth_table3, truth_table4)

    expr5 = (Not(a) | c) & (a | b)
    expr6 = (c | b | a) & (c | b | Not(a)) & (c | Not(b) | Not(a)) & (Not(c) | b | a)
    # expr6 = (a | c) & (a | b)
    expr5 = (a | ~b) & (a | ~c) & (b | ~a) & (b | ~d) & (~a | ~c) & (~d | ~b) & (~d | ~c)
    expr5 = (a | d | ~b) & (a | d | ~c) & (b | c | ~a) & (b | c | ~d)
    expr6 = ((~a) | c | d) & (a | b | (~c)) & (a | b | (~d)) & ((~b) | c | d)
    expr5 = sp.to_cnf(expr5)
    expr6 = sp.to_cnf(expr6)

    variables5, table5 = clauselCalculator.get_truth_table(expr5)
    print("table5")
    clauselCalculator.print_truth_table(table5, variables5, expr5)

    #true_expressions = clauselCalculator.generate_expression_from_true_rows(table5, variables5)
    #for expression in true_expressions:
    #    print(expression)

    #combined_expression = clauselCalculator.combine_expression_list(true_expressions)
    #print(combined_expression)

    variables5, truth_table5 = clauselCalculator.get_truth_table(expr5)
    variables6, truth_table6 = clauselCalculator.get_truth_table(expr6)
    print("table5")
    clauselCalculator.print_truth_table(truth_table5, variables5, expr5)
    print("table6")
    clauselCalculator.print_truth_table(truth_table6, variables6, expr6)
    print("table5 == table6 ?")
    print(clauselCalculator.compare_truth_tables(truth_table5, truth_table6))
    #assert clauselCalculator.compare_truth_tables(truth_table5, truth_table6)

    variables5, truth_table5 = clauselCalculator.get_truth_table_reverse(expr5, reverse=True)
    variables6, truth_table6 = clauselCalculator.get_truth_table_reverse(expr6, reverse=True)
    print("table55")
    clauselCalculator.print_truth_table_reverse(truth_table5, variables5, expr5, reverse=True)
    print("table66")
    clauselCalculator.print_truth_table_reverse(truth_table6, variables6, expr6, reverse=True)
    #assert clauselCalculator.compare_truth_tables(truth_table5, truth_table6)

    variables5, truth_table5 = clauselCalculator.get_truth_table_reverse(expr5, reverse=False)
    variables6, truth_table6 = clauselCalculator.get_truth_table_reverse(expr6, reverse=False)
    print("table5")
    clauselCalculator.print_truth_table_reverse(truth_table5, variables5, expr5, reverse=False)
    print("table6")
    clauselCalculator.print_truth_table_reverse(truth_table6, variables6, expr6, reverse=False)
    #assert clauselCalculator.compare_truth_tables(truth_table5, truth_table6)


def test_binary_Clausel_Calculator_List_To_Expression_And_Negation():
    print()
    clauselCalculator = clauselC.ClauselCalculator("", "", "", "", "")

    # Example usage
    expr1List = ['g_2_0_b1', '!g_2_0_b2', '!g_2_0_b3', 'g_2_0_b4', '!g_2_0_b5', 'g_2_0_b6']
    expr2List = ['g_2_0_b1', '!g_2_0_b2', '!g_2_0_b3', 'g_2_0_b4', '!g_2_0_b5', '!g_2_0_b6']

    new_expr1_list = clauselCalculator.expression_replace_sign_in_list(expr1List, "!", "~")
    new_expr2_list = clauselCalculator.expression_replace_sign_in_list(expr2List, "!", "~")

    new_expr1 = clauselCalculator.combine_expression_list(new_expr1_list)
    new_expr2 = clauselCalculator.combine_expression_list(new_expr2_list)

    new_expr1_cnf = clauselCalculator.get_cnf(new_expr1)
    new_expr2_cnf = clauselCalculator.get_cnf(new_expr2)

    print("CNF of expr1:", new_expr1_cnf)
    print("CNF of expr2:", new_expr2_cnf)
    result = clauselCalculator.compare_expressions(new_expr1, new_expr2)
    print("Are expr1 and expr2 equivalent?", result)
    assert result == False

    expr1List = ['g_2_0_b1', '~g_2_0_b2', '~g_2_0_b3', 'g_2_0_b4', '~g_2_0_b5', '~g_2_0_b6']
    expr2List = ['g_2_0_b1', '~g_2_0_b2', '~g_2_0_b3', 'g_2_0_b4', '~g_2_0_b5', '~g_2_0_b6']

    new_expr1_list = clauselCalculator.expression_replace_sign_in_list(expr1List, "!", "~")
    new_expr2_list = clauselCalculator.expression_replace_sign_in_list(expr2List, "!", "~")

    new_expr1 = clauselCalculator.combine_expression_list(new_expr1_list)
    new_expr2 = clauselCalculator.combine_expression_list(new_expr2_list)

    new_expr1_cnf = clauselCalculator.get_cnf(new_expr1)
    new_expr2_cnf = clauselCalculator.get_cnf(new_expr2)

    print("CNF of expr1:", new_expr1_cnf)
    print("CNF of expr2:", new_expr2_cnf)
    result = clauselCalculator.compare_expressions(new_expr1, new_expr2)
    print("Are expr1 and expr2 equivalent?", result)
    assert result == True

    expr1 = clauselCalculator.combine_expression_list(['a', 'b'])
    expr2 = clauselCalculator.combine_expression_list(['d', '~e', '~f'])

    negated_expr1 = clauselCalculator.negate_expression(expr1)
    negated_expr2 = clauselCalculator.negate_expression(expr2)

    assert negated_expr1 == ~ sp.sympify(expr1)
    assert negated_expr2 == ~ sp.sympify(expr2)

    # Negate expression
    print("Negated expr1:", str(negated_expr1))
    print("Negated expr2:", str(negated_expr2))

def test_binary_Clausel_Calculator_List_To_Expression_And_Implication_and_Equivalence():
    print()
    clauselCalculator = clauselC.ClauselCalculator("", "", "", "", "")

    expr1 = clauselCalculator.combine_expression_list(['a', 'b'])
    expr2 = clauselCalculator.combine_expression_list(['d', '~e', '~f'])

    # Implication
    print("Implication (expr1 => expr2):", clauselCalculator.implies(expr1, expr2))
    expressionSol = sp.sympify("((~ a) | (~ b) | d) & ((~ a) | (~ b) | (~ e)) & ((~ a) | (~ b) | (~ f))")
    assert clauselCalculator.implies(expr1, expr2) == expressionSol

    # Equivalence
    print("Equivalence (expr1 <=> expr2):", clauselCalculator.equivalent(expr1, expr2))
    expressionSol = sp.sympify("((~ a) | (~ b) | d) & ((~ a) | (~ b) | (~ e)) & ((~ a) | (~ b) | (~ f)) & (a | (~ d) | e | f) & (b | (~ d) | e | f)")
    assert clauselCalculator.equivalent(expr1, expr2) == expressionSol

def test_binary_Clausel_Calculator_List_of_Expressions_And_Negate():
    print()
    clauselCalculator = clauselC.ClauselCalculator("", "", "", "", "")

    expr1 = ['a & b']
    expr2 = ['c | d']
    expr3 = ['a & b | a & ~b']

    expr_list = ['a & b', 'c | d', 'a & b | a & ~b']
    negated_expr_list = clauselCalculator.negate_expression_list(expr_list)
    print(negated_expr_list)

    expr1.extend(expr2)
    expr1.extend(expr3)
    print(expr1)

    negated_expr1 = clauselCalculator.negate_expression_list(expr1)

    assert negated_expr1 == negated_expr_list

def test_binary_Clausel_Calculator_List_of_Expressions_Implication_And_Equivalent():
    print()
    clauselCalculator = clauselC.ClauselCalculator("", "", "", "", "")

    expr1_list = ['a & b']
    expr2_list = ['c | d']
    expr3_list = ['a & b | a & ~b', 'b | a & ~b']
    #expr1_list = ['a']

    expr1 = clauselCalculator.combine_expression_list(expr1_list)
    expr2 = clauselCalculator.combine_expression_list(expr2_list)
    expr3 = clauselCalculator.combine_expression_list(expr3_list)

    # Implication
    implicationResult = clauselCalculator.implies(expr1, expr2)
    assert implicationResult == clauselCalculator.get_cnf(Implies(expr1, expr2))
    print("Implication (expr1 => expr2):", implicationResult)

    # Equivalence
    equivalenceResult = clauselCalculator.equivalent(expr1, expr2)
    variables1, truth_table1 = clauselCalculator.get_truth_table_reverse(equivalenceResult, reverse=False)
    clauselCalculator.print_truth_table_reverse(truth_table1, variables1, equivalenceResult, reverse=False)
    expr1 = sp.sympify(expr1)
    expr2 = sp.sympify(expr2)
    equialvalentExpr = Equivalent(expr1, expr2)
    equialvalentExpr = clauselCalculator.get_cnf(equialvalentExpr)
    variables2, truth_table2 = clauselCalculator.get_truth_table_reverse(equialvalentExpr, reverse=False)
    clauselCalculator.print_truth_table_reverse(truth_table2, variables2, equialvalentExpr, reverse=False)
    #wolframAlpaExpr = clauselCalculator.string_to_sympy_bool_expr("((Not a) Or c Or d) And (a Or (Not c)) And (a Or (Not d))")
    wolframAlpaExpr = clauselCalculator.string_to_sympy_bool_expr("((Not a) Or (Not b) Or c Or d) And (a Or (Not c)) And (a Or (Not d)) And (b Or (Not c)) And (b Or (Not d))")
    assert wolframAlpaExpr == equialvalentExpr
    assert clauselCalculator.get_cnf(equialvalentExpr) == equivalenceResult
    assert clauselCalculator.compare_truth_tables(truth_table1, truth_table2)
    print("Equivalence (expr1 <=> expr2):", equivalenceResult)

def test_binary_Clausel_Calculator_List_of_Expressions_Equivalent():
    print()
    clauselCalculator = clauselC.ClauselCalculator("", "", "", "", "")
    #expr1 = ['a', 'b']
    expr2 = ['a | b']
    expr3 = ['a & b | a & ~b']
    expr4 = ['~a | ~b | c | d']
    expr5 = ['(~a | d) & (~b | d) & (c | d)']

    result1 = clauselCalculator.is_equivalent(expr2, expr3)
    result2 = clauselCalculator.is_equivalent(expr2, expr4)
    result3 = clauselCalculator.is_equivalent(expr4, expr5)

    print("Are expr1 and expr2 equivalent?", result1)
    print("Are expr1 and expr3 equivalent?", result2)
    print("Are expr1 and expr3 equivalent?", result3)

    assert result1 == False
    assert result2 == False
    assert result3 == False

def test_binary_Clausel_Calculator_Print_Truth_Table_no_test():
    print()
    clauselCalculator = clauselC.ClauselCalculator("", "", "", "", "")

    expr1 = ['a & b']
    expr2 = ['a & b', 'c & d', 'e & f', 'g & h', 'i']

    print("Truth table for expr1:")
    variables1, truth_table1 = clauselCalculator.get_truth_table(expr1)
    clauselCalculator.print_truth_table(truth_table1, variables1, expr1)
    print("\nTruth table for expr2:")
    variables2, truth_table2 = clauselCalculator.get_truth_table(expr2)
    clauselCalculator.print_truth_table(truth_table2, variables2, expr2)

def test_binary_Clausel_Calculator_Print_Truth_Table_no_test2():
    print()
    clauselCalculator = clauselC.ClauselCalculator("", "", "", "", "")

    # #
    #
    # expr4 = ['!a | !b | c | d']
    # expr5 = ['(!a | d) & (!b | d) & (c | d)']
    # print("\nTruth table for expr4:")
    # clauselCalculator.print_truth_table(expr4)
    # print("\nTruth table for expr5:")
    # clauselCalculator.print_truth_table(expr5)
    # print("Are expr4 and expr5 equivalent?", clauselCalculator.is_equivalent(expr4, expr5))
    # print("Are expr4 and expr5 equivalent?", clauselCalculator.is_equivalent2(expr4, expr5))

def test_binary_Clausel_Calculator_allBinaryVariableName():
    print()
    clauselCalculator = clauselC.ClauselCalculator("", "", "", "", "")
    mapBinaryForNotUs = {"a": ['110', '101'], "b": ['010', '111']}
    mapBinaryForAllUs = {"c": ['001', '100'], "d": ['011', '000']}
    allBinaryVariableName = clauselCalculator.getAllUniqueVariableNames(mapBinaryForNotUs, mapBinaryForAllUs)
    assert allBinaryVariableName == {'100', '011', '111', '010', '110', '001', '101', '000'}


def test_binary_Clausel_Calculator_Truthtable_4_Equivalents_():
    print()
    clauselCalculator = clauselC.ClauselCalculator("", "", "", "", "")
    a = clauselCalculator.get_Symbol("a")
    b = clauselCalculator.get_Symbol("b")
    c = clauselCalculator.get_Symbol("c")
    d = clauselCalculator.get_Symbol("d")

    expr5 = Equivalent(a, b) & Equivalent(a, c) & Equivalent(a, d)
    expr6 = Equivalent(a, b) & Equivalent(b, c) & Equivalent(c, d)
    expr6 = ((~ a) | (~ b) | c) & ((~ a) | (~ b) | d) & (a | (~ c) | (~ d)) & (b | (~ c) | (~ d))
    expr5 = Equivalent(And(a, b), And(c, d))
    # expr6 = (a | c) & (a | b)

    #variables5, table5 = clauselCalculator.get_truth_table(expr5)
    #print("table5")
    #clauselCalculator.print_truth_table(table5, variables5, expr5)

    #true_expressions = clauselCalculator.generate_expression_from_true_rows(table5, variables5)
    #for expression in true_expressions:
    #    print(expression)

    #combined_expression = clauselCalculator.combine_expression_list(true_expressions)
    #print(combined_expression)

    #variables5, truth_table5 = clauselCalculator.get_truth_table(expr5)
    #variables6, truth_table6 = clauselCalculator.get_truth_table(expr6)
    #print("table5")
    #clauselCalculator.print_truth_table(truth_table5, variables5, expr5)
    #print("table6")
    #clauselCalculator.print_truth_table(truth_table6, variables6, expr6)
    #print("table5 == table6 ?")
    #print(clauselCalculator.compare_truth_tables(truth_table5, truth_table6))
    #assert clauselCalculator.compare_truth_tables(truth_table5, truth_table6)

    variables5, truth_table5 = clauselCalculator.get_truth_table_reverse(expr5, reverse=True)
    variables6, truth_table6 = clauselCalculator.get_truth_table_reverse(expr6, reverse=True)
    print("table5")
    clauselCalculator.print_truth_table_reverse(truth_table5, variables5, expr5, reverse=True)
    print("table6")
    clauselCalculator.print_truth_table_reverse(truth_table6, variables6, expr6, reverse=True)
    assert clauselCalculator.compare_truth_tables(truth_table5, truth_table6)

    variables5, truth_table5 = clauselCalculator.get_truth_table_reverse(expr5, reverse=False)
    variables6, truth_table6 = clauselCalculator.get_truth_table_reverse(expr6, reverse=False)
    print("table5")
    clauselCalculator.print_truth_table_reverse(truth_table5, variables5, expr5, reverse=False)
    print("table6")
    clauselCalculator.print_truth_table_reverse(truth_table6, variables6, expr6, reverse=False)
    assert clauselCalculator.compare_truth_tables(truth_table5, truth_table6)

def test_binary_Clausel_Calculator_Truthtable_4_Equivalents():
    print()
    clauselCalculator = clauselC.ClauselCalculator("", "", "", "", "")
    binary_var_list = [['~g_0_0_b1', '~g_0_0_b2', '~g_0_0_b3', '~g_0_0_b4', '~g_0_0_b5'],
                       ['~g_0_0_b1', '~g_0_0_b2', '~g_0_0_b3', '~g_0_0_b4', 'g_0_0_b5'],
                       ]
    true_values = ['g_0_0_b1', 'g_0_0_b2', 'g_0_0_b3', 'g_0_0_b4', 'g_0_0_b5', 'g_0_10_b1', 'g_0_10_b4', 'g_0_10_b6',
                   'g_0_11_b1', 'g_0_11_b6', 'g_0_12_b1', 'g_0_13_b1', 'g_0_13_b2', 'g_0_13_b3', 'g_0_13_b4',
                   'g_0_13_b5', 'g_0_13_b6', 'g_0_14_b1', 'g_0_14_b2', 'g_0_14_b3', 'g_0_14_b4', 'g_0_14_b5',
                   'g_0_1_b1', 'g_0_1_b2', 'g_0_1_b4', 'g_0_1_b5', 'g_0_1_b6', 'g_0_2_b1', 'g_0_2_b4', 'g_0_2_b6',
                   'g_0_3_b1', 'g_0_3_b6', 'g_0_4_b1', 'g_0_5_b1', 'g_0_5_b2', 'g_0_5_b3', 'g_0_5_b6', 'g_0_6_b1',
                   'g_0_6_b4', 'g_0_6_b6', 'g_0_7_b1', 'g_0_7_b6', 'g_0_8_b1', 'g_0_9_b1', 'g_0_9_b2', 'g_0_9_b3',
                   'g_0_9_b6', 'g_1_0_b1', 'g_1_0_b2', 'g_1_0_b3', 'g_1_0_b4', 'g_1_0_b5', 'g_1_0_b6', 'g_1_10_b2',
                   'g_1_10_b3', 'g_1_10_b5', 'g_1_11_b1', 'g_1_11_b2', 'g_1_11_b3', 'g_1_11_b4', 'g_1_11_b5',
                   'g_1_12_b1', 'g_1_12_b2', 'g_1_12_b4', 'g_1_12_b5', 'g_1_12_b6', 'g_1_13_b1', 'g_1_13_b2',
                   'g_1_13_b3', 'g_1_13_b4', 'g_1_13_b5', 'g_1_13_b6', 'g_1_14_b1', 'g_1_14_b2', 'g_1_14_b3',
                   'g_1_14_b4', 'g_1_14_b5', 'g_1_14_b6', 'g_1_1_b2', 'g_1_1_b3', 'g_1_1_b5', 'g_1_1_b6', 'g_1_2_b2',
                   'g_1_2_b3', 'g_1_2_b5', 'g_1_3_b1', 'g_1_3_b2', 'g_1_3_b3', 'g_1_3_b4', 'g_1_3_b5', 'g_1_4_b1',
                   'g_1_4_b2', 'g_1_4_b4', 'g_1_4_b5', 'g_1_4_b6', 'g_1_5_b2', 'g_1_5_b3', 'g_1_5_b5', 'g_1_5_b6',
                   'g_1_6_b2']

from itertools import product

def tseitin_transformation(formula):
    counter = 1
    def tseitin_helper(f):
        nonlocal counter
        if isinstance(f, And):
            a = symbols('a_{}'.format(counter))
            counter += 1
            and_clauses = And(*(Or(~a, tseitin_helper(arg)) for arg in f.args))
            and_clause = And(a, *f.args)
            return And(and_clauses, and_clause)
        elif isinstance(f, Or):
            a = symbols('a_{}'.format(counter))
            counter += 1
            or_clauses = And(*(Or(a, ~tseitin_helper(arg)) for arg in f.args))
            or_clause = Or(~a, *f.args)
            return And(or_clauses, or_clause)
        elif isinstance(f, Not):
            return Not(tseitin_helper(f.args[0]))
        else:
            return f
    tseitin_formula = tseitin_helper(formula)
    return simplify(tseitin_formula)

def to_cnf_custom(formula):
    if isinstance(formula, And):
        conjuncts = [to_cnf_custom(arg) for arg in formula.args]
        return distribute_and_over_or_recursive(*conjuncts)
    elif isinstance(formula, Or):
        disjuncts = [to_cnf_custom(arg) for arg in formula.args]
        return Or(*disjuncts)
    elif isinstance(formula, Not):
        return Not(to_cnf_custom(formula.args[0]))
    else:
        return formula

def distribute_and_over_or(A, B):
    if isinstance(A, Or) and isinstance(B, Or):
        return And(*[Or(a, b) for a in A.args for b in B.args])
    elif isinstance(A, Or):
        return And(*[Or(a, B) for a in A.args])
    elif isinstance(B, Or):
        return And(*[Or(A, b) for b in B.args])
    else:
        return And(A, B)

def distribute_and_over_or_recursive(*conjuncts):
    if len(conjuncts) == 1:
        return conjuncts[0]
    elif len(conjuncts) == 2:
        return distribute_and_over_or(conjuncts[0], conjuncts[1])
    else:
        return distribute_and_over_or(conjuncts[0], distribute_and_over_or_recursive(*conjuncts[1:]))


def testCustomTestCase():
    # Variablen definieren
    g_0_0_b1, g_0_0_b2, g_0_0_b3, g_0_0_b4, g_1_0_b1, g_1_0_b2, g_1_0_b3, g_1_0_b4, g_2_0_b1, g_2_0_b2, g_2_0_b3, g_2_0_b4, g_0_1_b1, g_0_1_b2, g_0_1_b3, g_0_1_b4, g_1_1_b1, g_1_1_b2, g_1_1_b3, g_1_1_b4, g_2_1_b1, g_2_1_b2, g_2_1_b3, g_2_1_b4, g_0_2_b1, g_0_2_b2, g_0_2_b3, g_0_2_b4, g_1_2_b1, g_1_2_b2, g_1_2_b3, g_1_2_b4, g_2_2_b1, g_2_2_b2, g_2_2_b3, g_2_2_b4 = symbols("g_0_0_b1 g_0_0_b2 g_0_0_b3 g_0_0_b4 g_1_0_b1 g_1_0_b2 g_1_0_b3 g_1_0_b4 g_2_0_b1 g_2_0_b2 g_2_0_b3 g_2_0_b4 g_0_1_b1 g_0_1_b2 g_0_1_b3 g_0_1_b4 g_1_1_b1 g_1_1_b2 g_1_1_b3 g_1_1_b4 g_2_1_b1 g_2_1_b2 g_2_1_b3 g_2_1_b4 g_0_2_b1 g_0_2_b2 g_0_2_b3 g_0_2_b4 g_1_2_b1 g_1_2_b2 g_1_2_b3 g_1_2_b4 g_2_2_b1 g_2_2_b2 g_2_2_b3 g_2_2_b4")

    input_formula = Or(
        And(~g_0_0_b1, ~g_0_0_b2, ~g_0_0_b3, ~g_0_0_b4),
        And(~g_1_0_b1, ~g_1_0_b2, ~g_1_0_b3, ~g_1_0_b4),
        And(~g_2_0_b1, ~g_2_0_b2, ~g_2_0_b3, ~g_2_0_b4),
        And(~g_0_1_b1, ~g_0_1_b2, ~g_0_1_b3, ~g_0_1_b4),
        And(~g_1_1_b1, ~g_1_1_b2, ~g_1_1_b3, ~g_1_1_b4),
        And(~g_2_1_b1, ~g_2_1_b2, ~g_2_1_b3, ~g_2_1_b4),
        And(~g_0_2_b1, ~g_0_2_b2, ~g_0_2_b3, ~g_0_2_b4),
        And(~g_1_2_b1, ~g_1_2_b2, ~g_1_2_b3, ~g_1_2_b4),
        And(~g_2_2_b1, ~g_2_2_b2, ~g_2_2_b3, ~g_2_2_b4),
    )
    cnf_formula = to_cnf_custom(input_formula)
    print(cnf_formula)

    g = {}
    for i in range(3):
        for j in range(3):
            for k in range(1, 5):
                g[i, j, k] = symbols("g_{}_{}_b{}".format(i, j, k))

    input_formula = Or(
        And(~g[0, 0, 1], ~g[0, 0, 2], ~g[0, 0, 3], ~g[0, 0, 4]),
        And(~g[1, 0, 1], ~g[1, 0, 2], ~g[1, 0, 3], ~g[1, 0, 4]),
        And(~g[2, 0, 1], ~g[2, 0, 2], ~g[2, 0, 3], ~g[2, 0, 4]),
        And(~g[0, 1, 1], ~g[0, 1, 2], ~g[0, 1, 3], ~g[0, 1, 4]),
        And(~g[1, 1, 1], ~g[1, 1, 2], ~g[1, 1, 3], ~g[1, 1, 4]),
        And(~g[2, 1, 1], ~g[2, 1, 2], ~g[2, 1, 3], ~g[2, 1, 4]),
        And(~g[0, 2, 1], ~g[0, 2, 2], ~g[0, 2, 3], ~g[0, 2, 4]),
        And(~g[1, 2, 1], ~g[1, 2, 2], ~g[1, 2, 3], ~g[1, 2, 4]),
        And(~g[2, 2, 1], ~g[2, 2, 2], ~g[2, 2, 3], ~g[2, 2, 4]),
    )
    tseitin_formula = tseitin_transformation(input_formula)
    print(tseitin_formula)

def test_TseitinTransformation():
    # Definieren Sie Variablen
    A = Var("A")
    B = Var("B")
    C = Var("C")

    # Definieren Sie eine Formel (z.B. (A ∧ B) → C)
    formula = (A & B) >> C

    # Definieren Sie eine Formel (z.B. (A ∧ B) → C)
    # Die Funktion `Implies` wird hier durch eine äquivalente Form (~A ∨ ~B ∨ C) ersetzt.
    #formula = (~A | ~B | C)
    #formula = nnf.And(A, B)

    # Die Formel ist bereits in CNF, daher ist keine Konvertierung erforderlich.
    cnf_formula = formula.to_CNF()

    # Verwenden Sie den And-Operator (z.B. (A ∧ B))
    and_formula = A & B

    # Definieren Sie eine Formel (z.B. (A ∧ B) → C)
    # Die Funktion `Implies` wird hier durch eine äquivalente Form (~A ∨ ~B ∨ C) ersetzt.
    formula = (A.negate() | B.negate()) | C

    # Die Formel ist bereits in CNF, daher ist keine Konvertierung erforderlich.
    cnf_formula = formula

    # Drucken Sie die ursprüngliche Formel und die CNF-Version
    print("Original Formula:", formula)
    print("CNF Formula:", cnf_formula)

    # Drucken Sie die ursprüngliche Formel und die CNF-Version
    print("Original Formula:", formula)
    print("CNF Formula:", cnf_formula)