library(tidyverse)
library(ggpubr)
library(rstatix)

df = read.csv("full_child_df.csv")
head(df,3)


df <- df %>%
    gather(key = "time", value = "score", Before_Mock, After_Mock) %>%
    convert_as_factor(pers_id, time)
head(df, 3)

#GLM model
model = lm(score ~ age + app + Trait + time  + gender, data = df)
#Sum of squares summary
summary.aov(model)
summary(model)


#Same analysis
res.aov <- df %>% 
    anova_test(score ~ age+Trait + time*app*gender)
get_anova_table(res.aov)



#Simple effects
df %>%
    group_by(gender) %>%
    anova_test(score ~ age + Trait + app*time)

df %>%
    group_by(time) %>%
    anova_test(score ~ age + Trait + app*gender)




df = read.csv("full_child_df_rms.csv")

model = lm(mpr.age ~ app+age+Trait+gender+Before_Mock, data = df)
summary(model)

library(gtsummary)
t1 <- tbl_regression(model)

# Use function from gt package to save table, after converting to 
# gt object using as_gt()
gt::gtsave(as_gt(t1), filename = "test.png")
