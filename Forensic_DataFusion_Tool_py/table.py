"""" Developed by Michele Verdi"""

""""Importazione funzioni da altre pagine"""
from Forensic_DataFusion_Tool_py.print_table import stampaTabelle
from Forensic_DataFusion_Tool_py.data_removal import passaggiodataremoval
from Forensic_DataFusion_Tool_py.pre_processing import passaggioPreProcessing
from Forensic_DataFusion_Tool_py.plots import passaggioscelta_grafici
from Forensic_DataFusion_Tool_py.exploration import passaggioExploration



def caricamentoTabelle(Dati, n):
    """Funzione per passaggio dati, creata per evitare confusione"""
    """In futuro può essere eliminata senza alcun problema"""
    
    stampaTabelle(Dati,n, "Dati", True)
    passaggiodataremoval(Dati,n)
    passaggioPreProcessing(Dati,n)
    passaggioscelta_grafici(Dati, n)
    passaggioExploration(Dati,n)
   
    
    
    
    

       
    


    
    
        

   
    
    
        



   
   
    
    
    
   
   
