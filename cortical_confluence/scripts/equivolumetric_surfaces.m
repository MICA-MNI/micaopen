function new_coord = equivolumetric_surfaces(gm, wm, num_surfs)

% input:
% gm     upper, pial surface structure with coord and tri 
% wm     lower, white surface structure with coord and tri 


% translated to matlab from the surface-tools toolbox
% https://github.com/kwagstyl/surface_tools

% code is identical except for the calculation of area by BrainStorm tool
% rather than minctool

vectors= wm.coord - gm.coord;

% calculate area
wm.faces = wm.tri;
wm.vertices = wm.coord';
[~, ~, ~, ~, aw] = tessellation_stats(wm,0);
gm.faces = gm.tri;
gm.vertices = gm.coord';
[~, ~, ~, ~, ap] = tessellation_stats(gm,0);

for ii = 1:num_surfs
    
    disp(['creating surface-' num2str(ii)])
    
    % defining beta
    % Compute euclidean distance fraction, beta, that will yield the desired
    % volume fraction, alpha, given vertex areas in the white matter surface, aw,
    % and on the pial surface, ap. 
    % A surface with `alpha` fraction of the cortical volume below it and 
    % `1 - alpha` fraction above it can then be constructed from pial, px, and 
    % white matter, pw, surface coordinates as `beta * px + (1 - beta) * pw`.
    
    alpha = ii/(num_surfs-1);
    
    if alpha == 0
        betas = zeros(size(aw));
    elseif alpha == 1
        betas = ones(size(aw));
    else
        betas = 1-(1./(ap - aw) .* (-aw + sqrt((1-alpha)*(ap.^2) + alpha*(aw.^2))));
    end
    
    betas(isnan(betas)) = 0;
    betas(isinf(betas)) = 1;
    
    new_coord(:,:,ii)  = gm.coord + vectors.*betas;
        
end


