%% a_moment_of_change.m 
%
% written by Casey Paquola
% MICA lab, Montreal Neurological Institute
% October 2018 - July 2019
%

% initiate project 
for init_project = 1
    
    GH          = '/data_/mica1/03_projects/casey/';
    baseDir     = [GH '/micaopen/a_moment_of_change/'];
    outDir      = [baseDir '/output/'];
    mkdir(outDir)
    figDir      = [baseDir '/figures/'];
    mkdir(figDir)
    
    % useful scripts
    addpath(genpath(baseDir))
    addpath(genpath([GH '/micaopen/MPC']))
    addpath([GH '/micaopen/surfstat_addons']) 
    addpath([GH '/micaopen/surfstat_chicago'])
    addpath([GH '/micaopen/diffusion_map_embedding']) 
    
    % colormaps
    addpath([baseDir '/colourmaps/viridis']) 
    c = load([baseDir '/colourmaps/cbrewer/colorbrewer.mat']);
    colorbrewer = c.colorbrewer; 
    inferno     = inferno(); 
    magma       = magma(); 
    plasma      = plasma();
    cmap_mes = flipud([122, 168, 64; 245, 166, 149; 249, 214, 121 ; 96, 130, 172]/255);

    % surface and parcellation
    FS = SurfStatAvSurf({[baseDir '/maps/lh.pial'] [baseDir '/maps/rh.pial']});
    load([baseDir '/maps/mask.mat'],'mask')
    [~, lh_annot_lab, ~] = read_annotation([baseDir '/maps/lh.sjh.annot']);
    [~, rh_annot_lab, ~] = read_annotation([baseDir '/maps/rh.sjh.annot']);
    parc = [lh_annot_lab; rh_annot_lab];
    uparcel = unique(parc);
    
    % data
    load([baseDir 'microstructure_profiles.mat'], 'MP2')
    load([baseDir '/demographics.mat'], 'age', 'sex', 'subj')
    load([baseDir '/thick.mat'])
    load([baseDir '/blurr.mat'])
    
    % atlases
    mes_classes = annot2classes([baseDir '/maps/lh.mesulam.annot'], [baseDir '/maps/rh.mesulam.annot'], 0);
    for node = 1:length(uparcel)
        mes_parc(node) = mode(mes_classes(parc==uparcel(node)));
    end

end

%% FIGURE 1 - Characterisation of intracortical myelin profiles
% correct MT profiles for partial volume effect
for corrections = 1
    corr_pve    = 0; %optional step. Findings were consistent without pve correction
    % optional: surface- and node-wise correction for pve
    if corr_pve == 1
        MP2_corr = zeros(size(MP2));
        for surf = 1:size(MP2,1)
            for node = 1:size(MP2,2)
                CSF = squeeze(csf2(surf, node, :));
                Model = 1 + term(CSF) + random(Subj) + I;
                slm = SurfStatLinMod(squeeze(MP2(surf,node,:)), Model);
                slm = SurfStatT( slm, CSF);
                csf_lin(surf,node) = slm.t;
                MP2_corr(surf,node,:) = (squeeze(MP2(surf,node,:)) - slm.X*slm.coef)';
            end
        end
        MP2 = MP2_corr + mean(MP2, 3); 
    end
end

for Figure1 = 1
    
    % look at the average MT profile
    f = figure;
    plot(mean(mean(MP2,3),2), 1:size(MP2,1)); % note row 1 is adjacent to the wm boundary, row 12 is adjacent to pial
    
    % calculate MT moments
    MTmoments = [];
    MTmoments(:,:,1) = squeeze(mean(MP2,1))';
    MTmoments(:,:,2) = squeeze(std(MP2))';
    MTmoments(:,:,3) = squeeze(skewness(MP2))';
    MTmoments(:,:,4) = squeeze(kurtosis(MP2))';
    
    % Figure 1 (top) - surface projection of group-average MT moments, taken
    % within the baseline cohort
    f = figure('units','centimeters','outerposition',[0 0 30 30]);
    cmap_bl = interp_colormap(colorbrewer.seq.BuPu{1,9}/255, 26);
    MTmoments_bl    = zeros(size(MTmoments,3), size(MTmoments,2));
    MTmoments_stats = zeros(size(MTmoments,3),2);
    for m = 1:4
        
        MTmoments_bl(m,:) = mean(MTmoments(1:end/2,:,m));
        
        MTmoments_stats(m,1) = mean(MTmoments_bl(m,:));
        MTmoments_stats(m,2) = std(MTmoments_bl(m,:));
        
        surface_map = BoSurfStatMakeParcelData(MTmoments_bl(m,:), FS, parc);
        clim = [prctile(mean(MTmoments(1:end/2,:,m)),5) prctile(mean(MTmoments(1:end/2,:,m)),95)]; % set colour limits
        surface_map(~mask) = sum(clim)/2;
        BoSurfStat_calibrate4Views(surface_map, FS, ...
            [-0.15+(m*0.2) 0.86 0.1 0.1; -0.05+(m*0.2) 0.76 0.1 0.1; ...
            -0.15+(m*0.2) 0.76 0.1 0.1; -0.05+(m*0.2) 0.86 0.1 0.1], ...
            1:4, round(clim, 2), cmap_bl)
        hbar = colorbar('horiz', 'Ticks', round(clim, 2), 'FontName', 'Arial');
        hbar.Position = [-0.085+(m*0.2) 0.76 0.07 0.01];
    end
    corr(MTmoments_bl') % cross-correspondence of MT moments, showing unique but related information
    
    exportfig(f, [figDir, '/Figure_1C.png'], 'Format', 'png', 'FontMode', 'fixed',...
              'color', 'cmyk','Resolution',300 );
    
    % export MT moments with atlas assignments for joyplotting in R (Figure1_joyplots.R)
    T = table(mes_parc', MTmoments_bl(1,:)', MTmoments_bl(2,:)', MTmoments_bl(3,:)', MTmoments_bl(4,:)', ...
        'VariableNames', {'mesulam', 'mean', 'sd', 'skewness', 'kurtosis'});
    writetable(T, [outDir, '/MTmoments_bl.csv'])
end


for Figure1A = 1
    
    clear moment_exem
    [moment_exem(1,:,1), moment_exem(1,:,2)] = max(MTmoments_bl');
    [moment_exem(2,:,1), moment_exem(2,:,2)] = min(MTmoments_bl');
    idx = reshape(moment_exem(:,[1 3],2), 1, 4);
    
    f = figure;
    for ii = 1:4
            
        this_MP = mean(MP2(:,idx(ii),1:end/2),3);
        median(this_MP)
        if ii < 3
            this_col = colorbrewer.qual.Set2{1,3}(1,:)/255;
        else
            this_col = colorbrewer.qual.Set2{1,3}(3,:)/255;
        end

        % show greyscale version
        a(ii) = axes('position', [(0.21*ii)-0.2 0.7 0.03 0.2]);
        imagesc(this_MP, [500 1350]); axis off
        colormap(a(ii), flipud(gray))
        
        % show MT profile
        a(ii+5) = axes('position', [(0.21*ii)-0.16 0.7 0.15 0.2]);
        plot(this_MP, 1:12, 'Color', this_col, 'LineWidth', 2);
        set(gca, 'YTickLabel', [])
        set(gca, 'XTickLabel', [])
        ylim([1 12])
        xlim([500 1350])
    end

    exportfig(f, [figDir, '/Figure_1A_profile_exemplars.png'], 'Format', 'png', 'FontMode', 'fixed',...
              'color', 'cmyk','Resolution',300 );

end


% Figure 1B  - roi profiles for each mesulam class
for Figure_1B = 1
  
    rois = {'V1', 'V2', 'BA7', 'BA24'};
    
    % load myelin pictures
    img_MP  =  zeros(1000,4);
    for ii = 1:4
        tmp = imread([figDir 'layers_' rois{ii} '.jpg']);
        img_MP(:,ii) = resample(mean(tmp(:,50:150,1),2), 1000, length(tmp));
    end
    
    % invert
    img_MPi = (img_MP*-1) + 255;
    
    for ii = 1:4

        % smooth profiles
        img_MPs(:,ii) = smooth(img_MPi(:,ii),100);
        
        % calculate moments
        test_moments(1,ii) = mean(img_MPs(:,ii));
        test_moments(2,ii) = std(img_MPs(:,ii));
        test_moments(3,ii) = skewness(img_MPs(:,ii));
        test_moments(4,ii) = kurtosis(img_MPs(:,ii));
        
    end
    
    % select rois and check on the surface
    rois = [12171529; 3482412; 2908416; 16729688]; % v1,  v2 (BA18), SPL (BA7), ACC (BA24)
    uparc = unique(parc);
    roi_surface = zeros(1, length(uparc)); % preinitialise for displaying rois on the surface
    for ii=1:length(rois)
        this_parc = find(uparc == rois(ii));
        roi_surface(this_parc) = ii;
    end
    SurfStatViewData(BoSurfStatMakeParcelData(roi_surface, FS, parc), FS)
    colormap([1,1,1; cmap_mes])
    
    f = figure('units','centimeters','outerposition',[0 0 30 30]);
    for ii = 1:length(rois)
        
        % find parcel number
        this_parc = find(uparc == rois(ii));
        
        % for display rois on the surface
        roi_surface(this_parc) = ii;
        
        % select profiles
        this_MP = MP2(:,this_parc,end/2);
        roi_MP(:,ii) = this_MP;
        this_img = img_MPs(:,ii);

        % show MT profile
        a(ii) = axes('position', [0.19 1-(0.17*ii) 0.08 0.15]);
        plot(this_MP, 1:12, 'Color', cmap_mes(ii,:), 'LineWidth', 1);
        axis off
        ylim([1 12])
        xlim([600 1300])
        
        % show image-based myelin profile
        a(ii) = axes('position', [0.1 1-(0.17*ii) 0.08 0.15]);
        plot(this_img, flip(1:length(this_img)), 'Color', cmap_mes(ii,:), 'LineWidth', 1);
        axis off
        ylim([1 length(this_img)])
        xlim([0 255])
        
        % record moments for each
        roi_moments(:,ii,1) = test_moments(1:4,ii);
        roi_moments(:,ii,2) = MTmoments_bl(:,this_parc);
    end

    exportfig(f, [figDir, '/Figure_1B_profile_rois.png'], 'Format', 'png', 'FontMode', 'fixed',...
              'color', 'cmyk','Resolution',300 );
    
    f = figure;
    for m = 1:4
        
        a(m) = axes('position', [(m*0.25)-0.2 0.8 0.15 0.15]); 
        scatter(1:4, roi_moments(m,:,1), 15, 1:4, 'filled') 
        xlim([0 5])
        colormap(a(m), cmap_mes)
        set(gca, 'FontSize', 5)
        
        a(m) = axes('position', [(m*0.25)-0.2 0.6 0.15 0.15]);
        scatter(1:4, roi_moments(m,:,2), 15, 1:4, 'filled')
        xlim([0 5])
        colormap(a(m), cmap_mes)
        set(gca, 'FontSize', 5)
        
    end
    
    exportfig(f, [figDir, '/Figure_1B_roi_moments.png'], 'Format', 'png', 'FontMode', 'fixed',...
              'color', 'cmyk','Resolution',300 );
    
end

%% BASELINE MPC
for Figure_1d = 1
    
    % create mpc matrix
    MPC_bl = build_mpc(mean(MP2(:,:,1:end/2),3), []);

    % create t-stat gradient
    normAngleMatrix = connectivity2normangle(MPC_bl, 90);
    [embedding, results] = mica_diffusionEmbedding(normAngleMatrix, 'ncomponents', 30, 'symmetryMargin', 1e-05);

    f = figure('units','centimeters','outerposition',[0 0 30 30]);
   
    % MPC ordered by the gradient
    a(3) = axes('position',[0.01 0.79 .16 .16]);
    [~, idx] = sort(embedding(:,1));
    colourMatrix = repmat(embedding(idx,1)', [length(embedding),1])';
    colourMatrix(normAngleMatrix(idx, idx) == 0.5) = min(embedding(:,1)) - 0.1;
    imagesc(colourMatrix, [min(embedding(:,1)) max(embedding(:,1))]);
    set(gca, 'YTickLabel', [])
    set(gca, 'XTickLabel', [])
    colormap(a(3), [1,1,1; inferno])
    camroll(135)
    hbar = colorbar('horiz');
    hbar.Position = [0.04 0.77 0.1 0.01];
    
    % project first gradient onto the cortical surface
    surface_map = BoSurfStatMakeParcelData(embedding(:,1), FS, parc);
    surface_map = surface_map .* mask';
    surface_map = SurfStatSmooth(surface_map, FS, 5);
    BoSurfStat_calibrate4Views(surface_map, FS, ...
        [0.2 0.84 0.12 0.12; 0.32 0.74 0.12 0.12; ...
        0.2 0.74 0.12 0.12; 0.32 0.84 0.12 0.12], ...
        1:4, [min(surface_map) max(surface_map)], inferno)

    % correlation with moments
    a(1) = axes('position', [0.47 0.79 0.16 0.16]);
    scatter(embedding(:,1), MTmoments_bl(1,:), 15, mes_parc, 'filled', ...
        'MarkerEdgeColor', 'k');
    set(gca, 'YTickLabel', [])
    set(gca, 'XTickLabel', [])
    xlim([-0.13 0.13])
    ylim([700 1000])
    colormap(a(1), cmap_mes)
    corr(embedding(:,1), MTmoments_bl(1,:)')
    
    a(2) = axes('position', [0.69 0.79 0.16 0.16]);
    scatter(embedding(:,1), MTmoments_bl(3,:), 15, mes_parc, 'filled', ...
         'MarkerEdgeColor', 'k');
    set(gca, 'YTickLabel', [])
    set(gca, 'XTickLabel', [])
    xlim([-0.13 0.13])
    ylim([-0.6 1.4])
    colormap(a(2), cmap_mes)
    corr(embedding(:,1), MTmoments_bl(3,:)')

    exportfig(f, [figDir, '/Figure_1D.png'], 'Format', 'png', 'FontMode', 'fixed',...
              'color', 'cmyk','Resolution',300 );

end

%% Supplement - regional variation in moments, when controlling for mean
for correction = 1
    
    mean_bl = MTmoments_bl(1,:)';
    moment_reg(1,:) = mean_bl;
    Model = 1 + term(mean_bl);
    for m = 2:4
        clear slm
        slm = SurfStatLinMod(MTmoments_bl(m,:)', Model);
        slm = SurfStatT( slm, mean_bl);
        moment_reg(m,:) = (MTmoments_bl(m,:)' - slm.X*slm.coef) + mean(MTmoments_bl(m,:)); 
        moment_reg_corr(m) = corr(moment_reg(m,:)', MTmoments_bl(m,:)');
    end
    
end

for Figure = 1
        
    f = figure('units','normalized','outerposition',[0 0 1 1]);
    for m = 1:4
        
        surface_map = BoSurfStatMakeParcelData(moment_reg(m,:), FS, parc);
        clim = [prctile(moment_reg(m,:),5) prctile(moment_reg(m,:),95)]; % set colour limits
        surface_map = surface_map .* mask';
        BoSurfStat_calibrate4Views(surface_map, FS, ...
            [-0.2+(m*0.2) 0.86 0.1 0.1; -0.12+(m*0.2) 0.76 0.1 0.1; ...
            -0.2+(m*0.2) 0.76 0.1 0.1; -0.12+(m*0.2) 0.86 0.1 0.1], ...
            1:4, clim, cmap_bl)
        hbar = colorbar('horiz');
        hbar.Position = [-0.145+(m*0.2) 0.76 0.07 0.01];
    end
    
    exportfig(f, [figDir, '/moments_reg_mean.png'], 'Format', 'png', 'FontMode', 'fixed',...
              'color', 'cmyk','Resolution',300 );
 
end

%% FIGURE 2 

% Figure 2C - exemplar profiles for ROIS
for Figure2C = 1
    
    % define age strata
    age_strata = 1 + (age>16) + (age>18) + (age>20) + (age>22) + (age>24);  
    
    f = figure('units','centimeters','outerposition',[0 0 30 30]);
    cmap_line = colorbrewer.seq.YlGn{1,7}(2:7,:)/255;
    for ii = 1:length(rois)
       
        this_roi = find(uparc==rois(ii));

        a(ii) = axes('position', [0.2 0.9-(ii*0.21) 0.15 0.17]);
        % average for age strata
        tmpMP       = mean(squeeze(MP2(:,this_roi,age<16)),2);
        plot(tmpMP, (1:size(MP2,1)), 'LineWidth', 2, 'Color', cmap_line(1,:)); hold on;
        ROImoments(1, 1, ii) = mean(tmpMP);
        ROImoments(2, 1, ii) = std(tmpMP);
        ROImoments(3, 1, ii) = skewness(tmpMP);
        ROImoments(4, 1, ii) = kurtosis(tmpMP);

        tmpMP       = mean(squeeze(MP2(:,this_roi,age>25)),2);
        plot(tmpMP, (1:size(MP2,1)), 'LineWidth', 2, 'Color', cmap_line(5,:)); hold on;
        ROImoments(1, 2, ii) = mean(tmpMP);
        ROImoments(2, 2, ii) = std(tmpMP);
        ROImoments(3, 2, ii) = skewness(tmpMP);
        ROImoments(4, 2, ii) = kurtosis(tmpMP);
        xlim([600 1250])
        ylim([1 size(MP2,1)])
        hold off
        
        for strata = 1:6
            thisMP(:,strata) = mean(squeeze(MP2(:,this_roi,age_strata==strata)),2);
            a(ii+10) = axes('position', [0.4+(strata*0.02) 0.9-(ii*0.21) 0.017 0.17]);
            imagesc(mean(squeeze(MP2(:,this_roi,age_strata==strata)),2)); axis off
            colormap(gray)
        end
    end
    
    exportfig(f, [figDir, '/Figure_2A.png'], 'Format', 'png', 'FontMode', 'fixed',...
              'color', 'cmyk','Resolution',300 );
    
end

% Figure 2B - Age-related changes in intracortical MT profiles
for Figure2B = 1
    
    % set up linear mixed effect model
    Age         = term(age);
    Sex         = term(sex);
    Subj        = term( var2fac (subj) );
    M1          = 1 + Age + Sex + random(Subj) + I;

    % model relationship between age and each MT moment
    age_effects = zeros(size(MTmoments,3), 6);
    for m = 1:4
        
        clear slm
        slm = SurfStatLinMod( MTmoments(:,:,m), M1);
        
        % positive age effect
        slm = SurfStatT( slm, age);
        out_t(m,:) = slm.t;
        tmp = SurfStatQ( slm );
        out_q(m,out_t(m,:)>0) = tmp.Q(out_t(m,:)>0);
        
        fig2b_maps(m,:) = out_t(m,:);
        
        % negative age effect
        slm = SurfStatT( slm, -age);
        tmp = SurfStatQ( slm );
        out_q(m,out_t(m,:)<0) = tmp.Q(out_t(m,:)<0);
        
        % collate effects
        age_effects(m,1) = nnz(out_t(m,:)>0) / size(MTmoments,2); % percentage of cortex with increase
        age_effects(m,2) = nnz((out_t(m,:).*(out_q(m,:)<0.00625))>0)  / size(MTmoments,2); % percentage of cortex with sig increase
        age_effects(m,3) = nnz(out_t(m,:)<0)  / size(MTmoments,2); % percentage of cortex with decrease
        age_effects(m,4) = nnz((out_t(m,:).*(out_q(m,:)<0.00625))<0) / size(MTmoments,2); % percentage of cortex with sig decrease

        % range of effect sizes across the cortex
        tmp         = (out_t(m,:).*(out_q(m,:)<0.00625));
        tmp(tmp==0) = [];
        t_range(m,1)= min(tmp);
        t_range(m,2)= max(tmp);
        
        % rate of change in % 
        eval_max_age = slm.coef(1,:) + (slm.coef(2,:)*max(age));
        eval_min_age = slm.coef(1,:) + (slm.coef(2,:)*min(age));
        rate_change(m,:) = (diff([eval_max_age; eval_min_age]) ./ abs(eval_min_age)) * 100;
        tmp = rate_change(m,:) .* (out_q(m,:)<0.00625);
        tmp(tmp==0) = [];
        rate_change_ci(m,1)= prctile(tmp,2.5);
        rate_change_ci(m,2)= prctile(tmp,97.5);
         
    end
    age_effects(:,5) = min(out_t'); % for range of t-statistics
    age_effects(:,6) = max(out_t');
    csvwrite([outDir 'fig2b_maps.csv'], fig2b_maps)
    
    % model surface-effects
    for ii = 1:size(MP2,1)
        
        clear slm
        slm = SurfStatLinMod( squeeze(MP2(ii,:,:))', M1);
        
        % positive age effect
        slm = SurfStatT( slm, age);
        out_surf_t(ii,:) = slm.t;
        
    end
        
    f = figure('units','centimeters','outerposition',[0 0 30 30]);
    clear t_range
    cmap_tstat = interp_colormap(flipud(colorbrewer.div.RdBu{1,11}/255), 26);    
    for m = 1:4
        
        % project significant effects to cortical surfaces
        % threshold represents Bonferroni correction for four two-sided tests
        surface_map = BoSurfStatMakeParcelData(out_t(m,:).*(out_q(m,:)<0.00625), FS, parc);
        clim        = [-7 7]; % consistent colourmap across surfaces
        BoSurfStat_calibrate4Views(surface_map, FS, ...
            [-0.15+(m*0.2) 0.86 0.1 0.1; -0.05+(m*0.2) 0.76 0.1 0.1; ...
            -0.15+(m*0.2) 0.76 0.1 0.1; -0.05+(m*0.2) 0.86 0.1 0.1], ...
            1:4, clim, cmap_tstat)
        hbar = colorbar('horiz', 'Ticks', clim, 'FontName', 'Arial');
        hbar.Position = [-0.085+(m*0.2) 0.76 0.07 0.01];
                
        % show surface wise changes
        [~, tmp] = sort(out_q(m,:));
        which_nodes = find(out_q(m,:)<0.00625);
        t_range(:,:,m) = [mean(out_surf_t(:,which_nodes),2) - std(out_surf_t(:,which_nodes),[],2)...
            mean(out_surf_t(:,which_nodes),2) ...
            mean(out_surf_t(:,which_nodes),2) + std(out_surf_t(:,which_nodes),[],2)];
        a(m) = axes('position', [(m*0.2)-0.12 0.57 0.07 0.15]);
        for ii = 1:size(MP2,1)
            plot(t_range(ii,1:3,m),[ii ii ii], 'Color', 'k')
            hold on
        end
        scatter(t_range(:,2,m),1:size(MP2,1),20,t_range(:,2,m), 'filled')
        caxis([-7 7])
        colormap(a(m), cmap_tstat)
        ylim([0 size(MP2,1)+1])
        xlim([-10 10])
        
        % show change by age strata for those peaks
        a(m+5)      = axes('position', [(m*0.2)-0.04 0.57 0.1 0.15]);
        tmpMP       = mean(mean(squeeze(MP2(:,which_nodes,age<16)),2),3);
        plot(tmpMP, (1:size(MP2,1)), 'LineWidth', 1, 'Color', cmap_line(1,:)); hold on;
        tmpMP       = mean(mean(squeeze(MP2(:,which_nodes,age>25)),2),3);
        plot(tmpMP, (1:size(MP2,1)), 'LineWidth', 1, 'Color', cmap_line(5,:));
        xlim([600 1250])
        ylim([1 size(MP2,1)])
        set(gca, 'YTickLabel', [])
        hold off

        % baseline and t-stat correlation
        a(m+10) = axes('position', [-0.12+(m*0.2) 0.3 0.15 0.15]);
        scatter(MTmoments_bl(m,:), out_t(m,:), 10, mes_parc, 'filled')
        colormap(a(m+10), [1,1,1; cmap_mes])
    end
     
    exportfig(f, [figDir, '/Figure_2B.png'], 'Format', 'png', 'FontMode', 'fixed',...
              'color', 'cmyk','Resolution',300 );
       
end

% Figure 2C  - Age-related changes across cortical types
for Figure2C = 1
 
    dlmwrite([outDir '/moment_tstats.txt'], [mes_parc' out_t' out_q'])

end

%% Supplement - regional variation and age changes while controlling for thickness or blurring
for correction_and_figure = 1
    
    for t = 1:2
        
        if t == 1
            type='thickness';
            regr=thick2;
        else
            type='blurr';
            regr=blurr2;
        end
        
        % node-wise correction for thickness
        MTmoments_corr = zeros(size(MTmoments));
        for m = 1:4
            for node = 1:size(MTmoments,2)
                R = regr(node, :)';
                Model = 1 + term(R) + random(Subj) + I;
                slm = SurfStatLinMod(MTmoments(:,node,m), Model);
                slm = SurfStatT( slm, R);
                MTmoments_corr(:,node,m) = (MTmoments(:,node,m) - slm.X*slm.coef)';
            end
            MTmoments_corr(:,:,m) = MTmoments_corr(:,:,m) + mean(MTmoments(:,:,m));
        end
        
        f = figure('units','normalized','outerposition',[0 0 1 1]);
        
        for figure_A_regional = 1
            
            for m = 1:4
                
                regr_bl = mean(MTmoments_corr(:,:,m)); 
                regr_bl_corr(m,t) = corr(regr_bl', MTmoments_bl(m,:)');
                surface_map = BoSurfStatMakeParcelData(regr_bl, FS, parc);
                clim = [prctile(regr_bl,5) prctile(regr_bl,95)]; % set colour limits
                surface_map = surface_map .* mask';
                BoSurfStat_calibrate4Views(surface_map, FS, ...
                    [-0.15+(m*0.17) 0.86 0.1 0.1; -0.07+(m*0.17) 0.76 0.1 0.1; ...
                    -0.15+(m*0.17) 0.76 0.1 0.1; -0.07+(m*0.17) 0.86 0.1 0.1], ...
                    1:4, round(clim, 2), viridis)
                hbar = colorbar('horiz', 'Ticks', round(clim, 2));
                hbar.Position = [-0.095+(m*0.17) 0.76 0.07 0.01];
            end % calculate average MT moments for mesulam classes
    class_moment = zeros(size(MTmoments,1), 4, size(MTmoments,3));
    for mes = 1:4
        class_moment(:,mes,:) = mean(MTmoments(:,mes_parc==mes,:),2);
    end
    
    % perform linear mixed effect models for mesulam classes
    for m = 1:4
        slm = SurfStatLinMod( class_moment(:,:,m), M1);
        % positive age effect
        slm = SurfStatT( slm, age);
        mes_out_t(m,:) = slm.t;
        tmp = SurfStatQ( slm );
        mes_out_q(m,mes_out_t(m,:)>0) = tmp.Q(mes_out_t(m,:)>0);
        % negative age effect
        slm = SurfStatT( slm, -age);
        tmp = SurfStatQ( slm );
        mes_out_q(m,mes_out_t(m,:)<0) = tmp.Q(mes_out_t(m,:)<0);        
    end
            
        end
        
        for figure_B_baseline_corr = 1

                age_to_term = age(1:end/2);
                sex_to_term = double(sex(1:end/2));

                out_t = zeros(size(MPmoments,3), size(MPmoments,2));
                for ii = 1:size(MPmoments,2)
                    
                    regr_to_term = regr(ii,1:end/2)';
                    
                    M2 = 1 + term(age_to_term) + term(sex_to_term) + term(regr_to_term);
                    
                    slm = SurfStatLinMod(squeeze(MPmoments(1:end/2, ii, :)), M2);
                    slm = SurfStatT( slm, regr_to_term );
                    out_t(:,ii) = slm.t;

                end
    
            
            cmap_corr = interp_colormap(flipud(colorbrewer.div.RdBu{1,11}/255), 26);
            for m = 1:4
                
                % project significant effects to cortical surfaces
                % threshold represents Bonferroni correction for four two-sided tests
                surface_map = BoSurfStatMakeParcelData(out_t(m,:), FS, parc);
                surface_map = surface_map .* mask';
                clim        = [-5 5]; % consistent colourmap across surfaces
                
                BoSurfStat_calibrate4Views(surface_map, FS, ...
                    [-0.15+(m*0.17) 0.56 0.1 0.1; -0.07+(m*0.17) 0.46 0.1 0.1; ...
                    -0.15+(m*0.17) 0.46 0.1 0.1; -0.07+(m*0.17) 0.56 0.1 0.1], ...
                    1:4, clim, cmap_corr)
                hbar = colorbar('horiz', 'Ticks', clim);
                hbar.Position = [-0.095+(m*0.17) 0.46 0.07 0.01];
                
            end
            
        end
        
        for figure_C_age_changes = 1
            
            % model relationship between age and each MT moment
            out_t = zeros(size(MPmoments,3), size(MPmoments,2));
            out_q = zeros(size(MPmoments,3), size(MPmoments,2));
            for m = 1:4
                
                clear slm
                slm = SurfStatLinMod(MTmoments_corr(:,:,m), M1);
                
                % positive age effect
                slm = SurfStatT( slm, age);
                out_t(m,:) = slm.t;
                tmp = SurfStatQ( slm );
                out_q(m,out_t(m,:)>0) = tmp.Q(out_t(m,:)>0);
                
                regr_age_corr(m,t) = corr(out_t(m,:)', age_change(m,:)');
                
                % negative age effect
                slm = SurfStatT( slm, -age);
                tmp = SurfStatQ( slm );
                out_q(m,out_t(m,:)<0) = tmp.Q(out_t(m,:)<0);
                
            end
            
            cmap_tstat = interp_colormap(flipud(colorbrewer.div.RdBu{1,11}/255), 26);
            for m = 1:4
                
                % project significant effects to cortical surfaces
                % threshold represents Bonferroni correction for four two-sided tests
                surface_map = BoSurfStatMakeParcelData(out_t(m,:).*(out_q(m,:)<0.00625), FS, parc);
                clim        = [-7 7]; % consistent colourmap across surfaces

                BoSurfStat_calibrate4Views(surface_map, FS, ...
                    [-0.15+(m*0.17) 0.26 0.1 0.1; -0.07+(m*0.17) 0.16 0.1 0.1; ...
                    -0.15+(m*0.17) 0.16 0.1 0.1; -0.07+(m*0.17) 0.26 0.1 0.1], ...
                    1:4, clim, cmap_tstat)
                hbar = colorbar('horiz', 'Ticks', clim);
                hbar.Position = [-0.095+(m*0.17) 0.16 0.07 0.01];

            end
            
        end
        
        exportfigbo(f, strcat(figDir, '/morph_regr_', type, '.png'), 'png', 10)
        
    end
    
end

%% FIGURE 4 - Age-related changes of MT profile covariance

for Figure4 = 1
    
    % Figure4A - microstructural similarity changes with age
    for Figure4A = 1
        
        % construct MPCs
        parfor sub = 1:size(MP2,3)
            MPC2(:,:,sub) = build_mpc(MP2(:,:,sub), []);
        end
        
        % set up for figure
        cmap_mpc = interp_colormap(colorbrewer.seq.YlOrRd{1,9}./255, 26);
        [mes_sorted, mes_idx] = sort(mes_parc);

        % Figure 4A (left) - example construction of MPC
        f = figure;
        a(1) = axes('position', [0.1 0.65 0.2 0.3]);
        plot(MP2(:,91,1), 1:size(MP2,1), 'k', 'LineWidth', 1.5); hold on;
        plot(MP2(:,916,1), 1:size(MP2,1), 'k', 'LineWidth', 1.5); hold on;
        plot(mean(MP2(:,:,1),2), 1:size(MP2,1), ...
            'Color', [0.5 0.5 0.5], 'LineStyle', '--', 'LineWidth', 1.5);
        xlim([min(min(MP2(:,[91,916]))) max(max(MP2(:,[91,916],1)))])
        partialcorr(MP2(:,91,1), MP2(:,916,1), mean(MP2(:,:,1),2))
        hold off
        
        % MPC matrix
        a(2) = axes('position', [0.4 0.65 0.3 0.3]);
        imagesc(mean(MPC2(mes_idx,mes_idx,:),3), [0 1]); axis off
        colormap(a(2), cmap_mpc) 
        a(3) = axes('position', [0.39 0.65 0.008 0.3]);
        imagesc(mes_sorted'); axis off
        colormap(a(3), [1,1,1; cmap_mes])
        a(4) = axes('position', [0.4 0.952 0.3 0.008]);
        imagesc(mes_sorted); axis off
        colormap(a(4), [1,1,1; cmap_mes])
        a(5) = axes('position', [0.702 0.65 0.008 0.3]);
        imagesc(mes_sorted'); axis off
        colormap(a(5), [1,1,1; cmap_mes])
        a(6) = axes('position', [0.4 0.64 0.3 0.008]);
        imagesc(mes_sorted); axis off
        colormap(a(6), [1,1,1; cmap_mes])
        a(7) = axes('position', [0.8 0.65 0.008 0.3]);
        imagesc([1:100]'); axis off
        colormap(a(7), cmap_mpc)
        
        % run model at the edge level
        MPC2_long = [];
        parfor sub = 1:size(MPC2,3)
            MPC2_long(sub,:) = squareform(MPC2(:,:,sub));
        end
        idx = sum(MPC2_long)==0; % identify zero columns
        clear slm
        slm = SurfStatLinMod(MPC2_long(:,~idx), M1);
        slm = SurfStatT( slm, age );
        pos_q = CP_SurfStatQ( slm);
        pos_t_MPC = zeros(1, size(MPC2,2));
        pos_t_MPC(~idx) = slm.t;
        pos_t_MPC = squareform(pos_t_MPC);
        
        % t-statistic matrix
        slim_mes    = mes_parc(mes_parc>0);
        slim_t_MPC  = pos_t_MPC(mes_parc>0,mes_parc>0);
        [mes_idx, idx] = sort(slim_mes);
        a(2) = axes('position', [0.05 0.15 0.3 0.3]);
        imagesc(slim_t_MPC(idx,idx), [-4 4]); axis off
        colormap(a(2), cmap_tstat)
        a(3) = axes('position', [0.04 0.15 0.008 0.3]);
        imagesc(mes_idx'); axis off
        colormap(a(3), cmap_mes)
        a(4) = axes('position', [0.05 0.452 0.3 0.008]);
        imagesc(mes_idx); axis off
        colormap(a(4), cmap_mes)
        a(5) = axes('position', [0.352 0.15 0.008 0.3]);
        imagesc(mes_idx'); axis off
        colormap(a(5), cmap_mes)
        a(6) = axes('position', [0.05 0.14 0.3 0.008]);
        imagesc(mes_idx); axis off
        colormap(a(6), cmap_mes)
        
        % t-statistics matrix collapsed class
        for ii = 1:4
            for jj = 1:4
                tmp = pos_t_MPC(mes_parc==ii,mes_parc==jj);
                pos_t_MPC_class_mean(ii,jj) = mean(tmp(:));
                pos_t_MPC_class_sd(ii,jj) = std(tmp(:));
            end
        end
        a(5) = axes('position', [0.4 0.15 0.3 0.3]);
        errorbar(pos_t_MPC_class_mean(:), pos_t_MPC_class_sd(:), 'o', ...
            'Color', 'k', 'MarkerFaceColor', 'k', 'MarkerSize', 5)
        colormap(a(5), cmap_tstat)
        
        exportfig(f, [figDir, '/Figure_4A.png'], 'Format', 'png', 'FontMode', 'fixed',...
              'color', 'cmyk','Resolution',300 );
    end
    
        % set up coordinates
        for node = 1:length(uparcel)
            nodeCentroid(node,1:3) = mean(FS.coord(:,parc==uparcel(node)),2);
        end
        
        % postive figure
        pos_edges = zeros(1, size(MPC2,2));
        pos_edges(~idx) = slm.t .* (pos_q<0.025);
        pos_edges = squareform(pos_edges);
        [e_row, e_col] = find(pos_edges);
        edge_coords = [];
        for edge = 1:length(e_row)/2
            v1 = nodeCentroid(e_row(edge),:);
            v2 = nodeCentroid(e_col(edge),:);
            edge_coords(:,:,edge) = [v2;v1];
            edge_weight(edge) = pos_edges(e_row(edge), e_col(edge));
        end
        f = figure;
        CP_SurfStatViewEdges(edge_coords, edge_weight, FS, colorbrewer.seq.Reds{1,9}(2:9,:)/255)
        cbar            = [0.1:0.01:1]';
        a(3)            = axes('position',[0.01 0.75 0.02 0.2]);
        imagesc(flipud(cbar),[0.5 1]), axis off;
        colormap(a(3), colorbrewer.seq.Reds{1,9}(2:9,:)/255);
        exportfigbo(f, strcat(figDir, '/Supp_Figure_9A_pos.png'), 'png', 10)
        
        % negative edges
        slm = SurfStatT( slm, -age );
        neg_q = SurfStatQ( slm );
        neg_edges = zeros(1, size(MPC2,2));
        neg_edges(~idx) = slm.t .* (neg_q.Q<0.025);
        neg_edges = squareform(neg_edges);
        
        % negative figure
        [e_row, e_col] = find(neg_edges);
        edge_coords = [];
        edge_weight = [];
        for edge = 1:length(e_row)/2
            v1 = nodeCentroid(e_row(edge),:);
            v2 = nodeCentroid(e_col(edge),:);
            edge_coords(:,:,edge) = [v2;v1];
            edge_weight(edge) = neg_edges(e_row(edge), e_col(edge));
        end
        f = figure;
        CP_SurfStatViewEdges(edge_coords, edge_weight, FS, colorbrewer.seq.Blues{1,9}(2:end,:)/255)
        cbar            = [0.1:0.01:1]';
        a(3)            = axes('position',[0.01 0.75 0.02 0.2]);
        imagesc(flipud(cbar),[0.5 1]), axis off;
        colormap(a(3), colorbrewer.seq.Blues{1,9}(2:end,:)/255);
        
        exportfig(f, [figDir, '/Supp_Figure_9A_neg.png'], 'Format', 'png', 'FontMode', 'fixed',...
              'color', 'cmyk','Resolution',300 );
        
        % percentage increasing vs decreasing
        edge_effects(1) = nnz(pos_t_MPC>0) / nnz(pos_t_MPC);
        edge_effects(2) = nnz(pos_edges) / nnz(pos_t_MPC);
        edge_effects(3) = nnz(neg_edges) / nnz(pos_t_MPC);
        
        % Figure 4B - Spatial topography of age-related changes in
        % microstructural simiilarity
        for Figure4B = 1
            
            f = figure('units','centimeters','outerposition',[0 0 30 30]);
            coluse = flipud(plasma);
            
            % create t-stat gradient
            normAngleMatrix = connectivity2normangle(pos_t_MPC, 90);
            [embedding, results] = mica_diffusionEmbedding(normAngleMatrix, 'ncomponents', 30, 'symmetryMargin', 1e-05);
            
            % variance explained by eigenvectors
            a(1)    = axes('position',[0.05 .75 0.2 .2]);
            s       = sum(results.lambdas);
            x       = 1:10;
            scatter(x, results.lambdas(1:10)/s, 20, 'k', 'd', 'filled');
            
            % t-statistics ordered by the gradient
            a(2) = axes('position',[0.3 .75 0.25 .2]);
            [~, idx] = sort(embedding(:,1));
            imagesc(pos_t_MPC(idx,idx), [-4 4]); axis off
            h1 = colorbar('eastoutside');
            colormap(a(2), interp_colormap(flipud(colorbrewer.div.RdBu{1,9}/255), 26))
            
            % coloured 
            a(3) = axes('position',[0.6 .75 0.25 .2]);
            colourMatrix = repmat(embedding(idx,1)', [length(embedding),1])';
            colourMatrix(normAngleMatrix(idx, idx) == 0.5) = min(embedding(:,1)) - 0.1;
            imagesc(colourMatrix, [min(embedding(:,1)) max(embedding(:,1))]); axis off
            h2 = colorbar('eastoutside');
            colormap(a(3), [0,0,0; coluse])
            
            % project first gradient onto the cortical surface
            surface_map = BoSurfStatMakeParcelData(embedding(:,1), FS, parc);
            surface_map = surface_map .* mask';
            BoSurfStat_calibrate4Views(surface_map, FS, ...
                [0.55 0.4 0.2 0.2; 0.74 0.24 0.2 0.2; 0.55 0.24 0.2 0.2; 0.74 0.4 0.2 0.2], ...
                1:4, [min(surface_map) max(surface_map)], coluse)

            % bin the developmental gradient
            bins = 10;
            [~, idx] = sort(embedding(:,1));
            Drank = sort_back((1:length(embedding(:,1)))', idx);
            Dbins = discretize(Drank,bins);
            
            % create age-strata mpc gradients
            normAngleMatrix = connectivity2normangle(mean(MPC2(:,:,age_strata==1),3), 90);
            [young_embed, results] = mica_diffusionEmbedding(normAngleMatrix, 'ncomponents', 30, 'symmetryMargin', 1e-05);
            var_expl(1,:) = results.lambdas/sum(results.lambdas);
            
            normAngleMatrix = connectivity2normangle(mean(MPC2(:,:,age_strata==3),3), 90);
            [mid_embed, results] = mica_diffusionEmbedding(normAngleMatrix, 'ncomponents', 30, 'symmetryMargin', 1e-05);
            var_expl(2,:) = results.lambdas/sum(results.lambdas);

            normAngleMatrix = connectivity2normangle(mean(MPC2(:,:,age_strata==6),3), 90);
            [old_embed, results] = mica_diffusionEmbedding(normAngleMatrix, 'ncomponents', 30, 'symmetryMargin', 1e-05);
            var_expl(3,:) = results.lambdas/sum(results.lambdas);
            
            % align extreme age gradients to mid age gradient 
            [U,~,V] = svd(mid_embed.' * young_embed,0);
            U = U(:, 1:min(size(U,2), size(V,2)));
            V = V(:, 1:min(size(U,2), size(V,2)));
            xfms = V * U';
            alignEmbed(:,:,1) = young_embed * xfms;
            
            [U,~,V] = svd(mid_embed.' * old_embed,0);
            U = U(:, 1:min(size(U,2), size(V,2)));
            V = V(:, 1:min(size(U,2), size(V,2)));
            xfms = V * U';
            alignEmbed(:,:,2) = old_embed * xfms;
           
            f = figure('units','centimeters','outerposition',[0 0 30 30]);
            col_mpc = flipud(inferno);
            col_mpc = col_mpc(1:200,:);
            
            % show gradients
            for ii = 1:2
                surface_map = BoSurfStatMakeParcelData(alignEmbed(:,1,ii), FS, parc);
                clim = [-0.18 0.22];
                surface_map = surface_map .* mask';
                BoSurfStat_calibrate2Views(surface_map, FS, ...
                    [(ii*0.22)-0.21 0.8 0.2 0.2], [(ii*0.22)-0.21 0.64 0.2 0.2], ...
                    1, 2, clim, col_mpc)
                hbar = colorbar('horiz', 'XTick', clim);
                hbar.Position = [(ii*0.22)-0.15 0.63 0.1 0.01];
            end

            f = figure('units','centimeters','outerposition',[0 0 30 30]);
            % show anchors
            ii = 10;
            surface_map = BoSurfStatMakeParcelData(Dbins==ii, FS, parc);
            bincol = coluse(round(length(coluse)/10 * ii),:);
            BoSurfStat_calibrate2Views(surface_map, FS, ...
                [0.01 0.8 0.2 0.2], [0.01 0.64 0 0], ...
                1, 2, [0 1], [1,1,1; bincol])
            
            ii = 1;
            surface_map = BoSurfStatMakeParcelData(Dbins==ii, FS, parc);
            bincol = coluse(round(length(coluse)/10 * ii),:);
            BoSurfStat_calibrate2Views(surface_map, FS, ...
                [0.01 0.8 0 0], [0.01 0.64 0.2 0.2], ...
                1, 2, [0 1], [1,1,1; bincol])
            
            % correlation with anchors
            cmap_tstat = interp_colormap(flipud(colorbrewer.div.RdBu{1,11}/255), 26);
            ii = 10;
            anchor_diff = mean(mean(MPC2(Dbins==ii,:,age_strata==6),3),1) - ...
                mean(mean(MPC2(Dbins==ii,:,age_strata==1),3),1);
            surface_map = BoSurfStatMakeParcelData(anchor_diff, FS, parc);
            surface_map = SurfStatSmooth(surface_map, FS, 5);
            surface_map = surface_map .* mask';
            anchor_map = BoSurfStatMakeParcelData(Dbins==ii, FS, parc);
            surface_map(anchor_map==1) = 1; 
            bincol = coluse(round(length(coluse)/10 * ii),:);
            BoSurfStat_calibrate2Views(surface_map, FS, ...
                [0.23 0.8 0.2 0.2], [0.45 0.8 0.2 0.2], ...
                1, 2, [-0.5 0.5], [1,1,1; cmap_tstat; 0,0,0])
            
            ii = 1;
            anchor_diff = mean(mean(MPC2(Dbins==ii,:,age_strata==6),3),1) - ...
                mean(mean(MPC2(Dbins==ii,:,age_strata==1),3),1);
            surface_map = BoSurfStatMakeParcelData(anchor_diff, FS, parc);
            surface_map = SurfStatSmooth(surface_map, FS, 5);
            surface_map = surface_map .* mask';
            anchor_map = BoSurfStatMakeParcelData(Dbins==ii, FS, parc);
            surface_map(anchor_map==1) = 1;    
            bincol = coluse(round(length(coluse)/10 * ii),:);
            BoSurfStat_calibrate2Views(surface_map, FS, ...
                [0.23 0.64 0.2 0.2], [0.45 0.64 0.2 0.2], ...
                1, 2, [-0.5 0.5], [1,1,1; cmap_tstat; 0,0,0])
            
            hbar = colorbar('horiz', 'XTick',  [-0.5 0.5]);
            hbar.Position = [0.38 0.63 0.1 0.01];
            
            exportfig(f, [figDir, '/Figure_4B_anchors.png'], 'Format', 'png', 'FontMode', 'fixed',...
              'color', 'cmyk','Resolution',300 );
            
       end
       
       for Figue_4C = 1 
             
            % show profiles within each age range
            Id = mean(MP2(:,:,age_strata==1),3);
            for ii = 1:bins
                binMP(:,ii,1) = mean(Id(:,Dbins==ii),2);
            end

            Id = mean(MP2(:,:,age_strata==6),3);
            for ii = 1:bins
                binMP(:,ii,2) = mean(Id(:,Dbins==ii),2);
            end
            
           f = figure('units','centimeters','outerposition',[0 0 30 30]);
            
           % t-statistic change in mean and skewness
           clim = [-7 7];
           surface_map = BoSurfStatMakeParcelData(fig2b_maps(1,:), FS, parc);
           surface_map = SurfStatSmooth(surface_map, FS, 5);
           surface_map = surface_map .* mask';
           BoSurfStat_calibrate2Views(surface_map, FS, ...
                [0.01 0.8 0.2 0.2], [0.01 0.64 0.2 0.2], ...
                1, 2, clim, cmap_tstat)
           hbar = colorbar('horiz', 'XTick', clim);
           hbar.Position = [0.06 0.63 0.1 0.01];
            
           surface_map = BoSurfStatMakeParcelData(fig2b_maps(3,:), FS, parc);
           surface_map = SurfStatSmooth(surface_map, FS, 5);
           surface_map = surface_map .* mask';
           BoSurfStat_calibrate2Views(surface_map, FS, ...
                [0.23 0.8 0.2 0.2], [0.23 0.64 0.2 0.2], ...
                1, 2, clim, cmap_tstat)
           hbar = colorbar('horiz', 'XTick', clim);
           hbar.Position = [0.28 0.63 0.1 0.01];
           
           exportfig(f, [figDir, '/Figure_4C_left.png'], 'Format', 'png', 'FontMode', 'fixed',...
              'color', 'cmyk','Resolution',300 );

           f = figure('units','centimeters','outerposition',[0 0 30 30]);
            
           % mean and skewness between age brackets
           cmap_age = [colorbrewer.seq.YlGn{1,7}(2,:)/255; ...
               colorbrewer.seq.YlGn{1,7}(6,:)/255];
           a(1) = axes('position',[0.1 0.68 0.17 0.3]);
           for ii = 1:bins
               plot(squeeze(mean(binMP(:,ii,:))), [ii, ii], 'Color', [0,0,0], 'LineWidth', 3); hold on
           end
           for strata = 1:2
               scatter(mean(binMP(:,:,strata)), 1:bins, 50, cmap_age(strata,:), 'filled'); hold on
           end
           ylim([0 11])
           a(2) = axes('position',[0.27 0.68 0.17 0.3]);
           for ii = 1:bins
               plot(squeeze(skewness(binMP(:,ii,:))), [ii, ii], 'Color', [0,0,0], 'LineWidth', 3); hold on
           end
           for strata = 1:2
               scatter(skewness(binMP(:,:,strata)), 1:bins, 50, cmap_age(strata,:), 'filled'); hold on
           end
           ylim([0 11])
           set(gca, 'YTickLabel', [])
           
           % correlation with anchor changes
           ii = 10;
           anchor_diff = mean(mean(MPC2(Dbins==ii,:,age_strata==6),3),1) - ...
                mean(mean(MPC2(Dbins==ii,:,age_strata==1),3),1);
           a(1) = axes('position',[0.47 0.83 0.14 0.14]);
           scatter(fig2b_maps(1,:), anchor_diff, 7, [0.6 0.6 0.6], ...
               'filled', 'MarkerEdgeColor', 'k');
           xlim([min(fig2b_maps(1,:)) max(fig2b_maps(1,:))])
           ylim([min(anchor_diff) max(anchor_diff)])
           set(gca, 'YTickLabel', [])
           set(gca, 'XTickLabel', [])
           [r, p] = corr(fig2b_maps(1,:)', anchor_diff')
           
           a(2) = axes('position',[0.64 0.83 0.14 0.14]);
           scatter(fig2b_maps(3,:), anchor_diff, 7, [0.6 0.6 0.6], ...
               'filled', 'MarkerEdgeColor', 'k');
           xlim([min(fig2b_maps(3,:)) max(fig2b_maps(3,:))])
           ylim([min(anchor_diff) max(anchor_diff)])
           set(gca, 'YTickLabel', [])
           set(gca, 'XTickLabel', [])
           [r, p] = corr(fig2b_maps(3,:)', anchor_diff')
           
           ii = 1;
           anchor_diff = mean(mean(MPC2(Dbins==ii,:,age_strata==6),3),1) - ...
                mean(mean(MPC2(Dbins==ii,:,age_strata==1),3),1);
           a(3) = axes('position',[0.47 0.68 0.14 0.14]);
           scatter(fig2b_maps(1,:), anchor_diff, 7, [0.6 0.6 0.6], ...
               'filled', 'MarkerEdgeColor', 'k');
           xlim([min(fig2b_maps(1,:)) max(fig2b_maps(1,:))])
           ylim([min(anchor_diff) max(anchor_diff)])
           set(gca, 'YTickLabel', [])
           set(gca, 'XTickLabel', [])
           [r, p] = corr(fig2b_maps(1,:)', anchor_diff')

           a(4) = axes('position',[0.64 0.68 0.14 0.14]);
           scatter(fig2b_maps(3,:), anchor_diff, 7, [0.6 0.6 0.6], ...
               'filled', 'MarkerEdgeColor', 'k');
           xlim([min(fig2b_maps(3,:)) max(fig2b_maps(3,:))])
           ylim([min(anchor_diff) max(anchor_diff)])
           set(gca, 'YTickLabel', [])
           set(gca, 'XTickLabel', [])
           [r, p] = corr(fig2b_maps(3,:)', anchor_diff')
            
              exportfig(f, [figDir, '/Figure_4C_right.png'], 'Format', 'png', 'FontMode', 'fixed',...
              'color', 'cmyk','Resolution',300 );
            
            % gradient by classes
            dlmwrite([outDir '/gradient_classes.csv'],[mes_parc embedding(:,1)])
            
            % write out values for neurosynth decoding
            synthDir = '/data_/mica1/03_projects/casey/sandbox1/BigBrainScripts/neurosynth_terms/';
            clear synth_terms
            formatSpec = '%s%[^\n\r]';
            fileID = fopen([synthDir 'term_names.txt'],'r');
            tmp = textscan(fileID, formatSpec, 'Delimiter', ' ', 'TextType', 'string',  'ReturnOnError', false);
            synth_terms = tmp{1};
            terms_func_order = synth_terms([13, 9, 22, 15, 1, 10, 2, 16, 18, 14, 23, 4, 21, 12, 3, 11, 24, 6, 8, 17, 5, 18, 7, 19]);
            clear grad_synth
            grad_synth(:,1) = embedding(:,1);
            for ii = 1:length(synth_terms)
                lh = load_mgh(char(strcat(synthDir, 'lh.', terms_func_order(ii), '.mgh')));
                rh = load_mgh(char(strcat(synthDir, 'rh.', terms_func_order(ii), '.mgh')));
                tmp = Bo_surfData2parcelData([lh; rh]', parc); % parcellate
                grad_synth(:,ii+1) = tmp;
            end
            csvwrite([outDir '/gradient_synthing.csv'],grad_synth)  
       end
end


%% Supplement - absolute difference in moments matrices and age-related changes
for Supp_Fig = 1
    
    for m = 1:3
    
        for sub = 1:size(MTmoments,1)
            parfor n1 = 1:size(MTmoments,2)
                moment_diff(n1,:,sub) = abs(diff([repmat(MTmoments(sub,n1,m), size(MTmoments,2), 1)'; MTmoments(sub,:,m)]));
            end
        end

        % set up terms
        Age         = term(age);
        Sex         = term(sex);
        Subj        = term( var2fac (subj) );
        M1          = 1 + Age + Sex + random(Subj) + I;

        % run model at the edge level
        moment_diff_long = [];
        parfor sub = 1:size(moment_diff,3)
            moment_diff_long(sub,:) = squareform(moment_diff(:,:,sub));
        end
        clear slm
        slm = SurfStatLinMod(moment_diff_long, M1);
        slm = SurfStatT( slm, age );
        pos_q = CP_SurfStatQ( slm);
        pos_t_moment = zeros(1, size(moment_diff,2));
        pos_t_moment = slm.t;
        pos_t_moment = squareform(pos_t_moment);

        f = figure('units','centimeters','outerposition',[0 0 30 30]);

                % age-related changes gradient
                coluse = flipud(plasma);
                cmap_tstat = interp_colormap(flipud(colorbrewer.div.RdBu{1,11}/255), 26);

                % create t-stat gradient
                normAngleMatrix = connectivity2normangle(pos_t_moment, 90);
                [moment_gradients(:,:,m), results] = mica_diffusionEmbedding(normAngleMatrix, 'ncomponents', 30, 'symmetryMargin', 1e-05);

                % variance explained by eigenvectors
                a(1)    = axes('position',[0.11 0.75 0.175 .175]);
                s       = sum(results.lambdas);
                x       = 1:10;
                scatter(x, results.lambdas(1:10)/s, 20, 'k', 'd', 'filled');

                % mean t-statistics across gradient
                [~, idx] = sort(moment_gradients(:,1,m));
                a(2) = axes('position',[0.31 .75 0.175 .175]);
                imagesc(pos_t_moment(idx,idx)); axis off
                colormap(a(2), cmap_tstat)

                % project first gradient onto the cortical surface
                surface_map = BoSurfStatMakeParcelData(moment_gradients(:,1,m), FS, parc);
                surface_map = surface_map .* mask';

                BoSurfStat_calibrate4Views(surface_map, FS, ...
                    [0.1 0.55 0.2 0.2; 0.3 0.4 0.2 0.2; 0.1 0.4 0.2 0.2; 0.3 0.55 0.2 0.2], ...
                    1:4, [min(surface_map) max(surface_map)], coluse)
                hbar2 = colorbar('horiz');
                hbar2.Position = [0.25 0.42 0.1 0.01];
                
                % show scatter plot correlation between moment based and
                % mpc developmental gradients
                a(3)    = axes('position',[0.22 0.2 0.175 .175]);
                scatter(moment_gradients(:,1,m), embedding(:,1), 10, [0.5 0.5 0.5], 'filled')
                xlim([min(moment_gradients(:,1,m)) max(moment_gradients(:,1,m))])
                ylim([min(embedding(:,1)) max(embedding(:,1))])
                l = lsline;
                l.LineWidth = 3;
                l.Color = 'k';

                exportfigbo(f, char(strcat(figDir, '/moment', string(m), '_diff.png')), 'png', 10)
                
    end

end



%% SPECIFICTY OF MYELIN EFFECTS
% Controlling for thickness and blurring
% map change in thickness across age range
out_t = zeros(size(MPmoments,2), 4, 2, 2);
out_q = zeros(size(MPmoments,2), 4, 2, 2);

for baseline = 1
    
    age_to_term = age(1:end/2);
    sex_to_term = double(sex(1:end/2));
    
    for ii = 1:size(MPmoments,2)
        thick_to_term = thick2(ii,1:end/2)';

        M2 = 1 + term(age_to_term) + term(sex_to_term) + term(thick_to_term);

        slm = SurfStatLinMod(squeeze(MPmoments(1:end/2, ii, :)), M2);
        slm = SurfStatT( slm, thick_to_term );
        out_t(ii,:,1,1) = slm.t;
        tmp = SurfStatQ( slm );
        out_q(ii,slm.t>0,1,1) = tmp.Q(slm.t>0);
        
        slm = SurfStatT( slm, -thick_to_term );
        tmp = SurfStatQ( slm );
        out_q(ii,slm.t>0,1,1) = tmp.Q(slm.t>0);
        
        
        blurr_to_term = blurr2(ii,1:end/2)';

        M2 = 1 + term(age_to_term) + term(sex_to_term) + term(blurr_to_term);

        slm = SurfStatLinMod(squeeze(MPmoments(1:end/2, ii, :)), M2);
        slm = SurfStatT( slm, blurr_to_term );
        out_t(ii,:,2,1) = slm.t;
        tmp = SurfStatQ( slm );
        out_q(ii,slm.t>0,2,1) = tmp.Q(slm.t>0);
        
        slm = SurfStatT( slm, -blurr_to_term );
        tmp = SurfStatQ( slm );
        out_q(ii,slm.t>0,2,1) = tmp.Q(slm.t>0);
        
    end

end


for longitudinal = 1
    
    sex2 = double(sex);
    
    for ii = 1:size(MPmoments,2)
        
        thick_to_term = thick2(ii,:)';

        M2 = 1 + Age + term(sex2) + term(thick_to_term) + random(Subj) + I;

        slm = SurfStatLinMod(squeeze(MPmoments(:, ii, :)), M2);
        slm = SurfStatT( slm, thick_to_term );
        out_t(ii,:,1,2) = slm.t;
        tmp = SurfStatQ( slm );
        out_q(ii,slm.t>0,1,2) = tmp.Q(slm.t>0);
        
        slm = SurfStatT( slm, -thick_to_term );
        tmp = SurfStatQ( slm );
        out_q(ii,slm.t>0,1,2) = tmp.Q(slm.t>0);
        
        
        blurr_to_term = blurr2(ii,:)';

        M2 = 1 + Age + term(sex2) + term(blurr_to_term) + random(Subj) + I;

        slm = SurfStatLinMod(squeeze(MPmoments(:, ii, :)), M2);
        slm = SurfStatT( slm, blurr_to_term );
        out_t(ii,:,2,2) = slm.t;
        tmp = SurfStatQ( slm );
        out_q(ii,slm.t>0,2,2) = tmp.Q(slm.t>0);
        
        slm = SurfStatT( slm, -blurr_to_term );
        tmp = SurfStatQ( slm );
        out_q(ii,slm.t>0,2,2) = tmp.Q(slm.t>0);
        
    end

end

for figure = 1
    
    f = figure('units','normalized','outerposition',[0 0 1 1]);
    
    coluse = interp_colormap(colorbrewer.div.RdBu{1,9}/255, 26);
    
    for moment = 1:4
        for modality = 1:2
            for t = 1:2
            
            toMap = zeros(1, length(unique(parc)));
            this = out_t(:,moment,modality,t) .* (out_q(:,moment,modality,t)<0.003);
            toMap(1,1:505) = this(1:505);
            toMap(1,507:1011) = this(506:end);
            
            MomentCov = BoSurfStatMakeParcelData(toMap, FS, parc);
            MomentCov = MomentCov .* mask';
            MomentCov = SurfStatSmooth(MomentCov, FS, 4);
                        
            BoSurfStat_calibrate2Views(MomentCov, FS, ...
                [(0.1*moment)+((t-1)*0.5)-0.09 (0.3*modality) 0.1 0.1], ...
                [(0.1*moment)+((t-1)*0.5)-0.09 (0.3*modality)-0.1 0.1 0.1], ...
                1, 2, [-5 5], coluse)

            end
        end
    end
    
end

exportfig(f, [figDir, '/morph_confounds.png'], 'Format', 'png', 'FontMode', 'fixed',...
              'color', 'cmyk','Resolution',300 );






