function [a,cb]=BoSurfStatViewP(pval,surf,title,background)

%SurfStatViewP for P-values of peaks and clusters.
%
% Usage: [a,cb] = SurfStatViewP(pval, av [,pvalthresh]);
%
% pval.P      = 1 x v matrix of corrected P-values for vertices.
% pval.C      = 1 x v matrix of corrected P-values for clusters.
% pval.mask   = 1 x v, 1=inside, 0=outside, v=#vertices.
% pval.thresh = P-value threshold for plot, 0.05 by default.
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
if ~isfield(pval,'thresh')
    pval.thresh=0.05;
end

signifpeak=pval.P<pval.thresh;
if isfield(pval,'C')
    signifclus=pval.C<pval.thresh;
    t1=signifclus.*(1-signifpeak).*(127-pval.C/pval.thresh*126);
else
    signifclus=0;
    t1=0;
end
t2=signifpeak.*(255-pval.P/pval.thresh*126);
t3=(1-signifpeak).*(1-signifclus)*128;
tt=(t1+t2+t3).*pval.mask*pval.thresh;

[a,cb]=BoSurfStatViewData(tt,surf,title,background);
cm=[zeros(1,3); 
    zeros(127,1)   (0:126)'/127   ones(127,1); ones(1,3)*0.8;
    ones(127,1)    (0:126)'/127   zeros(127,1)];
colormap(cm);
for i=1:length(a)
    set(a(i),'CLim',[0 255]*pval.thresh);
end

set(cb,'XTick',[1 64 127 129 192 255]/255*max(tt));
pstr1=num2str(round(pval.thresh*1000)/1000);
pstr2=num2str(round(pval.thresh*1000/2)/1000);
set(cb,'XTickLabel',strvcat(['     ' pstr1],['   ' pstr2],...
    ' ',['   0 ' pstr1],['   ' pstr2],'   0'));
xl=get(cb,'XLabel');
set(xl,'String','P Cluster               P Vertex')

dcm_obj=datacursormode(gcf);
set(dcm_obj,'UpdateFcn',@SurfStatDataCursorP,'DisplayStyle','window');

return
end
