library(mclust)

clusters <- read.csv("output.csv", sep=",", header=T, row.names=1)

clusters2 <- read.csv("output_test.csv", sep=",", header=T, row.names = 1)

clusters$dom <- row.names(clusters)

clusters2$dom <- row.names(clusters2)

names(clusters) <- c("cluster_predict", "dom")
names(clusters2) <- c("cluster_gt", "dom")

cm <- merge(clusters, clusters2, by="dom")

adjustedRandIndex(cm$cluster_predict, cm$cluster_gt)
