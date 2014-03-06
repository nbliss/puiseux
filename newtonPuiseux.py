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
		while slopePoly[key][-1]==0: #don't care about coeffs that are 0
			slopePoly[key].pop()
		slopePoly[key]=[complex(x) for x in np.roots(slopePoly[key])]
		#while 0 in slopePoly[key]: slopePoly[key].remove(0)
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
		notIn = True
		for term in solutions:
			if initialTerm == term:
				notIn=False
				break
		if notIn:
			message = str(initialTerm)+' is not the first'\
			' term of a Puiseux solution of '+ str(poly)
			raise ValueError(message)
	else:
		notIn = True
		for term in initialTerms(poly):
			if initialTerm == term:
				notIn=False
				break
		if notIn:
			message = str(initialTerm)+' is not the first'\
			' term of a Puiseux solution of '+ str(poly)
			raise ValueError(message)
	# at this point 'solutions' is populated with at least the first terms
	numTerms = solutions[initialTerm][0]
	if numTerms == -1: # placeholder for when the series is fully computed
		return solutions[initialTerms][2]
	while numTerms < n:
		# plugging (y+terms) into poly
		toPlug = solutions[initialTerm][2]
		#nextPoly = poly.evaluate(mypoly({0:toPlug,1:1}))
		nextPoly = poly.evaluate(mypoly({0:toPlug,1:toPlug.monicLT()}))
		hull = lowerHull(nextPoly.support())
		"""
		print '--------begin hull--------'
		print "Terms: ",toPlug
		print "p(terms): ",poly.evaluate(toPlug)
		print "lower hull: ",hull
		for i in xrange(len(hull)-1):print slp(hull[i],hull[i+1])
		print '--------end hull--------'
		"""
		if showPlot: ploty(nextPoly.support())
		slopes = [slp(hull[i],hull[i+1]) for i in xrange(len(hull)-1)] 
		if slopes[0]>=0:
			if poly(toPlug)!=0:
				print "Error!!! No negative slopes but poly doesn't vanish!!"
				print "p(stuff)==",poly(toPlug)
			solutions[initialTerm][0] = -1
			return solutions[initialTerm][2]
		if slopes[1]<0: print "Error!!! Multiple negative slope segments!!"
		newCoeff = -nextPoly.internal[hull[0][0]].LC()/nextPoly.internal[hull[1][0]].LC()
		newExp = solutions[initialTerm][1]-slp(hull[0],hull[1])
		solutions[initialTerm][0]+=1
		solutions[initialTerm][1] = newExp
		solutions[initialTerm][2]+=puiseux({newExp:newCoeff})
		numTerms+=1
	return solutions[initialTerm][2]


if __name__=='__main__':
	import sys
	try: n = int(sys.argv[1])
	except Exception: n = 0
	if n==0:
		p = mypoly({0:puiseux({Fraction(5):1}), 1:puiseux({Fraction(7,2):1}), 2:puiseux({Fraction(1):1}), 3:puiseux({Fraction(-1):1}), 5:puiseux({Fraction(-1,2):1}), 6:puiseux([[1,[1,2]]]), 7:puiseux([[1,[10,3]]]), 8:puiseux([[1,[5,2]]])})
		it = initialTerms(p)
		print it
		first = puiseux({Fraction(2):(0.232785615938+0.792551992515j)})
		#first = puiseux({Fraction(-1,4):1j})
		print p(first)
		nextPoly = p(mypoly({0:first,1:1}))
		print lowerHull(nextPoly.support())
		print
		print expand(p,first,10)
	elif n==1:
		p = mypoly({0:puiseux({4:2}),1:puiseux({2:1}),2:puiseux({1:4}),3:puiseux({0:4})})
		print p
		it = initialTerms(p)
		print it
		first = puiseux({2:-2})
		print expand(p,first,4,showPlot=False)
	elif n==2:
		p = mypoly({1:puiseux({3:2,5:1}),2:puiseux({2:-2,4:4}),3:puiseux({3:-5})})
		print p
		it = initialTerms(p)
		print it
		term = puiseux({-1:(-0.4+0j)})
		print expand(p,term,3,showPlot=False)




