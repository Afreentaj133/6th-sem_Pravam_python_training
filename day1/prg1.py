import pandas as pd

# Read CSV
df = pd.read_csv("students.csv")

print("Original Data:\n", df)

# ✅ Adding a new column (Pass/Fail)
df["Result"] = df["Marks"].apply(lambda x: "Pass" if x >= 80 else "Fail")

# ✅ Adding another column (Grade)
def grade(marks):
    if marks >= 90:
        return "A"
    elif marks >= 80:
        return "B"
    else:
        return "C"

df["Grade"] = df["Marks"].apply(grade)

print("\nAfter Adding Columns:\n", df)

# ❌ Deleting a column
df = df.drop("Age", axis=1)

print("\nAfter Deleting 'Age' Column:\n", df)