import pandas as pd

# Sample data
data = {
    ('Main Header 1', 'Subheader 1-1'): [1, 2, 3],
    ('Main Header 1', 'Subheader 1-2'): [4, 5, 6],
    ('Main Header 2', 'Subheader 2-1'): [7, 8, 9],
    ('Main Header 2', 'Subheader 2-2'): [10, 11, 12],
}

# Creating the DataFrame with a MultiIndex for columns
df = pd.DataFrame(data)

# Exporting to Excel
df.to_excel('output.xlsx', index=True)
