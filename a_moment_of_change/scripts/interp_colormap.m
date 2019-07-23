function extended_cmap = interp_colormap(cmap, expansion)

% cmap          colormap with 3 columns and 2 or more rows
% expansion     integer for degree of expansion

extended_cmap = [];
for ii = 1:size(cmap,1)-1
    for c = 1:3
        new_bit(:,c) = linspace(cmap(ii,c), cmap(ii+1,c), expansion);
    end
    extended_cmap = [extended_cmap; cmap(ii,:); new_bit];
end

