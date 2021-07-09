"""
Degree and eigenvector centrality measures.
"""

import scipy.sparse as ssp
import numpy as np
import pandas as pd

from utils import regress_out, unravel_symmetric, tfce


def compute_dc(c, thresh=0.2):
    """Compute degree centrality.

    Parameters
    ----------
    c: np.ndarray of shape (n_vertices, n_vertices)
        Connectivity matrix.
    thresh: float, default=0.2
        Threshold. Only consider vertices that exceed this threshold in the
        computation of the degree centrality.

    Returns
    -------
    dc: np.ndarray of shape (n_vertices,)
        Array with number of connections exceeding the threshold for each
        vertex.
    """

    dc = c > thresh
    d = np.diagonal(dc).astype(np.float32)
    dc = np.sum(dc, axis=1).astype(np.float32)
    dc -= d
    dc /= (dc.size - 1)
    return dc


def compute_ec(c, thresh=None, binary=False):
    """Compute eigenvector centrality.

    Parameters
    ----------
    c: np.ndarray of shape (n_vertices, n_vertices)
        Connectivity matrix.
    thresh: float, default=None
        Threshold. Zero-out vertices below this threshold.
    binary: bool, default=False
        Use binary connectivity matrix. Only if threshold is provided.
    Returns
    -------
    dc: np.ndarray of shape (n_vertices,)
        Eigenvector with the largest eigenvalue of the connectivity matrix.
    """

    if thresh is not None:
        c = c.copy()
        if binary:
            c = (c > thresh).astype(np.float32)
        else:
            c[c < thresh] = 0

    _, ec = ssp.linalg.eigsh(c, k=1, which="LM", maxiter=None, tol=0)
    ec = ec.flatten().real
    norm = np.sign(ec.sum()) * np.linalg.norm(ec)
    ec /= norm
    return ec


def _compute_conn_measures(df_phen, con, sd, dd):
    n_subjects = df_phen.shape[0]
    conf = pd.get_dummies(df_phen[['Age', 'Sex', 'Site']]).to_numpy()

    dc, ec = [None] * n_subjects, [None] * n_subjects
    n_rois = int((1 + np.sqrt(1 + 8 * con.shape[-1]))/2)
    for i, c in enumerate(con):
        c = unravel_symmetric(c, n_rois)
        dc[i] = compute_dc(c, thresh=.2)
        ec[i] = compute_ec(c)

    dc = np.vstack(dc)
    dc = regress_out(dc, conf)

    ec = np.vstack(ec)
    ec = regress_out(ec, conf)

    dc_hat, ec_hat = dc.copy(), ec.copy()
    for i in range(n_rois):
        idio = np.column_stack([sd.T[i], dd.T[i]])
        dc_hat[:, i] = regress_out(dc[:, i:i+1], idio).ravel()
        ec_hat[:, i] = regress_out(ec[:, i:i+1], idio).ravel()

    return dc, ec, dc_hat, ec_hat


def analyze_connectivity(df_phen, surf, con, sd, dd, n_perm=100):
    """Analyze connectivity differences between ASD vs TD before and after
    accounting for idiosyncrasy.

    Idiosyncrasy as manifested in `sd` and `dd`.

    Parameters
    ----------
    df_phen: pd.DataFrame of shape (n_subjects, n_cov)
        Demographics.
    surf: BSPolyData
        Cortical surface.
    con: list of ndarray of shape (n_parcels, n_parcels)
    sd: np.ndarray of shape (n_subjects, n_parcels)
        Surface distance.
    dd: np.ndarray of shape (n_subjects, n_parcels)
        Diffusion distance.
    n_perm: int, default=100
        Number of permutations.

    Returns
    -------
    dc_sig: np.ndarray of shape (n_parcels,)
        Array with parcels with significant differences in degree centrality.
    dc_sig_hat: np.ndarray of shape (n_parcels,)
        Array with parcels with significant differences in degree centrality
        after controlling for idiosyncrasy.
    ec_sig: np.ndarray of shape (n_parcels,)
        Array with parcels with significant differences in eigenvector
        centrality.
    ec_sig_hat: np.ndarray of shape (n_parcels,)
        Array with parcels with significant differences in eigenvector
        centrality after controlling for idiosyncrasy.

    """
    dc, ec, dc_hat, ec_hat = _compute_conn_measures(df_phen, con, sd, dd)

    dc_tval, dc_sig = tfce(df_phen, surf, dc, n_perm=n_perm)
    dc_hat_tval, dc_hat_sig = tfce(df_phen, surf, dc_hat, n_perm=n_perm)

    ec_tval, ec_sig = tfce(df_phen, surf, ec, n_perm=n_perm)
    ec_hat_tval, ec_hat_sig = tfce(df_phen, surf, ec_hat, n_perm=n_perm)

    return dc_sig, dc_hat_sig, ec_sig, ec_hat_sig


