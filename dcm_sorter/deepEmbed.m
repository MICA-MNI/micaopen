%% deepembedding_play.m 
% Playing with deep embedding
%
% Written by Casey Paquola
% MICA lab, Montreal
% October 2018

% init project
for init_project = 1
    
    GH          = '/data_/mica1/03_projects/casey/';
    vtkp        = '/data_/mica1/03_projects/casey/micasoft/matlab/vtk';
    nifti       = '/data_/mica1/03_projects/casey/micasoft/matlab/NIfTI_20140122';
    addpath([GH '/micasoft/matlab/useful'])
    addpath([GH '/sandbox1/BigBrainScripts'])
    addpath([GH '/micaopen/surfstat_addons'])
    addpath('/data_/mica1/03_projects/reinder/rajasoft/matlab/01_hcp/surfaces')
    addpath([GH '/micasoft/matlab/colormaps/viridis'])
    addpath([GH '/micasoft/matlab/colormaps/'])
    addpath([GH '/micasoft/parcellations/Gradients/'])
    addpath(genpath([GH '/micasoft/matlab/diffusionEmbedding']))
    m = load(strcat(GH, '/micasoft/matlab/colormaps/margulies_gradient_colormap.mat'));
    margulies   = m.hcp_colormap;
    c = load([GH '/micasoft/matlab/colormaps/cbrewer/colorbrewer.mat']);
    colorbrewer = c.colorbrewer;
    inferno     = inferno();
    viridis     = viridis();
    magma       = magma();
    plasma      = plasma();
    fparul      = fake_parula();
    
    addpath(vtkp)
    addpath(nifti)
    
end

for load_HCP = 1
    
    for group_gradient = 1
        
        dataDir             = '/host/yeatman/local_raid/casey/hcp_surfs/MSM/';
        num_surf            = 14;
        GPATH               = strcat(dataDir, string(num_surf), 'surfs/');

        disp('load data')
        for load_data = 1
            
            load(strcat(GPATH, 'Zgroup.mat'),'Zgroup');
            MPC = Zgroup;
            load(strcat(dataDir, 'C10.mat'),'C10')
            load(strcat(dataDir, 's20.mat'),'s20')
            HCP_s20 = s20;
            
        end
        
        % create mask
        load('/host/fladgate/local_raid/HCP_data/templatesParcellations/conte69_64k/surf/corticalMask.mat')
        mask = mask.cortex;
             
    end
    
    load(strcat(dataDir, 'avgFuncMat.mat'), 'avgFuncMat');
    FC_Z = avgFuncMat;
    normAngleMatrix = connectivity2normangle(FC_Z, 90);
    [FCgrad, results] = mica_diffusionEmbedding(normAngleMatrix, 'ncomponents', 10, 'symmetryMargin', 1e-05);
    
end

%% 
bin_num = [2; 3; 4; 5];

[~, idx] = sort(FCgrad(:,1));
FUrank = sort_back((1:length(FCgrad(:,1)))', idx);

f = figure;
for x = 1:length(bin_num)
   
    bins = discretize(FUrank, bin_num(x));

    for y = 1:bin_num(x)
        
        tmpEmbed = [];
        normAngleMatrix = connectivity2normangle(MPC(bins==y,bins==y), 90);
        [tmpEmbed, ~] = mica_diffusionEmbedding(normAngleMatrix, 'ncomponents', 1, 'symmetryMargin', 1e-05);
        deepEmbed(bins==y,x) = rescale(tmpEmbed(:,1), min(FUrank(bins==y)), max(FUrank(bins==y)));
        
    end
    
    
    [f, xi] = ksdensity(deepEmbed(:,x));
    a(x) = axes('position', [0.01+((x-1)*0.25) 0.7 0.25 0.15]);
    patch(xi, f, xi); axis off
    colormap(inferno);
    
    DOnSurf = BoSurfStatMakeParcelData(deepEmbed(:,x), C10, HCP_s20);
    DOnSurf = DOnSurf.* mask;
    D1s = SurfStatSmooth(DOnSurf, C10, 5);
    positions = [0.01+((x-1)*0.25) 0.5 0.12 0.12; 0.01+((x-1)*0.25) 0.38 0.12 0.12; ...
        0.1+((x-1)*0.25) 0.38 0.12 0.12; 0.1+((x-1)*0.25) 0.5 0.12 0.12];
    extent = [min(D1s) max(D1s)];
    ax = 1:4;
    BoSurfStat_calibrate4Views(D1s, C10, positions, ax, extent, inferno)
    
    corr(deepEmbed(:,x), FUrank')
    
end
 
  for z = 1:10  
      for y = 1:bin_num(x)

           tmp = FUrank(bins==y);
           newtmp(bins==y) = tmp(randperm(length(tmp)));

      end
      corr(newtmp', FUrank')
  end
  





