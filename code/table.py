"""" Developed by Michele Verdi"""

""""Importazione funzioni da altre pagine"""
from print_table import stampaTabelle
from data_removal import passaggiodataremoval
from pre_processing import passaggioPreProcessing
from plots import passaggioscelta_grafici
from exploration import passaggioExploration



def caricamentoTabelle(Dati, n):
    """Funzione per passaggio dati, creata per evitare confusione"""
    """In futuro può essere eliminata senza alcun problema"""
    
    stampaTabelle(Dati,n, "Dati", True)
    passaggiodataremoval(Dati,n)
    passaggioPreProcessing(Dati,n)
    passaggioscelta_grafici(Dati, n)
    passaggioExploration(Dati,n)