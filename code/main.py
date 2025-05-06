import os
from pandas import read_excel
from plots import generate_bivariate_plots # change in capsule

''' 
TO BE SET AS FILE TO RUN IN THE CAPSULE
Note: all imports in the imported modules to GUI libraries such as webview and tkinter should be commented in the capsule
'''

## Read the table
df = read_excel(os.path.join(os.path.abspath(os.path.dirname(__file__)),"../data/spettri_QEPAS_v0.2.xlsx")) # change in capsule
df.columns = df.columns.astype(str)

## Show Bivariate Graphs
x_var = "8.0126"
y_var = "9.0877"
assert x_var in df.columns and y_var in df.columns
column_headers = list(df.columns.values)
typology=str(column_headers[1])
fig = generate_bivariate_plots(df, x_var, y_var, typology)
fig.savefig(os.path.join(os.path.abspath(os.path.dirname(__file__)),"../results/bivariate_plot.png")) # change in capsule

## Data Removal


## SVN Pre-Processing


## Principal Component Analysis
