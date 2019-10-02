%% --
% load this github from 
clear 
GH = '/Users/boris/Documents/1_github/micaopen'
addpath(genpath(GH))

myFile = 'ts.mat';
mySurf = 'SM.mat';
myYeo  = 'yeo.mat'; 

load(mySurf); 
load(myFile);
load(myYeo);


f=figure, BoSurfStatViewData(yeo, SM,'')



%% --   
% build correlation matrix 
r               = corr(ts);
z               = 0.5 * log( (1+r) ./ (1-r) ); 
z(isinf(z))     = 0; 
z(isnan(z))     = 0;
    


f=figure, 
    imagesc(z,[0 1])

[sy, sindex] = sort(yeo); 
f=figure, 
    imagesc(z(sindex,sindex),[0 1])
    
% --     
mPFC            = 730; 
PCC             = 3215; 
VIS             = 2748; 

f=figure;  
    SurfStatViewData(z(VIS,:),SM,'','black')
    SurfStatColLim([-0.7 0.7]);
    colormap(parula);
    

    
 seed = ts(:,PCC); 
 rmap               = corr(seed, ts);
 f=figure;  
    SurfStatViewData(rmap,SM,'','black')
    SurfStatColLim([0 0.7]);