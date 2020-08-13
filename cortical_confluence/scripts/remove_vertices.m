function [surf_slim, tagMap] = remove_vertices(surf, rm_logical)

% remove vertices and corresponding triangles from a  surface. 
% Also renumbers the triangles and produces a tagMap matching old vertex
% numbers to the New Order. 

vnew = surf.coord;
tagMap = nan(length(vnew), 2); 
tagMap(:,1) = 1:length(vnew); % old assignment
newCount = cumsum(~rm_logical); % counts the vertices that are to remain
tagMap(~rm_logical,2) = newCount(~rm_logical); % new assignment

% remove vertices
vnew(:,rm_logical==1) = []; 

% remove triangles
fnew = surf.tri; 
[r,~] = find(ismember(fnew,find(rm_logical==1))); % find the position (rows) of the faces to delete
fnew(r,:) = []; % deletes faces that reference any vertice removed

% renumber the triangles
fnewRenumbered = tagMap(fnew(:),2);
fnewRenumbered = reshape(fnewRenumbered,size(fnew));

% save out
surf_slim.tri = fnewRenumbered;
surf_slim.coord = vnew;


