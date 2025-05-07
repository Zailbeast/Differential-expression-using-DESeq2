import pandas as pd
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np

# Load the cleaned dataset
cleaned_df = pd.read_csv("cleaned_differential_expression_results.csv")

# Log-transform baseMean for dimensionality reduction
cleaned_df['log_baseMean'] = np.log2(cleaned_df['baseMean'] + 1)

# Perform PCA on log-transformed baseMean values
pca = PCA(n_components=2)
components = pca.fit_transform(cleaned_df[['log_baseMean']])

# Create a scatter plot of PCA results
plt.figure(figsize=(8, 6))
plt.scatter(components[:, 0], components[:, 1], alpha=0.7, c='blue')
plt.xlabel('Principal Component 1 (PC1)')
plt.ylabel('Principal Component 2 (PC2)')
plt.title('PCA of Gene Expression')

# Save the PCA plot as an image
plt.savefig('pca_plot.png', dpi=300, bbox_inches='tight')
print("PCA plot saved as 'pca_plot.png'.")

# Show the plot
plt.show()
