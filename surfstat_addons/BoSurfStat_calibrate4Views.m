function BoSurfStat_calibrate4Views(data, Slo, pos, handles, clim, cmap)
% function BoSurfStat_calibrate2Views(data, Slo, pos4by4, handes4by1, clim)
% shows lateral and medial for the left hemisphere at 1 specified position 
% vectors [x y h w] 
%
%
% author: boris@bic.mni.mcgill.ca
v=length(data);
vl=1:(v/2);
vr=vl+v/2;
t=size(Slo.tri,1);
tl=1:(t/2);
tr=tl+t/2;
a(handles(1)) =axes('position',[pos(1,1) pos(1,2) pos(1,3) pos(1,4)]);
trisurf(Slo.tri(tl,:),Slo.coord(1,vl),Slo.coord(2,vl),Slo.coord(3,vl),...
double(data(vl)),'EdgeColor','none');
view(-90,0); 
daspect([1 1 1]); axis tight; camlight; axis vis3d off;
lighting phong; material dull; shading interp;
set(a(handles(1)),'CLim',clim);   
colormap(a(handles(1)),cmap)

a(handles(2))=axes('position',[pos(2,1) pos(2,2) pos(2,3) pos(2,4)]);
trisurf(Slo.tri(tl,:),Slo.coord(1,vl),Slo.coord(2,vl),Slo.coord(3,vl),...
double(data(vl)),'EdgeColor','none');
view(90,0); 
daspect([1 1 1]); axis tight; camlight; axis vis3d off;
lighting phong; material dull; shading interp;
set(a(handles(2)),'CLim',clim); 
colormap(a(handles(2)),cmap)

a(handles(3))=axes('position',[pos(3,1) pos(3,2) pos(3,3) pos(3,4)]);
trisurf(Slo.tri(tr,:)-v/2,Slo.coord(1,vr),Slo.coord(2,vr),Slo.coord(3,vr),...
    double(data(vr)),'EdgeColor','none');
view(-90,0); 
daspect([1 1 1]); axis tight; camlight; axis vis3d off;
lighting phong; material dull; shading interp;
set(a(handles(3)),'CLim',clim); 
colormap(a(handles(3)),cmap)

a(handles(4))=axes('position',[pos(4,1) pos(4,2) pos(4,3) pos(4,4)]);
trisurf(Slo.tri(tr,:)-v/2,Slo.coord(1,vr),Slo.coord(2,vr),Slo.coord(3,vr),...
    double(data(vr)),'EdgeColor','none');
view(90,0); 
daspect([1 1 1]); axis tight; camlight; axis vis3d off;
lighting phong; material dull; shading interp;
set(a(handles(4)),'CLim',clim); 
colormap(a(handles(4)),cmap)
