"""
ADOs Calibrated Severity Scores vs Idiosyncrasy
"""

import itertools
from scipy.stats import pearsonr
import numpy as np
import pandas as pd

from brainspace.utils.parcellation import reduce_by_labels

from utils import regress_out, ICN_NAMES


def _compute_net_idio(df_phen, dd, sd, lab_ref):
    """Network-wise idiosyncrasy. """

    dd_net = reduce_by_labels(dd, lab_ref, axis=0)
    dd_net = pd.DataFrame(dd_net, columns=ICN_NAMES)
    dd_net['Average'] = dd.mean(1)

    sd_net = reduce_by_labels(sd, lab_ref, axis=0)
    sd_net = pd.DataFrame(sd_net, columns=ICN_NAMES)
    sd_net['Average'] = sd.mean(1)

    df_ados = pd.concat([sd_net, dd_net], keys=['SD', 'DD'], axis=1)
    for k in ['Age', 'Group', 'Site', 'Sex', 'CSS']:
        df_ados[k] = df_phen[k].to_numpy()

    # Remove subject with no CSS
    mask_na = np.logical_or(~pd.isna(df_ados['CSS']),  df_ados.Group != 'ASD')
    df_ados = df_ados[mask_na].copy()

    return df_ados


def analyze_ados(df_phen, dd, sd, lab_ref):
    """

    Parameters
    ----------
    df_phen:  pd.DataFrame of shape (n_subjects, n_cov)
        Demographics.
    dd: np.ndarray of shape (n_subjects, n_parcels)
        Diffusion distance.
    sd: np.ndarray of shape (n_subjects, n_parcels)
        Surface distance
    lab_ref: np.ndarray of shape (n_parcels,)
        ICN labeling of reference embedding.

    Returns
    -------
    df: pd.DataFrame
        Dataframe with results of relationship between ADOS CSS and `sd`
        and `dd` measures of idiosyncrasy.
    """

    df_ados = _compute_net_idio(df_phen, dd, sd, lab_ref)

    mask_asd = df_ados.Group == 'ASD'
    mask_cn = ~mask_asd

    mets = ['DD', 'SD']
    net_names_test = ['Average', 'DAN', 'DMN', 'SMN', 'VAN']
    mi_col = pd.MultiIndex.from_product([mets, net_names_test])
    df_res = pd.DataFrame(0, index=['pearson', 'pval'], columns=mi_col)
    conf = pd.get_dummies(df_ados[['Age', 'Site', 'Sex']]).to_numpy()

    # ADOS CSS vs idiosyncrasy
    css = df_ados[mask_asd]['CSS'].to_numpy()
    for sc, nn in itertools.product(mets, net_names_test):
        idio = df_ados[(sc, nn)].to_numpy()[:, None]
        idio = regress_out(idio, conf, mask_control=mask_cn).ravel()
        idio = idio[mask_asd]

        r, p = pearsonr(idio, css)
        df_res.loc['pval', (sc, nn)] = p
        df_res.loc['pearson', (sc, nn)] = r

    df_res = df_res.stack(1)
    df_res = df_res.loc['pearson'].applymap(lambda x: f'{x:.3f}') + \
        df_res.loc['pval'].applymap(lambda x: f' ({x:.3f})')

    return df_res
