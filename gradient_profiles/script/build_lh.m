function [intra_dissimilarity_parcel,intra_dissimilarity_5k] = build_lh(MPCG,SCG,FCG,num_GS,num_parcel,num_vertex,mask,parcellation)
% output:
% intra_dissimilarity_parcel: a P by 1 vector. P is the number of parcels in atlas.
% intra_dissimilarity_5k: a V by 1 vector. V is the number of vertices.
%
% input:
% MPCG: microstructural gradients
% SCG: structural gradients
% FCG: functural gradients
% num_GS: number of gradients in each modality
% num_parcel: number of parcels in atlas
% mask: mask of cortex area
% parcellation: label of parcellation

% rescale gradients to [-1 1]
MPCGS   = MPCG(:,1:num_GS);
MPCGS   = MPCGS/max(max(abs(MPCGS)));
SCGS    = SCG(:,1:num_GS);
SCGS    = SCGS/max(max(abs(SCGS)));
FCGS    = FCG(:,1:num_GS); 
FCGS    = FCGS/max(max(abs(FCGS)));
gs_all	= [MPCGS,SCGS,FCGS];

% gradient profiles construction
gs_all_midw         = zeros(size(mask,1),num_GS*3);
gs_all_midw(mask,:) = gs_all; %_zscore

intra_dissimilarity_5k=zeros(num_vertex,1);
for ii=1:num_parcel
    % distance between vertices to mean GP within a parcel
    gs_parcel=gs_all_midw(parcellation==ii,:);
    gs_parcel_mean=mean(gs_parcel,1);% =median(gs_parcel,1);
    gs_temp=[gs_parcel_mean;gs_parcel];
    distance_mean_sub    = pdist(gs_temp,'cosine');
    distance_mean_sub = squareform(distance_mean_sub);
    intra_dissimilarity_5k(parcellation==ii,1)=distance_mean_sub(1,2:end)';
end
intra_dissimilarity_parcel=zeros(num_parcel,1);% intra distance average on each paecel
for ii=1:num_parcel
intra_dissimilarity_parcel(ii,1)=mean(intra_dissimilarity_5k(parcellation==ii),1);
end

