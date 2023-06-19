# acquire dependencies
pacman::p_load(pacman, dplyr, ggplot2, ggpubr, readr)

# load data
data_file <- "/Users/shahin/Desktop/Codes/work/six_paired_ttest_data.csv"
data <- read_csv(data_file)

data_file2 <- "/Users/shahin/Desktop/Codes/work/two_by_six_anova_data.csv"
data2 <- read_csv(data_file2)

# remove PX006, PX008, and PX076 (they had pre-study sx)
data <- subset(data, id != "sub-PX006" & id != "sub-PX008" & id != "sub-PX076")
data2 <- subset(data2, id != "sub-PX006" & id != "sub-PX008" & id != "sub-PX076")

# split data into groupings of group_module
grouped <- group_split(data %>% group_by(group, module))
HC_epi <- do.call(rbind.data.frame, grouped[1])
HC_sem <- do.call(rbind.data.frame, grouped[2])
HC_spa <- do.call(rbind.data.frame, grouped[3])
TLE_epi <- do.call(rbind.data.frame, grouped[4])
TLE_sem <- do.call(rbind.data.frame, grouped[5])
TLE_spa <- do.call(rbind.data.frame, grouped[6])

# run all six one-tailed paired sample t-tests
HC_epiE <- HC_epi[HC_epi['condition']=='E',][['accuracy']]
HC_epiD <- HC_epi[HC_epi['condition']=='D',][['accuracy']]
HC_epi_test <- t.test(HC_epiE, HC_epiD, paired=TRUE, alternative="greater")

HC_semE <- HC_sem[HC_sem['condition']=='E',][['accuracy']]
HC_semD <- HC_sem[HC_sem['condition']=='D',][['accuracy']]
HC_sem_test <- t.test(HC_semE, HC_semD, paired=TRUE, alternative="greater")

HC_spaE <- HC_spa[HC_spa['condition']=='E',][['accuracy']]
HC_spaD <- HC_spa[HC_spa['condition']=='D',][['accuracy']]
HC_spa_test <- t.test(HC_spaE, HC_spaD, paired=TRUE, alternative="greater")

TLE_epiE <- TLE_epi[TLE_epi['condition']=='E',][['accuracy']]
TLE_epiD <- TLE_epi[TLE_epi['condition']=='D',][['accuracy']]
TLE_epi_test <- t.test(TLE_epiE, TLE_epiD, paired=TRUE, alternative="greater")

TLE_semE <- TLE_sem[TLE_sem['condition']=='E',][['accuracy']]
TLE_semD <- TLE_sem[TLE_sem['condition']=='D',][['accuracy']]
TLE_sem_test <- t.test(TLE_semE, TLE_semD, paired=TRUE, alternative="greater")

TLE_spaE <- TLE_spa[TLE_spa['condition']=='E',][['accuracy']]
TLE_spaD <- TLE_spa[TLE_spa['condition']=='D',][['accuracy']]
TLE_spa_test <- t.test(TLE_spaE, TLE_spaD, paired=TRUE, alternative="greater")

# adjust p-values w/ FDR method
p_vals <- c(HC_epi_test$p.value, HC_sem_test$p.value, HC_spa_test$p.value,
            TLE_epi_test$p.value, TLE_sem_test$p.value, TLE_spa_test$p.value)
p_fdr <- p.adjust(p_vals, method="fdr")

# print results
contrast <- c(HC_epi_test$data.name, HC_sem_test$data.name, HC_spa_test$data.name,
              TLE_epi_test$data.name, TLE_sem_test$data.name, TLE_spa_test$data.name)
t_stat <- as.numeric(c(HC_epi_test$statistic, HC_sem_test$statistic, HC_spa_test$statistic,
                       TLE_epi_test$statistic, TLE_sem_test$statistic, TLE_spa_test$statistic))
full_ttest_res <- tibble(contrast, t_stat, p_vals, p_fdr)
print(full_ttest_res)

# visualize results
HC_data <- data2[data2$group=="HC",]
TLE_data <- data2[data2$group=="TLE",]

HC_res <- full_ttest_res[1:3,]
HC_res$group1 <- c("Epi-E", "Sem-E", "Spa-E")
HC_res$group2 <- c("Epi-D", "Sem-D", "Spa-D")
HC_res$p.signif <- c("****", "****", "****")
HC_res$y.position <- c(103, 103, 103)
HC_res$x <- c(1.5, 3.5, 4.5)
HC_res$xmin <- c(1, 3, 5)
HC_res$xmax <- c(2, 4, 6)

TLE_res <- full_ttest_res[4:6,]
TLE_res$group1 <- c("Epi-E", "Sem-E", "Spa-E")
TLE_res$group2 <- c("Epi-D", "Sem-D", "Spa-D")
TLE_res$p.signif <- c("****", "****", "****")
TLE_res$y.position <- c(103, 103, 103)
TLE_res$x <- c(1.5, 3.5, 4.5)
TLE_res$xmin <- c(1, 3, 5)
TLE_res$xmax <- c(2, 4, 6)

bxp1 <- ggboxplot(HC_data, x="iREP_measurement", y="accuracy", facet.by="group", xlab=FALSE, ggtheme=theme_minimal(),
                  ylim=c(0, 105)) +
  stat_pvalue_manual(HC_res, tip.length=0, hide.ns=TRUE) + scale_y_continuous(breaks=c(0, 20, 40, 60, 80, 100)) +
  theme(axis.line = element_line(colour = "black"), panel.grid.major=element_blank(), panel.grid.minor=element_blank(),
        panel.border=element_blank(), panel.background=element_blank())

bxp2 <- ggboxplot(TLE_data, x="iREP_measurement", y="accuracy", facet.by="group", xlab=FALSE, ggtheme=theme_minimal(),
                  ylim=c(0, 105)) +
  stat_pvalue_manual(TLE_res, tip.length=0, hide.ns=TRUE) + scale_y_continuous(breaks=c(0, 20, 40, 60, 80, 100)) +
  theme(axis.line = element_line(colour = "black"), panel.grid.major=element_blank(), panel.grid.minor=element_blank(),
        panel.border=element_blank(), panel.background=element_blank())

combined_plot <- ggarrange(bxp1, bxp2, ncol=2, nrow=1)
combined_plot
