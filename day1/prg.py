import pandas as pd

# Read CSV file
df = pd.read_csv("students.csv")

# Show full data
print("Full Data:\n", df)

# Show first 5 rows
print("\nFirst 5 rows:\n", df.head())

# Show basic info
print("\nInfo:\n")
print(df.info())

# Show statistics
print("\nSummary:\n", df.describe())

# Filter students with marks > 85
high_scorers = df[df["Marks"] > 85]
print("\nHigh Scorers:\n", high_scorers)