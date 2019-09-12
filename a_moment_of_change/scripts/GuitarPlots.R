## spin permute z-scores

## load t-stats 
df <- read.csv('./output/moment_tstats.txt',header=FALSE)
colnames(df) <- c("mesulam", "mean", "sd", "skewness", "kurtosis", "mean_qs","sd_qs","skew_qs","kurt_qs")
df$mesulam <- as.factor(car::recode(df$mesulam,"0='cortical wall';1='paralimbic'; 2='hetermodal';3='unimodal';4='idiotypic'"))

df$mean <- replace(df$mean, df$mean_qs > 0.00625, 'no')
df$sd <- replace(df$sd, df$sd_qs > 0.00625, 'no')
df$skewness <- replace(df$skewness, df$skew_qs > 0.00625, 'no')
df$kurtosis <- replace(df$kurtosis, df$kurt_qs > 0.00625, 'no')

df$mean <- as.factor(replace(df$mean, df$mean_qs < 0.00625, 'yes'))
df$sd <- as.factor(replace(df$sd, df$sd_qs < 0.00625, 'yes'))
df$skewness <- as.factor(replace(df$skewness, df$skew_qs < 0.00625, 'yes'))
df$kurtosis <- as.factor(replace(df$kurtosis, df$kurt_qs < 0.00625, 'yes'))
df_struct <- melt(df, id= c("mesulam"), measure.vars = c("mean","sd","skewness","kurtosis"))
real_count <- table(df_struct)[,,'yes']


## load rotations and reload orginal
df <- read.csv('./output/moment_tstats.txt',header=FALSE)
colnames(df) <- c("mesulam", "mean", "sd", "skewness", "kurtosis", "mean_qs","sd_qs","skew_qs","kurt_qs")
df$mesulam <- as.factor(car::recode(df$mesulam,"0='cortical wall';1='paralimbic'; 2='hetermodal';3='unimodal';4='idiotypic'"))

df_perm <- read.csv('./data/perm_sphere_10000.csv',header = FALSE)

## spin permuta the orginal table (excluding the classes)
permTable=array(NA,c(5,4,dim(df_perm)[2]))
permTableDiff=array(NA,c(5,4,dim(df_perm)[2]))
pTable=array(NA,c(5,4,dim(df_perm)[2]))
for (i in 1:dim(df_perm)[2]){
  df_label <- df$mesulam
  df_temp <- df[df_perm[,i],2:9]
  df_temp <- cbind(df_label,df_temp)
  
  df_temp$mean <- replace(df_temp$mean, df_temp$mean_qs > 0.00625, 'no')
  df_temp$sd <- replace(df_temp$sd, df_temp$sd_qs > 0.00625, 'no')
  df_temp$skewness <-replace(df_temp$skewness, df_temp$skew_qs > 0.00625, 'no')
  df_temp$kurtosis <- replace(df_temp$kurtosis, df_temp$kurt_qs > 0.00625, 'no')
  
  df_temp$mean <- as.factor(replace(df_temp$mean, df_temp$mean_qs < 0.00625, 'yes'))
  df_temp$sd <- as.factor(replace(df_temp$sd, df_temp$sd_qs < 0.00625, 'yes'))
  df_temp$skewness <- as.factor(replace(df_temp$skewness, df_temp$skew_qs < 0.00625, 'yes'))
  df_temp$kurtosis <- as.factor(replace(df_temp$kurtosis, df_temp$kurt_qs < 0.00625, 'yes'))
  
  df_temp <- melt(df_temp, id= c("df_label"), measure.vars = c("mean","sd","skewness","kurtosis"))
  
  tempTable <- table(df_temp)
  permTable[,,i] <- tempTable[,,'yes']
}

meanTable <- apply(permTable, c(1,2), mean) 
sdTable <- apply(permTable, c(1,2), sd) 

## plot the z-scores
zTable <- (real_count-meanTable)/sdTable
cmap_mes=c("#7ca840","#f8a796", "#fbd779", "#6182ac")
cmap_ve2=c("#8B1C61", "#0000CF", "#01883D", "#EF9A01", "#FFFE01", "#01FFFF", "#FF00FE")

data <- as.data.frame(zTable)
data <- data[data$mesulam!="cortical wall", ]
data$struct <- factor(data$mesulam, levels = c("limbic", "insula", "association1","association2","secondary sensory","primary sensory","motor"))

bars <- ggplot(data=data, aes(y=Freq, x=mesulam,fill=mesulam)) +
  geom_bar(position="dodge",stat="identity",alpha = 0.5) +
  scale_fill_manual(values = cmap_mes) + 
  theme_minimal() +
  scale_x_discrete(breaks = NULL) +
  labs(x = "",
       y = "Z-Score") +
  theme(legend.position = "bottom",
        legend.title = element_blank(),
        title = element_blank()) +
  facet_grid(~variable, scales = "fixed") +
  theme(
    strip.background = element_blank(),
    strip.text.x = element_blank()
  )

## get p-values
pTable <- 2*pnorm(-abs(zTable))

## FDR correct
library(magrittr)
pTable <- pTable %>% 
  as.matrix %>% 
  as.vector %>% 
  p.adjust(method='bonferroni') %>% 
  matrix(ncol=4)

## plot null distribution with real count as points
dataReal <- as.data.frame(real_count)
dataNULL <- as.data.frame(as.table(permTable))

dataNULL$Var1<- dplyr::recode(dataNULL$Var1,A="cortical wall",B='hetermodal', 
                       C='idiotypic', D='paralimbic', E='unimodal',
                       .default = levels(dataNULL$Var1))
dataNULL$Var2<- dplyr::recode(dataNULL$Var2,A="mean",B='sd', 
                              C='skewness', D='kurtosis',
                              .default = levels(dataNULL$Var2))
dataNULL <- dataNULL[dataNULL$Var1!="cortical wall", ]
colnames(dataNULL) <- c("mesulam","variable","perm","Freq")
dataReal <- dataReal[dataReal$mesulam!="cortical wall", ]

dataFULL <- merge(dataNULL, dataReal, by = c("mesulam","variable"), all=TRUE)
dataFULL$mesulam <- factor(dataFULL$mesulam, levels = c("paralimbic", "hetermodal", "unimodal","idiotypic"))

ggplot(data=dataFULL, aes(y=mesulam,x=Freq.x,fill=mesulam)) +
  geom_density_ridges(alpha = 0.2) +
  geom_point(aes(y=mesulam,x=Freq.y, fill=mesulam),size=5,shape=21) +
  scale_fill_manual(values = cmap_mes) + 
  scale_colour_manual(values = cmap_mes) + 
  theme_minimal() +
  theme(legend.position = "bottom",
        legend.title = element_blank(),
        title = element_blank()) +
  facet_grid(~variable, scales = "fixed") +
  theme(
    axis.text.x = element_blank(),
    strip.background = element_blank(),
    #strip.text.x = element_blank(),
    panel.spacing = unit(2, "lines")
  ) +
  coord_flip()