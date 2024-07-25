import numpy as np
from .pca_pathway import *

def create_gene_set(universe, psize, n_perm=1000, seed = None, rng = None):
    """This function creates a random gene set from a universe of genes 

    Args:
        universe (set): A set of all possible genes
        psize (int): Number of genes in a gene set 
        n_perm (int): Number of permutations to create a random gene set. Defaults to 1000.
    Returns:
        pd.DataFrame : genrated pathways and theur corresponding genes.
    """    
    if rng is None:
        rng = np.random.default_rng(seed) 

    # Create a DataFrame with two columns: 'pathway' and 'genes'
    # 'pathway' contains pathway numbers ranging from 1 to n_perm
    # 'genes' contains lists of genes, each list being a random selection of psize genes from the universe
    gene_set = pd.DataFrame({
        'pathway': range(1, n_perm + 1),
        'genes': [rng.choice(list(universe), size=psize, replace=False).tolist() for _ in range(n_perm)]})
    return gene_set


def pca_random(reg_net, edges, res_pca_pathways, pathways_list, n_perm=1000, seed = None, rng = None, scale_data = True, center_data = True):
    """This function creates random gene sets and runs PCA analysis on them 

    Args:
        reg_net (pd.DataFrame) : Numeric matrix with samples in columns, features in rows
        edges (pd.DataFrame): containing information on "reg" and "tar"
        res_pca_pathways (pd.DataFrame): Output result of pca_pathway function 
        pathways_list (list): A list of pathways 
        n_perm (int): Number of permutations to create a random gene set. Defaults to 1000. Defaults to 1000.
        scale_data (bool): whether to scale the data (TRUE) or not (FALSE). Defaults to True.
        center_data (bool): whether to center the data (TRUE) or not (FALSE). Defaults to True.

    Returns:
        DataFrame : PCA results from random gene sets 
    """   
    # Extract the unique sizes of pathways from the PCA results 
    pathways_size = res_pca_pathways['pathway_size'].unique() 
    # Create a set of all unique genes in the provided pathways list
    universe = set(gene for genes in pathways_list['genes'] for gene in genes)
    # Initialize a list to store PCA results from random gene sets
    res_pca_random = []
    # Loop over each unique pathway size
    for psize in pathways_size:
        # Generate random gene sets of the current pathway size
        random_genes = create_gene_set(universe, psize, n_perm=n_perm, seed = seed, rng = rng)
        # Run PCA analysis on the generated random gene sets
        res_pca = pca_pathway(random_genes, reg_net, edges,scale_data=scale_data, center_data=center_data)
        # Append the PCA results to the list if it's not empty
        res_pca = res_pca[res_pca['pc1'].notna()]            
        res_pca_random.append(res_pca)

    # Concatenate all PCA results into a single DataFrame
    res_pca_random_all = pd.concat(res_pca_random, ignore_index=True)
    return res_pca_random_all



    

