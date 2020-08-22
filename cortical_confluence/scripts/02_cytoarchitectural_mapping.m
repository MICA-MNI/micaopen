% 02_cytoarchitectural_mapping.m
% written by Casey Paquola @ MICA, MNI, 2020*

for set_up = 1
    
    %micaopen    = '/path/to/parent/directory/';
    %mainDir     = [micaopen '/CorticalConfluence/'];
    micaopen    = 'C:\Users\cpaq3\Desktop\GitHub\micaopen\';
    mainDir     = 'C:\Users\cpaq3\OneDrive\montreal\6_CorticalConfluence\micaopen\';
    
    % scripts
    addpath(genpath(micaopen)) 
    addpath(genpath(mainDir)) 
    
    % load data
    load([mainDir 'output/hipp_right_coord.mat']);
    load([mainDir 'output/confluent_surface_right.mat']);
    tmp = load([mainDir 'output/MP_right.mat']);
    MP = 1./tmp.array; % inverted so high values are higher cellular density
    
    % colourmaps
    load([mainDir 'dependencies\colorbrewer.mat']);
    
end

for organise_data = 1
    
    % select releveant profiles and smooth within the confluent model
    MP_slim = MP(:,confluence_labels==0);
    MP_slim = SurfStatSmooth(MP_slim, Cslim, 4);
    
    % sort distance from bridghead
    [~, PD_idx] = sort(bridge_dist, 'ascend');
  
end

for run_mpc = 1
   
    % MPC and embedding
    good_vert = ~isnan(mean(MP_slim));
    MP_slimmer = MP_slim;
    MP_slimmer(:,~good_vert) = [];
    MPC = build_mpc(MP_slimmer, []);
    norm_angle_matrix    = connectivity2normangle(MPC,90);
    [embedding, results] = mica_diffusionEmbedding(norm_angle_matrix, 'symmetryMargin', 1e-05);
    save([mainDir '/output/MPC.mat'], 'norm_angle_matrix', 'MPC', 'embedding', 'results', 'good_vert');
  
end

for figure_1 = 1

    f = figure('units','centimeters','outerposition',[0 0 20 20]);
    
    cmap_int    = interp_colormap(colorbrewer.seq.Greys{1,9}/255,23);
    cmap_mpc    = interp_colormap(colorbrewer.seq.YlOrRd{1,9}/255,23);
    cmap_grad   = interp_colormap(colorbrewer.div.Spectral{1,9}/255,23);

    % all profiles
    a(1) = axes('position', [0.01 0.75 0.2 0.2]);
    imagesc(MP_slim(:,PD_idx), [prctile(MP_slim(:),1) prctile(MP_slim(:),99)]);
    axis off
    colormap(a(1), cmap_int)    
  
    % MPC
    a(4) = axes('position', [0.37 0.75 0.2 0.2]);
    [~, PD_idx_slim] = sort(bridge_dist(good_vert), 'ascend'); 
    imagesc(MPC(PD_idx_slim,PD_idx_slim)); axis off
    camroll(45)
    caxis(a(4), [1.7 2.8])
    colormap(a(4), cmap_mpc)
    
    % norm_angle_matrix ordered by principle gradient
    a(5) = axes('position', [0.6 0.75 0.2 0.2]);
    [~, idx] = sort(embedding(:,1));
    colourMatrix = repmat(embedding(idx,1)', [length(embedding),1])';
    colourMatrix(norm_angle_matrix(idx, idx) == 0.5) = median(embedding(:,1));
    imagesc(colourMatrix, [min(embedding(:,1)) max(embedding(:,1))]); axis off
    camroll(45)
    colormap(a(5), cmap_grad)
    
    % variance explained by gradients
    a(6) = axes('position', [0.85 0.75 0.13 0.2]);
    scatter(1:10, results.lambdas(1:10)/sum(results.lambdas), 20, 'k', 'filled');
    
    % show 1st gradient the confluent cortex
    clim = [min(embedding(:,1)) max(embedding(:,1))];
    pos = [-0.05 0.4 0.3 0.3; ...
       0.2 0.48 0 0; ...
       0 0.42 0 0; ...
       0.2 0.38 0.3 0.3];
    toMap = zeros(1,length(Cslim.coord));
    toMap(good_vert) = embedding(:,1);
    ViewConfluence(toMap, Cslim, pos, 1:4, clim, cmap_grad)
    
    % gradient values by subregion
    a(10) =  axes('position', [0.55 0.45 0.15 0.2]);
    boxplot(embedding(:,1), regions(good_vert));
    
    % gradient values by PD
    a(7) =  axes('position', [0.75 0.45 0.2 0.13]);
    xdata = bridge_dist(good_vert)';
    ydata = double(embedding(:,1));
    [y3,~,output] = fit(xdata, ydata,'poly3');
    scatter(bridge_dist(good_vert), embedding(:,1), 2, [0.5 0.5 0.5], 'filled');
    hold on
    xlim([min(bridge_dist) max(bridge_dist)])
    ylim([min(embedding(:,1)) max(embedding(:,1))])
    p = plot(y3);
    legend('off')
    p.LineWidth = 2;
    p.Color = 'k';

    exportfigbo(f, [homeDir 'figures/MPC_confluence.png'], 'png', 10)
   
end


for mp_features = 1
    
    X = [MP_slim(:,good_vert)' ...
        mean(MP_slim(:,good_vert))' std(MP_slim(:,good_vert))' skewness(MP_slim(:,good_vert),1)'];
    y = bridge_dist(good_vert);
    save([homeDir '/output/bigbrain_features.mat'], 'X', 'y')
    
end

