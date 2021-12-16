from scipy import stats
import numpy as np
from mne.stats import permutation_cluster_test

from brainspace.mesh import mesh_elements as me


ICN_NAMES = np.array(['DAN', 'FPN', 'DMN', 'VN', 'LSN', 'SMN', 'VAN'])


def unravel_symmetric(x, size, as_sparse=False, part='both', fmt='csr'):
    """Build symmetric matrix from array with upper triangular elements.

    Parameters
    ----------
    x : 1D ndarray
        Input data with elements to go in the upper triangular part.
    size : int
        Number of rows/columns of matrix.
    as_sparse : bool, optional
        Return a sparse matrix. Default is False.
    part: {'both', 'upper', 'lower'}, optional
        Build matrix with elements if both or just on triangular part.
        Default is both.
    fmt: str, optional
        Format of sparse matrix. Only used if ``as_sparse=True``.
        Default is 'csr'.

    Returns
    -------
    sym : 2D ndarray or sparse matrix, shape = (size, size)
        Array with the lower/upper or both (symmetric) triangular parts
        built from `x`.

    """

    k = 1
    if (size * (size + 1) // 2) == x.size:
        k = 0
    elif (size * (size - 1) // 2) != x.size:
        raise ValueError('Cannot unravel data. Wrong size.')

    shape = (size, size)
    if as_sparse:
        mask = x != 0
        x = x[mask]

        idx = np.triu_indices(size, k=k)
        idx = [idx1[mask] for idx1 in idx]
        if part == 'lower':
            idx = idx[::-1]
        elif part == 'both':
            idx = np.concatenate(idx), np.concatenate(idx[::-1])
            x = np.tile(x, 2)

        xs = ssp.coo_matrix((x, idx), shape=shape)
        if fmt != 'coo':
            xs = xs.asformat(fmt, copy=False)

    else:
        mask_lt = np.tri(size, k=-k, dtype=np.bool)
        xs = np.zeros(shape, dtype=x.dtype)

        xs[mask_lt.T] = x
        if part == 'both':
            xs.T[mask_lt.T] = x
        elif part == 'lower':
            xs = xs.T

    return xs


def regress_out(y, x, mask_control=None, add_intercept=True):
    """Removes effects of x from y

    Parameters
    ----------
    y : np.ndarray of shape (n_subjects, n_points)
        Data to be deconfounded.
    x : np.ndarray of shape (n_subjects, n_feat_to_control_for)
       Variables to control for.
    mask_control : np.ndarray of shape (n_subjects,), default=None
        Boolean array of control subjects. If provided, only fit model to
        controls and regress out from all.
    add_intercept : bool, default=True
        Add intercept.

    Returns
    -------
    xd: np.ndarray of shape (n_subjects, n_points)
        Deconfounded data.
    """

    if add_intercept:
        x = np.column_stack([np.ones(y.shape[0]), x])

    if mask_control is not None:
        betas = np.linalg.lstsq(x[mask_control], y[mask_control],
                                rcond=None)[0]
    else:
        betas = np.linalg.lstsq(x, y, rcond=None)[0]

    if add_intercept:
        res = x[:, 1:].dot(-betas[1:])
    else:
        res = x.dot(-betas)
    res += y

    return res


def tfce(x, mask_asd, surf, n_perm=100, alpha=0.05):
    """ TFCE.

    Parameters
    ----------
    x: np.ndarray of shape (n_subjects, n_vertices)
        Data.
    mask_asd: np.ndarray of shape (n_subjects,)
        Boolean mask indicating ASD (True) and TD (False).
    surf: BSPolydata
        Cortical surface.
    n_perm: int, default=100
        Number of permutations.
    alpha: float, default=0.05
         Significance threshold.

    Returns
    -------
    t_obs: np.ndarray of shape (n_vertices,)
        t-statistic.
    sig: np.ndarray of shape (n_vertices,)
        Boolean array with significant vertices set to True.
    """

    adj = None
    if 'mask' in surf.point_keys:
        mask = surf.PointData['mask'] == 1
        adj = me.get_immediate_adjacency(surf, mask=mask)

    def stat_fun(*args):
        return stats.ttest_ind(*args)[0]

    p_F_obsp, p_cl, clp_pv, h0 = \
        permutation_cluster_test([x[mask_asd], x[~mask_asd]], tail=0,
                                 connectivity=adj, n_permutations=n_perm,
                                 out_type='indices', check_disjoint=True,
                                 seed=0, n_jobs=-1, stat_fun=stat_fun,
                                 threshold=dict(start=0, step=0.25),
                                 t_power=1, verbose=0)

    good_cluster_inds = np.where(clp_pv < alpha)[0]
    sig = np.full_like(p_F_obsp, 0, dtype=bool)
    if good_cluster_inds.size > 0:
        idx = [p_cl[i][0].ravel() for i, p in enumerate(clp_pv) if p < alpha]
        idx = np.concatenate(idx)
        sig[idx] = 1

    obs = stat_fun(x[mask_asd], x[~mask_asd])

    return obs, sig