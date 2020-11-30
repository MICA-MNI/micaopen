function y = eccentricity(x)
% Eccentricity of the first three gradients.
%
%   y = ECCENTRICITY(X) computes distance from the origin of points
%   described by of the first three columns of x.

y = sqrt(sum(x(:,1:3).^2,2));
end
