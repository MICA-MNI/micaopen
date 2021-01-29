function master_figure1()
% Constructs the subfigures of Figure 1
%
%   MASTER_FIGURE1() constructs the subfigures of Figure 1 of Vos de Wael
%   et al., 2020, bioRxiv. All generated figures are stored in
%   micaopen/temporal_gradients/+temporal_gradients/figures/figure_1/. For
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
figure_dir = char(package_dir + fs +  "figures" + fs + "figure_1" + fs); % Make char as export_fig doesn't accept strings.
if ~exist(figure_dir, 'dir')
    mkdir(figure_dir)
end

% Load data. 
load(data_file, ...
    'gm_hcp_discovery', ...
    'connectivity_vector_3829', ...
    'surf_lh', ...
    'surf_rh', ...
    'connectivity_distance', ...
    'degree_centrality', ...
    'c69_20k', ...
    'sc_mask', ...
    'temporalLobe_msk');

% Mask data for visualization
connectivity_vector_3829(~c69_20k.mask) = -inf;

% Grab eccentricity
import temporal_gradients.support.eccentricity
ecc = [eccentricity(gm_hcp_discovery.aligned{1}(:,1:3)); 
       eccentricity(gm_hcp_discovery.aligned{2}(:,1:3))];
pinksequential = [255,247,243
                  253,224,221
                  252,197,192
                  250,159,181
                  247,104,161
                  221,52,151
                  174,1,126
                  122,1,119
                  73,0,106];
cmap = interp1(linspace(0,1,size(pinksequential,1)),pinksequential,linspace(0,1,64))/255;

% Basic Figures
build_connectivity_surface(connectivity_vector_3829,surf_lh,surf_rh, figure_dir);
build_affinity_matrix(sc_mask,temporalLobe_msk,c69_20k.mask,figure_dir);
build_scree_plot(gm_hcp_discovery.lambda{1}, [figure_dir, 'left_scree.png']);
build_gradient_surfaces([gm_hcp_discovery.aligned{1};gm_hcp_discovery.aligned{2}],surf_lh,temporalLobe_msk, figure_dir);
build_graph_scatters(gm_hcp_discovery,{connectivity_distance.hcp_discovery,degree_centrality.hcp_discovery}, ...
    ["Connectivity Distance","Degree Centrality"], figure_dir);
build_graph_scatters_3d(gm_hcp_discovery,{ecc, connectivity_distance.hcp_discovery,degree_centrality.hcp_discovery}, ...
    [0.5, 4; 10,20; 0.5e7,2e7],{cmap, parula,parula},["Eccentricity", "Connectivity Distance","Degree Centrality"], figure_dir);
end

%% Figure builders
function build_connectivity_surface(data_vec, surf_lh, surf_rh, figure_dir)
% Plots left temporal pole connectivity profile.
%
%   BUILD_CONNECTIVITY_SURFACE(data_vec, surf_lh, surf_rh, figure_dir)
%   plots the vector data_vec onto the surfaces surf_lh and surf_rh. The
%   generated figure is stored as  figure_dir/leftPoleConnectivity.png. 

% Create surface plots.
obj = plot_hemispheres(data_vec,{surf_lh,surf_rh});

% Adjust color limits and colormap. 
set(obj.handles.axes,'CLim',[-3.5 4.5]);
obj.handles.cb.Ticks = [-3.5 4.5];
obj.handles.cb.Limits = [-3.5 4.5];
cmap = hot(256);
cmap = cmap(1:220,:);
colormap([cmap;.7 .7 .7]);

% Add a sphere in the seed location. 
coord = surf_lh.coord(:,3829);
for ii = 1:2
    axes(obj.handles.axes(ii)); hold on 
    scatter3(obj.handles.axes(ii),coord(1),coord(2),coord(3),2000,[0 0 0],'.')
end

% Export. 
export_fig([figure_dir, 'leftPoleConnectivity.png'],'-m2','-png');
close(gcf);
end


function build_affinity_matrix(sc,mask_temporal,mask_midline,figure_dir)
% Builds an affinity matrix figure
%
%   BUILD_AFFINITY_MATRIX(sc,mask_temporal,mask_midline,figure_dir) plots
%   an affinity matrix for input matrix sc. Only the rows included in
%   vector mask_midline and columns included in vector mask_temporal are
%   kept.The resulting figure is stored as figure_dir/affinity.png.

% Left hemispheric connectivity
sc_mask = sc(mask_midline,mask_temporal);
sc_left = sc_mask(1:end/2,1:end/2);

% Sparse connectivity
sc_left(sc_left < prctile(sc_left,75)) = 0;

% Affinity matrix
cosine_similarity = 1-squareform(pdist(sc_left','cosine'));

% Build figure
h.fig = figure('color','w');
h.ax = axes();
h.img = imagesc(cosine_similarity);
h.cb = colorbar;
set(h.ax                                , ...
    'Box'               , 'off'         , ...
    'DataAspectRatio'   ,  [1 1 1]      , ...
    'PlotBoxAspectRatio', [1 1 1]       , ...
    'Xtick'             , []            , ...
    'YTick'             , []            , ...
    'Visible'           , 'off'         ); 
set(h.cb                                , ...
    'Position'          , [ .85 .3 .03, .4], ...
    'Ticks'             , [0 1]         , ...
    'FontName'          , 'DroidSans'   , ...
    'FontSize'          , 36            );

% Export
export_fig([figure_dir, 'affinity.png'],'-m2','-png');
close(gcf)
end


function build_scree_plot(lambda,filename)
% Builds a scree plot.
%
%   BUILD_SCREE_PLOT(lambda,name) builds a scree plot from a vector of
%   eigenvalues sorted by size (lambda). The scree plot is stored as the
%   designated filename. Note that filename must be a .png file. 

h = scree_plot(lambda);
set(h.axes,'XTick',[0 40],'YTick',[0 .35], 'FontName', 'DroidSans',  ...
    'XLim', [0, 40], 'YLim', [0, .35], 'FontSize', 38)
set(h.plot,'Marker','.','MarkerSize',25);
export_fig(filename,'-m2','-png');
close(gcf);
end


function build_gradient_surfaces(gradients,surf_lh,temporalLobe_msk,figure_dir)
% Builds surfaces displaying gradients.
%
%   BUILD_GRADIENT_SURFACES(gradients,surf_lh,surf_rh,temporalLobe_msk,
%   figure_dir) plots the column vectors of gradients onto surface surf_lh. 
%   A temporal lobe mask must be provided. The resulting
%   figure is stored as figure_dir/gradients.png. 

% Construct a temporal lobe 'parcellation'.
fake_parcellation = zeros(20000,1);
fake_parcellation(temporalLobe_msk) = 1:3428;

% Plot surfaces.
obj = plot_hemispheres(gradients(1:end/2,1:3),{surf_lh},'LabelText',"Gradient " + (1:3), ...
    'Parcellation',fake_parcellation(1:end/2), 'views', 'lmi');

% Adjust colormap and color limits.
colormap([.7 .7 .7; parula])
lim = [-3.6 3.6; -2.4 2.1; -.7 1.4];
obj.colorlimits(lim);

% Export. 
export_fig([figure_dir, 'gradients.png'],'-m2','-png');
close(gcf);

% Repeat for eccentricity.
import temporal_gradients.support.eccentricity
obj = plot_hemispheres(eccentricity(gradients(1:end/2,1:3)),{surf_lh},'LabelText',"Eccentricity", ...
    'Parcellation',fake_parcellation(1:end/2), 'views', 'lmi');

pinksequential = [255,247,243
                  253,224,221
                  252,197,192
                  250,159,181
                  247,104,161
                  221,52,151
                  174,1,126
                  122,1,119
                  73,0,106];
cmap = interp1(linspace(0,1,size(pinksequential,1)),pinksequential,linspace(0,1,64))/255;
colormap([.7 .7 .7 ; cmap(1:end-10,:)])
lim = [0.5, 4];
obj.colorlimits(lim);
export_fig([figure_dir, 'eccentricity.png'],'-m2','-png');
close(gcf);
end

function build_graph_scatters(GM,data,modality_name, figure_dir)
% Builds 2D scatter plots for connectivity distance and degree centrality.
%
%   BUILD_GRAPH_SCATTERS(GM,data,modality_name,figure_dir) builds scatter
%   plots of eccentricity versus the columns of data (here: connectivity
%   distance and degree centrality). A modality name is provided for file
%   naming. Figures are stored in figure_dir.

hemi_name = ["left", "right"];
import temporal_gradients.support.eccentricity
import temporal_gradients.support.metric_scatter

for hemi = 1:2
    % Get indices for left/right.
    if hemi == 1
        idx = 1:1714;
    else
        idx = 1715:3428;
    end
        for modality = 1:2
            % Get modality specific properties.
            if modality == 1
                ylim = [10 20];
                ylab = 'Connectivity Distance';
            else
                ylim = [0 3.5]*10e6;
                ylab = 'Degree Centrality';
            end
            name = string(figure_dir) + ...
                hemi_name(hemi) + "_" + modality_name(modality) +".png";
            
            % Plot
            metric_scatter(eccentricity(GM.aligned{hemi}(:,1:3)), ...
                           data{modality}(idx), ...
                           [0,5],ylim,'Eccentricity',ylab,true,name);
        end
end
end


function build_graph_scatters_3d(GM,data,clim,cmap,modality_name, figure_dir)
% Builds 3D scatter plots for connectivity distance and degree centrality.
%
%   BUILD_GRAPH_SCATTERS_3D(GM,data,clim,cmap,modality_name,figure_dir)
%   builds scatter plots of columns of data (here: connectivity distance
%   and degree centrality). in 3D gradient space (here: connectivity
%   distance and degree centrality). Color limits and colormap are provided
%   in clim and cmap, respectively. A modality name is provided for file
%   naming. Figures are stored in figure_dir.

hemi_name = ["lh", "rh"];
import temporal_gradients.support.eccentricity
import temporal_gradients.support.metric_scatter_3d

for hemi = 1:2
    % Get indices for left/right.
    if hemi == 1
        idx = 1:1714;
    else
        idx = 1715:3428;
    end
    for modality = 1:numel(data)
        % Get modality specific properties.
        name = figure_dir + ...
            "scatter3d_" + ...
            hemi_name(hemi) + "_" + modality_name(modality) +".png";
        
        % Plot
        metric_scatter_3d(GM.aligned{hemi}, data{modality}(idx), ...
            clim(modality,:),replace(name,'T1w/T2w.png','T1wT2w.png'), cmap{modality});
    end
end
end