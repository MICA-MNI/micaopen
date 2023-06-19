## note: the ANOVA model here is a 2x6 mixed ANOVA:
## 1 b/w subject factor 'group' w/ 2 levels (HC, TLE)
## 1 w/n subject factor 'iREP_measurement' w/ 6 levels (Epi-E, Epi-D, Sem-E, Sem-D, Spa-E, Spa-D)

# acquire dependencies
pacman::p_load(pacman, dplyr, ggpubr, readr, rstatix)

# load data
data_file <- "/Users/shahin/Desktop/Codes/work/two_by_six_anova_data.csv"
data <- read_csv(data_file)

# remove PX006, PX008, and PX076 (they had pre-study sx)
data <- subset(data, id != "sub-PX006" & id != "sub-PX008" & id != "sub-PX076")

# show descriptive statistics
desc_stats <- data %>%
  group_by(group, iREP_measurement) %>%
  get_summary_stats(accuracy, type="mean_sd")
print(desc_stats)

# visualize data
bxp <- ggboxplot(data=data, x="iREP_measurement", y="accuracy", xlab="",
                 ylab="accuracy (%)", ylim=c(0, 100), width=.5,
                 color="group", palette=c("black", "darkgrey")) +
  theme(panel.background=element_rect(fill="white"), panel.grid = element_blank())
bxp

# fit ANOVA model: using formula
main_formula <- accuracy ~ group * iREP_measurement + Error(id/iREP_measurement)
aov_tbl <- anova_test(data=data, formula=main_formula, effect.size="pes")
get_anova_table(aov_tbl, correction="GG")

# run simple main effect of group at iREP_measurement (no need for additional decomposition since group has only 2 levels)
posthoc_formula <- accuracy ~ group

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

# visualize results for group_at_iREP
pwc <- pwc %>% add_xy_position(x="iREP_measurement")
pwc$y.position <- c(101.5, 101.5, 101.5, 101.5, 101.5, 101.5)
pwc$x <- c(2, 1, 4, 3, 6, 5)
pwc$xmin <- c(1.8, .8, 3.8, 2.8, 5.8, 4.8)
pwc$xmax <- c(2.2, 1.2, 4.2, 3.2, 6.2, 5.2)

bxp +
  stat_pvalue_manual(pwc, tip.length=0, hide.ns=TRUE)


res_tbl <- cbind(pwc['iREP_measurement'], pwc['t'], pwc['df'], pwc['p'], pwc['p.signif'])
res_tbl


t_tbl <- pwc['iREP_measurement']
t_tbl$baseline <- pwc$t
t_tbl$age_sex_res <- c(4.0702059, 3.0651469, 1.6961698, -0.3708203, 2.5172309, 2.0565162)
t_tbl$moca_epitrack_res <- c(3.2220548, 2.0570621, 0.9862143, -1.8930982, 2.2466266, 1.1720319)
#t_tbl$z_hip <- c(4.0546301, 3.0577508, 1.5874027, -0.9293365, 2.3744233, 1.9543916)


t_plot <- ggplot(data=t_tbl, aes(x=iREP_measurement, y=age_sex_res-baseline, group=1, linetype='age & sex')) + geom_line() + geom_point(size=.75) +
  geom_line(aes(y=moca_epitrack_res-baseline, linetype='MoCA & EpiTrack')) + geom_point(aes(y=moca_epitrack_res-baseline), size=.75) +
  theme(legend.position="bottom", legend.key=element_rect(fill="transparent", colour="transparent")) +
  #geom_line(aes(y=z_hip_res, linetype='hippocampus volume')) + geom_point(aes(y=z_hip_res), size=.75) +
  theme(panel.background=element_rect(fill="white"), panel.grid = element_blank()) +
  labs(x="", y=expression(Delta*"t"), linetype="control analysis") +
  ylim(-2.5, 0)
t_plot


## verify ANOVA assumptions: outliers
#outliers <- data %>%
#  group_by(group, iREP_measurement) %>%
#  identify_outliers(accuracy)

#extreme_idx <- outliers$is.extreme
#sub_to_remove <- outliers[extreme_idx,]['id']

#for (subID in sub_to_remove$id) {
#  data <- data[data['id']!= subID,]
#}

## verify ANOVA assumptions: normality
#data %>%
#  group_by(group, iREP_measurement) %>%
#  shapiro_test(accuracy)

#ggqqplot(data, "accuracy", ggtheme = theme_bw()) +
#  facet_grid(group ~ iREP_measurement) +
#  theme(panel.background=element_rect(fill="white"), panel.grid = element_blank())

## verify ANOVA assumptions: variance homogeneity
#data %>%
#  group_by(iREP_measurement) %>%
#  levene_test(accuracy ~ group)