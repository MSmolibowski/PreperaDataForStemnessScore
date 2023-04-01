import pandas as pd

directory_path = 'data/dodatkoweDane/xlms/' #remember to your path must end with /
file_name = 'Dodatkowe próby czerniak.xlsx'                    #just file name with extension ex: data.xlsx

path = directory_path + file_name
sheet_name = 'Ektoderma'

df = pd.read_excel(path,  sheet_name= sheet_name)

path_to_save_file = 'data/dodatkoweDane/FilesDifferentExtensions/'
file_save_name = 'Czerniak_Ektoderma.tsv'   #remember what sep is used for spec file extension
path = path_to_save_file + file_save_name

df.to_csv(path, sep = '\t', index= False)

print('Done')