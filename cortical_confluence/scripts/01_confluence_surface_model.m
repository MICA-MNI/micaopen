% 01_confluence_surface_model.m

for set_up = 1
    
    micaopen    = '/path/to/parent/directory/';
    mainDir     = [micaopen '/CorticalConfluence/'];
    
    % scripts
    addpath(genpath([GH '/micaopen/'])) 
    
end

%% HIPPOCAMPAL PROFILES
for hippocampus_fresh = 1
    
    APres = 512; PDres = 256; IOres = 16;
   
    for right = 1

        x_world = [1:998; rescale(1:998, 2.4, 42)];
        y_world = [1:1324; rescale(1:1324, -17.7, 35.3)];
        z_world = [1:1082; rescale(1:1082, -36.6, 6.5)];

        % load coordinates
        load([mainDir '/data/LaminarFeatures/Vxyz-Isovolume_hemi-R.mat']);
        Vxyz = round(Vxyz);
        inds = sub2ind(sz, Vxyz(:,1),Vxyz(:,2),Vxyz(:,3));
        bad = isnan(inds);
        inds(bad) = 1;
        Vxyz_reshape = reshape(Vxyz,[(APres*PDres),(IOres),3]);

        % make triangles for the inner surface
        inner_surf.coord = squeeze(Vxyz_reshape(:,1,:))';
        t = [1:(APres+1)*(PDres+1)]';
        F = [t,t+1,t+(APres+1) ; t,t-1,t-(APres+1)];
        badfaces = any(F>(APres)*(PDres) | F<=0 , 2);
        F(badfaces,:) = [];
        inner_surf.tri = F;
        bad_tri = nan(length(inner_surf.tri), 1);  % remove big triangles
        parfor ii = 1:length(inner_surf.tri)
            if range(inner_surf.coord(2,inner_surf.tri(ii,:))) > 400
                bad_tri(ii) = 1;
            else
                bad_tri(ii) = 0;
            end
        end
        inner_surf.tri(bad_tri==1,:) = [];
        trisurf(inner_surf.tri, inner_surf.coord(1,:), inner_surf.coord(2,:),inner_surf.coord(3,:));

        % downsample   
        numFaces    = round(length(inner_surf.tri)/50);                     % fifty-fold downsample
        patchNormal = patch('Faces', inner_surf.tri, 'Vertices', inner_surf.coord','Visible','off');
        Lds         = reducepatch(patchNormal,numFaces);
        [~,indexR]  = intersect(patchNormal.Vertices,Lds.vertices,'rows');      % index of selected vertices
        
        % select and rescale
        inner_surf.tri      = double(Lds.faces);
        inner_surf.coord    = zeros(3, length(Lds.vertices));
        for ii = 1:length(Lds.vertices)
            inner_surf.coord(1,ii) = x_world(2,Lds.vertices(ii,1)==x_world(1,:));
            inner_surf.coord(2,ii) = y_world(2,Lds.vertices(ii,2)==y_world(1,:));
            inner_surf.coord(3,ii) = z_world(2,Lds.vertices(ii,3)==z_world(1,:));
        end
        
        % and for outer surface
        outer_surf.tri      = inner_surf.tri;
        outer_surf.coord    = zeros(3, length(Lds.vertices));
        these_verts = squeeze(Vxyz_reshape(indexR,end,:));
        for ii = 1:length(Lds.vertices)
                outer_surf.coord(1,ii) = x_world(2,these_verts(ii,1)==x_world(1,:));
                outer_surf.coord(2,ii) = y_world(2,these_verts(ii,2)==y_world(1,:));
                outer_surf.coord(3,ii) = z_world(2,these_verts(ii,3)==z_world(1,:));
        end
       
        % AP PD IO
        APsamp = [1:APres]/(APres+1); 
        PDsamp = [1:PDres]/(PDres+1); 
        IOsamp = [1:IOres]/(IOres+1); 
        [v,u,w] = meshgrid(PDsamp,APsamp,IOsamp); % have to switch AP and PD because matlab sucks
        Vuvw = [u(:),v(:),w(:)];
        Vuvw_reshape    = reshape(Vuvw,[(APres*PDres),(IOres),3]);
        positioning     = squeeze(Vuvw_reshape(indexR,end,:));
        AP_hipp         = positioning(:,1);
        PD_hipp         = positioning(:,2);
        trisurf(inner_surf.tri, inner_surf.coord(1,:), inner_surf.coord(2,:),inner_surf.coord(3,:), PD_hipp);
        
        % get region labels
        ManSeg = load_nii([mainDir '/data/BIDS_40um/manual_masks/sub-bbhist/anat/sub-bbhist_hemi-R_label-HippSubfieldsJD.nii']);
        ManSeg = ManSeg.img;
        flatmap = ManSeg(inds);
        flatmap(bad) = nan;
        flatmap = ManSeg(inds);
        flatmap(flatmap<7 | flatmap>11) = nan; % segmented values are all >7 (otherwise may be cyst or SRLM)
        flatmap = reshape(flatmap,[(APres),(PDres),(IOres)]);
        flatmap = fillmissing(flatmap,'nearest');
        ManualSubfieldborders = [];
        ManualSubfieldborders(:,:) = mode(flatmap,3);
        subfields = reshape(ManualSubfieldborders,[(APres*PDres), 1]);
        region_hipp = subfields(indexR);
        trisurf(inner_surf.tri, inner_surf.coord(1,:), inner_surf.coord(2,:),inner_surf.coord(3,:), region_hipp);
        
        save([mainDir 'output/hipp_right_coord.mat'], 'inner_surf', 'outer_surf', 'PD_hipp', 'AP_hipp', 'region_hipp');
        
    end    
   
end

%% LINKING THE HIPPOCAMPUS AND CORTEX
for confluence = 1
    
    % hippocampal profiles
    load([mainDir 'output/hipp_right_coord.mat']);

    % from pial to the inner surface
    P = SurfStatReadSurf({[data '/dependencies/gray_right_327680.obj']});
    I = inner_surf;
    
    % remove "wall" vertices
    % conditioned on unknown + superior to the closest hippocampal
    % bridgehead
    load([micaopen '/data/bigbrain_wall.mat']);
    wall_idx = find(bigbrain_wall==1);
    rm_idx = zeros(1,length(P.coord));
    PD1 = find(PD_hipp==min(PD_hipp));
    n1 = length(PD1);
    for ii = 1:length(wall_idx) 
        d = sqrt(sum((repmat(P.coord(:,wall_idx(ii)),1,n1) - I.coord(:,PD1)).^2));
        d = abs(diff([repmat(P.coord(2,wall_idx(ii)),1,n1); I.coord(2,PD1)]));
        [~, closest_bridgehead] = min(d);
        if P.coord(3,wall_idx(ii)) - I.coord(3,PD1(closest_bridgehead)) > 0
            rm_idx(wall_idx(ii)) = 1;
        end
    end
    P_slim = remove_vertices(P, rm_idx);
  
    % find links along the proximal edge of the hippocampus
    edg = SurfStatEdg(I);
    new_tri = [0 0 0];
    n1 = length(P_slim.coord);
    for ii = 1:length(PD1)
       potential_edge = [edg(edg(:,1)==PD1(ii),2); edg(edg(:,2)==PD1(ii),1)];
       good_edge = potential_edge(ismember(potential_edge, PD1));  % matching to other edge vertices of the hippocampus
        if length(good_edge)>2  % take the closest in each direction
           clear tmp 
           y_shift = I.coord(2,good_edge) - I.coord(2,PD1(ii));
            y_shift(y_shift<0) = nan;
            [~, tmp(1)] = min(y_shift);
            y_shift = I.coord(2,good_edge) - I.coord(2,PD1(ii));
            y_shift(y_shift>0) = nan;
            [~, tmp(2)] = max(y_shift);
            good_edge = good_edge(tmp);
       end
       cort_vert = zeros(1,2);
       for jj = 1:length(good_edge)
           d1 = sqrt(sum((repmat(I.coord(:,PD1(ii)),1,n1) - P_slim.coord).^2));
           d2 = sqrt(sum((repmat(I.coord(:,good_edge(jj)),1,n1) - P_slim.coord).^2));
           [min_d, idx_d] = min(sum([d1; d2]));                  % find nearest cortical vertex for the hippocampal pair
           cort_vert(1,jj) = idx_d(1)+length(I.coord);
           new_tri = [new_tri; double([PD1(ii) good_edge(jj)  cort_vert(1,jj)])];
       end
       if length(good_edge) == 2
            new_tri = [new_tri; double([PD1(ii) cort_vert(1,:)])];  % make a triangle between the bridgehead and the cortical pair
       end
    end   
    new_tri(1,:) = [];
    
    % create the confluence surface
    C.coord = [I.coord P_slim.coord];
    C.tri   = [I.tri; P_slim.tri+length(I.coord); new_tri];
    for ii = 1:length(C.tri)
       bad_row(ii) = length(unique( C.tri(ii,:)));
    end
    C.tri(bad_row<3,:) = [];
    
    % check for fewer triangles than neibouring vertices
    parc_conf = [ones(1,length(I.coord))'; bigbrain_wall(~rm_idx)];
    wall_idx_con = find(bigbrain_wall);
    unique_triangles = unique(sort(C.tri,2), 'rows', 'stable');
    edg=unique([unique_triangles(:,[1 2]); unique_triangles(:,[1 3]); unique_triangles(:,[2 3])],'rows');
    edg=SurfStatEdg(C);
    new_tri = [0 0 0];
    for ii = 1:length(wall_idx_con)
        % check that there are two unique triangles with each neighbour
        [which_edg, ~] = find(edg==wall_idx_con(ii));
        these_edg = edg(which_edg,:);
        for jj = 1:size(these_edg,1)
           which_tri = find(sum((these_edg(jj,1)==C.tri)  + (these_edg(jj,2)==C.tri),2)==2);
           num_tri = size(unique(sort(C.tri(which_tri,:),2), 'rows'),1);
           if num_tri < 2
               % find any linked neighbours and join the three
                new_vert = these_edg(jj,:); new_vert(new_vert==wall_idx_con(ii)) = [];
                [which_edg, ~] = find(edg==new_vert);
                these_edg2 = unique(edg(which_edg,:));
                potential_edges = these_edg2(ismember(these_edg2, these_edg));
                potential_edges(potential_edges==wall_idx_con(ii)) = [];
                potential_edges(potential_edges==new_vert) = [];
                for kk = 1:size(potential_edges,1)
                   new_tri = [new_tri;  wall_idx_con(ii) new_vert potential_edges(kk)];
                end  
           end
        end
    end
    new_tri(1,:) = [];
    C.tri = [C.tri; new_tri];
    
    save([mainDir 'output/confluent_surface_right.mat'], 'C', 'PD1', 'parc_conf');
  
end

%% SAMPLE AND VISUALISE INTRACORTICAL SURFACES
% for outer/wm surface
O = outer_surf;
W = SurfStatReadSurf([mainDir '/data/white_right_327680.obj']);
W_slim = remove_vertices(W, rm_idx);
Co.coord = [O.coord W_slim.coord];
Co.tri = C.tri;

% get coordinates for equivolumteric surfaces and save out
new_coords = equivolumetric_surfaces(C, Co,14);
AllEvSurf = zeros(3,16,length(C.coord));
AllEvSurf(:,1,:) = C.coord;
AllEvSurf(:,2:15,:) = permute(real(new_coords), [1 3 2]);
AllEvSurf(:,16,:) = Co.coord;
save([homeDir 'constructs/AllEvSurf_right.mat'], 'AllEvSurf')

%% PROXIMITY TO BRIDGEHEADS
tmp = imGeodesicSurface(Cslim, [homeDir '/data/full8_400um_2009b_sym_rsp.nii'], PD1, zeros(1,length(Cslim.coord)));
bridge_dist = min(tmp);
bridge_dist(length(inner_surf.coord)+1:end) = bridge_dist(length(inner_surf.coord)+1:end)*-1;