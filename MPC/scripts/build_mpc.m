function [MPC, I] = build_mpc(MP, parc)

%   build_mpc   Construct a microstructure profile covariance matrix
%   
%   INPUT
%   MP          surfaces x vertices matrix containing intensity values
%   parc        1 x vertices vector with unique integrers correpsonding to 
%               node assignment. Leave empty, [], for a vertex-wise MPC
%
%
%   OUTPUT
%   MPC         microstructural profile covariance matrix
%   I           microstructure intensity profiles (node-wise if parc is given)
%

if isempty(parc)
    downsample = 0;
else
    downsample = 1;
end
    
% parcellate vertices into nodes with provided parcellation scheme
if downsample==1
    uparcel         = unique(parc); 
    parcelMP      = zeros(size(MP,1),length(uparcel)); 
    
    for ii = 1:length(uparcel)
        thisparcel                  = uparcel(ii);
        tmpMP                     = MP(:,parc==thisparcel);
        tmpMP(:,mean(tmpMP)==0)   = [];
    
        % change outliers to nan
        % isoutlier is a builtin function of matlab17b and later
        % add the isoutlier script from this package to your path for
        % earlier matlab versions
        idx                     = isoutlier(mean(tmpMP));
        outliers(ii)            = sum(idx);
        tmpMP2                = tmpMP;
        tmpMP2(1:end,idx)     = NaN;
    
        % parcel, ignoring nans
        I(:,ii)        = nanmean(tmpMP2,2);
    end       
    szI = [size(MP,1) length(unique(parc))];
    szZ = [length(unique(parc)) length(unique(parc))];
else
    I = MP;
    szI = size(MP);
    szZ = [size(MP,1) size(MP,1)];
end
             
if nnz(isnan(I)) > 0
    
    disp('warning: problem with parcellation, mpc will be NaNs')
    I = NaN(szI);
    MPC = NaN(szZ);
    
else
    
    % create MPC matrix from partial correlation
    R = partialcorr(I, mean(I,2));
    
end


            