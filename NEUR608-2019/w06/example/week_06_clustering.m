%% init  

clear 
cd('/Users/boris/Documents/1_github/micaopen/NEUR608-2019/w06/example')
GH = '/Users/boris/Documents/1_github/micaopen'
addpath(genpath(GH))

load('Glasser2016.mat'); 
load('fsaverage.midthickness_mni_32k_fs_LR.mat');

parcels                 = parcellation210.indexmax; 
parcels(isnan(parcels)) = 0; 
f=figure; BoSurfStatViewData(parcels, G,''); colormap(linspecer)


%% load time series and build connectomes 
d = SurfStatListDir('HCP*'); 

for i = 1:length(d) 
    
    ts = load(d{i}); 
    r1 = corr(ts.rfMRI_REST1_LR); z1 = 0.5 * log( (1+r1) ./ (1-r1) ); 
    r2 = corr(ts.rfMRI_REST1_RL); z2 = 0.5 * log( (1+r2) ./ (1-r2) ); 
    r3 = corr(ts.rfMRI_REST2_LR); z3 = 0.5 * log( (1+r3) ./ (1-r3) ); 
    r4 = corr(ts.rfMRI_REST2_RL); z4 = 0.5 * log( (1+r4) ./ (1-r4) ); 
    z(:,:,i) = (z1+z2+z3+z4)./4; 
end 

z(isinf(z)) = 0; 
z(isnan(z)) = 0; 

meanz       = mean(z,3); 
f=figure;  
    imagesc(meanz,[0 1]); 

    
% visualize degree (to verify going back to surface)
dc                  = mean(meanz,2); 
dcmap               = mica_parcelData2surfData([0; dc], G, parcels); 
f = figure;    
    BoSurfStatViewData(dcmap, G,''); 
    
    
%%  k-means cluster, n=2
close all 
[cidx2,cmeans2]     = kmeans(meanz,2,'dist','cosine','Replicates',10);
[silh2,h]           = silhouette(meanz,cidx2,'cosine');
[scidx2, sindex]    = sort(cidx2); 


% display clustering 
f=figure;  
subplot(1,4,1), imagesc(cidx2); 
subplot(1,4,2), imagesc(meanz)
subplot(1,4,3), imagesc(scidx2);
subplot(1,4,4), imagesc(meanz(sindex,sindex));

cidx2map               = mica_parcelData2surfData([0; cidx2], G, parcels); 
f = figure;    
    BoSurfStatViewData(cidx2map, G,['2 clusters:' num2str(mean(silh2))]);    
    colormap(linspecer)

    
%% k-means cluster, n=7  
close all
n = 6
[cidxn,cmeans2]     = kmeans(meanz,n,'dist','cosine','Replicates',10);
[silhn,h]           = silhouette(meanz,cidxn,'cosine');
[scidxn, sindex]    = sort(cidxn); 


% display clustering 
f=figure;  
subplot(1,4,1), imagesc(cidxn); 
subplot(1,4,2), imagesc(meanz)
subplot(1,4,3), imagesc(scidxn);
subplot(1,4,4), imagesc(meanz(sindex,sindex));

cidxnmap    = mica_parcelData2surfData([0; cidxn], G, parcels); 
f = figure;    
    BoSurfStatViewData(cidxnmap, G,['7 clusters:' num2str(mean(silhn))]);   
    colormap(linspecer)

    
    
%% hierarchical 
d           = pdist(meanz,'cosine');
tree        = linkage(d,'average');
[h,nodes]   = dendrogram(tree,0);
t           = cluster(tree, 'MaxClust',7); 
tmap        = mica_parcelData2surfData([0; t], G, parcels); 
f = figure;    
    BoSurfStatViewData(tmap, G,['7 clusters hierarchical']);   
    colormap(linspecer)

