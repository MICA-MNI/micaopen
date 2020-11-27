function [FaceNormal, FaceArea, FaceCenter, VertexNormal, VertexArea, SuspectFace, NumFacesEachVertex, Duplicated_Faces, Not_Twice_Faces] = tessellation_stats(FV,VERBOSE);
%TESSELLATION_STATS - Calculate statistics of the tesselation and hunt for suspicious faces and vertices
% function [FaceNormal, FaceArea, FaceCenter, VertexNormal, VertexArea, SuspectFace, NumFacesEachVertex, Duplicated_Faces, Not_Twice_Faces] = tessellation_stats(FV,VERBOSE);
% function [FaceNormal, FaceArea, FaceCenter, VertexNormal, VertexArea, SuspectFace, NumFacesEachVertex] = tessellation_stats(FV,VERBOSE);
%
% Optional slightly faster calls:
%
% Return the statistics of the planar triangles:
% function [FaceNormal, FaceArea, FaceCenter] = tessellation_stats(FV,VERBOSE);
% 
% Return also the statistics of the vertices
% function [FaceNormal, FaceArea, FaceCenter, VertexNormal, VertexArea] = tessellation_stats(FV,VERBOSE);
%
% For INPUT of FV.vertices of size numVert x 3 and FV.faces of size numTri x 3, 
% then OUTPUTs are:
%
% FaceNormal is 3 x numTri, the normal of each face
% FaceArea is 1 x numTri, the area of each face
% FaceCenter is 3 x numTri, the location of the center of each face
% 
% Additional calculation of the vertex statistics:
%
% VertexNormal is 3 x numVert, the average normal assigned to each vertex,
%   see description below.
% VertexArea is 1 x numVert, the average area assigned to each vertex, see
%   description below.
%
% Additional calculation of properly ordered and arranged triangles
%
% SuspectFace is 1 x numTri, each element giving the number of times the triangle
%   was identified as suspicious, see calculation below.
%
% NumFacesEachVertex is 1 x numVert, each element giving the number of faces
%   attached to a vertex. Vertices with 0 faces are unassigned, 1 and 2 faces
%   are most likely at edges.
%
% Duplicated_Faces, Not_Twice_Faces
%   Each is a cell array, each element contains the one or more faces that are
%   adjacent a bad edge. Duplicated_Faces are adjacent an edge that was
%   specified more than once in the same direction. Not_Twice_Faces are adjacent
%   an edge that was not specified exactly once in each direction, but are not
%   in the set of duplicated edges.
%   
%
% VERTEX NORMALS RELATIVE TO MATLAB'S
%
% If the same FV is fed into Matlab's "h = patch(FV);" function, then vnorm =
% get(h,'vertexnormals'); returns exactly the same as VertexNormal calculated
% here, EXCEPT: vnorm is the reverse direction (CW ordering is positive in
% Matlab), and the norm of vnorm is twice that of VertexNormal (inconsequential
% scaling difference).
%
% SURFACE TEST
%
% This routine also performs a basic test of the ordering of the
%   vertices. Each face should be entered in the same CCW or CW direction. If a
%   triangle is ordered differently from it's neighbors in a smooth region, then
%   its normal vector will point in the opposite direction. A list of possible
%   problem faces will be displayed, where the figure number is the face number
%   in question. In very irregular surfaces (such as the cortex), the problem
%   face may be simply tucked in too tightly to the local surface for the
%   algorithm to catch.
%
% SuspectFace is 1 x numTri, gives the number of tests that detected a possibly
%   bad face ordered in a direction opposite of the adjacent faces. A "patch" is
%   formed at a vertex by finding all faces that are attached to a given vertex.
%   The unweighted average of the face normals is computed, then dotted with
%   each of the face normals. A face is marked as suspect if it's normal points
%   in the opposite direction of the unweighted average normal. The process is
%   repeated for all vertices, so that each triangular face is included in three
%   tests. The SuspectFace is the cumulative detection score, such that
%   SuspectFace(i) == 3 indicates that all three vertices marked the ith face as
%   suspect. Detections of 1 and 2 indicate that only one or two of the vertices
%   marked the face as suspect.
%
% If VERBOSE is true, then this routine will offer to display all triangular
%   faces that had SuspectFace == 3, i.e. all three vertices triggered the
%   detection.
%
% NumFacesEachVertex, since we are generally expecting closed surfaces in brain
%   analysis, representing cortical surfaces or boundary elements, then vertices
%   with 0, 1, or 2 faces only are worthy of further attention.
%
% For constant approximations across the triangle, then use FaceNormal and FaceCenter.
% For linear approximations, then use VertexNormals and vertices.
% VertexArea is the effective area spanned by a vertex, analogous to the FaceArea
%   spanned by triangle.
%
% CALCULATION of VERTEX NORMALS and AREAS
%
% Vertices in a tesselation are technically point discontinuities in the surface
% description, Edges are line discontinuities. In a closed surface, then there
% are precisely 2(N-2) faces for N vertices, so there are nearly half as many
% vertex parameters as triangle centers representing the same surface. Hence
% vertex representations of linear variation across the triangles are a popular
% alternative to triangle center representation of a constant variation. 
%
% The average area assigned to each vertex is found by dividing the area of a
%  face by three and assigning this equally to all three vertices. Each vertex
%  therefore has as its area the sum of 1/3 of the areas of the attached to the
%  vertex.
% The average normal is found by weighting the unit length normals of each face
%  attached to a vertex by the area of that face, then averaging. The length of
%  the average normal reflects this averaging.

%<autobegin> ---------------------- 26-May-2004 11:34:37 -----------------------
% --------- Automatically Generated Comments Block Using AUTO_COMMENTS ---------
%
% CATEGORY: Utility - Numeric
%
% Alphabetical list of external functions (non-Matlab):
%   toolbox\sort_key.m
%
% Subfunctions in this file, in order of occurrence in file:
%   c = cross(a,b);
%
% At Check-in: $Author: Mosher $  $Revision: 9 $  $Date: 5/26/04 10:02a $
%
% This software is part of BrainStorm Toolbox Version 2.0 (Alpha) 24-May-2004
% 
% Principal Investigators and Developers:
% ** Richard M. Leahy, PhD, Signal & Image Processing Institute,
%    University of Southern California, Los Angeles, CA
% ** John C. Mosher, PhD, Biophysics Group,
%    Los Alamos National Laboratory, Los Alamos, NM
% ** Sylvain Baillet, PhD, Cognitive Neuroscience & Brain Imaging Laboratory,
%    CNRS, Hopital de la Salpetriere, Paris, France
% 
% See BrainStorm website at http://neuroimage.usc.edu for further information.
% 
% Copyright (c) 2004 BrainStorm by the University of Southern California
% This software distributed  under the terms of the GNU General Public License
% as published by the Free Software Foundation. Further details on the GPL
% license can be found at http://www.gnu.org/copyleft/gpl.html .
% 
% FOR RESEARCH PURPOSES ONLY. THE SOFTWARE IS PROVIDED "AS IS," AND THE
% UNIVERSITY OF SOUTHERN CALIFORNIA AND ITS COLLABORATORS DO NOT MAKE ANY
% WARRANTY, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO WARRANTIES OF
% MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE, NOR DO THEY ASSUME ANY
% LIABILITY OR RESPONSIBILITY FOR THE USE OF THIS SOFTWARE.
%<autoend> ------------------------ 26-May-2004 11:34:37 -----------------------


% ----------------------------- Script History ---------------------------------
% JCM 13-May-2004 Creation
% JCM 13-May-2004 Further efficiencies for fast retrievals of constant or linear
%                 tesselation statistics, or longer surface checks of
%                 neighborhoods. 
% JCM 14-May-2004 Surface checks dramatically improved in speed using no do
%                 loops.
% JCM 15-May-2004 Comments updating, code cleaning, removal or renaming of
%                 parameters. 
% ----------------------------- Script History ---------------------------------

% Simple Example of 2-d triangles to check units
%                   (1,5)
%   
% (1,0) ----------- (1,1)
%   |                 |
%   |                 |
% (0,0) ------------(1,0)
%
%
% number vertices as
%                 5
%
%   4 ----------- 3
%  
%   1 ----------- 2
%
% FV.vertices = [0 0 0; 1 0 0; 1 1 0; 0 1 0; 1 5 0];% in the plane of the screen
% FV.faces = [1 2 3; 1 3 4; 3 5 4]; % outward from screen

if ~exist('VERBOSE','var'),
   VERBOSE = 1; % default talkative case
end

% Output decisions
VERTEX = 0; % default flag, don't compute vertices
SUSPECT = 0; % default flag, don't test ordering
if nargout > 3,
   VERTEX = 1; % compute vertices information
end
if nargout > 5,
   SUSPECT = 1; % test ordering
end

numTri = size(FV.faces,1); % number of faces
numVert = size(FV.vertices,1); % number of vertices

% --------------------------- Triangle Statistics ------------------------------
% calculate the area and normals for each triangle

if VERBOSE,
   disp(sprintf('Generating statistics for %.0f faces. . .',numTri));
end

Vertices = FV.vertices(FV.faces',:);
% each set of three rows of Vertices is one triangle

% now difference them to get the vectors on two sides
dVertices = diff(Vertices);
dVertices(3:3:end,:) = []; % remove the transition between triangles

% now each pair of rows in dVertices represents each triangle
% row 1 is vector from 1 to 2
% row 2 is vector from 2 to 3

% v1 = dVertices(1:2:end,:)'; % each column is side one of a triangle
% v2 = dVertices(2:2:end,:)'; % side two

% right-hand rule, counter-clockwise ordering of the triangle yields a positive
% upward area and normal.
% Call a fast subfunction of this function:
WeightedNormals = cross(dVertices(1:2:end,:)',dVertices(2:2:end,:)')/2; 
% each column is the normal for each triangle
% the length the vector gives the area

FaceArea = sqrt(sum(WeightedNormals .* WeightedNormals)); % the area
FaceNormal = WeightedNormals ./ (FaceArea([1 1 1],:)); % normalize them

% now calculate the centers of each triangle
FaceCenter = cumsum(Vertices);
FaceCenter = FaceCenter(3:3:end,:); % every third summation for every triangle
FaceCenter = diff([0 0 0;FaceCenter])'/3; % average of each summation
% each column is the mean of the vertices of the triangles
% so now we know the center, area, and the normal vector of each triangle

if ~VERTEX
   % only wanted tesselation statistics
   return
end


% --------------------------- Faces Connectivity -------------------------------
% first calculate what faces go with which vertex

[VertexNumbering,I] = sort(FV.faces(:)); % sorted Vertex numbers

FacesNumbering = rem(I-1,numTri)+1; % triangle number for each Vertex

% For the ith vertex, then FacesNumbering(VertexNumbering == i) returns the indices of the
%  polygons attached to the ith vertex.
%
% For the set of vertices in the row vector sv (e.g sv = [3 5 115 121]), then use
%  [i,ignore] = find(VertexNumbering(:,ones(1,length(sv))) == (ones(size(VertexNumbering,1),1)*sv));
%  (compares the Vertex numbers to the indices, extracts the row indices into i)
%  then FacesNumbering(i) returns the indices. Apply unique to clean up.

% So now we know what faces are connected to each vertex


% --------------------------- Vertices Statistics ------------------------------
% For each vertex, there is a neighborhood of triangles
% Find the mean of the centers of these triangles, and see if all normals are in
% the same direction away from this center.

% fast analysis, no do-loops

if VERBOSE,
   disp(sprintf('Generating statistics for %.0f vertices. . .',numVert));
end

% First, sort and replicate weighted norms for each vertex using FacesNumbering
AllWeightedNorms = cumsum(WeightedNormals(:,FacesNumbering),2);
AllAverages = cumsum(FaceArea(FacesNumbering));

% now extract each sum
VertNdx = find(diff([VertexNumbering;Inf])); % each column where a new vertex starts
% pull out the sum for each vertex, then difference from previous vertex to get
% the sum for just that vertex
SortedWeightedNorms = diff([[0;0;0] AllWeightedNorms(:,VertNdx)],1,2);
SortedAverages = diff([0 AllAverages(:,VertNdx)]);

% divide by the number of faces used in the sum to get a mean
NumFacesEachPatch = diff([0;VertNdx]); % the number of faces for each vertex
NumFacesEachPatch = NumFacesEachPatch(:)'; % ensure row vector
% the average weighted norm
SortedWeightedNorms = SortedWeightedNorms ./ NumFacesEachPatch([1 1 1],:);
SortedAverages = SortedAverages/3; % 1/3 assignment
% the average area assigned to each vertex. 1/3 of the area of each triangle is
% assigned equally to it's vertices

% now make sure it' assigned to the right vertex numbers
VertexNormal = zeros(3,numVert); % each column is the average surface normal for each vertex
VertexNormal(:,VertexNumbering(VertNdx)) = SortedWeightedNorms;
VertexArea = zeros(1,numVert); 
VertexArea(VertexNumbering(VertNdx)) = SortedAverages;


if ~SUSPECT,
   % don't want ordering tests, we're done,
   return
end

% ------------------------------ Surface Check ---------------------------------
% fast analysis, no do-loops

if VERBOSE,
   disp(sprintf('Examining the patch around %.0f vertices. . .',numVert));
end

% Want to detect if a few of the normals in a vertex patch are pointed in the
% opposite direction. Rather than use the weighted vertex normal, we will form
% the unweighted normal
% First, sort and replicate unweighted norms for each vertex using FacesNumbering
AllNorms = cumsum(FaceNormal(:,FacesNumbering),2);
SortedNorms = diff([[0;0;0] AllNorms(:,VertNdx)],1,2);
% the average unweighted norm
SortedNorms = SortedNorms ./ NumFacesEachPatch([1 1 1],:);
% now make sure it' assigned to the right vertex numbers
VertexUnweightedNormal = zeros(3,numVert); % each column is the average surface normal for each vertex
VertexUnweightedNormal(:,VertexNumbering(VertNdx)) = SortedNorms;

% form the dot product of each normal with it's average normal

InOut = sign(sum(FaceNormal(:,FacesNumbering) .* VertexUnweightedNormal(:,VertexNumbering)));
RevDir = find(InOut < 0); % normals in the reverse direction.

% FacesNumbering(RevDir) gives me the Triangle numbers for ones that reversed
BadTri = sort(FacesNumbering(RevDir));
BadTriNdx = find(diff([BadTri;Inf])); % changes in the BadTri numbers
NumBad = diff([0;BadTriNdx]); % how many times was the triangle marked as bad

SuspectFace = zeros(1,numTri); % number of times a face is detected as bad.
SuspectFace(BadTri(BadTriNdx)) = NumBad;


% ---------------------------- Vertex Statistics --------------------------------
% How many faces are attached to each vertex, including unassigned ones
NumFacesEachVertex = zeros(1,numVert); % 
NumFacesEachVertex(VertexNumbering(VertNdx)) = NumFacesEachPatch(:)';


% ----------------------------- Edge Statistics --------------------------------

% schematic representation of edges [odd edge vertex, even edge vertex];
% Edges = FV.faces(:,[1 2 2 3 3 1]); % each pair of columns is an edge
% The row number is the face number
% Order all of the odd columns adjacent the even columns
% First column is the odd edge number, then second column is the even edge number
Edges = reshape(FV.faces(:,[1 2 3 2 3 1]),[],2); % columns reordered for reshaping

if VERBOSE,
   disp(sprintf('Sorting %.0f edge descriptions . . .',size(Edges,1)));
end

[Edges,EdgeDirection] = sort(Edges,2); % sort each row, retaining direction
% EdgeDirection(i,:) gives the ordering [1 2] or [2 1] for each Edge(i,:)
[Edges_and_Directions, EdgeFaceNumber] = sort_key([Edges EdgeDirection]);
EdgeFaceNumber = rem(EdgeFaceNumber-1,size(FV.faces,1))+1; % adjust the block lex ordering
% EdgeFaceNumber(i) gives us the corresponding face number for the Edge(i,:)

% so the vector [Edges_and_Directions(i,:) EdgeFaceNnumber(i)]
%  gives use information about the ith edge

% In a triangle manifold, each edge should have been used twice, once in each
% direction. By the keyed sorting, the directions are also sorted for each edge

% Diff the edge numberings with their directions
diff_Edges_and_Directions = diff([0 0 0 0; Edges_and_Directions]);

% Each time an edge changes, then diff catches it
numEdges = sum(any(diff_Edges_and_Directions(:,1:2),2));

if VERBOSE,
   disp(sprintf('Examining %.0f distinct edges . . .',numEdges));
end

% if an edge in the same direction was specified more than once, then we can
% detect as
ndx_Duplicated_Edge = find(~any(diff_Edges_and_Directions,2));

% if an edge is repeated properly then the difference is zero in the edge
% numbering but is different in the edge direction
ndx_Repeated_Edge = find(~any(diff_Edges_and_Directions(:,1:2),2));

% all edges should have been specified twice, find those that were not
diff_ndx = diff([0;ndx_Repeated_Edge]);

ndx_NotTwice = find(diff_ndx ~= 2); % something wrong with this edge
ndx_NotTwice = ndx_Repeated_Edge(ndx_NotTwice); % in the original Edges_and_Directions

% so Edges_and_Directions([ndx_NotTwice;ndx_Duplicated_Edge]) are problem edges,
% maybe duplicated between the sets. An edge specified only once would be caught
% in NotTwice only.
Duplicated_Edges = unique(Edges_and_Directions(ndx_Duplicated_Edge,1:2),'rows');
Not_Twice_Edges = unique(Edges_and_Directions(ndx_NotTwice,1:2),'rows');

% remove the duplicated edges from the not Twice
Not_Twice_Edges = setdiff(Not_Twice_Edges,Duplicated_Edges,'rows');

% now get all faces for these edges, for visualization purposes and tracking
% there should not be that many, so don't worry about do loop
Duplicated_Faces = cell(1,size(Duplicated_Edges,1));
for i = 1:size(Duplicated_Edges,1),
   Duplicated_Faces{i} = EdgeFaceNumber(find(Edges_and_Directions(:,1) == Duplicated_Edges(i,1) & ...
      Edges_and_Directions(:,2) == Duplicated_Edges(i,2)))';
end

Not_Twice_Faces = cell(1,size(Not_Twice_Edges,1));
for i = 1:size(Not_Twice_Edges,1),
   Not_Twice_Faces{i} = EdgeFaceNumber(find(Edges_and_Directions(:,1) == Not_Twice_Edges(i,1) & ...
      Edges_and_Directions(:,2) == Not_Twice_Edges(i,2)))';
end




% ----------------------------- VERBOSE Display --------------------------------

if VERBOSE,
   
   % ------------------------ Closed Surface Check -----------------------------
   
   % there may be more vertices in the description than actually used
   if length(VertNdx) ~= numVert,
      disp(sprintf('\nThere are %.0f vertices that are unused in the faces description.',...
         numVert - length(VertNdx)));
   end
   
   EulerCharacteristic = numTri + length(VertNdx) - numEdges;
   disp(' ')
   disp('Poincaré Formula Check for Triangles:')
   disp('In a truly closed surface of triangles, then the number of triangles is')
   disp(sprintf('   number of triangles  ==   2 * (the number of vertices - 2).'));
   disp(sprintf('With %.0f triangles comprising %.0f vertices,',...
      numTri, length(VertNdx)))
   disp(sprintf('the numbers %.0f == %.0f here suggest:',numTri,2*(length(VertNdx) - 2)))
   disp(' ')
   if numTri == 2*(length(VertNdx) - 2),
      disp('CLOSED SURFACE')
   else
      disp('OPEN SURFACE')
   end
   
   disp(' ')
      disp('General Poincaré Formula Check:')
   disp(sprintf(...
      'There are %.0f faces, %.0f vertices, %.0f edges,',numTri,length(VertNdx),numEdges));
   disp(sprintf('such that the Poincaré Formula is %.0f + %.0f - %.0f = %.0f',...
      numTri,length(VertNdx),numEdges,EulerCharacteristic))
   
   if EulerCharacteristic > 0 & ~rem(EulerCharacteristic,2),
      % positive even number
      disp(sprintf('\nThe Euler Characteristic of %.0f suggests a surface of genus %.0f',...
         EulerCharacteristic,round((EulerCharacteristic - 2)/2)));
   end
   disp(' ')
   if EulerCharacteristic == 2,
      disp('CLOSED SURFACE')
   else
      disp('Not surface of genus 0 (not a closed surface)');
   end
   
   % Edges at the boundary or adjacent faces that are reverse wound
   
   disp(' ');
   if ~isempty(Duplicated_Faces),
      disp(sprintf('BAD, there are %.0f edges that were duplicated in the face descriptions.',...
         length(Duplicated_Faces)));
      disp(sprintf('The faces adjacent these edges are in Duplicated_Faces'));
   else
      disp('Good, no edges were duplicated in the face descriptions.');
   end
   
   disp(' ');
   if ~isempty(Not_Twice_Faces),
      disp(sprintf('BAD, there are %.0f edges that were not specified twice, once in each direction.',...
         length(Not_Twice_Faces)));
      disp(sprintf('The faces adjacent these edges are in Not_Twice_Faces'));
   else
      disp('Good, all edges were properly used twice, once in each direction.');
   end
    
   
   % ------------------------- Suspicious Vertices -----------------------------
   
   maxFace = max(NumFacesEachVertex);
   
   disp(' ');
   
   for i = 0:maxFace,
      disp(sprintf('There are %6.0f vertices with %3.0f faces attached.',...
         sum(NumFacesEachVertex == i),i));
   end
   
   % one and two faces are not in the interior regions
   ndx = find(NumFacesEachVertex == 1 | NumFacesEachVertex == 2);
   
   
   if length(ndx) > 0,
      PLOTLEN = input(sprintf('Plot how many of these %.0f isolated (1 or 2) vertices: ',length(ndx)));
   else
      % none found
      PLOTLEN = 0; % don't bother asking
   end
   
   for i = 1:PLOTLEN,
      
      % get the vertices for the bad face
      iVert = ndx(i);
      
      % get the faces attached to this vertex
      % For the ith vertex, then FacesNumbering(VertexNumbering == i) returns the indices of the
      %  polygons attached to the ith vertex.
      
      fndx = FacesNumbering(VertexNumbering == iVert); % the faces attached to these vertices
      
      figure
      set(gcf,'Name',sprintf('Vertex %.0f with %.0f faces attached',iVert,NumFacesEachVertex(iVert)));
      h = patch('vertices',FV.vertices,'faces',FV.faces(fndx,:),'facecolor','r','edgecolor','k');
      axis equal
      axis vis3d
      hold on
      plot3(FaceCenter(1,fndx),FaceCenter(2,fndx),FaceCenter(3,fndx),'*');
      plot3(FV.vertices(iVert,1),FV.vertices(iVert,2),FV.vertices(iVert,3),'g+');
      ma = mean(FaceArea(fndx)); % mean area
      quiver3(FaceCenter(1,fndx),FaceCenter(2,fndx),FaceCenter(3,fndx),...
         FaceNormal(1,fndx),FaceNormal(2,fndx),FaceNormal(3,fndx),.25);
      set(h,'FaceAlpha',.8)
      hold off
      cameratoolbar('Show'); % activate the camera toolbar
      ret = cameratoolbar; % for strange reason, this activates the default orbit mode.
      drawnow
   end
   
   
   % -------------------------- Suspicious Faces -------------------------------
   
   disp(' ');
   
   for i = 0:2,
      disp(sprintf('There are %6.0f faces with %1.0f suspect detects.',...
         sum(SuspectFace == i),i));
   end
   
   ndx = find(SuspectFace > 2);
   disp(sprintf(...
      '\nThere are %.0f faces with more than two suspicious direction tests.\n',...
      length(ndx)));
   
   if length(ndx) > 0,
      PLOTLEN = input(sprintf('Plot how many of these %.0f suspect faces: ',length(ndx)));
   else
      % none found
      PLOTLEN = 0; % don't bother asking
   end
   
   if PLOTLEN > 0
      disp(sprintf('Suspect face is painted green.'));
   end
   
   for i = 1:PLOTLEN,
      
      % get the vertices for the bad face
      iVert = FV.faces(ndx(i),:);
      iVert = iVert(:)'; % ensure row vector
      
      % get the faces attached to these vertices
      % For the set of vertices in the row vector sv (e.g sv = [3 5 115 121]), then
      % use
      %  [i,ignore] = find(VertexNumbering(:,ones(1,length(sv))) == (ones(size(VertexNumbering,1),1)*sv));
      %  (compares the Vertex numbers to the indices, extracts the row indices into i)
      %  then FacesNumbering(i) returns the indices.
      
      [fndx, ignore] = find(VertexNumbering(:,ones(1,length(iVert))) == (ones(size(VertexNumbering,1),1)*iVert));
      fndx = FacesNumbering(fndx); % the faces attached to these vertices
      fndx = unique(fndx); % ensure unique
      nifndx = fndx;
      nifndx(find(nifndx == ndx(i))) = []; % remove the ith face
      
      figure
      set(gcf,'Name',sprintf('Face %.0f with %.0f suspect detects',ndx(i),SuspectFace(ndx(i))));
      % not the ith face
      h = patch('vertices',FV.vertices,'faces',FV.faces(nifndx,:),'facecolor','r','edgecolor','k');
      % the ith face
      hi = patch('vertices',FV.vertices,'faces',FV.faces(ndx(i),:),'facecolor','g');
      axis equal
      axis vis3d
      hold on
      plot3(FaceCenter(1,fndx),FaceCenter(2,fndx),FaceCenter(3,fndx),'*')
      ma = mean(FaceArea(fndx)); % mean area
      quiver3(FaceCenter(1,fndx),FaceCenter(2,fndx),FaceCenter(3,fndx),...
         FaceNormal(1,fndx),FaceNormal(2,fndx),FaceNormal(3,fndx),0.25);
      set(h,'FaceAlpha',.8)
      hold off
      cameratoolbar('Show'); % activate the camera toolbar
      ret = cameratoolbar; % for strange reason, this activates the default orbit mode.
      drawnow
   end
end

% done


% ------------------------------ CROSS PRODUCT ---------------------------------
function c = cross(a,b);
% fast computation, no permutes

% Calculate cross product
c = [a(2,:).*b(3,:)-a(3,:).*b(2,:)
   a(3,:).*b(1,:)-a(1,:).*b(3,:)
   a(1,:).*b(2,:)-a(2,:).*b(1,:)];