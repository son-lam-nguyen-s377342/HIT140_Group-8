import pandas as pd
import matplotlib.pyplot as plt

# Load the datasets
dataset1 = pd.read_csv("../datasets/dataset1.csv")
dataset2 = pd.read_csv("../datasets/dataset2.csv")

# Merge datasets on the 'ID' column
merged_data = pd.merge(dataset1, dataset2, on="ID")

# List of screen time columns for analysis
screen_time_columns = ["C_we", "C_wk", "G_we", "G_wk", "S_we", "S_wk", "T_we", "T_wk"]

# Calculate mean for each activity
mean_screen_time = merged_data[screen_time_columns].mean()

# Display the calculated statistics
print("Mean Screen Time for Each Activity:")
print(mean_screen_time)

# Calculate mean by gender
mean_screen_time_by_gender = merged_data.groupby("gender")[screen_time_columns].mean()

# Display the results for mean by gender
print("Mean Screen Time by Gender:")
print(mean_screen_time_by_gender)

# List of screen time columns for weekdays and weekends
weekend_columns = ["C_we", "G_we", "S_we", "T_we"]  # Weekend screen time columns
weekday_columns = ["C_wk", "G_wk", "S_wk", "T_wk"]  # Weekday screen time columns


# Extract only the screen time columns for plotting
screen_time_columns = ["C_we", "C_wk", "G_we", "G_wk", "S_we", "S_wk", "T_we", "T_wk"]
mean_screen_time = mean_screen_time_by_gender[screen_time_columns]

# Rename the columns for better readability
mean_screen_time.columns = [
    "Computer (Weekend)",
    "Computer (Weekday)",
    "Video Game (Weekend)",
    "Video Game (Weekday)",
    "Smartphone (Weekend)",
    "Smartphone (Weekday)",
    "TV (Weekend)",
    "TV (Weekday)",
]

# Transpose for easier plotting
mean_screen_time_transposed = mean_screen_time.T

# Plot the average screen time for both males and females as a grouped bar chart
mean_screen_time_transposed.plot(kind="bar", figsize=(14, 8), color=["blue", "orange"])
plt.title(
    "Average Screen Time for Male and Female Respondents Across Different Activities"
)
plt.xlabel("Activity")
plt.ylabel("Average Hours")
plt.xticks(rotation=45)
plt.legend(["Female", "Male"], title="Gender")
plt.tight_layout()
plt.savefig("./mean_screen_time_by_gender.png", dpi=300)
plt.show()
