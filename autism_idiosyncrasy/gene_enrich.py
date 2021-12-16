"""
Gene enrichment analysis.
"""

from scipy import stats
import numpy as np
import pandas as pd

import statsmodels.api as sm
from joblib import Parallel, delayed, cpu_count

from brainspace.null_models import SpinPermutations


def _linregress(x, y):
    xd = x - x.mean()
    yd = y - y.mean(0)

    xs = xd @ xd
    slope = xd @ yd
    slope /= xs
    return slope


def _run_one_linregress(x, y):
    mx = ~np.isnan(x)
    x = x[mx]
    y = y[mx]
    return _linregress(x, y)


def _run_chunk_linregress(perms, y):
    n_rep = perms.shape[0]
    rperm = np.zeros((n_rep, y.shape[1]))
    for i in range(n_rep):
        rperm[i] = _run_one_linregress(perms[i], y)

    return rperm


def _check_n_jobs(n_jobs):
    if n_jobs == 0:  # invalid according to joblib's conventions
        raise ValueError("'n_jobs == 0' is not a valid choice.")
    if n_jobs < 0:
        return max(1, cpu_count() - int(n_jobs) + 1)
    return min(n_jobs, cpu_count())


def _get_n_chunks(n_perm, n_jobs):
    if n_jobs >= n_perm:
        c = np.ones(n_jobs, dtype=int)
        c[n_perm:] = 0
    else:
        c = np.full(n_jobs, n_perm//n_jobs, dtype=int)
        c[:n_perm % n_jobs] += 1
    return c


def _get_chunked_pairs(n_perm, n_chunks):
    c = _get_n_chunks(n_perm, n_chunks)
    c = np.insert(np.cumsum(c), 0, 0)
    c = np.c_[c[:-1], c[1:]]
    c = c[:min(n_chunks, n_perm)]
    return c


def _run_parallel_linregress(perms, y, n_jobs=1):
    if n_jobs == 1:
        return _run_chunk_linregress(perms, y)

    n_rep = perms.shape[0]
    n_jobs = _check_n_jobs(n_jobs)
    cpairs = _get_chunked_pairs(n_rep, n_jobs)
    res = Parallel(n_jobs=n_jobs)(
            delayed(_run_chunk_linregress)(perms[i:j], y)
            for cid, (i, j) in enumerate(cpairs))

    rperm = np.vstack(res)
    return rperm


def _ttest_1samp_fast_tval(x, popmean=0):
    n = x.shape[0]
    d = x.mean(0) - popmean
    v = x.var(0, ddof=1)
    denom = np.sqrt(v / n)

    with np.errstate(divide='ignore', invalid='ignore'):
        t = np.divide(d, denom)
    return t


def get_shared_genes(dict_genes):
    common_genes = None
    for k, v in dict_genes.items():
        if common_genes is None:
            common_genes = v.columns
        else:
            common_genes = np.intersect1d(common_genes, v.columns)

    # Only consider common genes
    for k, v in dict_genes.items():
        dict_genes[k] = v[common_genes]

    return dict_genes


def _select_genes_one(dict_genes, name, sphere_lh, sphere_rh, n_perm=100):

    sids = list(dict_genes.keys())
    n_donor = len(sids)
    n_genes = dict_genes[sids[0]].shape[1]

    sph_lh, sph_rh = sphere_lh, sphere_rh
    m_lh, m_rh = sph_lh.PointData['parcel'] > 0, sph_rh.PointData['parcel'] > 0

    sp = SpinPermutations(n_rep=n_perm, random_state=0).fit(sph_lh, sph_rh)

    x_lh, x_rh = sph_lh.PointData[name], sph_rh.PointData[name]
    x = np.r_[x_lh[m_lh], x_rh[m_rh]]

    spins = sp.randomize(x_lh, x_rh)
    perms = np.c_[spins[0][:, m_lh], spins[1][:, m_rh]]

    slopes = []
    perm_slopes = []
    for sid in sids:
        genes = dict_genes[sid]
        y = genes.to_numpy()

        s = [_linregress(x, y1[:, None])[0] for y1 in y.T]
        slopes.append(np.array(s))

        ps = _run_parallel_linregress(perms, y, n_jobs=-1)
        perm_slopes.append(ps)

    slopes = np.array(slopes)
    tp = [stats.ttest_1samp(s1, 0) for s1 in slopes.T]
    tval = np.array([t[0] for t in tp])

    aux = np.empty((n_perm, n_donor, n_genes))
    for j in range(n_perm):
        aux[j] = np.array([perm_slopes[i][j] for i in range(n_donor)])
    perm_slopes = aux

    tval_perm = np.empty((n_perm, n_genes))
    for i in range(perm_slopes.shape[0]):
        tval_perm[i] = _ttest_1samp_fast_tval(perm_slopes[i])

    pval_perm = np.mean(tval >= tval_perm, 0)
    return tval, pval_perm


def select_genes(dict_genes, sphere_lh, sphere_rh, n_perm=100, df_gandal=None):
    """Gene enrichment analysis.

    Parameters
    ----------
    dict_genes: dict of pd.Dataframe
        Dictionary with pd.Dataframe of genes for each donor in the AHBA
        dataset.
    sphere_lh: BSPolyData
        Sphere for left hemisphere.
    sphere_rh: BSPolyData
        Sphere for right hemisphere.
    n_perm: int, default=None
    df_gandal: pd.DataFrame, default=None
        Dataframe with logFC for ASD, SCZ and BD.

    Returns
    -------
    selected_genes: list of str
        Genes with significant spatial overlap with idiosyncrasy measures.
    """

    from abagen.correct import keep_stable_genes

    dict_genes = get_shared_genes(dict_genes)
    genes = list(dict_genes.values())[0].columns

    tval_sd, pval_sd = _select_genes_one(dict_genes, 'SD', sphere_lh,
                                         sphere_rh, n_perm=n_perm)

    tval_dd, pval_dd = _select_genes_one(dict_genes, 'DD', sphere_lh,
                                         sphere_rh, n_perm=n_perm)

    mask_selected = np.logical_and(pval_sd < 0.05, pval_dd < 0.05)
    selected_genes = genes[mask_selected]

    # Only keep stable genes
    stable_genes = keep_stable_genes(list(dict_genes.values()), threshold=.5,
                                     percentile=False, rank=True)[0]

    selected_genes = np.intersect1d(stable_genes.columns, selected_genes)

    if df_gandal is None:
        return selected_genes

    df = pd.DataFrame(np.c_[tval_sd, tval_dd], index=genes,
                      columns=['SD', 'DD'])
    df_gandal.rename(columns={'gene_name': 'gene_symbol'}, inplace=True)
    df = df.merge(df_gandal.set_index('gene_symbol'), on='gene_symbol')

    df_res = pd.DataFrame('', columns=['SD', 'DD'], index=['ASD', 'SCZ', 'BD'])
    for idio in ['SD', 'DD']:
        y = df[[idio]]
        for k in ['ASD', 'SCZ', 'BD']:
            fc = f'{k}.log2FC'
            x = df[[fc, 'percentage_gene_gc_content']]
            x['Constant'] = 1
            rlm_results = sm.RLM(y, x).fit()

            tv, pv = rlm_results.tvalues[0], rlm_results.pvalues[0]
            df_res.loc[k, idio] = f'{tv:.3f} ({pv:.3f})'

    return selected_genes, df_res
