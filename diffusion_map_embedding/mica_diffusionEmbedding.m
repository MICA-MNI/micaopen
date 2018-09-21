function [embedding, result] = mica_diffusionEmbedding(data, varargin)
% MICA_DIFFUSIONEMBEDDING   Diffusion embedding.
%   [embeddings, results] = MICA_DIFFUSIONEMBEDDING(data, varargin)
%   calculates the components of the data matrix using the diffusion
%   embedding algorithm. Returns the embeddings and a structure containing
%   other relevant results. 
%
%   Name-value pairs:
%       'alpha'             Set alpha value (default: 0.5).
%       'nComponents'       Sets number of components. Leave blank for
%                               automatic selection.
%       'diffusionTime'     Diffusion time (default: 0). 
%       'symmetryMargin'    Allows a margin of error in the symmetry of the
%                               matrix. All upper triangular values will be
%                               set to their corresponding lower triangular
%                               values if, and only if, their differences
%                               fall within [-symmetryMargin,
%                               symmetryMargin].
%
%   Python code by Satrajid Ghosh (https://github.com/satra/mapalign).
%   Ported to MATLAB by Reinder Vos de Wael (Jul 2017).
%
%   References:
%   [1] Coifman, R.R.; S. Lafon. (2006). "Diffusion maps". Applied and
%   Computational Harmonic Analysis 21: 5-30. doi:10.1016/j.acha.2006.04.006

%% Check input arguments.

p = inputParser;
addParameter(p, 'alpha'         , 0.5       , @isnumeric    );
addParameter(p, 'nComponents'   , nan       , @isnumeric    );
addParameter(p, 'diffusionTime' , 0         , @isnumeric    ); 
addParameter(p, 'symmetryMargin', 0         , @isnumeric    ); 

% Parse the input
parse(p, varargin{:});
in = p.Results; 

% Check for data symmetry. 
symmetryDiff = unique(tril(data)-triu(data).');
if max(symmetryDiff(:)) > in.symmetryMargin || min(symmetryDiff(:)) < -in.symmetryMargin
   error('Asymmetry in the data matrix is too large.')
% If not symmetric, but within margins, make it symmetric. 
elseif ~issymmetric(data)
    data = tril(data) + tril(data,-1).'; 
end  

% Check if the graph is connected. 
if ~all(conncomp(graph(data)) == 1)
    error('Graph is not connected.')
end

% Parameter for later use. 
sz = size(data); 

%% Run diffusion embedding. 

% Rescale the data. 
%   Choice of alpha determines properties of the diffusion embedding.
%   alpha=1 approximates the Laplace-Beltrami operator, alpha=0.5
%   approximates the Fokker-Planck diffusion and alpha= is a classical
%   graph Laplacian normalization.
d = sum(data,2) .^ -in.alpha;
L = data .* (d*d.'); 

d2 = sum(L,2) .^ -1;
M = bsxfun(@times, L, d2);

% Get the eigenvectors and eigenvalues
[eigvec,eigval] = eig(M);
eigval = diag(eigval);

% Sort eigenvectors and values.
[eigval, idx] = sort(eigval,'descend');
eigvec = eigvec(:,idx);

% Remove small eigenvalues. 
n = max(2, floor(sqrt(sz(1)))); 
eigval = eigval(1:n);
eigvec = eigvec(:,1:n);

% Scale eigenvectors by the largest eigenvector. 
psi = bsxfun(@rdivide, eigvec, eigvec(:,1));

% Automatically determines the diffusion time and scales the eigenvalues. 
if in.diffusionTime == 0
    in.diffusionTime = exp(1 - log(1 - eigval(2:end)) ./ log(eigval(2:end)));
    eigval = eigval(2:end) ./ (1 - eigval(2:end)); 
else
    eigval = eigval(2:end) .^ in.diffusionTime;
end

% Set the threshold for number of components. 
eigvalRatio = eigval ./eigval(1);
threshold = max([.05,eigvalRatio(end)]);
nComponentsAuto = min([sum(eigvalRatio > threshold)-1, sz(1)]);

if isnan(in.nComponents)
    in.nComponents = nComponentsAuto;
end

% Calculate embedding and bring the data towards output format. 
embedding = bsxfun(@times, psi(:,2:(in.nComponents+1)), eigval(1:in.nComponents).');
result = struct('diffusionTime', in.diffusionTime.', 'lambdas', eigval.', ...
    'nComponents', in.nComponents, 'nComponentsAuto', nComponentsAuto, ...
    'vectors', eigvec); 

