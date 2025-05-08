import scipy
import seaborn as sns
import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from pandas import DataFrame
from sklearn.preprocessing import scale
from scipy.signal import savgol_filter
from sklearn.decomposition import PCA
from matplotlib.ticker import MaxNLocator

# Generate a grid of plots: histograms, KDE, correlation heatmap, and scatterplot
def generate_bivariate_plots(df: DataFrame, x_var, y_var, typology):
    fig, axs=plt.subplots(ncols=2, nrows=2, figsize=(20, 14))
    fig.suptitle('Bivariate Plots')
    sns.set_style("whitegrid")
    sns.histplot(ax=axs[0,0], data=df, x=x_var, hue=typology) 
    sns.histplot(ax=axs[0,1], data=df, x=x_var, hue=typology, kde=True, stat='density')
    sns.displot(df, x=x_var, hue = typology, kind = 'kde')
    numeric_data = df.select_dtypes(include=[np.number])
    sns.heatmap(numeric_data.corr(), annot=False, cmap='Reds', vmin=-1, vmax=1, ax=axs[1,0])
    sns.scatterplot(data=df, x=x_var, y=y_var, hue = typology, ax=axs[1,1])
    sns.set_style("whitegrid")
    fig.tight_layout()
    return fig

# Interactive 2D scatterplot
def generate_bivariate_html_scatter(df: DataFrame, x_var, y_var, typology):
    return px.scatter(df, x=x_var, y=y_var, color=typology)

# Interactive multivariate scatterplots with different color and size mappings
def generate_multivariate_html_scatters(df: DataFrame, x_var, y_var, size, typology):
    fig1 = px.scatter(df, x=x_var, y=y_var, color=typology, size=size) 
    fig2 = px.scatter(df, x=x_var, y=y_var, color=size)  
    return fig1, fig2

# Remove row based on ID column
def remove_row(df: DataFrame, row_value):
    column_headers = list(df.columns.values)
    ID=column_headers[0]
    IDrighe = df[ID].to_numpy()
    nrighe=len(IDrighe)
    for x in range (nrighe) :
        if str(IDrighe[x])==str(row_value):
            index=x
    return df.drop(df.index[index])

# Remove column by name
def remove_column(df: DataFrame, column_value):
    column_headers=list(df.columns.values)
    for y in range (len(column_headers)):
        if str(column_headers[y])==str(column_value):
            val=y
    return df.drop(df.columns[val], axis=1)

# Autoscaling: standardize to mean=0, std=1
def compute_autoscaling(df: DataFrame):
    scaled_values = scale(df.values)
    scaled_df = pd.DataFrame(scaled_values, columns=df.columns, index=df.index)
    return scaled_df

# Mean centering: subtract column mean
def compute_meancentering(df: DataFrame):
    return df.apply(lambda x: x-x.mean()) 

# Standard Normal Variate (SNV) transformation: row-wise normalization
def compute_snv(input_data: np.ndarray):
    output_data = np.zeros_like(input_data)
    for i in range(input_data.shape[0]):
        output_data[i,:] = (input_data[i,:] - np.mean(input_data[i,:])) / np.std(input_data[i,:])
    return output_data

# Savitzky-Golay smoothing
def compute_savitzky_golay(df: DataFrame):
    return savgol_filter(df, 7, polyorder = 2, deriv=0)

# Plot original and preprocessed data
def generate_preprocessing_plot(original_data: np.ndarray, processed_data: np.ndarray, x_axis_labels, title: str):
    fig, (ax1, ax2) = plt.subplots(2,figsize=(15,15))
    ax1.plot(x_axis_labels,  original_data.T)
    ax1.set_title('Original data')
    ax2.plot(x_axis_labels,  processed_data.T)
    ax2.set_title(title)
    ax1.xaxis.set_major_locator(MaxNLocator(nbins=20, prune='both'))
    ax2.xaxis.set_major_locator(MaxNLocator(nbins=20, prune='both'))
    fig.tight_layout()
    return fig

# Merge two dataframes using the first column of the second (e.g., "Samples") as key
def fuse_data(left, right):
    column_headers = list(right.columns.values)
    ID=str(column_headers[0])
    return pd.merge(left, right, on=[ID])

# Perform PCA on numeric data (excluding first two columns)
def compute_pca(n_components: int, df: DataFrame):
    numeric_data=df.drop(df.columns[[0,1]], axis=1)
    numeric_data.columns=numeric_data.columns.astype(str)
    pca = PCA(n_components)
    transformed_data = pca.fit_transform(numeric_data)
    return pca, transformed_data

# Plot PCA variance explained
def generate_scree_plots(pca: PCA):
    cumulative_variance = np.cumsum(pca.explained_variance_ratio_)
    pc_values = np.arange(1, pca.n_components_ + 1)
    fig1, ax1 = plt.subplots()
    ax1.plot(pc_values, pca.explained_variance_ratio_, 'ro-', linewidth=2)
    ax1.set_title('Scree Plot - Individual Variance')
    ax1.set_xlabel('Principal Component')
    ax1.set_ylabel('Proportion of Variance Explained')
    fig1.tight_layout()
    fig2, ax2 = plt.subplots()
    ax2.plot(pc_values, cumulative_variance, 'ro-', linewidth=2)
    ax2.set_title('Scree Plot - Cumulative Variance')
    ax2.set_xlabel('Principal Component')
    ax2.set_ylabel('Cumulative Proportion of Variance Explained')
    fig2.tight_layout()
    return fig1, fig2

# Create PCA scores and loadings DataFrames
def get_scores_and_loadings(pca: PCA, transformed_data: np.ndarray, df: DataFrame):
    non_feature_cols = df.columns[:2].tolist()
    feature_cols = df.columns[2:]
    pc_names = [f"PC{i+1}" for i in range(pca.n_components_)]
    scores_df = pd.DataFrame(transformed_data, columns=pc_names, index=df.index)
    for col in reversed(non_feature_cols):
        scores_df.insert(0, col, df[col].values)
    loadings_df = pd.DataFrame(pca.components_.T, columns=pc_names, index=feature_cols)
    loadings_df["Attributes"] = loadings_df.index
    return scores_df, loadings_df

# 2D interactive PCA scatterplots (scores and loadings)
def generate_pca_html_2d_scatters(scores: DataFrame, loadings: DataFrame, class_column: str, pc_x: str, pc_y: str):
    fig1 = px.scatter(scores, x=pc_x, y=pc_y, color=class_column, hover_data=[class_column], hover_name=scores.index) 
    fig1.update_xaxes(zeroline=True, zerolinewidth=1, zerolinecolor='Black')
    fig1.update_yaxes(zeroline=True, zerolinewidth=1, zerolinecolor='Black')
    fig1.update_layout(height=600, width=800, title_text='Scores Plot colored by'+ class_column)
    fig2 = px.scatter(loadings, x=pc_x, y=pc_y, text="Attributes")
    fig2.update_xaxes(zeroline=True, zerolinewidth=1, zerolinecolor='Black')
    fig2.update_yaxes(zeroline=True, zerolinewidth=1, zerolinecolor='Black')
    fig2.update_traces(textposition='top center')
    fig2.update_layout(height=600, width=800, title_text='Loadings Plot')
    return fig1, fig2

# 3D interactive PCA scatterplot (scores only)
def generate_pca_html_3d_scatters(scores: DataFrame, class_column: str, pc_x: str, pc_y: str, pc_z: str):
    fig = px.scatter_3d(scores, x=pc_x, y=pc_y, z=pc_z,color=class_column, hover_data=[class_column], hover_name=scores.index)
    return fig

# Calculate Hotelling’s T2 and Q-residuals for outlier detection
def detect_outliers(df: DataFrame, scores: DataFrame, loadings: DataFrame, class_column: str, n_components: int):
    X1=df.drop(df.columns[[0,1]], axis=1)
    X1.columns = X1.columns.astype(str)
    T = scores.iloc[:,2:n_components+2]
    P = loadings.iloc[:,0:n_components]
    Err = X1 - np.dot(T,P.T)
    Q = np.sum(Err**2, axis=1)
    Tsq = np.sum((T/np.std(T, axis=0))**2, axis=1)
    conf = 0.95 
    Tsq_conf = mean_confidence_interval(Tsq.values, confidence=conf)
    Tsq_conf = Tsq_conf[2]
    Q_conf = mean_confidence_interval(Q.values, confidence=conf)
    Q_conf = Q_conf[2]
    hot_q_data = {'T2': Tsq, 'Qres': Q, str(class_column): df[str(class_column)]}  
    hot_q_data = pd.DataFrame(hot_q_data, index = df.index)
    valori2={}
    valori2[1]= hot_q_data
    normalized_Q = Q / np.max(Q)
    normalized_Tsq = Tsq / np.max(Tsq)
    normalized_hot_q_data = {'T2': normalized_Tsq, 'Qres': normalized_Q, str(class_column): df[str(class_column)]} 
    normalized_hot_q_data = pd.DataFrame(normalized_hot_q_data, index=df.index)
    return hot_q_data, normalized_hot_q_data, Q, Tsq, Q_conf, Tsq_conf

# Compute confidence interval bounds
def mean_confidence_interval(data, confidence):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m, m-h, m+h

# Generate interactive scatterplots for T2 vs Q-residuals (raw and normalized)
def generate_outliers_html_scatters(hot_q_data, normalized_hot_q_data, Q, Tsq, Q_conf, Tsq_conf, class_column):
    fig1 = px.scatter(hot_q_data, x="T2", y="Qres", hover_data={'Sample': (hot_q_data.index)},  color = str(class_column))  
    fig1.add_hline(y=abs(Q_conf),line_dash="dot", line_color='Red')
    fig1.add_vline(x=Tsq_conf,line_dash="dot", line_color='Red')
    fig1.update_traces(textposition='top center')
    fig1.update_layout(height=600, width=800, title_text="Hotelling's T2 vs Q-residuals")
    fig2 = px.scatter(normalized_hot_q_data, x="T2", y="Qres", hover_data={'Sample': (normalized_hot_q_data.index)}, color=str(class_column))
    fig2.add_hline(y=abs(Q_conf / np.max(Q)), line_dash="dot", line_color='Red')
    fig2.add_vline(x=Tsq_conf / np.max(Tsq), line_dash="dot", line_color='Red')
    fig2.update_traces(textposition='top center')
    fig2.update_layout(height=600, width=800, title_text="Normalized Hotelling's T2 vs Q-residuals")
    return fig1, fig2