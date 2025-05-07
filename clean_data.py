import pandas as pd

# Load the dataset (replace 'differential_expression_results.csv' with your actual file name)
df = pd.read_csv("differential_expression_results.csv")

# Drop rows with NA in critical columns and where baseMean is zero or less
cleaned_df = df.dropna(subset=['baseMean', 'log2FoldChange', 'padj'])
cleaned_df = cleaned_df[cleaned_df['baseMean'] > 0]

# Save the cleaned data to a new CSV file
cleaned_df.to_csv("cleaned_differential_expression_results.csv", index=False)

# Display a message confirming the save
print("Cleaned dataset has been saved to 'cleaned_differential_expression_results.csv'.")
