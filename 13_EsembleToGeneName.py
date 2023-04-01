import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import socket
import os


def find_gene_id(gene_symbol):
    # construct the URL for the gene search results page
    url = f'https://www.ncbi.nlm.nih.gov/gene/?term={gene_symbol}'

    # send a GET request to the URL
    while True:
        try:
            response = requests.get(url)
            break
        except requests.exceptions.RequestException as e:
            print(f"Connection error: {e}. Retrying in 5 seconds...")
            time.sleep(5)

    # parse the HTML content of the response using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # extract the gene ID from the HTML code
    gene_id_element = soup.find('h1', {'class': 'title'})

    if gene_id_element is not None:
        gene_id = gene_id_element.find('span', {'class': 'gn'}).text
        print(f"Gene ID for {gene_symbol} is: {gene_id}")
        return gene_id
    else:
        print(f"No gene ID found for {gene_symbol}")
        return None


def scrape_gene_ids(df):
    # retrieve a list of gene symbols from the DataFrame
    gene_symbols = df['tracking_id'].tolist()

    # create a dictionary to store gene IDs
    gene_id_dict = {}

    # loop through each gene symbol and find the corresponding gene ID
    for gene_symbol in gene_symbols:
        # check if the gene ID has already been found for this gene symbol
        if gene_symbol in gene_id_dict:
            continue

        # find the gene ID for the current gene symbol
        gene_id = find_gene_id(gene_symbol)

        # update the gene ID dictionary with the new gene ID (or 'NoGeneID' if the ID wasn't found)
        gene_id_dict[gene_symbol] = gene_id if gene_id is not None else 'NoGeneID'

    # create a new column for the gene IDs in the DataFrame
    df['GeneName'] = df['tracking_id'].apply(lambda x: gene_id_dict[x])

    return df

if __name__ == '__main__':
    # set the input and output folder paths
    input_folder_path = 'data/dodatkoweDane/Esemble id/EsembleShorterLists'
    output_folder_path = 'data/dodatkoweDane/Esemble id/EsembleToGeneName'

    for filename in os.listdir(input_folder_path):
        # check if the file is a TSV file
        if filename.endswith(".tsv"):
            # load the TSV file into a dataframe
            df = pd.read_csv(os.path.join(input_folder_path, filename), sep="\t")
            print(filename)
            # scrape the gene IDs
            df = scrape_gene_ids(df)

            # save the updated DataFrame to a new CSV file
            df.to_csv(os.path.join(output_folder_path, 'GeneName_'+filename), index=False)