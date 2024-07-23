import os
from typing import List
from model.poliza import Poliza
import fitz

from axa.data_auto import get_data_auto_axa
from axa.data_vida import get_data_vida_axa
from axa.data_gmm import get_data_gmm_axa
from mapfre.data_gmm import get_data_gmm_mapfre
from mapfre.data_casas import get_data_casas_mapfre
from core.initial_data import check_aseguradora, check_ramo_axa, check_ramo_mapfre
from utils.constants import ASEGURADORA_AXA, ASEGURADORA_MAPFRE, RAMO_AUTOS, RAMO_GMM, RAMO_VIDA, RAMO_CASAS


def get_info_pdf(file: str) -> Poliza:
    doc = fitz.open(file)
    aseguradora = check_aseguradora(doc)

    if aseguradora == ASEGURADORA_AXA:

        ramo = check_ramo_axa(doc)
        
        if ramo == RAMO_VIDA:
            return get_data_vida_axa(doc)
        elif ramo == RAMO_AUTOS:  
            return get_data_auto_axa(doc)
        elif ramo == RAMO_GMM:
            return get_data_gmm_axa(doc)  
    
    if aseguradora == ASEGURADORA_MAPFRE:
        ramo = check_ramo_mapfre(doc)
    
        if ramo == RAMO_GMM:
            return get_data_gmm_mapfre(doc) 
        elif ramo == RAMO_CASAS:
            return get_data_casas_mapfre(doc)

    doc.close()

def get_list_info_pdf(folder: str) ->  List[Poliza]:
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".pdf"):
                print(file)
                print(get_info_pdf(file=os.path.join(root, file)))