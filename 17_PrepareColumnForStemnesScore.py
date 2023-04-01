import pandas as pd

path = 'data/dodatkoweDane/Esemble id/GeneNameToEntrezID/merged/Merged_EntrezID_GeneName_EsembleGeneList.tsv'
gene_list = pd.read_csv(path, sep = '\t')

gene_list['GeneID'] = gene_list['GeneID'].apply(lambda x: str(x))
gene_list['gene_id'] = gene_list['GeneName'] + '|' + gene_list['GeneID']

gene_list.to_csv(path, sep = '\t', index= False)