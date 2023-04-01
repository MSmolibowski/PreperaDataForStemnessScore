import pandas as pd

# Load the first csv file
df1 = pd.read_csv('data/Czerniak/CzerniakPrepared_withID/FirstGeneName_ID.csv', sep=';')

# Filter out rows where Gene ID == NoGeneID
df1 = df1[df1['Gene ID'] != 'NoGeneID']

df1["gene_id"] = df1["Gene Symbol"] + "|" + df1["Gene ID"]
df1["gene_id"] = df1["gene_id"].apply(lambda x: str(x).replace(' ', ''))
df1.insert(0, 'gene_id', df1.pop('gene_id'))
df1 = df1.drop(['Probe Set ID', 'Gene Symbol', 'Gene ID'], axis=1)

df1.to_csv('data/CzerniakData/CzerniakPrepared_withID/FirstGeneName_Ready.tsv', sep='\t', index=False)

# Load the second csv file
df2 = pd.read_csv('data/Czerniak/CzerniakPrepared_withID/WithoutMultipleGeneNames_ID.csv', sep=';')

# Filter out rows where Gene ID == NoGeneID
df2 = df2[df2['Gene ID'] != 'NoGeneID']

df2["gene_id"] = df2["Gene Symbol"] + "|" + df2["Gene ID"]
df2["gene_id"] = df2["gene_id"].apply(lambda x: str(x).replace(' ', ''))
df2.insert(0, 'gene_id', df2.pop('gene_id'))
df2 = df2.drop(['Probe Set ID', 'Gene Symbol', 'Gene ID'], axis=1)

df2.to_csv('data/CzerniakData/CzerniakPrepared_withID/WithoutMultipleGeneNames_Ready.tsv', sep='\t', index=False)