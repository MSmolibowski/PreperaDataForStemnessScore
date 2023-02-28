# PreperaDataForStemnessScore
Durring my job I had to prepare data for PanCanStem program (R program) which was used for "Machine Learning Identifies Stemness Features Associated with Oncogenic Dedifferentiation" and It can be found here: http://www.cell.com/cell/fulltext/S0092-8674(18)30358-1.

Program is avaliable here: https://github.com/BioinformaticsFMRP/PanCanStem_Web



#How data for program should look like:
Programs requires data in tsv format, with first column named gene_id where are stored gene names with their Entrez gene id separated by |.
example: A1BG|1; A1CF|29974 etc.
values must be sorted ascending

My data descritpion:
- SKMES, H2073 - 8 samples, each sample in triplicate,
  - gene names and gene id in files,
  - FPKM values,
  - TPM values,
- Czerniak - 8 samples in triplicate, splited in two different files (first file - 2 columns for every sample, second file - 1 column for every sample),
  - gene names in files,
  - no gene id in files,
  - other columns not neccesary for analysis in files,
  
Scripts description:
---------------------------
> 0_CheckAuthorsResults

To be sure that code is working fine and results are ok I performed analysis using data delivered by authors.
When I got results I wanted to compare results published by authors with mine.
This script takes results I got after using programm, authors of program results and merge them using column named 'samples'

Results were ok so I starded prepering my own data sets to perform analysis on RNAseq data from 2 cancer cell lines (SKEMS and H2073) and oncological patients (Czerniak).

## 1_H2073_SKMES_PrepareData
This script takes csv files for SKMES and H2073 and:
~def prepare_data(data, file_name):
  - create new column 'gene_id', using values from columns 'Gene_Symbol' and 'Gene_ID',
  - create seperate file for data with FPKM and TPKM values,
  - (filtering) delete rows where number of 0 in row is equal = [7, 5, 2, 1, 0] (rows with 30%, 20%, 10%, 5% of 0 in row were remover)
  - save created files as .tsv file,
  - call calculate_mean function,
~ def calculate_mean(data, numb, file_name, switcher):
  - calculate mean for every samle using 3 columns,
  - save results for every sample to new dataframe
  - save created dataframe as new .tsv file,
  (At the end there will be 4 folders: FPKM, TPM, FPKM_MEAN, TPM_MEAN, in each folder there will be 5 files for H2073 and 5 files for SKMES)
  
 ## 2_CombineStemnesResults
 After preparing so many data I wanted so see how deleting different number of rowas and how using mean value for samples will affect results
 I wanted to merge all files for H2073 and SKMES data, 
 This script read files created by R program and merge them.
 Seperatly for H2073, H2073 with calculated mean values and so on.
 
 > 3_CzerniakMergeFiles
 This script takes both Czerniak files and:
 - leave only neccesary columns,
 - merge both dataframes to one using 'Probe Set ID' column,
 - rearange columns to desired order,
 - save file as .csv file, sep = ';',
 
 > 4_CzerniakPrepareData
 This script:
 - read file created by 3_CzerniakMergeFiles,
 - drop rows where gene name was equal '---',
 - create two dataframes where:
    -> first df: drop rows with '//' in their cell in 'Gene Symbol' column (sometimes there were multiple gene names in cells separated by '//')
    -> second df: save rows with multiple gene names but leave only first gene name,
 - save both files as csv files 
(first file: WithoutMultipleGeneNames.csv, second file: FirstGeneName.csv)

> 5_CzerniakSmallerGeneLists
This script:
- read one of files (FirstGeneName.csv, there is more gene names than in second file, but all genes in second file match to genes in first file)
- create multiple genes list, (every gene list has max 2000 gene names)
- save created gene lists as .tsv files,

!Created list were used for finding genes id for gene names

> 6_CzerniakGetID
This script was used for scraping genes id from ncbi web site.
- read all gene name lists (in sequence),
- create dictionary using gene name list from readed data,
- for every gene in dictionary use url = f'https://www.ncbi.nlm.nih.gov/gene/?term=({gene_symbol}+%5BGene+Name%5D)+AND+Homo+sapiens%5BOrganism%5D'
and get gene id from https page and add it to dictionary,
- create new column named 'Gene ID' and assign gene id to matching gene names using data from dictionary,
- save updated file as .tsv

! this code has safeguard which prevents connection loss, if the connection with internet is lost, code waits until connection returns,
!!! Scraping genes from webside for almost 20 000 genes was very slow, finding genes id for 2000 records took 3-6h

> 7_CzerniakGetID_Entrez
I created this code to perform searching genes id faster.
This code:
- read all gene name lists (in sequence),
- create dictionary using gene name list from readed data,
- for every gene in dictionary use Entrez function and finds gene id for gene     handle = Entrez.esearch(db='gene', term=f'"{gene_symbol}"[Gene Name] AND Homo sapiens[Organism]')
- create new column named 'Gene ID' and assign gene id to matching gene names using data from dictionary,
- save updated file as .tsv,

! finding genes id using this code was much much faster, 30minutes for 2000 gene names,

> 8_CzerniakMergeFiles_ID 
This code:
- reads all files with found genes id to one list,
- merge files to one file,
- save created file as .tsv,

 > 9_CzerniakCreateFileForStemnesScore
 This code:
 - read first and second file (.csv),
 - read file with all genes and their id (MainGeneList_ID.tsv),
 - create new column named 'Gene ID' in first and second file,
 - assign gene id to proper gene name using values from MainGeneList_ID.tsv,
 - save updated files as .csv,
 
 > 10_CzeniakFilterAndFinallPrepare
 This code:
 - read first and second file (.csv),
 - create gene_id column using values from 'Gene Symbol' and 'Gene ID' columns,
 - drop  'Probe Set ID', 'Gene Symbol', 'Gene ID' columns,
 - save updated files as .tsv,
 
 > 11_CzerniakUniqRowGenes
 This code:
 - read selected file (first or second),
 - delete rows with duplicated gene name in 'gene_id' column,
 - replace ',' to '.' in every column with numerical values,
 - sort all values scending using 'gene_id' column,
 - save file as .tsv,
 
 > 12_RNA_script_mod_MS
 It is modified code from https://github.com/BioinformaticsFMRP/PanCanStem_Web which was used for analysis.
- In this code I had to add few lines of code which converts data to proper format, because function which had to do it didn't work.
- I added also for loop to read multipple files from specified directory to perform analysis for many files without changeing path to file for every single file. 
- Added functionality which creates required folder to store results of performed analysis.
 
 
 



