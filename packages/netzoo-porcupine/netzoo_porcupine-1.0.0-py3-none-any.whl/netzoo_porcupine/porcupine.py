import pandas as pd
import numpy as np
from scipy.stats import ttest_1samp

def calculate_statistics(res_pca_pathway, res_pca_rndm_set):
    """This function compares the PCA score for a pathway to a set of PCA scores of random gene sets of the same size as pathway. It calculates p-value and effect size.

    Args:
        res_pca_pathway (pd.DataFrame): Result taable of pca_pathway function for one pathway
        res_pca_rndm_set (pd.DataFrame): Result table of pca_random function for one pathway

    Returns:
        pd.DataFrame: a table of statistics (p-value and effect size) for each pathway.
    """

    pc1_rndm = res_pca_rndm_set['pc1'].values
    pathway = res_pca_pathway["pathway"]
    path_size = res_pca_pathway["pathway_size"]
    pc1_pathway = res_pca_pathway["pc1"]
    
    # Calculate the p-value
    _, pvalue = ttest_1samp(pc1_rndm, popmean=pc1_pathway, alternative='less')

    # Calculate effect size with Cohen's D 
    mean_diff = abs(np.mean(pc1_rndm) - pc1_pathway)
    pooled_std = np.std(pc1_rndm, ddof=1)    
    effect_size = mean_diff / pooled_std


    
    # Store results in a DataFrame 
    stat_res = pd.DataFrame({
        "pathway": [pathway],
        "pathway_size": [path_size],
        "pc1": [pc1_pathway],
        "pval": [pvalue],
        "es": [effect_size]
    })
    
    return stat_res


def porcupine(res_pca_pathways, res_pca_rndm):
    """This function compares results of PCA analysis for each pathway versus a set of random genes sets. It calculates p-value and effect size for each pathway.

    Args:
        res_pca_pathways (pd.DataFrame): Output result table of pca_pathway function
        res_pca_rndm (pd.DataFrame): Output result table of pca_random function 

    Returns:
        pd.DataFrame: a table of statistics (pvalue and effect size) for each pathway
    """
    # Extract the unique sizes of pathways from the PCA results 
    pathways_size = res_pca_pathways['pathway_size'].unique()

    # Create an empty DataFrame
    res_all = pd.DataFrame()

    # Loop over each unique pathway size
    for path_size in pathways_size:
        print("Pathways with size", path_size)
        # Create sets with pathways of the same pathway size
        res_pathway_set = res_pca_pathways[res_pca_pathways['pathway_size'] == path_size]
        res_rndm_set = res_pca_rndm[res_pca_rndm['pathway_size'] == path_size]
        # Apply the calculate_statistics function on each pathway of the created set 
        res = res_pathway_set.apply(lambda x: calculate_statistics(x, res_rndm_set), axis=1)
        # Concatenate the DataFrmae with the obtained results
        res_all = pd.concat([res_all, pd.concat(res.tolist(), ignore_index=True)], ignore_index=True)    
        

    return res_all



    
    


    

