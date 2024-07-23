import fitz

from mapfre.constants import (RECT_MAPFRE_HOGAR_CONTRATANTE, RECT_MAPFRE_HOGAR_DOMICILIO, RECT_MAPFRE_HOGAR_RFC, RECT_MAPFRE_HOGAR_CP,
RECT_MAPFRE_HOGAR_TELEFONO, RECT_MAPFRE_HOGAR_POLIZA, RECT_MAPFRE_HOGAR_VIGENCIA_INI, 
RECT_MAPFRE_HOGAR_VIGENCIA_FIN, RECT_MAPFRE_HOGAR_GASTOS_EXPEDICION, RECT_MAPFRE_HOGAR_PRIMA_TOTAL,
RECT_MAPFRE_HOGAR_FORMA_PAGO, RECT_MAPFRE_HOGAR_MONEDA, RECT_MAPFRE_HOGAR_CONDUCTO_COBRO, RECT_MAPFRE_HOGAR_PRIMA_NETA,
RECT_MAPFRE_HOGAR_PAGO_FRACCIONADO)
from model.poliza import Poliza
from utils.constants import ASEGURADORA_MAPFRE, RAMO_CASAS, PERIDO_PAGO_CONTADO
from utils.string_utils import get_dia_cobro, homologa_forma_pago, homologa_moneda, homologa_periodo_pago
from utils.string_utils import quitar_espacios, str_to_float
from utils.utils import pagos_periodos, truncate

#sirve para caratula de polizas y para renovaciones
def get_data_casas_mapfre(doc: fitz.Document) -> Poliza:
    page = doc[0] #ingresamos a la primera pagina de la poliza
    
    p = Poliza()#iniciamos la clase poliza
    p.aseguradora = ASEGURADORA_MAPFRE
    p.ramo = RAMO_CASAS
    
    p.poliza = page.get_textbox(RECT_MAPFRE_HOGAR_POLIZA).strip()
    
    p.contrante_nombre = quitar_espacios(page.get_textbox(RECT_MAPFRE_HOGAR_CONTRATANTE))
    p.contratante_domicilio = quitar_espacios(page.get_textbox(RECT_MAPFRE_HOGAR_DOMICILIO) + " " + page.get_textbox(RECT_MAPFRE_HOGAR_CP))
    p.contratante_rfc = quitar_espacios(page.get_textbox(RECT_MAPFRE_HOGAR_RFC))
    p.contratante_telefono = page.get_textbox(RECT_MAPFRE_HOGAR_TELEFONO)
    
    p.fecha_inicio_vigencia = page.get_textbox(RECT_MAPFRE_HOGAR_VIGENCIA_INI)
    p.fecha_fin_vigencia = page.get_textbox(RECT_MAPFRE_HOGAR_VIGENCIA_FIN)
    p.id_pago = homologa_forma_pago(page.get_textbox(RECT_MAPFRE_HOGAR_CONDUCTO_COBRO))
    
    if p.fecha_inicio_vigencia:
        p.dia_cobro = get_dia_cobro(p.fecha_inicio_vigencia)
    
    p.id_periodo = homologa_periodo_pago(page.get_textbox(RECT_MAPFRE_HOGAR_FORMA_PAGO))
    p.id_moneda = homologa_moneda(page.get_textbox(RECT_MAPFRE_HOGAR_MONEDA))
    pago_fraccionado = str_to_float(page.get_textbox(RECT_MAPFRE_HOGAR_PAGO_FRACCIONADO))
    
    #obteniendo el pago si es de CONTADO
    p.prima_neta = str_to_float(page.get_textbox(RECT_MAPFRE_HOGAR_PRIMA_NETA))
    p.prima_total = str_to_float(page.get_textbox(RECT_MAPFRE_HOGAR_PRIMA_TOTAL))
    
    p.prima_inicial = p.prima_total
    p.prima_subsecuente = p.prima_total
    
    #sacando pago fraccionado
    if p.id_periodo != PERIDO_PAGO_CONTADO:
        pagos = pagos_periodos(p.id_periodo)
        
        gastos_expedicion = str_to_float(page.get_textbox(RECT_MAPFRE_HOGAR_GASTOS_EXPEDICION))
        
        prima_subsecuente = ((p.prima_neta + pago_fraccionado) *1.16) / pagos
        prima_inicial = prima_subsecuente + (gastos_expedicion * 1.16)
        
        p.prima_inicial = truncate(prima_inicial)
        p.prima_subsecuente = truncate(prima_subsecuente)
    
    return p
        
        