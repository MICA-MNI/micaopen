function a = CP_SurfStatViewEdges( edge_coords, edge_weight, surf, cmap)

%Basic viewer for surface data.
% 
% Usage: [ a, cb ] = CP_SurfStatViewEdges( data, surf [,title [,background]] );
% 
% data        = v x v matrix of edge-wise data, v=#vertices
% surf.coord  = 3 x v matrix of coordinates.
% surf.tri    = t x 3 matrix of triangle indices, 1-based, t=#triangles.
% title       = any string, data name by default.
% background  = background colour, any matlab ColorSpec, such as 
%   'white' (default), 'black'=='k', 'r'==[1 0 0], [1 0.4 0.6] (pink) etc.
%   Letter and line colours are inverted if background is dark (mean<0.5).
%
% a  = vector of handles to the axes, left to right, top to bottom. 
% cb = handle to the colorbar.

if nargin<4 
    cmap=parula;
end

% set up edge-wise colourmap
edge_colours = floor(rescale(edge_weight, 1, length(cmap)));

% find cut between hemispheres, assuming they are concatenated
t=size(surf.tri,1);
v=size(surf.coord,2);
tmax=max(surf.tri,[],2);
tmin=min(surf.tri,[],2);
% to save time, check that the cut is half way
if min(tmin(t/2+1:t))-max(tmax(1:t/2))==1
    cut=t/2;
    cuv=v/2;
else % check all cuts
    for i=1:t-1
        tmax(i+1)=max(tmax(i+1),tmax(i));
        tmin(t-i)=min(tmin(t-i),tmin(t-i+1));
    end
    cut=min([find((tmin(2:t)-tmax(1:t-1))==1) t]);
    cuv=tmax(cut);
end
tl=1:cut;
tr=(cut+1):t;
vl=1:cuv;
vr=(cuv+1):v;

h=0.39;
w=0.4;

r=max(surf.coord,[],2)-min(surf.coord,[],2);
w1=h/r(2)*r(1)*3/4;
h1=h/r(2)*r(1); % h/r(2)*r(3)

a(1)=axes('position',[0.055 0.62 h*3/4 w]);
for edge = 1:size(edge_coords,3)
   if sum(edge_coords(:,1,edge) < max(surf.coord(1,vl))) == 2
          plot3(edge_coords(:,1,edge), edge_coords(:,2,edge), ...
                edge_coords(:,3,edge), 'Color', cmap(edge_colours(edge),:),...
                'LineWidth', 1); hold on
   end
end
colormap(gray)
trisurf(surf.tri(tl,:),surf.coord(1,vl),surf.coord(2,vl),surf.coord(3,vl),...
    ones(1,length(vl)), 'EdgeColor','none');
alpha 0.15
view(-90,0); 
daspect([1 1 1]); axis tight; camlight; axis vis3d off;
lighting phong; material dull; shading interp;

a(2)=axes('position',[0.3 0.58 w h]);
for edge = 1:size(edge_coords,3)
          plot3(edge_coords(:,1,edge), edge_coords(:,2,edge), ...
                edge_coords(:,3,edge), 'Color', cmap(edge_colours(edge),:),...
                'LineWidth', 1); hold on
end
colormap(gray)
trisurf(surf.tri,surf.coord(1,:),surf.coord(2,:),surf.coord(3,:),...
    ones(1,length(surf.coord)),'EdgeColor','none');
alpha 0.15
view(0,90); 
daspect([1 1 1]); axis tight; camlight; axis vis3d off;
lighting phong; material dull; shading interp;

a(3)=axes('position',[1-0.055-h*3/4 0.62 h*3/4 w]);
for edge = 1:size(edge_coords,3)
   if sum(edge_coords(:,1,edge) > max(surf.coord(1,vl))) == 2
          plot3(edge_coords(:,1,edge), edge_coords(:,2,edge), ...
                edge_coords(:,3,edge), 'Color', cmap(edge_colours(edge),:),...
                'LineWidth', 1); hold on
   end
end
trisurf(surf.tri(tr,:)-cuv,surf.coord(1,vr),surf.coord(2,vr),surf.coord(3,vr),...
    ones(1,length(vr)),'EdgeColor','none');
alpha 0.15
view(90,0);
daspect([1 1 1]); axis tight; camlight; axis vis3d off;
lighting phong; material dull; shading interp;

return
end
