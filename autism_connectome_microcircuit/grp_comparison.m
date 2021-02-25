%% Basic settings
clear;clc; close all

%%% Add path
% BrainSpace: https://github.com/MICA-MNI/BrainSpace/tree/Development
addpath(genpath('/data/mica2/boyong/ETC/toolbox/BrainSpace-Development'));

% gifti toolbox: https://www.artefact.tk/software/matlab/gifti
addpath(genpath('/data/mica2/boyong/ETC/toolbox/gifti-1.6'));

% SurfStat: https://www.math.mcgill.ca/keith/surfstat/
addpath(genpath('/data/mica2/boyong/ETC/toolbox/surfstat'));

ProcPath = '/data/mica2/boyong/43_MFM_ASD/0.code/open_code';
addpath(genpath(ProcPath));
toolboxPath = strcat(ProcPath,'/toolbox');


%%% Basic settings
ncompo = 5;         % number of components to generate
ncompo_select = 3;  % number of components to use
NumROI = 200;       % number of ROIs
NumPerm = 1000;     % number of permutations

%%% Load data and surfaces
load(strcat(ProcPath,'/DC_mean.mat'));
% cortical surface
[surf_ctx_lh, surf_ctx_rh] = load_conte69();
labeling = load_parcellation('schaefer',NumROI);
exp_tmp = ['parc = labeling.schaefer_',int2str(NumROI),';'];
eval(exp_tmp);

%% Generate template gradients
sparsity = 0;
gm_L = GradientMaps('kernel', 'cs', 'approach', 'dm', 'n_components', ncompo);
gm_L = gm_L.fit(DC_mean(1:NumROI/2,1:NumROI/2), 'sparsity', sparsity);
gm_R = GradientMaps('kernel', 'cs', 'approach', 'dm', 'n_components', ncompo);
gm_R = gm_R.fit(DC_mean(1+NumROI/2:end,1+NumROI/2:end), 'sparsity', sparsity);

gm_temp   = [ [gm_L.gradients{1}; gm_R.gradients{1}] ];  % template manifold
gm_lambda = (gm_L.lambda{1} + gm_R.lambda{1})/2;         % eigenvalues

%%% Visualize
% scree plot
scree_plot(gm_lambda);

% gradients
LT = cell(1,ncompo_select);
for nc = 1:ncompo_select;  LT{nc} = strcat('E',int2str(nc));  end
obj = plot_hemispheres(gm_temp(:,1:ncompo_select), {surf_ctx_lh,surf_ctx_rh}, 'labeltext', LT,'views','lm','parcellation',parc);
obj.colorlimits([-5, 5]);
cmap = parula;
obj.colormaps(cmap)
obj.labels('FontSize',10)

% 3D scatter plot & surfaces
colour_coding = colour2gradients3(gm_temp(:,3), -gm_temp(:,2), -gm_temp(:,1));
cmap = colour_coding;
figure('Position',[100 800 600 500]);
for nr = 1:NumROI
    scatter3(gm_temp(nr,1), gm_temp(nr,2), gm_temp(nr,3), 100,...
        'MarkerFaceColor',cmap(nr,:),'MarkerEdgeColor','k');
    hold on;    
end
xlabel('Gradient 1', 'fontsize', 15, 'fontweight', 'bold');
ylabel('Gradient 2', 'fontsize', 15, 'fontweight', 'bold');
zlabel('Gradient 3', 'fontsize', 15, 'fontweight', 'bold');
axis([-8 6 -6 6 -4 4]);
set(gca,'XTick',[-8:7:6]);
set(gca,'YTick',[-6:6:6]);
set(gca,'ZTick',[-4:4:4]);
set(gca,'FontSize',13);

load(strcat(toolboxPath,'/fsaverage.midthickness_mni_32k_fs_LR.mat'));
FS = G;
nonwall = [2:NumROI+1];
colourness_vertices = []; colourness_vertices_smooth =[];
to_colour = zeros(length(unique(parc)),3);
to_colour(nonwall,:) = colour_coding;
for col = 1:3
    colourness_vertices(:,col) = BoSurfStatMakeParcelData(to_colour(:,col), FS, parc);
    colourness_vertices_smooth(:,col) = SurfStatSmooth(colourness_vertices(:,col)', FS, 3);
end
figure('Position',[700 800 600 500]);
colourSurface(colourness_vertices_smooth, FS, [0.61 0.5 0.2 0.2; 0.61 0.33 0.2 0.2; 0.8 0.33 0.2 0.2; 0.8 0.5 0.2 0.2]);

%% Multivariate group comparison
%%% Between-group comparison
% prepare dependent variable
gm_ind = [];    % # of subj x # of ROI x # of gradients (84 x 200 x 3)

% prepare model
Age_term = term(Age);
temp = zeros(NumSubj,2); temp(find(Site == 1),1) = 1; temp(find(Site == 2),2) = 1;
Site_term = term(temp, {'TCD','NYU'});
temp = zeros(NumSubj,2); temp(find(Sex == 1),1) = 1; temp(find(Sex == 2),2) = 1;
Sex_term = term(temp, {'M','F'});
temp = zeros(NumSubj,2); temp(find(Grp == 1),1) = 1; temp(find(Grp == 2),2) = 1;
Grp_term = term(temp, {'ASD','CTL'});

% fit the model
M = 1 + Age_term + Site_term + Sex_term + Grp_term;
slm = SurfStatLinMod(gm_ind, M);

% compare groups
contrast = Grp_term.ASD - Grp_term.CTL;
slm = SurfStatT(slm, contrast);
pval = 1-tcdf(slm.t, slm.df);
pcor = pval_adjust(pval, 'fdr');
sig_idx = find(pcor < 0.05);
sig_t = zeros(NumROI,1);    sig_t(sig_idx) = slm.t(sig_idx);

%%% Visualize
LT = []; LT{1} = 'ASD vs. CTL';
obj = plot_hemispheres(sig_t, {surf_lh,surf_rh}, 'labeltext', LT,'views','lm','parcellation',parc);
obj.colorlimits([0 3.5]);
cmap = inferno; cmap(1,:) = [181/255 181/255 181/255];
obj.colormaps(cmap)
obj.labels('FontSize',10)
