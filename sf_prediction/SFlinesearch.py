"""
Adapted from Pymanopt
"""

from __future__ import division

import scipy.linalg as la
import numpy as np


def retri(x):
    x, r = la.qr(x, check_finite=False, overwrite_a=True)
    s = np.sign(np.diag(r))
    s += .5
    x *= np.sign(s)
    return x


def retr(x, d, alpha):
    newx = x @ d
    newx *= alpha
    newx += x
    if newx.ndim == 2:
        return retri(newx)

    for i, x1 in enumerate(newx):
        newx[i] = retri(x1)
    return newx


class LineSearchAdaptive(object):
    '''
    Adaptive line-search
    '''

    def __init__(self, contraction_factor=.5, suff_decr=.5, maxiter=10,
                 initial_stepsize=1):
        self._contraction_factor = contraction_factor
        self._suff_decr = suff_decr
        self._maxiter = maxiter
        self._initial_stepsize = initial_stepsize
        self._oldalpha = None

    def search(self, objective, man, x, d, f0, df0):
        norm_d = man.norm(x, d)

        if self._oldalpha is not None:
            alpha = self._oldalpha
        else:
            alpha = self._initial_stepsize / norm_d
        alpha = float(alpha)

        newx = retr(x, d, alpha)  # man.retr(x, alpha * d)
        newf = objective(newx)
        cost_evaluations = 1

        while (newf > f0 + self._suff_decr * alpha * df0 and
               cost_evaluations <= self._maxiter):
            # Reduce the step size.
            alpha *= self._contraction_factor

            # Look closer down the line.
            newx = retr(x, d, alpha)  # man.retr(x, alpha * d)
            newf = objective(newx)

            cost_evaluations += 1

        if newf > f0:
            alpha = 0
            newx = x

        stepsize = alpha * norm_d

        # Store a suggestion for what the next initial step size trial should
        # be. On average we intend to do only one extra cost evaluation. Notice
        # how the suggestion is not about stepsize but about alpha. This is the
        # reason why this line search is not invariant under rescaling of the
        # search direction d.

        # If things go reasonably well, try to keep pace.
        if cost_evaluations == 2:
            self._oldalpha = alpha
        # If things went very well or we backtracked a lot (meaning the step
        # size is probably quite small), speed up.
        else:
            self._oldalpha = 2 * alpha

        return stepsize, newx
