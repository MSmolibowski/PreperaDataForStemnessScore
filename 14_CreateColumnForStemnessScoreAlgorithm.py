import pandas as pd
import os

path = 'data/dodatkoweDane/Esemble id/GeneNameToEntrezID/merged/Merged_EntrezID_GeneName_EsembleGeneList.tsv'

df = pd.read_csv(path, sep = '\t')
df['GeneID'] = df['GeneID'].apply(lambda x: str(x))
df['gene_id'] = df['GeneName'] + '|' + df['GeneID']

null_gene = df[df['GeneName'].isnull()]
print(null_gene)