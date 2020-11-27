function f = mica_scatter2Groups(data1,data2,multiplier)
% f = mica_scatter2Groups(data1,data2, multiplier)
if nargin == 2
   multiplier = 0.1; 
end
f=figure
y1 = nanmean(data1,2); 
n1 = length(y1); 
x1 = ones(size(y1)) + randn(n1,1)*multiplier; 

f=figure, hold on  
plot(x1,y1,'o',...
    'MarkerSize', 15,...
    'MarkerEdgeColor',[1 1 1],...
        'MarkerFaceColor',[0 0 0])
    
y2 = nanmean(data2,2); 
n2 = length(y2); 
x2 = ones(size(y2)) + randn(n2,1)*multiplier + 1; 

plot(x2,y2,'o',...
    'MarkerSize', 15,...
    'MarkerEdgeColor',[1 1 1],...
        'MarkerFaceColor',[1 0 0])
    
plot([0.8 1.2], [mean(y1) mean(y1)],'k','LineWidth',2)
plot([0.9 1.1], [mean(y1)+std(y1) mean(y1)+std(y1)],'k')
plot([0.9 1.1], [mean(y1)-std(y1) mean(y1)-std(y1)],'k')

plot([1.8 2.2], [mean(y2) mean(y2)],'r','LineWidth',2)
plot([1.9 2.1], [mean(y2)+std(y2) mean(y2)+std(y2)],'r')
plot([1.9 2.1], [mean(y2)-std(y2) mean(y2)-std(y2)],'r')
d = [data1;data2]; 
m1 = nanmin(d(:)); 
m2 = nanmax(d(:));
axis([0 3 m1 m2])

