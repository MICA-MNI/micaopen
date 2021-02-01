function wM = WeightedMan(wei, gm_ind, ncompo)
    % Calculate subcortical-weighted manifold
    %
    % Input:
    % wei: subcortico-cortical connection [#ROI(ctx) x #ROI(sctx)]
    % gm_ind : individual gradient [#ROI(ctx) x #component]
    % ncompo : number of components to use
    %
    % Output:
    % wM: subcortical-weighted manifold [1 x #ROI(sctx)]
    %     if there is no subcortico-cortical connection, wM = NaN
    
    nroi_sctx = size(wei,2);
    gm_weight_cent = zeros(ncompo,nroi_sctx);
    for sc = 1:nroi_sctx
        gm_weight = gm_ind(:,1:ncompo) .* wei(:,sc);
        non0_gm = gm_weight(find(mean(gm_weight,2) ~= 0),:);
        gm_weight_cent(:,sc) = mean(non0_gm);
    end
    wM = mean(gm_weight_cent);
end
