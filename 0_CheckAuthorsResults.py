import pandas as pd

authorsResults = pd.read_csv("data/StemnesAuthorsResults/StemnesScoreAuthorResults.csv", sep = ';')
mineResults = pd.read_csv("data/StemnesResultCheck/MineAuthorsDataResults.txt", sep = '\t')
mineResults.columns = ['sample', 'mine_res']

new_df = pd.DataFrame()
new_df['sample'] = authorsResults['TCGAlong.id']
new_df['authors_res'] = authorsResults['mRNAsi']

#print(mineResults)
new_df = new_df.merge(mineResults, on='sample', how='left')     #merge two df and place values to proper samples using left join

new_df.to_csv('data/StemnesResultCheck/Mine&AuthorsResults_merged.csv', sep = ';', index=False)