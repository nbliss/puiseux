from puiseuxPoly import puiseux
from mypoly import mypoly
from expandParallel import solutionList
from fractions import Fraction as fr
import cPickle
if __name__=='__main__':
    p = mypoly({0:puiseux({5:1}),1:puiseux({fr(7,2):1}),2:puiseux({1:1}),3:puiseux({-1:1}),5:puiseux({fr(-1,2):1}),6:puiseux({fr(1,2):1}),7:puiseux({fr(10,3):1}),8:puiseux({fr(5,2):1})})
    p = mypoly({0:puiseux({0:(0.602188930612+0.991723585529j)}),4:puiseux({3:0.991343060948+0.811367139699j})})
    p = cPickle.load(open("failurePoly.p","rb"))
    print p
    print
    n=7
    sols = solutionList(p,n,True)
    print sols[0]
    print
    print p(sols[0])
    for sol in sols:
        expList = [p(sol.trunc(j)).order() for j in xrange(1,len(sol.internal))]
        print [str(item) for item in expList]
