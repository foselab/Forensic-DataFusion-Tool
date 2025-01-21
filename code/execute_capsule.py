from pandas import read_excel, DataFrame
from table import caricamentoTabelle

def main():
    # where to put the data frame
    dataframe_collection = {}
    # open the excel file
    Dati = read_excel("../data/spettri_QEPAS_v0.2.xlsx")
    dataframe_collection[0] = DataFrame(Dati)

    # just to test the reading
    #print(dataframe_collection[0].values)

    caricamentoTabelle(dataframe_collection, 0)



if __name__ == "__main__":
    main()