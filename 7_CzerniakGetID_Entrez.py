import pandas as pd
import time
import os
from Bio import Entrez


def find_gene_id(gene_symbol):
    # Use Entrez Programming Utilities to query the gene database
    handle = Entrez.esearch(db='gene', term=f'"{gene_symbol}"[Gene Name] AND Homo sapiens[Organism]')
    record = Entrez.read(handle)

    # Check if any records were returned
    if record['Count'] == '0':
        print(f"No gene ID found for {gene_symbol}")
        return None

    # Retrieve the gene ID from the first record
    gene_id = record['IdList'][0]
    print(f"Gene ID for {gene_symbol} is: {gene_id}")
    return gene_id


def scrape_gene_ids(df):
    # Retrieve a list of gene symbols from the DataFrame
    gene_symbols = df['Gene Symbol'].tolist()

    # Create a dictionary to store gene IDs
    gene_id_dict = {}

    # Loop through each gene symbol and find the corresponding gene ID
    for gene_symbol in gene_symbols:
        # Check if the gene ID has already been found for this gene symbol
        if gene_symbol in gene_id_dict:
            continue

        # Find the gene ID for the current gene symbol
        gene_id = find_gene_id(gene_symbol)

        # Update the gene ID dictionary with the new gene ID (or 'NoGeneID' if the ID wasn't found)
        gene_id_dict[gene_symbol] = gene_id if gene_id is not None else 'NoGeneID'

    # Create a new column for the gene IDs in the DataFrame
    df['Gene ID'] = df['Gene Symbol'].apply(lambda x: gene_id_dict[x])

    return df


if __name__ == '__main__':
    # Set the email address to use for API queries
    Entrez.email = 'your_email@address.com'

    # Set the input and output folder paths
    input_folder_path = 'data/Czerniak/GeneLists'
    output_folder_path = 'data/Czerniak/GeneListID_Entrez'

    # Loop through each input file in the input folder
    for filename in os.listdir(input_folder_path):
        # Check if the file is a TSV file
        if filename.endswith(".tsv"):
            # Load the TSV file into a dataframe
            df = pd.read_csv(os.path.join(input_folder_path, filename), sep="\t")
            print(filename)

            # Scrape the gene IDs using the API
            df = scrape_gene_ids(df)

            # Save the updated DataFrame to a new CSV file
            df.to_csv(os.path.join(output_folder_path, 'ID_'+filename), index=False)