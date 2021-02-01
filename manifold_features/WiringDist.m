function WD = WiringDist(gm_ind, ncompo)
    % Calculate wiring distance
    % 
    % Input:
    % gm_ind : individual gradient [#ROI x #component]
    % ncompo : number of components to use
    %
    % OutPut:
    % WD: wiring distance [#ROI x #ROI]
    
    nroi   = size(gm_ind,1);    
    WD = zeros(nroi,nroi);
    for nr1 = 1:nroi
        for nr2 = 1:nroi
            seed = gm_ind(nr1,:);
            targ = gm_ind(nr2,:);
            WD(nr1,nr2) = norm(seed-targ);
        end
    end
end