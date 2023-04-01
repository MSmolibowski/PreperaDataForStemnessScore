import pandas as pd
import math

# Load data from CSV file into pandas DataFrame
df = pd.read_csv('data/dodatkoweDane/Esemble id/esemble_id.csv', sep=';')

df['tracking_id'] = df['tracking_id'].str.split('.').str[0]

# Determine the number of gene lists needed
num_lists = math.ceil(len(df) / 2000)

# Split gene list into smaller lists of 2000 genes each
gene_lists = [df['tracking_id'][i:i+2000].tolist() for i in range(0, len(df['tracking_id']), 2000)]

# Save each gene list to a TSV file with a numbered filename
for i, gene_list in enumerate(gene_lists):
    filename = 'EsembleGeneList_{}.tsv'.format(i+1)
    df = pd.DataFrame({'tracking_id': gene_list})
    df.to_csv(f'data/dodatkoweDane/Esemble id/EsembleShorterLists/{filename}', sep='\t', index=False)