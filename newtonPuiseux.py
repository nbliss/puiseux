from convexHull import lowerHull,ploty
from convexHull import slope as slp
from fractions import Fraction
from puiseuxPoly import puiseux
from mypoly import mypoly
import numpy as np

currentPoly=None
solutions={}
# {first term:[#terms n,highest exponent,1st term + 2nd term + 3rd term + ... + nth term]}
def initialTerms(poly):
	"""
	Returns a list of the first terms of each of
	the Puiseux series solutions of poly, and initializes 
	'solutions' to {1st term of solution 1:[1,-exponent,firstTerm],
	1st term of solution 2:[1,-exponent,firstTerm], ...}
	"""
	global currentPoly
	global solutions
	if currentPoly==poly:
		return solutions.keys()
	solutions={}
	currentPoly = poly
	hull = lowerHull(poly.support())
	slopes = [slp(hull[i],hull[i+1]) for i in xrange(len(hull)-1)]
	slopeExps = {slope:[] for slope in slopes}
	slopeExps[slopes[0]].append(hull[0][0])
	oldSlope = slopes[0]
	for i in xrange(1,len(hull)):
		slopeExps[oldSlope].append(hull[i][0])
		if (i<len(hull)-1) and slopes[i]!=oldSlope:
			oldSlope = slopes[i]
			slopeExps[oldSlope].append(hull[i][0])
	slopePoly = {}
	for slope in slopeExps:
		deg = max(slopeExps[slope])
		slopePoly[slope] = [0 for i in xrange(deg+1)]
		for i in slopeExps[slope]:
			slopePoly[slope][i] = poly.internal[i].LC()
		slopePoly[slope].reverse()
	for key in slopePoly:
		slopePoly[key]=[complex(x) for x in np.roots(slopePoly[key])]
		while 0 in slopePoly[key]: slopePoly[key].remove(0)
		for coeff in slopePoly[key]:
			firstTerm = puiseux({-key:coeff}) # negative of slope
			solutions[firstTerm]=[1,-key,firstTerm]
	return solutions.keys()

def expand(poly,initialTerm,n=4,showPlot=False):
	"""
	Returns the first n terms (or more) of the Puiseux series
	solution of poly with first term initialTerm, and
	updates 'solutions' with the extra terms.
	"""
	global currentPoly
	global solutions
	if solutions!={} and currentPoly==poly:
		if initialTerm not in solutions:
			message = str(initialTerm)+' is not the first'\
			' term of a Puiseux solution of '+ str(poly)
			raise ValueError(message)
	else:
		if initialTerm not in initialTerms(poly):
			message = str(initialTerm)+' is not the first'\
			' term of a Puiseux solution of '+ str(poly)
			raise ValueError(message)
	# at this point either we've populated 'solutions' with the first terms,
	# or 'expand' or 'initialTerms' had been called before and populated it with
	# one or more terms
	numTerms = solutions[initialTerm][0]
	while numTerms < n:
		# plugging (y+terms) into poly
		nextPoly = poly.evaluate(mypoly({0:solutions[initialTerm][2],1:1}))
		hull = lowerHull(nextPoly.support())
		print '--------hull--------'
		print hull
		for i in xrange(len(hull)-1):print slp(hull[i],hull[i+1])
		print '--------hull--------'
		if showPlot: ploty(nextPoly.support())
		newCoeff = -poly.internal[hull[0][0]].LC()/poly.internal[hull[1][0]].LC()
		newExp = solutions[initialTerm][1]-slp(hull[0],hull[1])
		solutions[initialTerm][0]+=1
		solutions[initialTerm][1] = newExp
		solutions[initialTerm][2]+=puiseux({newExp:newCoeff})
		numTerms+=1
	return solutions[initialTerm][2]


if __name__=='__main__':
	p = mypoly({0:puiseux({Fraction(5):1}), 1:puiseux({Fraction(7,2):1}), 2:puiseux({Fraction(1):1}), 3:puiseux({Fraction(-1):1}), 5:puiseux({Fraction(-1,2):1}), 6:puiseux([[1,[1,2]]]), 7:puiseux([[1,[10,3]]]), 8:puiseux([[1,[5,2]]])})
	it = initialTerms(p)
	print it
	for term in it:
		print 'start-----------------'
		print p.evaluate(term)
		print 'end-----------------'
	print solutions
	print expand(p,it[-3],2)
