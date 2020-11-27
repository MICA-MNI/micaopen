function cohen = mica_cohensd_twogroups(G1, G2) 
m1      = mean(G1,1);
m2      = mean(G2,1); 
s1      = std(G1,0,1); 
s2      = std(G2,0,1); 
n1      = size(G1,1); 
n2      = size(G2,1); 
s       = sqrt(((s1.^2 * (n1-1)) + (s2.^2 * (n2-1))) ./ (n1+n2-2));
cohen   = (m1-m2)./s; 
        