import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

class kmeans_group:
    """
    This class performs K-means clustering on the genotype matrix after reducing its dimensionality using Truncated SVD.
    
    Attributes:
        n_components (int): Number of components for Truncated SVD.
        start_k (int): Starting number of clusters for K-means.
        end_k (int): Ending number of clusters for K-means.
        random_state (int): Random state for reproducibility.
        svd (TruncatedSVD): Instance of Truncated SVD.
        k_values (range): Range of cluster numbers to evaluate.
        sse (list): Sum of squared errors for each K.
        silhouette_scores (list): Silhouette scores for each K.
    """
    
    def __init__(self, n_components=2, start_k=2, end_k=10, random_state=42):
        """
        Initializes the KMeansGroup class with the given parameters.
        
        Parameters:
            n_components (int): Number of components for Truncated SVD.
            start_k (int): Starting number of clusters for K-means.
            end_k (int): Ending number of clusters for K-means.
            random_state (int): Random state for reproducibility.
        """
        self.n_components = n_components
        self.start_k = start_k
        self.end_k = end_k
        self.random_state = random_state
        self.svd = TruncatedSVD(n_components=self.n_components, random_state=self.random_state)
        self.k_values = range(self.start_k, self.end_k + 1)
        self.sse = []
        self.silhouette_scores = []

    def fit_transform(self, X):
        """
        Applies Truncated SVD to the genotype matrix and returns the transformed data.
        
        Parameters:
            X (array-like): The input data to be transformed.
        
        Returns:
            X_svd (array-like): The transformed data after applying Truncated SVD.
        """
        X_svd = self.svd.fit_transform(X)
        return X_svd

    def evaluate_clusters(self, X_svd):
        """
        Evaluates K-means clustering for different values of K using SSE and silhouette scores.
        
        Parameters:
            X_svd (array-like): The input data in the reduced dimensionality space.
        """
        for k in self.k_values:
            kmeans = KMeans(n_clusters=k, random_state=self.random_state)
            kmeans.fit(X_svd)
            self.sse.append(kmeans.inertia_)
            score = silhouette_score(X_svd, kmeans.labels_)
            self.silhouette_scores.append(score)

    def plot_evaluation_metrics(self):
        """
        Plots the SSE and silhouette scores for different values of K to help determine the optimal number of clusters.
        """
        plt.figure(figsize=(12, 6))
        sns.set(style="whitegrid")

        # Plotting the Elbow Method graph
        plt.subplot(1, 2, 1)
        sns.lineplot(x=self.k_values, y=self.sse, marker='o')
        plt.xlabel('Number of Clusters')
        plt.ylabel('SSE')
        plt.title('Elbow Method For Optimal k')
        
        # Plotting the Silhouette Scores graph
        plt.subplot(1, 2, 2)
        sns.lineplot(x=self.k_values, y=self.silhouette_scores, marker='o')
        plt.xlabel('Number of Clusters')
        plt.ylabel('Silhouette Score')
        plt.title('Silhouette Score For Each k')
        plt.show()

    def cluster(self, X_svd, n_clusters):
        """
        Performs K-means clustering on the reduced data with the specified number of clusters.
        
        Parameters:
            X_svd (array-like): The input data in the reduced dimensionality space.
            n_clusters (int): The number of clusters to form.
        
        Returns:
            y_kmeans (array-like): Cluster labels for each point in the dataset.
            centers (array-like): Coordinates of cluster centers.
        """
        kmeans = KMeans(n_clusters=n_clusters, random_state=self.random_state)
        y_kmeans = kmeans.fit_predict(X_svd)
        return y_kmeans, kmeans.cluster_centers_

    def plot_clusters(self, X_svd, y_kmeans, centers):
        """
        Plots the K-means clustering results including the data points and cluster centers.
        
        Parameters:
            X_svd (array-like): The input data in the reduced dimensionality space.
            y_kmeans (array-like): Cluster labels for each point in the dataset.
            centers (array-like): Coordinates of cluster centers.
        """
        plt.figure(figsize=(10, 6))
        sns.scatterplot(x=X_svd[:, 0], y=X_svd[:, 1], hue=y_kmeans, palette='Spectral', s=50, alpha=0.7, legend=None)
        sns.scatterplot(x=centers[:, 0], y=centers[:, 1], color='red', s=200, marker='X')
        plt.xlabel('Component 1')
        plt.ylabel('Component 2')
        plt.title(f'K-means Clustering with {len(centers)} Clusters')
        plt.show()