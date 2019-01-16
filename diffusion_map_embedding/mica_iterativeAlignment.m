function [realigned, xfms] = mica_iterativeAlignment(embeddings,nIterations,firstTarget)
% MICA_ITERATIVEALIGNMENT   Align components using Procrustes method.
%   realigned = MICA_ITERATIVEALIGNMENT(embeddings,nIterations) aligns the
%   components of embeddings using Procrustes method. Embeddings is a cell
%   array, each cell contains an m-by-n array where m is the number of
%   vertices and n the number of components of one subject. embeddings can
%   also be a numeric array of size m-by-n-by-l where m is the number of
%   vertices, n the number of components and l the number of subjects.
%   Components are aligned iteratively using nIterations iterations. The
%   first alignment aligns all subjects to the components in the first cell
%   of embeddings. Subsequent alignments align all components to the mean
%   realigned components of the previous iteration.
%
%   realigned = MICA_ITERATIVEALIGNMENT(embeddings,nIterations,firstTarget)
%   aligns all components to the provided first target on the first
%   iteration (e.g. components of group average), rather than the first
%   subject.
%
%   [realigned, xfms] = MICA_ITERATIVEALIGNMENT(embeddings,nIterations,firstTarget)
%   also returns the final transformation matrices xfms. 
%
%   MATLAB adaptation of the Satrajit Ghosh's Python code
%   (https://github.com/satra/mapalign). 
%
%   Written by Reinder Vos de Wael (Jul 2017)
    
% Check if equal number of components in all subjects.
try 
    cat(3,embeddings{:});    
catch err
    if strcmp(err.identifier,'MATLAB:catenate:dimensionMismatch')
        warning('Target and source embedding have a different number of dimensions. Attempting to solve anyway.')
    else
        throw(err)
    end
end

% Set starting parameters. 
if exist('firstTarget','var')
    target = firstTarget;
else
    target = embeddings{1};
end
realigned = target; 

for ii = 1:nIterations
    % Calculate new target and clear workspace. 
    if ii > 1
        target = mean(realigned,3); 
        clearvars realigned xfms 
    end
    
    % Run realignment. 
    for jj = 1:numel(embeddings)
        if ii == 1 && jj == 1 && ~exist('firstTarget','var'); continue; end 
        [U,~,V] = svd(target.' * embeddings{jj},0);
        
        % This corresponds with the Satrajit Python code (Numpy seems to do
        % this implicitly in its svd), but is it correct?
        U = U(:, 1:min(size(U,2), size(V,2)));
        V = V(:, 1:min(size(U,2), size(V,2)));
        
        % Calculate the transformation.
        xfms{jj} = V * U';
        
        % Apply the transformation. 
        realigned(:,:,jj) = embeddings{jj} * xfms{jj};
    end
end
