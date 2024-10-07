"""" Developed by Michele Verdi"""

""""Importazione funzioni da altre pagine"""
from stampa_tabelle import stampaTabelle
from data_removal import passaggiodataremoval
from Pre_Processing import passaggioPreProcessing
from scelta_Grafici import passaggioscelta_grafici
from scelta_Exploration import passaggioExploration



def caricamentoTabelle(Dati, n):
    """Funzione per passaggio dati, creata per evitare confusione"""
    """In futuro può essere eliminata senza alcun problema"""
    
    stampaTabelle(Dati,n, "Dati", True)
    passaggiodataremoval(Dati,n)
    passaggioPreProcessing(Dati,n)
    passaggioscelta_grafici(Dati, n)
    passaggioExploration(Dati,n)
   
    
    
    
    

       
    


    
    
        

   
    
    
        



   
   
    
    
    
   
   
