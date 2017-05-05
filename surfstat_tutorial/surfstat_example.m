%% get this turial from mica-mni.github.io/micaopen/surfstat_tutorial/

%% set path to dowloaded location
P='/Users/boris/GitHub/micaopen/surfstat_tutorial/'; 
addpath([P 'surfstat'])


%% 1. Load the surface data 
cd([P 'fsaverage5'])
SP = SurfStatAvSurf({'lh.pial','rh.pial'})
SW = SurfStatAvSurf({'lh.white','rh.white'})

% generate a mid thickness surface 
SM.coord = (SP.coord + SW.coord)./2; 
SM.tri   = SP.tri; 


%% 2. load brain mask and some useful surface features 
cd([P 'fsaverage5'])
load('mask.mat'), 
load('curv.mat')
load('yeo.mat')
load('aparc.mat')
load('lobes.mat')


%% 3. Display what we have been loading

% first the brain mask  
f=figure, 
SurfStatViewData(double(mask),SW,'mask on white matter surface')

f=figure,
SurfStatViewData(double(mask),SP, 'mask on pial surface')

f=figure,
SurfStatViewData(double(mask),SM, 'mask on mid-thickness surface')

% then the curvature data 
f=figure,
SurfStatViewData(curv, SM, 'curvature')

% and now a binarized colormap 
f=figure,
SurfStatViewData(sign(curv), SM, 'curvature, signed')
colormap([0.6 .6 .6; .8 .8 .8])

% 3 different parcellations maybe 
f=figure, 
    subplot(1,3,1), SurfStatView1(yeo,SM)
    subplot(1,3,2), SurfStatView1(aparc,SM)
    subplot(1,3,3), SurfStatView1(lobes,SM)

    
%%  ready for some analysis! 
% load csv file that contains our participant ids, groups and IVs 
cd(P)
fid      = fopen('myStudy.csv'); % final group
C        = textscan(fid,'%s%s%n%s%n','Delimiter',',',...
                    'headerLines',1,'CollectOutput',1);
fclose(fid);
    
ID       = C{1}(:,1); 
GR       = C{1}(:,2);
AGE      = C{2};
HAND     = C{3};
IQ       = C{4};


% then we load the thickness data  
left    = strcat(ID, '_lh2fsaverage5_20.mgh');
right   = strcat(ID, '_rh2fsaverage5_20.mgh');

cd([P 'thickness'])
T       = SurfStatReadData([left, right]); 


% we could verify whether all looks great 
f=figure, 
    imagesc(T,[1.5 4])
    colormap(parula)
    
f=figure, 
    SurfStatViewData(T(1,:),SM, 'first case') 
    SurfStatColLim([1.5 4])
    colormap(parula)
    
f=figure, 
    SurfStatViewData(mean(T,1),SM, 'mean thickness across all subjects') 
    SurfStatColLim([1.5 4])
    colormap(parula)
    
f=figure, 
    SurfStatViewData(std(T,0,1),SM, 'std thickness across all subjects') 
     SurfStatColLim([0 .5])
    colormap(hot)
    

    
%% now we can finally do a first models: lets look at effects of age

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
 
    
% multiple comparison correction: none
p = 1-tcdf(slm.t,slm.df); 
f=figure 
    SurfStatViewData(p, SM, 'p-value') 
    SurfStatColLim([0 0.05]) 
    colormap([parula; .8 .8 .8])
    
% multiple comparison correction: Bonferroni
p = 1-tcdf(slm.t,slm.df); 
p = p*size(p,2); 
f=figure 
    SurfStatViewData(p, SM, 'Bonferroni p-value') 
    SurfStatColLim([0 0.05]) 
    colormap([parula; .8 .8 .8])
    
% multiple comparions using fdr     
qval = SurfStatQ(slm,mask);     
f=figure 
    SurfStatView(qval, SM, 'fdr') 
   
% multiple comparions using random field theory          
pval = SurfStatP(slm,mask);     
f=figure 
    SurfStatView(pval, SM, 'rft') 

% the findings are hyper significant - so we can threshold very agressively     
f=figure 
    SurfStatView(pval.P, SM, 'rft') 


    
%% so we know that age is important - lets control for it when assessing group differences 
A  = term(AGE); 
G  = term(GR); 

% group difference 
M = 1 + A + G; 
slm = SurfStatLinMod(T, M, SW); 
slm = SurfStatT(slm, G.Group1-G.Group2)

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



%% lets assess interactions
A  = term(AGE); 
G  = term(GR); 

% group difference 
M = 1 + A + G + A*G;  
slm = SurfStatLinMod(T, M, SW); 
slm = SurfStatT(slm, (-AGE.*G.Group2)-(-AGE.*G.Group1))

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

    
    