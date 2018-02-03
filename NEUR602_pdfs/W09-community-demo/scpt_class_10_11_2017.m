addpath E:\MATLAB\BCT

load data

n = length(fc);
fc = fc.*~eye(n);   % zero out diagonal
sc(sc>0) = 1;       % binarize

% visualize
figure;
imagesc(sc);

figure;
spy(sc);

% number of nodes
n = length(sc);

%--------------------------------------------------------------------------
% find communities in a functional network
%--------------------------------------------------------------------------
gamvals = 0:0.01:0.3;
ngam = length(gamvals);

nreps = 40;
ci = zeros(n,ngam,nreps);   % community assignments
q = zeros(ngam,nreps);      % modularity values
ciu = zeros(n,ngam);        % consensus communities

parpool;
for igam = 1:ngam
    gam = gamvals(igam);
    
    % use the uniform null model, define custom objective
    B = fc;
    B(fc<gam) = 0;
     
    fprintf('gam %1.2i ',igam);
    tic;
    parfor irep = 1:nreps
        [ci(:,igam,irep),q(igam,irep)] = community_louvain(B,[],[],[]);
    end
    
    citemp = squeeze(ci(:,igam,:));
    ag = agreement(citemp) / nreps; % agreement (probability)
    
    cinull = zeros(size(citemp));
    % get null agreement
    parfor irep = 1:nreps
        cinull(:,irep) = citemp(randperm(n),irep);
    end
    agnull = agreement(cinull) / nreps;
    tau = mean(agnull(:));
    
    % get consensus (see Lancichinetti & Fortunato (2012))
    ciu(:,igam) = consensus_und(ag,tau,10);
    
    fprintf(' finished in %.2f s\n',toc);
end

% plot consensus community assignments
figure;
imagesc(ciu); 
xlabel('gamma values')
ylabel('node index')
colorbar;

% look at partition similarity
rzvals = zeros(ngam,2);
for igam = 1:ngam
    rz = zeros(nreps);
    mask = triu(ones(nreps),1) > 0;
    for i = 1:(nreps - 1)
        parfor j = (i + 1):nreps
            % z-score of Rand index (similarity between partitions)
            rz(i,j) = fcn_randz(ci(:,igam,i),ci(:,igam,j));
        end
    end
    rzvec = rz(mask);
    rzvals(igam,1) = mean(rzvec);
    rzvals(igam,2) = std(rzvec)^2;
    fprintf('gam %i of %i\n',igam,ngam);
end

% want max mean, min variance
figure;
plotyy(gamvals,rzvals(:,1),gamvals,rzvals(:,2))
legend({'mean randz','var randz'})

% set partition to use
cic = ciu(:,22);

str = sum(abs(fc))';

[~,i] = sortrows([cic str],[1 -2]);
figure;
imagesc(fc(i,i));
%colormap(cmap)
caxis([-0.3 0.3])

figure;
for ii = 1:max(cic) 
    subplot(2,4,ii)
    scatter3(coor(:,1),coor(:,2),coor(:,3),50,[0.8 0.8 0.8]); hold on
    scatter3(coor(cic==ii,1),coor(cic==ii,2),coor(cic==ii,3),50,'b','filled');
    view(90,90);
    axis image
end
    

