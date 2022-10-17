function cohen = Cohen(G1, G2)
m1      = nanmean(G1, 1);
m2      = nanmean(G2, 1);
s1      = nanstd(G1, 0, 1);
s2      = nanstd(G2, 0, 1);
n1      = size(G1, 1);
n2      = size(G2, 1);
s       = sqrt(((s1^2 * (n1-1)) + (s2^2 * (n2-1))) / (n1+n2-2)); % pooled & weighted standard deviation
cohen   = (m1-m2) / s;

