import logging
from functools import partial

from nnf import Var
from nnf.operators import And, Or
import nnf as nnfs
import nnf.tseitin as ts
import sympy as sp
import src._clauselCalculator as clauselC
import src._timeCalculator as timeC
import src._clauselCalculator_NNF as ccNNF

def test_nnf_Or_And():

    A = Var("A")
    B = Var("B")
    C = Var("C")
    D = Var("D")

    formula1 = (A & B) | (C & D)
    formula2 = Or({And({A, B}), And({C, D})})
    formula3 = ts.to_CNF(formula1)
    formula4 = formula1.to_CNF()

    print(formula1)
    print(formula2)
    print(formula3)
    print(formula4)

def test_nnf_And_Or_Not():
    A = Var("A")
    B = Var("B")
    C = Var("C")
    D = Var("D")

    formula2 = (~A & ~B) | (C & D)
    formula2 = Or({And({~A, B}), And({C, D})})
    print(formula2)

def test_nnf_Tseitin2():
    g_0_0_b1 = Var("g_0_0_b1")
    g_0_0_b2 = Var("g_0_0_b2")
    g_0_0_b3 = Var("g_0_0_b3")
    g_0_0_b4 = Var("g_0_0_b4")
    g_1_0_b1 = Var("g_1_0_b1")
    g_1_0_b2 = Var("g_1_0_b2")
    g_1_0_b3 = Var("g_1_0_b3")
    g_1_0_b4 = Var("g_1_0_b4")
    g_2_0_b1 = Var("g_2_0_b1")
    g_2_0_b2 = Var("g_2_0_b2")
    g_2_0_b3 = Var("g_2_0_b3")
    g_2_0_b4 = Var("g_2_0_b4")
    g_0_1_b1 = Var("g_0_1_b1")
    g_0_1_b2 = Var("g_0_1_b2")
    g_0_1_b3 = Var("g_0_1_b3")
    g_0_1_b4 = Var("g_0_1_b4")
    g_1_1_b1 = Var("g_1_1_b1")
    g_1_1_b2 = Var("g_1_1_b2")
    g_1_1_b3 = Var("g_1_1_b3")
    g_1_1_b4 = Var("g_1_1_b4")
    g_2_1_b1 = Var("g_2_1_b1")
    g_2_1_b2 = Var("g_2_1_b2")
    g_2_1_b3 = Var("g_2_1_b3")
    g_2_1_b4 = Var("g_2_1_b4")
    g_0_2_b1 = Var("g_0_2_b1")
    g_0_2_b2 = Var("g_0_2_b2")
    g_0_2_b3 = Var("g_0_2_b3")
    g_0_2_b4 = Var("g_0_2_b4")
    g_1_2_b1 = Var("g_1_2_b1")
    g_1_2_b2 = Var("g_1_2_b2")
    g_1_2_b3 = Var("g_1_2_b3")
    g_1_2_b4 = Var("g_1_2_b4")
    g_2_2_b1 = Var("g_2_2_b1")
    g_2_2_b2 = Var("g_2_2_b2")
    g_2_2_b3 = Var("g_2_2_b3")
    g_2_2_b4 = Var("g_2_2_b4")

    formula1 = (g_0_0_b1.negate()) & (g_0_0_b2.negate()) & (g_0_0_b3.negate()) & (g_0_0_b4.negate()) | \
               (g_1_0_b1.negate()) & (g_1_0_b2.negate()) & (g_1_0_b3.negate()) & (g_1_0_b4.negate()) | \
               (g_2_0_b1.negate()) & (g_2_0_b2.negate()) & (g_2_0_b3.negate()) & (g_2_0_b4.negate()) | \
               (g_0_1_b1.negate()) & (g_0_1_b2.negate()) & (g_0_1_b3.negate()) & (g_0_1_b4.negate()) | \
               (g_1_1_b1.negate()) & (g_1_1_b2.negate()) & (g_1_1_b3.negate()) & (g_1_1_b4.negate()) | \
               (g_2_1_b1.negate()) & (g_2_1_b2.negate()) & (g_2_1_b3.negate()) & (g_2_1_b4.negate()) | \
               (g_0_2_b1.negate()) & (g_0_2_b2.negate()) & (g_0_2_b3.negate()) & (g_0_2_b4.negate()) | \
               (g_1_2_b1.negate()) & (g_1_2_b2.negate()) & (g_1_2_b3.negate()) & (g_1_2_b4.negate()) | \
               (g_2_2_b1.negate()) & (g_2_2_b2.negate()) & (g_2_2_b3.negate()) & (g_2_2_b4.negate())

    formula2 = (~Var("g_0_0_b1")) & (~Var("g_0_0_b1")) & (~Var("g_0_0_b3")) & (~Var("g_0_0_b4")) | (~Var("g_1_0_b1")) & (~Var("g_1_0_b2")) & (~Var("g_1_0_b3")) & (~Var("g_1_0_b4")) | (~Var("g_2_0_b1")) & (~Var("g_2_0_b2")) & (~Var("g_2_0_b3")) & (~Var("g_2_0_b4")) | (~Var("g_0_1_b1")) & (~Var("g_0_1_b2")) & (~Var("g_0_1_b3")) & (~Var("g_0_1_b4")) | (~Var("g_1_1_b1")) & (~Var("g_1_1_b2")) & (~Var("g_1_1_b3")) & (~Var("g_1_1_b4")) | (~Var("g_2_1_b1")) & (~Var("g_2_1_b2")) & (~Var("g_2_1_b3")) & (~Var("g_2_1_b4")) | (~Var("g_0_2_b1")) & (~Var("g_0_2_b2")) & (~Var("g_0_2_b3")) & (~Var("g_0_2_b4")) | (~Var("g_1_2_b1")) & (~Var("g_1_2_b2")) & (~Var("g_1_2_b3")) & (~Var("g_1_2_b4")) | (~Var("g_2_2_b1")) & (~Var("g_2_2_b2")) & (~Var("g_2_2_b3")) & (~Var("g_2_2_b4"))

    nnf = ccNNF._ccNNF()

    formula3_str = nnf.transform_input('(~g_0_0_b1) & (g_0_0_b2) & (~g_0_0_b3) & (g_0_0_b4) | (~g_1_0_b1) & (~g_1_0_b2) & (~g_1_0_b3) & (~g_1_0_b4) | (~g_2_0_b1) & (~g_2_0_b2) & (g_2_0_b3) & (~g_2_0_b4) | (~g_0_1_b1) & (~g_0_1_b2) & (~g_0_1_b3) & (~g_0_1_b4) | (~g_1_1_b1) & (~g_1_1_b2) & (~g_1_1_b3) & (~g_1_1_b4) | (~g_2_1_b1) & (~g_2_1_b2) & (~g_2_1_b3) & (g_2_1_b4) | (~g_0_2_b1) & (~g_0_2_b2) & (~g_0_2_b3) & (~g_0_2_b4) | (~g_1_2_b1) & (~g_1_2_b2) & (g_1_2_b3) & (~g_1_2_b4) | (~g_2_2_b1) & (~g_2_2_b2) & (~g_2_2_b3) & (g_2_2_b4)')
    formula3 = nnf.execute_transformed_code(formula3_str)

    time_calculator = timeC.TimeCalculator()
    time_calculator.start_with_task_name("CNF NNF")

    nnf2 = ccNNF._ccNNF()
    input = '(~g_0_0_b1) & (g_0_0_b2) & (~g_0_0_b3) & (g_0_0_b4) | (~g_1_0_b1) & (~g_1_0_b2) & (~g_1_0_b3) & (~g_1_0_b4) | (~g_2_0_b1) & (~g_2_0_b2) & (g_2_0_b3) & (~g_2_0_b4) | (~g_0_1_b1) & (~g_0_1_b2) & (~g_0_1_b3) & (~g_0_1_b4) | (~g_1_1_b1) & (~g_1_1_b2) & (~g_1_1_b3) & (~g_1_1_b4) | (~g_2_1_b1) & (~g_2_1_b2) & (~g_2_1_b3) & (g_2_1_b4) | (~g_0_2_b1) & (~g_0_2_b2) & (~g_0_2_b3) & (~g_0_2_b4) | (~g_1_2_b1) & (~g_1_2_b2) & (g_1_2_b3) & (~g_1_2_b4) | (~g_2_2_b1) & (~g_2_2_b2) & (~g_2_2_b3) & (g_2_2_b4)'

    # Verwende functools.partial, um die Methode und das Objekt an measure_and_run zu übergeben
    bound_method = partial(nnf2.process_formula, input)
    processed_output = time_calculator.measure_and_run(bound_method)
    print(processed_output)

    nnf3 = ccNNF._ccNNF()

    input = '(~g_0_0_b1) & (g_0_0_b2) & (~g_0_0_b3) & (g_0_0_b4) | (~g_1_0_b1) & (~g_1_0_b2) & (~g_1_0_b3) & (~g_1_0_b4) | (~g_2_0_b1) & (~g_2_0_b2) & (g_2_0_b3) & (~g_2_0_b4) | (~g_0_1_b1) & (~g_0_1_b2) & (~g_0_1_b3) & (~g_0_1_b4) | (~g_1_1_b1) & (~g_1_1_b2) & (~g_1_1_b3) & (~g_1_1_b4) | (~g_2_1_b1) & (~g_2_1_b2) & (~g_2_1_b3) & (g_2_1_b4) | (~g_0_2_b1) & (~g_0_2_b2) & (~g_0_2_b3) & (~g_0_2_b4) | (~g_1_2_b1) & (~g_1_2_b2) & (g_1_2_b3) & (~g_1_2_b4) | (~g_2_2_b1) & (~g_2_2_b2) & (~g_2_2_b3) & (g_2_2_b4)'

    # Verwende functools.partial, um die Methode und das Objekt an measure_and_run zu übergeben
    bound_method = partial(nnf3.process_formula, input)
    processed_output = time_calculator.measure_and_run(bound_method)
    print(processed_output)

    nnf4 = ccNNF._ccNNF()
    input = '(~g_0_0_b1) & (g_0_0_b2) & (~g_0_0_b3) & (g_0_0_b4) | (~g_1_0_b1) & (~g_1_0_b2) & (~g_1_0_b3) & (~g_1_0_b4) | (~g_2_0_b1) & (~g_2_0_b2) & (g_2_0_b3) & (~g_2_0_b4) | (~g_0_1_b1) & (~g_0_1_b2) & (~g_0_1_b3) & (~g_0_1_b4) | (~g_1_1_b1) & (~g_1_1_b2) & (~g_1_1_b3) & (~g_1_1_b4) | (~g_2_1_b1) & (~g_2_1_b2) & (~g_2_1_b3) & (g_2_1_b4) | (~g_0_2_b1) & (~g_0_2_b2) & (~g_0_2_b3) & (~g_0_2_b4) | (~g_1_2_b1) & (~g_1_2_b2) & (g_1_2_b3) & (~g_1_2_b4) | (~g_2_2_b1) & (~g_2_2_b2) & (~g_2_2_b3) & (g_2_2_b4)'

    # Verwende functools.partial, um die Methode und das Objekt an measure_and_run zu übergeben
    bound_method = partial(nnf4.process_formula, input)
    processed_output = time_calculator.measure_and_run(bound_method)
    print(processed_output)

    try:
        cnf_formula = formula1.to_CNF()
        cnf_formula = formula2.to_CNF()
        cnf_formula = formula3.to_CNF()
        processed_output = nnf.process_output(cnf_formula)

        processed_output = nnf2.process_formula('(~g_0_0_b1) & (g_0_0_b2) & (~g_0_0_b3) & (g_0_0_b4) | (~g_1_0_b1) & (~g_1_0_b2) & (~g_1_0_b3) & (~g_1_0_b4) | (~g_2_0_b1) & (~g_2_0_b2) & (g_2_0_b3) & (~g_2_0_b4) | (~g_0_1_b1) & (~g_0_1_b2) & (~g_0_1_b3) & (~g_0_1_b4) | (~g_1_1_b1) & (~g_1_1_b2) & (~g_1_1_b3) & (~g_1_1_b4) | (~g_2_1_b1) & (~g_2_1_b2) & (~g_2_1_b3) & (g_2_1_b4) | (~g_0_2_b1) & (~g_0_2_b2) & (~g_0_2_b3) & (~g_0_2_b4) | (~g_1_2_b1) & (~g_1_2_b2) & (g_1_2_b3) & (~g_1_2_b4) | (~g_2_2_b1) & (~g_2_2_b2) & (~g_2_2_b3) & (g_2_2_b4)')

    except TimeoutError:
        print("Timeout of " + str(time_calculator.max_time) + "s for \"" + str(
                time_calculator.task_name) + "\" reached, terminating code. No Solution found in that time")
    finally:
        time_calculator.stop()
        time_duration = time_calculator.get_duration()
        print(time_duration)
        logging.info(time_duration)

    print()
    print(processed_output)

    clauselCalculator = clauselC.ClauselCalculator("", "", "", "", "")
    test = [[['~g_0_0_b1', '~g_0_0_b2', '~g_0_0_b3'], ['~g_0_1_b1', '~g_0_1_b2', '~g_0_1_b3', '~g_0_1_b4']], [['~g_1_0_b1', '~g_1_0_b2', '~g_1_0_b3'], ['~g_1_1_b1', '~g_1_1_b2', '~g_1_1_b3', '~g_1_1_b4']], [['~g_2_0_b1', '~g_2_0_b2', '~g_2_0_b3'], ['~g_2_1_b1', '~g_2_1_b2', '~g_2_1_b3', '~g_2_1_b4']], [['~g_0_1_b1', '~g_0_1_b2', '~g_0_1_b3', 'g_0_1_b4'], ['~g_0_2_b1', '~g_0_2_b2', '~g_0_2_b3']], [['~g_1_1_b1', '~g_1_1_b2', '~g_1_1_b3', 'g_1_1_b4'], ['~g_1_2_b1', '~g_1_2_b2', '~g_1_2_b3']], [['~g_2_1_b1', '~g_2_1_b2', '~g_2_1_b3', 'g_2_1_b4'], ['~g_2_2_b1', '~g_2_2_b2', '~g_2_2_b3']]]
    #test1 = ['(~g_0_0_b1) & (~g_0_0_b2) & (~g_0_0_b3) & (~g_0_0_b4) | (~g_1_0_b1) & (~g_1_0_b2) & (~g_1_0_b3) & (~g_1_0_b4) | (~g_2_0_b1) & (~g_2_0_b2) & (~g_2_0_b3) & (~g_2_0_b4) | (~g_0_1_b1) & (~g_0_1_b2) & (~g_0_1_b3) & (~g_0_1_b4) | (~g_1_1_b1) & (~g_1_1_b2) & (~g_1_1_b3) & (~g_1_1_b4) | (~g_2_1_b1) & (~g_2_1_b2) & (~g_2_1_b3) & (~g_2_1_b4) | (~g_0_2_b1) & (~g_0_2_b2) & (~g_0_2_b3) & (~g_0_2_b4) | (~g_1_2_b1) & (~g_1_2_b2) & (~g_1_2_b3) & (~g_1_2_b4) | (~g_2_2_b1) & (~g_2_2_b2) & (~g_2_2_b3) & (~g_2_2_b4)', '(~g_0_0_b1) & (~g_0_0_b2) & (~g_0_0_b3) & (g_0_0_b4) | (~g_1_0_b1) & (~g_1_0_b2) & (~g_1_0_b3) & (g_1_0_b4) | (~g_2_0_b1) & (~g_2_0_b2) & (~g_2_0_b3) & (g_2_0_b4) | (~g_0_1_b1) & (~g_0_1_b2) & (~g_0_1_b3) & (g_0_1_b4) | (~g_1_1_b1) & (~g_1_1_b2) & (~g_1_1_b3) & (g_1_1_b4) | (~g_2_1_b1) & (~g_2_1_b2) & (~g_2_1_b3) & (g_2_1_b4) | (~g_0_2_b1) & (~g_0_2_b2) & (~g_0_2_b3) & (g_0_2_b4) | (~g_1_2_b1) & (~g_1_2_b2) & (~g_1_2_b3) & (g_1_2_b4) | (~g_2_2_b1) & (~g_2_2_b2) & (~g_2_2_b3) & (g_2_2_b4)', '(~g_0_0_b1) & (~g_0_0_b2) & (g_0_0_b3) & (~g_0_0_b4) | (~g_1_0_b1) & (~g_1_0_b2) & (g_1_0_b3) & (~g_1_0_b4) | (~g_2_0_b1) & (~g_2_0_b2) & (g_2_0_b3) & (~g_2_0_b4) | (~g_0_1_b1) & (~g_0_1_b2) & (g_0_1_b3) & (~g_0_1_b4) | (~g_1_1_b1) & (~g_1_1_b2) & (g_1_1_b3) & (~g_1_1_b4) | (~g_2_1_b1) & (~g_2_1_b2) & (g_2_1_b3) & (~g_2_1_b4) | (~g_0_2_b1) & (~g_0_2_b2) & (g_0_2_b3) & (~g_0_2_b4) | (~g_1_2_b1) & (~g_1_2_b2) & (g_1_2_b3) & (~g_1_2_b4) | (~g_2_2_b1) & (~g_2_2_b2) & (g_2_2_b3) & (~g_2_2_b4)', '(~g_0_0_b1) & (~g_0_0_b2) & (g_0_0_b3) & (g_0_0_b4) | (~g_1_0_b1) & (~g_1_0_b2) & (g_1_0_b3) & (g_1_0_b4) | (~g_2_0_b1) & (~g_2_0_b2) & (g_2_0_b3) & (g_2_0_b4) | (~g_0_1_b1) & (~g_0_1_b2) & (g_0_1_b3) & (g_0_1_b4) | (~g_1_1_b1) & (~g_1_1_b2) & (g_1_1_b3) & (g_1_1_b4) | (~g_2_1_b1) & (~g_2_1_b2) & (g_2_1_b3) & (g_2_1_b4) | (~g_0_2_b1) & (~g_0_2_b2) & (g_0_2_b3) & (g_0_2_b4) | (~g_1_2_b1) & (~g_1_2_b2) & (g_1_2_b3) & (g_1_2_b4) | (~g_2_2_b1) & (~g_2_2_b2) & (g_2_2_b3) & (g_2_2_b4)', '(~g_0_0_b1) & (g_0_0_b2) & (~g_0_0_b3) & (~g_0_0_b4) | (~g_1_0_b1) & (g_1_0_b2) & (~g_1_0_b3) & (~g_1_0_b4) | (~g_2_0_b1) & (g_2_0_b2) & (~g_2_0_b3) & (~g_2_0_b4) | (~g_0_1_b1) & (g_0_1_b2) & (~g_0_1_b3) & (~g_0_1_b4) | (~g_1_1_b1) & (g_1_1_b2) & (~g_1_1_b3) & (~g_1_1_b4) | (~g_2_1_b1) & (g_2_1_b2) & (~g_2_1_b3) & (~g_2_1_b4) | (~g_0_2_b1) & (g_0_2_b2) & (~g_0_2_b3) & (~g_0_2_b4) | (~g_1_2_b1) & (g_1_2_b2) & (~g_1_2_b3) & (~g_1_2_b4) | (~g_2_2_b1) & (g_2_2_b2) & (~g_2_2_b3) & (~g_2_2_b4)', '(~g_0_0_b1) & (g_0_0_b2) & (~g_0_0_b3) & (g_0_0_b4) | (~g_1_0_b1) & (g_1_0_b2) & (~g_1_0_b3) & (g_1_0_b4) | (~g_2_0_b1) & (g_2_0_b2) & (~g_2_0_b3) & (g_2_0_b4) | (~g_0_1_b1) & (g_0_1_b2) & (~g_0_1_b3) & (g_0_1_b4) | (~g_1_1_b1) & (g_1_1_b2) & (~g_1_1_b3) & (g_1_1_b4) | (~g_2_1_b1) & (g_2_1_b2) & (~g_2_1_b3) & (g_2_1_b4) | (~g_0_2_b1) & (g_0_2_b2) & (~g_0_2_b3) & (g_0_2_b4) | (~g_1_2_b1) & (g_1_2_b2) & (~g_1_2_b3) & (g_1_2_b4) | (~g_2_2_b1) & (g_2_2_b2) & (~g_2_2_b3) & (g_2_2_b4)', '(~g_0_0_b1) & (g_0_0_b2) & (g_0_0_b3) & (~g_0_0_b4) | (~g_1_0_b1) & (g_1_0_b2) & (g_1_0_b3) & (~g_1_0_b4) | (~g_2_0_b1) & (g_2_0_b2) & (g_2_0_b3) & (~g_2_0_b4) | (~g_0_1_b1) & (g_0_1_b2) & (g_0_1_b3) & (~g_0_1_b4) | (~g_1_1_b1) & (g_1_1_b2) & (g_1_1_b3) & (~g_1_1_b4) | (~g_2_1_b1) & (g_2_1_b2) & (g_2_1_b3) & (~g_2_1_b4) | (~g_0_2_b1) & (g_0_2_b2) & (g_0_2_b3) & (~g_0_2_b4) | (~g_1_2_b1) & (g_1_2_b2) & (g_1_2_b3) & (~g_1_2_b4) | (~g_2_2_b1) & (g_2_2_b2) & (g_2_2_b3) & (~g_2_2_b4)', '(~g_0_0_b1) & (g_0_0_b2) & (g_0_0_b3) & (g_0_0_b4) | (~g_1_0_b1) & (g_1_0_b2) & (g_1_0_b3) & (g_1_0_b4) | (~g_2_0_b1) & (g_2_0_b2) & (g_2_0_b3) & (g_2_0_b4) | (~g_0_1_b1) & (g_0_1_b2) & (g_0_1_b3) & (g_0_1_b4) | (~g_1_1_b1) & (g_1_1_b2) & (g_1_1_b3) & (g_1_1_b4) | (~g_2_1_b1) & (g_2_1_b2) & (g_2_1_b3) & (g_2_1_b4) | (~g_0_2_b1) & (g_0_2_b2) & (g_0_2_b3) & (g_0_2_b4) | (~g_1_2_b1) & (g_1_2_b2) & (g_1_2_b3) & (g_1_2_b4) | (~g_2_2_b1) & (g_2_2_b2) & (g_2_2_b3) & (g_2_2_b4)', '(g_0_0_b1) & (~g_0_0_b2) & (~g_0_0_b3) & (~g_0_0_b4) | (g_1_0_b1) & (~g_1_0_b2) & (~g_1_0_b3) & (~g_1_0_b4) | (g_2_0_b1) & (~g_2_0_b2) & (~g_2_0_b3) & (~g_2_0_b4) | (g_0_1_b1) & (~g_0_1_b2) & (~g_0_1_b3) & (~g_0_1_b4) | (g_1_1_b1) & (~g_1_1_b2) & (~g_1_1_b3) & (~g_1_1_b4) | (g_2_1_b1) & (~g_2_1_b2) & (~g_2_1_b3) & (~g_2_1_b4) | (g_0_2_b1) & (~g_0_2_b2) & (~g_0_2_b3) & (~g_0_2_b4) | (g_1_2_b1) & (~g_1_2_b2) & (~g_1_2_b3) & (~g_1_2_b4) | (g_2_2_b1) & (~g_2_2_b2) & (~g_2_2_b3) & (~g_2_2_b4)']

    time_calculator = timeC.TimeCalculator()
    time_calculator.start_with_task_name("CNF SymPy")

    try:
        clauselCalculator.generate_sympy_expression(test)

    except TimeoutError:
        print("Timeout of " + str(time_calculator.max_time) + "s reached, terminating code. No Solution found in that time")

    finally:
        time_calculator.stop()
        time_duration = time_calculator.get_duration()
        print(time_duration)
        logging.info(time_duration)

    print()
    print(formula1)
    print("cnf_formula")
    print(cnf_formula)

def test_compare_cnf_timings():
    clauselCalculator = clauselC.ClauselCalculator("", "", "", "", "")
    expression1 = ['(~g_0_0_b1) & (~g_0_0_b2) & (~g_0_0_b3) & (~g_0_0_b4) | (~g_1_0_b1) & (~g_1_0_b2) & (~g_1_0_b3) & (~g_1_0_b4) | (~g_2_0_b1) & (~g_2_0_b2) & (~g_2_0_b3) & (~g_2_0_b4) | (~g_0_1_b1) & (~g_0_1_b2) & (~g_0_1_b3) & (~g_0_1_b4) | (~g_1_1_b1) & (~g_1_1_b2) & (~g_1_1_b3) & (~g_1_1_b4) | (~g_2_1_b1) & (~g_2_1_b2) & (~g_2_1_b3) & (~g_2_1_b4) | (~g_0_2_b1) & (~g_0_2_b2) & (~g_0_2_b3) & (~g_0_2_b4) | (~g_1_2_b1) & (~g_1_2_b2) & (~g_1_2_b3) & (~g_1_2_b4) | (~g_2_2_b1) & (~g_2_2_b2) & (~g_2_2_b3) & (~g_2_2_b4)', '(~g_0_0_b1) & (~g_0_0_b2) & (~g_0_0_b3) & (g_0_0_b4) | (~g_1_0_b1) & (~g_1_0_b2) & (~g_1_0_b3) & (g_1_0_b4) | (~g_2_0_b1) & (~g_2_0_b2) & (~g_2_0_b3) & (g_2_0_b4) | (~g_0_1_b1) & (~g_0_1_b2) & (~g_0_1_b3) & (g_0_1_b4) | (~g_1_1_b1) & (~g_1_1_b2) & (~g_1_1_b3) & (g_1_1_b4) | (~g_2_1_b1) & (~g_2_1_b2) & (~g_2_1_b3) & (g_2_1_b4) | (~g_0_2_b1) & (~g_0_2_b2) & (~g_0_2_b3) & (g_0_2_b4) | (~g_1_2_b1) & (~g_1_2_b2) & (~g_1_2_b3) & (g_1_2_b4) | (~g_2_2_b1) & (~g_2_2_b2) & (~g_2_2_b3) & (g_2_2_b4)', '(~g_0_0_b1) & (~g_0_0_b2) & (g_0_0_b3) & (~g_0_0_b4) | (~g_1_0_b1) & (~g_1_0_b2) & (g_1_0_b3) & (~g_1_0_b4) | (~g_2_0_b1) & (~g_2_0_b2) & (g_2_0_b3) & (~g_2_0_b4) | (~g_0_1_b1) & (~g_0_1_b2) & (g_0_1_b3) & (~g_0_1_b4) | (~g_1_1_b1) & (~g_1_1_b2) & (g_1_1_b3) & (~g_1_1_b4) | (~g_2_1_b1) & (~g_2_1_b2) & (g_2_1_b3) & (~g_2_1_b4) | (~g_0_2_b1) & (~g_0_2_b2) & (g_0_2_b3) & (~g_0_2_b4) | (~g_1_2_b1) & (~g_1_2_b2) & (g_1_2_b3) & (~g_1_2_b4) | (~g_2_2_b1) & (~g_2_2_b2) & (g_2_2_b3) & (~g_2_2_b4)', '(~g_0_0_b1) & (~g_0_0_b2) & (g_0_0_b3) & (g_0_0_b4) | (~g_1_0_b1) & (~g_1_0_b2) & (g_1_0_b3) & (g_1_0_b4) | (~g_2_0_b1) & (~g_2_0_b2) & (g_2_0_b3) & (g_2_0_b4) | (~g_0_1_b1) & (~g_0_1_b2) & (g_0_1_b3) & (g_0_1_b4) | (~g_1_1_b1) & (~g_1_1_b2) & (g_1_1_b3) & (g_1_1_b4) | (~g_2_1_b1) & (~g_2_1_b2) & (g_2_1_b3) & (g_2_1_b4) | (~g_0_2_b1) & (~g_0_2_b2) & (g_0_2_b3) & (g_0_2_b4) | (~g_1_2_b1) & (~g_1_2_b2) & (g_1_2_b3) & (g_1_2_b4) | (~g_2_2_b1) & (~g_2_2_b2) & (g_2_2_b3) & (g_2_2_b4)', '(~g_0_0_b1) & (g_0_0_b2) & (~g_0_0_b3) & (~g_0_0_b4) | (~g_1_0_b1) & (g_1_0_b2) & (~g_1_0_b3) & (~g_1_0_b4) | (~g_2_0_b1) & (g_2_0_b2) & (~g_2_0_b3) & (~g_2_0_b4) | (~g_0_1_b1) & (g_0_1_b2) & (~g_0_1_b3) & (~g_0_1_b4) | (~g_1_1_b1) & (g_1_1_b2) & (~g_1_1_b3) & (~g_1_1_b4) | (~g_2_1_b1) & (g_2_1_b2) & (~g_2_1_b3) & (~g_2_1_b4) | (~g_0_2_b1) & (g_0_2_b2) & (~g_0_2_b3) & (~g_0_2_b4) | (~g_1_2_b1) & (g_1_2_b2) & (~g_1_2_b3) & (~g_1_2_b4) | (~g_2_2_b1) & (g_2_2_b2) & (~g_2_2_b3) & (~g_2_2_b4)', '(~g_0_0_b1) & (g_0_0_b2) & (~g_0_0_b3) & (g_0_0_b4) | (~g_1_0_b1) & (g_1_0_b2) & (~g_1_0_b3) & (g_1_0_b4) | (~g_2_0_b1) & (g_2_0_b2) & (~g_2_0_b3) & (g_2_0_b4) | (~g_0_1_b1) & (g_0_1_b2) & (~g_0_1_b3) & (g_0_1_b4) | (~g_1_1_b1) & (g_1_1_b2) & (~g_1_1_b3) & (g_1_1_b4) | (~g_2_1_b1) & (g_2_1_b2) & (~g_2_1_b3) & (g_2_1_b4) | (~g_0_2_b1) & (g_0_2_b2) & (~g_0_2_b3) & (g_0_2_b4) | (~g_1_2_b1) & (g_1_2_b2) & (~g_1_2_b3) & (g_1_2_b4) | (~g_2_2_b1) & (g_2_2_b2) & (~g_2_2_b3) & (g_2_2_b4)', '(~g_0_0_b1) & (g_0_0_b2) & (g_0_0_b3) & (~g_0_0_b4) | (~g_1_0_b1) & (g_1_0_b2) & (g_1_0_b3) & (~g_1_0_b4) | (~g_2_0_b1) & (g_2_0_b2) & (g_2_0_b3) & (~g_2_0_b4) | (~g_0_1_b1) & (g_0_1_b2) & (g_0_1_b3) & (~g_0_1_b4) | (~g_1_1_b1) & (g_1_1_b2) & (g_1_1_b3) & (~g_1_1_b4) | (~g_2_1_b1) & (g_2_1_b2) & (g_2_1_b3) & (~g_2_1_b4) | (~g_0_2_b1) & (g_0_2_b2) & (g_0_2_b3) & (~g_0_2_b4) | (~g_1_2_b1) & (g_1_2_b2) & (g_1_2_b3) & (~g_1_2_b4) | (~g_2_2_b1) & (g_2_2_b2) & (g_2_2_b3) & (~g_2_2_b4)', '(~g_0_0_b1) & (g_0_0_b2) & (g_0_0_b3) & (g_0_0_b4) | (~g_1_0_b1) & (g_1_0_b2) & (g_1_0_b3) & (g_1_0_b4) | (~g_2_0_b1) & (g_2_0_b2) & (g_2_0_b3) & (g_2_0_b4) | (~g_0_1_b1) & (g_0_1_b2) & (g_0_1_b3) & (g_0_1_b4) | (~g_1_1_b1) & (g_1_1_b2) & (g_1_1_b3) & (g_1_1_b4) | (~g_2_1_b1) & (g_2_1_b2) & (g_2_1_b3) & (g_2_1_b4) | (~g_0_2_b1) & (g_0_2_b2) & (g_0_2_b3) & (g_0_2_b4) | (~g_1_2_b1) & (g_1_2_b2) & (g_1_2_b3) & (g_1_2_b4) | (~g_2_2_b1) & (g_2_2_b2) & (g_2_2_b3) & (g_2_2_b4)', '(g_0_0_b1) & (~g_0_0_b2) & (~g_0_0_b3) & (~g_0_0_b4) | (g_1_0_b1) & (~g_1_0_b2) & (~g_1_0_b3) & (~g_1_0_b4) | (g_2_0_b1) & (~g_2_0_b2) & (~g_2_0_b3) & (~g_2_0_b4) | (g_0_1_b1) & (~g_0_1_b2) & (~g_0_1_b3) & (~g_0_1_b4) | (g_1_1_b1) & (~g_1_1_b2) & (~g_1_1_b3) & (~g_1_1_b4) | (g_2_1_b1) & (~g_2_1_b2) & (~g_2_1_b3) & (~g_2_1_b4) | (g_0_2_b1) & (~g_0_2_b2) & (~g_0_2_b3) & (~g_0_2_b4) | (g_1_2_b1) & (~g_1_2_b2) & (~g_1_2_b3) & (~g_1_2_b4) | (g_2_2_b1) & (~g_2_2_b2) & (~g_2_2_b3) & (~g_2_2_b4)']
    time_calculator = timeC.TimeCalculator()
    time_calculator.start_with_task_name("clauselCalculator.simplifyExpressions")

    result_Count = clauselCalculator.countSympyVariables(expression1)
    try:
        result = clauselCalculator.simplifyExpressions(expression1)
        print()

    except TimeoutError:
        print("Timeout of " + str(
            time_calculator.max_time) + "s reached, terminating code. No Solution found in that time")

    finally:
        time_calculator.stop()
        time_duration = time_calculator.get_duration()
        print()

        print(time_duration)
        #print(result)

    nnf = ccNNF._ccNNF()
    time_calculator.start_with_task_name("nnf.process_formula")

    try:
        for index in range(len(expression1)):
            processed_output = nnf.process_formula(expression1[index])

    except TimeoutError:
        print("Timeout of " + str(time_calculator.max_time) + "s for \"" + str(
            time_calculator.task_name) + "\" reached, terminating code. No Solution found in that time")
    finally:
        time_calculator.stop()
        time_duration = time_calculator.get_duration()
        print(time_duration)
        logging.info(time_duration)

    print()
    #print(processed_output)

def test_nnf_Equivalent():
    A = Var("A")
    B = Var("B")
    C = Var("C")
    D = Var("D")
    nnf = ccNNF._ccNNF()
    formula1 = sp.Equivalent(sp.symbols("A"), sp.symbols("B"))
    formula1 = ~sp.And(~sp.symbols("A"), ~sp.symbols("B"))
    formula2 = sp.to_cnf(formula1)

    result = '(~((Var("A") | Var("b"))))'
    eval(result)


    result = '((((~Var("g_0_0_b1")) & (~Var("g_0_0_b2"))) | ~((~Var("g_0_1_b1")) & (~Var("g_0_1_b2")))) & (((~Var("g_0_1_b1")) & (~Var("g_0_1_b2"))) | ~((~Var("g_0_0_b1")) & (~Var("g_0_0_b2")))))'
    result = '(((~Var("A1") & ~Var("A2")) | ~(~Var("B1") & ~Var("B2"))) & ((~Var("B1") & ~Var("B2")) | ~(~Var("A1") & ~Var("A2"))))'

    result = nnf.transformEquivalent('equivalent(((~Var("g_0_0_b1")) & (~Var("g_0_0_b2"))), ((~Var("g_0_1_b1")) & (~Var("g_0_1_b2"))))')
    eval(result)

    #eval('Equivalent(((~Var("g_0_0_b1")) & (~Var("g_0_0_b2"))), ((~Var("g_0_1_b1")) & (~Var("g_0_1_b2"))))')

    #eval('((And({~Var("g_0_0_b1"), ~Var("g_0_0_b2")})).implicates(And({~Var("g_0_1_b1"), ~Var("g_0_1_b2")})))')
    #eval('(((~Var("g_0_0_b1")) & (~Var("g_0_0_b2")))).implicates(((~Var("g_0_1_b1")) & (~Var("g_0_1_b2"))))')
    #eval('((((~Var("g_0_0_b1")) & (~Var("g_0_0_b2")))).implicates(((~Var("g_0_1_b1")) & (~Var("g_0_1_b2")))) & (((~Var("g_0_1_b1")) & (~Var("g_0_1_b2")))).implicates(((~Var("g_0_0_b1")) & (~Var("g_0_0_b2")))))')

    #formula3 = Equivalent(~A & ~B, C & D)
    #print(formula3)

def test_nnf_Implies():

    A = Var("A")
    B = Var("B")
    C = Var("C")
    D = Var("D")

    formula4 = Implies(~A & ~B, C & D)
    print(formula4)
