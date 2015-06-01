from fractions import Fraction
from numpy.random import randint
def lowerHull(inputpts):
   """
   Given a list of lists (2-dimensional points), computes
   their lower hull, i.e. returns a list of the points on
   the lower hull ordered in the positive x-direction.
   Uses the algorithm from ??'s *Computational Geometry*
   """
   sorter = lambda x,y:x[1]-y[1] if x[0]==y[0] else x[0]-y[0]
   pts = sorted(inputpts,cmp=sorter)
   i = 0
   n = len(pts)-1
   while i<n: # remove points with repeated x-values
      if pts[i][0]==pts[i+1][0]:
         pts.remove(pts[i+1])
         n-=1
      else: i+=1
   if len(pts)<3: return pts
   i,n = 2,len(pts)
   while i<n:
      try:
         newSlope = slope(pts[i-1],pts[i])
      except IndexError:
         print pts
         print len(pts)
         print i
         print n,'<---'
      prevSlope = slope(pts[i-2],pts[i-1])
      if newSlope < prevSlope: 
         pts.pop(i-1)
         n-=1
         i-=1
         j = i
         while j>1:
            prevSlope = slope(pts[i],pts[i-1])
            wayback = slope(pts[i-2],pts[i-1])
            if prevSlope < wayback:
               pts.pop(i-1)
               n-=1
               j-=1
               i-=1
            else: break
      i+=1
   return pts



def slope(pt1,pt2):
   """
   Given two points (lists), returns the slope of the
   line connecting the two as a python :py:class:`fractions.Fraction` object
   """
   return Fraction(pt2[1]-pt1[1],pt2[0]-pt1[0])

def ploty(points,s):
   """
   Uses :py:mod:`matplotlib` to display a plot of the points and their
   lower hull connected with line segments.
   """
   import matplotlib
   #matplotlib.use('macosx')
   import matplotlib.pyplot as plt

   """
   fig = plt.figure()
   #Put figure window on top of all other windows
   fig.canvas.manager.window.attributes('-topmost', 1)
   #After placing figure window on top, allow other windows to be on top of it later
   fig.canvas.manager.window.attributes('-topmost', 0)
   """
   hull = lowerHull(points)
   plt.plot([pt[0] for pt in hull],[pt[1] for pt in hull])
   plt.plot([pt[0] for pt in points],[pt[1] for pt in points],'bo')
   plt.plot([pt[0] for pt in hull],[pt[1] for pt in hull],'ro')
   xmax = float(max([pt[0] for pt in points]))
   ymax = float(max([pt[1] for pt in points]))
   xmin = float(min([pt[0] for pt in points]))
   ymin = float(min([pt[1] for pt in points]))
   plt.axis([xmin-1,xmax+1,ymin-1,ymax+1])
   #plt.show()
   path = '/Users/nathanbliss/Documents/Google Drive/UIC_coursework/researchSpring14/pics/'+str(s)+'__'+str(randint(1e3,1e4))+'.png'
   #a = plt.savefig(path)
   #print a
   plt.clf()
   return hull

if __name__=='__main__':
   points = [[1,10],[1,5],[2,3],[3,3],[3,5],[4,4],[5,5],[4,6],[6,9]]
   #points = [[0, Fraction(5, 1)], [1, Fraction(7, 2)], [2, Fraction(1, 1)], [3, Fraction(-1, 1)], [5, Fraction(-1, 2)], [6, Fraction(1, 2)], [7, Fraction(10, 3)], [8, Fraction(5, 2)]]
   #points = [[0,4],[1,3],[3,2],[5,1],[7,0]]
   points = [[0, 3], [2, 2], [4, 6], [5, 0], [6, 4], [7, 3]]
   hull = lowerHull(points)
   print points
   print hull
   ploty(points,1)
