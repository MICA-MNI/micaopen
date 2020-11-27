function map2surf = mica_parcelData2surfData(mapOnParcel, S, parcel)
% map2surf = mica_parcelData2surfData(mapOnParcel, S, parcel)
% makes a surfacefile with 1 x v points from a 1 x p parcellation data, 
% needs to supply a 1 x p surface parcellation (with p unique elements) 
%
% author: boris@bic.mni.mcgill.ca


n = size(mapOnParcel,1);
if n==1 
    
    map2surf = zeros(1,size(S.coord,2)); 
    size(map2surf)  
    for i=1:size(mapOnParcel,2)
    
        index = find(parcel==i); 
        if ~isempty(index)
            map2surf(index) = mapOnParcel(i); 
        end
    
    end

else
    
    map2surf = zeros(n,size(S.coord,2)); 
    size(map2surf)  

    for i=1:size(mapOnParcel,2)
    
        index = find(parcel==i); 
        if ~isempty(index)
            map2surf(1:n,index) = repmat(mapOnParcel(1:n,i),1,length(index)); 
        end

    end
end
