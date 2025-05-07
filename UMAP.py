import pandas as pd
import umap
import matplotlib.pyplot as plt
import numpy as np

# Load the cleaned dataset
cleaned_df = pd.read_csv("cleaned_differential_expression_results.csv")

# Log-transform baseMean for dimensionality reduction
cleaned_df['log_baseMean'] = np.log2(cleaned_df['baseMean'] + 1)

# Perform UMAP on log-transformed baseMean values
reducer = umap.UMAP(random_state=42)
embedding = reducer.fit_transform(cleaned_df[['log_baseMean']])

# Create a scatter plot of UMAP results
plt.figure(figsize=(8, 6))
plt.scatter(embedding[:, 0], embedding[:, 1], alpha=0.7, c='blue')
plt.xlabel('UMAP Dimension 1')
plt.ylabel('UMAP Dimension 2')
plt.title('UMAP of Gene Expression')

# Save the UMAP plot as an image
plt.savefig('umap_plot.png', dpi=300, bbox_inches='tight')
print("UMAP plot saved as 'umap_plot.png'.")

# Show the plot
plt.show()
