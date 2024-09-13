function [gradient_profile,inter_dissimilarity] = build_gh(MPCG,SCG,FCG,num_GS,num_parcel,mask,parcellation)
% output:
% inter_dissimilarity: a P by 1 vector. P is number of parcels in atlas.
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
% gradient_profile    = zeros(num_parcel,size(gs_all,2));
gs_all_midw         = zeros(size(mask,1),num_GS*3);
gs_all_midw(mask,:) = gs_all; %_zscore
for ii = 1:num_parcel
    label_parcel    = parcellation==ii;
    gradient_profile(ii,:) = mean(gs_all_midw(label_parcel,:),1); 
end
% compute cosine distance
d           = pdist(gradient_profile,'cosine');
z           = squareform(d);
inter_dissimilarity   = mean(z,1)';
