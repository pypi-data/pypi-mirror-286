import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.datasets import load_iris
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import LabelEncoder


def plot_pca(X, y, title='PCA Projection', n_components=2):
    """
    This function performs Truncated SVD on the dataset and plots the result in 2D.
    """
    # Encode labels to ensure they are in a suitable format for coloring
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    labels = label_encoder.classes_

    # Perform Truncated SVD
    svd = TruncatedSVD(n_components=n_components)
    X_reduced = svd.fit_transform(X)

    # Prepare DataFrame for Seaborn plotting
    df = pd.DataFrame(X_reduced, columns=['Component 1', 'Component 2'])
    df['Class'] = y_encoded
    
    # Calculate explained variance
    explained_variance = svd.explained_variance_ratio_
    component_1_var = explained_variance[0] * 100
    component_2_var = explained_variance[1] * 100

    # Plotting using Seaborn
    plt.figure(figsize=(8, 6))
    scatter = sns.scatterplot(data=df, x='Component 1', y='Component 2', hue='Class', palette='Spectral', s=60, edgecolor='k', legend='full')
    plt.title(title)
    plt.xlabel(f'Component 1 ({component_1_var:.2f}% Variance)')
    plt.ylabel(f'Component 2 ({component_2_var:.2f}% Variance)')
    plt.grid(True)
    plt.legend(title='Class', loc = 'upper left', labels=labels)
    plt.show()
    
def plot_cumulative_variance(X, title ='Cumulative Variance Explained by Principal Components', n_components=10):
    """
    This function plots the number of principal components retained vs. cumulative variance explained.
    """
    svd = TruncatedSVD(n_components=n_components)
    svd.fit(X)
    cumulative_variance = svd.explained_variance_ratio_.cumsum()

    # Prepare DataFrame for Seaborn plotting
    df_variance = pd.DataFrame({
        'Number of Principal Components': range(1, n_components + 1),
        'Cumulative Variance Explained': cumulative_variance
    })

    # Plotting using Seaborn
    plt.figure(figsize=(8, 6))
    sns.lineplot(data=df_variance, x='Number of Principal Components', y='Cumulative Variance Explained', marker='o')
    plt.xlabel('Number of Principal Components')
    plt.ylabel('Cumulative Variance Explained')
    plt.title(title)
    plt.grid(True)
    plt.show()