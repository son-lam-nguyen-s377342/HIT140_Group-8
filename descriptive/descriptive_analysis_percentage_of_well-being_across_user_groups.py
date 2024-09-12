import matplotlib.pyplot as plt
import pandas as pd

# Dataset 2 (screen time), and Dataset 3 (well-being indicators)
dataset3 = pd.read_csv("../datasets/dataset3.csv")
dataset2 = pd.read_csv("../datasets/dataset2.csv")

# Merge Dataset 2 (screen time) with Dataset 3 (well-being indicators) on participant ID
# The "ID" column serves as the unique identifier for participants in both datasets
merged_data = pd.merge(dataset2, dataset3, on="ID")

# Identify columns that contain well-being indicators
# The first column is the "ID", and the rest of the columns represent well-being scores
well_being_columns = dataset3.columns[1:]

# Low well-being: Participants with any score of 1 or 2 in any well-being indicator
# High well-being: Participants with scores of 4 or 5 in ALL well-being indicators
low_well_being = (
    merged_data[well_being_columns].apply(lambda x: (x == 1) | (x == 2)).any(axis=1)
)
high_well_being = (
    merged_data[well_being_columns].apply(lambda x: (x == 4) | (x == 5)).all(axis=1)
)

# Create a new "WellBeing" column in the merged data
# Default classification is "Medium" well-being
merged_data["WellBeing"] = "Medium"

# Update the "WellBeing" column based on the conditions for low and high well-being
# Participants with low well-being are labeled as "Low"
merged_data.loc[low_well_being, "WellBeing"] = "Low"

# Participants with high well-being are labeled as "High"
merged_data.loc[high_well_being, "WellBeing"] = "High"


# Define a function to classify users based on their primary screen time activity
def classify_user(row):
    """
    Classifies a user into one of four categories based on their primary screen time activity.
    - "Computer User" if their computer time is greater than all other activities combined.
    - "Gamer" if their gaming time is the highest.
    - "Smartphone User" if their smartphone time is the highest.
    - "TV Watcher" for all other users (i.e., if TV watching time is highest).

    Args:
        row: A row of the DataFrame representing a participant's screen time for various activities.

    Returns:
        A string indicating the user's primary activity.
    """
    if (
        row["C_wk"] + row["C_we"]
        > row[["G_wk", "G_we", "S_wk", "S_we", "T_wk", "T_we"]].sum()
    ):
        return "Computer User"
    elif (
        row["G_wk"] + row["G_we"]
        > row[["C_wk", "C_we", "S_wk", "S_we", "T_wk", "T_we"]].sum()
    ):
        return "Gamer"
    elif (
        row["S_wk"] + row["S_we"]
        > row[["C_wk", "C_we", "G_wk", "G_we", "T_wk", "T_we"]].sum()
    ):
        return "Smartphone User"
    else:
        return "TV Watcher"


# Apply the classify_user function to each row in the dataset
# Add a new column "UserGroup" indicating the participant's primary screen time activity
merged_data["UserGroup"] = merged_data.apply(classify_user, axis=1)

# Group the data by "UserGroup" (primary activity) and "WellBeing" (low, medium, high)
# Count the number of participants in each combination of UserGroup and WellBeing
well_being_counts = (
    merged_data.groupby(["UserGroup", "WellBeing"]).size().unstack().fillna(0)
)

# Normalize the counts to get the proportion of participants in each well-being category per UserGroup
# Multiply by 100 to convert proportions to percentages
well_being_percentage = (
    well_being_counts.div(well_being_counts.sum(axis=1), axis=0) * 100
)

# Plot the results using a stacked bar chart
ax = well_being_percentage.plot(
    kind="bar", stacked=True, figsize=(10, 6), colormap="Set3"
)

# Set plot title and labels
plt.title(
    "Percentage of Low, Medium, and High Well-being Across User Groups"
)  # Title of the plot
plt.xlabel("User Group")  # Label for the x-axis
plt.ylabel("Percentage")  # Label for the y-axis (reflecting percentage)

# Add percentage annotations on each bar
for p in ax.patches:
    width = p.get_width()
    height = p.get_height()
    x, y = p.get_xy()
    if (
        height > 0
    ):  # Only annotate if the height of the bar (percentage) is greater than zero
        ax.annotate(
            f"{height:.1f}%", (x + width / 2, y + height / 2), ha="center", va="center"
        )

plt.tight_layout()  # Automatically adjust the layout for readability

# Save the plot to a PNG file with high resolution (300 DPI)
plt.savefig("./Percentage_of_Low_and_High_Well-being_Across_User_Groups.png", dpi=300)

# Show the plot on the screen
plt.show()
