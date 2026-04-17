import pandas as pd

# Basic CSV reading
df = pd.read_csv('data.csv')

# With options
df = pd.read_csv('data.csv', delimiter=',', header=0, encoding='utf-8')
import pandas as pd

# Read specific sheet
df = pd.read_excel('data.xlsx', sheet_name='Sheet1')

# Read multiple sheets
df_dict = pd.read_excel('data.xlsx', sheet_name=None)  # Returns all sheets
import pandas as pd

df = pd.read_json('data.json')
# Text file
df = pd.read_csv('data.txt', delimiter='\t')  # Tab-separated

# SQL database
df = pd.read_sql('SELECT * FROM table_name', connection)

# Parquet
df = pd.read_parquet('data.parquet')

# HTML
df = pd.read_html('file.html')  # Returns list of tables