function BoSurfStatViewsFlex( data, mask, vol, my_range, orientation,varargin);

%Viewer for slices of volumetric data.
%
% Usage: SurfStatViews( data, vol [, z [, layout ]] );
%
% data       = n x v matrix of data if k=1, or n x v x k array of data if 
%              k>1, or a memory map of same.
% vol.lat    = nx x ny x nz logical array, 1=in, 0=out.
% vol.vox    = 1 x 3 vector of voxel sizes in mm.
% vol.origin = position in mm of the first voxel.
% z          = 1 x s vector of z coordinates of slices. Default is 0.
%              The nearest slices are displayed. 
% layout     = matrix of indices from 1:(n*k*s) specifying which slice
%              appears in position layout(i,j), with 0 for an empty image.
%              Default is reshape(1:(n*k*s),n,k*s).


newdata = reshape(data,[size(vol.lat,1) size(vol.lat,2) 1 size(vol.lat,3)]);
newmask = reshape(mask,[size(vol.lat,1) size(vol.lat,2) 1 size(vol.lat,3)]);
newdata(newmask==0) = -6666; 

% if axial
if strcmp(orientation,'axl') 
    newdata = permute(newdata,[2 1 3 4]);
% if coronal
elseif strcmp(orientation,'cor') 
    newdata = permute(newdata,[4 1 3 2]);
    newdata = flipdim(newdata,1);
% sagittal 
elseif strcmp(orientation,'sag') 
    newdata = permute(newdata,[4 2 3 1]);
    newdata = flipdim(newdata,1);
end

montage(newdata,'DisplayRange', my_range, varargin{:});
colorbar; colormap(spectral(256));

if strcmp(orientation,'axl') 
     xlabel('axial (L >> R)'); ylabel('top >> bottom'); 
elseif strcmp(orientation,'cor') 
     xlabel('coronal (L>>R)'); ylabel('front >> back'); 
elseif strcmp(orientation,'sag') 
    xlabel('sagittal'); ylabel('right >> left'); 
end
axis equal; axis off; 



background='black';
whitebg(gcf,background);
set(gcf,'Color',background,'InvertHardcopy','off');

set(gcf,'PaperPosition',[0.25 2.5 6 4.5]);