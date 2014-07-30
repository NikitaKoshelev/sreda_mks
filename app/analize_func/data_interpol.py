# coding=utf-8
import numpy as np
from scipy import interpolate
from scipy.signal import cspline1d, cspline1d_eval
from numpy import r_


def movingaverage(values, window):
    weigths = np.repeat(1.0, window)/window
    smas = np.convolve(values, weigths, 'valid')
    return smas


def ExpMovingAverage(values, window):
    weights = np.exp(np.linspace(-1., 0., window))
    weights /= weights.sum()
    a = np.convolve(values, weights, mode='full')[:len(values)]
    a[:window] = a[window]
    return a


def cubic_spline(x, y, xnew=None):
    if xnew is None:
        return u'Выберите новый массив Х'
    s = interpolate.InterpolatedUnivariateSpline(x, y)
    return s(xnew)


def interpolate_1d(x, y, xnew=None):
    if xnew is None:
        return u'Выберите новый массив Х'
    f2 = interpolate.interp1d(x,y)
    return f2(xnew)


def razrezh(values=None, step=1):
    if values is None:
        return u'Выберите список значений'
    return values[::step]


def spline(x, y, s=100.0, k=1, nest=-1, num_points=75):
    # find the knot points
    tckp,u = interpolate.splprep([x, y], s=s, k=k, nest=nest)

    # evaluate spline, including interpolated points
    xnew,ynew = interpolate.splev(np.linspace(0, 1, num_points), tckp)
    del tckp,u
    return xnew,ynew