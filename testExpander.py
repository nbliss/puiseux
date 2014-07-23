from puiseuxPoly import puiseux
from mypoly import mypoly
from expandParallel import solutionList
from puiseuxExpansion import solutionList as SL2
from fractions import Fraction as fr
from numpy.random import random,randint,choice

class tester(object):
    """
    Class to allow testing
    """
    def __init__(self,toTest,ydeg,xdeg,fracExps=False):
        """
        :py:data:`ydeg`
        """
        self.ydeg = ydeg
        self.xdeg = xdeg
        self.fracExps = fracExps
        self.toTest = toTest
        self.monomials = []
        for i in xrange(ydeg+1):
            for j in xrange(xdeg+1):
                self.monomials.append((i,j))

    def reset(self,ydeg,xdeg,fracExps=False):
        self.__init__(toTest,ydeg,xdeg,fracExps)

    def testIncreasingExps(self,trials,numterms=6):
        for i in xrange(trials):
            p = self.genRandom()
            try:
                sols = self.toTest(p,numterms,True)
            except Exception:
                print p
            for sol in sols:
                expList = [p(sol.trunc(j)).order() for j in xrange(1,numterms)]
                for k in xrange(len(expList)-1):
                    if not expList[k]<expList[k+1]:
                        print expList
                        print p(sol)

    def genRandom(self):
        """
        Generates a random polynomial whose y-degree is <= ``self.ydeg``
        and x-degree <= ``self.xdeg``.
        """
        poly = {}
        size = randint(2,len(self.monomials))
        support = choice(len(self.monomials),size,replace=False)
        support = [self.monomials[i] for i in support]
        for mon in support:
            if mon[0] not in poly:
                poly[mon[0]] = puiseux({mon[1]:complex(random(),random())})
            else:
                poly[mon[0]] += puiseux({mon[1]:complex(random(),random())})
        return mypoly(poly)

    def testAll(self):
        pass

if __name__=='__main__':
    a = tester(solutionList,4,4)
    #a = tester(SL2,4,4)
    a.testIncreasingExps(10,numterms=4)


