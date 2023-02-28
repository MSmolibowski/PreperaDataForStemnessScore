import pandas as pd

#=============================================
def only_Mich(data):     #leave only columns with 'Mitch' in col name
    df1 = data[data.columns[0]]
    df2 = data.filter(regex='Mich')
    df_ret = pd.concat([df1, df2], axis=1)


    return df_ret
#=============================================

R1_path = 'data/Czerniak/R1.csv'
R2_path =  'data/Czerniak/R2.csv'
save_path = 'data/Czerniak/Czerniak_merged.csv'

# Load the first sheet
R1_data = pd.read_csv(R1_path, sep=';',encoding='ISO-8859-1', low_memory=False)
# Load the second sheet
R2_data = pd.read_csv(R2_path, sep=';', encoding='ISO-8859-1', low_memory=False)

temp = pd.DataFrame(R2_data['Gene Symbol'])

R2_data = only_Mich(R2_data)
R2_data['Gene Symbol'] = temp['Gene Symbol']

R1_data = only_Mich(R1_data)

merged_data = pd.merge(R2_data, R1_data, on='Probe Set ID', how='inner')

# Select only the columns
columns_to_keep = ['Probe Set ID'] + ['Gene Symbol'] + [col for col in merged_data.columns if 'Mich' in col]

merged_data = merged_data[columns_to_keep]      #copy only selected columns
#columns1 = merged_data.columns.tolist()

# Rearrange the columns to match the desired order
merged_data = merged_data[['Probe Set ID', 'Gene Symbol' , 'MichI_1', 'MichI_2', 'MichI_3',
                           'MichI_H6_1', 'MichI_H6_2', 'Mich1_H6_3',
                           'MichII_1', 'Mich_II_2', 'MichII_3',
                           'MichII_H6_1', 'MichII_H6_2', 'MichII_H6_3',
                           'MichI_sfery_1', 'MichI_sfery_2', 'MichI_sfery_3',
                           'MichI_H6_Sfery_1', 'MichI_H6_Sfery_2', 'MichI_H6_sfery',
                           'MichII_Sfery_1', 'MichII_Sfery_2', 'MichII_sfery_3',
                           'MichII_H6_Sfery_1', 'MichII_H6_Sfery_2', 'MichII_H6_sfery_3']] #set the order of columns in df (not changing names!) !!



merged_data.to_csv(save_path, sep=';', index=False)

