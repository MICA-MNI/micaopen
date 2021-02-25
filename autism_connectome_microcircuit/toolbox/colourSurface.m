function colourSurface(colour_coding, M, positions)

% colourSurface(colour_coding, M)
% colour_coding         RGB colour code for each vertex (vertices x 3)
% M                     surface structure
% positions             position in figure, four rows
%
% edited from SurfStat in November 2018, Casey Paquola

v=length(colour_coding);
vl=1:(v/2);
vr=double(vl+(v/2));
t=size(M.tri,1);
tl=1:(t/2);
tr=tl+t/2;

a(1) =axes('position', positions(1,:));
trisurf(M.tri(tl,:),M.coord(1,vl),M.coord(2,vl),M.coord(3,vl), vl, 'EdgeColor','none');
view(-90,0);
daspect([1 1 1]); axis tight; camlight; axis vis3d off;
lighting phong; material dull;
colormap(a(1), colour_coding(vl,1:3));

a(2) =axes('position',positions(2,:));
trisurf(M.tri(tl,:),M.coord(1,vl),M.coord(2,vl),M.coord(3,vl), vl, 'EdgeColor','none');
view(90,0);
daspect([1 1 1]); axis tight; camlight; axis vis3d off;
lighting phong; material dull;
colormap(a(2), colour_coding(vl,1:3));

a(3) = axes('position', positions(3,:));
trisurf(M.tri(tr,:)-(v/2),M.coord(1,vr),M.coord(2,vr),M.coord(3,vr), 1:length(vr), 'EdgeColor','none');
view(-90,0);
daspect([1 1 1]); axis tight; camlight; axis vis3d off;
lighting phong; material dull;
colormap(a(3), colour_coding(vr,1:3));

a(4) = axes('position', positions(4,:));
trisurf(M.tri(tr,:)-v/2,M.coord(1,vr),M.coord(2,vr),M.coord(3,vr), vl, 'EdgeColor','none');
view(90,0);
daspect([1 1 1]); axis tight; camlight; axis vis3d off;
lighting phong; material dull;
colormap(a(4), colour_coding(vr,1:3));