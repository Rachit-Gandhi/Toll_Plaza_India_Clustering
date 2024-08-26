import pandas as pd

df_2021 = pd.read_csv(r'tolls-with-metadata.csv')
df_2022 = pd.read_csv(r'tolls-with-metadata copy.csv')

def merge_toll_plaza_data(df_2021, df_2022):
    # Identify the key column
    key_column = 'id'  # Replace with your actual key column name

    # Identify columns present in both dataframes
    common_columns = list(set(df_2021.columns) & set(df_2022.columns))
    
    # Ensure the key column is included
    if key_column not in common_columns:
        common_columns.append(key_column)

    # Merge dataframes
    merged_df = pd.merge(df_2022, df_2021[common_columns], 
                         on=key_column, how='left', suffixes=('', '_2021'))

    # Update NaN values in df_2022 with data from df_2021
    for col in common_columns:
        if col != key_column:
            merged_df[col].fillna(merged_df[f'{col}_2021'], inplace=True)
            merged_df.drop(f'{col}_2021', axis=1, inplace=True)

    return merged_df

# Assume df_2021 and df_2022 are already loaded
final_df = merge_toll_plaza_data(df_2021, df_2022)
final_df.to_csv('final_toll.csv')

# final_df now contains all 2022 data, with NaN values filled from 2021 data where possible