%% main analysis
% test environment: MATLAB R2021a
% Brainspace toolbox v0.1.10 is needed
% spm12 toolbox is needed
% Link for downloading plotSurfaceROIBoundary: https://github.com/StuartJO/plotSurfaceROIBoundary
clear;clc;

% settings
pmap_threshold = 0.05; % threshold of pmap of the Julich-Brain
num_GS = 5; % number of gradients in gradient files
num_parcel = 228; % number of regions in Julich-Brain Atlas
num_vertex = 9684; % number of verties on fs-LR_5k surface

% load fsLR-32k surface 
load('C:\MICA\Github\micasoft-master\parcellations/fs_LR-conte69/fsaverage.midthickness_mni_32k_fs_LR.mat');
C69 = G; clear G;
% load fsLR-5k surface 
load('C:\MICA\gradient_profiles\data/fsLR_5k_YWNE.mat');
C69_10k = struct('coord', coord, 'tri', int32(tri));
mask_crtx = mask; % mask of the fsLR-5k surface
[surf_l, surf_r] = split_surfaces(C69_10k); % the fsLR-5k surface
% pmap of the Julich-Brain on fsLR-32k
load('C:\MICA\gradient_profiles\data\pmap_conte69_new.mat');
pmap_c69     = pmap_conte69;
% pmap of the Julich-Brain on fsLR-5k
cc = zeros(4842,114);
aa = gifti('C:\MICA\gradient_profiles\data\pmaps_fsLR_5k_L.func.gii');
aa = aa.cdata;
pmap_lh = [aa,cc];
aa2=gifti('C:\MICA\gradient_profiles\data\pmaps_fsLR_5k_R.func.gii');
aa2=aa2.cdata;
pmap_rh=[cc,aa2];
pmap_10k  = [pmap_lh;pmap_rh]';

% load parcellation of Julich-Brain atlas
load('C:\MICA\gradient_profiles\data/label_JUB.mat')
label_parcel228 = label_parcel228;

% load gradients
load('C:\MICA\gradient_profiles\data/FCGS_10subjs_sesaverage_FWHM3.mat');
load('C:\MICA\gradient_profiles\data/MPCGS_10subjs_sesaverage_FWHM3_YW.mat');
load('C:\MICA\gradient_profiles\data/SCGS_10subjs_sesaverage_FWHM3.mat');
MPCG_group_align = mean(MPCGS_sesaver_all_smooth,3);
SCG_group_align = mean(SCGS_sesaver_all_smooth,3);
FCG_group_align = mean(FCGS_sesaver_all_smooth,3);

% visualization of Julich-Brain atlas
temp_c69_lh = gifti('C:\MICA\gradient_profiles\data/fsLR-32k.L.inflated.surf.gii');
temp_c69_rh = gifti('C:\MICA\gradient_profiles\data/fsLR-32k.R.inflated.surf.gii');
c69_boundry_inflate_lh.vertices = temp_c69_lh.vertices;
c69_boundry_inflate_lh.faces = temp_c69_lh.faces;
pmap_thre2 = pmap_c69;
JBlabel_32k=zeros(size(pmap_c69,2),1);
for ii=1:size(pmap_c69,2)
    xx=pmap_c69(:,ii);
    if max(xx)>pmap_threshold 
        yy=find(xx==max(xx));
        JBlabel_32k(ii,1)=yy;
    end
end
figure; p = plotSurfaceROIBoundary(c69_boundry_inflate_lh,JBlabel_32k(1:32492),(1:114)','midpoint',[lines(229)],1);
view([-90 0])

% colormap settings
mycolorpoint=[[0 40 126];[0 58 186];[0 86 214];[0 113 240];[26 128 243];[69 162 255];...
    [228 241 255];[255 255 255];[255 220 220];[255 170 170];[255 140 140];[255 110 110];...
    [255 80 80];[255 50 50];[190 30 30];];
mycolorposition=[10 60 110 150 170 220 270 330 390 430 480 520 560 600 640];
mycolormap_r=interp1(mycolorposition,mycolorpoint(:,1),1:640,'linear','extrap');
mycolormap_g=interp1(mycolorposition,mycolorpoint(:,2),1:640,'linear','extrap');
mycolormap_b=interp1(mycolorposition,mycolorpoint(:,3),1:640,'linear','extrap');
blue_red=[mycolormap_r',mycolormap_g',mycolormap_b']/255;
blue_red=round(blue_red*10^4)/10^4;
red=blue_red(321:640,:);
blue=flip(blue_red(1:320,:));
load('C:\MICA\gradient_profiles\data\colormaps/vik.mat')
load('C:\MICA\gradient_profiles\data\colormaps/imola.mat')
load('C:\MICA\gradient_profiles\data\colormaps/buda.mat')
load('C:\MICA\gradient_profiles\data\colormaps/batlow.mat')
load('C:\MICA\gradient_profiles\data\colormaps/oslo.mat')
load('C:\MICA\gradient_profiles\data\colormaps/roma.mat')
load('C:\MICA\gradient_profiles\data\colormaps/nuuk.mat')
roma_flip=flip(roma);

%% generation of gradient profiles and inter-areal dissimilarity
[gradient_profile, inter_dissimilarity] = build_dissimila(MPCG_group_align(:,1:5),SCG_group_align(:,1:5),...
    FCG_group_align(:,1:5),num_GS,num_parcel,mask_crtx,label_parcel228);
% visualization of gradient profiles
figure;imagesc(gradient_profile);
set(gca, 'XTick',0);set(gca, 'YTick',0);
colormap(roma_flip);
colorbar('ticklength',0);

% visualization of inter-areal dissimilarity
inter_dissimilarity_32k   = mica_parcelData2surfData( [0;inter_dissimilarity], C69, JBlabel_32k)';
inter_dissimilarity_5k   = mica_parcelData2surfData([0;inter_dissimilarity], C69_10k, label_parcel228)';
Gs=zeros(length(mask_crtx),1); 
Gs(mask_crtx,:)=inter_dissimilarity_5k(mask_crtx,:);    
A=plot_hemispheres(Gs,{surf_l, surf_r}, 'labeltext',{'cosine dist'});
A.colormaps([0.8 0.8 0.8; imola]);
A.colorlimits([0.85,1.098]);

% label of 228 parcels on fsLR_5k
% csdist_parcel_vertex(label_parcel228==0)=1.02;% need to be MODIFIED!!!!!!
% csdist_parcel_vertex(mask_crtx'==0)=1.02;% need to be MODIFIED!!!!!!

%%% find areas with highest/lowest heterogeneity using spin test
NumPerm = 1000;
Xperm = spin_permutations(inter_dissimilarity_5k, C69_10k, NumPerm,'random_state',0);
gs_all_midw = zeros(size(mask_crtx,1),15);
gs_all_midw(mask_crtx,:) = [MPCG_group_align(:,1:5),SCG_group_align(:,1:5),FCG_group_align(:,1:5)]; %_zscore
spin_vertex = zeros(size(gs_all_midw,1),NumPerm);
temp_x = Xperm{1};
for jj = 1:NumPerm
    spin_vertex(:,jj) = temp_x(:,1,jj);
end
% vertex to parc
spin_parc = zeros(num_parcel,NumPerm);
for nr = 1:num_parcel
    idx = find(label_parcel228 == nr);
    spin_parc(nr,:) = mean(spin_vertex(idx,:));
end

p_perm = zeros(num_parcel,1);
p_label = ones(num_parcel,1);
for ng = 1:num_parcel
    prctile_rank = mean(spin_parc(ng,:) > inter_dissimilarity(ng,1));
    if prctile_rank < 0.5
        p_perm(ng,:) = prctile_rank;
    else
        p_perm(ng,:) = 1 - prctile_rank;
        p_label(ng,:) = -1;
    end
end
% find parcels significantly different from 1000 permulations
p_perm(p_perm==0)=0.0005;
nosig_idx   = find(p_perm>0.05);
logP      = -log10(p_perm);
logP(nosig_idx)= 0;
logP_diff = logP.*p_label;
% FDR correction
FDR         = mafdr(p_perm,'BHFDR', true); 
nosigFDR_idx   = find(FDR>0.05);
logFDR      = -log10(FDR);
logFDR(nosigFDR_idx)= 0;
p_label_lower = p_label;
p_label(p_label<0)=0;%remove negative values
logFDR_diff = logFDR.*p_label;
%lower heterogeneity
p_label_lower = p_label_lower*-1;
p_label_lower(p_label_lower<0) = 0;%remove negative values
logFDR_lower = logFDR.*p_label_lower;
logFDR_lower(116,1) = 0;% remove the region near to midwall
% visualization
spin_map        = mica_parcelData2surfData([0,logFDR_diff'], C69_10k, label_parcel228)';
Gs = zeros(length(mask_crtx),1); 
Gs(mask_crtx,:) = spin_map(mask_crtx,:);    
A = plot_hemispheres(Gs,{surf_l, surf_r}, 'labeltext',{'heterogeneity'});
A.colormaps([0.8 0.8 0.8; red]);
spin_map_lower        =  mica_parcelData2surfData([0,logFDR_lower'], C69_10k, label_parcel228)';%lower hetero
Gs(mask_crtx,:) = spin_map_lower(mask_crtx,:);    
A = plot_hemispheres(Gs,{surf_l, surf_r}, 'labeltext',{'heterogeneity'});
A.colormaps([0.8 0.8 0.8; blue]);

%%% association between inter-areal dissimilarity and BigBrain g1
load('C:\MICA\gradient_profiles\data/bigbrain_g1_fsLR_5k.mat');
bbgs_5k = bbgs_5k;
bbgs_parcel = zeros(size(pmap_10k,1),1);
bbgs_midw = zeros(size(mask_crtx,1),1);
bbgs_midw(mask_crtx,:) = bbgs_5k(mask_crtx,:); %_zscore
for ii=1:size(pmap_10k,1)
    label_parcel = find(label_parcel228==ii);
    bbgs_parcel(ii,:) = mean(bbgs_midw(label_parcel,:),1); 
end
bbgs_flip = bbgs_parcel*-1;
A = plot_hemispheres(bbgs_flip,{surf_l, surf_r},'parcellation', label_parcel228', 'labeltext',{'BBG1'});
A.colormaps([0.8 0.8 0.8; vik]);

% correlation between inter-areal dissimilarity and BigBrain gradient1
[r_dissimila_BBGS,p_dissimila_BBGS] = corr(inter_dissimilarity,bbgs_flip,'type','Spearman');
figure;scatter(inter_dissimilarity,bbgs_flip,150,'MarkerEdgeColor',[1 1 1],...
              'MarkerFaceColor',[0 0 0],'LineWidth',1.5);
xlim([0.85 1.12])
xticks([0.9 1.0 1.1])
ylim([-0.6 0.6])
yticks([-0.6 -0.1 0.6])
set(gca,'FontSize',18);
set(gca,'Linewidth',1.5);

% distribution in mesulam
load('C:\MICA\gradient_profiles\data/mesulam_fsLR_5k.mat');
label_mesulam=mesulam_fsLR_5k';
label_mesulam_parc=zeros(1,num_parcel);
for ii=1:num_parcel
    label_mesulam_parc(1,ii)=mode(label_mesulam(label_parcel228==ii));
end
dissimila_Paralim=inter_dissimilarity(label_mesulam_parc==1);
dissimila_Hetero=inter_dissimilarity(label_mesulam_parc==2);
dissimila_uni=inter_dissimilarity(label_mesulam_parc==3);
dissimila_Idio=inter_dissimilarity(label_mesulam_parc==4);
[~,p_dissimila_m1,~,tdissimila_m1]=ttest2(dissimila_Hetero,dissimila_Paralim);
[~,p_dissimila_m2,~,tdissimila_m2]=ttest2(dissimila_uni,dissimila_Paralim);
[~,p_dissimila_m3,~,tdissimila_m3]=ttest2(dissimila_Idio,dissimila_Paralim);
[~,p_dissimila_m4,~,tdissimila_m4]=ttest2(dissimila_uni,dissimila_Hetero);
[~,p_dissimila_m5,~,tdissimila_m5]=ttest2(dissimila_Idio,dissimila_Hetero);
[~,p_dissimila_m6,~,tdissimila_m6]=ttest2(dissimila_Idio,dissimila_uni);

%% intra-areal dissimilarity
distance_intra_5k=zeros(num_vertex,1);
distance_mesulam_mean=zeros(num_vertex,1);

gs2=-Inf(num_vertex,1);
for ii=1:num_parcel
    % distance between vertices to mean GP within a parcel
    gs_parcel=gs_all_midw(label_parcel228==ii,:);
    gs_parcel_mean=mean(gs_parcel,1);% =median(gs_parcel,1);
    gs_temp=[gs_parcel_mean;gs_parcel];
    distance_mean_sub    = pdist(gs_temp,'cosine');
    distance_mean_sub = squareform(distance_mean_sub);
    distance_intra_5k(label_parcel228==ii,1)=distance_mean_sub(1,2:end)';
end

% threshold for visualization
distance_raw=distance_intra_5k(label_parcel228~=0);
p1 = prctile(distance_raw,95);
distance_intra_5k_p95 = distance_intra_5k;
distance_intra_5k_p95(distance_intra_5k_p95>p1)=p1;
A=plot_hemispheres(distance_intra_5k_p95,{surf_l, surf_r}, 'labeltext',{'intra dstnc mn'});
A.colormaps([0.8 0.8 0.8; buda]);
% distribution of parcelwise VH in mesulam's 4 classes (Uni is significantly different to all 3 classes)
% for t-test
LH_Paralim=distance_intra_5k(label_parcel228~=0 & label_mesulam==1);
LH_Hetero=distance_intra_5k(label_parcel228~=0&label_mesulam==2);
LH_uni=distance_intra_5k(label_parcel228~=0&label_mesulam==3);
LH_Idio=distance_intra_5k(label_parcel228~=0&label_mesulam==4);
t_mesulam=zeros(4,4);
[~,p_m1,~,tm1]=ttest2(LH_Hetero,LH_Paralim);
[~,p_m2,~,tm2]=ttest2(LH_uni,LH_Paralim);
[~,p_m3,~,tm3]=ttest2(LH_Idio,LH_Paralim);
[~,p_m4,~,tm4]=ttest2(LH_uni,LH_Hetero);
[~,p_m5,~,tm5]=ttest2(LH_Idio,LH_Hetero);
[~,p_m6,~,tm6]=ttest2(LH_Idio,LH_uni);
t_mesulam(2,1)=tm1.tstat;
t_mesulam(3,1)=tm2.tstat;
t_mesulam(4,1)=tm3.tstat;
t_mesulam(3,2)=tm4.tstat;
t_mesulam(4,2)=tm5.tstat;
t_mesulam(4,3)=tm6.tstat;

% spin test
sphere_a=gifti('C:\MICA\gradient_profiles\data/fsLR_5k-regular.L.sphere.surf.gii');
sphere_b=gifti('C:\MICA\gradient_profiles\data/fsLR_5k-regular.R.sphere.surf.gii');
sphere_5k_lh.tri=sphere_a.faces;
sphere_5k_lh.coord=sphere_a.vertices';
sphere_5k_rh.tri=sphere_b.faces;
sphere_5k_rh.coord=sphere_b.vertices';
load('C:\MICA\gradient_profiles\data/mesulam_fsLR_32k.mat')
n_permutations = 1000;
y_rand = spin_permutations({inter_dissimilarity_5k(1:4842),inter_dissimilarity_5k(4843:9684)}, ...
                  {sphere_5k_lh,sphere_5k_rh}, n_permutations,'random_state',0);
% Merge the rotated data into single vectors
LH_5k_rotated = squeeze([y_rand{1}(:,1,:); y_rand{2}(:,1,:)]);

% t of random
LH_Paralim_rand=LH_5k_rotated(label_mesulam==1,:);
LH_Hetero_rand=LH_5k_rotated(label_mesulam==2,:);
LH_uni_rand=LH_5k_rotated(label_mesulam==3,:);
LH_Idio_rand=LH_5k_rotated(label_mesulam==4,:);
[~,~,~,t_rand_m1]=ttest2(LH_Hetero_rand,LH_Paralim_rand);
[~,~,~,t_rand_m2]=ttest2(LH_uni_rand,LH_Paralim_rand);
[~,~,~,t_rand_m3]=ttest2(LH_Idio_rand,LH_Paralim_rand);
[~,~,~,t_rand_m4]=ttest2(LH_uni_rand,LH_Hetero_rand);
[~,~,~,t_rand_m5]=ttest2(LH_Idio_rand,LH_Hetero_rand);
[~,~,~,t_rand_m6]=ttest2(LH_Idio_rand,LH_uni_rand);
prctile_rank_LH_M1 = mean(tdissimila_m1.tstat > t_rand_m1.tstat);
prctile_rank_LH_M2 = mean(tdissimila_m2.tstat > t_rand_m2.tstat);
prctile_rank_LH_M3 = mean(tdissimila_m3.tstat > t_rand_m3.tstat);
prctile_rank_LH_M4 = mean(tdissimila_m4.tstat > t_rand_m4.tstat);
prctile_rank_LH_M5 = mean(tdissimila_m5.tstat > t_rand_m5.tstat);
prctile_rank_LH_M6 = mean(tdissimila_m6.tstat > t_rand_m6.tstat);

%FDR correction
p_lh_mesulam=[p_m1;p_m2;p_m3;p_m4;p_m5;p_m6];
FDR_lh_mesulam         = mafdr(p_lh_mesulam,'BHFDR', true); 

% for lh in mesulam visualization
LH_Paralim_95=distance_intra_5k_p95(label_parcel228~=0 & label_mesulam==1);
LH_Hetero_95=distance_intra_5k_p95(label_parcel228~=0&label_mesulam==2);
LH_uni_95=distance_intra_5k_p95(label_parcel228~=0&label_mesulam==3);
LH_Idio_95=distance_intra_5k_p95(label_parcel228~=0&label_mesulam==4);

% internal vertex-hetero of all regions
distance_intra_parcel=zeros(num_parcel,1);% intra distance average on each paecel
for ii=1:num_parcel
distance_intra_parcel(ii,1)=mean(distance_intra_5k(label_parcel228==ii),1);
end
% distance_intra_Parcel_on5k = mica_parcelData2surfData([0,distance_intra_parcel], C69_10k, label_parcel228)'; 
A=plot_hemispheres(distance_intra_parcel,{surf_l, surf_r},'parcellation', label_parcel228', 'labeltext',{'LH parcel'});
A.colormaps([0.8 0.8 0.8; buda]);

% associaton with bigbrain g1 g2
[r_LH_BBGS,p_LH_BBGS]=corr(distance_intra_parcel,bbgs_flip,'type','Spearman');
figure;scatter(distance_intra_parcel,bbgs_flip(:,1),150,'MarkerEdgeColor',[1 1 1],...
              'MarkerFaceColor',[0 0 0],'LineWidth',1.5);
xlim([-0.02 0.3])
xticks([0 0.15 0.3])
ylim([-0.8 0.6])
yticks([-0.8 -0.1 0.6])
set(gca,'FontSize',18);
set(gca,'Linewidth',1.5);

figure;scatter(distance_intra_parcel,bbgs_flip,150,'MarkerEdgeColor',[1 1 1],...
              'MarkerFaceColor',[0 0 0],'LineWidth',1.5);
xlim([-0.02 0.3])
xticks([0 0.15 0.3])
ylim([-0.5 0.5])
yticks([-0.5 0 0.5])
set(gca,'FontSize',18);
set(gca,'Linewidth',1.5);

% spin test
bbg1_c69   = mica_parcelData2surfData( [0;bbgs_flip], C69, JBlabel_32k)';
lh_c69   = mica_parcelData2surfData( [0;distance_intra_parcel], C69, JBlabel_32k)';
[sphere_lh, sphere_rh] = load_conte69('spheres');
n_permutations = 1000;
y_rand = spin_permutations({bbg1_c69(1:32492),bbg1_c69(32493:64984)}, ...
                  {sphere_lh,sphere_rh}, n_permutations,'random_state',0);
% Merge the rotated data into single vectors
bbg1_rotated = squeeze([y_rand{1}(:,1,:); y_rand{2}(:,1,:)]);
% Find correlation between diversity and dissimila
[r_original_bbg1lh, pval_bbg1lh_spin] = corr(distance_intra_parcel,bbgs_flip, ...
                'rows','pairwise','type','spearman');
% pval_thick_spin = 0
r_rand_bbg1 = corr(lh_c69,bbg1_rotated, 'rows','pairwise','type','spearman');
% Compute percentile rank.
 prctile_rank_bbg1_lh = mean(r_original_bbg1lh > r_rand_bbg1);
 % prctile_rank_thick = 0.9410
 significant_bbg1_lh = prctile_rank_bbg1_lh < 0.025 || prctile_rank_bbg1_lh >= 0.975;

%% association with cross-task diversity
% global variability
num_task = 9;
load('C:\MICA\gradient_profiles\data/diversityariability_global_9tasks_cosine_distance.mat')%diversity_cosine

diversity_global(isnan(diversity_global))=0;
diversity_global_parcel = zeros(num_parcel,num_task);
for ii=1:num_parcel
    diversity_global_parcel(ii,:) = mean(diversity_global(label_parcel228==ii,:),1);
end
figure;imagesc(diversity_global_parcel);colormap(batlow);
set(gca, 'XTick',0);set(gca, 'YTick',0);colorbar('ticklength',0);

diversity_alltask = mean(diversity_global_parcel,2);
A = plot_hemispheres(diversity_alltask,{surf_l, surf_r},'parcellation', label_parcel228', 'labeltext',{'itfv'});
A.colormaps([0.8 0.8 0.8; batlow]);
% A.colorlimits([0.26,0.85]);
A.colorlimits([0.14,0.77]);
[r_dissimila_tdiversity,p_dissimila_tdiversity] = corr(inter_dissimilarity,[diversity_alltask,diversity_global_parcel],'type','Spearman');
figure;scatter(inter_dissimilarity,diversity_alltask,150,'MarkerEdgeColor',[1 1 1],...
              'MarkerFaceColor',[0 0 0],'LineWidth',1.5);
xlim([0.85 1.12]); xticks([0.9 1.0 1.1]);
ylim([0.23 0.9]); yticks([0.3 0.6 0.9]);
ylim([0.1 0.8]); yticks([0.1 0.45 0.8]);
set(gca,'FontSize',18);
set(gca,'Linewidth',1.5);

% local heterogeneity
[r_lh_tdiversity,p_lh_tdiversity]=corr(distance_intra_parcel,[diversity_alltask,diversity_global_parcel],'type','Spearman');
figure;scatter(distance_intra_parcel,diversity_alltask,150,'MarkerEdgeColor',[1 1 1],...
              'MarkerFaceColor',[0 0 0],'LineWidth',1.5);
 xlim([-0.02 0.3]); xticks([0 0.15 0.3]);
ylim([0.25 0.9]); yticks([0.3 0.60 0.9]);
ylim([0.1 0.8]); yticks([0.1 0.45 0.8]);
set(gca,'FontSize',18);
set(gca,'Linewidth',1.5);
   
% spin permutations 
% Let's create some rotations
diversity_alltask_c69   = mica_parcelData2surfData( [0,diversity_alltask'], C69, JBlabel_32k)';
lh_c69   = mica_parcelData2surfData( [0;distance_intra_parcel], C69, JBlabel_32k)';

diversity_alltask_c69_lh=diversity_alltask_c69(1:32492);
diversity_alltask_c69_rh=diversity_alltask_c69(32493:64984);
[surf_lh, surf_rh] = load_conte69;
[sphere_lh, sphere_rh] = load_conte69('spheres');
n_permutations = 1000;
y_rand = spin_permutations({diversity_alltask_c69(1:32492),diversity_alltask_c69(32493:64984)}, ...
                  {sphere_lh,sphere_rh}, n_permutations,'random_state',0);
% Merge the rotated data into single vectors
diversity_rotated = squeeze([y_rand{1}(:,1,:); y_rand{2}(:,1,:)]);

% Find correlation between cross-task diversity and dissimila
[r_original_diversity, pval_diversity_spin] = corr(inter_dissimilarity,diversity_alltask, ...
                'rows','pairwise','type','spearman');
% pval_thick_spin = 0
r_rand_diversity = corr(inter_dissimilarity_32k,diversity_rotated, 'rows','pairwise','type','spearman');
% Compute percentile rank.
prctile_rank_diversity = mean(r_original_diversity > r_rand_diversity);
 % prctile_rank_thick = 0.9410
significant_diversity = prctile_rank_diversity < 0.025 || prctile_rank_diversity >= 0.975;
 
% Find correlation between diversity and lh
[r_original_diversity_lh, pval_diversity_spin_lh] = corr(distance_intra_parcel,diversity_alltask, ...
                'rows','pairwise','type','spearman');
% pval_thick_spin = 0
r_rand_diversity_lh = corr(lh_c69,diversity_rotated, 'rows','pairwise','type','spearman');
% Compute percentile rank.
 prctile_rank_diversity_lh = mean(r_original_diversity_lh > r_rand_diversity_lh);
 % prctile_rank_thick = 0.9410
 significant_diversity_lh = prctile_rank_diversity_lh < 0.025 || prctile_rank_diversity_lh >= 0.975;
 
