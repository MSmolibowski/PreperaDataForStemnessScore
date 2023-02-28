import pandas as pd
import math

# Load data from CSV file into pandas DataFrame
df = pd.read_csv('data/Czerniak/CzerniakPrepared/FirstGeneName.csv', sep=';')

# Determine the number of gene lists needed
num_lists = math.ceil(len(df) / 2000)

# Split gene list into smaller lists of 2000 genes each
gene_lists = [df['Gene Symbol'][i:i+2000].tolist() for i in range(0, len(df['Gene Symbol']), 2000)]

# Save each gene list to a TSV file with a numbered filename
for i, gene_list in enumerate(gene_lists):
    filename = 'GeneList_{}.tsv'.format(i+1)
    df = pd.DataFrame({'Gene Symbol': gene_list})
    df.to_csv(f'data/Czerniak/GeneLists/{filename}', sep='\t', index=False)