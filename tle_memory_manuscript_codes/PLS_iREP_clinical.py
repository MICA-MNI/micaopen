# housekeeping____________________________________________________________________________________________________________________________________________
import random
import warnings
import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt

from numpy.typing import NDArray
from scipy.stats import norm, pearsonr, zmap
from pyls.types.behavioral import BehavioralPLS
from statsmodels.stats.multitest import fdrcorrection
from pyls.compute import procrustes, svd, varexp, xcorr
warnings.filterwarnings(action='ignore')

# load, reformat, and reorganize data_____________________________________________________________________________________________________________________
data = pd.read_csv('PLS_data.csv')
data = data.drop(['L_hipVol', 'R_hipVol', 'onsetAge', 'laterality', 'Moca_total', 'Epitrack_total_ageCorrected', 'edu_score'], axis=1)
data = data.dropna()

data['Age'] = data['Age'].astype(float)
data['Sex'] = pd.get_dummies(data['Sex'], drop_first=True); data['Group'] = 1 - pd.get_dummies(data['Group'], drop_first=True)
data['Epi_E'] = data['Epi_E'].astype(float); data['Epi_D'] = data['Epi_D'].astype(float)
data['Sem_E'] = data['Sem_E'].astype(float); data['Sem_D'] = data['Sem_D'].astype(float)
data['Spa_E'] = data['Spa_E'].astype(float); data['Spa_D'] = data['Spa_D'].astype(float)

ID = data.loc[:, 'ID'] # just for record
X = stats.zscore(data.loc[:, ['Age', 'Sex', 'Group', 'HU_L_hipVol', 'HU_R_hipVol']])
Y = stats.zscore(data.loc[:, ['Epi_E', 'Epi_D', 'Sem_E', 'Sem_D', 'Spa_E', 'Spa_D']])

# compute & decompose main cross-correlation matrix_______________________________________________________________________________________________________
R = xcorr(X, Y) # x-correlation matrix { matlab: R = (zscore(Y)' * zscore(X)) / (length(X) - 1) }
u, s, v = svd(R) # singular value decomposition of x-correlation matrix { matlab: [v, s, u] =  svd(R, 0) }

# extract statistics______________________________________________________________________________________________________________________________________
Xweights = u # predictor coefficients or saliences
Yweights = v # response coefficients or saliences

Xscores = X.values @ Xweights # latent predictor scores (ie, predictor projections onto latent predictor components)
Yscores = Y.values @ Yweights # latent response scores (ie, response projections onto latent response components)

Xloadings = xcorr(Xscores, X) # x-correlation b/w latent predictors & original predictors
Yloadings = xcorr(Yscores, Y) # x-correlation b/w latent responses & original responses

eigenVals = np.diag(s)
effect_sizes = np.diag(varexp(s)) * 100 # percent-covariance explained by each latent component { matlab: ((eigenVals .^ 2) / sum(eigenVals .^ 2)) * 100 }

# visualize scree plot of effect sizes____________________________________________________________________________________________________________________
x_axis_ticks = range(1, eigenVals.shape[0] + 1)
y_axis_ticks = range(0, 101, 20)
cum_effect_sizes = [effect_sizes[0], np.sum(effect_sizes[0:2]), np.sum(effect_sizes[0:3]), np.sum(effect_sizes[0:4]), np.sum(effect_sizes[0:5])]

for idx in range(1):
    ScreePlot = plt.figure()

    ax = ScreePlot.add_axes([.1, .1, .8, .8])
    ax.plot(x_axis_ticks, cum_effect_sizes, '--', linewidth=1.5, color='black')
    ax.plot(x_axis_ticks, effect_sizes, '-', linewidth=1.5, color='black')
    ax.set_xlabel('LC')
    ax.set_xticks(x_axis_ticks)
    ax.set_ylabel('covariance explained (%)')
    ax.set_yticks(y_axis_ticks)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.legend(['cumulative', 'single'])

    plt.show()

# visualize correlations b/w latent scores for each component_____________________________________________________________________________________________
LV_corr_y_ticks = range(-4, 5, 2)

for component in range(1):
    Lx = Xscores[:, component]
    Ly = Yscores[:, component]
    m, b = np.polyfit(Lx, Ly, 1)
    rho, pval = pearsonr(Lx, Ly)
    r = str(round(rho, 3))
    p = str(round(pval, 3))

    ScratterPlot = plt.figure()

    ax = ScratterPlot.add_axes([.1, .1, .8, .8])
    ax.set_xlabel('clinical composite scores')
    ax.set_xlim([-4, 3])
    ax.set_ylabel('iREP composite scores')
    ax.set_ylim([-5, 4])
    ax.set_yticks(LV_corr_y_ticks)
    ax.scatter(Lx[0:52, ], Ly[0:52, ], marker='o', color='white', edgecolor='black') # HC, change depending on wAcc or Acc
    ax.scatter(Lx[52:72, ], Ly[52:72, ], marker='o', color='gray', edgecolor='black') # TLE, change depending on wAcc or Acc
    ax.plot(Lx, m * Lx + b, color='black', linewidth=1.25)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.legend(['HC', 'TLE'])

    plt.show()

# run permutations to assess significance of latent variables_____________________________________________________________________________________________
numPerm = 5000 # numPerm = len(ID) * (len(ID) - 1)
d_perm = np.zeros((len(eigenVals), numPerm)) # ie, 5 x 5000

for perm in range(numPerm):
    # resample Y (w/o replacement)
    perm_idx = np.array(random.sample(range(len(ID)), len(ID)))
    Yperm = Y.values[perm_idx, :]

    # compute & decompose new R for permuted Y & original X
    Rperm = xcorr(X, Yperm)
    Uperm, Sperm, Vperm = svd(Rperm)

    # realign permuted singular values to the same space as origintal eigen values via procrustes method
    procrustes_perm_mat = v.T @ Vperm
    [n, o, p] = svd(procrustes_perm_mat)
    rotation_perm_mat = n @ p.T

    Uperm_rotated = Uperm @ Sperm @ rotation_perm_mat
    Sperm_rotated = np.sqrt(np.sum(Uperm_rotated**2, axis=0))

    d_perm[:, perm] = Sperm_rotated

perm_P_vals = (np.sum(d_perm > np.vstack(eigenVals), axis=1) + 1) / (numPerm + 1)

# visualize each component's actual singular value against its null distribution__________________________________________________________________________
n_bin = 250
gauss_factor = 17.5 # to increase amplitude of gaussian curve to better fit histogram...somewhat subjective...
gauss_y_ticks = range(0, 81, 20)

for component in range(1):
    vertical_line = eigenVals[component]
    eigVal = str(round(vertical_line, 2))
    perm_sing_values = d_perm[component,:]
    pVal = str(round(perm_P_vals[component], 4))

    PermNullDist = plt.figure()

    ax = PermNullDist.add_axes([.1, .1, .8, .8])
    ax.set_xlabel('eigenvalue distribution')
    ax.set_xlim([0, 1.2])
    ax.set_ylabel('frequency')
    ax.set_ylim([0, 80])
    ax.set_yticks(gauss_y_ticks)

    _, x_spread, _ = ax.hist(perm_sing_values, n_bin, color='black')
    mu_hist, sigma_hist = stats.norm.fit(perm_sing_values)
    gaussian_curve = stats.norm.pdf(x_spread, mu_hist, sigma_hist)

    ax.vlines(vertical_line, 0, 80, colors='black', linestyles='dashdot', linewidth=1.25)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.show()

# run bootstraps to assess reliability of loadings________________________________________________________________________________________________________
numBoot = 5000 # numBoot = len(ID) * (len(ID) - 1)
obs_order = np.array(range(len(ID)))
Xloadings_boot_distribution = np.zeros((X.shape[1], len(eigenVals), numBoot)) # ie, 5 x 5 x 5000
Yloadings_boot_distribution = np.zeros((Y.shape[1], len(eigenVals), numBoot)) # ie, 6 x 5 x 5000

for boot in range(numBoot):
    # resample data (w/ replacement)
    boot_idx = random.choices(obs_order, k=len(obs_order))
    Xboot = X.values[boot_idx, :]
    Yboot = Y.values[boot_idx, :]

    # compute & decompose new R for bootstrapped X & Y
    Rboot = xcorr(Xboot, Yboot)
    Uboot, Sboot, Vboot = svd(Rboot)

    # realign bootstrapped saliences to the same space as original coefficiencts via procrustes method
    procrustes_boot_mat_U = u.T @ Uboot
    [aa, bb, cc] = svd(procrustes_boot_mat_U)
    rotation_boot_mat_U = aa @ cc.T
    Uboot_rotated = Uboot @ rotation_boot_mat_U

    procrustes_boot_mat_V = v.T @ Vboot
    [dd, ee, ff] = svd(procrustes_boot_mat_V)
    rotation_boot_mat_V = dd @ ff.T
    Vboot_rotated = Vboot @ rotation_boot_mat_V

    # compute X & Y bootstrapped scores
    Xweights_boot = Uboot_rotated
    Yweights_boot = Vboot_rotated
    Xscores_boot = Xboot @ Xweights_boot
    Yscores_boot = Yboot @ Yweights_boot

    # compute X & Y bootstrapped loadings and assign to respective distributions
    Xloadings_boot_distribution[:, :, boot] = xcorr(Xscores_boot, Xboot)
    Yloadings_boot_distribution[:, :, boot] = xcorr(Yscores_boot, Yboot)

# compute 95% confidence intervals, standard deviations/errors, and bootstrap ratios for loadings
ci = 95
low = (100 - ci) / 2
high = 100 - low
prc = [low, high]

Xloadings_boot_ci = np.zeros((X.shape[1], len(eigenVals), 2))
Xloadings_boot_ci[:, :, 0], Xloadings_boot_ci[:, :, 1] = np.percentile(Xloadings_boot_distribution, prc, axis=-1)
Yloadings_boot_ci = np.zeros((Y.shape[1], len(eigenVals), 2))
Yloadings_boot_ci[:, :, 0], Yloadings_boot_ci[:, :, 1] = np.percentile(Yloadings_boot_distribution, prc, axis=-1)

Xloadings_boot_SD = np.std(Xloadings_boot_distribution, axis=-1, ddof=1) # note: ddof=1 --> sample SD (as opposed to population SD)
Yloadings_boot_SD = np.std(Yloadings_boot_distribution, axis=-1, ddof=1)

Xloadings_boot_SE = Xloadings_boot_SD / np.sqrt(numBoot)
Yloadings_boot_SE = Yloadings_boot_SD / np.sqrt(numBoot)

X_bsr = Xloadings / Xloadings_boot_SD # note: bootstrap ratios are equivalent to z-scores provided that the bootstrapped loadings are normally distributed
Y_bsr = Yloadings / Yloadings_boot_SD

# determine elements in ci matrices that include 0
X_ci_zero = np.zeros(Xloadings.shape)
Y_ci_zero = np.zeros(Yloadings.shape)

for row in range(X_ci_zero.shape[0]):
    for col in range(X_ci_zero.shape[1]):
        X_ci_zero[row, col] = Xloadings_boot_ci[row, col, 0] <= 0 <= Xloadings_boot_ci[row, col, 1]
for row in range(Y_ci_zero.shape[0]):
    for col in range(Y_ci_zero.shape[1]):
        Y_ci_zero[row, col] = Yloadings_boot_ci[row, col, 0] <= 0 <= Yloadings_boot_ci[row, col, 1]

# extract FDR-corrected p-values for bootstrap ratios
X_pVal = norm.sf(abs(X_bsr))*2 # two-tailed
Y_pVal = norm.sf(abs(Y_bsr))*2

X_pVal_column = X_pVal.reshape(X_pVal.shape[0] * X_pVal.shape[1])
Y_pVal_column = Y_pVal.reshape(Y_pVal.shape[0] * Y_pVal.shape[1])

X_fdr = fdrcorrection(X_pVal_column, alpha=.05)
Y_fdr = fdrcorrection(Y_pVal_column, alpha=.05)

X_fdr_hypothesis = X_fdr[0].reshape(Xloadings.shape)
X_fdr_pVals = X_fdr[1].reshape(Xloadings.shape)

Y_fdr_hypothesis = Y_fdr[0].reshape(Yloadings.shape)
Y_fdr_pVals = Y_fdr[1].reshape(Yloadings.shape)

# visualize loadings w/ standard deviation________________________________________________________________________________________________________________
Ylabels_predictor = list(['age', 'sex', 'group', 'L hipp', 'R hipp', ''])
Ylabels_response = list(['Epi-E', 'Epi-D', 'Sem-E', 'Sem-D', 'Spa-E', 'Spa-D', ''])

for component in range(1):
    # create predictor, response, and compound loading subplots
    Xval_predictor = np.array(range(Xloadings.shape[0]))
    Yval_predictor = Xloadings.values[:, component][::-1]
    mask1_predictor = Yval_predictor < 0
    mask2_predictor = Yval_predictor >= 0

    Xval_response = np.array(range(Yloadings.shape[0]))
    Yval_response = Yloadings.values[:, component][::-1]
    mask1_response = Yval_response < 0
    mask2_response = Yval_response >= 0

    LoadingPlots, (ax1, ax2) = plt.subplots(1, 2)
    LoadingPlots.suptitle('LC' + str(component + 1))

    ax1.barh(Xval_predictor[mask1_predictor], Yval_predictor[mask1_predictor],
             xerr=Xloadings_boot_SD[:, component][::-1][mask1_predictor], capsize=3, color='white', edgecolor='black')
    ax1.barh(Xval_predictor[mask2_predictor], Yval_predictor[mask2_predictor],
             xerr=Xloadings_boot_SD[:, component][::-1][mask2_predictor], capsize=3, color='white', edgecolor='black')
    ax1.set_xlabel('clinical loadings')
    ax1.set_yticklabels(Ylabels_predictor[::-1])
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)

    ax2.barh(Xval_response[mask1_response], Yval_response[mask1_response],
             xerr=Yloadings_boot_SD[:, component][::-1][mask1_response], capsize=3, color='white', edgecolor='black')
    ax2.barh(Xval_response[mask2_response], Yval_response[mask2_response],
             xerr=Yloadings_boot_SD[:, component][::-1][mask2_response], capsize=3, color='white', edgecolor='black')
    ax2.set_xlabel('iREP loadings')
    ax2.set_yticklabels(Ylabels_response[::-1])
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)

    plt.show()

# visualize all z-scores (i.e., bootstrap ratios)_________________________________________________________________________________________________________
all_labels = list(['age', 'sex', 'R hipp', 'L hipp', 'Sem-E', 'Sem-D', 'Spa-E', 'Epi-D', 'Epi-E', 'Spa-D', 'group'])

for component in range(1):
    x_z = X_bsr.values[:, component]
    y_z = Y_bsr.values[:, component]
    sorted_z = np.sort(np.concatenate([x_z, y_z]))[::-1]
    n_yticks = np.array(range(sorted_z.shape[0]))

    ZscoresPlot = plt.figure()
    ax = ZscoresPlot.add_axes([.1, .1, .8, .8])

    ax.set_title('LC' + str(component + 1))
    ax.barh(n_yticks, sorted_z, color='white', edgecolor='black')
    ax.set_xlabel('Z')
    ax.set_yticks(n_yticks)
    ax.set_yticklabels(all_labels[::-1])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.show()
