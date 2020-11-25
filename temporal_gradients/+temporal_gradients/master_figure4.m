function master_figure4()
package_dir = regexp(mfilename('fullpath'),'.*\+temporal_gradients','match','once');
load(package_dir + "/data/figure_data.mat", ...
    'gm_hcp_discovery', ...
    'surf_lh', ...
    'surf_rh', ...
    'evo_data', ...
    'temporalLobe_msk');

evo_data_tl = structfun(@(x) x(temporalLobe_msk), evo_data, 'uniform', false);
evo_data_tl = [evo_data_tl.HMS, evo_data_tl.exp];

% Basic connectivity figures
figure_dir = [package_dir, '/figures/figure_4/'];
if ~exist(figure_dir, 'dir')
    mkdir(figure_dir)
end

scatter_plots_3d(gm_hcp_discovery,evo_data_tl,[0,4;0,70], figure_dir);
scatter_plots_2d(gm_hcp_discovery,evo_data_tl,[0,4;0,70], figure_dir);
metric_surfaces(evo_data_tl, {surf_lh,surf_rh}, temporalLobe_msk, figure_dir);
end

function scatter_plots_3d(gm,Y,clim,figure_dir)
side = ["left","right"];
type = ["fhi","exp"];
for ii = 1:2
    for jj = 1:size(Y,2)
        if ii == 1
            y = Y(1:end/2,jj);
        else
            y = Y(end/2+1:end,jj);
        end
        temporal_gradients.support.metric_scatter_3d(gm.aligned{ii},y,clim(jj,:), ...
            figure_dir + "/3d_scatter_" + ...
            side{ii} + "_" + type{jj} + ".png")
    end
end
end
function scatter_plots_2d(gm,Y,lim,figure_dir)
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
fake_parcellation = zeros(20000,1);
fake_parcellation(mask) = 1:3428;
obj = plot_hemispheres(Y,surfaces,'labeltext',{{'Functional','Homology Index'},{'Areal', 'Expansion'}},'parcellation',fake_parcellation);
obj.colorlimits([0 4; 0 70]);
obj.colormaps([.7 .7 .7 ;parula]);
set(obj.handles.text,'FontSize',16);
export_fig([figure_dir '/hemispheres.png'],'-m2','-png')
end