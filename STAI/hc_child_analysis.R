library(tidyverse)
library(ggpubr)
library(rstatix)
library(gt)
library(parameters)
library(gtsummary)
outDir = "/users/simon/Documents/GitHub/Msc_Thesis/Figures/"


df = read.csv("stai_with_app.csv")
head(df,3)

df <- df %>%
    gather(key = "time", value = "score", Before_Mock, After_Mock) %>%
    convert_as_factor(pers_id, time)
head(df, 3)

#GLM model
model = lm(score ~ age + Trait + time + gender + app, data = df)
#Sum of squares summary
summary.aov(model)
summary(model)


#Same analysis
res.aov <- df %>% 
    anova_test(score ~ age+Trait + time+app*gender)
get_anova_table(res.aov)



library(gtsummary)
t1 <- tbl_regression(model)%>%
    bold_p(t = 0.05)%>%
    modify_column_unhide(column = std.error)

t1
# Use function from gt package to save table, after converting to 
# gt object using as_gt()
gt::gtsave(as_gt(t1), filename = "test.png")



#RMS MOVEMENT AND SCAN TIME
#missing for app_004,9,18,20
df = read.csv("full_child_df_rms.csv")

#RMS
rms_model = lm(mpr_age ~ age+gender+app+Trait+Before_Mock, data = df)
summary(rms_model)

#Prep_time
prep_model = lm(prep_time_min ~  age+gender+app+Trait+Before_Mock, data = df)
summary(prep_model)

#Scan_time
scan_model = lm(scan_time_min ~  age+gender+app+Trait+Before_Mock, data = df)
summary(scan_model)


#Create Tables
#RMS
(rms_table <- as_gt(tbl_regression(rms_model)%>%
    bold_p(t = 0.05)%>%
    modify_column_unhide(column = std.error)))
#Prep
(prep_table <- as_gt(tbl_regression(prep_model)%>%
    bold_p(t = 0.05)%>%
    modify_column_unhide(column = std.error)))
#Scan
(scan_table <- as_gt(tbl_regression(scan_model)%>%
    bold_p(t = 0.05)%>%
    modify_column_unhide(column = std.error)))

#Save Tables
gt::gtsave(rms_table, filename = paste(outDir,"reg_rms_coef.png"))
gt::gtsave(prep_table, filename = paste(outDir,"reg_prep_coef.png"))
gt::gtsave(scan_table, filename = paste(outDir,"reg_scan_coef.png"))






