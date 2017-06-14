function [a,cb]=BoSurfStatView(struct,surf,title,background);

%SurfStatView is a simple viewer for surface structures.
% 
% Usage: [a,cb] = SurfStatView(struct, surf [,title [,background]]);
% 
% struct      = 1 x v vector of data, v=#vertices or structure of same,
%             = zeros(1,v) if empty.
% surf.coord  = 3 x v matrix of coordinates.
% surf.tri    = 3 x t matrix of triangle indices, 1-based, t=#triangles.
% title       = any string, data name by default.
% background  = background colour, any matlab ColorSpec, such as 
%   'white' (default), 'black'=='k', 'r'==[1 0 0], [1 0.4 0.6] (pink) etc.
%   Letter and line colours are inverted if background is dark (mean<0.5). 
%
% a  = vector of handles to the axes, left to right, top to bottom. 
% cb = handle to the colorbar.
%
% To change the colour limits, use SurfStatColLim([min, max]);
% To change the colour map, use e.g. colormap('jet'); you might have to use
% SurfStatColLim again to get the colour bar right. 
% Surfaces can be edited in the figure window by clicking e.g. "Rotate 3D".
% If you want to customize the plot, modify the code in SurfStatViewData. 

if nargin<3 | isempty(title)
    title=inputname(1);
end
if nargin<4
    background='white';
end

if isempty(struct)
    struct=zeros(1,size(surf.coord,2));
end

if ~isstruct(struct)

    [a,cb]=BoSurfStatViewData(struct,surf,title,background);
else
    if isfield(struct,'P') 
        [a,cb]=BoSurfStatViewP(struct,surf,title,background); 
    end
    if isfield(struct,'Q')
        [a,cb]=BoSurfStatViewQ(struct,surf,title,background); 
    end
end    
    
return
end

