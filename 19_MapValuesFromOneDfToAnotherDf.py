import pandas as pd
import os

def map_records(df, df_PSC):
    # select only the rows in df1 that have matching gene_id values in df2
    df1_matching = df_PSC[df_PSC['gene_id'].isin(df['gene_id'])]

    # merge the matching rows from df1 with df2, keeping all columns from both DataFrames
    merged_df = pd.merge(df1_matching, df, on='gene_id')

    return merged_df


#----------------
path = 'data/filtered/TPM'
output_folder_path = 'data/OurDataWithExtraData/ExtraDataTPM'
for file_name in os.listdir(path):

    PSC_file_path = 'data/dodatkoweDane/gene_idMapedToEsemble/Czerniak_PSC.tsv_gene_id'
    EkEd_file_path = 'data/dodatkoweDane/gene_idMapedToEsemble/Czerniak_Ektoderma.tsv_gene_id'

    df_PSC = pd.read_csv(PSC_file_path, sep='\t')
    df_EkEd = pd.read_csv(EkEd_file_path, sep='\t')

    if file_name.endswith(".tsv"):
        # Load the TSV file into a dataframe
        df = pd.read_csv(os.path.join(path, file_name), sep="\t")

        df = map_records(df, df_PSC)
        df = map_records(df, df_EkEd)

        # Save the updated DataFrame to a new CSV file
        df.to_csv(os.path.join(output_folder_path, 'WithExtraData_' + file_name), index=False)


