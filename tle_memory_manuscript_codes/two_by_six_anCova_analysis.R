## note: the ANCOVA model here is a 2x6 mixed ANOVA:
## 1 b/w subject factor 'group' w/ 2 levels (HC, TLE)
## 1 w/n subject factor 'iREP_measurement' w/ 6 levels (Epi-E, Epi-D, Sem-E, Sem-D, Spa-E, Spa-D)
## covariates are either age & sex, EpiTrack & MocA, or normalized total hippocampal volume

# acquire dependencies
pacman::p_load(pacman, dplyr, readr, rstatix)

# load data
data_file <- "/Users/shahin/Desktop/Codes/work/two_by_six_anCova_data.csv"
data <- read_csv(data_file)
data <- subset(data, select=c(id, group, iREP_measurement, accuracy, covar_age, covar_sex))
data <- na.omit(data)

# remove PX006, PX008, and PX076 (they had pre-study sx)
data <- subset(data, id != "sub-PX006" & id != "sub-PX008" & id != "sub-PX076")

# show descriptive statistics
desc_stats <- data %>%
  group_by(group, iREP_measurement) %>%
  get_summary_stats(accuracy, type="mean_sd")
print(desc_stats)

# extract residual accuracy scores (ie, regress out covariates)
covar_frml <- accuracy ~ covar_age + covar_sex
covar_model <- lm(data=data, formula=covar_frml)
data['res_accuracy'] <- covar_model$residuals

# fit ANOVA model: using formula
main_formula <- res_accuracy ~ group * iREP_measurement + Error(id/iREP_measurement)
aov_tbl <- anova_test(data=data, formula=main_formula, effect.size="pes", type=3)
get_anova_table(aov_tbl, correction="GG")

# run simple main effect of group at iREP_measurement (no need for additional decomposition since group has only 2 levels)
posthoc_formula <- res_accuracy ~ group

group_at_iREP <- data %>%
  group_by(iREP_measurement) %>%
  anova_test(formula=posthoc_formula, effect.size="pes") %>%
  get_anova_table()
group_at_iREP

# conduct pairwise comparisons between group levels for each iREP_measurement
# (it's redundant because it yields the same results as simple main effects but I need it for visualization)
pwc <- data %>%
  group_by(iREP_measurement) %>%
  pairwise_t_test(formula=posthoc_formula)
# use t_test to get t-statistics (setting var.equal to TRUE yields same results as pairwise_t_test)
pwc2 <- data %>%
  group_by(iREP_measurement) %>%
  t_test(formula=posthoc_formula, var.equal=TRUE, detailed=TRUE)
# add stats to pwc
pwc$t <- pwc2$statistic
pwc$df <- pwc2$df
pwc

res_tbl <- cbind(pwc['iREP_measurement'], pwc['t'], pwc['df'], pwc['p'], pwc['p.signif'])
res_tbl
