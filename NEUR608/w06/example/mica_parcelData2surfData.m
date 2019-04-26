function map2surf = mica_parcelData2surfData(mapOnParcel, S, parcel)
% map2surf = mica_parcelData2surfData(mapOnParcel, S, parcel)
% makes a surfacefile with 1 x v points from a 1 x p parcellation data, 
% needs to supply a 1 x p surface parcellation (with p unique elements) 
%
% author: boris@bic.mni.mcgill.ca

n = size(mapOnParcel,1);
k = size(S.coord,2);

map2surf = zeros(1,k); 

uparcel = unique(parcel);

for i=1:length(uparcel)
    uparcel(i)
    index = find(parcel==uparcel(i));
    if ~isempty(index)
        map2surf(index) = mapOnParcel(i); 
    end
    
end

