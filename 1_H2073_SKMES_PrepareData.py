#-----------------Description--------------------
#-----------------Libraries----------------------
import pandas as pd
import os
#----------------Functions-----------------------
#********************************************************************
def prepare_data(data, file_name):
    data['Gene_ID'] = data['Gene_ID'].apply(lambda x: str(x))
    data['gene_id'] = data['Gene_Symbol'] + '|' + data['Gene_ID']

    df_fpkm = data.filter(regex='FPKM')
    df_tpm = data.filter(regex='TPM')

    df_fpkm.insert(0, 'gene_id', data['gene_id'])
    df_tpm.insert(0, 'gene_id', data['gene_id'])

    numb_of_0_in_row = [7, 5, 2, 1, 0]
    for numb in numb_of_0_in_row:
        # Create a boolean mask that is True for rows where the number of zeros is greater than 7
        mask = (df_fpkm == 0).sum(axis=1) > numb

        # Use the mask to drop the rows from the dataframe
        df_fpkm = df_fpkm.drop(df_fpkm[mask].index)
        df_tpm = df_tpm.drop(df_tpm[mask].index)

        #save filtered data
        df_fpkm.to_csv(f'data/filtered/FPKM/{file_name}_FPKM_{numb}.tsv', sep = '\t', index= False)
        df_fpkm.to_csv(f'data/filtered/TPM/{file_name}_TPM_{numb}.tsv', sep = '\t', index= False)

        calculate_mean(df_fpkm, numb, file_name, 'FPKM')
        calculate_mean(df_tpm, numb, file_name, 'TPM')

#********************************************************************
def calculate_mean(data, numb, file_name, switcher):
    df_mean = pd.DataFrame()

    # Define the prefixes for the columns to be included in each mean calculation
    prefixes = ['K1', 'K2', 'S1', 'S2', 'S3', 'S4', 'S5', 'S6']

    for prefix in prefixes:
        cols = [col for col in data.columns if col.startswith(prefix)]
        df_mean[prefix + f'{switcher}_mean'] = data[cols].mean(axis=1)

    df_mean = df_mean.apply(lambda x: x.round(6))
    df_mean.insert(0, 'gene_id', data['gene_id'])
    df_mean.to_csv(f'data/filtered/MEAN/{switcher}_MEAN/{file_name}_{numb}_{switcher}_MEAN.tsv',sep='\t', index=False)

#********************************************************************
#---------------CODE-----------------------------
#read data
data_H = pd.read_csv('data/csv/H2073.csv', sep=';')
data_S = pd.read_csv('data/csv/SKMES.csv', sep=';', low_memory=False)

#unify column names
data_S.columns = data_H.columns

print(f'Preparing data for H2073')
prepare_data(data_H, 'H2073')
print(f'Finished')
print()
print(f'Preparing data for SKMES')
prepare_data(data_S, 'SKMES')
print(f'Finished')

#-----------------------------------------------
