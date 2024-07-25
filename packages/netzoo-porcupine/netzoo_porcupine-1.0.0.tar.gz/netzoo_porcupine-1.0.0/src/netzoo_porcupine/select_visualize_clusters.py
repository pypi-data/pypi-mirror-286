import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from yellowbrick.cluster import KElbowVisualizer
from .pca_scores import *
import seaborn as sns

def select_number_clusters(pathways_list, reg_net, edges, scale_data=True, center_data=True, kmax=8, random_state = 156):
    """Visualize and select the optimal number of clusters based on PCA scores.

    Args:
        pathways_list (pd.DataFrame): List of pathways
        reg_net (pd.DataFrame): Numeric matrix with samples in columns, features in rows
        edges (pd.DataFrame): DataFrame containing information on "reg" and "tar"
        scale_data (bool, optional): Whether to scale the data (TRUE) or not (FALSE). Defaults to True.
        center_data (bool, optional): Whether to center the data (TRUE) or not (FALSE). Defaults to True.
        kmax (int, optional): Maximum number of clusters to consider. Defaults to 8.
        random_state (int, optional): Seed for random number generator for reproducibility. Defaults to 42.
    Returns:
        None: The function will plot the optimal number of clusters using the silhouette method.
    """
    # Get the PCA scores for the pathways
    pca_scores = get_pathway_ind_scores(pathways_list, reg_net, edges, scale_data = scale_data, center_data = center_data)
    # Extract the PCA scores for clustering
    results = pca_scores[['Dim.1', 'Dim.2']]
    # Initialize the KMeans model
    model = KMeans(random_state = random_state)
    # Initialize the KElbowVisualizer with the silhouette metric
    visualizer = KElbowVisualizer(model, k=(2, kmax+1), metric='silhouette', timings=False)
    # Fit the visualizer with the data
    visualizer.fit(results)
    # Show the plot
    visualizer.show()
    
def visualize_clusters(pathway_of_interest, reg_net, edges, number_of_clusters, scale_data=True, center_data=True, random_state = 156):
    """Visualization of clustering of patients into specified number of clusters

    Args:
        pathway_of_interest (tuple or pd.Series): List with genes in a pathway of interest
        reg_net (pd.DataFrame): Numeric matrix with samples in columns, features in rows
        edges (pd.DataFrame): DataFrame containing information on "reg" and "tar"
        number_of_clusters (int): specifying the number of clusters
        scale_data (bool, optional): Whether to scale the data (TRUE) or not (FALSE). Defaults to True.
        center_data (bool, optional): Whether to center the data (TRUE) or not (FALSE). Defaults to True.

    Returns:
        plot : The function will plot the clustering of patients 
    """
    results = get_pathway_ind_scores(pathway_of_interest, reg_net, edges, scale_data, center_data)
    
    # Assure that results is a DataFrame
    data = results[['Dim.1','Dim.2']]
    
    if scale_data or center_data:
        scaler = StandardScaler(with_mean=center_data, with_std=scale_data)
        data = scaler.fit_transform(data)
    
    # Perform k-means clustering
    kmeans = KMeans(n_clusters=number_of_clusters, n_init=25, random_state= random_state)
    clusters = kmeans.fit_predict(data)
    
    # Create a DataFrame with the cluster assignments
    data_with_clusters = pd.DataFrame(data, columns=[f'Feature{i+1}' for i in range(data.shape[1])])
    data_with_clusters['Cluster'] = clusters
    
    
    # Plotting
    plt.figure(figsize=(6, 6))
    sns.scatterplot(x='Feature1', y='Feature2', hue='Cluster', data=data_with_clusters, palette='viridis')
    plt.title('Clusters plot')
    plt.xlabel('Dim.1')
    plt.ylabel('Dim.2')
    plt.legend(title='Cluster')
    plt.grid(True)
    plt.show()
    
    return {'plot': plt, 'clusters': kmeans}