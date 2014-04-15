john_mapping <- read.csv("mapping.csv", sep=",", header=T)

jake_mapping <- read.csv("ResultsV1Small.csv", sep=",", header=T)

names(jake_mapping) <- c("url", "URL")

merged_mapping = merge(jake_mapping, john_mapping, by="url")

write.csv(merged_mapping, file="merged_output.csv")
