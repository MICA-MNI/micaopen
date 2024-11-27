% this is a demo code for showing how to generate vertex-wise gradients
% used in the main analysis, including MPC, SC, FC gradients

clc; clear;
% Add path of the necessary toolbox
addpath('PATH OF surfstat');
addpath(genpath('PATH OF BrainSpace'));
addpath('PATH OF gifti-1.6');

savedir = 'PATH OF YOUR SAVE FOLDER';
% the vertex-wise MPC, SC, FC matrices are available at the OSF platform 
% (https://osf.io/mhq3f/). Download them  
datadir='PATH OF YOUR DATA';

% settings
nG=10; % number of gradients
T=90; % threshold for gradients estimate
num_subj=10; % number of subjects
num_ses=3; % number of sessions
num_vert=4842; % number of vertices in each hemisphere
FWHM=3; % smooth setting

% load subject list
HCList = readtable('YOUR SUBJECT LIST'); % your custom sublist, e.g. "sub-PNC001 sub-PNC002 sub-PNC003" 
HCList=HCList.ID;
% Load fsLR-5k surface, parcellation, and mask
load('/micaopen/gradient_profiles/data/fsLR_5k_YWNE.mat');
load('/micaopen/gradient_profiles/data/colormaps/vik.mat')
c69_10k = struct('coord',coord,'tri',tri);
[surf_l2, surf_r2] = split_surfaces(c69_10k);
% settings for gradients estimate
gm = GradientMaps('kernel', 'na', 'alignment', 'pa','approach', 'dm', 'n_components', nG);
fsLR_5k = struct('coord', coord, 'tri', int32(tri));

%% Estimate structural gradients
SC_all=zeros(num_vert*2,num_vert*2,num_subj,num_ses);
mask_lh=mask(1:4842,1);
mask_rh=mask_lh;
%%% estimate SC template gradient
% load 5k SC data
for kk=1:2 % 2 sessions of dwi
for ii =1:num_subj
    sub=['sub-',HCList{ii,1}];
    filename=[datadir,sub,'/ses-0',num2str(kk),'/dwi/connectomes/',sub,'_ses-0',num2str(kk),'_surf-fsLR-5k_desc-iFOD2-40M-SIFT2_full-connectome.shape.gii'];
    A0=gifti(filename);
    A1=A0.cdata;
    SC_sub=transpose(A1)+triu(A1,1);
    SC_all(:,:,ii,kk)=SC_sub;
end
end
SC_group1=mean(SC_all,4);
% group-averaged SC
SC_group=mean(SC_group1,3);

% estimate SC template gradients for left and right hemisphere
sc_lh=SC_group(1:4842,1:4842);
SC_lh_mask=sc_lh(mask_lh==1,mask_lh==1);
SC_lh_mask(SC_lh_mask==0)=eps;
g_sub = gm.fit(SC_lh_mask, 'sparsity', T);
lambda_temp=g_sub.lambda{1};
lambda_sclh=sum(lambda_temp(1:5,:));
g_template=g_sub.gradients{1};
sc_rh=SC_group(4843:9684,4843:9684);
SC_rh_mask=sc_rh(mask_rh==1,mask_rh==1);
SC_rh_mask(SC_rh_mask==0)=eps;
g_sub_rh = gm.fit(SC_rh_mask, 'sparsity', T,'reference',g_template);
lambda_temp=g_sub_rh.lambda{1};
lambda_scrh=sum(lambda_temp(1:5,:));
g_rh_template=g_sub_rh.aligned{1};
% concatenate left and right SC gradient together, apply mask, smooth
SCGS_template=[g_template;g_rh_template];
GS1=zeros(length(mask),10);
GS1(mask,:)=SCGS_template;
SCG_smooth = SurfStatSmooth(GS1', fsLR_5k, FWHM)';
SCGS_template_smooth=SCG_smooth(mask,:);
% visualization of SC temelate gradients
SCGS_view=zeros(9684,5);
SCGS_view(mask,:)=SCGS_template_smooth(:,1:5);
A=plot_hemispheres(SCGS_view,{surf_l2, surf_r2},'labeltext',{'SCG1','SCG2','SCG3','SCG4','SCG5'});
A.colormaps(vik);
A.colorlimits([-0.06,0.06]);

%%% Estimate SC individual gradiets, align it using SC template gradients
SCGS_all_smooth=zeros(sum(mask_rh)*2,nG,num_subj,2);
for kk=1:2 % 2 sessions of dwi
    for jj =1:num_subj
        SC_indi=SC_all(:,:,jj,kk);
        sc_lh=SC_indi(1:4842,1:4842);
        SC_lh_mask=sc_lh(mask_lh==1,mask_lh==1);
        SC_lh_mask(SC_lh_mask==0)=eps;
        g_sub = gm.fit(SC_lh_mask, 'sparsity', T,'reference',SCGS_template_smooth(1:4432,:));
        g_lh_indi=g_sub.aligned{1};
        sc_rh=SC_indi(4843:9684,4843:9684);
        SC_rh_mask=sc_rh(mask_rh==1,mask_rh==1);
        SC_rh_mask(SC_rh_mask==0)=eps;
        g_sub_rh = gm.fit(SC_rh_mask, 'sparsity', T,'reference',SCGS_template_smooth(4433:8864,:));
        g_rh_indi=g_sub_rh.aligned{1};
        GS1=zeros(length(mask),10);
        GS1(mask,:)=[g_lh_indi;g_rh_indi];
        SCG_smooth = SurfStatSmooth(GS1', fsLR_5k, FWHM)';
        SCGS_all_smooth(:,:,jj,kk)=SCG_smooth(mask,:);
    end
    SCGS_groupaverage=mean(SCGS_all_smooth(:,:,:,kk),3);
    % visualization
    SCGS_view=zeros(9684,5);
    SCGS_view(mask,:)=SCGS_groupaverage(:,1:5);
    A=plot_hemispheres(SCGS_view,{surf_l2, surf_r2},'labeltext',{'SCG1','SCG2','SCG3','SCG4','SCG5'});
    A.colormaps(vik);
end
SCGS_all_smooth_ses1=SCGS_all_smooth(:,:,:,1);
SCGS_all_smooth_ses2=SCGS_all_smooth(:,:,:,2);
% gradients of session-averaged matrix of each subject
SCGS_sesaver_all_smooth=zeros(sum(mask_rh)*2,nG,num_subj);
for jj =1:num_subj
    SC_indi=SC_group1(:,:,jj);
    sc_lh=SC_indi(1:4842,1:4842);
    SC_lh_mask=sc_lh(mask_lh==1,mask_lh==1);
    SC_lh_mask(SC_lh_mask==0)=eps;
    g_sub = gm.fit(SC_lh_mask, 'sparsity', T,'reference',SCGS_template_smooth(1:4432,:));
    g_lh_indi=g_sub.aligned{1};
    sc_rh=SC_indi(4843:9684,4843:9684);
    SC_rh_mask=sc_rh(mask_rh==1,mask_rh==1);
    SC_rh_mask(SC_rh_mask==0)=eps;
    g_sub_rh = gm.fit(SC_rh_mask, 'sparsity', T,'reference',SCGS_template_smooth(4433:8864,:));
    g_rh_indi=g_sub_rh.aligned{1};
    GS1=zeros(length(mask),10);
    GS1(mask,:)=[g_lh_indi;g_rh_indi];
    SCG_smooth = SurfStatSmooth(GS1', fsLR_5k, FWHM)';
    SCGS_sesaver_all_smooth(:,:,jj)=SCG_smooth(mask,:);
end

save([homedir '/results/SC/SCGS_10subjs_ses1_FWHM3.mat'],'SCGS_all_smooth_ses1')
save([homedir '/results/SC/SCGS_10subjs_ses2_FWHM3.mat'],'SCGS_all_smooth_ses2')
save([savedir '/results/SC/SCGS_10subjs_sesaverage_FWHM3_',num2str(T),'.mat'],'SCGS_sesaver_all_smooth')

%% Estimate MPC gradients 
MPC_all=zeros(sum(mask),sum(mask),num_subj,num_ses);
for kk=1:num_ses
    for ii =1:num_subj
        sub=['sub-',HCList{ii,1}];
        B1=gifti([datadir,sub,'/ses-0',num2str(kk),'/mpc/acq-T1map/',sub,'_ses-0',num2str(kk),'_surf-fsLR-5k_desc-intensity_profiles.shape.gii']);
        MP_sub=B1.cdata;
        MP_sub_smooth_withmask = SurfStatSmooth(MP_sub, fsLR_5k, FWHM);
        MP_sub_smooth = MP_sub_smooth_withmask(:,mask);
        [MPC, I, problemNodes] = build_mpc(MP_sub_smooth,[]);
        MPC_all(:,:,ii,kk)=MPC;
    end
end

MPC_group1=mean(MPC_all(:,:,:,:),4);
MPC_group=mean(MPC_group1(:,:,:),3);
% estimate MPC gradients
g_sub = gm.fit(MPC_group, 'sparsity', T);
lambda_temp=g_sub.lambda{1};
lambda_mpc=sum(lambda_temp(1:5,:));
MPCGS_template=g_sub.gradients{1};
% smooth MPC gradients
GS1=zeros(length(mask),10);
GS1(mask,:)=MPCGS_template;
grpG_smooth = SurfStatSmooth(GS1', fsLR_5k, FWHM)';
MPCGS_template_smooth=grpG_smooth(mask,:);
% visualization
MPCGS_Tview=zeros(9684,5);
MPCGS_Tview(mask,:)=MPCGS_template_smooth(:,1:5);
A=plot_hemispheres(MPCGS_Tview,{surf_l2, surf_r2},'labeltext',{'MPCG1','MPCG2','MPCG3','MPCG4','MPCG5'});
A.colormaps(vik);
save([homedir '/results/MPC/MPCGS_template_10subjs_3ses_YW.mat'],'MPCGS_template_smooth')

% MPC individual gradiets
MPCGS_all=zeros(sum(mask),nG,num_subj,num_ses);
for kk=1:num_ses
for jj =1:num_subj
    MPC_indi=MPC_all(:,:,jj,kk);
    g_sub = gm.fit(MPC_indi, 'sparsity', T,'reference',MPCGS_template_smooth);
    g_MPC_indi=g_sub.aligned{1};
    GS2=zeros(length(mask),10);
    GS2(mask,:)=g_MPC_indi;
    grpG_smooth = SurfStatSmooth(GS2', fsLR_5k, FWHM)';
    MPCGS_all(:,:,jj,kk) = grpG_smooth(mask,:);
end

MPCGS_all_group=mean(MPCGS_all(:,:,:,kk),3);

MPCGS_view=zeros(9684,5);
MPCGS_view(mask,:)=MPCGS_all_group(:,1:5);
A=plot_hemispheres(MPCGS_view,{surf_l2, surf_r2},'labeltext',{'MPCG1','MPCG2','MPCG3','MPCG4','MPCG5'});
A.colormaps(vik);
end
MPCGS_all_smooth_ses1=MPCGS_all(:,:,:,1);
MPCGS_all_smooth_ses2=MPCGS_all(:,:,:,2);
MPCGS_all_smooth_ses3=MPCGS_all(:,:,:,3);
% gradients of session-averaged matrix of each subject
MPCGS_sesaver_all_smooth=zeros(sum(mask_rh)*2,nG,num_subj);
for jj =1:num_subj
    MPC_indi=MPC_group1(:,:,jj);
    g_sub = gm.fit(MPC_indi, 'sparsity', T,'reference',MPCGS_template_smooth);
    g_MPC_indi=g_sub.aligned{1};
    GS2=zeros(length(mask),10);
    GS2(mask,:)=g_MPC_indi;
    grpG_smooth = SurfStatSmooth(GS2', fsLR_5k, FWHM)';
    MPCGS_sesaver_all_smooth(:,:,jj) = grpG_smooth(mask,:);
end

save([homedir '/results/MPC/MPCGS_10subjs_ses1_FWHM3_YW.mat'],'MPCGS_all_smooth_ses1')
save([homedir '/results/MPC/MPCGS_10subjs_ses2_FWHM3_YW.mat'],'MPCGS_all_smooth_ses2')
save([homedir '/results/MPC/MPCGS_10subjs_ses3_FWHM3_YW.mat'],'MPCGS_all_smooth_ses3')
save([savedir '/results/MPC/MPCGS_10subjs_sesaverage_FWHM3_YW_',num2str(T),'.mat'],'MPCGS_sesaver_all_smooth')

%% Estimate FC gradients 
FC_all=zeros(num_vert*2,num_vert*2,num_subj,num_ses);
for kk=1:num_ses
for ii =1:num_subj
        sub=['sub-',HCList{ii,1}];

    C0=gifti([datadir,sub,'/ses-0',num2str(kk),'/func/desc-me_task-rest_bold/surf/',sub,'_ses-0',num2str(kk),'_surf-fsLR-5k_desc-FC.shape.gii']);
    C1=C0.cdata;
    FC_sub=transpose(C1)+triu(C1,1);
    FC_z=.5 * log( (1+FC_sub) ./ (1-FC_sub) );
    FC_z(FC_z==Inf)=1;
    FC_all(:,:,ii,kk)=FC_z;
end
end
FC_group1=mean(FC_all(:,:,:,:),4);
FC_group=mean(FC_group1(:,:,:),3);

% estimate FC temolate gradients
FC_mask=FC_group(mask==1,mask==1);
g_sub = gm.fit(FC_mask, 'sparsity', T);
lambda_temp=g_sub.lambda{1};
lambda_fc=sum(lambda_temp(1:5,:));
FCGS_template=g_sub.gradients{1};
GS1=zeros(length(mask),10);
GS1(mask,:)=FCGS_template;
FCG_smooth = SurfStatSmooth(GS1', fsLR_5k, FWHM)';
FCGS_template_smooth=FCG_smooth(mask,:);
FCGS_Tview=zeros(9684,5);
FCGS_Tview(mask,:)=FCGS_template_smooth(:,1:5);
A=plot_hemispheres(FCGS_Tview,{surf_l2, surf_r2},'labeltext',{'FCG1','FCG2','FCG3','FCG4','FCG5'});
A.colormaps(vik);
save([homedir '/results/FC/FCGS_template_10subjs_3ses_FWHM3.mat'],'FCGS_template_smooth')

% estimate FC individual gradiets
FCGS_all=zeros(sum(mask),nG,num_subj,num_ses);
for kk=1:num_ses
for jj =1:num_subj
    FC_indi=FC_all(:,:,jj,kk);
    FC_sub_mask=FC_indi(mask==1,mask==1);
    g_sub = gm.fit(FC_sub_mask, 'sparsity', T,'reference',FCGS_template_smooth);
    g_FC_indi=g_sub.aligned{1};
    GS2=zeros(length(mask),10);
    GS2(mask,:)=g_FC_indi;
    grpG_smooth = SurfStatSmooth(GS2', fsLR_5k, FWHM)';
    FCGS_all(:,:,jj,kk) = grpG_smooth(mask,:);
end

FCGS_all_group=mean(FCGS_all(:,:,:,kk),3);

FCGS_view=zeros(9684,5);
FCGS_view(mask,:)=FCGS_all_group(:,1:5);
A=plot_hemispheres(FCGS_view,{surf_l2, surf_r2},'labeltext',{'FCG1','FCG2','FCG3','FCG4','FCG5'});
A.colormaps(vik);
% A.colorlimits([-0.06,0.06]);
end
FCGS_all_smooth_ses1=FCGS_all(:,:,:,1);
FCGS_all_smooth_ses2=FCGS_all(:,:,:,2);
FCGS_all_smooth_ses3=FCGS_all(:,:,:,3);
% gradients of session-averaged matrix of each subject
FCGS_sesaver_all_smooth=zeros(sum(mask),nG,num_subj);
for jj =1:num_subj
    FC_indi=FC_group1(:,:,jj);
    FC_sub_mask=FC_indi(mask==1,mask==1);
    g_sub = gm.fit(FC_sub_mask, 'sparsity', T,'reference',FCGS_template_smooth);
    g_FC_indi=g_sub.aligned{1};
    GS2=zeros(length(mask),10);
    GS2(mask,:)=g_FC_indi;
    grpG_smooth = SurfStatSmooth(GS2', fsLR_5k, FWHM)';
    FCGS_sesaver_all_smooth(:,:,jj) = grpG_smooth(mask,:);
end
save([homedir '/results/FC/FCGS_10subjs_ses1_FWHM3.mat'],'FCGS_all_smooth_ses1')
save([homedir '/results/FC/FCGS_10subjs_ses2_FWHM3.mat'],'FCGS_all_smooth_ses2')
save([homedir '/results/FC/FCGS_10subjs_ses3_FWHM3.mat'],'FCGS_all_smooth_ses3')
save([savedir '/results/FC/FCGS_10subjs_sesaverage_FWHM3_',num2str(T),'.mat'],'FCGS_sesaver_all_smooth')

