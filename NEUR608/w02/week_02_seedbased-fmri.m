%% --
% load this github from 
clear 
GH = '/Users/boris/Documents/1_github/micaopen'
addpath(genpath(GH))

myFile = 'ts.mat';
mySurf = 'SM.mat';
myYeo  = 'yeo.mat'; 
myLabel = 'label-Cambridge308.fsa5-LR.mat'

load(mySurf); 
load(myFile);
load(myYeo);
load(myLabel); 


f=figure, BoSurfStatViewData(label_fsa5, SM,'')

parcelts = mica_surfData2parcelData(ts, label_fsa5); 



%% --   
% build correlation matrix 
r               = corr(parcelts);
z               = 0.5 * log( (1+r) ./ (1-r) ); 
z(isinf(z))     = 0; 
z(isnan(z))     = 0;
    
f=figure, 
    imagesc(z,[0 1])
    
 

% build affinity matrix 

    
 