from puiseuxPoly import puiseux
from fractions import Fraction
class mypoly(object):
    """
    Represents a univariate polynomial with :py:class:`puiseuxPoly.puiseux`
    coefficients.
    """
    def __init__(self,poly,checkReduced=True):
        """
        2x^2-3x+1 would be input as [[2,2],[-3,1],[1,0]]
        and represented internally as {2:2,1:-3,0:1} i.e. the keys
        are the exponents and the values are the coefficients
        --OR-- can be input as a dictionary, in which case it will
        just be copied to internal

        Coefficients can be complex, int, long (if you really want to),
        or (in the most usefull case) puiseux polynomials (using the
        puiseuxPoly class).

        **Maybe not**: they might need to be Puiseux objects?

        checkReduced is a flag that determines if when setting
        up the internal representation we check for like terms.
        Be careful with it!!! If poly is a dict, checkReduced doesn't
        matter since it can't have repeated keys (exponents)
        """
        if type(poly)==dict:
            self.internal = poly
        elif checkReduced:
            self.internal = {poly[0][1]:poly[0][0]}
            for mon in poly[1:]:
                coeff = mon[0]
                exponent = mon[1]
                if exponent in self.internal:
                    self.internal[exponent] += coeff
                else: self.internal[exponent] = coeff
        else:
            self.internal = {}
            for elt in poly:
                self.internal[elt[1]]=elt[0]
        for key in self.internal.keys():
            if self.internal[key]==0:
                self.internal.pop(key)
        if self.internal=={}:self.internal = {0:0}

    def __eq__(self,other):
        if type(other)==mypoly:
            if self.internal.keys() != other.internal.keys(): return False
            equal = True
            for key in self.internal.keys():
                if self.internal[key]!=other.internal[key]:
                    equal = False
                    break
            return equal
        else:
            l = self.internal.keys()
            if len(l)==1 and l[0]==0:
                return self.internal[l]==other
            elif len(l)==0: return other==0
            return False

    def __add__(self,other):
        if type(other) in [puiseux,int,float,Fraction,long,complex]:
            mp = {}
            for key in self.internal.keys():
                mp[key] = self.internal[key]+other
            return mypoly(mp)
        elif type(other)==mypoly:
            toReturn = {}
            for key in self.internal.keys():
                if key in other.internal.keys():
                    toReturn[key]=self.internal[key]+other.internal[key]
                else:
                    toReturn[key]=self.internal[key]
            for key in other.internal.keys():
                if key not in toReturn:
                    toReturn[key]=other.internal[key]
            return mypoly(toReturn)
        else: raise TypeError("can't do that")

    def __sub__(self, other):
        if type(other) in [puiseux,int,float,Fraction,long,complex]:
            mp = {}
            for key in self.internal.keys():
                mp[key] = self.internal[key]-other
            return mypoly(mp)
        elif type(other)==mypoly:
            toReturn = {}
            for key in self.internal.keys():
                if key in other.internal.keys():
                    toReturn[key]=self.internal[key]-other.internal[key]
                else:
                    toReturn[key]=self.internal[key]
            for key in other.internal.keys():
                if key not in toReturn:
                    toReturn[key]=(-other.internal[key])
            return mypoly(toReturn)
        else: raise TypeError("can't do that")


    def __mul__(self, other):
        if type(other) in [puiseux,int,float,Fraction,long,complex]:
            mp = {}
            for key in self.internal.keys():
                mp[key] = self.internal[key]*other
            return mypoly(mp)
        elif type(other)==mypoly:
            toReturn = {}
            for key1 in other.internal.keys():
                for key2 in self.internal.keys():
                    coeff = other.internal[key1]*self.internal[key2]
                    exponent = key1 + key2
                    if exponent in toReturn:
                        toReturn[exponent] += coeff
                    else: toReturn[exponent]=coeff
            return mypoly(toReturn,checkReduced=False)
        else: 
            raise TypeError("can't do that")

    def __rmul__(self,other):return self*other
    def __radd__(self,other):return self+other
    def __rsub__(self,other):return (-self)+other

    def __pow__(self,other):
        if type(other)==int and other>=0:
            if other==0:
                return mypoly({0:puiseux({Fraction(0,1):1})})
            else:
                toReturn = mypoly({0:puiseux({Fraction(0,1):1})})
                for i in xrange(other):
                    toReturn = self*toReturn
                return toReturn
        elif type(other)==int:
            raise TypeError("don't have support for negative exponents")
        else: raise TypeError("can't do that")

    def __neg__(self):
        mp = {}
        for key in self.internal.keys():
            mp[key] = -self.internal[key]
        return mypoly(mp)

    def __repr__(self):
        listy = sorted(self.internal.keys())
        if listy[0]==0:
            ypart = ''
        else: ypart = 'y^'+str(listy[0])
        if type(self.internal[listy[0]])==puiseux:
            toReturn = '('+str(self.internal[listy[0]])+')'+ ypart
        else:
            toReturn = str(self.internal[listy[0]])+ ypart
        for elt in listy[1:]:
            if type(self.internal[elt])==int and self.internal[elt]<0:
                toReturn+=' - '+str(0-self.internal[elt])+'y^'+str(elt)
            elif type(self.internal[elt])==puiseux:
                toReturn += ' + ('+str(self.internal[elt])+')y^'+str(elt)
            else:
                toReturn+=' + '+str(self.internal[elt])+'y^'+str(elt)
        return toReturn
 
    def __str__(self):
        return self.__repr__()

    def __call__(self,value):
        """
        Calls :py:func:`evaluate`
        """
        return self.evaluate(value)

    def evaluate(self,value):
        """
        Evaluates self at value.

        Use Horner's scheme to speed this up?
        """
        toReturn = 0
        for exponent in self.internal.keys():
            toReturn = (value**exponent)*self.internal[exponent]+toReturn 
        return toReturn

    def support(self):
        """
        Returns a list of ordered pairs *(a,b)* where *a* is the degree
        of a monomial in :py:data:`self` and *b* is the order of that monomial's
        Puiseux coefficient.
        """
        toReturn = []
        for key in self.internal.keys():
            coeff = self.internal[key]
            if type(coeff)==puiseux:
                toReturn.append([key,coeff.order()])
            else:
                toReturn.append([key,0])
        return toReturn

    def degree(self):
        """
        Returns the degree of :py:data:`self`.
        """
        return max(self.internal.keys())

if __name__=='__main__':
    poly = mypoly({0:puiseux({2:1,3:-1}),1:puiseux({1:-2}),2:puiseux({0:1})})
    poly = mypoly({0:puiseux({4:2}),1:puiseux({2:1}),2:puiseux({1:4}),3:puiseux({0:4})})
    print 'poly: ',poly
    first = puiseux({2:-2})
    print first
    print poly(first)
    print poly
    print poly.support()
    print poly.degree()
