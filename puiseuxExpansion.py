from convexHull import lowerHull,ploty
from convexHull import slope as slp
from fractions import Fraction
from puiseuxPoly import puiseux
from mypoly import mypoly
import numpy as np

def initialTerms(poly,positivesOnly=False):
    """
    Return a list of (gamma,c) pairs giving the
    first terms of each Puiseux solution of poly.
    """
    hull = lowerHull(poly.support())
    slopes = [slp(hull[i],hull[i+1]) for i in xrange(len(hull)-1)]
    # dictionary with slope:[list of vertices on that edge]
    slope_vertices = {slope:[] for slope in slopes}
    slope_vertices[slopes[0]].append(hull[0][0])
    oldSlope = slopes[0]
    for i in xrange(1,len(hull)):
        slope_vertices[oldSlope].append(hull[i][0])
        if (i<len(hull)-1) and slopes[i]!=oldSlope:
            oldSlope = slopes[i]
            slope_vertices[oldSlope].append(hull[i][0])
    slope_roots = {}
    for slope in slope_vertices:
        if positivesOnly and slope>=0: continue
        deg = max(slope_vertices[slope])
        slope_roots[slope] = [0 for i in xrange(deg+1)]
        for i in slope_vertices[slope]:
            slope_roots[slope][i] = poly.internal[i].LC()
        slope_roots[slope].reverse()
    for key in slope_roots:
        while slope_roots[key][-1]==0: #don't care about coeffs that are 0
            slope_roots[key].pop()
        slope_roots[key]=[complex(x) for x in np.roots(slope_roots[key])]
    toReturn = []
    for slope in slope_roots:
        for coeff in slope_roots[slope]:
            toReturn.append((-slope,coeff))
    #########################
    # Removing duplicates
    toReturn2 = []
    for item in toReturn:
        if item not in toReturn2:
            toReturn2.append(item)
    #########################
    return toReturn2


def firstTerms(poly):
    return [puiseux({gamma:c}) for (gamma,c) in initialTerms(poly)]


def solutionList(poly,nterms):
    if poly.degree()==0:return []
    toReturn = []
    it = initialTerms(poly)
    p = puiseux({it[0][0]:it[0][1]})
    for firstTerm in initialTerms(poly):
        recurse(poly,firstTerm,[firstTerm],toReturn,nterms)
    if len(toReturn)!=poly.degree():
        print "Uh-oh. Polynomial is degree ",poly.degree()," but we've found ",len(toReturn)," solutions"
    return toReturn

def recurse(poly,currentMonomial,currentList,bigList,depth):
    """
    bigList will contain lists of terms for each solution (list of lists).
    currentList is the one we're currently computing.
    Working with lists instead of Puiseux objects for speed and ease of access
    Assumes currentMonomial is already in the list, and adds the new ones found.
    """
    if depth==0:
        bigList.append(currentList)
        return
    toPlug = mypoly({1:puiseux({currentMonomial[0]:1}),0:puiseux({currentMonomial[0]:currentMonomial[1]})})
    nextPoly = poly(toPlug)
    if len(nextPoly.internal.keys())==1:
        bigList.append(currentList)
        return
    nextTerms = initialTerms(nextPoly,positivesOnly=True)
    if nextTerms==[]:
        bigList.append(currentList)
        return
    for term in nextTerms:
        revisedList = [a for a in currentList]
        revisedList.append((term[0]+currentList[-1][0],term[1]))
        recurse(nextPoly,term,revisedList,bigList,depth-1)



if __name__=='__main__':
    import sys
    try: n = int(sys.argv[1])
    except Exception: n = 0
    try: numterms = int(sys.argv[2])
    except Exception: numterms = 4
    if n==0: p = mypoly({0:puiseux({1:1}),1:puiseux({0:2}),2:puiseux({1:1})})
    elif n==1: p = mypoly({0:puiseux({4:2}),1:puiseux({2:1}),2:puiseux({1:4}),3:puiseux({0:4})})
    elif n==2: p = mypoly({0:puiseux({Fraction(5):1}), 1:puiseux({Fraction(7,2):1}), 2:puiseux({Fraction(1):1}), 3:puiseux({Fraction(-1):1}), 5:puiseux({Fraction(-1,2):1}), 6:puiseux([[1,[1,2]]]), 7:puiseux([[1,[10,3]]]), 8:puiseux([[1,[5,2]]])})
    elif n==3: p = mypoly({0:puiseux({1:1}),1:puiseux({2:2})})
    elif n==4:  p = mypoly({0:puiseux({0:-1,2:1}),2:puiseux({0:1})})
    else: p = mypoly({0:puiseux({2:1}),2:puiseux({0:1})})
    print p
    print "\n\n"
    for item in solutionList(p,numterms):
        print '---->----'
        sol = puiseux({itemy[0]:itemy[1] for itemy in item})
        print 'Solution: ',sol
        print 'First term of p(solution): ',p(sol).LT()
        print '----<----'

def solutionIterators(poly):
    """
    *** NOT IMPLEMENTED ***
    Returns a list of generators of the Puiseux roots of poly.
    So solutionIterators(poly)[i].next() can be called repeatedly
    to show the ith solution of poly.
    """
    raise NotImplementedError("solutionIterator isn't implemented (haven't \
        figured out a good way to deal with branching yet)")
    toReturn = []
    for root in initialTerms(poly):
        def rootGen():
            nextPoly = poly
            prevRoot = root
            lastExp = 0
            while True:
                yield puiseux({prevRoot[1]+lastExp:prevRoot[0]})
                nextPoly = nextPoly(mypoly({1:puiseux({prevRoot[1]:1}),0:puiseux({prevRoot[1]:prevRoot[0]})}))
 
