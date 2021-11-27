library(gtsummary)
out_dir = "/Users/simon/Documents/GitHub/Msc_Thesis/Figures/"

df = read.csv("full_child_df_rms.csv")
df = head(df, -1)


df$app[df$app == 0] = "No App"
df$app[df$app == 1] = "With App"

#App table with contin var
t1 = df %>%
    select(Trait,Before_Mock, After_Mock, app) %>%
    tbl_summary(
        by = app,
        type = everything() ~ "continuous2",
        statistic = all_continuous() ~ c("{N_nonmiss}",
                                         "{median} ({p25}, {p75})", 
                                         "{min}, {max}"),
        missing = "no"
    )

#Gender table with contin var
t2 = df %>%
    select(Trait,Before_Mock, After_Mock, gender) %>%
    tbl_summary(
        by = gender,
        type = everything() ~ "continuous2",
        statistic = all_continuous() ~ c("{N_nonmiss}",
                                         "{median} ({p25}, {p75})", 
                                         "{min}, {max}"),
        missing = "no"
    )

#Save tables
gt::gtsave(as_gt(t1), filename = paste(out_dir,"app_table.png",sep =""))
gt::gtsave(as_gt(t2), filename = paste(out_dir,"gender_table.png",sep =""))
