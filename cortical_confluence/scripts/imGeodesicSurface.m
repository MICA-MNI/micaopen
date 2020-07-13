function dist = imGeodesicSurface(surface, volume_file, startpoints, ignore)

% use surface to volume projections and imGeoDist to map distances
% input:
% surface           surface structure in SurfStat format
% volume_file       template volume (ensure SurfStat compatability) -
%                   doesn't necessarily need to be matched to the surface, I think, but is
%                   used as a basic template for header information
% startpoints       list of coordinates of start points in surface space (n x 3) or 
%                   vertex indicies corresponding to the surface (n x 1)                   
% ignore            exclusion mask in surface space (1 x length(surface.coord))

% written by Casey Paquola @ MICA, MNI, 2020*

% shift to positive space and round numbers
Surfpos = surface;
Surfpos.coord = round(surface.coord + abs(min(surface.coord'))') + 2;

% project the surface to volume space
vol = SurfStatReadVol1(volume_file);
vol.dim = ceil(max(Surfpos.coord'));  % change dimensions to suit the specific surface
vol.origin = [0 0 0];                 % set origin to the corner of the FOV
vol.data = zeros(vol.dim);            % empty data
for ii = 1:length(Surfpos.coord)
    if ignore(ii)==0                      % don't map the exclusion mask to the volume
        this = [Surfpos.coord(:,ii)-1 Surfpos.coord(:,ii)+1];
        this(this==0) = 1;
        vol.data(this(1,1):this(1,2),this(2,1):this(2,2),this(3,1):this(3,2)) = 1;  % add data to points in the volumes, with 1 degree of padding
    end
end
vol.dim = size(vol.data); % update dimensions
vol.vox = [1 1 1];


% perform distance calculations
dist = zeros(length(startpoints), length(Surfpos.coord));
parfor ii = 1:length(startpoints)
  
    disp(ii);

    if size(startpoints,2) == 3
       seeds  = round(startpoints(ii,:)' + abs(min(surface.coord'))' + 1)';
    else
       seeds = Surfpos.coord(:,startpoints(ii));
    end
    
    % transform to volume space and allocate
    marker             = false(size(vol.data));
    marker(seeds(1), seeds(2), seeds(3)) = true;
   
    % calculate distance and add as data in a volume structure
    DIST               = imChamferDistance3d(vol.data, marker);
    DIST(isnan(DIST))  = 0; DIST(isinf(DIST)) = 0;
    
    % collect distance measurements
    V                  = vol; 
    V.data             = DIST; 
    dist(ii,:)  = CPSurfStatVol2Surf(V,Surfpos);
    
end