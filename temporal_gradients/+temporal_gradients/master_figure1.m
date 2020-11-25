function master_figure1()
% Load data
package_dir = regexp(mfilename('fullpath'),'.*\+temporal_gradients','match','once');
load(package_dir + "/data/figure_data.mat", ...
    'gm_hcp_discovery', ...
    'connectivity_vector_3829', ...
    'surf_lh', ...
    'surf_rh', ...
    'connectivity_distance', ...
    'node_strength', ...
    'c69_20k', ...
    'sc_mask', ...
    'temporalLobe_msk');

% Mask data for visualization
connectivity_vector_3829(~c69_20k.mask) = -inf;

% Basic connectivity figures
figure_dir = [package_dir, '/figures/figure_1/'];
if ~exist(figure_dir, 'dir')
    mkdir(figure_dir)
end

build_basic_connectivity_surface(connectivity_vector_3829,surf_lh,surf_rh, figure_dir);
build_basic_connectivity_matrix(sc_mask,temporalLobe_msk,c69_20k.mask,figure_dir);
build_affinity_matrix(sc_mask,temporalLobe_msk,c69_20k.mask,figure_dir);
build_scree_plot(gm_hcp_discovery.lambda{1}, [figure_dir, 'left_scree.png']);
build_gradient_surfaces([gm_hcp_discovery.aligned{1};gm_hcp_discovery.aligned{2}],surf_lh,surf_rh,temporalLobe_msk, figure_dir);
build_gradient_in_euclidean(gm_hcp_discovery.aligned{1}(:,1:3),surf_lh,temporalLobe_msk,1, [figure_dir, 'color_left.png']);
build_graph_scatters(gm_hcp_discovery,{connectivity_distance.hcp_discovery,node_strength.hcp_discovery}, ...
    ["Connectivity Distance","Node Strength"], figure_dir);
build_graph_scatters_3d(gm_hcp_discovery,{connectivity_distance.hcp_discovery,node_strength.hcp_discovery}, ...
    [10,20; 0.5e7,2e7],{parula,parula},["Connectivity Distance","Node Strength"], figure_dir);
end

%% Figure builders
function build_basic_connectivity_surface(sc, surf_lh, surf_rh, figure_dir)
obj = plot_hemispheres(sc,{surf_lh,surf_rh});
set(obj.handles.axes,'CLim',[-3.5 4.5]);
obj.handles.cb.Ticks = [-3.5 4.5];
obj.handles.cb.Limits = [-3.5 4.5];
cmap = hot(256);
cmap = cmap(1:220,:);
colormap([cmap;.7 .7 .7]);
coord = surf_lh.coord(:,3829);
for ii = 1:2
    axes(obj.handles.axes(ii)); hold on 
    scatter3(obj.handles.axes(ii),coord(1),coord(2),coord(3),2000,[0 0 0],'.')
end
export_fig([figure_dir, 'leftPoleConnectivity.png'],'-m2','-png');
close(gcf);
end
function build_basic_connectivity_matrix(sc,mask_temporal,mask_midline,figure_dir)
h.fig = figure('units','normalized','position',[0 0 1 1],'Color','w'); 
h.ax = axes;

mat = sc(mask_temporal(1:end/2),mask_midline);
rng(0); mat = mat(randperm(size(mat,1)),:);
h.img = imagesc(mat);

caxis([-3.5 4.5])
axis square equal 
h.ax.Visible = 'off';
h.ax.View = [90 90];
h.ax.DataAspectRatio = [4 1 1];
cmap = hot(256);
cmap = cmap(1:220,:);
colormap([cmap;.7 .7 .7]);
export_fig([figure_dir, 'matrix.png'],'-m2','-png');
close(gcf);
end
function build_affinity_matrix(sc,mask_temporal,mask_midline,figure_dir)

% Left hemispheric connectivity
sc_mask = sc(mask_midline,mask_temporal);
sc_left = sc_mask(1:end/2,1:end/2);

% Sparse connectivity
sc_left(sc_left < prctile(sc_left,75)) = 0;

% Affinity matrix
cosine_similarity = 1-squareform(pdist(sc_left','cosine'));

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
export_fig([figure_dir, 'affinity.png'],'-m2','-png');

end
function build_scree_plot(lambda,name)
h = scree_plot(lambda);
set(h.axes,'XTick',[0 40],'YTick',[0 .35], 'FontName', 'DroidSans',  ...
    'XLim', [0, 40], 'YLim', [0, .35], 'FontSize', 38)
set(h.plot,'Marker','.','MarkerSize',25);
export_fig(name,'-m2','-png');
close(gcf);
end
function build_gradient_surfaces(gradients,surf_lh,surf_rh,temporalLobe_msk,figure_dir)
fake_parcellation = zeros(20000,1);
fake_parcellation(temporalLobe_msk) = 1:3428;
obj = plot_hemispheres(gradients(:,1:3),{surf_lh,surf_rh},'LabelText',"Gradient " + (1:3), ...
    'Parcellation',fake_parcellation);
colormap([.7 .7 .7; parula])
lim = [-3.6 3.6; -2.4 2.1; -.7 1.4];
obj.colorlimits(lim);
export_fig([figure_dir, 'gradients.png'],'-m2','-png');
close(gcf);
end
function build_gradient_in_euclidean(gradients,surf,mask,side,name)
fake_parcellation = zeros(10000,1);
if side == 1
    fake_parcellation(mask(1:end/2)) = 1:sum(mask)/2;
else
    fake_parcellation(mask(end/2+1:end)) = 1:sum(mask)/2;
end
h = gradient_in_euclidean(gradients,surf,fake_parcellation);
set(h.axes_scatter                              , ...
    'XLim'              , [-4 4]                , ...
    'YLim'              , [-4 4]                , ...
    'ZLim'              , [-4 4]                , ...
    'XTick'             , [-4 0 4]              , ...
    'YTick'             , [-4 0 4]              , ...
    'ZTick'             , [-4 0 4]              , ...
    'FontName'          , 'DroidSans'           , ...
    'FontSize'          , 22                    );
set(h.scatter,'SizeData',100);
export_fig(name,'-m2','-png');
close(gcf);
end
function build_graph_scatters(GM,data,modality_name, figure_dir)
hemi_name = ["left", "right"];
import temporal_gradients.support.eccentricity
import temporal_gradients.support.metric_scatter

for hemi = 1:2
    if hemi == 1
        idx = 1:1714;
    else
        idx = 1715:3428;
    end
        for modality = 1:2
            if modality == 1
                ylim = [10 20];
                ylab = 'Connectivity Distance';
            else
                ylim = [0 3.5]*10e6;
                ylab = 'Node Strength';
            end
            name = string(figure_dir) + ...
                hemi_name(hemi) + "_" + modality_name(modality) +".png";
            metric_scatter(eccentricity(GM.aligned{hemi}(:,1:3)), ...
                           data{modality}(idx), ...
                           [0,5],ylim,'Eccentricity',ylab,true,name);
        end
end
end
function build_graph_scatters_3d(GM,data,clim,cmap,modality_name, figure_dir)
hemi_name = ["lh", "rh"];
import temporal_gradients.support.eccentricity
import temporal_gradients.support.metric_scatter_3d

for hemi = 1:2
    if hemi == 1
        idx = 1:1714;
    else
        idx = 1715:3428;
    end
    for modality = 1:numel(data)
        name = figure_dir + ...
            "scatter3d_" + ...
            hemi_name(hemi) + "_" + modality_name(modality) +".png";
        metric_scatter_3d(GM.aligned{hemi}, data{modality}(idx), ...
            clim(modality,:),replace(name,'T1w/T2w.png','T1wT2w.png'), cmap{modality});
    end
end
end