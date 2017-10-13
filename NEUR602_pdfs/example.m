% load matlab toy example 
load fisheriris

% display data 
f=figure, imagesc(meas)

% k-means clustering with sq euclidean, k=2 
[cidx2,cmeans2] = kmeans(meas,2,'dist','sqeuclidean');
[silh2,h] = silhouette(meas,cidx2,'sqeuclidean');
f=figure, imagesc([cidx2, meas])
title('data with cluster assignment')


% k-means clustering with sq euclidean, k=3 
[cidx2,cmeans2] = kmeans(meas,3,'dist','sqeuclidean');
[silh2,h] = silhouette(meas,cidx2,'sqeuclidean');
f=figure, imagesc([cidx2, meas])
title('data with cluster assignment')

[s, i] = sort(cidx2)
f=figure, imagesc([cidx2(i), meas(i,:)])


% k-means clustering with sq euclidean, k=4 
[cidx2,cmeans2] = kmeans(meas,4,'dist','sqeuclidean');
[silh2,h] = silhouette(meas,cidx2,'sqeuclidean');
f=figure, imagesc([cidx2, meas])
title('data with cluster assignment')

[s, i] = sort(cidx2)
f=figure, imagesc([cidx2(i), meas(i,:)])


% k-means clustering with city-block, k=4 
[cidx2,cmeans2] = kmeans(meas,4,'dist','city');
[silh2,h] = silhouette(meas,cidx2,'city');
f=figure, imagesc([cidx2, meas])
title('data with cluster assignment')

[s, i] = sort(cidx2)
f=figure, imagesc([cidx2(i), meas(i,:)])





%% look at data structure 
x = corr(meas)
data = meas(:,1:3); 
f=figure, 
title('data raw')
subplot(1,2,1), 
scatter3(data(:,1),data(:,2),data(:,3))

subplot(1,2,2), 
hold on
[cidx2,cmeans2] = kmeans(data,2,'dist','sqeuclidean');
symb = {'kx','rx'}
for i=1:2
    scatter3(data(cidx2==i,1),data(cidx2==i,2),data(cidx2==i,3),symb{i})
end
scatter3(cmeans2(1,1),cmeans2(1,2),cmeans2(1,3),'ko')
scatter3(cmeans2(2,1),cmeans2(2,2),cmeans2(2,3),'ro')
title('data with cluster assignment')




eucD = pdist(meas,'euclidean');
clustTreeEuc = linkage(eucD,'average');



% hierarchical clustering 
eucD = pdist(meas,'euclidean');
clustTreeEuc = linkage(eucD,'average');
[h,nodes] = dendrogram(clustTreeEuc,0);
h_gca = gca;
h_gca.TickDir = 'out';
h_gca.TickLength = [.002 0];
h_gca.XTickLabel = [];


% hierarchical clustering 
eucD = pdist(meas,'cosine');
clustTreeEuc = linkage(eucD,'average');
[h,nodes] = dendrogram(clustTreeEuc,0);
h_gca = gca;
h_gca.TickDir = 'out';
h_gca.TickLength = [.002 0];
h_gca.XTickLabel = [];

