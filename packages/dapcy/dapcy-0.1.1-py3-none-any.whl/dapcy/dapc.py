from sklearn.pipeline import Pipeline
from sklearn.decomposition import TruncatedSVD
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import KFold, StratifiedKFold, cross_val_score
from sklearn.metrics import confusion_matrix, classification_report
from joblib import Parallel, delayed

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


class dapc:
    """
    This class performs the DAPC method using truncated SVD and LDA.
    
    Attributes:
        n_components (int): Number of components for truncated SVD.
        random_state (int): Random state for reproducibility.
        pipeline (Pipeline): sklearn pipeline.
        label_encoder (LabelEncoder): Encoder for target labels.
        svd (TruncatedSVD): Instance of truncated SVD.
        lda (LinearDiscriminantAnalysis): Instance of LDA.
    """
    
    def __init__(self, n_components=2, random_state=42):
        """
        Initializes the DAPC class with the given parameters.
        
        Parameters:
            n_components (int): Number of components for truncated SVD.
            random_state (int): Random state for reproducibility.
        """
        
        self.n_components = n_components
        self.random_state = random_state
        self.pipeline = None
        self.label_encoder = None
        self.svd = None
        self.lda = None
        
    def create_pipeline(self):
        """Create a DAPC pipeline."""
        
        self.svd = TruncatedSVD(n_components=self.n_components, random_state=self.random_state)
        self.lda = LinearDiscriminantAnalysis()
        self.pipeline = Pipeline([
            ('svd', self.svd),
            ('lda', self.lda)
        ])
    
    def evaluate_pipeline(self, X, y, cv_scheme='stratified', splits=5, n_jobs=-1):
        """
        Evaluate the pipeline using cross-validation.
        
        Parameters:
            X (array-like): Genotype (csr) matrix.
            y (array-like): Target labels.
            cv_scheme (str): Cross-validation scheme ('kfold' or 'stratified').
            splits (int): Number of splits for the cross-validation.
            n_jobs (int): Number of jobs to run in parallel.
        
        Returns:
            float: Mean accuracy score.
        """
        
        if not self.pipeline:
            self.create_pipeline()
        if not self.label_encoder:
            self.label_encoder = LabelEncoder().fit(y)
        y_encoded = self.label_encoder.transform(y)
        random_state = self.random_state

        if cv_scheme == 'kfold':
            cv = KFold(n_splits=splits, random_state=random_state)
        elif cv_scheme == 'stratified':
            print("Changing random_state value to None (see Sklearn's StratifiedKFold documentation)")
            random_state = None
            cv = StratifiedKFold(n_splits=splits, random_state=random_state)
        else:
            raise ValueError("Invalid cv_scheme. Use 'kfold' or 'stratified'.")

        scores = cross_val_score(self.pipeline, X, y_encoded, cv=cv, n_jobs=n_jobs, scoring='accuracy')
        return np.mean(scores)

    def grid_search(self, X, y, n_components_range, cv_scheme='stratified', splits=5, n_jobs=-1):
        """
        Perform a parallel grid search to find the best number of principal components.
        
        Parameters:
            X (array-like): Genotype (csr) matrix.
            y (array-like): Target labels.
            n_components_range (range): Range of n_components to search over.
            cv_scheme (str): Cross-validation scheme ('kfold' or 'stratified').
            splits (int): Number of splits for the cross-validation.
            n_jobs (int): Number of jobs to run in parallel.
        
        Returns:
            tuple: Best number of components and the corresponding score.
        """
        
        def process(n_components):
            self.n_components = n_components
            self.create_pipeline()
            score = self.evaluate_pipeline(X, y, cv_scheme=cv_scheme, splits=splits, n_jobs=n_jobs)
            return n_components, score

        results = Parallel(n_jobs=n_jobs, verbose=10, backend='threading')(delayed(process)(i) for i in n_components_range)
        best_n_components, best_score = max(results, key=lambda x: x[1])
        self.n_components = best_n_components
        self.create_pipeline()
        return best_n_components, best_score
    
    def refit_model(self, X, y):
        """
        Refit the model with the parameters on the dataset.
        
        Parameters:
            X (array-like): Genotype (csr) matrix.
            y (array-like): Target labels.
        """
        
        if not self.pipeline:
            self.create_pipeline()
        if not self.label_encoder:
            self.label_encoder = LabelEncoder().fit(y)
        y_encoded = self.label_encoder.transform(y)
        self.pipeline.fit(X, y_encoded)
        print(f"Model refitted with n_components={self.n_components}")

    def predict(self, X):
        """
        Make predictions using the fitted model.
        
        Parameters:
            X (array-like): Genotype (csr) matrix.
        
        Returns:
            array-like: Predicted target labels.
        
        Raises:
            Exception: If the model is not fitted yet.
        """
        
        if self.pipeline and self.label_encoder:
            predictions = self.pipeline.predict(X)
            return self.label_encoder.inverse_transform(predictions)
        else:
            raise Exception("Model is not fitted yet. Please refit the model using refit_model method.")
            
    def get_svd_info(self):
        """
        Retrieve the SVD eigenvalues and explained variance.
        
        Returns:
            tuple: Eigenvalues and explained variance.
        
        Raises:
            Exception: If the model is not fitted yet.
        """
        if self.svd:
            eigenvalues = self.svd.singular_values_
            explained_variance = self.svd.explained_variance_ratio_
            return eigenvalues, explained_variance
        else:
            raise Exception("Model is not fitted yet. Please fit the model first.")
    
    def plot_lda(self, X, y):
        """Plot the DA results."""
        if not self.pipeline:
            self.create_pipeline()
        if not self.label_encoder:
            self.label_encoder = LabelEncoder().fit(y)
        
        # Fit the pipeline
        self.pipeline.fit(X, y)
        
        # Transform the data
        X_transformed = self.pipeline.transform(X)
        
        # Create a DataFrame for plotting
        df = pd.DataFrame(X_transformed, columns=[f'Component {i+1}' for i in range(X_transformed.shape[1])])
        df['label'] = y
        
        # Plot using Seaborn
        plt.figure(figsize=(10, 8))
        sns.scatterplot(x='Component 1', y='Component 2', hue='label', palette='viridis', data=df, legend='full')
        plt.title('LDA plot')
        plt.xlabel('Component 1')
        plt.ylabel('Component 2')
        plt.legend(title='Class')
        plt.show()

    def plot_confusion_matrix(self, X, y, title='Confusion Matrix'):
        """
        Plot the confusion matrix for the fitted model.
        
        Parameters:
            X (array-like): Genotype (csr) matrix.
            y (array-like): Target labels.
            title (str): Title of the plot.
        
        Raises:
            Exception: If the model is not fitted yet.
        """
        
        if not self.pipeline:
            raise Exception("Model is not fitted yet. Please refit the model using refit_model method.")
        if not self.label_encoder:
            self.label_encoder = LabelEncoder().fit(y)
        y_encoded = self.label_encoder.transform(y)

        # Predict using the pipeline
        y_pred = self.pipeline.predict(X)
        
        # Compute confusion matrix
        cm = confusion_matrix(y_encoded, y_pred)
        
        # Plot confusion matrix using Seaborn
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=self.label_encoder.classes_, yticklabels=self.label_encoder.classes_)
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        plt.title(title)
        plt.show()

    def classification_report(self, X, y):
        """
        Generate a classification report for the refitted model.
        
        Parameters:
            X (array-like): Genotype (csr) matrix.
            y (array-like): Target labels.
        
        Raises:
            Exception: If the model is not fitted yet.
        """
        if not self.pipeline:
            raise Exception("Model is not fitted yet. Please fit the model using refit_model method.")
        if not self.label_encoder:
            self.label_encoder = LabelEncoder().fit(y)
        y_encoded = self.label_encoder.transform(y)

        # Predict using the pipeline
        y_pred = self.pipeline.predict(X)
        
        # Generate classification report
        report = classification_report(y_encoded, y_pred, target_names=self.label_encoder.classes_)
        print(report)
        
    def get_pca_loadings(self, X):
        """Generate the loadings dataframe for the PC components."""
        if not self.svd:
            self.create_pipeline()
        
        # Fit the SVD model
        self.svd.fit(X)
        
        # Extract the loading matrix
        loadings = self.svd.components_
        
        # Create a DataFrame for the loadings
        features = [f'SNP {i+1}' for i in range(loadings.shape[1])]
        loadings_df = pd.DataFrame(loadings.T, index=features, columns=[f'Component {i+1}' for i in range(loadings.shape[0])])
        
        return loadings_df

    def get_top_loadings(self, loadings_df, component=1, top_n=10):
        """Get the top N loadings for a specific PC component.
        
        Parameters:
        - loadings_df: DataFrame containing the loadings
        - component: Component index to get the top loadings for (1-based index)
        - top_n: Number of top loadings to retrieve
        
        Returns:
        - DataFrame containing the top N loadings for the specified component
        """
        if component < 1 or component > loadings_df.shape[1]:
            raise ValueError(f"Component index out of range. Must be between 1 and {loadings_df.shape[1]}.")
        
        # Get the loadings for the specified component
        component_loadings = loadings_df.iloc[:, component - 1]
        
        # Get the top N loadings
        top_loadings = component_loadings.abs().nlargest(top_n)
        
        # Create a DataFrame for the top loadings
        top_loadings_df = loadings_df.loc[top_loadings.index, f'Component {component}']
        
        return top_loadings_df.reset_index()

    def plot_top_loadings(self, top_loadings_df, component=1):
        """Plot the top loadings for a specific PC component.
        
        Parameters:
        - top_loadings_df: DataFrame containing the top loadings
        - component: Component index to plot the loadings for (1-based index)
        """
        # Plot using Seaborn
        plt.figure(figsize=(12, 8))
        sns.barplot(x='index', y=f'Component {component}', data=top_loadings_df, palette='viridis')
        plt.title(f'Top Loadings for Component {component}')
        plt.xlabel('SNP')
        plt.ylabel('Loading')
        plt.xticks(rotation=90)
        plt.show()
        
    def save_pca_components(self, X, filename='pc_components.csv'):
        """Save the PCA components for plotting to a CSV file."""
        if not self.svd:
            self.create_pipeline()
        
        # Fit the SVD model
        self.svd.fit(X)
        
        # Transform the data
        X_transformed = self.svd.transform(X)
        
        # Create a DataFrame for the components
        components_df = pd.DataFrame(X_transformed, columns=[f'Component {i+1}' for i in range(X_transformed.shape[1])])
        
        # Save to CSV
        components_df.to_csv(filename, index=False)

    def save_lda_components(self, X, y, filename='lda_components.csv'):
        """Save the LDA components for plotting to a CSV file."""
        if not self.pipeline:
            self.create_pipeline()
        if not self.label_encoder:
            self.label_encoder = LabelEncoder().fit(y)
        
        # Encode the labels
        y_encoded = self.label_encoder.transform(y)
        
        # Fit the pipeline
        self.pipeline.fit(X, y_encoded)
        
        # Transform the data
        X_transformed = self.pipeline.transform(X)
        
        # Create a DataFrame for the components
        components_df = pd.DataFrame(X_transformed, columns=[f'Component {i+1}' for i in range(X_transformed.shape[1])])
        components_df['label'] = self.label_encoder.inverse_transform(y_encoded)
        
        # Save to CSV
        components_df.to_csv(filename, index=False)

    def save_pca_loadings(self, X, filename='pca_loadings.csv'):
        """Save the PCA loadings for plotting to a CSV file."""
        loadings_df = self.get_pca_loadings(X)
        loadings_df.to_csv(filename, index=True)

    def save_pca_loadings(self, X, filename='pca_loadings.csv'):
        """Save the PCA loadings for plotting to a CSV file."""
        loadings_df = self.get_pca_loadings(X)
        loadings_df.to_csv(filename, index=True)

    def save_eigen_info(self, X, filename='eigen_info.csv'):
        """Save the eigenvectors and eigenvalues from PCA to a CSV file."""
        if not self.svd:
            self.create_pipeline()
        
        # Fit the SVD model
        self.svd.fit(X)
        
        # Get the eigenvalues and explained variance
        eigenvalues = self.svd.singular_values_
        explained_variance = self.svd.explained_variance_ratio_
        
        # Create a DataFrame for the eigen info
        eigen_df = pd.DataFrame({
            'Eigenvalue': eigenvalues,
            'Explained Variance': explained_variance
        })
        
        # Save to CSV
        eigen_df.to_csv(filename, index=False)

    def get_score_accuracy(self, X, y):
        if not self.pipeline:
            raise Exception("Model is not fitted yet. Please fit the model using refit_model method.")
        if not self.label_encoder:
            self.label_encoder = LabelEncoder().fit(y)
        y_encoded = self.label_encoder.transform(y)

        y_pred = self.pipeline.predict(X)
        accuracy = accuracy_score(y_encoded, y_pred)
        return accuracy