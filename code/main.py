import os
from pandas import read_excel
from core import *

## TO BE SET AS FILE TO RUN IN THE CAPSULE

base_path = os.path.abspath(os.path.dirname(__file__))
data_path = os.path.join(base_path, "..", "data")
results_path = os.path.join(base_path, "..", "results")
if not os.path.exists(results_path):
    os.makedirs(results_path)

# NOTE: when running in the capsule environment, replace the path logic above with:
# data_path = "/data"
# results_path = "/results"

## === Configuration Section ===
## Modify the following parameters to run the analysis on your dataset
# Name of the input Excel file (must be placed in the /data folder)
input_xlsx = "spettri_QEPAS_v0.2.xlsx"
# Column names (as strings) to use for bivariate scatter plot (must match headers in Excel file)
x_var = "8.0126"
y_var = "9.0877"
# ID of the row and name of the column to remove from the dataset (as strings)
# Row is expected to match an entry in the first column
row = "2"
column = "8.0126"
# Number of principal components to retain in PCA
n_components = 6
# Name of the column containing class labels for color coding in PCA and outlier plots
class_column = "Class"
# Principal components to use for 2D PCA score/loadings plots
pc_x = "PC1"
pc_y = "PC2"
## ==================================

## Read the table
print("Reading Excel file...")
df = read_excel(os.path.join(data_path, input_xlsx))
df.columns = df.columns.astype(str)
print("Data loaded successfully with shape:", df.shape)

## Show Bivariate Graphs
assert x_var in df.columns and y_var in df.columns
column_headers = list(df.columns.values)
typology = str(column_headers[1])
print(f"Generating bivariate plot for '{x_var}' vs '{y_var}'...")
fig = generate_bivariate_plots(df, x_var, y_var, typology)
bivariate_path = os.path.join(results_path, "bivariate_plot.png")
fig.savefig(bivariate_path)
print(f"Bivariate plot saved to: {bivariate_path}")

## Data Removal
print(f"Removing row with ID = {row} and column = {column}...")
df = remove_row(df, row)
df = remove_column(df, column)
print("Row and column removed. New shape:", df.shape)
rows_cols_removed_path = os.path.join(results_path, "data_rows_cols_removed.xlsx")
df.to_excel(rows_cols_removed_path, index=False)
print(f"Cleaned data saved to: {rows_cols_removed_path}")

## SNV Pre-Processing
print("Applying SNV preprocessing...")
original_data = df.iloc[:, 2:].to_numpy()
pre_processed_data = compute_snv(original_data)
x_axis_labels = df.columns[2:].tolist()
print(f"Generating plot for original and preprocessed data...")
fig = generate_preprocessing_plot(original_data, pre_processed_data, x_axis_labels, 'SNV')
snv_plot_path = os.path.join(results_path, "snv_pre_processing.png")
fig.savefig(snv_plot_path)
print(f"SNV preprocessing plot saved to: {snv_plot_path}")

## Fuse Data
print("Fusing raw and SNV-preprocessed data...")
snv_df = pd.DataFrame(pre_processed_data, columns=x_axis_labels, index=df.index)
snv_df.insert(0, "Samples", df["Samples"].values)
fused_df = fuse_data(df, snv_df)
print("Fused dataset shape:", fused_df.shape)
fused_data_path = os.path.join(results_path, "fused_snv_data.xlsx")
fused_df.to_excel(fused_data_path, index=False)
print(f"Fused dataset saved to: {fused_data_path}")

## Principal Component Analysis
print("Computing PCA with", n_components, "components...")
pca, transformed_data = compute_pca(n_components, fused_df)
fig1, fig2 = generate_scree_plots(pca)
print(f"Generating scree plots...")
scree_individual_path = os.path.join(results_path, "scree-individual-variance.png")
scree_cumulative_path = os.path.join(results_path, "scree-cumulative-variance.png")
fig1.savefig(scree_individual_path)
fig2.savefig(scree_cumulative_path)
print(f"Scree plots saved to: {scree_individual_path}, {scree_cumulative_path}")

print("Extracting PCA scores and loadings...")
scores_df, loadings_df = get_scores_and_loadings(pca, transformed_data, fused_df)
scores_path = os.path.join(results_path, "pca_scores.xlsx")
loadings_path = os.path.join(results_path, "pca_loadings.xlsx")
scores_df.to_excel(scores_path, index=False)
loadings_df.to_excel(loadings_path, index=False)
print(f"PCA scores saved to: {scores_path}")
print(f"PCA loadings saved to: {loadings_path}")

## PCA Plots
fig1, fig2 = generate_pca_html_2d_scatters(scores_df, loadings_df, class_column, pc_x, pc_y)
pca_scores_html_path = os.path.join(results_path, "pca_scores.html")
pca_loadings_html_path = os.path.join(results_path, "pca_loadings.html")
fig1.write_html(pca_scores_html_path, auto_open=False)
fig2.write_html(pca_loadings_html_path, auto_open=False)
print(f"PCA scores HTML plot saved to: {pca_scores_html_path}")
print(f"PCA loadings HTML plot saved to: {pca_loadings_html_path}")

## Outlier Detection
print("Detecting outliers based on Hotelling's T² and Q-residuals...")
hot_q_data, normalized_hot_q_data, Q, Tsq, Q_conf, Tsq_conf = detect_outliers(fused_df, scores_df, loadings_df, class_column, n_components)
print(f"Generating outlier scatter plots...")
fig1, fig2 = generate_outliers_html_scatters(hot_q_data, normalized_hot_q_data, Q, Tsq, Q_conf, Tsq_conf, class_column)
outliers_html_path = os.path.join(results_path, "hotelling_t2_vs-q_residuals.html")
outliers_norm_html_path = os.path.join(results_path, "norm_hotelling_t2_vs-q_residuals.html")
fig1.write_html(outliers_html_path, auto_open=False)
fig2.write_html(outliers_norm_html_path, auto_open=False)
print(f"Outlier plots saved to: {outliers_html_path}, {outliers_norm_html_path}")

print("Processing complete. All results saved in:", results_path)