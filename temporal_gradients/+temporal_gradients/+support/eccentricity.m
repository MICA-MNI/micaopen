function y = eccentricity(x)
% Eccentricity of the first three gradients.
y = sqrt(sum(x(:,1:3).^2,2));
end
