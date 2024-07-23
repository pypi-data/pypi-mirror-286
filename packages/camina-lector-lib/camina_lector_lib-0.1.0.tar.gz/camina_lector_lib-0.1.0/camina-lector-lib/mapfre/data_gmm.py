import fitz

from mapfre.constants import (RECT_MAPFRE_GMM_CONTRATANTE,RECT_MAPFRE_GMM_PLAN, RECT_MAPFRE_GMM_POLIZA, RECT_MAPFRE_GMM_VIGENCIA_INI,
RECT_MAPFRE_GMM_VIGENCIA_FIN,SEARCH_MAPFRE_GMM_DOMICILIO, SEARCH_MAPFRE_GMM_CP, SEARCH_MAPFRE_GMM_RFC, SEARCH_MAPFRE_GMM_COMODIN,
SEARCH_MAPFRE_GMM_FORMA_DE_PAGO, SEARCH_MAPFRE_GMM_PRIMA_NETA, SEARCH_MAPFRE_GMM_MONEDA, SEARCH_MAPFRE_GMM_GASTOS_EXPEDICION, 
SEARCH_MAPFRE_GMM_PAGO_FRACCIONADO, SEARCH_MAPFRE_GMM_PRIMA_TOTAL)
from model.poliza import Poliza
from utils.constants import  RAMO_GMM, PERIDO_PAGO_CONTADO, ASEGURADORA_MAPFRE
from utils.string_utils import get_dia_cobro, homologa_periodo_pago, homologa_sa, homologa_moneda
from utils.string_utils import quitar_espacios, str_to_float
from utils.utils import pagos_periodos, truncate

def get_data_gmm_mapfre(doc: fitz.Document) -> Poliza:
    page = doc[0] #se obtiene la primera pagina de la poliza
    
    p = Poliza()#init class poliza
    p.aseguradora = ASEGURADORA_MAPFRE
    p.ramo = RAMO_GMM
    
    p.poliza = page.get_textbox(RECT_MAPFRE_GMM_POLIZA).strip()
    
    p.contrante_nombre = quitar_espacios(page.get_textbox(RECT_MAPFRE_GMM_CONTRATANTE))
    rfcRect = page.search_for(SEARCH_MAPFRE_GMM_RFC)
    if rfcRect != []:
       rfcRect[0].x0 = rfcRect[0].x0 + 37
       rfcRect[0].x1 = rfcRect[0].x1 + 175
       p.contratante_rfc = quitar_espacios(page.get_textbox(rfcRect[0]))
    
    cpRect = page.search_for(SEARCH_MAPFRE_GMM_CP)
    if cpRect != []:
        cpRect[0].x0 = cpRect[0].x0 + 25  
        cpRect[0].x1 = cpRect[0].x1 + 125
        cp = (page.get_textbox(cpRect[0]))   
        
    domicilioRect = page.search_for(SEARCH_MAPFRE_GMM_DOMICILIO)
    if domicilioRect != []:
        domicilioRect[0].x0 = domicilioRect[0].x0 + 57
        domicilioRect[0].x1 = domicilioRect[0].x1 + 267
        domicilioRect[0].y1 = rfcRect[0].y1 - 15
        p.contratante_domicilio = quitar_espacios(page.get_textbox(domicilioRect[0]) + " " + page.get_textbox(cpRect[0]))
    
    p.fecha_inicio_vigencia = quitar_espacios(page.get_textbox(RECT_MAPFRE_GMM_VIGENCIA_INI))
    p.fecha_fin_vigencia = quitar_espacios(page.get_textbox(RECT_MAPFRE_GMM_VIGENCIA_FIN))
    p.programa = quitar_espacios(page.get_textbox(RECT_MAPFRE_GMM_PLAN))
    
    if p.fecha_inicio_vigencia:
        p.dia_cobro = get_dia_cobro(p.fecha_inicio_vigencia)
        
    suma_asegurada_rect = page.search_for(SEARCH_MAPFRE_GMM_COMODIN)
    if suma_asegurada_rect != []:
        suma_asegurada_rect[0].x0 = suma_asegurada_rect[0].x0 + 144
        suma_asegurada_rect[0].x1 = suma_asegurada_rect[0].x1+ 191
        p.suma_asegurada = homologa_sa(page.get_textbox(suma_asegurada_rect[0]))
    
    deducibleRect = page.search_for(SEARCH_MAPFRE_GMM_COMODIN)
    if deducibleRect != []:
        deducibleRect[0].x0 = deducibleRect[0].x0 + 257
        deducibleRect[0].x1 = deducibleRect[0].x1+ 284
        p.deducible = str_to_float(page.get_textbox(deducibleRect[0]))
    
    coaseguroRect = page.search_for(SEARCH_MAPFRE_GMM_COMODIN)
    if coaseguroRect != []:
        coaseguroRect[0].x0 = coaseguroRect[0].x0 + 372
        coaseguroRect[0].x1 = coaseguroRect[0].x1+ 354
        p.coaseguro = page.get_textbox(coaseguroRect[0])
    
    coaseguro_tope_rect = page.search_for(SEARCH_MAPFRE_GMM_COMODIN)
    if coaseguro_tope_rect != []:
        coaseguro_tope_rect[0].x0 = coaseguro_tope_rect[0].x0 + 417
        coaseguro_tope_rect[0].x1 = coaseguro_tope_rect[0].x1+ 436
        p.coaseguro_tope = page.get_textbox(coaseguro_tope_rect[0])
    
    #obteniendo variables de pag 2
    page=doc[1]
    
    forma_pago_Rect = page.search_for(SEARCH_MAPFRE_GMM_FORMA_DE_PAGO)
    if (forma_pago_Rect != []):
        forma_pago_Rect[0].x0 = forma_pago_Rect[0].x0 +90
        forma_pago_Rect[0].x1 = forma_pago_Rect[0].x1 +179  
        p.id_periodo = homologa_periodo_pago(page.get_textbox(forma_pago_Rect[0]))
    
    moneda_Rect = page.search_for(SEARCH_MAPFRE_GMM_MONEDA)
    if  moneda_Rect != []:
        moneda_Rect[0].x0 = moneda_Rect[0].x0 +193
        moneda_Rect[0].x1 = moneda_Rect[0].x1 +207
        p.id_moneda = homologa_moneda(page.get_textbox(moneda_Rect[0]))
    
    
        
    pago_fraccionado_Rect = page.search_for(SEARCH_MAPFRE_GMM_PAGO_FRACCIONADO)
    if pago_fraccionado_Rect != []:
        pago_fraccionado_Rect[0].x0 += 165
        pago_fraccionado_Rect[0].x1 += 74
        pago_fraccionado_Rect[0].y0 += 14
        pago_fraccionado_Rect[0].y1 += 14
        pago_fraccionado = str_to_float(page.get_textbox(pago_fraccionado_Rect[0]))
        
    
    #obteniendo el pago si es contado 
    prima_neta_Rect = page.search_for(SEARCH_MAPFRE_GMM_PRIMA_NETA) 
    if prima_neta_Rect != []:
        prima_neta_Rect[0].x0 = prima_neta_Rect[0].x0 +64
        prima_neta_Rect[0].x1 = prima_neta_Rect[0].x1 +157
        p.prima_neta = str_to_float(page.get_textbox(prima_neta_Rect[0]))
    
    prima_total_Rect = page.search_for(SEARCH_MAPFRE_GMM_PRIMA_TOTAL)
    if prima_total_Rect != []:
        prima_total_Rect[0].x0 +=70
        prima_total_Rect[0].x1 +=149
        p.prima_total = str_to_float(page.get_textbox(prima_total_Rect[0]))
    
    p.prima_inicial = p.prima_total
    p.prima_subsecuente = p.prima_total
    
    #Si es pago fraccionado
    if p.id_periodo != PERIDO_PAGO_CONTADO:
        pagos = pagos_periodos(p.id_periodo)
        
        gastos_expedicion_Rect = page.search_for(SEARCH_MAPFRE_GMM_GASTOS_EXPEDICION)
        if gastos_expedicion_Rect != []:
            gastos_expedicion_Rect[0].x0 +=119
            gastos_expedicion_Rect[0].x1 +=78 
            gastos_expedicion = str_to_float(page.get_textbox(gastos_expedicion_Rect[0]))
        
        prima_subsecuente = ((p.prima_neta + pago_fraccionado)*1.16)/pagos
        prima_inicial = prima_subsecuente + (gastos_expedicion * 1.16)
        #prima_inicial = p.prima_total - prima_subsecuente
        
        p.prima_inicial = truncate(prima_inicial)
        p.prima_subsecuente = truncate(prima_subsecuente)
        
    return p
    
    



