import pandas as pd
# put Genes ID to proper gene names in both files
# Load the merged gene list file
gene_list_file = 'data/Czerniak/GeneListID_Entrez/MainGeneList_ID.tsv'
df_gene_list = pd.read_csv(gene_list_file, sep='\t')

# Load the two CSV files with gene names
first_gene_file = 'data/Czerniak/CzerniakPrepared/FirstGeneName.csv'
df_first_gene = pd.read_csv(first_gene_file, sep = ';')

without_multiple_file = 'data/Czerniak/CzerniakPrepared/WithoutMultipleGeneNames.csv'
df_without_multiple = pd.read_csv(without_multiple_file, sep =';')

# Create a dictionary to map gene symbols to gene IDs
gene_dict = dict(zip(df_gene_list['Gene Symbol'], df_gene_list['Gene ID']))

# Update the gene IDs in the first CSV file
df_first_gene['Gene ID'] = df_first_gene['Gene Symbol'].map(gene_dict)

# Update the gene IDs in the second CSV file
df_without_multiple['Gene ID'] = df_without_multiple['Gene Symbol'].map(gene_dict)

# Save the updated CSV files
df_first_gene.to_csv('data/Czerniak/CzerniakPrepared_withID/FirstGeneName_ID.csv',sep = ';' , index=False)
df_without_multiple.to_csv('data/Czerniak/CzerniakPrepared_withID/WithoutMultipleGeneNames_ID.csv',sep = ';', index=False)