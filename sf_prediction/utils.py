import warnings
from time import time
from collections import defaultdict
import numpy as np
import pandas as pd

from scipy.stats import pearsonr

from pymanopt import Problem
from pymanopt.manifolds import Rotations

from scipy import sparse as ssp
from scipy import linalg
import scipy.optimize as sopt
import scipy.linalg._matfuncs_inv_ssq
from scipy.sparse.linalg import eigsh
from scipy.sparse.csgraph import connected_components

from sklearn.utils import check_random_state

from typing import List

from brainspace.gradient.utils import is_symmetric, make_symmetric
from SFConjugateGradient import SFConjugateGradient, BetaTypes


def logm(A):
    # Avoid circular import ... this is OK, right?
    return scipy.linalg._matfuncs_inv_ssq._logm(A)


def update_weights(sw_train, fc_pos, tri, rot, alpha):
    n_train = len(sw_train)
    n_rois = sw_train[0].shape[1]
    x = [None] * n_train
    intercept = np.ones((n_rois*(n_rois-1)//2, 1))
    for i in range(n_train):
        x[i] = np.hstack([predict_fc(sw_train[i], rot, tri).T, intercept])

    x = np.stack(x, 0)
    y = fc_pos
    return _non_negative_ridge(x, y, alpha, solver='TNC')


def _non_negative_ridge(X, y, alpha, solver=None):
    nc = X[0].shape[1]

    # x^T Q x + C_col x
    qs = X.swapaxes(-2, -1) @ X
    for q in qs:
        q.flat[::nc + 1] += alpha

    cs = (X.swapaxes(-2, -1) @ y[..., None]).squeeze()
    cs *= -2

    def loss(w):
        return np.mean(w.T.dot(qs).dot(w) + cs.dot(w))

    def grad(w):
        return np.mean(qs.dot(w)*2 + cs, axis=0)

    w0 = np.ones(nc)
    bounds = ((0, None),) * nc
    coef = sopt.minimize(loss, w0, jac=grad, method=solver, bounds=bounds).x
    return coef


def _graph_is_connected(graph):
    return connected_components(graph)[0] == 1


def diffusion_mapping(adj, n_components=10, alpha=0.5, drop_first=True,
                      random_state=0):
    """Compute diffusion map of affinity matrix.

    Parameters
    ----------
    adj : ndarray or sparse matrix, shape = (n, n)
        Affinity matrix.
    alpha : float, optional
        Anisotropic diffusion parameter, ``0 <= alpha <= 1``. Default is 0.5.

    Returns
    -------
    v : ndarray, shape (n, n_components)
        Eigenvectors of the affinity matrix in same order.
    w : ndarray, shape (n_components,)
        Eigenvalues of the affinity matrix in descending order.

    References
    ----------
    * Coifman, R.R.; S. Lafon. (2006). "Diffusion maps". Applied and
      Computational Harmonic Analysis 21: 5-30. doi:10.1016/j.acha.2006.04.006
    * Joseph W.R., Peter E.F., Ann B.L., Chad M.S. Accurate parameter
      estimation for star formation history in galaxies using SDSS spectra.
    """

    if isinstance(adj, list):
        n = len(adj)
        v, w = [None] * n, [None] * n
        for i, x1 in enumerate(adj):
            v[i], w[i] = diffusion_mapping(x1, n_components=n_components,
                                           alpha=alpha, drop_first=drop_first,
                                           random_state=random_state)
        return v, w

    use_sparse = ssp.issparse(adj)

    if drop_first:
        n_components = min(adj.shape[0], n_components+1)

    # Make symmetric
    if not is_symmetric(adj, tol=1e-10):
        warnings.warn('Affinity is not symmetric. Making symmetric.')
        adj = make_symmetric(adj, check=False, copy=True, sparse_format='coo')
    else:  # Copy anyways because we will be working on the matrix
        adj = adj.tocoo(copy=True) if use_sparse else adj.copy()

    # Check connected
    if not _graph_is_connected(adj):
        warnings.warn('Graph is not fully connected.')

    if alpha > 0:
        if use_sparse:
            d = np.power(adj.sum(axis=1).A1, -alpha)
            adj.data *= d[adj.row]
            adj.data *= d[adj.col]
        else:
            d = np.power(adj.sum(axis=1, keepdims=True), -alpha)
            adj *= d
            adj *= d.T

    if use_sparse:
        d_alpha = np.power(adj.sum(axis=1).A1, -.5)
        adj.data *= d_alpha[adj.row]
        adj.data *= d_alpha[adj.col]
    else:
        d = np.power(adj.sum(axis=1, keepdims=True), -.5)
        adj *= d
        adj *= d.T

    rs = check_random_state(random_state)
    v0 = rs.uniform(-1, 1, adj.shape[0])

    # Find largest eigenvalues and eigenvectors
    w, v = eigsh(adj, k=n_components, which='LM', tol=0, v0=v0)

    # Sort descending
    w, v = w[::-1], v[:, ::-1]
    if drop_first:
        w, v = w[1:], v[:, 1:]
    v *= np.sign(v[np.abs(v).argmax(axis=0), range(v.shape[1])])
    return v, w


def create_walks(nt, sc_grad, sc_lamb, cumulate=False, ref=None):
    if isinstance(sc_grad, list):
        w = [None] * len(sc_grad)
        for i, s in enumerate(sc_grad):
            w[i] = create_walks(nt, s, sc_lamb[i], cumulate=cumulate, ref=ref)
        return w

    if nt < 0:
        w = sc_grad * (sc_lamb / (1 - sc_lamb))

    elif nt > 0:
        if cumulate:
            w = sc_grad * (sc_lamb ** nt)
        else:
            w = sc_grad * (sc_lamb ** np.arange(1, nt + 1)[:, None, None])
    else:
        w = sc_grad

    if w.ndim == 2:
        w = w[None]

    if ref is not None:
        w = w @ (sc_grad.T @ ref)

    return w


def preprocess_sc(sc, tri):
    return [x/x.max() for x in sc]


def get_initial_rotations(sc_grad, sc_lamb, fc_grad, fc_lamb, n_rot=1):
    fw = (fc_grad * fc_lamb) @ fc_grad.T @ sc_grad
    rotations = []
    for i in range(1, n_rot+1):
        sw = (sc_grad * sc_lamb**i) @ sc_grad.T @ sc_grad

        a, _, b = linalg.svd(fw.astype(np.float64) @ sw.T.astype(np.float64))
        rot = b.T @ a.T

        if abs(1.0 - np.linalg.det(rot)) > 1e-10:
            c = np.append(np.ones(rot.shape[0] - 1), -1)
            rot = (b.T * c) @ a.T

        rotations.append(rot)

    if n_rot == 1:
        return rotations[0]
    return np.stack(rotations, 0)


def predict(sc_grad, tri, rot, weights):
    nr, nc = len(sc_grad), np.count_nonzero(tri)
    pred = np.empty((nr, nc), dtype=np.float32)
    for i, grad in enumerate(sc_grad):
        pred[i] = predict_fc(grad, rot, tri, weights=weights)
    pred *= 2
    pred -= 1
    return pred


def eval_data(sc_grad, fc_gt, tri, weights, q):
    scores_pearson = np.empty(len(fc_gt))

    n2 = np.count_nonzero(tri)
    pred = np.empty((len(fc_gt), n2), dtype=np.float32)
    for idx, fc1 in enumerate(fc_gt):
        dsc = predict_fc(sc_grad[idx], q, tri, weights=weights)
        p = 2 * dsc - 1
        pred[idx] = p
        scores_pearson[idx] = pearsonr(p, fc1[tri])[0]
    return scores_pearson, pred


def predict_and_grad(sc_grad, rot, tri, weights):
    # R * X * X'
    RXXt = (rot @ sc_grad) @ sc_grad.swapaxes(-1, -2)

    # (R * X * X') * R'
    d = RXXt @ rot.swapaxes(-1, -2)

    # Euclidean distance matrix
    # 2d - d*diag(I) - diag(I)'*d
    diag = -np.diagonal(d, axis1=-1, axis2=-2)
    d *= 2
    d += diag[:, None]
    d += diag[..., None]

    # Build RBF kernels
    d = d[:, tri]
    gamma = 1/d.std(axis=1, keepdims=True)
    d *= gamma
    d = np.exp(d, d)

    # Fuse
    pred = d.T @ weights[:-1] + weights[-1]

    return d, gamma, pred, RXXt


def predict_fc(sc_grad, rot, tri, weights=None):
    d = rot @ sc_grad
    d = d @ d.swapaxes(-1, -2)

    diag = -np.diagonal(d, axis1=-1, axis2=-2)
    d *= 2
    d += diag[:, None]
    d += diag[..., None]

    # Build RBF kernels
    d = d[:, tri]
    d /= d.std(axis=1, keepdims=True)
    d = np.exp(d, d)

    if weights is not None:
        return d.T @ weights[:-1] + weights[-1]
    return d


def _manopt_learn(sc_grad, fc_pos, w, n_walks=2, n_rots=1, rot=None,
                  manopt_iter=10, n_iter=10, verbose=2, mu1=0.01, mu2=0.001):

    ns = fc_pos.shape[0]
    n_rois = sc_grad[0].shape[1]

    tri = np.tri(n_rois, k=-1, dtype=np.bool_).T
    mask_diag = np.eye(n_rois, dtype=np.bool_)
    manifold = Rotations(n_rois, k=n_rots)

    ###########################################################################
    ###########################################################################
    def gossip(x):
        dist_reg = x[1:].swapaxes(-1, -2) @ x[:-1]
        dist_reg = np.real(np.stack([logm(d) for d in dist_reg], 0))

        # skew - see manopt
        dist_reg -= dist_reg.swapaxes(-1, -2)
        dist_reg *= .5
        return dist_reg

    def grad(x, store=None):
        kernels = np.empty((n_walks, n_rois, n_rois))
        kernels[:, mask_diag] = 1 - w.sum()

        # Grad data term
        g = None
        for i in range(ns):

            if store is None:
                ker, gamma, p, RXXt = predict_and_grad(sc_grad[i], x, tri, w)
                dif = fc_pos[i] - p
            else:
                ker, gamma, dif, RXXt = store[i]

            ker *= dif

            kernels[:, tri] = kernels.swapaxes(-1, -2)[:, tri] = ker
            obj = -kernels @ RXXt
            obj += kernels.sum(1)[..., None] * RXXt
            s = 8 * w[:-1] * gamma.ravel()
            obj *= s[:, None, None]

            if g is None:
                if n_rots == 1 and obj.squeeze().ndim > 2:
                    g = obj.sum(0)
                else:
                    g = obj
            else:
                if n_rots == 1 and obj.squeeze().ndim > 2:
                    g += obj.sum(0)
                else:
                    g += obj

        # Grad regularization:  -2*R1 @ logm(R1.T@R0)
        if w.size > 2 and mu2 > 0:
            reg = gossip(x) if store is None else store['reg']
            g[1:] -= 2 * (mu2/(w.size-1)) * (x[1:] @ reg)

        g /= ns

        # Map Euclidean gradient to Riemannian
        g = x.swapaxes(-2, -1) @ g
        g -= g.swapaxes(-2, -1)
        g *= .5
        return g

    def cost(x, return_store=False):
        if return_store:
            store = dict()

        c = 0
        for i in range(ns):
            if return_store:
                ker, gamma, p, RXXt = predict_and_grad(sc_grad[i], x, tri, w)
                dif = fc_pos[i] - p
                store[i] = [ker, gamma, dif, RXXt]
            else:
                p = predict_fc(sc_grad[i], x, tri, weights=w)
                dif = fc_pos[i] - p

            c += 2 * np.linalg.norm(dif) ** 2

        c /= ns

        # Cost of diagonal
        c += n_rois * (1 - w.sum())**2

        # Cost Riemannian regularization
        if w.size > 2 and mu2 > 0:
            reg = gossip(x)
            c += (mu2/(w.size - 1)) * np.linalg.norm(reg) ** 2
            if return_store:
                store['reg'] = reg

        if return_store:
            return c, store
        return c
    ###########################################################################
    ###########################################################################

    # Problem
    manopt_iter = max(3, manopt_iter)
    verbosity = 2 if verbose > 2 else 0
    problem = Problem(manifold, cost, grad=grad, verbosity=verbosity)
    solver = SFConjugateGradient(beta_type=BetaTypes.FletcherReeves,
                                 maxiter=manopt_iter, cost_fun=cost,
                                 grad_fun=grad)

    t1 = time()
    for it in range(n_iter):
        if verbose > 1:
            print(f'{it + 1:>2} ', end='')

        # Update rotations
        rot = solver.solve(problem, x=rot)

        # Update weights
        w = update_weights(sc_grad, fc_pos, tri, rot, mu1)

    if verbose > 1:
        print(f'done! {time()-t1:.2f}s')
    return rot, w


def run_sf_prediction(sc_train: List[np.ndarray], fc_train: List[np.ndarray],
                      sc_test: List[np.ndarray], fc_test: List[np.ndarray],
                      n_walks: int = 10, mu1: float = 0.01, mu2: float = 0,
                      single_length: bool = False, shared_rot: bool = False,
                      n_comp: int = 50, warm_start: bool = True,
                      n_iter: int = 20, manopt_iter: int = 5,
                      verbose: bool = True):
    """Train/test prediction of functional connectivity

    Parameters
    ----------
    sc_train: list of ndarray
        Structural connectivity matrices for training.
    fc_train: list of ndarray
        Functional connectivity matrices for training.
    sc_test: list of ndarray
        Structural connectivity for testing.
    fc_test: list of ndarray
        Functional connectivity for testing.
    n_walks: int
        Maximum length of random walks.
    mu1: float, default = 0.01
        Strength of ridge regularization.
    mu2: float, default = 0
        Strength of Riemannian regularization. Not used if set to 0.
    single_length: bool, default = False
        Only consider random walks of a specific length.
    shared_rot: bool, default = False
        Only use one single rotation shared by all random walks.
    n_comp: int, default = 50
        Number of structural eigenvectors.
    warm_start: bool, default = True
        Initialize next iteration's parameters (weights and rotations) with
        those learned in previous iteration.
    n_iter: int, default = 20
        Number of iterations for optimization.
    manopt_iter: int, default = 20
        Number of Conjugate gradient iteration for each outer iteration.
    verbose: bool, default = True
        Verbosity.

    Returns
    -------
    scores: list of pd.DataFrame
        DataFrame with prediction performance in test data.
    params: dict of list
        Optimal Weights and rotations matrices learned for each  random walk
        length.
    preds: dict of list
        Predicted connectivity matrices for each random walk length.
    """

    t0 = time()

    n_rois = sc_train[0].shape[0]
    n_train = len(sc_train)
    n_test = len(sc_test)

    tri = np.tri(n_rois, k=-1, dtype=np.bool_).T

    # Preprocessing
    sc_train = preprocess_sc(sc_train, tri)
    sc_test = preprocess_sc(sc_test, tri)

    fc_pos = np.vstack([f[tri] for f in fc_train])
    fc_pos += 1
    fc_pos *= .5

    # Embedding
    kwds = dict(alpha=0, n_components=n_comp, drop_first=False, random_state=0)
    sv_train, sl_train = diffusion_mapping(sc_train, **kwds)
    sv_test, sl_test = diffusion_mapping(sc_test, **kwds)

    sg1, sl1 = sv_train[0], sl_train[0]
    fg1, fl1 = diffusion_mapping(.5 * (1+fc_train[0]), **kwds)
    #########################################################################
    #########################################################################

    # Create dataframes to store results
    met = ['pearson']
    if isinstance(n_walks, (list, np.ndarray)):
        walks = list(n_walks)
    else:
        walks = range(1, n_walks+1)

    names = ['Metric', 'Dataset', 'Walk']
    col_train = pd.MultiIndex.from_product([met, ['train'], walks],
                                           names=names)
    scores_train = pd.DataFrame(0, columns=col_train, index=range(n_train))
    col_test = pd.MultiIndex.from_product([met, ['test'], walks],
                                          names=names)
    scores_test = pd.DataFrame(0, columns=col_test, index=range(n_test))
    scores = {'train': scores_train, 'test': scores_test}

    preds = defaultdict(dict)
    params = dict()
    for i, iw in enumerate(walks):
        t1 = time()

        sw_train = create_walks(iw, sv_train, sl_train, cumulate=single_length,
                                ref=sv_train[0])

        n_rots = 1 if (shared_rot or single_length) else iw
        q0 = get_initial_rotations(sg1, sl1, fg1, fg1, n_rot=n_rots)
        if warm_start and i > 0:
            if shared_rot:
                q0 = q.squeeze()
            elif single_length:
                q0 = q.squeeze()
            else:
                q0[:i] = q

        q = q0

        # Initial weights
        if single_length:
            w = np.ones(2) / 2
        else:
            w = np.ones(iw+1) / (iw+1)

        # Optimization
        n_walks_learn = 1 if single_length else iw
        q, w = _manopt_learn(sw_train, fc_pos, w, n_walks=n_walks_learn,
                             n_rots=n_rots, rot=q,
                             manopt_iter=manopt_iter, n_iter=n_iter,
                             verbose=verbose, mu1=mu1, mu2=mu2)

        # Save rotations and weights
        params[iw] = [q, w]

        # Evaluate
        sw_test = create_walks(iw, sv_test, sl_test, cumulate=single_length,
                               ref=sv_train[0])
        list_sw = [sw_train] + [sw_test]
        list_gt = [fc_train] + [fc_test]
        for k, sw, fc in zip(['train', 'test'], list_sw, list_gt):
            pc, pred = eval_data(sw, fc, tri, w, q)
            scores[k].loc[:, ('pearson', k, iw)] = pc
            preds[iw][k] = pred

        if verbose > 0:
            if iw == walks[0]:
                print('         Train        Test')

            p = scores_train.loc[:, ('pearson', 'train', iw)]
            mean_tr, sd_tr = p.agg({'mp': 'mean', 'sp': 'std'})

            p = scores_test.loc[:, ('pearson', 'test', iw)]
            mean_te, sd_te = p.agg({'mp': 'mean', 'sp': 'std'})

            pm = '\u00B1'
            print(f'Walk {iw:>2}: {mean_tr:.3f}{pm}{sd_tr:.3f}  '
                  f'{mean_te:.3f}{pm}{sd_te:.3f}\t\t{time() - t1:>8.2f}s')

            if iw == walks[-1]:
                print(f"{' '*33}\t\t{'-'*9}")
                print(f"{' '*33}\t\t{time() - t0:>8.2f}s")

    return scores_test, params, preds
