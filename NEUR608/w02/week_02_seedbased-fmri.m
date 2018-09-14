%% --
% load this github from 
GH = '/Users/boris/Documents/1_github/micaopen'
addpath(genpath(GH))

myFile = 'ts.mat';
mySurf = 'SM.mat';
myYeo  = 'yeo.mat'; 

load(mySurf); 
load(myFile);
load(myYeo);

%% --   
% build correlations 
r               = corr(ts);
z               = 0.5 * log( (1+r) ./ (1-r) ); 
z(isinf(z))     = 1; 
z(isnan(z))     = 1;
mPFC            = 730; 
PCC             = 3215; 
VIS             = 2748; 

f=figure;  
    SurfStatViewData(z(VIS,:),SM,'','black');
    SurfStatColLim([-0.7 0.7]);
    colormap(parula);
    

    
 