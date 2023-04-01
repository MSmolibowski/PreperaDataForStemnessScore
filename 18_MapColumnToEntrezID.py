import pandas as pd
import os

path_gene_id = 'data/dodatkoweDane/Esemble id/GeneNameToEntrezID/merged/Merged_EntrezID_GeneName_EsembleGeneList.tsv'
gene_id = pd.read_csv(path_gene_id, sep = '\t')
gene_dict = dict(zip(gene_id['tracking_id'], gene_id['gene_id']))

path = 'data/dodatkoweDane/FilesDifferentExtensions/'
file_name = 'Czerniak_Ektoderma.tsv'

df = pd.read_csv(path+file_name, sep = '\t')
df['tracking_id'] = df['tracking_id'].str.split('.').str[0]

df['gene_id'] = df['tracking_id'].map(gene_dict)

# drop all rows with 'NoGeneID|NoGeneID' in gene_id column
df = df[df['gene_id'] != 'NoGeneID|NoGeneID']

# drop all rows with empty cells in gene_id column
df = df.dropna(subset=['gene_id'])

# get a list of column names
cols = list(df.columns)

# move the gene_id column to the beginning of the list
cols.insert(0, cols.pop(cols.index('gene_id')))

# use the updated list of column names to re-order the DataFrame columns
df = df.loc[:, cols]

# drop the tracking_id column from the DataFrame
df = df.drop('tracking_id', axis=1)

# Sort the DataFrame based on the 'gene_id' column in ascending order
df = df.sort_values(by=['gene_id'], ascending=True)

# select only the columns with numeric data types
numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns

# round the values in these columns to 6 decimal places
df[numeric_cols] = df[numeric_cols].round(6)

save_file_path = 'data/dodatkoweDane/gene_idMapedToEsemble/'
save_file_name = file_name+'_gene_id'

df.to_csv(save_file_path+save_file_name, sep = '\t', index= False)

