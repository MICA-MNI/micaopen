<<<<<<< Updated upstream
function [a,cb]=BoSurfStatViewData2(data,surf,title,background,clim);
=======
function [a,cb]=BoSurfStatViewData(data,surf,title,background);
>>>>>>> Stashed changes

%BoSurfStatViewData is a simple viewer for surface data.
% 
% Usage: [a,cb]=BoSurfStatViewData(data, surf [,title [,background]]);
% 
% data        = 1 x v vector of data, v=#vertices
% surf.coord  = 3 x v matrix of coordinates.
% surf.tri    = 3 x t matrix of triangle indices, 1-based, t=#triangles.
% title       = any string, data name by default.
% background  = background colour, any matlab ColorSpec, such as 
%   'white' (default), 'black'=='k', 'r'==[1 0 0], [1 0.4 0.6] (pink) etc.
%   Letter and line colours are inverted if background is dark (mean<0.5).
%
% a  = vector of handles to the axes, left to right, top to bottom. 
% cb = handle to the colorbar.

if nargin<3 
    title=inputname(1);
end
if nargin<4
    background='white';
end

v=length(data);
vl=1:(v/2);
vr=vl+v/2;
t=size(surf.tri,1);
tl=1:(t/2);
tr=tl+t/2;
<<<<<<< Updated upstream
if nargin<5
    
    clim=[min(data),max(data)];

    if clim(1)==clim(2)
        clim=clim(1)+[-1 0];
    end
end
=======
clim=[min(data),max(data)];
if clim(1)==clim(2)
    clim=clim(1)+[-1 0];
end

>>>>>>> Stashed changes
clf;
colormap(spectral(256));


<<<<<<< Updated upstream
h=0.25;
w=0.20;

a(1)=axes('position',[0.3 0.6 w h]);
=======
h=0.27;
w=0.23;

a(1)=axes('position',[0.26 0.55 w h]);
>>>>>>> Stashed changes
trisurf(surf.tri(tl,:),surf.coord(1,vl),surf.coord(2,vl),surf.coord(3,vl),...
    double(data(vl)),'EdgeColor','none');
view(-90,0); 
daspect([1 1 1]); axis tight; camlight; axis vis3d off;
lighting phong; material dull; shading interp;

<<<<<<< Updated upstream
a(2)=axes('position',[0.3+w 0.6 w h]);
=======
a(2)=axes('position',[0.26+w 0.55 w h]);
>>>>>>> Stashed changes
trisurf(surf.tri(tl,:),surf.coord(1,vl),surf.coord(2,vl),surf.coord(3,vl),...
    double(data(vl)),'EdgeColor','none');
view(90,0); 
daspect([1 1 1]); axis tight; camlight; axis vis3d off;
lighting phong; material dull; shading interp;

<<<<<<< Updated upstream
a(3)=axes('position',[0.3 0.3 w h]);
=======
a(3)=axes('position',[0.26 0.33 w h]);
>>>>>>> Stashed changes
trisurf(surf.tri(tr,:)-v/2,surf.coord(1,vr),surf.coord(2,vr),surf.coord(3,vr),...
    double(data(vr)),'EdgeColor','none');
view(-90,0); 
daspect([1 1 1]); axis tight; camlight; axis vis3d off;
lighting phong; material dull; shading interp;

<<<<<<< Updated upstream
a(4)=axes('position',[0.3+w 0.3 w h]);
=======
a(4)=axes('position',[0.26+w 0.33 w h]);
>>>>>>> Stashed changes
trisurf(surf.tri(tr,:)-v/2,surf.coord(1,vr),surf.coord(2,vr),surf.coord(3,vr),...
    double(data(vr)),'EdgeColor','none');
view(90,0); 
daspect([1 1 1]); axis tight; camlight; axis vis3d off;
lighting phong; material dull; shading interp;


for i=1:length(a)
    set(a(i),'CLim',clim);
    set(a(i),'Tag',['SurfStatView ' num2str(i) ]);
end

<<<<<<< Updated upstream

cb=colorbar('location','South');
set(cb,'Position',[0.35 0.22 0.3 0.03]);
=======
cb=colorbar('location','East');
set(cb,'Position',[0.8 0.47 0.05 0.2]);
>>>>>>> Stashed changes
set(cb,'XAxisLocation','bottom');
h=get(cb,'Title');
set(h,'String',title);

whitebg(gcf,background);
set(gcf,'Color',background,'InvertHardcopy','off');

dcm_obj=datacursormode(gcf);
set(dcm_obj,'UpdateFcn',@SurfStatDataCursor,'DisplayStyle','window');
colormap parula

return
end
