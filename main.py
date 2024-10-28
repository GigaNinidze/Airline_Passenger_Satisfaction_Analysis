# Import necessary libraries for analysis and visualization
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load the dataset
data = pd.read_csv('test.csv')  # Relative path

# Drop the unnecessary 'Unnamed: 0' column
data = data.drop(columns=['Unnamed: 0'])

# Fill missing values in 'Arrival Delay in Minutes' with the median
data['Arrival Delay in Minutes'] = data['Arrival Delay in Minutes'].fillna(data['Arrival Delay in Minutes'].median())

# Set the plot style
sns.set(style='whitegrid')

# 1. Data Overview and Cleaning
print("=== Data Overview ===")
print(f"Dataset has {data.shape[0]} rows and {data.shape[1]} columns.")
print("=== Sample of Data ===")
print(data.head())

# Check for any remaining missing values
print("\n=== Missing Values in Each Column ===")
print(data.isnull().sum())

# 2. Create satisfaction_numeric column (Convert satisfaction to numeric)
data['satisfaction_numeric'] = data['satisfaction'].apply(lambda x: 1 if x == 'satisfied' else 0)

# 3. Display Min, Max, and Mean Values for Each Numeric Column (Excluding 'id')
print("\n=== Statistical Summary for Each Numeric Column ===")
# Exclude 'id' from the statistical summary
numeric_cols = data.select_dtypes(include=['float64', 'int64']).columns.difference(['id'])
for col in numeric_cols:
    min_value = data[col].min()
    max_value = data[col].max()
    mean_value = data[col].mean()
    print(f"{col}: Min = {min_value}, Max = {max_value}, Mean = {mean_value:.2f}")

# 4. Correlation Analysis (Drop non-numeric columns and plot correlation heatmap)
# Select only numeric columns excluding 'id'
numeric_data = data.loc[:, numeric_cols]  # Now excludes 'id' column

# Generate correlation matrix
corr_matrix = numeric_data.corr()

# Create a mask for the lower triangle to keep the heatmap cleaner
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))

# Set up the matplotlib figure
plt.figure(figsize=(12, 8))

# Draw the heatmap with the mask
sns.heatmap(corr_matrix, mask=mask, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5,
            annot_kws={"size": 10}, cbar_kws={"shrink": 0.8, "label": "Correlation Coefficient"})
plt.title('Correlation Matrix of Numeric Variables', fontsize=16)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()  # Adjust layout to fit labels

# Save the heatmap
plt.savefig('correlation_heatmap.png')
plt.close()  # Close the figure after saving

# 5. Grouping Data by Satisfaction (to explore averages by satisfaction group)
# Select only numeric columns for grouping
numeric_cols_only = data.select_dtypes(include=['float64', 'int64']).columns
grouped_satisfaction = data.groupby('satisfaction')[numeric_cols_only].mean()

print("\n=== Average Values Grouped by Satisfaction ===")
print(grouped_satisfaction)

# 6. Visualize Key Relationships with Satisfaction

# 6a. Visualize Flight Distance by Satisfaction (Bar Plot)
plt.figure(figsize=(8, 6))
sns.barplot(x='satisfaction', y='Flight Distance', data=data, palette='coolwarm')
plt.title('Average Flight Distance by Satisfaction')
plt.xlabel('Satisfaction')
plt.ylabel('Average Flight Distance')

# Save the flight distance bar plot
plt.savefig('flight_distance_by_satisfaction.png')
plt.close()

# 6b. Visualize Arrival Delay by Satisfaction (Bar Plot)
plt.figure(figsize=(8, 6))
sns.barplot(x='satisfaction', y='Arrival Delay in Minutes', data=data, palette='coolwarm')
plt.title('Average Arrival Delay by Satisfaction')
plt.xlabel('Satisfaction')
plt.ylabel('Average Arrival Delay (Minutes)')

# Save the arrival delay bar plot
plt.savefig('arrival_delay_by_satisfaction.png')
plt.close()

# 7. Feature Engineering: Categorize Age into Groups
# Create age categories
bins = [0, 18, 35, 60, 100]
labels = ['Young', 'Adult', 'Middle-Aged', 'Senior']
data['Age Group'] = pd.cut(data['Age'], bins=bins, labels=labels)

# Visualize Satisfaction by Age Group (Count Plot)
plt.figure(figsize=(8, 6))
sns.countplot(x='Age Group', hue='satisfaction', data=data, palette='coolwarm')
plt.title('Satisfaction by Age Group')
plt.xlabel('Age Group')
plt.ylabel('Count')

# Update x-tick labels to show age ranges
plt.xticks(ticks=[0, 1, 2, 3], labels=['Young (0-18)', 'Adult (18-35)', 'Middle-Aged (35-60)', 'Senior (60-100)'])

# Save the age group satisfaction plot
plt.savefig('satisfaction_by_age_group.png')
plt.close()

# 8. Final Summary Table: Grouped by Age Group and Satisfaction
print("\n=== Data Grouped by Age Group and Satisfaction ===")
print(data.groupby(['Age Group', 'satisfaction']).size())