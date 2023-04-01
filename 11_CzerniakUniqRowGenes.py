import pandas as pd

df = pd.read_csv('data/Czerniak/CzerniakReadyForStemnesScore/temp/WithoutMultipleGeneNames_Ready.tsv', sep='\t')

df = df.drop_duplicates(subset=['gene_id'])
# Replace ',' with '.'
df = df.replace(',', '.', regex=True)

# drop rows without values in the gene_id column
df.dropna(subset=['gene_id'], inplace=True)

# Sort the DataFrame based on the 'gene_id' column in ascending order
df = df.sort_values(by=['gene_id'], ascending=True)
print(df.head())
df.to_csv('data/CzerniakData/CzerniakReadyForStemnesScore/WithoutMultipleGeneNames_Ready_Uniq.tsv', sep = '\t', index = False)

