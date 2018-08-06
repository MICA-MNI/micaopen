function dataT2 = mica_crossTemplateNN(dataT1, Template1,Template2)
% dataT2 = mica_crossTemplateNN(dataT1, Template1,Template2)
% maps data from Templae1 to Template2 - based on a simple nearest
% neighbour. Caution is warranted - some more advanced registrations may be
% better than this simple hack
%
% Boris@MICA - June 4 2018
n2 = size(Template1.coord,2); 
for i = 1:size(Template2.coord,2)
    i
    d = sqrt(sum((repmat(Template2.coord(1:3,i),1,n2) - Template1.coord).^2)); 
    index = find(d==min(d)); 
    index_us(1,i) = index; 
    dataT2(:,i) = dataT1(:,index); 
end