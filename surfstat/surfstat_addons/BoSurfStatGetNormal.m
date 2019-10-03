function surf = BoSurfStatGetNormal(surf,failflag)

if failflag == 1
    surf.coord = [surf.coord,[0;0;0]];
    v=size(surf.coord,2);
    surf.tri   = [surf.tri;[v,v,v];[v,v,v]];


    u1=surf.coord(:,surf.tri(:,1));
    d1=surf.coord(:,surf.tri(:,2))-u1;
    d2=surf.coord(:,surf.tri(:,3))-u1;
    c=cross(d1,d2,1);
    surf.normal=zeros(3,v);
    for j=1:3
        for k=1:3
            surf.normal(k,:)=surf.normal(k,:)+accumarray(surf.tri(:,j),c(k,:)')';
        end
    end
    surf.normal=surf.normal./(ones(3,1)*sqrt(sum(surf.normal.^2,1)));

    surf.coord = surf.coord(:,1:(end-1)); 
    surf.tri   = surf.tri(1:(end-2),:);
    surf.normal = surf.normal(:,1:(end-1)); 
else
    
    v=size(surf.coord,2);
    u1=surf.coord(:,surf.tri(:,1));
    d1=surf.coord(:,surf.tri(:,2))-u1;
    d2=surf.coord(:,surf.tri(:,3))-u1;
    c=cross(d1,d2,1);
    surf.normal=zeros(3,v);
    for j=1:3
        for k=1:3
            surf.normal(k,:)=surf.normal(k,:)+accumarray(surf.tri(:,j),c(k,:)')';
        end
    end
    surf.normal=surf.normal./(ones(3,1)*sqrt(sum(surf.normal.^2,1)));
    
end