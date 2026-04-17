import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("students.csv")

print("📊 Student Data:\n", df)

# Use Marks directly (no subject-wise data)
df["Total"] = df["Marks"]
df["Average"] = df["Marks"]

# Grade calculation
def grade(marks):
    if marks >= 90:
        return "A"
    elif marks >= 75:
        return "B"
    elif marks >= 60:
        return "C"
    else:
        return "D"

df["Grade"] = df["Marks"].apply(grade)

print("\nUpdated Data:\n", df)

# 🔹 Class Statistics using NumPy
mean_marks = np.mean(df["Average"])
max_marks = np.max(df["Average"])
min_marks = np.min(df["Average"])

print("\n📊 Class Stats:")
print("Mean:", mean_marks)
print("Highest:", max_marks)
print("Lowest:", min_marks)

# ------------------ 📊 VISUALIZATION ------------------

# 1️⃣ Bar Graph - Total Marks
plt.figure()
plt.bar(df["Name"], df["Total"])
plt.title("Total Marks of Students")
plt.xlabel("Students")
plt.ylabel("Total Marks")
plt.show()

# 2️⃣ Pie Chart - Grade Distribution
plt.figure()
grade_counts = df["Grade"].value_counts()
plt.pie(grade_counts, labels=grade_counts.index, autopct='%1.1f%%')
plt.title("Grade Distribution")
plt.show()

# 3️⃣ Line Graph - Average Marks
plt.figure()
plt.plot(df["Name"], df["Average"], marker='o')
plt.title("Average Marks Trend")
plt.xlabel("Students")
plt.ylabel("Average Marks")
plt.show()

# 4️⃣ Histogram - Average Distribution
plt.figure()
plt.hist(df["Average"])
plt.title("Distribution of Average Marks")
plt.xlabel("Average")
plt.ylabel("Frequency")
plt.show()
