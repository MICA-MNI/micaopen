function thisclus = BoSurfStatCoordTable(thisclus,SM,AREA)

for i = 1:length(thisclus.clus.clusid)
    thispeak = max(thisclus.t(thisclus.clusid==i))
    thisclus.clus.peakt(i,1) = thispeak;
    index = find(thisclus.t == thispeak); 
    thisclus.clus.peakvert(i,1) = index; 
    thisclus.clus.x(i,1) = SM.coord(1,index); 
    thisclus.clus.y(i,1) = SM.coord(2,index); 
    thisclus.clus.z(i,1) = SM.coord(3,index); 
    thisclus.clus.area(i,1) = sum(AREA(thisclus.clusid==i)); 
end 

for i = 1:length(thisclus.peak.t)
    thisclus.peak.x(i,1) = SM.coord(1,thisclus.peak.vertid(i)); 
    thisclus.peak.y(i,1) = SM.coord(2,thisclus.peak.vertid(i)); 
    thisclus.peak.z(i,1) = SM.coord(3,thisclus.peak.vertid(i)); 
end