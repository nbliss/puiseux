from convexHull import lowerHull,ploty
from convexHull import slope as slp
from fractions import Fraction
from puiseuxPoly import puiseux
from mypoly import mypoly
from multiprocessing import Process, Queue
import numpy as np

def initialTerms(poly,positivesOnly=False):
    """
    Return a list of (*gamma,c)* pairs giving the
    first terms of each Puiseux solution of :py:data:`poly`.
    """
    hull = lowerHull(poly.support())
    if len(hull)==1:
        return []
    slopes = []
    for i in xrange(len(hull)-1):
        slopes.append(slp(hull[i],hull[i+1])) 
    slope_vertices = {} # dictionary with slope:[list of vertices on that edge]
    for slope in slopes:
        slope_vertices[slope] = []
    slope_vertices[slopes[0]].append(hull[0][0])
    oldSlope = slopes[0]
    for i in xrange(1,len(hull)):
        slope_vertices[oldSlope].append(hull[i][0])
        if (i<len(hull)-1) and slopes[i]!=oldSlope:
            oldSlope = slopes[i]
            slope_vertices[oldSlope].append(hull[i][0])
    slope_roots = {}
    for slope in slope_vertices.keys():
        if positivesOnly and slope>=0: continue
        deg = max(slope_vertices[slope])
        toAdd = []
        for i in xrange(deg+1):
            toAdd.append(0)
        slope_roots[slope] = toAdd
        for i in slope_vertices[slope]:
            slope_roots[slope][i] = poly.internal[i].LC()
        slope_roots[slope].reverse()
    for key in slope_roots.keys():
        while slope_roots[key][-1]==0: #don't care about coeffs that are 0
            slope_roots[key].pop()
        toAdd = []
        for x in np.roots(slope_roots[key]):
            toAdd.append(complex(x))
        slope_roots[key] = toAdd
    toReturn = []
    for slope in slope_roots.keys():
        for coeff in slope_roots[slope]:
            toReturn.append((-slope,coeff))
    ############################
    # Removing duplicates
    toReturn2 = []
    for item in toReturn:
        if item not in toReturn2:
            toReturn2.append(item)
    ############################
    return toReturn2


def firstTerms(poly):
    """
    Using :py:func:`initialTerms`, returns a list of the first
    terms of the puiseux solotions of :py:data:`poly` as :py:class:`puiseuxPoly.puiseux` objects.
    """
    toReturn = []
    for (gamma,c) in initialTerms(poly):
        toReturn.append(puiseux({gamma:c})) 
    return toReturn


def solutionList(poly,nterms,asPuiseuxObject=False):
    """
    Calls :py:func:`recurse` in parallel to compute a list
    of the first :py:data:`nterms` puiseux series solutions of
    :py:data:`poly`. If :py:data:`asPuiseuxObject` is false, they are
    returned as lists of *(gamma,c)* pairs; otherwise they are returned
    as :py:class:`puiseuxPoly.puiseux` objects.
    """
    if poly.degree()==0:return []
    toReturn = []
    lowest = poly.lowestDegree()
    if lowest>0:
        toReturn+=[[(0,0)] for i in xrange(lowest)]
    poly = poly.reduced()
    if poly.degree()==0:
        if asPuiseuxObject:return puiseuxify(toReturn)
        else: return toReturn

    q = Queue()
    inTerms = initialTerms(poly)
    procList = [] ######
    for firstTerm in inTerms[1:]:
        p = Process(target=recurse,args=(poly,firstTerm,[firstTerm],q,nterms-1)) ######
        procList.append(p) ######
        p.start() ######
    recurse(poly,inTerms[0],[inTerms[0]],q,nterms-1)
    for p in procList:
        p.join() ######
    q.put(0)
    toAdd = q.get()
    while toAdd !=0:
        toReturn.append(toAdd) ######
        toAdd = q.get()
    if len(toReturn)!=poly.degree()+lowest:
        print "Uh-oh. Polynomial is degree ",poly.degree()," but we've found ",len(toReturn)," solutions"
    
    # return as a list of puiseux objects instead of a list of term tuples
    if asPuiseuxObject:return puiseuxify(toReturn)
    else: return toReturn

def puiseuxify(listy):
    """
    Takes a list of lists of (*c,gamma*) tuples and turns
    it into the corresponding list of puiseux polynomials.
    """
    newRet = []
    for item in listy:
        pu = {}
        for pair in item:
            pu[pair[0]]=pair[1]
        newRet.append(puiseux(pu))
    return newRet 

def recurse(poly,currentMonomial,currentList,q,depth):
    """
    bigList will contain lists of terms for each solution (list of lists).
    currentList is the one we're currently computing.
    Working with lists instead of Puiseux objects for speed and ease of access
    Assumes currentMonomial is already in the list, and adds the new ones found.
    """
    if depth<1 or currentMonomial==(0,0):
        q.put(currentList) ######
        return
    toPlug = mypoly({1:puiseux({currentMonomial[0]:1}),0:puiseux({currentMonomial[0]:currentMonomial[1]})})
    nextPoly = poly(toPlug)
    nextTerms = initialTerms(nextPoly,positivesOnly=True)
    if nextTerms==[]:
        q.put(currentList) ######
        return
    procList = []
    for term in nextTerms[1:]:
        revisedList = []
        for a in currentList:
            revisedList.append(a)
        revisedList.append((term[0]+currentList[-1][0],term[1]))
        p = Process(target=recurse,args=(nextPoly,term,revisedList,q,depth-1)) ######
        procList.append(p) ######
        p.start() ######
    revisedList = []
    for a in currentList:
        revisedList.append(a)
    nt = nextTerms[0]
    revisedList.append((nt[0]+currentList[-1][0],nt[1]))
    recurse(nextPoly,nt,revisedList,q,depth-1)
    for p in procList:
        p.join() ######


if __name__=='__main__':
    import sys
    """
    try: n = int(sys.argv[1])
    except Exception: n = 0
    """
    try: s = sys.argv[1]
    except Exception: s = 'circle'
    try: numterms = int(sys.argv[2])
    except Exception: numterms = 4
    optList = {'other':mypoly({0:puiseux({1:1}),1:puiseux({0:2}),2:puiseux({1:1})}),\
               'arxiv':mypoly({0:puiseux({4:2}),1:puiseux({2:1}),2:puiseux({1:4}),3:puiseux({0:4})}),\
               'walker':mypoly({0:puiseux({Fraction(5):1}), 1:puiseux({Fraction(7,2):1}), 2:puiseux({Fraction(1):1}), 3:puiseux({Fraction(-1):1}), 5:puiseux({Fraction(-1,2):1}), 6:puiseux([[1,[1,2]]]), 7:puiseux([[1,[10,3]]]), 8:puiseux([[1,[5,2]]])}),\
               'terminates':mypoly({0:puiseux({1:1}),1:puiseux({2:2})}),\
               'seminar':mypoly({2:puiseux({0:1}),1:puiseux({1:2,2:2}),0:puiseux({0:-1})}),\
               'circle':mypoly({0:puiseux({0:-1,2:1}),2:puiseux({0:1})}),\
               'squares':mypoly({0:puiseux({2:1}),2:puiseux({0:1})}),\
               'ellipticNonsmooth':mypoly({2:puiseux({0:-1}),0:puiseux({3:1,1:-27,0:2*27})}),\
               'test':mypoly({0:puiseux({1:1}),1:puiseux({2:4,0:2}),3:puiseux({1:2}),5:puiseux({2:-1})}),\
                'homotopy1':mypoly({2:puiseux({0:1}),1:puiseux({1:3}),0:puiseux({0:-1,1:-3})}),\
               'ellipticSmooth':mypoly({2:puiseux({0:-1}),0:puiseux({3:1,1:1,0:1})})}
    if s not in optList.keys() or s=='help':
        toPrint = '\n'+s+' is not a valid option. Please choose from: \n'
        toPrint += str(optList.keys())
        raise Exception(toPrint)
    p = optList[s]
    print p
    print "\n\n"
    #print solutionList(p,numterms)
    for item in solutionList(p,numterms):
        print '---->----'
        pu = {}
        for itemy in item:
            pu[itemy[0]]=itemy[1]
        sol = puiseux(pu)
        print 'Solution: ',sol
        print p(sol)
        print 'First term of p(solution): ',p(sol).LT()
        print '----<----'


