%% Generate template manifolds
clear;clc; close all

%%% Add path
% BrainSpace: https://github.com/MICA-MNI/BrainSpace/tree/Development
addpath(genpath('/directory/for/brainspace'));

% gifti toolbox: https://www.artefact.tk/software/matlab/gifti
addpath(genpath('/directory/for/gifti'));

ManEccenPath = '/data/mica2/boyong/45.NSPN_longi/0.code/code_eLife/ManEccen';
addpath(genpath(ManEccenPath));


%%% Basic settings
ncompo = 5;         % number of components to generate
ncompo_select = 3;  % number of components to use
NumROI = 200;       % number of ROIs

%%% Load data and surfaces
load('data.mat');
% cortical surface
[surf_lh, surf_rh] = load_conte69();
labeling = load_parcellation('schaefer',NumROI);
exp_tmp = ['parc = labeling.schaefer_',int2str(NumROI),';'];
eval(exp_tmp);
% subcortical surface
surf_L = SurfStatReadSurf(strcat(ManEccenPath,'/surface/sctx_template_L'));
surf_R = SurfStatReadSurf(strcat(ManEccenPath,'/surface/sctx_template_R'));


%%% Generate template gradients
sparsity = 0;
gm_L = GradientMaps('kernel', 'na', 'approach', 'dm', 'alignment', 'pa', 'n_components', ncompo);
gm_L = gm_L.fit(SC_group(1:NumROI/2,1:NumROI/2), 'sparsity', sparsity, 'reference', HCP_gradient_dti.gm(1:NumROI/2,:), 'niterations',500);
gm_R = GradientMaps('kernel', 'na', 'approach', 'dm', 'alignment', 'pa', 'n_components', ncompo);
gm_R = gm_R.fit(SC_group(1+NumROI/2:end,1+NumROI/2:end), 'sparsity', sparsity, 'reference', HCP_gradient_dti.gm(1+NumROI/2:end,:), 'niterations',100);

gm_temp   = [ [gm_L.aligned{1}; gm_R.aligned{1}] ];  % template manifold
gm_lambda = (gm_L.lambda{1} + gm_R.lambda{1})/2;     % eigenvalues

%%% Visualize template gradients
scree_plot(gm_lambda);

LT = cell(1,ncompo_select);
for nc = 1:ncompo_select;  LT{nc} = strcat('E',int2str(nc));  end
obj = plot_hemispheres(gm_temp(:,1:ncompo_select), {surf_lh,surf_rh}, 'labeltext', LT,'views','lm','parcellation',parc);
obj.colorlimits([-0.15, 0.15]);
cmap = viridis; cmap(1,:) = [181/255 181/255 181/255];
obj.colormaps(cmap)
obj.labels('FontSize',10)

%% Calculate manifold eccentricity
ME = ManEccen(gm_temp, gm_ind, 3);

%%% Visualize
LT = []; LT{1} = 'ManEccen';
obj = plot_hemispheres(ME, {surf_lh,surf_rh}, 'labeltext', LT,'views','lm','parcellation',parc);
obj.colorlimits([0, 0.15]);
cmap = viridis; cmap(1,:) = [181/255 181/255 181/255];
obj.colormaps(cmap)
obj.labels('FontSize',10)

%% Subcortical-weighted manifold
% SC_sctx: #ROI(ctx) x #ROI(sctx)
% (1) L-accumbens, (2) L-amygdala, (3) L-caudate, (4) L-hippocampus,
% (5) L-pallidum, (6) L-putamen, (7) L-thalamus,
% (8) R-accumbens, (9) R-amygdala, (10) R-caudate, (11) R-hippocampus,
% (12) R-pallidum, (13) R-putamen, (14) R-thalamus
wM = WeightedMan(SC_sctx, gm_ind, 3);

%%% Visualize
figure('Position',[100 200 700 500]);
[a,cb] = sctxSurfStatViewData(wM, surf_L, surf_R, 'wM', 'w');
cb.Limits = [0 0.15];
cb.Parent.Colormap = viridis;
for i = 1:4
    a(i).CLim = [0 0.15];
    a(i).ColorOrder = viridis;
end
