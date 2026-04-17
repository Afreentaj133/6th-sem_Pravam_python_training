import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet

# -----------------------------
# Step 1: Create Sample Dataset
# -----------------------------
data = {
    "Student": ["Aisha", "Rahul", "Kiran", "Sneha", "Arjun"],
    "Math": [85, 78, 92, 70, 88],
    "Science": [90, 75, 88, 72, 91],
    "English": [80, 85, 84, 75, 89]
}

df = pd.DataFrame(data)

# -----------------------------
# Step 2: Add Calculations
# -----------------------------
df["Total"] = df[["Math", "Science", "English"]].sum(axis=1)
df["Average"] = df["Total"] / 3

# -----------------------------
# Step 3: Generate Graphs
# -----------------------------

# 1. Bar Chart (Average Marks)
plt.figure()
plt.bar(df["Student"], df["Average"])
plt.title("Average Marks of Students")
plt.xlabel("Students")
plt.ylabel("Average Marks")
plt.savefig("bar_chart.png")
plt.close()

# 2. Line Chart (Total Marks)
plt.figure()
plt.plot(df["Student"], df["Total"], marker='o')
plt.title("Total Marks Trend")
plt.xlabel("Students")
plt.ylabel("Total Marks")
plt.savefig("line_chart.png")
plt.close()

# 3. Pie Chart (Math Distribution)
plt.figure()
plt.pie(df["Math"], labels=df["Student"], autopct='%1.1f%%')
plt.title("Math Marks Distribution")
plt.savefig("pie_chart.png")
plt.close()

# -----------------------------
# Step 4: Export to Excel
# -----------------------------
excel_file = "student_report.xlsx"
df.to_excel(excel_file, index=False)

print("Excel file generated:", excel_file)

# -----------------------------
# Step 5: Generate PDF Report
# -----------------------------
pdf_file = "student_report.pdf"

doc = SimpleDocTemplate(pdf_file)
styles = getSampleStyleSheet()

elements = []

# Title
elements.append(Paragraph("Student Performance Report", styles["Title"]))
elements.append(Spacer(1, 20))

# Add table data as text
for i, row in df.iterrows():
    text = f"{row['Student']} - Total: {row['Total']}, Average: {row['Average']:.2f}"
    elements.append(Paragraph(text, styles["Normal"]))
    elements.append(Spacer(1, 10))

# Add Graphs
elements.append(Spacer(1, 20))
elements.append(Paragraph("Graphs:", styles["Heading2"]))

elements.append(Image("bar_chart.png", width=400, height=200))
elements.append(Image("line_chart.png", width=400, height=200))
elements.append(Image("pie_chart.png", width=400, height=200))

# Build PDF
doc.build(elements)

print("PDF report generated:", pdf_file)