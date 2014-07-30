#coding=utf-8
from numpy import arange, cos, linspace, pi, sin, random
from scipy.interpolate import splprep, splev
from matplotlib import pyplot, rcParams
rcParams['font.sans-serif'] = 'Arial'

# make ascending spiral in 3-space
t=linspace(0,1.75*2*pi,100)

x = cos(t)
y = t

# add noise
#x+= random.normal(scale=0.5, size=x.shape)
y+= random.normal(scale=1, size=y.shape)

print x,y

# spline parameters
s=5.0 # smoothness parameter
k=3 # spline order
nest=-1 # estimate of number of knots needed (-1 = maximal)

# find the knot points
tckp,u = splprep([x,y],s=s,k=k,nest=nest)

# evaluate spline, including interpolated points
xnew,ynew = splev(linspace(0,1,500),tckp)

pyplot.plot(x,y,'bo-',label='data')
pyplot.plot(xnew,ynew,'r-',label='fit')
#pyplot.plot(linspace(0,1,100),y, 's')
pyplot.legend(loc='best')
pyplot.grid(True)
pyplot.xlabel('x')
pyplot.ylabel('y')


pyplot.show()