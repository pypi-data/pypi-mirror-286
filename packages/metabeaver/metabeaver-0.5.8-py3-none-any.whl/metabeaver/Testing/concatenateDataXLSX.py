import pandas as pd
import os

# Define the directory where the files are located
directory = r'C:\Users\lukep\Downloads\OneDrive_2023-04-25 _ Pall Lab order detail _ 2022 2023\Ecomm Files'

# Create an empty list to hold the dataframes
dfs = []

# Loop through all files in the directory and read them into a list of dataframes
for filename in os.listdir(directory):
    if filename.startswith('Ecomm Order contact information we'):
        print(filename)
        filepath = os.path.join(directory, filename)
        try:
            df = pd.read_excel(filepath, sheet_name='Ecomm Orders')
        except ValueError as ve:
            try:
                df = pd.read_excel(filepath, sheet_name='Ecomm Orders List')
            except ValueError as ve:
                try:
                    df = pd.read_excel(filepath, sheet_name='Order Details')
                except ValueError as ve:
                    try:
                        df = pd.read_excel(filepath, sheet_name='Ecomm Order Details')
                    except ValueError as ve:
                        df = pd.read_excel(filepath, sheet_name='Sheet1')
        dfs.append(df)

# Concatenate all dataframes into one
df_combined = pd.concat(dfs)

# Drop any rows that are full duplicates
df_combined = df_combined.drop_duplicates()

# Write the combined dataframe to Excel
df_combined.to_excel('combined_data.xlsx')

# Create a pivot table on the 'Sold-to party' column
pivot_table = df_combined.pivot_table(values='Net value', index='Sold-to party', aggfunc=['sum', 'count', 'mean'])

# Rename the columns to match the requested output
pivot_table.columns = ['Net value', 'Total orders', 'Average order value']

# Write the pivot table to Excel
pivot_table.to_excel('pivot_table.xlsx')
