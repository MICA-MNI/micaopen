function [CDC, CD] = build_CDC(FC,GD, parc,thre)

%   build_CDC   Calculate the connectivity distance coefficient (CDC) 
%   
%   INPUT
%   FC          parcells x parcells matrix containing functional connectivity values
%   GD          parcells x parcells matrix containing geodesic distance values
%   parc        number of parcells
%   thre        threshold of functional connectivity when buliding CDC,
%               
%
%   OUTPUT
%   CDC         connectivity distance coefficient
%   CD          connectivity distance
%

%%% bulit CD map
% threshold FC by row
FC_thre    = zeros(parc,parc);
for ii     = 1:parc
    FC_row            = FC(ii,:);
    p                 = prctile(FC_row,thre);
    FCbin             = ones(size(FC_row));
    FCbin(FC_row < p) = 0;
    FC_thre(ii,:)     = FCbin;
end

% estimate inter-hemisphere connections in GD Matrix
GD_fill                    = (GD(1:parc/2,1:parc/2) + GD(parc/2+1:parc,parc/2+1:parc))/2;
GD(1:parc/2,parc/2+1:parc) = GD_fill;
GD(parc/2+1:parc,1:parc/2) = GD_fill;

% build CD by averaging GD in thresholded FC
GD_FCthr = FC_thre.*GD;
CD       = mean(GD_FCthr,2);

%%% bulid CDC
[rh,~] = corr(FC,CD);
CDC    = rh(:,1);

end
