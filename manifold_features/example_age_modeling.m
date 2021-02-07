%% Basic settings
clear;clc; close all

%%% Add path
% BrainSpace: https://github.com/MICA-MNI/BrainSpace/tree/Development
addpath(genpath('/directory/for/brainspace'));

% gifti toolbox: https://www.artefact.tk/software/matlab/gifti
addpath(genpath('/directory/for/gifti'));

ManEccenPath = 'D:\research_tools\test\45.NSPN_longi\0.code\code_eLife\manifold_features';
addpath(genpath(ManEccenPath));


%%% Basic settings
ncompo = 5;         % number of components to generate
ncompo_select = 3;  % number of components to use
NumROI = 200;       % number of ROIs

%%% Load data and surfaces
load(strcat(ManEccenPath,'/data.mat'));
% cortical surface
[surf_ctx_lh, surf_ctx_rh] = load_conte69();
labeling = load_parcellation('schaefer',NumROI);
exp_tmp = ['parc = labeling.schaefer_',int2str(NumROI),';'];
eval(exp_tmp);
% subcortical surface
surf_sctx_lh = SurfStatReadSurf(strcat(ManEccenPath,'/surface/sctx_template_L'));
surf_sctx_rh = SurfStatReadSurf(strcat(ManEccenPath,'/surface/sctx_template_R'));
% colormap
load(strcat(ManEccenPath,'/colormap/coolwhitewarm.mat'));

%% Age modeling (manifold eccentricity)
% ME_ind: individual manifold eccentricity (concatenate two time points)
% contrast: age (concatenate two time points)
% mdl: linear model: 1 + age + sex + site + FD + random(subject) + I

%%% linear mixed effect modeling
slm = SurfStatLinMod(ME_ind, mdl_ManEccen);
slm = SurfStatT(slm, contrast);
pval = 1-tcdf(slm.t, slm.df);
pcor = pval_adjust(pval, 'fdr');
sig_idx = find(pcor < 0.05);
sig_t = zeros(NumROI,1);
sig_t(sig_idx) = slm.t(sig_idx);

%%% Visualize
LT = [];    LT{1} = 'T-statistic';
obj = plot_hemispheres(sig_t, {surf_ctx_lh,surf_ctx_rh}, 'labeltext', LT,'views','lm','parcellation',parc);
obj.colorlimits([0 4]);
cmap = coolwhitewarm; cmap = cmap(1+size(cmap,1)/2:end,:); cmap(1,:) = [181/255 181/255 181/255];
obj.colormaps(cmap)

%% Age modeling (Subcortical-weighted manifold)
% wM_ind: individual subcortical-weighted manifold

%%% linear mixed effect modeling
slm = SurfStatLinMod(wM_ind, mdl_WeightedMan);
slm = SurfStatT(slm, contrast);
pval = 1-tcdf(slm.t, slm.df);
pcor = pval_adjust(pval, 'fdr');
sig_idx = find(pcor < 0.05);
sig_t = zeros(7,1);
sig_t(sig_idx) = slm.t(sig_idx);
sig_t = vertcat(sig_t, sig_t);

%%% reorder subcortical index for visualization
idx_reorder = [7 6 2 5 4 3 1];
idx_reorder = [idx_reorder, idx_reorder];
% order (1~14)
% (1) L-accumbens, (2) L-amygdala, (3) L-caudate, (4) L-hippocampus,
% (5) L-pallidum, (6) L-putamen, (7) L-thalamus,
% (8) R-accumbens, (9) R-amygdala, (10) R-caudate, (11) R-hippocampus,
% (12) R-pallidum, (13) R-putamen, (14) R-thalamus
sig_t_re = sig_t(idx_reorder);

%%% Visualize
cmap = coolwhitewarm; cmap = cmap(1+size(cmap,1)/2:end,:); cmap(1,:) = [181/255 181/255 181/255];
figure('Position',[100 100 700 500]);
[a,cb]=sctxSurfStatViewData(sig_t_re, surf_sctx_lh, surf_sctx_rh, 'T-statistic', 'w');
cb.Limits = [0 4];
cb.Parent.Colormap = cmap;
for i = 1:4
    a(i).CLim = [0 4];
    a(i).ColorOrder = cmap;
end
