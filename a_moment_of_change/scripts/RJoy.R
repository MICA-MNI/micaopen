library(ggridges)
library(reshape2)
library(RColorBrewer)
library(ggplot2)

df <- read.csv('C:/Users/casey/Downloads/surfT.csv',header=TRUE)
df2 <- melt(df, id= c("Surf"))

df2$Surf <- as.numeric(df2$Surf)
df2$value <- as.numeric(df2$value)

p1 <- ggplot(df2, aes(x = value, y = reorder(variable, -sort(as.numeric(variable))), fill = ..x..)) +
  geom_density_ridges_gradient(scale = 3,gradient_lwd = 1.)  +
  scale_fill_gradientn(colors = rev(brewer.pal(10,"RdBu")),guide = "colourbar", limits = c(-10, 10)) + 
  scale_y_discrete(expand = c(0.01, 0)) +   # will generally have to set the `expand` option
  scale_x_continuous(expand = c(0, 0))  +
  theme_ridges() +
  labs(x = "T-Statistic", y = "Depth") +
  theme(legend.position = "none",
        legend.title = element_blank())

pdf(file = "C:/Users/casey/OneDrive/montreal/3_NSPN/Plots/Surface_T.pdf", height = 4, width = 2.5)
p1
dev.off()