%% SurfStat Tutorial Hands on session
% make sure that you are in windows keyboard mode (
% in top: Home >> Preferences >> Keyboad >> Shortcuts >> Windows Default Set
% then go to editor on top 

%% 0. define directory and add toolbox
P='//Users/'; 
addpath([P 'surfstat'])


%% 1. Load the surface data 
SP = SurfStatAvSurf({[P 'fsaverage5/lh.pial'],[P 'fsaverage5/rh.pial']})
SW = SurfStatAvSurf({[P 'fsaverage5/lh.white'],[P 'fsaverage5/rh.white']})

% generate a mid thickness surface 
SM.coord = (SP.coord + SW.coord)./2; 
SM.tri   = SP.tri; 


%% 2. load brain mask and some useful surface features 
load([P 'fsaverage5/mask.mat']), 
load([P 'fsaverage5/curv.mat'])



%% 3a. Display what we have been loading, first the brain masks 

% first the brain mask  
f=figure, 
SurfStatViewData(double(mask),SW,'mask on white matter surface')

f=figure,
SurfStatViewData(double(mask),SP, 'mask on pial surface')

f=figure,
SurfStatViewData(double(mask),SM, 'mask on mid-thickness surface')


%% 3b. Display some useful features, such as mean curvature 
% then the curvature data 
f=figure,
SurfStatViewData(curv, SM, 'curvature')

% and now a binarized colormap 
f=figure,
SurfStatViewData(sign(curv), SM, 'curvature, signed')
colormap([0.6 .6 .6; .8 .8 .8])



    
%%  4. ready for some analysis: load the spreadsheet  
% load csv file that contains our participant ids, groups and IVs 
fid      = fopen([P 'myStudy.csv']); % final group
C        = textscan(fid,'%s%s%n%s%n','Delimiter',',',...
                    'headerLines',1,'CollectOutput',1);
fclose(fid);

% we have to do a little bit of recoding 
ID       = C{1}(:,1); 
GR       = C{1}(:,2);
AGE      = C{2};
HAND     = C{3};
IQ       = C{4};


%% 4b. Load the thickness data
% generate the file names 
left    = strcat(P, 'thickness/', ID, '_lh2fsaverage5_20.mgh');
right   = strcat(P, 'thickness/', ID, '_rh2fsaverage5_20.mgh');

% load data into a matrix
T       = SurfStatReadData([left, right]); 


%% 4c. Display data that we just loaded 

% this is the data matrix 
f=figure, 
    imagesc(T,[1.5 4])
    colormap(parula)

    
% this is the first case     
f=figure, 
    SurfStatViewData(T(1,:),SM, 'first case') 
    SurfStatColLim([1.5 4])
    colormap(parula)
  
% this is the mean thickness across cases     
f=figure, 
    SurfStatViewData(mean(T,1),SM, 'mean thickness across all subjects') 
    SurfStatColLim([1.5 4])
    colormap(parula)

% this is the standard deviation across cases     
f=figure, 
    SurfStatViewData(std(T,0,1),SM, 'std thickness across all subjects') 
     SurfStatColLim([0 .5])
    colormap(hot)
    

    
%% 5a. now we can finally do a first models: effects of age

% first code some variables of interest  
A  = term(AGE); 

% then build a model 
M = 1 + A; 
f=figure, image(M)

% estimaste the model parameter s
slm = SurfStatLinMod(T, M, SW); 

% specifiy contrast 
slm = SurfStatT(slm, -AGE)

% display t-value 
f=figure 
    SurfStatViewData(slm.t, SM, 't-value') 
 
    
%% 5b. Multiple comparisons correction    

% alternative 1: none - we show uncorrected p-values, good for exploration
p = 1-tcdf(slm.t,slm.df); 
f=figure 
    SurfStatViewData(p, SM, 'p-value') 
    SurfStatColLim([0 0.05]) 
    colormap([parula; .8 .8 .8])

%%    
% alternative 2: Bonferroni correction, generally very severe 
p = 1-tcdf(slm.t,slm.df); 
p = p*size(p,2); 
f=figure 
    SurfStatViewData(p, SM, 'Bonferroni p-value') 
    SurfStatColLim([0 0.05]) 
    colormap([parula; .8 .8 .8])
 
%%    
% alternative 3: multiple comparions using fdr     
qval = SurfStatQ(slm,mask);     
f=figure 
    SurfStatView(qval, SM, 'fdr') 
 
%%    
% multiple comparions using random field theory          
pval = SurfStatP(slm,mask);     
f=figure 
    SurfStatView(pval, SM, 'rft') 

  
    
%% 6a: group comparison, with correction for age

% specify the terms 
A  = term(AGE); 
G  = term(GR); 

% model definition 
M = 1 + A + G; 

% model fitting 
slm = SurfStatLinMod(T, M, SW); 

% contrast 
slm = SurfStatT(slm, G.Group1-G.Group2)

%%
% display p-value 
f=figure 
    SurfStatViewData(slm.t, SM, 't-value') 

% fdr     
qval = SurfStatQ(slm,mask);     
f=figure 
    SurfStatView(qval, SM, 'fdr') 

% FWE at conservative CDTs     
pval = SurfStatP(slm,mask);     
f=figure 
    SurfStatView(pval, SM, 'rtf') 
    
% FWE at exploratory CDTs     
pval = SurfStatP(slm,mask, 0.025);     
f=figure 
    SurfStatView(pval, SM, 'rtf') 



    
%% not covered but for completeness: interactions

% terms 
A  = term(AGE); 
G  = term(GR); 

% model definition with interaction
M = 1 + A + G + A*G;  

% parameter estimation
slm = SurfStatLinMod(T, M, SW); 

% contrast (a bit more complex for interactions)
slm = SurfStatT(slm, (-AGE.*G.Group2)-(-AGE.*G.Group1))

%% display results 
f=figure 
    SurfStatViewData(slm.t, SM, 't-value') 


%% covariance
Seed    = T(:,14446); 
S       = term(Seed)

% group difference 
M = 1 + S;  
slm = SurfStatLinMod(T, M, SW); 
slm = SurfStatT(slm, Seed)

f=figure 
    SurfStatViewData(slm.t, SM, 't-value') 
    SurfStatColLim([0 12])
    colormap([0.8 .8 .8; parula])

    
    
