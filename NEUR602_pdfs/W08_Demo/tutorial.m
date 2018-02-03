% add BCT functions 
addpath('/Users/boris/Documents/5_softwareTools/toolboxes/2012-03-29_BCT')


a = load('/Users/boris/Desktop/Z.mat') 
A = a.Z; 
A = (A>0.5).*A; 

[kden,~,K] = density_und(A); %density and number of nodes and edges

%calculate the strengths strength
S = strengths_und(A);

f=figure, 
hist(S)

%some degree fun degree
degree = degrees_und(logical(A));

f=figure, 
hist(degree)



%isolated nodes
isonode = 1 - logical(degree(i,:));

%clustering coef
CC = clustering_coef_wu(A)';

%local efficiency
Eloc = efficiency_wei(A,1)';

%inverse the weight of the matrix to create connection-length matrix,
%i.e. map from weight to length
L = A;
L(logical(L)) = 1 ./ L(logical((L)));
%distance matrix contains lengths of shortest paths between all pairs
%of nodes; 
%D, distance (shortest weighted path) matrix; 
%B, number of edges in shortest weighted path matrix
[D, ~] = distance_wei(L);

%Characteristic path length, global efficiency and related statistics
[lambda(i),Eglob(i),ecc,radius,diameter] = charpath(D);
%normalized betweeness centrality
BC = betweenness_wei(L) / ((N-1)*(N-2))';


%nodal regional global efficiency, first calculate path length
C   =   all_shortest_paths(sparse(A));     
C   =   C + diag(diag(1./zeros(N)));
Lp = 1/(sum(sum(1./C))/(N*(N-1)));
    
 