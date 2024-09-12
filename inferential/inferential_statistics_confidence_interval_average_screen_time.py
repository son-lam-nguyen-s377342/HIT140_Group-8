import scipy.stats as st
import pandas as pd
import math

# Load datasets
df2 = pd.read_csv("../datasets/dataset2.csv")

# Extract activities for the analysis
screen_time_activities = [
    "C_we",
    "C_wk",
    "G_we",
    "G_wk",
    "S_we",
    "S_wk",
    "T_we",
    "T_wk",
]

# Store results in a list
results = []

# Loop through each activity and compute the statistics
for activity in screen_time_activities:
    data = df2[activity]

    # Compute the mean, standard deviation, sample size,
    #  and standard error
    mean_val = data.mean()
    std_dev = data.std()
    n = len(data)
    std_err = std_dev / math.sqrt(n)

    # Define the confidence level (99%)
    # and compute the t-critical value
    conf_level = 0.99
    alpha = 1 - conf_level
    t_crit = st.t.ppf(1 - alpha / 2, df=n - 1)

    # Compute the confidence interval
    ci_lower = mean_val - t_crit * std_err
    ci_upper = mean_val + t_crit * std_err

    # Append the result as a list
    results.append(
        [
            activity,
            f"{mean_val:.2f}",
            f"{std_dev:.2f}",
            n,
            f"{std_err:.2f}",
            f"{t_crit:.2f}",
            f"[{ci_lower:.2f}, {ci_upper:.2f}]",
        ]
    )

# Convert the list into a DataFrame
results_df = pd.DataFrame(
    results,
    columns=[
        "Activity",
        "Mean",
        "Std Dev",
        "Sample Size",
        "Std Error",
        "t-Critical",
        "Confidence Interval",
    ],
)

# Print the resulting DataFrame
print(results_df)
