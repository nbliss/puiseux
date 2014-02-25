class puiseux(object):
	def __init__(self,poly,checkReduced=True):
		from fractions import Fraction
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
			self.internal = {Fraction(elt[1][0],elt[1][1]):elt[0] for elt in poly}
		for key in self.internal.keys():
			if self.internal[key]==0:
				self.internal.pop(key)


	def __eq__(self,other):
		if type(other)==puiseux:
			if self.internal.keys() != other.internal.keys(): return False
			equal = True
			for key in set(self.internal.keys()+other.internal.keys()):
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
		from fractions import Fraction
		if type(other) in [int,float,Fraction,long,complex]:
			return puiseux({key : other+self.internal[key] for key in self.internal.keys()})
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
		from fractions import Fraction
		if type(other) in [int,float,Fraction,long,complex]:
			return puiseux({key : self.internal[key]-other for key in self.internal.keys()})
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
		from fractions import Fraction
		if type(other) in [int,float,Fraction,long,complex]:
			return puiseux({term:other*self.internal[term] for term in self.internal})
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
		from fractions import Fraction
		if type(other)==int and other>=0:
			if other==0:
				return puiseux({Fraction(0,1):1})
			else:
				toReturn = puiseux({Fraction(0,1):1})
				for i in xrange(other-1):
					toReturn *= self
				return toReturn
		elif type(other)==int:
			raise TypeError("don't have support for negative exponents")
		else: raise TypeError("can't do that")

	def __neg__(self):
		return puiseux({term:0-self.internal[term] for term in self.internal})

        def __rmul__(self,other):return self*other
        def __radd__(self,other):return self+other
        def __rsub__(self,other):return (-self)+other

	def __repr__(self):
		listy = sorted(self.internal.keys())
		if len(listy)==0: return '0'
		if self.internal[listy[0]]==1 and listy[0]!=0:
			toReturn = 'x^('+str(listy[0])+')'
		else:
			toReturn = str(self.internal[listy[0]])+'x^('+str(listy[0])+')'
		for elt in listy[1:]:
			if type(self.internal[elt])==int and self.internal[elt]<0:
				toReturn+=' - '+str(0-self.internal[elt])+'x^('+str(elt)+')'
			elif self.internal[elt]==1 and listy[0]!=0:
				toReturn+=' + x^('+str(elt)+')'
			else:
				toReturn+=' + '+str(self.internal[elt])+'x^('+str(elt)+')'
		return toReturn
 
	def __str__(self):
		return self.__repr__()

	def LT(self):
		"""
		Returns the leading term
		"""
		lt = min(self.internal.keys())
		return puiseux({lt:self.internal[lt]})

	def LC(self):
		"""
		Returns the leading coefficient
		"""
		return self.internal[min(self.internal.keys())]

	def order(self):
		return min(self.internal.keys())

	def commonDenom(self):
		L = [term.denominator for term in self.internal.keys()]
		def lcm(a,b):
			prod = a*b
			while a:
				a,b = b%a,a
			return prod/b
		return reduce(lcm,L)

if __name__=='__main__':
	a = puiseux([[2,(2,6)],[-3,(1,10)]])
	b = puiseux([[4,(4,7)],[-5,(1,2)]])
	print a,"   <-a"
	print b,"   <-b"
	print "heyo"
	print a-b,"  <- a-b"
	print -a,"  <- -a"
	print a+b,"   <- a+b"
	print a**2
	print b
	print
	print a.LT()
	print b.LT()
	print a*b
	print (a*b).LT()
	a*=3
	print a
