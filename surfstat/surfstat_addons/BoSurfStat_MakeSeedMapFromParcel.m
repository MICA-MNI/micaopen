function SeedS = BoSurfStat_MakeSeedMapFromParcel(Z,seed,Parcel, Slo)
% SeedS = BoSurfStat_MakeSeedMapFromParcel(Z,seed,Parcel, Slo)
% 
% boris@bic.mni.mcgill.ca
% october 2017
SeedOnSurf = BoSurfStatMakeParcelData(Z(seed,:), Slo, Parcel);
SeedS = SurfStatSmooth(SeedOnSurf,Slo,5); 