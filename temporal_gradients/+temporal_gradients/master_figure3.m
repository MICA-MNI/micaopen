function master_figure3()
% Constructs the subfigures of Figure 3
%
%   MASTER_FIGURE3() constructs the subfigures of Figure 3 of Vos de Wael
%   et al., 2020, bioRxiv. All generated figures are stored in
%   micaopen/temporal_gradients/+temporal_gradients/figures/figure_3/. For
%   details of each sub-figure see the figure-specific local functions. 
%
%   For more details consult our Github page at
%   https://github.com/MICA-MNI/micaopen/tree/master/temporal_gradients.

% Find local directory.
fs = string(filesep());
package_dir = regexp(mfilename('fullpath'),'.*\+temporal_gradients','match','once');

% Check for existence of the data file.
data_file = package_dir + fs + "data" + fs + "figure_data.mat";
if ~exist(data_file,'file')
    error('Could not find the data file. Please use temporal_gradients.download_data() to download the data file.');
end

% Set up figure directory.
figure_dir = char(package_dir + fs +  "figures" + fs + "figure_3" + fs);
if ~exist(figure_dir, 'dir')
    mkdir(figure_dir)
end

% Load data. 
load(data_file, ...
    'gm_hcp_discovery', ...
    'surf_lh', ...
    'surf_rh', ...
    'temporalLobe_msk', ...
    'yeo', ...
    'yeo_tl_predicted', ...
    'kfold_fc_r', ...
    'mics_fc_r', ...
    'repl_fc_r', ...
    'include', ...
    'r', ...
    'r_ho');

% Figures
yeo_figures(gm_hcp_discovery, ...
    temporalLobe_msk(1:end/2), ...
    include.l, ...
    double(yeo(1:end/2)), ...
    yeo_tl_predicted{1}, ...
    surf_lh, ...
    figure_dir);
decision_tree_figures({kfold_fc_r,repl_fc_r,mics_fc_r}, ...
    cat(3,r,r_ho), ...
    {surf_lh,surf_rh}, ...
    temporalLobe_msk, ...
    figure_dir);
end

function yeo_figures(gm, mask, include, canonical, predicted, surface, figure_dir)
% Plots all the yeo sub-figures
%
%   YEO_FIGURES(gm, mask, include, canonical, predicted, surface,
%   figure_dir) makes surface plots of the canonical yeo networks, the
%   predicted yeo networks and a manifold view of the canonical networks.
%   gm is the GradientMaps object of a dataset, mask is a temporal lobe
%   mask, include is a vector containing the overlap between our temporal
%   lobe vertices and those included in the yeo map (there's a slight
%   divergence in midline mask). canonical are the canonical yeo networks,
%   predicted are the predicted yeo networks, surface contains the cortical
%   surfaces and figure_dir is the directory where figures will be stored. 

% Yeo colormap
yeo_cmap = [178.5 178.5 178.5; 
                120 18 134;
                70 130 180;
                0 118 14; 
                196 58 250;
                220 248 164; 
                230 148 34;
                205 62 78]/255;

% Plot the canonical networks.
obj = plot_hemispheres(canonical,surface, ...
    'labeltext','Yeo Networks');
obj.colormaps(yeo_cmap);
obj.colorlimits([0,7])
export_fig([figure_dir, 'yeo_canonical.png'], '-png', '-m2');
close(gcf);

% Plot the predicted networks.
fake_parcellation = zeros(10000,1);
idx = find(mask);
fake_parcellation(idx(include)) = 1:sum(include);
obj = plot_hemispheres(predicted,surface,'parcellation',fake_parcellation, ...
    'labeltext',{{'Predicted', 'Networks'}});
obj.colormaps(yeo_cmap);
obj.colorlimits([0,7])
export_fig([figure_dir, 'yeo_predicted.png'], '-png', '-m2');
close(gcf);

% Plot the canonical in the manifold. 
import temporal_gradients.support.metric_scatter_3d
metric_scatter_3d(gm.aligned{1}(include,1:3),canonical(idx(include)), [0,7], ...
    [figure_dir, '/yeo_scatter3.png'], yeo_cmap);
end


function decision_tree_figures(subject_level,vertex_level,surfaces, temporalLobe_msk, figure_dir)
% Plots the decision tree sub-figures
%
%   DECISION_TREE_FIGURES(subject_level,vertex_level,surfaces, 
%   temporalLobe_msk, figure_dir) plots the histograms of subject-level
%   correlations for each hemisphere and site as well as surface plots for
%   the vertex level correlatinos. A temporal lobe mask is required.
%   Resulting figures are stored in the figure_dir directory. 

% Subject-level correlations.
h.fig = figure('Color','w','Units','Normalized','Position',[0 0 .7 .7]);
for ii = 1:3
    for hemi = 1:2        
        idx = (hemi-1)*3+ii;
        h.ax(ii,hemi) = subplot(2,3,idx);
        h.hist(ii,hemi) = histogram(subject_level{ii}(:,hemi),10);
        xlabel('Correlation (r)');
    end
end
set(h.ax                                    , ...
    'Box'                   , 'off'         , ...
    'PlotBoxAspectRatio'    , [1,1,1]       , ...
    'FontSize'              , 16            , ...
    'FontName'              , 'DroidSans'   , ...
    'XTick'                 , [0.25, 0.65]   , ...
    'XLim'                  , [0.25, 0.65]   , ...
    'YTick'                 , [0, 20]       , ...
    'YLim'                  , [0, 20]       );
set(h.hist                                  , ...
    'FaceColor'             , [.7 .7 .7]    );
for ii = 1:3
    h.ax(ii,2).Position = h.ax(ii,1).Position + [0 -.5 0 0];
end
export_fig([figure_dir, 'subjectwise_correlations.png'],'-png','-m2')

% Vertexwise correlations
fake_parcellation = zeros(20000,1);
fake_parcellation(temporalLobe_msk) = 1:3428;
plot = reshape(vertex_level,3428,3);
plot(plot<0) = 0.0001; % A bit above 0 otherwise gray will be assigned to these vertices too. 
obj = plot_hemispheres(plot, surfaces, 'parcellation',fake_parcellation, ...
    'labeltext', {{'HCP', 'Discovery'},{'HCP','Replication'},'MICS'});
obj.colormaps([.7 .7 .7; parula(10000)]);
obj.colorlimits([0 .9])
export_fig([figure_dir, 'vertexwise_correlations.png'], '-png', '-m2');

end
