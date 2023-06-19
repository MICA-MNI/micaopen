# housekeeping____________________________________________________________________________________________________________________________________________
import random
import warnings
import numpy as np
import pandas as pd
import statistics as sts
import scipy.stats as stats
from pyls import base, compute
import matplotlib.pyplot as plt
from scipy.stats import norm, pearsonr
from pyls.types.behavioral import BehavioralPLS
from statsmodels.stats.multitest import fdrcorrection

warnings.filterwarnings(action='ignore')
random.seed(7)

# load, reformat, and reorganize data_____________________________________________________________________________________________________________________
data = pd.read_csv('/Users/shahin/Desktop/Codes/work/PLS_data.csv')
data = data.drop(['onsetAge', 'edu_score', 'Moca_total', 'Epitrack_total_ageCorrected'], axis=1)
data = data.dropna()

# remove subjects who had pre-scan sx (ie, PX006, PX008, PX076)
PX006_idx = data[data.ID == "sub-PX006"].index
PX008_idx = data[data.ID == "sub-PX008"].index
PX076_idx = data[data.ID == "sub-PX076"].index

data = data.drop(PX006_idx)
data = data.drop(PX008_idx)
data = data.drop(PX076_idx)

data['Age'] = data['Age'].astype(float)
data['Sex'] = pd.get_dummies(data['Sex'], drop_first=True) * 1
data['Group'] = 1 - pd.get_dummies(data['Group'], drop_first=True)
data['HU_L_hipVol'] = data['HU_L_hipVol'].astype(float)
data['HU_R_hipVol'] = data['HU_R_hipVol'].astype(float)
data['Epi_E'] = data['Epi_E'].astype(float)
data['Sem_E'] = data['Sem_E'].astype(float)
data['Spa_E'] = data['Spa_E'].astype(float)
data['Epi_D'] = data['Epi_D'].astype(float)
data['Sem_D'] = data['Sem_D'].astype(float)
data['Spa_D'] = data['Spa_D'].astype(float)

# normalize hippocampal volumes wrt HC
laterality = data['laterality']

HC_L_hipVol = data.loc[data['Group'] == 1, ]['HU_L_hipVol']
HC_R_hipVol = data.loc[data['Group'] == 1, ]['HU_R_hipVol']

mean_HC_L_hipVol = np.mean(HC_L_hipVol)
mean_HC_R_hipVol = np.mean(HC_R_hipVol)
std_HC_L_hipVol = np.std(HC_L_hipVol)
std_HC_R_hipVol = np.std(HC_R_hipVol)

zHC_L_hipVol = sts.NormalDist(mean_HC_L_hipVol, std_HC_L_hipVol).zscore(HC_L_hipVol)
zHC_R_hipVol = sts.NormalDist(mean_HC_R_hipVol, std_HC_R_hipVol).zscore(HC_R_hipVol)
zHC_mean_hipVol = (zHC_L_hipVol + zHC_R_hipVol) / 2

LTLE_L_hipVol = data.loc[laterality != 'R', ].loc[data['Group'] == 0, ]['HU_L_hipVol']
RTLE_R_hipVol = data.loc[laterality == 'R', ].loc[data['Group'] == 0, ]['HU_R_hipVol']

zLTLE_L_hipVol = sts.NormalDist(mean_HC_L_hipVol, std_HC_L_hipVol).zscore(LTLE_L_hipVol)
zRTLE_R_hipVol = sts.NormalDist(mean_HC_R_hipVol, std_HC_R_hipVol).zscore(RTLE_R_hipVol)
zTLE_hipVol = zLTLE_L_hipVol.combine_first(zRTLE_R_hipVol)

data['z_hipVol'] = zHC_mean_hipVol.combine_first(zTLE_hipVol)
data['z_hipVol'] = data['z_hipVol'].astype(float)

ID = data.loc[:, 'ID']  # just for record
X = stats.zscore(data.loc[:, ['Age', 'Sex', 'Group', 'z_hipVol']])  # z score X
Y = stats.zscore(data.loc[:, ['Epi_E', 'Epi_D', 'Sem_E', 'Sem_D', 'Spa_E', 'Spa_D']])  # z score Y

# compute & decompose main cross-correlation matrix_______________________________________________________________________________________________________
R = compute.xcorr(X, Y)  # (Y.T @ X) / len(X)
u, s, v = compute.svd(R)  # singular value decomposition of x-correlation matrix { matlab: [v, s, u] =  svd(R, 0) }
bpls = BehavioralPLS(X, Y, n_perm=0, n_boot=0)  # somewhat redundant, but I need s later on and don't know how to extract from bpls

# extract statistics______________________________________________________________________________________________________________________________________
eigenVals = bpls.results.singvals  # estimate of how much covariance each latent component accounts for (np.diag(s))
effect_sizes = bpls.results.varexp * 100  # percent-covariances explained by latent components
cum_effect_sizes = np.cumsum(effect_sizes)

Xweights = bpls.results.x_weights  # u
Yweights = bpls.results.y_weights  # v

Xscores = bpls.results.x_scores  # X.values @ Xweights
Yscores = bpls.results.y_scores  # Y.values @ Yweights

Xloadings = compute.xcorr(Xscores, X)  # (stats.zscore(X).T @ stats.zscore(Xscores)) / len(Xscores)
Yloadings = compute.xcorr(Yscores, Y)  # (stats.zscore(Y).T @ stats.zscore(Yscores)) / len(Yscores)

#compound_loadings = compute.xcorr(Xscores, Y)  # bpls.results.y_loadings <-- not actual y_loadings but "compound" loading

# visualize scree plot of effect sizes____________________________________________________________________________________________________________________
x_axis_ticks = range(1, eigenVals.shape[0] + 1)
y_axis_ticks = range(0, 101, 20)

for index in range(1):
    ScreePlot = plt.figure()

    ax = ScreePlot.add_axes([.1, .1, .8, .8])
    ax.plot(x_axis_ticks, cum_effect_sizes, '--', linewidth=1.5, color='black')
    ax.plot(x_axis_ticks, effect_sizes, '-', linewidth=1.5, color='black')
    ax.set_ylabel('covariance explained (%)')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_xticks(x_axis_ticks)
    ax.set_yticks(y_axis_ticks)
    ax.set_xlabel('LC')

    plt.legend(['cumulative', 'single'])
    plt.show()

# run permutations to assess significance of singular values______________________________________________________________________________________________
n_perm = 5000
d_perm = np.zeros((len(eigenVals), n_perm))
n_HC = np.sum(data['Group'] == 1)
n_TLE = np.sum(data['Group'] == 0)
groups = [n_HC, n_TLE]

perm_idx = base.gen_permsamp(groups=groups, n_cond=1, n_perm=n_perm, seed=bpls.rs)  # generate permutation indices & apply to Y
Y_perm = Y.values[perm_idx]  # apply permutation indices to Y

for perm in range(n_perm):
    # compute & decompose new R for permuted Y & original X
    R_perm = compute.xcorr(X, Y_perm[:, perm])
    u_perm, s_perm, v_perm = compute.svd(R_perm, seed=bpls.rs)

    # apply procrustes alignment on permuted singular value
    s_perm_rot = np.sqrt(np.sum(compute.procrustes(v, v_perm, s_perm)**2, axis=0))

    # save output in permuted singular value array
    d_perm[:, perm] = s_perm_rot

perm_P_vals = compute.perm_sig(s, d_perm)

# visualize correlations b/w latent scores of significant components______________________________________________________________________________________
LV_corr_y_ticks = range(-4, 5, 2)
n_sig_comps = len([i for i in perm_P_vals if i < .05])

for component in range(n_sig_comps):
    Lx = Xscores[:, component]
    Ly = Yscores[:, component]
    m, b = np.polyfit(Lx, Ly, 1)
    rho, _ = pearsonr(Lx, Ly)
    r = str(round(rho, 3))
    p = str(round(perm_P_vals[component], 4))

    ScatterPlot = plt.figure()

    ax = ScatterPlot.add_axes([.1, .1, .8, .8])
    ax.scatter(Lx[data['Group'] == 1, ], Ly[data['Group'] == 1, ], marker='o', color='white', edgecolor='black')
    ax.scatter(Lx[data['Group'] == 0, ], Ly[data['Group'] == 0, ], marker='o', color='gray', edgecolor='black')
    ax.plot(Lx, m * Lx + b, color='black', linewidth=1.25)
    ax.set_xlabel('clinical composite scores')
    ax.text(1, -4, 'r=' + r + ', p=' + p)
    ax.set_ylabel('iREP composite scores')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_yticks(LV_corr_y_ticks)
    ax.set_xlim([-4, 3])
    ax.set_ylim([-5, 4])

    plt.legend(['HC', 'TLE'])
    plt.show()

# visualize each significant component's actual singular value against its null distribution______________________________________________________________
n_bin = 250
gauss_factor = 17.5 # to increase amplitude of gaussian curve to better fit histogram...somewhat subjective...
gauss_y_ticks = range(0, 81, 20)

for component in range(n_sig_comps):
    vertical_line = eigenVals[component]
    eigVal = str(round(vertical_line, 2))
    perm_sing_values = d_perm[component,:]
    pVal = str(round(perm_P_vals[component], 4))

    PermNullDist = plt.figure()

    ax = PermNullDist.add_axes([.1, .1, .8, .8])
    ax.set_xlabel('eigenvalue distribution')
    ax.set_yticks(gauss_y_ticks)
    ax.set_ylabel('frequency')
    ax.set_xlim([0, 1.2])
    ax.set_ylim([0, 80])

    _, x_spread, _ = ax.hist(perm_sing_values, n_bin, color='black')
    mu_hist, sigma_hist = stats.norm.fit(perm_sing_values)
    gaussian_curve = stats.norm.pdf(x_spread, mu_hist, sigma_hist)

    ax.vlines(vertical_line, 0, 80, colors='black', linestyles='dashdot', linewidth=1.25)
    #ax.text(vertical_line + .025, 41.5, 'sv = ' + eigVal)
    #ax.text(vertical_line + .025, 38.5, 'p = ' + pVal)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    plt.show()

# run bootstraps to assess reliability of saliences_______________________________________________________________________________________________________
n_boot = 5000
Xloadings_boot_distribution = np.zeros((X.shape[1], len(eigenVals), n_boot))  # 4 x 4 x 5000
Yloadings_boot_distribution = np.zeros((Y.shape[1], len(eigenVals), n_boot))  # 6 x 4 x 5000
boot_idx = base.gen_bootsamp(groups=groups, n_cond=1, n_boot=n_boot, seed=bpls.rs)  # generate bootstrap indices & apply to data
X_boot = X.values[boot_idx]
Y_boot = Y.values[boot_idx]

u_boot_distribution = np.zeros((X.shape[1], len(eigenVals), n_boot))

for boot in range(n_boot):
    # compute & decompose new R for bootstrapped data
    R_boot = compute.xcorr(X_boot[:, boot], Y_boot[:, boot])
    u_boot, s_boot, v_boot = compute.svd(R_boot, seed=bpls.rs)

    # apply procrustes alignment on bootstrapped X and Y weights
    u_boot_rot = compute.procrustes(u, u_boot, s_boot)
    v_boot_rot = compute.procrustes(v, v_boot, s_boot)

    # save bootstrapped u
    u_boot_distribution[:, :, boot] = u_boot_rot

    # compute bootstrapped latent scores
    Xscores_boot = X_boot[:, boot] @ u_boot_rot
    Yscores_boot = Y_boot[:, boot] @ v_boot_rot

    # compute bootstrapped loadings
    Xloadings_boot = compute.xcorr(Xscores_boot, X_boot[:, boot])
    Yloadings_boot = compute.xcorr(Yscores_boot, Y_boot[:, boot])

    # save bootstrapped loadings in respective arrays
    Xloadings_boot_distribution[:, :, boot] = Xloadings_boot
    Yloadings_boot_distribution[:, :, boot] = Yloadings_boot

# compute 95% confidence intervals, standard deviations, and bootstrap ratios for loadings
ci = 95
low = (100 - ci) / 2
high = 100 - low
prc = [low, high]

Xloadings_boot_ci = np.zeros((X.shape[1], len(eigenVals), 2))
Xloadings_boot_ci[:, :, 0], Xloadings_boot_ci[:, :, 1] = np.percentile(Xloadings_boot_distribution, prc, axis=-1)
Yloadings_boot_ci = np.zeros((Y.shape[1], len(eigenVals), 2))
Yloadings_boot_ci[:, :, 0], Yloadings_boot_ci[:, :, 1] = np.percentile(Yloadings_boot_distribution, prc, axis=-1)

Xloadings_boot_SD = np.std(Xloadings_boot_distribution, axis=-1, ddof=0)  # note: ddof=0 --> population SD (as opposed to sample SD)
Yloadings_boot_SD = np.std(Yloadings_boot_distribution, axis=-1, ddof=0)

#Xloadings_boot_SE = stats.sem(Xloadings_boot_distribution, axis=-1, ddof=1)
#Yloadings_boot_SE = stats.sem(Yloadings_boot_distribution, axis=-1, ddof=1)

X_bsr = Xloadings / Xloadings_boot_SD  # note: we use SD for loadings (ie, correlation coefficients) according to Valeria's papers
Y_bsr = Yloadings / Yloadings_boot_SD

# confirm bsr by using built-in function
Xloadings_boot_sum = np.sum(Xloadings_boot_distribution, axis=-1)
Xloadings_boot_square = np.sum(Xloadings_boot_distribution ** 2, axis=-1)
Yloadings_boot_sum = np.sum(Yloadings_boot_distribution, axis=-1)
Yloadings_boot_square = np.sum(Yloadings_boot_distribution ** 2, axis=-1)

X_bsr2, _ = compute.boot_rel(Xloadings, Xloadings_boot_sum, Xloadings_boot_square, n_boot)
Y_bsr2, _ = compute.boot_rel(Yloadings, Yloadings_boot_sum, Yloadings_boot_square, n_boot)

# confirm u based bsr using manual and built-in output
u_bsr = bpls.results.bootres.x_weights_normed

u_boot_sum = np.sum(u_boot_distribution, axis=-1)
u_boot_square = np.sum(u_boot_distribution ** 2, axis=-1)
u_bsr2, _ = compute.boot_rel(u, u_boot_sum, u_boot_square, n_boot)

u_boot_SD = np.std(u_boot_distribution, axis=-1, ddof=1)
u_bsr3 = u / u_boot_SD

# visualize loadings w/ CIs_______________________________________________________________________________________________________________________________
Ylabels_predictor = list(['age', 'sex', 'group', 'z-hipp'])
Ylabels_response = list(['Epi-E', 'Epi-D', 'Sem-E', 'Sem-D', 'Spa-E', 'Spa-D', ''])

for component in range(n_sig_comps):
    # create predictor, response, and compound loading subplots
    Xval_predictor = np.array(range(Xloadings.shape[0]))
    Yval_predictor = Xloadings.values[:, component][::-1]
    mask1_predictor = Yval_predictor < 0
    mask2_predictor = Yval_predictor >= 0

    Xval_response = np.array(range(Yloadings.shape[0]))
    Yval_response = Yloadings.values[:, component][::-1]
    mask3_response = Yval_response < 0
    mask4_response = Yval_response >= 0

    LoadingPlots, (ax1, ax2) = plt.subplots(1, 2)
    LoadingPlots.suptitle('LV' + str(component + 1))

    ax1.barh(Xval_predictor[mask1_predictor], Yval_predictor[mask1_predictor], color='white', edgecolor='black')
    ax1.barh(Xval_predictor[mask2_predictor], Yval_predictor[mask2_predictor], color='white', edgecolor='black')
    ax1.hlines(3, xmin=Xloadings_boot_ci[0, component, 0], xmax=Xloadings_boot_ci[0, component, 1], linewidth=1, color='k')
    ax1.hlines(2, xmin=Xloadings_boot_ci[1, component, 0], xmax=Xloadings_boot_ci[1, component, 1], linewidth=1, color='k')
    ax1.hlines(1, xmin=Xloadings_boot_ci[2, component, 0], xmax=Xloadings_boot_ci[2, component, 1], linewidth=1, color='k')
    ax1.hlines(0, xmin=Xloadings_boot_ci[3, component, 0], xmax=Xloadings_boot_ci[3, component, 1], linewidth=1, color='k')
    ax1.set_yticks([0, 1, 2, 3])
    ax1.set_yticklabels(Ylabels_predictor[::-1])
    ax1.set_xticks([-1, 0, 1])
    ax1.set_xlim([-1, 1])
    ax1.set_xlabel('clinical loadings')
    ax1.spines['top'].set_visible(False)
    ax1.spines['left'].set_visible(False)
    ax1.spines['right'].set_visible(False)

    ax2.barh(Xval_response[mask3_response], Yval_response[mask3_response], color='white', edgecolor='black')
    ax2.barh(Xval_response[mask4_response], Yval_response[mask4_response], color='white', edgecolor='black')
    ax2.hlines(5, xmin=Yloadings_boot_ci[0, component, 0], xmax=Yloadings_boot_ci[0, component, 1], linewidth=1, color='k')
    ax2.hlines(4, xmin=Yloadings_boot_ci[1, component, 0], xmax=Yloadings_boot_ci[1, component, 1], linewidth=1, color='k')
    ax2.hlines(3, xmin=Yloadings_boot_ci[2, component, 0], xmax=Yloadings_boot_ci[2, component, 1], linewidth=1, color='k')
    ax2.hlines(2, xmin=Yloadings_boot_ci[3, component, 0], xmax=Yloadings_boot_ci[3, component, 1], linewidth=1, color='k')
    ax2.hlines(1, xmin=Yloadings_boot_ci[4, component, 0], xmax=Yloadings_boot_ci[4, component, 1], linewidth=1, color='k')
    ax2.hlines(0, xmin=Yloadings_boot_ci[5, component, 0], xmax=Yloadings_boot_ci[5, component, 1], linewidth=1, color='k')
    ax2.set_yticklabels(Ylabels_response[::-1])
    ax2.set_xticks([-1, 0, 1])
    ax2.yaxis.set_label_position('right')
    ax2.yaxis.tick_right()
    ax2.set_xlim([-1, 1])
    ax2.set_xlabel('iREP loadings')
    ax2.spines['top'].set_visible(False)
    ax2.spines['left'].set_visible(False)
    ax2.spines['right'].set_visible(False)

    plt.show()

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

# visualize sorted bootsrapped ratios_____________________________________________________________________________________________________________________
LC1_bsr = {'LC1_bsr': np.concatenate((X_bsr[0], Y_bsr[0]))}
bsr_df = pd.DataFrame(data=LC1_bsr, index=['Age', 'Sex', 'Group', 'z-hipp',
                                           'Epi-E', 'Epi-D', 'Sem-E', 'Sem-D', 'Spa-E', 'Spa-D'])
sorted_bsr = bsr_df.sort_values(by='LC1_bsr')

bar_bsr = plt.figure()

ax = bar_bsr.add_axes([.1, .1, .8, .8])
ax.set_ylabel('bsr')
ax.set_xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
ax.bar(x=range(len(sorted_bsr)), height=list(sorted_bsr.values.flatten()), color='white', edgecolor='black')
ax.set_xticklabels(list(sorted_bsr.index), rotation=45)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.show()