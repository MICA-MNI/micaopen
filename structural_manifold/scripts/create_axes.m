function noncard = create_axes(eigenvectors)

% cardinal vectors
x_lin = [min(eigenvectors(:,1)):0.001:max(eigenvectors(:,1))];

% spin a line through deep-eigenvectors space and estimate the non-cardinal 
n_split = 16;
iter = 1/n_split;
x_lin = []; y_lin = [];

% stable y limits
for ii = 1:n_split
    x_lim(1) = min(eigenvectors(:,1)) + (iter*(ii-1)*range(eigenvectors(:,1)));
    x_lim(2) = max(eigenvectors(:,1)) - (iter*(ii-1)*range(eigenvectors(:,1)));
    y_lim = [min(eigenvectors(:,2)) max(eigenvectors(:,2))];
    if ii == (n_split/2)+1
        x_lin(ii,:) = repmat(x_lim,1,50);
        y_lin(ii,:) = resample([y_lim(1):0.001:y_lim(2)],...
        100, length([y_lim(1):0.001:y_lim(2)]));
    else 
        if ii > (n_split/2)+1
            x_lim = flip(x_lim);
            y_lim = flip(y_lim);
        end
        x_lin(ii,:) = resample([x_lim(1):0.001:x_lim(2)],...
        100, length([x_lim(1):0.001:x_lim(2)]));
        if ii > (n_split/2)+1
            x_lin(ii,:) = flip(x_lin(ii,:));
        end
        p_coef(ii,:) = polyfit(x_lim, y_lim, 2);
        y_lin(ii,:) = polyval(p_coef(ii,:), x_lin(ii,:));
    end
end
x_lin = flipud(x_lin);
y_lin = flipud(y_lin);

% stable x limits
for ii = 1:n_split
    x_lim = [min(eigenvectors(:,1)) max(eigenvectors(:,1))];
    x_lin(ii+n_split,:) = resample([x_lim(1):0.001:x_lim(2)], ...
            100, length([x_lim(1):0.001:x_lim(2)]));
    y_lim(1) = min(eigenvectors(:,2)) + (iter*ii*range(eigenvectors(:,2)));
    y_lim(2) = max(eigenvectors(:,2)) - (iter*ii*range(eigenvectors(:,2)));
    p_coef = polyfit(x_lim, y_lim, 2);
    y_lin(ii+n_split,:) = polyval(p_coef, x_lin(ii+n_split,:));
end

% reorganise order
x_lin = [x_lin(end-8:end,:); x_lin(1:end-9,:)];
y_lin = [y_lin(end-8:end,:); y_lin(1:end-9,:)];

% calculate value of each node along non-cardinal lines
% based off shortets euclidean distance to the line
n1 = length(x_lin);
noncard = zeros(size(eigenvectors,1),size(x_lin,1));
for ii = 1:size(eigenvectors,1)
    for jj = 1:size(x_lin,1)
        d = sqrt(sum((repmat(eigenvectors(ii,1:2)',1,n1) - [x_lin(jj,:); y_lin(jj,:)]).^2));
        noncard(ii,jj) = find(d==min(d));
    end
end