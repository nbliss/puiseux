from fractions import Fraction
TOLERANCE=1e-8
class puiseux(object):
    """
    Class to represent (truncated) Puiseux series.
    """
    def __init__(self,poly,checkReduced=False):
        """
        2x^(2/3)-3x^(4/7) would be input as
        [[2,(2,3)],[-3,(1,7)]] and represented internally as
        {Fraction(1,7):-3,Fraction(2,3):2}
        --OR-- input as a dictionary and just copied to internal

        checkReduced is a flag that determines if when setting
        up the internal representation we check for like terms.
        Be careful with it!!! If poly is a dict, checkReduced doesn't
        matter since it can't have repeated keys (exponents)
        """
        if type(poly)==dict:
            self.internal = poly
        elif checkReduced:
            self.internal = {Fraction(poly[0][1][0],poly[0][1][1]):poly[0][0]}
            for mon in poly[1:]:
                coeff = mon[0]
                exponent = Fraction(mon[1][0],mon[1][1])
                if exponent in self.internal:
                    self.internal[exponent] += coeff
                else: self.internal[exponent] = coeff
        else:
            self.internal = {}
            for elt in poly:
                self.internal[Fraction(elt[1][0],elt[1][1])] = elt[0]
        for key in self.internal.keys():
            if type(self.internal[key])==complex:
                if self.internal[key].imag==0:
                    self.internal[key] = self.internal[key].real
            if nearZero(self.internal[key]):
                self.internal.pop(key)
        if self.internal=={}:
            self.internal = {Fraction(0,1):0}

    def __eq__(self,other):
        if type(other)==puiseux:
            if self.internal.keys() != other.internal.keys():
                return False
            equal = True
            for key in self.internal.keys():
                if not nearZero(self.internal[key]-other.internal[key]):
                    equal = False
                    break
            return equal
        else:
            l = self.internal.keys()
            if len(l)==1 and l[0]==0:
                return self.internal[l[0]]==other
            elif len(l)==0: return other==0
            return False

    def __ne__(self,other):
        return not self.__eq__(other)

    def __add__(self,other):
        if type(other) in [int,float,Fraction,long,complex]:
            pu = {}
            for key in self.internal.keys():
                pu[key] = other+self.internal[key] 
            return puiseux(pu)
        elif type(other)==puiseux:
            toReturn = {}
            for key in self.internal.keys():
                if key in other.internal.keys():
                    toReturn[key]=self.internal[key]+other.internal[key]
                else:
                    toReturn[key]=self.internal[key]
            for key in other.internal.keys():
                if key not in toReturn:
                    toReturn[key]=other.internal[key]
            return puiseux(toReturn)
        else: raise TypeError("can't do that")

    def __sub__(self, other):
        if type(other) in [int,float,Fraction,long,complex]:
            pu = {}
            for key in self.internal.keys():
                pu[key] = self.internal[key]-other
            return puiseux(pu)
        elif type(other)==puiseux:
            toReturn = {}
            for key in self.internal.keys():
                if key in other.internal.keys():
                    toReturn[key]=self.internal[key]-other.internal[key]
                else:
                    toReturn[key]=self.internal[key]
            for key in other.internal.keys():
                if key not in toReturn:
                    toReturn[key]=(-other.internal[key])
            return puiseux(toReturn)
        else: raise TypeError("can't do that")


    def __mul__(self, other):
        if type(other) in [int,float,Fraction,long,complex]:
            pu = {}
            for key in self.internal.keys():
                pu[key] = other*self.internal[key]
            return puiseux(pu)
        elif type(other)==puiseux:
            toReturn = {}
            for key1 in other.internal.keys():
                for key2 in self.internal.keys():
                    coeff = other.internal[key1]*self.internal[key2]
                    exponent = key1 + key2
                    if exponent in toReturn:
                        toReturn[exponent] += coeff
                    else: toReturn[exponent]=coeff
            return puiseux(toReturn,checkReduced=False)
        else: raise TypeError("can't do that")

    def __pow__(self,other):
        if type(other)==int and other>=0:
            if other==0:
                return puiseux({Fraction(0,1):1})
            else:
                toReturn = puiseux({Fraction(0,1):1})
                for i in xrange(other):
                    toReturn *= self
                return toReturn
        elif type(other)==int:
            raise TypeError("don't have support for negative exponents")
        else: raise TypeError("can't do that")

    def __neg__(self):
        pu = {}
        for key in self.internal.keys():
            pu[key] = 0-self.internal[key]
        return puiseux(pu)

    def __rmul__(self,other):return self*other
    def __radd__(self,other):return self+other
    def __rsub__(self,other):return (-self)+other

    def __call__(self,value):
        """
        Evaluates :py:obj:`self`.

        Will break on fractional exponents!!!!

        Wait...Python allows fractions as exponents, so might be fine
        """
        toReturn = 0
        for ex in self.internal:
            if ex.denominator!=1:
                raise TypeError("Trying to use "+str(ex)+" as an exponent")
            toReturn += self.internal[ex]*value**ex
        return toReturn

    def __repr__(self):
        listy = sorted(self.internal.keys())
        if len(listy)==0: return '0'
        if self.internal[listy[0]]==1 and listy[0]!=0:
            toReturn = 'x^('+str(listy[0])+')'
        else:
            toReturn = '('+str(self.internal[listy[0]])+')x^('+str(listy[0])+')'
        for elt in listy[1:]:
            if type(self.internal[elt])==int and self.internal[elt]<0:
                toReturn+=' - '+str(0-self.internal[elt])+'x^('+str(elt)+')'
            elif self.internal[elt]==1 and listy[0]!=0:
                toReturn+=' + x^('+str(elt)+')'
            else:
                toReturn+=' + ('+str(self.internal[elt])+')x^('+str(elt)+')'
        return toReturn
 
    def __str__(self):
        return self.__repr__()

    def __hash__(self):
        return hash(sum(self.internal.keys()))

    def LT(self):
        """
        Returns the leading term.
        """
        lt = min(self.internal.keys())
        return puiseux({lt:self.internal[lt]})

    def monicLT(self):
        """
        Returns a monic version of the leading term.
        """
        return puiseux({min(self.internal.keys()):1})

    def LC(self):
        """
        Returns the leading coefficient.
        """
        return self.internal[min(self.internal.keys())]

    def TT(self):
        """
        Return the trailing term.
        """
        return self.internal[max(self.internal.keys())]

    def order(self):
        """
        Returns the minimum exponent.
        """
        return min(self.internal.keys())

    def trunc(self,n):
        """
        Returns the ``n`` lowest degree terms of ``self``, or just
        returns ``self`` if there are <= ``n`` terms.
        """
        if len(self.internal.keys())<=n: return self
        exps = sorted(self.internal.keys())[:n]
        return puiseux({i:self.internal[i] for i in exps})

    def commonDenom(self):
        """
        Returns the common denominator of the exponents.
        """
        L=[]
        for term in self.internal.keys():
            L.append(term.denominator)
        def lcm(a,b):
            prod = a*b
            while a:
                a,b = b%a,a
            return prod/b
        return reduce(lcm,L)

def nearZero(a):
    """
    Returns true if *a* is an int, long, or Fraction is and ==0.

    Also returns true if *a* is a float or complex and is near 0.
    """
    if type(a) in [int, long]: return a==0
    if type(a)==Fraction: return a==0
    if type(a) in [float,complex]:
        return abs(a)<TOLERANCE
    return abs(a)<TOLERANCE

if __name__=='__main__':
    a = puiseux([[2,(2,6)],[-3,(1,10)]])
    b = puiseux([[4,(4,7)],[-5,(1,2)]])
    c = puiseux([[4,(4,7)],[-5,(1,2)],[0,(3,4)]])
    print c
    print c.trunc(1)
    print c.trunc(0)
