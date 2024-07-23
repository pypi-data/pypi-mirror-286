import fitz

from axa.constants import RECT_AXA_RAMO_AUTO, RECT_AXA_RAMO_GMM, RECT_AXA_RAMO_VIDA, SEARCH_AXA_ASEGURADORA
from mapfre.constants import RECT_MAPFRE_HOGAR_RAMO,RECT_MAPFRE_GMM_RAMO,SEARCH_MAPFRE_ASEGURADORA
from utils.constants import ASEGURADORA_AXA, ASEGURADORA_MAPFRE,RAMO_AUTOS, RAMO_GMM, RAMO_VIDA, RAMO_CASAS

def check_aseguradora(doc: fitz.Document) -> int:
    page = doc[0] # pagina 1

    aseguradora = page.search_for(SEARCH_AXA_ASEGURADORA)
    if(aseguradora!=[]):
       return ASEGURADORA_AXA
   
    aseguradora = page.search_for(SEARCH_MAPFRE_ASEGURADORA)
    if(aseguradora!=[]):
        return ASEGURADORA_MAPFRE   
     
    return 0
    

def check_ramo_axa(doc: fitz.Document) -> int:
    page = doc[0] # pagina 1

    ramo = page.get_textbox(RECT_AXA_RAMO_AUTO).strip().upper()
    if "AUTO" in ramo:
        return RAMO_AUTOS
    
    ramo = page.get_textbox(RECT_AXA_RAMO_VIDA).strip().upper()
    if "VIDA" in ramo:
        return RAMO_VIDA
    
    ramo = page.get_textbox(RECT_AXA_RAMO_GMM).strip().upper()
    if "GASTOS" in ramo:
        return RAMO_GMM
    
    return 0

def check_ramo_mapfre(doc: fitz.Document) -> int:
    page = doc[0] #verifica en la pagina 1
    
    ramo = page.get_textbox(RECT_MAPFRE_HOGAR_RAMO).strip().upper()
    if "HOGAR" in ramo:
         return RAMO_CASAS
    
    ramo = page.get_textbox(RECT_MAPFRE_GMM_RAMO).strip().upper()
    if "PROTECCION" in ramo:
        return RAMO_GMM

    return 0




