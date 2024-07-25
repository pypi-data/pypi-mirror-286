from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np

def run_pca(data, scale_data=True, center_data=True):
    """This function perform PCA analysis on the data

    Args:
        data (pd.DataFrame): with samples in columns, and features in rows
        scale_data (bool): whether to scale the data (TRUE) or not (FALSE). Defaults to True
        center_data (bool):  whether to center the data (TRUE) or not (FALSE). Defaults to True.

    Returns:
        pd.DataFrame: _description_
    """    
    # Transpose the data matrix
    data_t = np.transpose(data)

    # Scale and/or center the data if specified
    if scale_data or center_data:
        # Initialize the StandardScaler object with mean centering and scaling
        scaler = StandardScaler(with_mean=center_data, with_std=scale_data)
        # Scale and center the data using the scaler object
        data = scaler.fit_transform(data_t)
    
    pca = PCA() # Initialize PCA object
    pca.fit(data) # Fit PCA to data
    
    # Calculate the percentage of variance explained by the first principal component
    pc1 = pca.explained_variance_ratio_[0] * 100
    
    result = pd.DataFrame({"pc1": pc1, "n_edges": data.shape[1]}, index=[0])
    return result


