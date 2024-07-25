import pyreadr

import pandas as pd

def load_data(net_file_path=None, edges_file_path=None):
    '''
    Loads both network data and edge information from files specified by the user

    Parameters:
    - net_file_path (str): path to the input networks data file
    - edges_file_path (str) : path to the input edges data file 

    Returns:
        - net (DataFrame): The network data
        - edges (DataFrame): The edges data
    '''
    
    net = load_net_file(net_file_path)

    edges = load_edges_file(edges_file_path)

    return net, edges

def load_net_file(net_file_path=None):
    '''
    Loads network data from file specified by the user   

    Parameters:
    - net_file_path (str): path to the input networks data file 

    Returns:
        - net (DataFrame): The network data
    '''
    
    if net_file_path is None:
        net_file_path = input("Network file path => ")
    data = pyreadr.read_r(net_file_path)
    net = data['net'] # Network data is stored in net

    return net

def load_edges_file(edges_file_path=None):
    '''
    Loads edges information from file specified by the user   

    Parameters:
    - edges_file_path (str): path to the input networks data file 

    Returns:
    - edges (DataFrame): The edges data
    '''

    if edges_file_path is None:
        edges_file_path = input("Edges file path => ")
    data_edges = pyreadr.read_r(edges_file_path)
    edges = data_edges['edges'] # Edge data is stored in edges

    return edges

def load_gmt(pathways_file_path=None):

    '''
    Load a .gmt file containing information about biological pathways

    Parameters:
    gmt_file (str): Path to the input .gmt file. Gmt file is downloaded
        from http://www.gsea-msigdb.org/gsea/msigdb/collections.jsp

    Returns:
    A list of pathways from the .gmt file
    '''
     
    if pathways_file_path is None:
        pathways_file_path = input("Pathways file path => ")

    pathways_list = []

    # Reading the .gmt file and extracting pathway and gene information
    with open(pathways_file_path, 'r') as file:
        for line in file:
            fields = line.split('\t') # Fields are tab-separated
            pathway = fields[0]  # Pathway name is the first field
            genes = [f.strip() for f in fields[2:]] # Extracting genes from fields, removing leading and trailing whitespace from each gene
            pathways_list.append((pathway, genes)) # Adding pathway name and gene list to pathways_list
    return pathways_list


def filter_pathways(pathways_list,edges):
    """
    Filter a list of pathways to include only genes present in networks

    Parameters:
    pathways_list : list of pathways
    edges : dataframe containing information on "reg" and "tar"

    Returns:
    A list of filtered pathways
    """
    
    # Extracting unique genes from edge data
    unique_edges = edges['tar'].unique()
    pathways_filt = []
    # Iterate over each pathway in the list
    for pathway, genes in pathways_list:
        filtered_genes = [gene for gene in genes if gene in unique_edges] # Filter genes to keep only those present in the unique genes from edges
        if filtered_genes:
            pathways_filt.append((pathway, filtered_genes)) # Append the pathway with filtered genes to the pathways_filt list if genes remain after filtering 

    # Creating a dataframe from patwhways_filt with columns 'pathway' and 'genes'
    pathways_filt = pd.DataFrame(pathways_filt, columns=['pathway', 'genes'])

    return pathways_filt



def filter_pathways_size(pathways_filt,minSize=5,maxSize=150):
    '''
    Filter a list of pathways based on specified minimum and maximum size for number of genes in a pathway

    Parameters:
    pathways_list : list of pathways
    minSize (int): minimum size for number of genes in a pathway (default = 5)
    maxSize (int): maximum size for number of genes in a pathway (default = 150)

    Returns:
    A list of filtered pathways
    '''
    # Filtering pathways based on the length of the gene list
    pathways_to_use = pathways_filt[
    (pathways_filt['genes'].apply(len) >= minSize) & # Filtering pathways with specified minimum size
    (pathways_filt['genes'].apply(len) <= maxSize) # Filtering pathways with specified maximum size
    ]

    return pathways_to_use

def pathways_sorting(pathways_list):
    sorted_pathways = pathways_list.sort_values(by='pathway')

    return sorted_pathways