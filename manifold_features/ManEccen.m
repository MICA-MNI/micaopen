function ME = ManEccen(gm_temp, gm_ind, ncompo)
    % Calculate manifold eccentricity
    % 
    % Input:
    % gm_temp: template gradient [#ROI x #component]
    % gm_ind : individual gradient [#ROI x #component]
    % ncompo : number of components to use
    %
    % OutPut:
    % ME: manifold eccentricity [#ROI x1]
    
    nroi   = size(gm_temp,1);    
    gm_center = mean(gm_temp(:,1:ncompo));
    ME = zeros(nroi,1);
    for nr = 1:nroi
        ME(nr,1) = norm(gm_center - gm_ind(nr,1:ncompo),2);
    end
end