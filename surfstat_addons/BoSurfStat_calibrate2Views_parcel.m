function BoSurfStat_calibrate2Views_parcel(data, Slo, pos1, pos2, handle1, handle2, clim, cmap)
% function BoSurfStat_calibrate2Views(data, Slo, pos1, pos2, clim)
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
a(handle1) =axes('position',[pos1(1) pos1(2) pos1(3) pos1(4)]);
trisurf(Slo.tri(tl,:),Slo.coord(1,vl),Slo.coord(2,vl),Slo.coord(3,vl),...
double(data(vl)),'EdgeColor','none');
view(-90,0); 
daspect([1 1 1]); axis tight; camlight; axis vis3d off;
lighting phong; material dull; shading flat;
set(a(handle1),'CLim',clim);   
colormap(a(handle1),cmap)

a(handle2)=axes('position',[pos2(1) pos2(2) pos2(3) pos2(4)]);
trisurf(Slo.tri(tl,:),Slo.coord(1,vl),Slo.coord(2,vl),Slo.coord(3,vl),...
double(data(vl)),'EdgeColor','none');
view(90,0); 
daspect([1 1 1]); axis tight; camlight; axis vis3d off;
lighting phong; material dull; shading flat;
set(a(handle2),'CLim',clim); 
colormap(a(handle2),cmap)