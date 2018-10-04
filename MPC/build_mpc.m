function [MPC, I, problemNodes] = build_mpc(data, parc)

%   build_mpc   Construct a microstructure profile covariance matrix
%   
%   INPUT
%   data        surfaces x vertices matrix containing intensity values
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
    parceldata      = zeros(size(data,1),length(uparcel)); 
    
    for ii = 1:length(uparcel)
        thisparcel                  = uparcel(ii);
        tmpdata                     = data(:,parc==thisparcel);
        tmpdata(:,mean(tmpdata)==0) = [];
    
        % change outliers to nan
        % isoutlier is a builtin function of matlab17b and later
        % add the isoutlier script from this package to your path for
        % earlier matlab versions
        idx                     = isoutlier(mean(tmpdata));
        outliers(ii)            = sum(idx);
        tmpdata2                = tmpdata;
        tmpdata2(1:end,idx)     = NaN;
    
        % parcel, ignoring nans
        I(:,ii)        = nanmean(tmpdata2,2);
    end       
    szI = [size(data,1) length(unique(parc))];
    szZ = [length(unique(parc)) length(unique(parc))];
else
    I = data;
    szI = size(data);
    szZ = [size(data,2) size(data,2)];
end
             
if nnz(isnan(I)) > 0
    
    problemNodes = find(isnan(I(1,:)));
    disp('warning: problem with parcellation, mpc will be NaNs')
    I = NaN(szI);
    MPC = NaN(szZ);
    
    
else
    
    problemNodes = 0;
    % create MPC matrix from partial correlation
    R = partialcorr(I, mean(I,2));
    % remove negative values
    R(R<0) = 0;
    % log transformation
    MPC = 0.5 * log( (1+R) ./ (1-R));
    MPC(isnan(MPC))     = 0; MPC(isinf(MPC)) = 0;
    
end


            