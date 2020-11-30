function master_figure4()
% Constructs the subfigures of Figure 4
%
%   MASTER_FIGURE4() constructs the subfigures of Figure 4 of Vos de Wael
%   et al., 2020, bioRxiv. All generated figures are stored in
%   micaopen/temporal_gradients/+temporal_gradients/figures/figure_4/. For
%   details of each sub-figure see the figure-specific local functions. 
%
%   For more details consult our Github page at
%   https://github.com/MICA-MNI/micaopen/tree/master/temporal_gradients.

% Find local directory.
fs = filesep();
package_dir = regexp(mfilename('fullpath'),'.*\+temporal_gradients','match','once');

% Check for existence of the data file.
data_file = package_dir + fs + "data" + fs + "figure_data.mat";
if ~exist(data_file,'file')
    error('Could not find the data file. Please use temporal_gradients.download_data() to download the data file.');
end

% Set up figure directory.
figure_dir = char(package_dir + fs +  "figures" + fs + "figure_4" + fs);
if ~exist(figure_dir, 'dir')
    mkdir(figure_dir)
end

% Load data. 
load(data_file, ...
    'gm_hcp_discovery', ...
    'surf_lh', ...
    'surf_rh', ...
    'evo_data', ...
    'temporalLobe_msk');

evo_data_tl = structfun(@(x) x(temporalLobe_msk), evo_data, 'uniform', false);
evo_data_tl = [evo_data_tl.HMS, evo_data_tl.exp];

scatter_plots_3d(gm_hcp_discovery,evo_data_tl,[0,4;0,70], figure_dir);
scatter_plots_2d(gm_hcp_discovery,evo_data_tl,[0,4;0,70], figure_dir);
metric_surfaces(evo_data_tl, {surf_lh,surf_rh}, temporalLobe_msk, figure_dir);
end

function scatter_plots_3d(gm,Y,clim,figure_dir)
% Builds 3D scatter plots.
%
%   SCATTER_PLOTS_3D(gm,Y,clim,,figure_dir) builds scatter plots of
%   columns of Y (here: functional homology and areal expansion) in 3D
%   gradient space. Color limits are provided in clim. Figures are stored
%   in figure_dir.

side = ["left","right"];
type = ["fhi","exp"];
for ii = 1:2 % hemisphere
    for jj = 1:size(Y,2) % modality
        % Select left/right hemisphere.
        if ii == 1
            y = Y(1:end/2,jj);
        else
            y = Y(end/2+1:end,jj);
        end
        % Plot
        temporal_gradients.support.metric_scatter_3d(gm.aligned{ii},y,clim(jj,:), ...
            figure_dir + "/3d_scatter_" + ...
            side{ii} + "_" + type{jj} + ".png")
    end
end
end


function scatter_plots_2d(gm,Y,lim,figure_dir)
% Builds 2D scatter plots.
%
%   SCATTER_PLOTS_2D(GM,Y,clim,,figure_dir) builds scatter plots of
%   eccentricity versus columns of Y (here: functional homology and areal
%   expansion). Y-axis limits are provided in lim. Figures are stored in
%   figure_dir.

side = ["left","right"];
type = ["fhi","exp"];
label = {'Functional Homology','Areal Expansion'};
import temporal_gradients.support.eccentricity
for ii = 1:2
    for jj = 1:size(Y,2)
        if ii == 1
            y = Y(1:end/2,jj);
        else
            y = Y(end/2+1:end,jj);
        end
        temporal_gradients.support.metric_scatter(eccentricity(gm.aligned{ii}(:,1:3)), ...
            y,[0,5],lim(jj,:),'Eccentricity',label{jj}, true, ...
            figure_dir + "2d_scatter_" + ...
            side{ii} + "_" + type{jj} + ".png")
    end
end
end


function metric_surfaces(Y,surfaces,mask, figure_dir)
% Plots data on surfaces
%
%   METRIC_SURFACES(Y,surfaces,mask,figure_dir) plots the column vectors of
%   Y onto the surfaces. A temporal lobe mask must be provided. Figures are
%   saved in figure_dir.

fake_parcellation = zeros(20000,1);
fake_parcellation(mask) = 1:3428;
obj = plot_hemispheres(Y,surfaces,'labeltext',{{'Functional','Homology Index'},{'Areal', 'Expansion'}},'parcellation',fake_parcellation);
obj.colorlimits([0 4; 0 70]);
obj.colormaps([.7 .7 .7 ;parula]);
set(obj.handles.text,'FontSize',16);
export_fig([figure_dir '/hemispheres.png'],'-m2','-png')
end