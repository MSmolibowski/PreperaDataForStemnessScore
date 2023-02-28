import pandas as pd

df = pd.read_csv('data/Czerniak/Czerniak_merged.csv', sep = ';')

df = df[df['Gene Symbol'] != '---']                 #exclude rows with '---'
df1 = df[~df['Gene Symbol'].str.contains("//")]     #exclude rows with '//' in them
df1_gene_symbol = df1['Gene Symbol'].tolist()
df1_gene_symbol = [gene.strip() for gene in df1_gene_symbol]

df2 = df
df2['Gene Symbol'] = df2['Gene Symbol'].apply(lambda x: x.split('//'))
df2['Gene Symbol'] = df2['Gene Symbol'].apply(lambda x: x[0])

df1.to_csv('data/Czerniak/CzerniakPrepared/WithoutMultipleGeneNames.csv', sep=';', index = False)
df2.to_csv('data/Czerniak/CzerniakPrepared/FirstGeneName.csv', sep=';', index = False)
