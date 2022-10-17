% import data
data               = readtable('PLS_data.csv');

% separate HC & PX (ie., TLE) hippocampal volumes
HC_idx             = contains(data.ID, 'HC');
PX_idx             = contains(data.ID, 'PX');

HC_L_hippVol       = data.HU_L_hipVol(HC_idx, :); HC_L_hippVol(end, :) = []; % remove nan
HC_R_hippVol       = data.HU_R_hipVol(HC_idx, :); HC_R_hippVol(end, :) = []; % remove nan

PX_L_hippVol       = data.HU_L_hipVol(PX_idx, :);
PX_R_hippVol       = data.HU_R_hipVol(PX_idx, :);

% compute absolute ipsilateral-contralateral asymmetry
HC_IC_asym         = (HC_L_hippVol - HC_R_hippVol) ./ ((HC_L_hippVol + HC_R_hippVol) / 2);

meanHC_IC_asym     = mean(HC_IC_asym);
stdHC_IC_asym      = std(HC_IC_asym);

PX_IC_asym         = (PX_L_hippVol - PX_R_hippVol) ./ ((PX_L_hippVol + PX_R_hippVol) / 2);
zPX_IC_asym        = (PX_IC_asym - meanHC_IC_asym) / stdHC_IC_asym;

abs_IC_asym_idx    = abs(zPX_IC_asym) > 1.5;

% compute ipsilater volume z-scores
meanHC_L           = mean(HC_L_hippVol);
meanHC_R           = mean(HC_R_hippVol);
stdHC_L            = std(HC_L_hippVol);
stdHC_R            = std(HC_R_hippVol);

zPX_L_hipVol      = (PX_L_hippVol - meanHC_L) / stdHC_L;
zPX_R_hipVol      = (PX_R_hippVol - meanHC_R) / stdHC_R;

laterality         = data.laterality; laterality(laterality == "-", :) = []; % remove HC
L_lat_idx          = or(laterality == "L", laterality == "L > R");
R_lat_idx          = or(laterality == "R", laterality == "L < R");

zPX_ipsi_vol       = zeros(size(PX_L_hippVol));
zPX_ipsi_vol(L_lat_idx, :) = zPX_L_hipVol(L_lat_idx, :);
zPX_ipsi_vol(R_lat_idx, :) = zPX_R_hipVol(R_lat_idx, :);

zPX_ipsi_vol_idx   = zPX_ipsi_vol < -1.5;

% combined hippocampal atrophy
combined_atrophy_idx = abs_IC_asym_idx + zPX_ipsi_vol_idx;
n_ipsi_atrophy     = sum(combined_atrophy_idx > 0);

