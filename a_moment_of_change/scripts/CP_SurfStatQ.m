function Q = CP_SurfStatQ( slm );

[l,v]=size(slm.t);

df=zeros(2);
ndf=length(slm.df);
df(1,1:ndf)=slm.df;
df(2,1:2)=slm.df(ndf);
df(1,ndf)=mean(slm.dfs);

reselspvert=ones(1,v);

P_val=stat_threshold(0,1,0,df,[10 slm.t],[],[],[],slm.k,[],[],0);
P_val=P_val(2:length(P_val));
np=length(P_val);
[P_sort, index]=sort(P_val);
r_sort=reselspvert(index);
c_sort=cumsum(r_sort);
P_sort=P_sort./(c_sort+(c_sort<=0)).*(c_sort>0)*sum(r_sort);
m=1;
Q_sort=zeros(1,np);
for i=np:-1:1
    if P_sort(i)<m
        m=P_sort(i);
    end
    Q_sort(i)=m;
end
Q=zeros(1,np);
Q(index)=Q_sort;