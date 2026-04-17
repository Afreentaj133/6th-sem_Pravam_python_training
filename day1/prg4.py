import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

# Fix for graph display
matplotlib.use('TkAgg')

# PDF
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet

# ------------------ LOAD DATA ------------------
df = pd.read_csv("students.csv")

print("\n========== 🎓 STUDENT PERFORMANCE REPORT ==========\n")
print("📊 Student Data:\n", df)

# ------------------ PROCESSING ------------------

# Grade function
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

# Stats
mean_marks = np.mean(df["Marks"])
max_marks = np.max(df["Marks"])
min_marks = np.min(df["Marks"])

topper = df.loc[df["Marks"].idxmax()]

# ------------------ PRINT REPORT ------------------

print("\n📊 Class Statistics:")
print(f"Average Marks : {mean_marks:.2f}")
print(f"Highest Marks : {max_marks}")
print(f"Lowest Marks  : {min_marks}")

print("\n🏆 Topper:")
print(f"{topper['Name']} with {topper['Marks']} marks")

print("\n📌 Grade Distribution:")
print(df["Grade"].value_counts())

# ------------------ EXCEL REPORT ------------------

excel_file = "Student_Report.xlsx"

with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
    df.to_excel(writer, index=False, sheet_name="Report")

print("✅ Excel file created successfully!")
# ------------------ PDF REPORT ------------------

pdf_file = "Student_Report.pdf"
doc = SimpleDocTemplate(pdf_file)

styles = getSampleStyleSheet()
content = []

# Title
content.append(Paragraph("Student Performance Report", styles["Title"]))
content.append(Spacer(1, 10))

# Stats
content.append(Paragraph(f"Average Marks: {mean_marks:.2f}", styles["Normal"]))
content.append(Paragraph(f"Highest Marks: {max_marks}", styles["Normal"]))
content.append(Paragraph(f"Lowest Marks: {min_marks}", styles["Normal"]))
content.append(Spacer(1, 10))

# Table Data
table_data = [["Name", "Marks", "Grade"]]

for i, row in df.iterrows():
    table_data.append([row["Name"], row["Marks"], row["Grade"]])

table = Table(table_data)
content.append(table)

# Build PDF
doc.build(content)
print("✅ PDF report generated:", pdf_file)

# ------------------ GRAPHS ------------------

# 1️⃣ Bar Graph
plt.figure()
plt.bar(df["Name"], df["Marks"])
plt.title("Student Marks")
plt.xlabel("Students")
plt.ylabel("Marks")
plt.show()

# 2️⃣ Pie Chart
plt.figure()
grade_counts = df["Grade"].value_counts()
plt.pie(grade_counts, labels=grade_counts.index, autopct='%1.1f%%')
plt.title("Grade Distribution")
plt.show()

# 3️⃣ Histogram
plt.figure()
plt.hist(df["Marks"])
plt.title("Marks Distribution")
plt.xlabel("Marks")
plt.ylabel("Frequency")
plt.show()