function [eta] = doEta_matal(corrData)

eta=zeros(size(corrData,1), size(corrData,1));

nnMat=ones(size(corrData,1));
nMat=ones(size(corrData,1),1);
lMat=ones(size(corrData,2),1);
n=size(corrData,1);
l=size(corrData,2);

tic

T= kron(transpose(nMat), ((corrData.*corrData)*lMat));

TTU= (T - 2*corrData*transpose(corrData) + transpose(T))/2;

M = (l/2) * (kron(transpose(nMat), ((1/l)*corrData*lMat).^2));

TTD = T + transpose(T) - M -transpose(M) - ((1/l)*corrData*lMat)*transpose(corrData*lMat);

eta = nnMat-(TTU./TTD);

eta=tril(eta,-1);
eta=eta+eta';
eta=eta+eye(size(eta));

toc
