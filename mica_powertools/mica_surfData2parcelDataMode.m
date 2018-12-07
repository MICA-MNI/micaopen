function [parceldata ] = mica_surfData2parcelDataMode(surfdata, surfparcel)
% function [parceldata parcelstd] = mica_surfData2parcelDataMode(surfdata, surfparcel)
% computes modes in each of the parcels and writes out a new matrix
% 
% input:    surfdata   = k * v surface data (k subjects, v vertices) 
%           surfparcel = 1 * v surface parcellation (u unique labels)
% output:   parceldata = k * u parcel mean matrix 
%           
% 
% author:   boris@bic.mni.mcgill.ca
% date:     Nov 2018
% version:  1

uparcel         = unique(surfparcel); 
parceldata      = zeros(size(surfdata,1),length(uparcel)); 
parcelstd      = zeros(size(surfdata,1),length(uparcel)); 

for i = 1:length(uparcel) 
    thisparcel      = uparcel(i); 
    parceldata(:,i) = mode(surfdata(:,surfparcel==thisparcel),2);
end
    