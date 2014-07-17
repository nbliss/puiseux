import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider
from puiseuxExpansion import solutionList
from mypoly import mypoly
from puiseuxPoly import puiseux
import sys


def solLists(poly,NUMTERMS,solNum=0):
    """
    For a mypoly poly, computes a list of the roots of
    the truncated power series of the solNum-th for 2 terms
    up through NUMTERMS terms, and returns these in one big list.
    """
    s = solutionList(poly,NUMTERMS)[solNum]
    sols = []

    for i in xrange(2,len(s)):
        toSolve = []
        for j in xrange(int(s[i][0])):toSolve.append(0)
        toSolve.append(0)
        for item in s[:i]:
            toSolve[int(item[0])] = item[1]
        #toSolve[1]=-1
        toSolve.reverse()
        roots = np.roots(toSolve)
        toAdd = []
        for j in xrange(len(roots)):
            toAdd.append([roots[j].real,roots[j].imag])
        toAdd = [[item[0] for item in toAdd],[item[1] for item in toAdd]]
        sols.append(toAdd)
    return sols,len(s)

def minmax(sols):
    """
    Takes the list of solution lists and computes a good
    graphing window
    """
    xmax,xmin = sols[0][0][0],sols[0][0][0]
    ymin,ymax = sols[0][1][0],sols[0][1][0]
    for sublist in sols:
        axmin,axmax = min(sublist[0]), max(sublist[0])
        aymin,aymax = min(sublist[1]), max(sublist[1])
        if axmin<xmin: xmin=axmin
        if axmax>xmax: xmax = axmax
        if aymin<ymin: ymin = aymin
        if aymax>ymax: ymax = aymax
    xdif = (xmax-xmin)/6
    ydif = (ymax-ymin)/6
    xmin -= xdif
    xmax += xdif
    ymin -= ydif
    ymax += ydif
    return [xmin,xmax,ymin,ymax]


class ChangingPlot(object):
    """
    Gives a pyplot object with a slider that shows the complex roots of
    the truncated power series for the number of terms on the slider.
    """
    def __init__(self,poly,NUMTERMS):
        self.sols,self.NUMTERMS = solLists(poly,NUMTERMS)
        self.windowBounds = minmax(self.sols)
        self.inc = 1.0

        self.fig, self.ax = plt.subplots()
        self.sliderax = self.fig.add_axes([0.2, 0.02, 0.6, 0.03],
                                          axisbg='yellow')

        self.slider = Slider(self.sliderax, 'Value', 0, self.NUMTERMS-3, valinit=self.inc)
        self.slider.on_changed(self.update)
        self.slider.drawon = False

        self.dot, = self.ax.plot(self.sols[0][0],self.sols[0][1], 'bo')
        self.ax.axis(self.windowBounds)

    def update(self, value):
        value = int(value)
        self.dot.set_data(self.sols[value][0],self.sols[value][1])
        self.slider.valtext.set_text('{}'.format(value))
        self.fig.canvas.draw()

    def show(self):
        plt.show()

if __name__=='__main__':
    NUMTERMS = 75
    poly = mypoly({0:puiseux({0:-1,2:1}),2:puiseux({0:1})})
    print solutionList(poly,4)
    #poly = mypoly({2:puiseux({0:-1}),0:puiseux({3:1,1:-27,0:2*27})})
    p = ChangingPlot(poly,NUMTERMS)
    if '-s' in sys.argv:
        p.show()
