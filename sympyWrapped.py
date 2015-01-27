from sympy import poly,pprint
from sympy.abc import x,y
from puiseuxPoly import puiseux
from mypoly import mypoly
from expandParallel import solutionList
from fractions import Fraction as fr
import sys
"""
A convenience class that uses Sympy to allow easier command line input.
Asks user for a polynomial and for the number of desired terms. Poly can
be input as, for example, (x^3-y)*(2x+4). Sympy takes care of the simplification and the script transforms it into a mypoly object and calls the solutionList function.
"""
s = raw_input("Enter a polynomial in x and y --> ") 
n = input("Enter the number of desired terms --> ")
s = s.replace('^','**')
p = poly(eval(s),x,y,domain='CC')
"""
d = {item[0][1]:puiseux({item[0][0]:complex(item[1])}) for item in p.terms()}
for item in p.terms():
    if item[0][1] in d.keys():
        d[item[0][1]]+=puiseux({item[0][0]:complex(item[1])})
    else: d[item[0][1]] = puiseux({item[0][0]:complex(item[1])})
m = mypoly(d)
"""
d = {item[0][1]:0 for item in p.terms()}
for item in p.terms():
    d[item[0][1]]+=puiseux({item[0][0]:complex(item[1])})
m = mypoly(d)
print m
for sol in solutionList(m,n,True):
    print
    print sol.LT()
    print sol
