import pandas as pd
import numpy as np
from .run_pca import *

def pca_pathway(pathways_list, reg_net, edges, scale_data=True, center_data=True):
    """
    This function runs PCA analysis for a list of pathways

    Args:
        pathways_list (pd.DataFrame): list of pathways 
        reg_net (pd.DataFrame) : Numeric matrix with samples in columns, features in rows
        edges (pd.DataFrame): containing information on "reg" and "tar"
        scale_data (bool, optional): whether to scale the data (TRUE) or not (FALSE). Defaults to True
        center_data (bool, optional):  whether to center the data (TRUE) or not (FALSE). Defaults to True.

    Returns:
        Dataframe with pca results for pathways in a pathway file
    """    
     # Initialize an empty list to store results for each pathway
    results = []
    # Iterate over each pathway in the pathways list
    for _, pathway in pathways_list.iterrows():
         # Process the pathway using PCA
        result = process_pathway(pathway, reg_net, edges, scale_data=scale_data, center_data=center_data)
        # Append the result to the results list
        results.append(result)
    # Convert the results list to a DataFrame
    res_pca = pd.DataFrame(results, columns=['pathway', 'pc1', 'n_edges', 'pathway_size'])

    return res_pca

def process_pathway(pathway, reg_net, edges, scale_data=True, center_data=True):
    """This function runs PCA analysis for one pathway 

    Args:
        pathway : a pathway with a list of genes associated 
        reg_net (pd.DataFrame) : Numeric matrix with samples in columns, features in rows
        edges (pd.DataFrame): containing information on "reg" and "tar"
        scale_data (bool, optional):whether to scale the data (TRUE) or not (FALSE). Defaults to True.
        center_data (bool, optional): whether to center the data (TRUE) or not (FALSE). Defaults to True.

    Returns:
       list: A list containing:
              - pathway : The input pathway 
              - pc1 (float): The first principal component score from the PCA analysis.
              - n_edges (int): The number of edges used in the PCA analysis.
              - n_genes (int): The number of genes in the pathway.
    """    
    # Identify the indices of edges where the target genes are in the pathway's gene list
    all_genes = (pathway['genes'])
    idx = edges[edges['tar'].isin(all_genes)].index
     # Extract the subset of the regulatory network corresponding to these indices
    subnet = reg_net.loc[idx]
    pc1 = None
    n_edges = None
    # Perform PCA analysis on the subset
    if not subnet.empty:
        pca_result = run_pca(subnet, scale_data=scale_data, center_data=center_data)
        pc1 = pca_result['pc1'].iloc[0]
        n_edges = pca_result['n_edges'].iloc[0]
 
    return (pathway.iloc[0], pc1, n_edges, len(pathway['genes']))