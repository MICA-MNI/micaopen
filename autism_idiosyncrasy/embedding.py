"""
Embedding and clustering of connectivity matrices.
"""

import warnings
from scipy import sparse as ssp
from scipy.spatial.distance import cdist
from scipy.sparse.linalg import eigsh
from scipy.sparse.csgraph import connected_components

import numpy as np
import pandas as pd

from joblib import Parallel, delayed

from sklearn import cluster
from sklearn.mixture import GaussianMixture
from sklearn.utils import check_random_state

from brainspace.gradient.utils import dominant_set
from brainspace.gradient.utils import is_symmetric, make_symmetric
from brainspace.utils.parcellation import reduce_by_labels

from utils import unravel_symmetric


def _graph_is_connected(graph):
    return connected_components(graph)[0] == 1


def diffusion_mapping(adj, n_components=10, alpha=0.5, random_state=None):
    """Compute diffusion map of affinity matrix.

    Parameters
    ----------
    adj : ndarray or sparse matrix, shape = (n, n)
        Affinity matrix.
    n_components : int or None, optional
        Number of eigenvectors. If None, selection of `n_components` is based
        on 95% drop-off in eigenvalues. When `n_components` is None,
        the maximum number of eigenvectors is restricted to
        ``n_components <= sqrt(n)``. Default is 10.
    alpha : float, optional
        Anisotropic diffusion parameter, ``0 <= alpha <= 1``. Default is 0.5.
    random_state : int or None, optional
        Random state. Default is None.

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

    rs = check_random_state(random_state)
    use_sparse = ssp.issparse(adj)

    # Make symmetric
    if not is_symmetric(adj, tol=1E-10):
        warnings.warn('Affinity is not symmetric. Making symmetric.')
        adj = make_symmetric(adj, check=False, copy=True, sparse_format='coo')
    else:  # Copy anyways because we will be working on the matrix
        adj = adj.tocoo(copy=True) if use_sparse else adj.copy()

    # Check connected
    if not _graph_is_connected(adj):
        warnings.warn('Graph is not fully connected.')

    ###########################################################
    # Step 2
    ###########################################################
    # When α=0, you get back the diffusion map based on the random walk-style
    # diffusion operator (and Laplacian Eigenmaps). For α=1, the diffusion
    # operator approximates the Laplace-Beltrami operator and for α=0.5,
    # you get Fokker-Planck diffusion. The anisotropic diffusion
    # parameter: \alpha \in \[0, 1\]
    # W(α) = D^{−1/\alpha} W D^{−1/\alpha}
    if alpha > 0:
        if use_sparse:
            d = np.power(adj.sum(axis=1).A1, -alpha)
            adj.data *= d[adj.row]
            adj.data *= d[adj.col]
        else:
            d = adj.sum(axis=1, keepdims=True)
            d = np.power(d, -alpha)
            adj *= d.T
            adj *= d

    ###########################################################
    # Step 3
    ###########################################################
    # Diffusion operator
    # P(α) = D(α)^{−1}W(α)
    if use_sparse:
        d_alpha = np.power(adj.sum(axis=1).A1, -1)
        adj.data *= d_alpha[adj.row]
        adj.data *= d_alpha[adj.col]
    else:
        d = np.power(adj.sum(axis=1, keepdims=True), -.5)
        d2 = np.power(adj.sum(axis=0, keepdims=True), -.5)
        adj *= d
        adj *= d2

    ###########################################################
    # Step 4
    ###########################################################
    # For repeatability of results
    v0 = rs.uniform(-1, 1, adj.shape[0])

    # Find largest eigenvalues and eigenvectors
    w, v = eigsh(adj, k=n_components + 1, which='LM', tol=0, v0=v0)

    # Sort descending
    w, v = w[::-1], v[:, ::-1]
    v *= np.sign(v[np.abs(v).argmax(axis=0), range(v.shape[1])])
    return v, w


class LabelGaussianMixture(GaussianMixture):
    """GMM adapted from scikit-learn. Added support for initialization
    with labeling or probabilities.

    init_params : ndarray or {'kmeans', 'random'}, defaults to 'kmeans'.
        The method used to initialize the weights, the means and the
        precisions.
        Must be one of::

            'kmeans' : responsibilities are initialized using kmeans.
            'random' : responsibilities are initialized randomly.
            ndarray : responsibilities are initialized based on the array of
               labels (n_samples,) or probabilities (n_samples, n_components).

    """

    def _initialize_parameters(self, X, random_state):
        """Initialize the model parameters.
        Parameters
        ----------
        X : array-like, shape  (n_samples, n_features)
        random_state : RandomState
            A random number generator instance.
        """

        n_samples, _ = X.shape

        # Array of labels (n_samples,) with n_components different labels
        # or probabilities (n_samples, n_components)
        if isinstance(self.init_params, np.ndarray):
            if self.init_params.shape == (n_samples,):
                ulab, label = np.unique(self.init_params, return_inverse=True)
                if ulab.size != self.n_components:
                    raise ValueError(f'Wrong number of initial labels. '
                                     f'Expected {self.n_components} labels.')
                resp = np.zeros((n_samples, self.n_components))
                resp[np.arange(n_samples), label] = 1
            elif self.init_params.shape == (n_samples, self.n_components):
                resp = self.init_params
                resp = resp / resp.sum(axis=1, keepdims=True)  # just in case
            else:
                raise ValueError("Wrong shape of initial params: "
                                 "{0}".format(self.init_params.shape))

        elif self.init_params == 'kmeans':
            resp = np.zeros((n_samples, self.n_components))
            label = cluster.KMeans(n_clusters=self.n_components, n_init=1,
                                   random_state=random_state).fit(X).labels_
            resp[np.arange(n_samples), label] = 1
        elif self.init_params == 'random':
            resp = random_state.rand(n_samples, self.n_components)
            resp /= resp.sum(axis=1)[:, np.newaxis]
        else:
            raise ValueError("Unimplemented initialization method '%s'"
                             % self.init_params)

        self._initialize(X, resp)


def gmm_cluster(x, init_lab, covariance_type='full'):
    """Clustering using GMM initialized with 7 Yeo networks.

    Parameters
    ----------
    x: np.ndarray of shape (n_vertices, n_eigenvectors)
        Embedding.
    init_lab:
        Labeling from 7 Yeo networks.
    covariance_type: str, default='full'
        Covariance type.

    Returns
    -------
    p: np.ndarray of shape (n_vertices, n_networks)
        Cluster probability.
    """

    gmm = LabelGaussianMixture(n_components=7,
                               covariance_type=covariance_type,
                               tol=0.001, reg_covar=1e-06, max_iter=100,
                               n_init=1, init_params=init_lab,
                               weights_init=None, means_init=None,
                               precisions_init=None, random_state=0,
                               warm_start=False, verbose=0,
                               verbose_interval=10)
    return gmm.fit(x).predict_proba(x)


def _embed_one(x, nc=30, keep=0.1, alpha=0.5, dt=1):
    n = int(.5 * (np.sqrt(8 * x.size + 1) - 1.) + 1)
    x = unravel_symmetric(x, n)
    np.fill_diagonal(x, 1)

    x = dominant_set(x, keep, norm=True, as_sparse=False)
    x = np.corrcoef(x)
    x[x < 0] = 0

    evec, lamb = diffusion_mapping(x, n_components=nc, alpha=alpha,
                                   random_state=0)
    evec, lamb = evec[:, 1:].astype(np.float32), lamb[1:].astype(np.float32)
    if dt <= 0:
        grad = evec * (lamb / (1 - lamb))
    else:
        grad = evec * (lamb ** dt)
    return evec, grad, lamb


def _get_prob_icn(schaefer1000_lab, yeo7_lab):
    prob_icn = reduce_by_labels(pd.get_dummies(yeo7_lab), schaefer1000_lab,
                                red_op='mean', dtype=np.float32, axis=1)
    prob_icn /= prob_icn.sum(axis=1, keepdims=True)
    return prob_icn


def generate_embeddings(fc, schaefer_lab, yeo7_lab):
    """Generate embedding and cluster in 7 ICNs.

    Parameters
    ----------
    fc: list of ndarray of shape (n_parcels, n_parcels)
        Functional connectivity matrix.
    schaefer_lab: ndarray of shape (n_vertices,)
        Schaefer parcellation with `n_parcels` parcels.
    yeo7_lab: ndarray of shape (n_vertices,)
        Yeo 7 network parcellation.

    Returns
    -------
    grad_ind: list of ndarray of shape (n_parcels, n_eigenvectors)
        Individual embeddings.
    grad_ref: ndarray of shape (n_parcels, n_eigenvectors)
        Reference embedding.
    prob_ind: list of ndarray of shape (n_parcels, 7)
        ICN probability for individual embeddings.
    prob_ref: ndarray of shape (n_parcels, 7)
        ICN probability for reference embedding.
    lab_ind: list of ndarray of shape (n_parcels,)
        ICN labels for individual embeddings.
    lab_ref: ndarray of shape (n_parcels,)
        ICN labels for reference embedding.
    """

    n_subjects = fc.shape[0]

    # embedding
    kwargs = {'keep': .1, 'alpha': 1, 'nc': 30, 'dt': 1}

    fc_ref = fc.mean(0)
    evec_ref, grad_ref = _embed_one(fc_ref, **kwargs)[:-1]

    grad_ind = [None] * n_subjects
    for i, x in enumerate(fc):
        ev1, grad1 = _embed_one(x, **kwargs)[:-1]
        grad_ind[i] = grad1 @ ev1.T @ evec_ref  # change of basis

    # clustering
    init_prob = _get_prob_icn(schaefer_lab, yeo7_lab)
    prob_ind = Parallel(n_jobs=-1)(
        delayed(gmm_cluster)(si, emb, init_prob)
        for si, emb in enumerate(grad_ind))

    prob_ind = np.stack(prob_ind, 0).astype(np.float32)
    prob_ref = gmm_cluster(1, grad_ref, init_prob).astype(np.float32)

    lab_ind = (prob_ind.argmax(-1) + 1).astype(np.uint8)
    lab_ref = (prob_ref.argmax(-1) + 1).astype(np.uint8)

    return grad_ind, grad_ref, prob_ind, prob_ref, lab_ind, lab_ref


def compute_sd(surf_lh, surf_rh, lab_ref, lab_ind, kind='min'):
    """ Compute surface distance

    Parameters
    ----------
    surf_lh: BSPolyData
        Left hemisphere.
    surf_rh: BSPolyData
        Right hemisphere.
    lab_ref: np.ndarray of shape (n_parcels,)
        ICN labeling of reference embedding.
    lab_ind: list of np.ndarray of shape (n_parcels,)
        ICN labeling of individual embeddings.
    kind: int or {'min'}, default='min'
        Compute minimum distance of percentile `kind` is int.

    Returns
    -------
    sd: np.ndarray of shape (n_subjects, n_parcels)
        Surface distance.
    """

    from overlap import _compute_geodist
    geo_dist = _compute_geodist(surf_lh, surf_rh)
    geo_lh, geo_rh = geo_dist['lh'], geo_dist['rh']

    lab = np.concatenate([surf_lh.PointData['schaefer1000_yeo7'],
                         surf_rh.PointData['schaefer1000_yeo7']])
    nlab = np.unique(lab)[1:].size
    mask_lh = np.zeros(nlab, dtype=np.bool)
    m = surf_lh.PointData['mask'] == 1
    nl = np.unique(surf_lh.PointData['schaefer1000_yeo7'][m]).size
    mask_lh[:nl] = True
    mask_rh = ~mask_lh

    dist = np.zeros_like(lab_ind, dtype=np.float)
    for lab_icn in range(1, 8):
        gt = lab_ref == lab_icn
        gt_lh = gt[mask_lh]
        gt_rh = gt[mask_rh]

        for i, lab1 in enumerate(lab_ind):
            seg = lab1 == lab_icn
            seg_lh = seg[mask_lh]
            seg_rh = seg[mask_rh]

            geo_net_lh = geo_lh[gt_lh][:, seg_lh]
            geo_net_rh = geo_rh[gt_rh][:, seg_rh]

            if kind == 'min':
                dist[i, mask_lh * gt] = geo_net_lh.min(axis=1)
                dist[i, mask_rh * gt] = geo_net_rh.min(axis=1)

            else:  # kind used as percentage (e.g., 5, 10)
                dist[i, mask_lh * gt] = np.percentile(geo_net_lh, kind, axis=1)
                dist[i, mask_rh * gt] = np.percentile(geo_net_rh, kind, axis=1)

    return dist


def compute_dd(lab_ref, lab_ind, grad_ref, grad_ind, kind='min'):
    """Compute diffusion distance

    Parameters
    ----------
    lab_ref: np.ndarray of shape (n_parcels,)
        ICN labeling of reference embedding.
    lab_ind: list of np.ndarray of shape (n_parcels,)
        ICN labeling of individual embeddings.
    grad_ref: ndarray of shape (n_parcels, n_eigenvectors)
        Reference embedding.
    grad_ind: list of ndarray of shape (n_parcels, n_eigenvectors)
        Individual embeddings.
    kind: int or {'min'}, default='min'
        Compute minimum distance of percentile `kind` is int.

    Returns
    -------
    dd: np.ndarray of shape (n_subjects, n_parcels)
        Diffusion distance.
    """

    dist = np.zeros_like(lab_ind, dtype=np.float)

    for lab_icn in range(1, 8):
        gt = lab_ref == lab_icn

        for j, lab in enumerate(lab_ind):
            seg = lab == lab_icn
            d = cdist(grad_ref[gt], grad_ind[j][seg], metric='sqeuclidean')

            if kind == 'min':
                dist[j, gt] = d.min(axis=1)
            else:
                dist[j, gt] = np.percentile(d, kind, axis=1)

    return dist
