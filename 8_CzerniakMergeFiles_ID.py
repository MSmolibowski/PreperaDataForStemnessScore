import os
import pandas as pd

# Set the input and output folder paths
output_folder_path = 'data/Czerniak/GeneListID_Entrez/ID_GeneLists'

# Create an empty list to store the dataframes
dfs = []

# Loop through each file in the output folder and load it into a dataframe
for filename in os.listdir(output_folder_path):
    if filename.endswith('.tsv'):
        df = pd.read_csv(os.path.join(output_folder_path, filename))
        dfs.append(df)

# Concatenate all the dataframes into a single dataframe
merged_df = pd.concat(dfs, ignore_index=True)

# Save as one
merged_df.to_csv('data/Czerniak/GeneListID_Entrez/MainGeneList_ID.tsv', sep = '\t', index = False)