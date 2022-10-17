## Design
# linear mixed-effects model

## housekeeping__________
# import libraries
pacman::p_load(pacman, lmerTest, texreg, afex, plyr, ggplot2, tibble,
               rstatix, ggpubr, mvtnorm, emmeans, multcomp)

## data manipulation__________ 
# load data
Data <- read.csv('lmem_iREP_data.csv')

# separate HC and TLE
Data_HC <- Data[Data$Group == 'HC',]
Data_TLE <- Data[Data$Group == 'TLE',]

# remove pre-assigned HCs to homogenize age
Data_HC <- Data_HC[Data_HC$Subjects != '2' &
                     Data_HC$Subjects != '3' &
                     Data_HC$Subjects != '5' &
                     Data_HC$Subjects != '11' &
                     Data_HC$Subjects != '13' &
                     Data_HC$Subjects != '18' &
                     Data_HC$Subjects != '29' &
                     Data_HC$Subjects != '38' &
                     Data_HC$Subjects != '46' &
                     Data_HC$Subjects != '47' &
                     Data_HC$Subjects != '50' &
                     Data_HC$Subjects != '56' &
                     Data_HC$Subjects != '61',]

# separate HC & TLE datasets
Data_HC_Epi <- Data_HC[Data_HC$Task == 'Epi',]
Data_HC_Sem <- Data_HC[Data_HC$Task == 'Sem',]
Data_HC_Spa <- Data_HC[Data_HC$Task == 'Spa',]

Data_TLE_Epi <- Data_TLE[Data_TLE$Task == 'Epi',]
Data_TLE_Sem <- Data_TLE[Data_TLE$Task == 'Sem',]
Data_TLE_Spa <- Data_TLE[Data_TLE$Task == 'Spa',]

# replace diff score > easy score with NaN in HCs
HC_del_Epi <- which(Data_HC_Epi['Score'][Data_HC_Epi$Condition == 'Diff',] >
                      Data_HC_Epi['Score'][Data_HC_Epi$Condition == 'Easy',])
if (length(HC_del_Epi > 0)) {
  for(i in 1:length(HC_del_Epi)) {
    Data_HC_Epi[2*HC_del_Epi[i]-1,]['Score'] = NaN
    Data_HC_Epi[2*HC_del_Epi[i],]['Score'] = NaN
  }
}

HC_del_Sem <- which(Data_HC_Sem['Score'][Data_HC_Sem$Condition == 'Diff',] >
                      Data_HC_Sem['Score'][Data_HC_Sem$Condition == 'Easy',])
if (length(HC_del_Sem > 0)) {
  for(ii in 1:length(HC_del_Sem)) {
    Data_HC_Sem[2*HC_del_Sem[ii]-1,]['Score'] = NaN
    Data_HC_Sem[2*HC_del_Sem[ii],]['Score'] = NaN
  }
}

HC_del_Spa <- which(Data_HC_Spa['Score'][Data_HC_Spa$Condition == 'Diff',] >
                      Data_HC_Spa['Score'][Data_HC_Spa$Condition == 'Easy',])
if (length(HC_del_Spa > 0)) {
  for(iii in 1:length(HC_del_Spa)) {
    Data_HC_Spa[2*HC_del_Spa[iii]-1,]['Score'] = NaN
    Data_HC_Spa[2*HC_del_Spa[iii],]['Score'] = NaN
  }
}

# replace diff score > easy score with NaN in TLEs
TLE_del_Epi <- which(Data_TLE_Epi['Score'][Data_TLE_Epi$Condition == 'Diff',] >
                       Data_TLE_Epi['Score'][Data_TLE_Epi$Condition == 'Easy',])
if (length(TLE_del_Epi > 0)) {
  for(j in 1:length(TLE_del_Epi)) {
    Data_TLE_Epi[2*TLE_del_Epi[j]-1,]['Score'] = NaN
    Data_TLE_Epi[2*TLE_del_Epi[j],]['Score'] = NaN
  }
}

TLE_del_Sem <- which(Data_TLE_Sem['Score'][Data_TLE_Sem$Condition == 'Diff',] >
                       Data_TLE_Sem['Score'][Data_TLE_Sem$Condition == 'Easy',])
if (length(TLE_del_Sem > 0)) {
  for(jj in 1:length(TLE_del_Sem)) {
    Data_TLE_Sem[2*TLE_del_Sem[jj]-1,]['Score'] = NaN
    Data_TLE_Sem[2*TLE_del_Sem[jj],]['Score'] = NaN
  }
}

TLE_del_Spa <- which(Data_TLE_Spa['Score'][Data_TLE_Spa$Condition == 'Diff',] >
                       Data_TLE_Spa['Score'][Data_TLE_Spa$Condition == 'Easy',])
if (length(TLE_del_Spa > 0)) {
  for(jjj in 1:length(TLE_del_Spa)) {
    Data_TLE_Spa[2*TLE_del_Spa[jjj]-1,]['Score'] = NaN
    Data_TLE_Spa[2*TLE_del_Spa[jjj],]['Score'] = NaN
  }
}

# bind and resort data
unsorted <- rbind(Data_HC_Epi, Data_HC_Sem, Data_HC_Spa, Data_TLE_Epi, Data_TLE_Sem, Data_TLE_Spa)
Data <- unsorted[order(unsorted$Subjects),]

# convert Subjects to factor
Data$Subjects <- as.factor(Data$Subjects)

# convert Score to double
Data$Score <- as.double(Data$Score)

# check variable classes
lapply(Data, class)

## check ANOVA assumptions__________
# data outliers
outliers <- Data %>%
  group_by(Group, Condition, Task) %>%
  identify_outliers(Score)
outliers

# compute extreme outliers (> 3 SD from the mean) if they exist
extremes <- c()
for (i in 1:nrow(outliers)) {
  if (outliers['is.extreme'][i,] == 'TRUE') {
    to_remove <- outliers[,c(-6,-7)][i,]
    extremes <- rbind(extremes, to_remove)
  }
}
extremes <- extremes[,c(4,1,2,3,5)]
extremes

# replace extreme outliers with NaNs
if (!is.null(extremes)) {
  idx <- c()
  for (i in 1:nrow(extremes)) {
    for (j in 1:nrow(Data)) {
      if (isTRUE((which(apply(Data[j,], 1, function(x) all(x == extremes[i,]))) == 1))) {
        idx <- append(idx, j)
        Data[j,]['Score'] = NaN
      }
    }
  }
  Data[idx,]
}

# normality of factor combinations
shapiro_norm <- Data %>%
  group_by(Group, Condition, Task) %>%
  shapiro_test(Score)
shapiro_norm

# qq plots
qqPlot <- ggqqplot(Data, 'Score', ggtheme = theme_minimal(), color = 'black') +
  facet_grid(Group + Condition ~ Task, labeller = 'label_both') +
  theme(panel.background = element_rect(fill = '#e6e6e3'), panel.grid = element_blank(),
        axis.text.x = element_text(face = 'bold', color = 'black', size = 10),
        axis.text.y = element_text(face = 'bold', color = 'black', size = 10))
qqPlot

# homogeneity of residual variances
levene_homogen <- Data %>%
  group_by(Condition, Task) %>%
  levene_test(Score ~ Group)
levene_homogen

## descriptive stats__________
dStats <- Data %>%
  group_by(Group, Condition, Task) %>%
  get_summary_stats(Score, type = 'mean_sd')
dStats

## visualize data__________
bxp <- ggboxplot(Data, x = 'Task', xlab = FALSE, y = 'Score', ylab = 'weighted accuracy', title = 'Data overview',
                 color = 'black', palette = c('#ff0200', '#ffcc02'), fill = 'Condition', facet.by = 'Group',
                 short.panel.labs = TRUE, ggtheme = theme_minimal(), bxp.errorbar = TRUE) +
  theme(panel.background = element_rect(fill = 'white'), panel.grid = element_blank(),
        axis.text.x = element_text(face = 'bold', color = 'black', size = 10),
        axis.text.y = element_text(face = 'bold', color = 'black', size = 10),
        axis.title.y = element_text(face = 'bold'))
bxp

## generate mixed effects models & choose the optimal one__________
# define models
M1 <- lmer(Score ~ 1 + Group + Task + Condition + (1|Subjects), data=Data)
M2 <- lmer(Score ~ 1 + Group * Task + Condition + (1|Subjects), data=Data)
M3 <- lmer(Score ~ 1 + Group * Condition + Task + (1|Subjects), data=Data)
M4 <- lmer(Score ~ 1 + Group + Task * Condition + (1|Subjects), data=Data)
M5 <- lmer(Score ~ 1 + Group * Task * Condition + (1|Subjects), data=Data)
M6 <- lmer(Score ~ 1 + Group + Task + Condition + Group:Task + Task:Condition + (1|Subjects), data=Data)

# compare models using likelihood ratio tests
lrt <- anova(M1, M2, M3, M4, M5, M6, test='LRT')
lrt

## Analysis & results
# main results
aov_tbl <- anova(M6)
aov_tbl
part_eta_vals <- partial_eta_squared(M6)
part_eta_vals

## simple Task x Condition interaction__________
# Condition @ Task
Cond_Task <- by(Data, Data$Task, lmer, formula = Score ~ 1 + Condition + (1 | Subjects))
Cond_at_Epi <- anova(Cond_Task$Epi)
Cond_at_Sem <- anova(Cond_Task$Sem)
Cond_at_Spa <- anova(Cond_Task$Spa)
Cond_at_Epi
Cond_at_Sem
Cond_at_Spa

        # post-hoc pairwise comparisons
        pwc_CatT <- emmeans(M6, pairwise ~ Condition | Task, adjust = 'fdr')
        pwc_CatT$contrasts

# Task @ Condition
Task_Cond <- by(Data, Data$Condition, lmer, formula = Score ~ 1 + Task + (1 | Subjects))
Task_at_Diff <- anova(Task_Cond$Diff)
Task_at_Easy <- anova(Task_Cond$Easy)
Task_at_Diff
Task_at_Easy

        # post-hoc pairwise comparisons
        pwc_TatC <- emmeans(M6, pairwise ~ Task | Condition, adjust = 'fdr')
        pwc_TatC$contrasts

# visualize Condition x Task interaction
barP_CxT <- ggbarplot(data = Data, x = 'Task', xlab = FALSE, y = 'Score', ylab = 'weighted accuracy',
                      title = 'Condition x Task', color = 'black', palette = c('#E69F00', 'lightgray'),
                      fill = 'Condition', position = position_dodge(.7), add = 'mean_se',
                      error.plot = 'errorbar')

star_CatT = ""
if (Cond_at_Epi$`Pr(>F)` < 0.05) {
  if (summary(pwc_CatT$contrasts)$p.value[1] < 0.0001) {
    star_CatT[1] = "****"
  } else if (summary(pwc_CatT$contrasts)$p.value[1] < 0.001) {
    star_CatT[1] = "***"
  } else if (summary(pwc_CatT$contrasts)$p.value[1] < 0.01) {
    star_CatT[1] = "**"
  } else if (summary(pwc_CatT$contrasts)$p.value[1] < 0.05) {
    star_CatT[1] = "*"
  } else {
    star_CatT[1] = " "
  }
} else {
  star_CatT[1] = " "
}
if (Cond_at_Sem$`Pr(>F)` < 0.05) {
  if (summary(pwc_CatT$contrasts)$p.value[2] < 0.0001) {
    star_CatT[2] = "****"
  } else if (summary(pwc_CatT$contrasts)$p.value[2] < 0.001) {
    star_CatT[2] = "***"
  } else if (summary(pwc_CatT$contrasts)$p.value[2] < 0.01) {
    star_CatT[2] = "**"
  } else if (summary(pwc_CatT$contrasts)$p.value[2] < 0.05) {
    star_CatT[2] = "*"
  } else {
    star_CatT[2] = " "
  }
} else {
  star_CatT[2] = " "
}
if (Cond_at_Spa$`Pr(>F)` < 0.05) {
  if (summary(pwc_CatT$contrasts)$p.value[3] < 0.0001) {
    star_CatT[3] = "****"
  } else if (summary(pwc_CatT$contrasts)$p.value[3] < 0.001) {
    star_CatT[3] = "***"
  } else if (summary(pwc_CatT$contrasts)$p.value[3] < 0.01) {
    star_CatT[3] = "**"
  } else if (summary(pwc_CatT$contrasts)$p.value[3] < 0.05) {
    star_CatT[3] = "*"
  } else {
    star_CatT[3] = " "
  }
} else {
  star_CatT[3] = " "
}

pVal_CatT <- tibble(
  Task = as.factor(c('Epi', 'Sem', 'Spa')),
  group1 = c('Diff', 'Diff', 'Diff'), group2 = c('Easy', 'Easy', 'Easy'),
  p.adj = summary(pwc_CatT$contrasts)$p.value, p.adj.signif = star_CatT,
  y.position = c(83, 100, 88), x = as.integer(c(1, 2, 3)),
  xmin = c(.825, 1.825, 2.825), xmax = c(1.175, 2.175, 3.175)
)

star_TatC = ""
for (i in 1:3) {
  if (Task_at_Diff$`Pr(>F)` < 0.05) {
    if (summary(pwc_TatC$contrasts)$p.value[i] < 0.0001) {
      star_TatC[i] = "****"
    } else if (summary(pwc_TatC$contrasts)$p.value[i] < 0.001) {
      star_TatC[i] = "***"
    } else if (summary(pwc_TatC$contrasts)$p.value[i] < 0.01) {
      star_TatC[i] = "**"
    } else if (summary(pwc_TatC$contrasts)$p.value[i] < 0.05) {
      star_TatC[i] = "*"
    } else {
      star_TatC[i] = " "
    }
  } else {
    star_TatC[i] = " "
  }
}
for (i in 1:3) {
  if (Task_at_Easy$`Pr(>F)` < 0.05) {
    if (summary(pwc_TatC$contrasts)$p.value[i+3] < 0.0001) {
      star_TatC[i+3] = "****"
    } else if (summary(pwc_TatC$contrasts)$p.value[i+3] < 0.001) {
      star_TatC[i+3] = "***"
    } else if (summary(pwc_TatC$contrasts)$p.value[i+3] < 0.01) {
      star_TatC[i+3] = "**"
    } else if (summary(pwc_TatC$contrasts)$p.value[i+3] < 0.05) {
      star_TatC[i+3] = "*"
    } else {
      star_TatC[i+3] = " "
    }
  } else {
    star_TatC[i+3] = " "
  }
}

pVal_TatC <- tibble(
  Condition = as.factor(c('Diff', 'Diff', 'Diff', 'Easy', 'Easy', 'Easy')),
  group1 = c('Epi', 'Epi', 'Sem', 'Epi', 'Epi', 'Sem'), group2 = c('Sem', 'Spa', 'Spa', 'Sem', 'Spa', 'Spa'),
  p.adj = summary(pwc_TatC$contrasts)$p.value, p.adj.signif = star_TatC,
  y.position = c(106, NaN, 106, 112, 118, 112), x = as.integer(c(1, 2, 3, 4, 5, 6)),
  xmin = c(.825, NaN, 1.825, 1.175, 1.175,  2.175), xmax = c(1.825, NaN, 2.825, 2.175, 3.175, 3.175)
)

barP_CxT +
  scale_y_continuous(breaks = seq(0, 100, 25)) +
  theme(panel.background = element_rect(fill = 'white'), panel.grid = element_blank(),
        axis.text.x = element_text(face = 'bold', color = 'black', size = 10),
        axis.text.y = element_text(face = 'bold', color = 'black', size = 10),
        axis.title.y = element_text(face = 'bold')) +
  stat_pvalue_manual(pVal_CatT, label = 'p.adj.signif', tip.length = 0.01, hide.ns = TRUE) +
  stat_pvalue_manual(pVal_TatC, label = 'p.adj.signif', tip.length = 0.01, hide.ns = TRUE)

## simple Group x Task interaction__________
# Group @ Task
Group_Task <- by(Data, Data$Task, lmer, formula = Score ~ 1 + Group + (1 | Subjects))
Group_at_Epi <- anova(Group_Task$Epi)
Group_at_Sem <- anova(Group_Task$Sem)
Group_at_Spa <- anova(Group_Task$Spa)
Group_at_Epi
Group_at_Sem
Group_at_Spa

        # post-hoc pairwise comparisons
        pwc_GatT <- emmeans(M6, pairwise ~ Group | Task, adjust = 'fdr')
        pwc_GatT$contrasts

# Task @ Group
Task_Group <- by(Data, Data$Group, lmer, formula = Score ~ 1 + Task + (1 | Subjects))
Task_at_HC <- anova(Task_Group$HC)
Task_at_TLE <- anova(Task_Group$TLE)
Task_at_HC
Task_at_TLE

        # post-hoc pairwise comparisons
        pwc_TatG <- emmeans(M6, pairwise ~ Task | Group, adjust = 'fdr')
        pwc_TatG$contrasts

# visualize Group x Task interaction
barP_GxT <- ggbarplot(data = Data, x = 'Task', xlab = FALSE, y = 'Score', ylab = 'accuracy (%)',
                      title = 'Group x Task', color = 'black', palette = c('white', '#767171'),
                      fill = 'Group', position = position_dodge(.7), add = 'mean_se',
                      error.plot = 'errorbar')

star_GatT = ""
if (Group_at_Epi$`Pr(>F)` < 0.05) {
  if (summary(pwc_GatT$contrasts)$p.value[1] < 0.0001) {
    star_GatT[1] = "****"
  } else if (summary(pwc_GatT$contrasts)$p.value[1] < 0.001) {
    star_GatT[1] = "***"
  } else if (summary(pwc_GatT$contrasts)$p.value[1] < 0.01) {
    star_GatT[1] = "**"
  } else if (summary(pwc_GatT$contrasts)$p.value[1] < 0.05) {
    star_GatT[1] = "*"
  } else {
    star_GatT[1] = " "
  }
} else {
  star_GatT[1] = " "
}
if (Group_at_Sem$`Pr(>F)` < 0.05) {
  if (summary(pwc_GatT$contrasts)$p.value[2] < 0.0001) {
    star_GatT[2] = "****"
  } else if (summary(pwc_GatT$contrasts)$p.value[2] < 0.001) {
    star_GatT[2] = "***"
  } else if (summary(pwc_GatT$contrasts)$p.value[2] < 0.01) {
    star_GatT[2] = "**"
  } else if (summary(pwc_GatT$contrasts)$p.value[2] < 0.05) {
    star_GatT[2] = "*"
  } else {
    star_GatT[2] = " "
  }
} else {
  star_GatT[2] = " "
}
if (Group_at_Spa$`Pr(>F)` < 0.05) {
  if (summary(pwc_GatT$contrasts)$p.value[3] < 0.0001) {
    star_GatT[3] = "****"
  } else if (summary(pwc_GatT$contrasts)$p.value[3] < 0.001) {
    star_GatT[3] = "***"
  } else if (summary(pwc_GatT$contrasts)$p.value[3] < 0.01) {
    star_GatT[3] = "**"
  } else if (summary(pwc_GatT$contrasts)$p.value[3] < 0.05) {
    star_GatT[3] = "*"
  } else {
    star_GatT[3] = " "
  }
} else {
  star_GatT[3] = " "
}

pVal_GatT <- tibble(
  Task = as.factor(c('Epi', 'Sem', 'Spa')),
  group1 = c('HC', 'HC', 'HC'), group2 = c('TLE', 'TLE', 'TLE'),
  p.adj = summary(pwc_GatT$contrasts)$p.value, p.adj.signif = star_GatT,
  y.position = c(78, NaN, NaN), x = as.integer(c(1, 2, 3)),
  xmin = c(.825, NaN, NaN), xmax = c(1.175, NaN, NaN)
)

star_TatG = ""
for (i in 1:3) {
  if (Task_at_HC$`Pr(>F)` < 0.05) {
    if (summary(pwc_TatG$contrasts)$p.value[i] < 0.0001) {
      star_TatG[i] = "****"
    } else if (summary(pwc_TatG$contrasts)$p.value[i] < 0.001) {
      star_TatG[i] = "***"
    } else if (summary(pwc_TatG$contrasts)$p.value[i] < 0.01) {
      star_TatG[i] = "**"
    } else if (summary(pwc_TatG$contrasts)$p.value[i] < 0.05) {
      star_TatG[i] = "*"
    } else if (summary(pwc_TatG$contrasts)$p.value[i] < 0.1) {
      star_TatG[i] = "."  
    } else {
      star_TatG[i] = " "
    }
  } else {
    star_TatG[i] = " "
  }
}
for (i in 1:3) {
  if (Task_at_TLE$`Pr(>F)` < 0.05) {
    if (summary(pwc_TatG$contrasts)$p.value[i+3] < 0.0001) {
      star_TatG[i+3] = "****"
    } else if (summary(pwc_TatG$contrasts)$p.value[i+3] < 0.001) {
      star_TatG[i+3] = "***"
    } else if (summary(pwc_TatG$contrasts)$p.value[i+3] < 0.01) {
      star_TatG[i+3] = "**"
    } else if (summary(pwc_TatG$contrasts)$p.value[i+3] < 0.05) {
      star_TatG[i+3] = "*"
    }  else if (summary(pwc_TatG$contrasts)$p.value[i+3] < 0.1) {
      star_TatG[i+3] = "."
    } else {
      star_TatG[i+3] = " "
    }
  } else {
    star_TatG[i+3] = " "
  }
}

pVal_TatG <- tibble(
  Group = as.factor(c('HC', 'HC', 'HC', 'TLE', 'TLE', 'TLE')),
  group1 = c('Epi', 'Epi', 'Sem', 'Epi', 'Epi', 'Sem'), group2 = c('Sem', 'Spa', 'Spa', 'Sem', 'Spa', 'Spa'),
  p.adj = summary(pwc_TatG$contrasts)$p.value, p.adj.signif = star_TatG,
  y.position = c(90, 96, 90, 102, 108, 102), x = as.integer(c(1, 2, 3, 4, 5, 6)),
  xmin = c(.825, .825, 1.825, 1.175, 1.175,  2.175), xmax = c(1.825, 2.825, 2.825, 2.175, 3.175, 3.175)
)

barP_GxT +
  scale_y_continuous(breaks = seq(0, 100, 25)) +
  theme(panel.background = element_rect(fill = 'white'), panel.grid = element_blank(),
        axis.text.x = element_text(face = 'bold', color = 'black', size = 10),
        axis.text.y = element_text(face = 'bold', color = 'black', size = 10),
        axis.title.y = element_text(face = 'bold')) +
  stat_pvalue_manual(pVal_GatT, label = 'p.adj.signif', tip.length = 0.01, hide.ns = TRUE) +
  stat_pvalue_manual(pVal_TatG, label = 'p.adj.signif', tip.length = 0.01, hide.ns = TRUE)

## Ainsi prend fin notre aventure! __________
