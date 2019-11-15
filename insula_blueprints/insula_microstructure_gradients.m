%% insula_microstructure_gradients.m 
%
% written by Jessica Royer
% MICA lab, Montreal Neurological Institute
% November 2018 - November 2019


%% Initiate project 
for init_project = 1     
    
    % directories
    GH = '/data_/mica1/03_projects/jessica/';    
    baseDir = [GH '/micaopen/insula_blueprints/'];
    
    % useful scripts
    addpath([GH '/micasoft/matlab/vtk']); 
    addpath([GH '/micasoft/matlab/NIfTI_20140122']); 
    addpath([GH '/micasoft/matlab/useful'])  
    addpath([GH '/micaopen/MPC'])
    addpath(genpath([GH '/micaopen/surfstat'])) 
    addpath(genpath([GH '/micaopen/BrainSpace'])) 

    % colormap
    load(strcat(baseDir, 'blue_cmap.mat'));
     
    % labels & surfaces
    FSinflate = SurfStatAvSurf({'/data_/mica1/01_programs/Freesurfer-6.0/subjects/fsaverage5/surf/lh.inflated' ...
                '/data_/mica1/01_programs/Freesurfer-6.0/subjects/fsaverage5/surf/rh.inflated'});
    FS = SurfStatAvSurf({'/data_/mica1/01_programs/Freesurfer-6.0/subjects/fsaverage5/surf/lh.pial' ...
                '/data_/mica1/01_programs/Freesurfer-6.0/subjects/fsaverage5/surf/rh.pial'});
    load(strcat(baseDir, 'insula_surface.mat'))
    
    nFS = length(FS.coord);
    load('/data_/mica1/03_projects/jessica/cinguloinsular/theGreatRerun/basics/erodedLabels.mat')
    labelsL = erodeLabels(erodeLabels < nFS/2);
    labelsR = erodeLabels(erodeLabels > nFS/2);
    labels = [labelsL; labelsR];
    
end

%% Generate MPC from HCP sample (n=109)

% Profiles for whole cortex
load(strcat(baseDir, 'profiles_T1T2_insula.mat'));
nSurf = size(Dlo_all,1);
nSubj = size(Dlo_all,3);

% ready matrix
Z_left = zeros(length(labelsL), length(labelsL), nSubj);
Z_right = zeros(length(labelsR), length(labelsR), nSubj);

% Build MPC
for s = 1:size(Dlo_all,3)
    [Z_left(:,:,s), ~] = build_mpc(Dlo_all_lh(:,:,s), []);
    [Z_right(:,:,s), ~] = build_mpc(Dlo_all_rh(:,:,s), []);
end

% Average MPC matrix across subjects
Z_left_all = mean(Z_left,3);
Z_right_all = mean(Z_right,3);


%% Generate MPC from MICA-MTL sample (n=32)

load(strcat(baseDir, 'profiles_qT1_insula.mat'));
nSurf = size(Dlo_all_mica,1);
nSubj = size(Dlo_all_mica,3);

% ready matrix
Z_left_mica = zeros(length(labelsL), length(labelsL), nSubj);
Z_right_mica = zeros(length(labelsR), length(labelsR), nSubj);

% Build MPC
for s = 1:size(Dlo_all_mica,3)
    [Z_left_mica(:,:,s), ~] = build_mpc(Dlo_mica_lh(:,:,s), []);
    [Z_right_mica(:,:,s), ~] = build_mpc(Dlo_mica_rh(:,:,s), []);
end

% Average MPC matrix across subjects
Z_left_micaAll = mean(Z_left_mica,3);
Z_right_micaAll = mean(Z_right_mica,3);


%% Generate gradients using BrainSpace, while aligning MICA sample gradients to HCP template
% Note that gradient signs can be flipped, as raw values are arbitrary
% In manuscript, some gradient signs were flipped for consistent presentation and for easier comprehension

% Right hemisphere
gm_r = GradientMaps('alignment','pa','n_components',10);
gm_r = gm_r.fit({Z_right_all,Z_right_micaAll});

g1_rh_hcp = gm_r.aligned{1}(:,1);
g2_rh_hcp = gm_r.aligned{1}(:,2);
g1_rh_mica = gm_r.aligned{2}(:,1);
g2_rh_mica = gm_r.aligned{2}(:,2);

% Left hemisphere
gm_l = GradientMaps('alignment','pa','n_components',10);
gm_l = gm_l.fit({Z_left_all,Z_left_micaAll});

g1_lh_hcp = gm_l.aligned{1}(:,1);
g2_lh_hcp = gm_l.aligned{1}(:,2);
g1_lh_mica = gm_l.aligned{2}(:,1);
g2_lh_mica = gm_l.aligned{2}(:,2);