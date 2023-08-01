from nnf import Var
from nnf.operators import And, Or, implies
import nnf as nnfs
import nnf.tseitin as ts
import sympy as sp
def test_nnf_Equivalent():
    formula1 = sp.Equivalent(sp.symbols("A"), sp.symbols("B"))
    formula1 = ~sp.And(~sp.symbols("A"), ~sp.symbols("B"))
    formula2 = sp.to_cnf(formula1)
    print(formula2)

    equivalent = 'implies(Var("A"), Var("B")) & implies(Var("B"), Var("A"))'
    result = '(~((Var("A") | Var("b"))))'
    equivalent = eval(equivalent)
    result = equivalent.to_CNF()

    result = '((((~Var("g_0_0_b1")) & (~Var("g_0_0_b2"))) | ~((~Var("g_0_1_b1")) & (~Var("g_0_1_b2")))) & (((~Var("g_0_1_b1")) & (~Var("g_0_1_b2"))) | ~((~Var("g_0_0_b1")) & (~Var("g_0_0_b2")))))'
    result = '(((~Var("A1") & ~Var("A2")) | ~(~Var("B1") & ~Var("B2"))) & ((~Var("B1") & ~Var("B2")) | ~(~Var("A1") & ~Var("A2"))))'

    eval(result)
    result = result.to_CNF()
    print(result)

def test_compare_2_expressions():
    exp1 = "(A | ~B) & (A | ~C) & (B | ~A) & (B | ~D) & (~A | ~C) & (~D | ~B) & (~D | ~C)"
    exp2 = "(A | D | ~B) & (A | D | ~C) & (B | C | ~A) & (B | C | ~D)"
