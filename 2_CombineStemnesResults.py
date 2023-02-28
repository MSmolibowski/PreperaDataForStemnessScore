import pandas as pd
import os

folder = 'FPKM_res'         #write folder name
path = f'C:/Users/mikol/Desktop/StemnesScoreAnalysis/PanCanStem_Web/Rmardown/data/results/{folder}'     #type path were results are stored
save_path = f'C:/Users/mikol/Desktop/StemnesScoreAnalysis/PanCanStem_Web/Rmardown/data/results/{folder}'    #write path were you want save your results

groups = ["H2073", "SKMES"]    #write group name

for group in groups:
    df_list = []
    first_file = True

    for file in os.listdir(path):                   #get files names stored in folder
        if file.endswith(".tsv") and group in file:     #perform operation only for .tsv file with specific group name
            file_path = os.path.join(path, file)        #create path to specific file
            df = pd.read_csv(file_path, sep='\t', header=None)  #read this file
            if first_file:
                column_names = ['file_name', file.strip('.tsv')]    #create column with names of samples and column with name of files from which data was taken
                df.columns = [column_names]     #here create column
                df_list.append(df)              #add to list df
                first_file = False
            else:
                column_names = ['', file.strip('.tsv')]
                df.columns = [column_names]
                df = df.iloc[:,1:]  #copy from file only column with results of analysis
                df_list.append(df)

    final_df = pd.concat(df_list, axis=1)       #combine all files in df list to one
    final_df.to_csv(os.path.join(save_path, group+"_all.csv"), sep=';', index=False)

