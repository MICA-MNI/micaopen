"""
Analyze ICNs overlap and entropy.
"""
import itertools
from scipy import stats
import numpy as np
import pandas as pd

from statsmodels.formula.api import ols
from statsmodels.stats.multitest import multipletests

from joblib import Parallel, delayed
from sklearn.metrics import f1_score, jaccard_score

from brainspace.mesh import mesh_operations as mop, mesh_elements as me

from utils import regress_out, ICN_NAMES


def _overlap_icn(lab_ref, lab_ind, lab_icn, name_icn, geo_dist):

    geo_lh, geo_rh = geo_dist['lh'], geo_dist['rh']
    nl = geo_lh.shape[0]

    gt = lab_ref == lab_icn
    gt_lh, gt_rh = gt[:nl], gt[nl:]
    n1 = np.count_nonzero(gt)

    n_subjects = lab_ind.shape[0]
    met = ['Dice', 'Jaccard', 'MSD', 'MHD']
    idx_col = pd.MultiIndex.from_product([met, [name_icn]])
    df_net = pd.DataFrame(0, index=range(n_subjects), columns=idx_col)

    for i, lab in enumerate(lab_ind):
        seg = lab == lab_icn
        seg_lh, seg_rh = seg[:nl], seg[nl:]
        n2 = np.count_nonzero(seg)

        df_net.loc[i, ('Dice', name_icn)] = f1_score(gt, seg)
        df_net.loc[i, ('Jaccard', name_icn)] = jaccard_score(gt, seg)

        mf = geo_lh[gt_lh][:, seg_lh].min(axis=1).sum()
        mf += geo_rh[gt_rh][:, seg_rh].min(axis=1).sum()
        mb = geo_lh[gt_lh][:, seg_lh].min(axis=0).sum()
        mb += geo_rh[gt_rh][:, seg_rh].min(axis=0).sum()
        df_net.loc[i, ('MSD', name_icn)] = (mf + mb) / (n1 + n2)
        df_net.loc[i, ('MHD', name_icn)] = max(mf / n1, mb / n2)

    return df_net


def _compute_geodist(surf_lh, surf_rh, parcel_name='schaefer1000_yeo7'):
    import warnings
    warnings.simplefilter('ignore')

    surf_lh = mop.downsample_with_parcellation(surf_lh, parcel_name)
    mask = surf_lh.PointData['parcel'] != 0
    geo_lh = me.get_ring_distance(surf_lh, n_ring=50,
                                  mask=mask).A.astype(np.float32)

    surf_rh = mop.downsample_with_parcellation(surf_rh, parcel_name)
    mask = surf_rh.PointData['parcel'] != 0
    geo_rh = me.get_ring_distance(surf_rh, n_ring=50,
                                  mask=mask).A.astype(np.float32)

    return {'lh': geo_lh, 'rh': geo_rh}


def _compute_overlap(df_phen, lab_ref, lab_ind, surf_lh, surf_rh):

    geo_dist = _compute_geodist(surf_lh, surf_rh)

    df_net_scores = Parallel(n_jobs=-1)(
        delayed(_overlap_icn)(
            lab_ref,
            lab_ind,
            lab_icn + 1,
            name_icn,
            geo_dist)
        for lab_icn, name_icn in enumerate(ICN_NAMES))

    df_net_scores = pd.concat(df_net_scores, axis=1)
    df_net_scores.sort_index(axis=1, level=0, sort_remaining=False)
    for k in df_phen.columns:
        df_net_scores[k] = df_phen[k].values
    df_net_scores.index = df_phen.index.get_level_values('SID')

    w = np.unique(lab_ref, return_counts=True)[1] / lab_ref.size
    for k in ['Dice', 'MSD', 'MHD', 'Jaccard']:
        df_net_scores[k, 'Cortex'] = (df_net_scores[k] * w).sum(1)

    return df_net_scores


def _analyze_icn_size(df_overlap, lab_ind):
    rec = np.vstack([np.unique(l1, return_counts=True)[1] for l1 in lab_ind])

    df_nv = df_overlap.copy()
    df_nv.drop('Cortex', level=1, axis=1)
    df_nv['NVert'] = np.nan
    for i, nn in enumerate(ICN_NAMES):
        df_nv[('NVert', '{0}'.format(nn))] = rec[:, i]

    mask_asd = df_nv['Group'] == 'ASD'
    tvs, pvs = stats.ttest_ind(rec[mask_asd], rec[~mask_asd])
    pvs = multipletests(pvs, alpha=0.05, method='fdr_bh')[1]

    df_pv_nvert = pd.DataFrame(pvs, index=ICN_NAMES, columns=['p'])
    df_pv_nvert['t'] = tvs

    return df_pv_nvert.sort_index()


def analyze_overlap(df_phen, lab_ref, lab_ind, surf_lh, surf_rh):
    """Analyze ICN overlap

    Parameters
    ----------
    df_phen: pd.DataFrame of shape (n_subjects, n_cov)
        Demographics.
    lab_ref: np.ndarray of shape (n_parcels,)
        ICN labeling of reference embedding.
    lab_ind: list of np.ndarray of shape (n_parcels,)
        ICN labeling of individual embeddings.
    surf_lh: BSPolyData
        Cortical surface for left hemisphere.
    surf_rh: BSPolyData
        Cortical surface for right hemisphere.

    Returns
    -------
    df_overlap: pd.DataFrame
        Dataframe with overlap measures for each individual and ICN with the
        reference labeling.
    df_ols: pd.DataFrame
        Dataframe with results on statistical differences between ASD and TD
        in network overlap measures.
    df_icn_size: pd.DataFrame
        DataFrame with results on statistical differences in ICNs size.
    """

    df_overlap = _compute_overlap(df_phen, lab_ref, lab_ind, surf_lh, surf_rh)
    cova = ['Age', 'Site', 'Sex', 'Group']
    met = ['Dice', 'MSD', 'MHD', 'Jaccard']

    formula = 'y ~ {}'.format(' + '.join(cova))
    df_form = df_overlap[cova].copy()

    net_names_ext = list(ICN_NAMES) + ['Cortex']
    mi = pd.MultiIndex.from_product([cova, ['p', 't', 'coef'],
                                     net_names_ext])
    df = pd.DataFrame(0, index=met, columns=mi)

    for k, nn in itertools.product(met, net_names_ext):
        df_form['y'] = df_overlap[(k, nn)].values
        mod = ols(formula=formula, data=df_form).fit()
        for kcov in cova:
            if kcov in mod.pvalues:
                df.loc[k, (kcov, 'p', nn)] = mod.pvalues[kcov]
                df.loc[k, (kcov, 't', nn)] = mod.tvalues[kcov]
                df.loc[k, (kcov, 'coef', nn)] = mod.params[kcov]
            else:
                for kk in mod.pvalues.keys():
                    if kk.startswith(kcov + '['):
                        df.loc[k, (kcov, 'p', nn)] = mod.pvalues[kk]
                        df.loc[k, (kcov, 't', nn)] = mod.tvalues[kk]
                        df.loc[k, (kcov, 'coef', nn)] = mod.params[kk]
                        break

    df.sort_index(level=0, axis=1, inplace=True)
    for k, v in itertools.product(met, cova):
        p = df.loc[k, (v, 'p')].values
        df.loc[k, (v, 'p')] = multipletests(p, alpha=0.05, method='fdr_bh')[1]

    df_icn_size = _analyze_icn_size(df_overlap, lab_ind)
    return df_overlap, df, df_icn_size


def _cohens_d(c0, c1):
    a = (np.mean(c0) - np.mean(c1))
    b = (np.sqrt((np.std(c0) ** 2 + np.std(c1) ** 2) / 2))
    return a/b


def _entropy_cohensd(df_phen, lab_ref, prob_ind):
    mask_asd = df_phen.Group == 'ASD'
    mask_cn = ~mask_asd

    ext_net_names = list(ICN_NAMES) + ['Cortex']
    df = pd.DataFrame(0, index=ext_net_names, columns=['Cohen\'s d'])
    for i, icn_name in enumerate(ext_net_names):
        if i == 7:
            icn_mask = np.ones_like(lab_ref, dtype=bool)
        else:
            icn_mask = lab_ref == i + 1

        ent = stats.entropy(np.mean(prob_ind[:, icn_mask], 1), axis=1)[:, None]
        conf = pd.get_dummies(df_phen[['Age', 'Sex', 'Site']]).values
        ent = regress_out(ent, conf, mask_control=mask_cn).ravel()
        df.loc[icn_name, "Cohen's d"] = _cohens_d(ent[mask_asd], ent[mask_cn])

    return df


def analyze_entropy(df_phen, lab_ref, prob_ind):
    """Compute ICN entropy

    Parameters
    ----------
    df_phen:  pd.DataFrame of shape (n_subjects, n_cov)
        Demographics.
    lab_ref: np.ndarray of shape (n_parcels,)
        ICN labeling of reference embedding.
    prob_ind: list of ndarray of shape (n_parcels, 7)
        ICN probability for individual embeddings.

    Returns
    -------
    cd: pd.DataFrame
        Effect sizes - Cohen's d.
    delta: np.ndarray of shape (n_parcels,)
        Array woth groupwise entropy difference.
    """

    mask_asd = df_phen.Group == 'ASD'
    mask_cn = ~mask_asd
    prob_net_cn = prob_ind[mask_cn].mean(0)
    prob_net_asd = prob_ind[mask_asd].mean(0)

    ent_cn = stats.entropy(prob_net_cn, axis=1)
    ent_asd = stats.entropy(prob_net_asd, axis=1)

    df_ent = _entropy_cohensd(df_phen, lab_ref, prob_ind)
    delta_ent = ent_asd - ent_cn

    return df_ent, delta_ent
