function [corrdiff, p] = mica_zdiff(r1,r2,n1,n2)
% computes the differernce of 2 correlation coefficients
% Usage: 
%  [corrdiff, p] = mica_zdiff(r1,r2,n1,n2)
% 
% Input
%  r1 and r2 are the correlation coefficients in group 1 and 2 respectively
%  n1 is size of group 1, n2 is size of group 2
% 
% Output:   
%  corrdiff is the z stat, p is the two tailed p value 
%
% taken from 
% FISHER, R. A., 1921: On the “probable error” of a coefficient of 
% correlation deduced from a small sample. Metron 1, 1-32. 
% function has been tested against:
% http://faculty.vassar.edu/lowry/rdiff.html

% boris@bic.mni.mcgill.ca, Dec 2008

z1 = 1/2 * log( (1+r1)   ./ (1-r1)   );
z2 = 1/2 * log( (1+r2)   ./ (1-r2)   );

corrdiff = (z1 - z2) ./ sqrt( 1/(n1-3) + 1/(n2-3) );
p = 2*(1-normcdf(abs(corrdiff)));

