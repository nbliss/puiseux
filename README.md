Summary of files and uses:

convexHull.py:
Has a function that computes the lower hull of a set of points in two dimensions. Also has a (very simple) function that computes the slope between two points, returning a fraction; and another function that takes a set of points, applies the lower hull function, and plots the result.

puiseuxPoly.py:
Defines a class of polynomials with (possibly negative) fractional exponents. Besides overriding operators to make for easier manipulation, it includes methods LT, LC, order, and commonDenom. LT returns the term with the lowest exponent (as another puiseux object). LC returns the coefficient of the leading term. Order returns the lowest exponent. commonDenom returns the least common multiple of the denominators of the exponents.

mypoly.py
Defines a class of univariate polynomials that can have coefficients that are 'puiseuxPoly' objects. Aside from overriding operators, it includes methods evaluate and support. Evaluate can be applied to any reasonable object--Python numeric types, puiseuxPoly's, or other mypoly's. If applied to a mypoly, returns a mypoly; if applied to a puiseuxPoly, returns a puiseuxPoly; otherwise, returns something based on the coefficients. 'support' returns the support of the polynomial, which is only interesting if the coefficients are puiseuxPolys. In that case it returns a list of one pair for each monomial in the polynomial,  where the first element is the degree of the monomial and the second is the exponent of the leading term of the coefficient puiseuxPoly.

newtonPuiseux.py
Has two methods, initialTerms and expand. InitialTerms takes a mypoly p and returns a list of the first terms of the puiseux expansions of solutions of p. Expand finds the next n terms of an expansion given a polynomial and the first term of the solution. Both methods return puiseuxPolys or lists thereof.
