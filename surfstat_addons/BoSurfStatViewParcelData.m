function BoSurfStatViewParcelData(mapOnParcel, S, parcel,vargin)

map2surf = zeros(1,size(S.coord,2)); 

uparcel = unique(parcel);
for i=1:length(uparcel)
    index = parcel==uparcel(i);
    map2surf(index) = mapOnParcel(i); 
end

BoSurfStatViewData(map2surf,S,vargin);