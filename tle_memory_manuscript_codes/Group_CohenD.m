%% housekeeping
DATA                  = readtable('PLS_data.csv');

%% cohen's D for raw scores

EpiE_raw              = DATA.Epi_E(~isnan(DATA.Epi_E));
EpiD_raw              = DATA.Epi_D(~isnan(DATA.Epi_D));
SemE_raw              = DATA.Sem_E(~isnan(DATA.Sem_E));
SemD_raw              = DATA.Sem_D(~isnan(DATA.Sem_D));
SpaE_raw              = DATA.Spa_E(~isnan(DATA.Spa_E));
SpaD_raw              = DATA.Spa_D(~isnan(DATA.Spa_D));

groups_EpiE_raw       = DATA.Group(~isnan(DATA.Epi_E));
groups_EpiD_raw       = DATA.Group(~isnan(DATA.Epi_D));
groups_SemE_raw       = DATA.Group(~isnan(DATA.Sem_E));
groups_SemD_raw       = DATA.Group(~isnan(DATA.Sem_D));
groups_SpaE_raw       = DATA.Group(~isnan(DATA.Spa_E));
groups_SpaD_raw       = DATA.Group(~isnan(DATA.Spa_D));

HC_EpiE_raw           = EpiE_raw(groups_EpiE_raw == "HC");
HC_EpiD_raw           = EpiD_raw(groups_EpiD_raw == "HC");
HC_SemE_raw           = SemE_raw(groups_SemE_raw == "HC");
HC_SemD_raw           = SemD_raw(groups_SemD_raw == "HC");
HC_SpaE_raw           = SpaE_raw(groups_SpaE_raw == "HC");
HC_SpaD_raw           = SpaD_raw(groups_SpaD_raw == "HC");

TLE_EpiE_raw          = EpiE_raw(groups_EpiE_raw == "TLE");
TLE_EpiD_raw          = EpiD_raw(groups_EpiD_raw == "TLE");
TLE_SemE_raw          = SemE_raw(groups_SemE_raw == "TLE");
TLE_SemD_raw          = SemD_raw(groups_SemD_raw == "TLE");
TLE_SpaE_raw          = SpaE_raw(groups_SpaE_raw == "TLE");
TLE_SpaD_raw          = SpaD_raw(groups_SpaD_raw == "TLE");

cohenD_EpiE           = Cohen(HC_EpiE_raw, TLE_EpiE_raw);
cohenD_EpiD           = Cohen(HC_EpiD_raw, TLE_EpiD_raw);
cohenD_SemE           = Cohen(HC_SemE_raw, TLE_SemE_raw);
cohenD_SemD           = Cohen(HC_SemD_raw, TLE_SemD_raw);
cohenD_SpaE           = Cohen(HC_SpaE_raw, TLE_SpaE_raw);
cohenD_SpaD           = Cohen(HC_SpaD_raw, TLE_SpaD_raw);

measure               = {'RAW_HC-TLE_EpiE';
                         'RAW_HC-TLE_EpiD';
                         'RAW_HC-TLE_SemE';
                         'RAW_HC-TLE_SemD';
                         'RAW_HC-TLE_SpaE';
                         'RAW_HC-TLE_SpaD'};

nHC                   = [size(HC_EpiE_raw, 1);
                         size(HC_EpiD_raw, 1);
                         size(HC_SemE_raw, 1);
                         size(HC_SemD_raw, 1);
                         size(HC_SpaE_raw, 1);
                         size(HC_SpaD_raw, 1)];

nTLE                  = [size(TLE_EpiE_raw, 1);
                         size(TLE_EpiD_raw, 1);
                         size(TLE_SemE_raw, 1);
                         size(TLE_SemD_raw, 1);
                         size(TLE_SpaE_raw, 1);
                         size(TLE_SpaD_raw, 1)];

CohenD                = [cohenD_EpiE;
                         cohenD_EpiD;
                         cohenD_SemE;
                         cohenD_SemD;
                         cohenD_SpaE;
                         cohenD_SpaD];

rawResults            = [table(measure) table(CohenD) table(nHC) table(nTLE)];

%% cohen's D for residual scores (age/sex regressed out)

age_AS_EpiE           = DATA.Age(~isnan(DATA.Epi_E));
age_AS_EpiD           = DATA.Age(~isnan(DATA.Epi_D));
age_AS_SemE           = DATA.Age(~isnan(DATA.Sem_E));
age_AS_SemD           = DATA.Age(~isnan(DATA.Sem_D));
age_AS_SpaE           = DATA.Age(~isnan(DATA.Spa_E));
age_AS_SpaD           = DATA.Age(~isnan(DATA.Spa_D));

sex_AS_EpiE           = DATA.Sex(~isnan(DATA.Epi_E));
sex_AS_EpiD           = DATA.Sex(~isnan(DATA.Epi_D));
sex_AS_SemE           = DATA.Sex(~isnan(DATA.Sem_E));
sex_AS_SemD           = DATA.Sex(~isnan(DATA.Sem_D));
sex_AS_SpaE           = DATA.Sex(~isnan(DATA.Spa_E));
sex_AS_SpaD           = DATA.Sex(~isnan(DATA.Spa_D));

Age_AS_EpiE           = term(age_AS_EpiE);
Sex_AS_EpiE           = term(sex_AS_EpiE);
slm_AS_EpiE           = SurfStatLinMod(EpiE_raw, 1 + Age_AS_EpiE + Sex_AS_EpiE);
res_AS_EpiE           = EpiE_raw - (slm_AS_EpiE.X * slm_AS_EpiE.coef);

Age_AS_EpiD           = term(age_AS_EpiD);
Sex_AS_EpiD           = term(sex_AS_EpiD);
slm_AS_EpiD           = SurfStatLinMod(EpiD_raw, 1 + Age_AS_EpiD + Sex_AS_EpiD);
res_AS_EpiD           = EpiD_raw - (slm_AS_EpiD.X * slm_AS_EpiD.coef);

Age_AS_SemE           = term(age_AS_SemE);
Sex_AS_SemE           = term(sex_AS_SemE);
slm_AS_SemE           = SurfStatLinMod(SemE_raw, 1 + Age_AS_SemE + Sex_AS_SemE);
res_AS_SemE           = SemE_raw - (slm_AS_SemE.X * slm_AS_SemE.coef);

Age_AS_SemD           = term(age_AS_SemD);
Sex_AS_SemD           = term(sex_AS_SemD);
slm_AS_SemD           = SurfStatLinMod(SemD_raw, 1 + Age_AS_SemD + Sex_AS_SemD);
res_AS_SemD           = SemD_raw - (slm_AS_SemD.X * slm_AS_SemD.coef);

Age_AS_SpaE           = term(age_AS_SpaE);
Sex_AS_SpaE           = term(sex_AS_SpaE);
slm_AS_SpaE           = SurfStatLinMod(SpaE_raw, 1 + Age_AS_SpaE + Sex_AS_SpaE);
res_AS_SpaE           = SpaE_raw - (slm_AS_SpaE.X * slm_AS_SpaE.coef);

Age_AS_SpaD           = term(age_AS_SpaD);
Sex_AS_SpaD           = term(sex_AS_SpaD);
slm_AS_SpaD           = SurfStatLinMod(SpaD_raw, 1 + Age_AS_SpaD + Sex_AS_SpaD);
res_AS_SpaD           = SpaD_raw - (slm_AS_SpaD.X * slm_AS_SpaD.coef);

groups_AS_EpiE        = DATA.Group(~isnan(DATA.Epi_E));
groups_AS_EpiD        = DATA.Group(~isnan(DATA.Epi_D));
groups_AS_SemE        = DATA.Group(~isnan(DATA.Sem_E));
groups_AS_SemD        = DATA.Group(~isnan(DATA.Sem_D));
groups_AS_SpaE        = DATA.Group(~isnan(DATA.Spa_E));
groups_AS_SpaD        = DATA.Group(~isnan(DATA.Spa_D));

HC_res_AS_EpiE        = res_AS_EpiE(groups_AS_EpiE == "HC");
HC_res_AS_EpiD        = res_AS_EpiD(groups_AS_EpiD == "HC");
HC_res_AS_SemE        = res_AS_SemE(groups_AS_SemE == "HC");
HC_res_AS_SemD        = res_AS_SemD(groups_AS_SemD == "HC");
HC_res_AS_SpaE        = res_AS_SpaE(groups_AS_SpaE == "HC");
HC_res_AS_SpaD        = res_AS_SpaD(groups_AS_SpaD == "HC");

TLE_res_AS_EpiE       = res_AS_EpiE(groups_AS_EpiE == "TLE");
TLE_res_AS_EpiD       = res_AS_EpiD(groups_AS_EpiD == "TLE");
TLE_res_AS_SemE       = res_AS_SemE(groups_AS_SemE == "TLE");
TLE_res_AS_SemD       = res_AS_SemD(groups_AS_SemD == "TLE");
TLE_res_AS_SpaE       = res_AS_SpaE(groups_AS_SpaE == "TLE");
TLE_res_AS_SpaD       = res_AS_SpaD(groups_AS_SpaD == "TLE");

cohenD_AS_EpiE        = Cohen(HC_res_AS_EpiE, TLE_res_AS_EpiE);
cohenD_AS_EpiD        = Cohen(HC_res_AS_EpiD, TLE_res_AS_EpiD);
cohenD_AS_SemE        = Cohen(HC_res_AS_SemE, TLE_res_AS_SemE);
cohenD_AS_SemD        = Cohen(HC_res_AS_SemD, TLE_res_AS_SemD);
cohenD_AS_SpaE        = Cohen(HC_res_AS_SpaE, TLE_res_AS_SpaE);
cohenD_AS_SpaD        = Cohen(HC_res_AS_SpaD, TLE_res_AS_SpaD);

measure               = {'AS_HC-TLE_EpiE';
                         'AS_HC-TLE_EpiD';
                         'AS_HC-TLE_SemE';
                         'AS_HC-TLE_SemD';
                         'AS_HC-TLE_SpaE';
                         'AS_HC-TLE_SpaD'};

nHC                   = [size(HC_res_AS_EpiE, 1);
                         size(HC_res_AS_EpiD, 1);
                         size(HC_res_AS_SemE, 1);
                         size(HC_res_AS_SemD, 1);
                         size(HC_res_AS_SpaE, 1);
                         size(HC_res_AS_SpaD, 1)];

nTLE                  = [size(TLE_res_AS_EpiE, 1);
                         size(TLE_res_AS_EpiD, 1);
                         size(TLE_res_AS_SemE, 1);
                         size(TLE_res_AS_SemD, 1);
                         size(TLE_res_AS_SpaE, 1);
                         size(TLE_res_AS_SpaD, 1)];

CohenD                = [cohenD_AS_EpiE;
                         cohenD_AS_EpiD;
                         cohenD_AS_SemE;
                         cohenD_AS_SemD;
                         cohenD_AS_SpaE;
                         cohenD_AS_SpaD];

AS_Results            = [table(measure) table(CohenD) table(nHC) table(nTLE)];

%% cohen's D for residual scores (age/sex/epitrack regressed out)

EpiE_ASE               = DATA.Epi_E(~or(isnan(DATA.Epitrack_total_ageCorrected), isnan(DATA.Epi_E)));
EpiD_ASE               = DATA.Epi_D(~or(isnan(DATA.Epitrack_total_ageCorrected), isnan(DATA.Epi_D)));
SemE_ASE               = DATA.Sem_E(~or(isnan(DATA.Epitrack_total_ageCorrected), isnan(DATA.Sem_E)));
SemD_ASE               = DATA.Sem_D(~or(isnan(DATA.Epitrack_total_ageCorrected), isnan(DATA.Sem_D)));
SpaE_ASE               = DATA.Spa_E(~or(isnan(DATA.Epitrack_total_ageCorrected), isnan(DATA.Spa_E)));
SpaD_ASE               = DATA.Spa_D(~or(isnan(DATA.Epitrack_total_ageCorrected), isnan(DATA.Spa_D)));

EPI_EpiE              = DATA.Epitrack_total_ageCorrected(~or(isnan(DATA.Epitrack_total_ageCorrected), isnan(DATA.Epi_E)));
EPI_EpiD              = DATA.Epitrack_total_ageCorrected(~or(isnan(DATA.Epitrack_total_ageCorrected), isnan(DATA.Epi_D)));
EPI_SemE              = DATA.Epitrack_total_ageCorrected(~or(isnan(DATA.Epitrack_total_ageCorrected), isnan(DATA.Sem_E)));
EPI_SemD              = DATA.Epitrack_total_ageCorrected(~or(isnan(DATA.Epitrack_total_ageCorrected), isnan(DATA.Sem_D)));
EPI_SpaE              = DATA.Epitrack_total_ageCorrected(~or(isnan(DATA.Epitrack_total_ageCorrected), isnan(DATA.Spa_E)));
EPI_SpaD              = DATA.Epitrack_total_ageCorrected(~or(isnan(DATA.Epitrack_total_ageCorrected), isnan(DATA.Spa_D)));

age_ASE_EpiE          = DATA.Age(~or(isnan(DATA.Epitrack_total_ageCorrected), isnan(DATA.Epi_E)));
age_ASE_EpiD          = DATA.Age(~or(isnan(DATA.Epitrack_total_ageCorrected), isnan(DATA.Epi_D)));
age_ASE_SemE          = DATA.Age(~or(isnan(DATA.Epitrack_total_ageCorrected), isnan(DATA.Sem_E)));
age_ASE_SemD          = DATA.Age(~or(isnan(DATA.Epitrack_total_ageCorrected), isnan(DATA.Sem_D)));
age_ASE_SpaE          = DATA.Age(~or(isnan(DATA.Epitrack_total_ageCorrected), isnan(DATA.Spa_E)));
age_ASE_SpaD          = DATA.Age(~or(isnan(DATA.Epitrack_total_ageCorrected), isnan(DATA.Spa_D)));

sex_ASE_EpiE          = DATA.Sex(~or(isnan(DATA.Epitrack_total_ageCorrected), isnan(DATA.Epi_E)));
sex_ASE_EpiD          = DATA.Sex(~or(isnan(DATA.Epitrack_total_ageCorrected), isnan(DATA.Epi_D)));
sex_ASE_SemE          = DATA.Sex(~or(isnan(DATA.Epitrack_total_ageCorrected), isnan(DATA.Sem_E)));
sex_ASE_SemD          = DATA.Sex(~or(isnan(DATA.Epitrack_total_ageCorrected), isnan(DATA.Sem_D)));
sex_ASE_SpaE          = DATA.Sex(~or(isnan(DATA.Epitrack_total_ageCorrected), isnan(DATA.Spa_E)));
sex_ASE_SpaD          = DATA.Sex(~or(isnan(DATA.Epitrack_total_ageCorrected), isnan(DATA.Spa_D)));

Age_ASE_EpiE          = term(age_ASE_EpiE);
Sex_ASE_EpiE          = term(sex_ASE_EpiE);
slm_ASE_EpiE          = SurfStatLinMod(EpiE_ASE, 1 + Age_ASE_EpiE + Sex_ASE_EpiE);
res_ASE_EpiE          = EpiE_ASE - (slm_ASE_EpiE.X * slm_ASE_EpiE.coef);

Age_ASE_EpiD          = term(age_ASE_EpiD);
Sex_ASE_EpiD          = term(sex_ASE_EpiD);
slm_ASE_EpiD          = SurfStatLinMod(EpiD_ASE, 1 + Age_ASE_EpiD + Sex_ASE_EpiD);
res_ASE_EpiD          = EpiD_ASE - (slm_ASE_EpiD.X * slm_ASE_EpiD.coef);

Age_ASE_SemE          = term(age_ASE_SemE);
Sex_ASE_SemE          = term(sex_ASE_SemE);
slm_ASE_SemE          = SurfStatLinMod(SemE_ASE, 1 + Age_ASE_SemE + Sex_ASE_SemE);
res_ASE_SemE          = SemE_ASE - (slm_ASE_SemE.X * slm_ASE_SemE.coef);

Age_ASE_SemD          = term(age_ASE_SemD);
Sex_ASE_SemD          = term(sex_ASE_SemD);
slm_ASE_SemD          = SurfStatLinMod(SemD_ASE, 1 + Age_ASE_SemD + Sex_ASE_SemD);
res_ASE_SemD          = SemD_ASE - (slm_ASE_SemD.X * slm_ASE_SemD.coef);

Age_ASE_SpaE          = term(age_ASE_SpaE);
Sex_ASE_SpaE          = term(sex_ASE_SpaE);
slm_ASE_SpaE          = SurfStatLinMod(SpaE_ASE, 1 + Age_ASE_SpaE + Sex_ASE_SpaE);
res_ASE_SpaE          = SpaE_ASE - (slm_ASE_SpaE.X * slm_ASE_SpaE.coef);

Age_ASE_SpaD          = term(age_ASE_SpaD);
Sex_ASE_SpaD          = term(sex_ASE_SpaD);
slm_ASE_SpaD          = SurfStatLinMod(SpaD_ASE, 1 + Age_ASE_SpaD + Sex_ASE_SpaD);
res_ASE_SpaD          = SpaD_ASE - (slm_ASE_SpaD.X * slm_ASE_SpaD.coef);

groups_ASE_EpiE       = DATA.Group(~or(isnan(DATA.Epitrack_total_ageCorrected), isnan(DATA.Epi_E)));
groups_ASE_EpiD       = DATA.Group(~or(isnan(DATA.Epitrack_total_ageCorrected), isnan(DATA.Epi_D)));
groups_ASE_SemE       = DATA.Group(~or(isnan(DATA.Epitrack_total_ageCorrected), isnan(DATA.Sem_E)));
groups_ASE_SemD       = DATA.Group(~or(isnan(DATA.Epitrack_total_ageCorrected), isnan(DATA.Sem_D)));
groups_ASE_SpaE       = DATA.Group(~or(isnan(DATA.Epitrack_total_ageCorrected), isnan(DATA.Spa_E)));
groups_ASE_SpaD       = DATA.Group(~or(isnan(DATA.Epitrack_total_ageCorrected), isnan(DATA.Spa_D)));

HC_res_ASE_EpiE       = res_ASE_EpiE(groups_ASE_EpiE == "HC");
HC_res_ASE_EpiD       = res_ASE_EpiD(groups_ASE_EpiD == "HC");
HC_res_ASE_SemE       = res_ASE_SemE(groups_ASE_SemE == "HC");
HC_res_ASE_SemD       = res_ASE_SemD(groups_ASE_SemD == "HC");
HC_res_ASE_SpaE       = res_ASE_SpaE(groups_ASE_SpaE == "HC");
HC_res_ASE_SpaD       = res_ASE_SpaD(groups_ASE_SpaD == "HC");

TLE_res_ASE_EpiE      = res_ASE_EpiE(groups_ASE_EpiE == "TLE");
TLE_res_ASE_EpiD      = res_ASE_EpiD(groups_ASE_EpiD == "TLE");
TLE_res_ASE_SemE      = res_ASE_SemE(groups_ASE_SemE == "TLE");
TLE_res_ASE_SemD      = res_ASE_SemD(groups_ASE_SemD == "TLE");
TLE_res_ASE_SpaE      = res_ASE_SpaE(groups_ASE_SpaE == "TLE");
TLE_res_ASE_SpaD      = res_ASE_SpaD(groups_ASE_SpaD == "TLE");

cohenD_ASE_EpiE       = Cohen(HC_res_ASE_EpiE, TLE_res_ASE_EpiE);
cohenD_ASE_EpiD       = Cohen(HC_res_ASE_EpiD, TLE_res_ASE_EpiD);
cohenD_ASE_SemE       = Cohen(HC_res_ASE_SemE, TLE_res_ASE_SemE);
cohenD_ASE_SemD       = Cohen(HC_res_ASE_SemD, TLE_res_ASE_SemD);
cohenD_ASE_SpaE       = Cohen(HC_res_ASE_SpaE, TLE_res_ASE_SpaE);
cohenD_ASE_SpaD       = Cohen(HC_res_ASE_SpaD, TLE_res_ASE_SpaD);

measure               = {'ASE_HC-TLE_EpiE';
                         'ASE_HC-TLE_EpiD';
                         'ASE_HC-TLE_SemE';
                         'ASE_HC-TLE_SemD';
                         'ASE_HC-TLE_SpaE';
                         'ASE_HC-TLE_SpaD'};

nHC                   = [size(HC_res_ASE_EpiE, 1);
                         size(HC_res_ASE_EpiD, 1);
                         size(HC_res_ASE_SemE, 1);
                         size(HC_res_ASE_SemD, 1);
                         size(HC_res_ASE_SpaE, 1);
                         size(HC_res_ASE_SpaD, 1)];

nTLE                  = [size(TLE_res_ASE_EpiE, 1);
                         size(TLE_res_ASE_EpiD, 1);
                         size(TLE_res_ASE_SemE, 1);
                         size(TLE_res_ASE_SemD, 1);
                         size(TLE_res_ASE_SpaE, 1);
                         size(TLE_res_ASE_SpaD, 1)];

CohenD                = [cohenD_ASE_EpiE;
                         cohenD_ASE_EpiD;
                         cohenD_ASE_SemE;
                         cohenD_ASE_SemD;
                         cohenD_ASE_SpaE;
                         cohenD_ASE_SpaD];

ASE_Results           = [table(measure) table(CohenD) table(nHC) table(nTLE)];

%% cohen's D for residual scores (age/sex/moca regressed out)

EpiE_ASM              = DATA.Epi_E(~or(isnan(DATA.Moca_total), isnan(DATA.Epi_E)));
EpiD_ASM              = DATA.Epi_D(~or(isnan(DATA.Moca_total), isnan(DATA.Epi_D)));
SemE_ASM              = DATA.Sem_E(~or(isnan(DATA.Moca_total), isnan(DATA.Sem_E)));
SemD_ASM              = DATA.Sem_D(~or(isnan(DATA.Moca_total), isnan(DATA.Sem_D)));
SpaE_ASM              = DATA.Spa_E(~or(isnan(DATA.Moca_total), isnan(DATA.Spa_E)));
SpaD_ASM              = DATA.Spa_D(~or(isnan(DATA.Moca_total), isnan(DATA.Spa_D)));

Moca_EpiE             = DATA.Moca_total(~or(isnan(DATA.Moca_total), isnan(DATA.Epi_E)));
Moca_EpiD             = DATA.Moca_total(~or(isnan(DATA.Moca_total), isnan(DATA.Epi_D)));
Moca_SemE             = DATA.Moca_total(~or(isnan(DATA.Moca_total), isnan(DATA.Sem_E)));
Moca_SemD             = DATA.Moca_total(~or(isnan(DATA.Moca_total), isnan(DATA.Sem_D)));
Moca_SpaE             = DATA.Moca_total(~or(isnan(DATA.Moca_total), isnan(DATA.Spa_E)));
Moca_SpaD             = DATA.Moca_total(~or(isnan(DATA.Moca_total), isnan(DATA.Spa_D)));

age_ASM_EpiE          = DATA.Age(~or(isnan(DATA.Moca_total), isnan(DATA.Epi_E)));
age_ASM_EpiD          = DATA.Age(~or(isnan(DATA.Moca_total), isnan(DATA.Epi_D)));
age_ASM_SemE          = DATA.Age(~or(isnan(DATA.Moca_total), isnan(DATA.Sem_E)));
age_ASM_SemD          = DATA.Age(~or(isnan(DATA.Moca_total), isnan(DATA.Sem_D)));
age_ASM_SpaE          = DATA.Age(~or(isnan(DATA.Moca_total), isnan(DATA.Spa_E)));
age_ASM_SpaD          = DATA.Age(~or(isnan(DATA.Moca_total), isnan(DATA.Spa_D)));

sex_ASM_EpiE          = DATA.Sex(~or(isnan(DATA.Moca_total), isnan(DATA.Epi_E)));
sex_ASM_EpiD          = DATA.Sex(~or(isnan(DATA.Moca_total), isnan(DATA.Epi_D)));
sex_ASM_SemE          = DATA.Sex(~or(isnan(DATA.Moca_total), isnan(DATA.Sem_E)));
sex_ASM_SemD          = DATA.Sex(~or(isnan(DATA.Moca_total), isnan(DATA.Sem_D)));
sex_ASM_SpaE          = DATA.Sex(~or(isnan(DATA.Moca_total), isnan(DATA.Spa_E)));
sex_ASM_SpaD          = DATA.Sex(~or(isnan(DATA.Moca_total), isnan(DATA.Spa_D)));

Age_ASM_EpiE          = term(age_ASM_EpiE);
Sex_ASM_EpiE          = term(sex_ASM_EpiE);
slm_ASM_EpiE          = SurfStatLinMod(EpiE_ASM, 1 + Age_ASM_EpiE + Sex_ASM_EpiE);
res_ASM_EpiE          = EpiE_ASM - (slm_ASM_EpiE.X * slm_ASM_EpiE.coef);

Age_ASM_EpiD          = term(age_ASM_EpiD);
Sex_ASM_EpiD          = term(sex_ASM_EpiD);
slm_ASM_EpiD          = SurfStatLinMod(EpiD_ASM, 1 + Age_ASM_EpiD + Sex_ASM_EpiD);
res_ASM_EpiD          = EpiD_ASM - (slm_ASM_EpiD.X * slm_ASM_EpiD.coef);

Age_ASM_SemE          = term(age_ASM_SemE);
Sex_ASM_SemE          = term(sex_ASM_SemE);
slm_ASM_SemE          = SurfStatLinMod(SemE_ASM, 1 + Age_ASM_SemE + Sex_ASM_SemE);
res_ASM_SemE          = SemE_ASM - (slm_ASM_SemE.X * slm_ASM_SemE.coef);

Age_ASM_SemD          = term(age_ASM_SemD);
Sex_ASM_SemD          = term(sex_ASM_SemD);
slm_ASM_SemD          = SurfStatLinMod(SemD_ASM, 1 + Age_ASM_SemD + Sex_ASM_SemD);
res_ASM_SemD          = SemD_ASM - (slm_ASM_SemD.X * slm_ASM_SemD.coef);

Age_ASM_SpaE          = term(age_ASM_SpaE);
Sex_ASM_SpaE          = term(sex_ASM_SpaE);
slm_ASM_SpaE          = SurfStatLinMod(SpaE_ASM, 1 + Age_ASM_SpaE + Sex_ASM_SpaE);
res_ASM_SpaE          = SpaE_ASM - (slm_ASM_SpaE.X * slm_ASM_SpaE.coef);

Age_ASM_SpaD          = term(age_ASM_SpaD);
Sex_ASM_SpaD          = term(sex_ASM_SpaD);
slm_ASM_SpaD          = SurfStatLinMod(SpaD_ASM, 1 + Age_ASM_SpaD + Sex_ASM_SpaD);
res_ASM_SpaD          = SpaD_ASM - (slm_ASM_SpaD.X * slm_ASM_SpaD.coef);

groups_ASM_EpiE       = DATA.Group(~or(isnan(DATA.Moca_total), isnan(DATA.Epi_E)));
groups_ASM_EpiD       = DATA.Group(~or(isnan(DATA.Moca_total), isnan(DATA.Epi_D)));
groups_ASM_SemE       = DATA.Group(~or(isnan(DATA.Moca_total), isnan(DATA.Sem_E)));
groups_ASM_SemD       = DATA.Group(~or(isnan(DATA.Moca_total), isnan(DATA.Sem_D)));
groups_ASM_SpaE       = DATA.Group(~or(isnan(DATA.Moca_total), isnan(DATA.Spa_E)));
groups_ASM_SpaD       = DATA.Group(~or(isnan(DATA.Moca_total), isnan(DATA.Spa_D)));

HC_res_ASM_EpiE       = res_ASM_EpiE(groups_ASM_EpiE == "HC");
HC_res_ASM_EpiD       = res_ASM_EpiD(groups_ASM_EpiD == "HC");
HC_res_ASM_SemE       = res_ASM_SemE(groups_ASM_SemE == "HC");
HC_res_ASM_SemD       = res_ASM_SemD(groups_ASM_SemD == "HC");
HC_res_ASM_SpaE       = res_ASM_SpaE(groups_ASM_SpaE == "HC");
HC_res_ASM_SpaD       = res_ASM_SpaD(groups_ASM_SpaD == "HC");

TLE_res_ASM_EpiE      = res_ASM_EpiE(groups_ASM_EpiE == "TLE");
TLE_res_ASM_EpiD      = res_ASM_EpiD(groups_ASM_EpiD == "TLE");
TLE_res_ASM_SemE      = res_ASM_SemE(groups_ASM_SemE == "TLE");
TLE_res_ASM_SemD      = res_ASM_SemD(groups_ASM_SemD == "TLE");
TLE_res_ASM_SpaE      = res_ASM_SpaE(groups_ASM_SpaE == "TLE");
TLE_res_ASM_SpaD      = res_ASM_SpaD(groups_ASM_SpaD == "TLE");

cohenD_ASM_EpiE       = Cohen(HC_res_ASM_EpiE, TLE_res_ASM_EpiE);
cohenD_ASM_EpiD       = Cohen(HC_res_ASM_EpiD, TLE_res_ASM_EpiD);
cohenD_ASM_SemE       = Cohen(HC_res_ASM_SemE, TLE_res_ASM_SemE);
cohenD_ASM_SemD       = Cohen(HC_res_ASM_SemD, TLE_res_ASM_SemD);
cohenD_ASM_SpaE       = Cohen(HC_res_ASM_SpaE, TLE_res_ASM_SpaE);
cohenD_ASM_SpaD       = Cohen(HC_res_ASM_SpaD, TLE_res_ASM_SpaD);

measure               = {'ASM_HC-TLE_EpiE';
                         'ASM_HC-TLE_EpiD';
                         'ASM_HC-TLE_SemE';
                         'ASM_HC-TLE_SemD';
                         'ASM_HC-TLE_SpaE';
                         'ASM_HC-TLE_SpaD'};

nHC                   = [size(HC_res_ASM_EpiE, 1);
                         size(HC_res_ASM_EpiD, 1);
                         size(HC_res_ASM_SemE, 1);
                         size(HC_res_ASM_SemD, 1);
                         size(HC_res_ASM_SpaE, 1);
                         size(HC_res_ASM_SpaD, 1)];

nTLE                  = [size(TLE_res_ASM_EpiE, 1);
                         size(TLE_res_ASM_EpiD, 1);
                         size(TLE_res_ASM_SemE, 1);
                         size(TLE_res_ASM_SemD, 1);
                         size(TLE_res_ASM_SpaE, 1);
                         size(TLE_res_ASM_SpaD, 1)];

CohenD                = [cohenD_ASM_EpiE;
                         cohenD_ASM_EpiD;
                         cohenD_ASM_SemE;
                         cohenD_ASM_SemD;
                         cohenD_ASM_SpaE;
                         cohenD_ASM_SpaD];

ASM_Results           = [table(measure) table(CohenD) table(nHC) table(nTLE)];

%% cohen's D for residual scores (age/sex/education regressed out)
EpiE_ASEd               = DATA.Epi_E(~or(isnan(DATA.edu_score), isnan(DATA.Epi_E)));
EpiD_ASEd               = DATA.Epi_D(~or(isnan(DATA.edu_score), isnan(DATA.Epi_D)));
SemE_ASEd               = DATA.Sem_E(~or(isnan(DATA.edu_score), isnan(DATA.Sem_E)));
SemD_ASEd               = DATA.Sem_D(~or(isnan(DATA.edu_score), isnan(DATA.Sem_D)));
SpaE_ASEd               = DATA.Spa_E(~or(isnan(DATA.edu_score), isnan(DATA.Spa_E)));
SpaD_ASEd               = DATA.Spa_D(~or(isnan(DATA.edu_score), isnan(DATA.Spa_D)));

EPI_EpiE              = DATA.edu_score(~or(isnan(DATA.edu_score), isnan(DATA.Epi_E)));
EPI_EpiD              = DATA.edu_score(~or(isnan(DATA.edu_score), isnan(DATA.Epi_D)));
EPI_SemE              = DATA.edu_score(~or(isnan(DATA.edu_score), isnan(DATA.Sem_E)));
EPI_SemD              = DATA.edu_score(~or(isnan(DATA.edu_score), isnan(DATA.Sem_D)));
EPI_SpaE              = DATA.edu_score(~or(isnan(DATA.edu_score), isnan(DATA.Spa_E)));
EPI_SpaD              = DATA.edu_score(~or(isnan(DATA.edu_score), isnan(DATA.Spa_D)));

age_ASEd_EpiE          = DATA.Age(~or(isnan(DATA.edu_score), isnan(DATA.Epi_E)));
age_ASEd_EpiD          = DATA.Age(~or(isnan(DATA.edu_score), isnan(DATA.Epi_D)));
age_ASEd_SemE          = DATA.Age(~or(isnan(DATA.edu_score), isnan(DATA.Sem_E)));
age_ASEd_SemD          = DATA.Age(~or(isnan(DATA.edu_score), isnan(DATA.Sem_D)));
age_ASEd_SpaE          = DATA.Age(~or(isnan(DATA.edu_score), isnan(DATA.Spa_E)));
age_ASEd_SpaD          = DATA.Age(~or(isnan(DATA.edu_score), isnan(DATA.Spa_D)));

sex_ASEd_EpiE          = DATA.Sex(~or(isnan(DATA.edu_score), isnan(DATA.Epi_E)));
sex_ASEd_EpiD          = DATA.Sex(~or(isnan(DATA.edu_score), isnan(DATA.Epi_D)));
sex_ASEd_SemE          = DATA.Sex(~or(isnan(DATA.edu_score), isnan(DATA.Sem_E)));
sex_ASEd_SemD          = DATA.Sex(~or(isnan(DATA.edu_score), isnan(DATA.Sem_D)));
sex_ASEd_SpaE          = DATA.Sex(~or(isnan(DATA.edu_score), isnan(DATA.Spa_E)));
sex_ASEd_SpaD          = DATA.Sex(~or(isnan(DATA.edu_score), isnan(DATA.Spa_D)));

Age_ASEd_EpiE          = term(age_ASEd_EpiE);
Sex_ASEd_EpiE          = term(sex_ASEd_EpiE);
slm_ASEd_EpiE          = SurfStatLinMod(EpiE_ASEd, 1 + Age_ASEd_EpiE + Sex_ASEd_EpiE);
res_ASEd_EpiE          = EpiE_ASEd - (slm_ASEd_EpiE.X * slm_ASEd_EpiE.coef);

Age_ASEd_EpiD          = term(age_ASEd_EpiD);
Sex_ASEd_EpiD          = term(sex_ASEd_EpiD);
slm_ASEd_EpiD          = SurfStatLinMod(EpiD_ASEd, 1 + Age_ASEd_EpiD + Sex_ASEd_EpiD);
res_ASEd_EpiD          = EpiD_ASEd - (slm_ASEd_EpiD.X * slm_ASEd_EpiD.coef);

Age_ASEd_SemE          = term(age_ASEd_SemE);
Sex_ASEd_SemE          = term(sex_ASEd_SemE);
slm_ASEd_SemE          = SurfStatLinMod(SemE_ASEd, 1 + Age_ASEd_SemE + Sex_ASEd_SemE);
res_ASEd_SemE          = SemE_ASEd - (slm_ASEd_SemE.X * slm_ASEd_SemE.coef);

Age_ASEd_SemD          = term(age_ASEd_SemD);
Sex_ASEd_SemD          = term(sex_ASEd_SemD);
slm_ASEd_SemD          = SurfStatLinMod(SemD_ASEd, 1 + Age_ASEd_SemD + Sex_ASEd_SemD);
res_ASEd_SemD          = SemD_ASEd - (slm_ASEd_SemD.X * slm_ASEd_SemD.coef);

Age_ASEd_SpaE          = term(age_ASEd_SpaE);
Sex_ASEd_SpaE          = term(sex_ASEd_SpaE);
slm_ASEd_SpaE          = SurfStatLinMod(SpaE_ASEd, 1 + Age_ASEd_SpaE + Sex_ASEd_SpaE);
res_ASEd_SpaE          = SpaE_ASEd - (slm_ASEd_SpaE.X * slm_ASEd_SpaE.coef);

Age_ASEd_SpaD          = term(age_ASEd_SpaD);
Sex_ASEd_SpaD          = term(sex_ASEd_SpaD);
slm_ASEd_SpaD          = SurfStatLinMod(SpaD_ASEd, 1 + Age_ASEd_SpaD + Sex_ASEd_SpaD);
res_ASEd_SpaD          = SpaD_ASEd - (slm_ASEd_SpaD.X * slm_ASEd_SpaD.coef);

groups_ASEd_EpiE       = DATA.Group(~or(isnan(DATA.edu_score), isnan(DATA.Epi_E)));
groups_ASEd_EpiD       = DATA.Group(~or(isnan(DATA.edu_score), isnan(DATA.Epi_D)));
groups_ASEd_SemE       = DATA.Group(~or(isnan(DATA.edu_score), isnan(DATA.Sem_E)));
groups_ASEd_SemD       = DATA.Group(~or(isnan(DATA.edu_score), isnan(DATA.Sem_D)));
groups_ASEd_SpaE       = DATA.Group(~or(isnan(DATA.edu_score), isnan(DATA.Spa_E)));
groups_ASEd_SpaD       = DATA.Group(~or(isnan(DATA.edu_score), isnan(DATA.Spa_D)));

HC_res_ASEd_EpiE       = res_ASEd_EpiE(groups_ASEd_EpiE == "HC");
HC_res_ASEd_EpiD       = res_ASEd_EpiD(groups_ASEd_EpiD == "HC");
HC_res_ASEd_SemE       = res_ASEd_SemE(groups_ASEd_SemE == "HC");
HC_res_ASEd_SemD       = res_ASEd_SemD(groups_ASEd_SemD == "HC");
HC_res_ASEd_SpaE       = res_ASEd_SpaE(groups_ASEd_SpaE == "HC");
HC_res_ASEd_SpaD       = res_ASEd_SpaD(groups_ASEd_SpaD == "HC");

TLE_res_ASEd_EpiE      = res_ASEd_EpiE(groups_ASEd_EpiE == "TLE");
TLE_res_ASEd_EpiD      = res_ASEd_EpiD(groups_ASEd_EpiD == "TLE");
TLE_res_ASEd_SemE      = res_ASEd_SemE(groups_ASEd_SemE == "TLE");
TLE_res_ASEd_SemD      = res_ASEd_SemD(groups_ASEd_SemD == "TLE");
TLE_res_ASEd_SpaE      = res_ASEd_SpaE(groups_ASEd_SpaE == "TLE");
TLE_res_ASEd_SpaD      = res_ASEd_SpaD(groups_ASEd_SpaD == "TLE");

cohenD_ASEd_EpiE       = Cohen(HC_res_ASEd_EpiE, TLE_res_ASEd_EpiE);
cohenD_ASEd_EpiD       = Cohen(HC_res_ASEd_EpiD, TLE_res_ASEd_EpiD);
cohenD_ASEd_SemE       = Cohen(HC_res_ASEd_SemE, TLE_res_ASEd_SemE);
cohenD_ASEd_SemD       = Cohen(HC_res_ASEd_SemD, TLE_res_ASEd_SemD);
cohenD_ASEd_SpaE       = Cohen(HC_res_ASEd_SpaE, TLE_res_ASEd_SpaE);
cohenD_ASEd_SpaD       = Cohen(HC_res_ASEd_SpaD, TLE_res_ASEd_SpaD);

measure               = {'ASEd_HC-TLE_EpiE';
                         'ASEd_HC-TLE_EpiD';
                         'ASEd_HC-TLE_SemE';
                         'ASEd_HC-TLE_SemD';
                         'ASEd_HC-TLE_SpaE';
                         'ASEd_HC-TLE_SpaD'};

nHC                   = [size(HC_res_ASEd_EpiE, 1);
                         size(HC_res_ASEd_EpiD, 1);
                         size(HC_res_ASEd_SemE, 1);
                         size(HC_res_ASEd_SemD, 1);
                         size(HC_res_ASEd_SpaE, 1);
                         size(HC_res_ASEd_SpaD, 1)];

nTLE                  = [size(TLE_res_ASEd_EpiE, 1);
                         size(TLE_res_ASEd_EpiD, 1);
                         size(TLE_res_ASEd_SemE, 1);
                         size(TLE_res_ASEd_SemD, 1);
                         size(TLE_res_ASEd_SpaE, 1);
                         size(TLE_res_ASEd_SpaD, 1)];

CohenD                = [cohenD_ASEd_EpiE;
                         cohenD_ASEd_EpiD;
                         cohenD_ASEd_SemE;
                         cohenD_ASEd_SemD;
                         cohenD_ASEd_SpaE;
                         cohenD_ASEd_SpaD];

ASEd_Results           = [table(measure) table(CohenD) table(nHC) table(nTLE)];

%% combine all results

all_cohenD            = [rawResults; AS_Results; ASE_Results; ASM_Results; ASEd_Results];

EpiE_cohenD           = all_cohenD.CohenD(1:6:end);
EpiD_cohenD           = all_cohenD.CohenD(2:6:end);
SemE_cohenD           = all_cohenD.CohenD(3:6:end);
SemD_cohenD           = all_cohenD.CohenD(4:6:end);
SpaE_cohenD           = all_cohenD.CohenD(5:6:end);
SpaD_cohenD           = all_cohenD.CohenD(6:6:end);

x_axis                = 1:5;
x_ticklabs            = {'raw', 'AS corrected', 'ASE corrected', 'ASM corrected', 'ASEd corrected'};

fig                   = figure; plot(x_axis, EpiE_cohenD, '--'); hold on;
                        plot(x_axis, EpiD_cohenD);
                        plot(x_axis, SemE_cohenD, '--');
                        plot(x_axis, SemD_cohenD);
                        plot(x_axis, SpaE_cohenD, '--');
                        plot(x_axis, SpaD_cohenD);
                        title("inter-group iREP Cohen's D");
                        xlim([0 5]); xticks(1:5); xticklabels(x_ticklabs);
                        ylim([-.4 1.4]); yticks(-.4:.4:1.4); ylabel("Cohen's D");
                        legend('EpiE', 'EpiD', 'SemE', 'SemD', 'SpaE', 'SpaD');
                        set(gca, 'box', 'off'); hold off;





