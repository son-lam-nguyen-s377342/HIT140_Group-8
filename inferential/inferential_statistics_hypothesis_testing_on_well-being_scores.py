# import pandas and scipy
import scipy.stats as st
import pandas as pd

# read dataset from file into the Pandas DataFrame
df1 = pd.read_csv("../datasets/dataset1.csv")
df2 = pd.read_csv("../datasets/dataset2.csv")
df3 = pd.read_csv("../datasets/dataset3.csv")

# merge the datasets
df = pd.merge(pd.merge(df1, df2, on="ID"), df3, on="ID")

# calculate total screen time on weekends (S_we, C_we, G_we, T_we)
df["Total_screen_time_we"] = df[["S_we", "C_we", "G_we", "T_we"]].sum(axis=1)

# define high and low screen time
median_screen_time = df["Total_screen_time_we"].median()
high_screen_time = df[df["Total_screen_time_we"] > median_screen_time]
low_screen_time = df[df["Total_screen_time_we"] <= median_screen_time]

# list of all well-being indicators to do t-test
well_being_indicators = [
    "Relx",
    "Optm",
    "Usef",
    "Intp",
    "Engs",
    "Dealpr",
    "Thcklr",
    "Goodme",
    "Clsep",
    "Conf",
    "Mkmind",
    "Loved",
    "Intthg",
    "Cheer",
]

# perform the t-test for each well-being indicator
results = []

for indicator in well_being_indicators:
    # extract well-being scores for both groups
    high_scores = high_screen_time[indicator]
    low_scores = low_screen_time[indicator]

    # calculate statistics for both groups
    x_bar_high = st.tmean(high_scores)
    s_high = st.tstd(high_scores)
    n_high = len(high_scores)

    x_bar_low = st.tmean(low_scores)
    s_low = st.tstd(low_scores)
    n_low = len(low_scores)

    # perform the two-sample t-test
    t_stats, p_val = st.ttest_ind_from_stats(
        x_bar_high,
        s_high,
        n_high,
        x_bar_low,
        s_low,
        n_low,
        equal_var=False,
        alternative="greater",
    )

    # store results
    results.append(
        {
            "Well-being indicator": indicator,
            "t-statistic": t_stats,
            "p-value": p_val,
            "Conclusion": "We reject the null hypothesis"
            if p_val < 0.05
            else "We accept the null hypothesis",
        }
    )

results_df = pd.DataFrame(results)
print(results_df)
