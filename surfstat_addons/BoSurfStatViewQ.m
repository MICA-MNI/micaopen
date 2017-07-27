function [a,cb]=BoSurfStatViewQ(qval,surf,title,background)

%SurfStatViewQ viewer for Q-values
%
% Usage: [a,cb] = SurfStatViewQ(qval,surf,title,background);
%
% qval.q      = 1 x v matrix of Q-values. 
% qval.mask   = 1 x v, 1=inside, 0=outside, v=#vertices.
% qval.thresh = qval.q threshold for plot, 0.05 by default.
% surf.coord  = 3 x v matrix of coordinates.
% surf.tri    = 3 x t matrix of triangle indices, 1-based, t=#triangles.
% title       = any string, data name by default.
% background  = background colour, any matlab ColorSpec, such as 
%   'white' (default), 'black'=='k', 'r'==[1 0 0], [1 0.4 0.6] (pink) etc.
%   Letter and line colours are inverted if background is dark (mean<0.5). 
%
% a  = vector of handles to the axes, left to right, top to bottom. 
% cb = handle to the colorbar.

if nargin<3 | isempty(title)
    title=inputname(1);
end
if nargin<4
    background='white';
end
if ~isfield(qval,'thresh')
    qval.thresh=0.05;
end

t1=(qval.Q<qval.thresh).*(255-qval.Q/qval.thresh*253);
t2=(qval.Q>=qval.thresh);
tt=(t1+t2).*qval.mask*qval.thresh;

[a,cb]=BoSurfStatViewData(tt,surf,title,background);
cm=[zeros(1,3); ones(1,3)*0.8; ones(254,1) (0:253)'/254 zeros(254,1)];
colormap(cm);
for i=1:length(a)
    set(a(i),'CLim',[0 255]*qval.thresh);
end

XTick=max(tt)*(2+(0:5)/5*253)/255;
set(cb,'XTick',XTick);
set(cb,'XTickLabel',num2str(qval.thresh*(5:-1:0)'/5));
xl=get(cb,'XLabel');
set(xl,'String','Q')

dcm_obj=datacursormode(gcf);
set(dcm_obj,'UpdateFcn',@SurfStatDataCursorQ,'DisplayStyle','window');

return
end
