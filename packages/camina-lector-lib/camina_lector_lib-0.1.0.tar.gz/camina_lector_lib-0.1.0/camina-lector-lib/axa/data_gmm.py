import fitz

from axa.constants import (RECT_AXA_GMM_CONTRATANTE, RECT_AXA_GMM_CALLE, RECT_AXA_GMM_RFC, RECT_AXA_GMM_TELEFONO, RECT_AXA_GMM_COLONIA, 
RECT_AXA_GMM_CIUDAD,RECT_AXA_GMM_PLAN, RECT_AXA_GMM_POLIZA, RECT_AXA_GMM_VIGENCIA_INI, RECT_AXA_GMM_VIGENCIA_FIN, RECT_AXA_GMM_FORMA_PAGO,
 RECT_AXA_GMM_PRIMA_NETA, RECT_AXA_GMM_GASTOS_EXPEDICION,  RECT_AXA_GMM_PRIMA_TOTAL,RECT_AXA_GMM_COBERTURAS, RECT_AXA_GMM_SUMA_ASEGURADA, 
 RECT_AXA_GMM_DEDUCIBLE, RECT_AXA_GMM_COASEGURO, RECT_AXA_GMM_COASEGURO_TOPE, RECT_AXA_GMM_FECHA_EMISION_INI,
 RECT_AXA_GMM_NOMBRE_ASEGURADO1, RECT_AXA_GMM_NOMBRE_ASEGURADO2, RECT_AXA_GMM_NOMBRE_ASEGURADO3, RECT_AXA_GMM_NOMBRE_ASEGURADO4,
 RECT_AXA_GMM_NOMBRE_ASEGURADO5,RECT_AXA_GMM_PARENTESCO_ASEGURADO1,RECT_AXA_GMM_PARENTESCO_ASEGURADO2,RECT_AXA_GMM_PARENTESCO_ASEGURADO3,
 RECT_AXA_GMM_PARENTESCO_ASEGURADO4,RECT_AXA_GMM_PARENTESCO_ASEGURADO5,RECT_AXA_GMM_CONDUCTO_COBRO,RECT_AXA_FECHA_NACIMIENTO_ASEGURADO1,
 RECT_AXA_FECHA_NACIMIENTO_ASEGURADO2,RECT_AXA_FECHA_NACIMIENTO_ASEGURADO3,RECT_AXA_FECHA_NACIMIENTO_ASEGURADO4,
 RECT_AXA_FECHA_NACIMIENTO_ASEGURADO5)
from model.poliza import Poliza
from model.asegurados import Asegurados
from utils.constants import ASEGURADORA_AXA, RAMO_GMM, PERIDO_PAGO_ANUAL
from utils.string_utils import get_dia_cobro, homologa_forma_pago, homologa_periodo_pago, homologa_sa
from utils.string_utils import quitar_espacios, str_to_float
from utils.utils import pagos_periodos, truncate

def get_data_gmm_axa(doc: fitz.Document) -> Poliza:
    page = doc[0]
    
    a = Asegurados() #init class Asegurados
    p = Poliza() #init class Poliza
    p.aseguradora = ASEGURADORA_AXA
    p.ramo = RAMO_GMM
    
    p.poliza = page.get_textbox(RECT_AXA_GMM_POLIZA).strip()
    
    p.contrante_nombre = quitar_espacios(page.get_textbox(RECT_AXA_GMM_CONTRATANTE))
    p.contratante_domicilio = quitar_espacios(page.get_textbox(RECT_AXA_GMM_CALLE) + page.get_textbox( RECT_AXA_GMM_COLONIA) + " " + page.get_textbox(RECT_AXA_GMM_CIUDAD))
    p.contratante_rfc = quitar_espacios(page.get_textbox(RECT_AXA_GMM_RFC))
    p.contratante_telefono = page.get_textbox(RECT_AXA_GMM_TELEFONO)
    
    p.fecha_inicio_vigencia = page.get_textbox(RECT_AXA_GMM_VIGENCIA_INI)
    p.fecha_fin_vigencia = page.get_textbox(RECT_AXA_GMM_VIGENCIA_FIN)
    p.id_periodo = homologa_periodo_pago(page.get_textbox(RECT_AXA_GMM_FORMA_PAGO))
    p.id_pago = homologa_forma_pago (page.get_textbox(RECT_AXA_GMM_CONDUCTO_COBRO))
    p.fecha_inicio_vigencia = page.get_textbox(RECT_AXA_GMM_FECHA_EMISION_INI)
    
    p.programa = page.get_textbox(RECT_AXA_GMM_PLAN)
    
    
    
    if p.fecha_inicio_vigencia:
        p.dia_cobro = get_dia_cobro(p.fecha_inicio_vigencia)
    
    p.coberturas = quitar_espacios(page.get_textbox(RECT_AXA_GMM_COBERTURAS)).strip()
    p.suma_asegurada = homologa_sa(page.get_textbox(RECT_AXA_GMM_SUMA_ASEGURADA))
    p.deducible = str_to_float(page.get_textbox(RECT_AXA_GMM_DEDUCIBLE))
    p.coaseguro = page.get_textbox(RECT_AXA_GMM_COASEGURO)
    p.coaseguro_tope = homologa_sa(page.get_textbox(RECT_AXA_GMM_COASEGURO_TOPE))
    
    #calcular el pago inicial y subsecuente dependiendo el periodo de pago
    p.prima_neta = str_to_float(page.get_textbox(RECT_AXA_GMM_PRIMA_NETA))
    p.prima_total = str_to_float(page.get_textbox(RECT_AXA_GMM_PRIMA_TOTAL))
    p.prima_inicial =  p.prima_total
    p.prima_subsecuente = p.prima_total
    
    if p.id_periodo != PERIDO_PAGO_ANUAL:
        pagos = pagos_periodos(p.id_periodo)
        
        gastos_expedicion = str_to_float (page.get_textbox(RECT_AXA_GMM_GASTOS_EXPEDICION))
        prima_subsecuente =  (p.prima_total-(gastos_expedicion * 1.16)) / pagos
        prima_inicial = p.prima_total - prima_subsecuente
        
        p.prima_inicial = truncate(prima_inicial)
        p.prima_subsecuente = truncate(prima_subsecuente)
    
    
    #cambio de pagina para tomar los asegurados
    page = doc[1]
    a.nombre_asegurado1= quitar_espacios(page.get_textbox(RECT_AXA_GMM_NOMBRE_ASEGURADO1))
    a.nombre_asegurado2= quitar_espacios(page.get_textbox(RECT_AXA_GMM_NOMBRE_ASEGURADO2))
    a.nombre_asegurado3= quitar_espacios(page.get_textbox(RECT_AXA_GMM_NOMBRE_ASEGURADO3))
    a.nombre_asegurado4= quitar_espacios(page.get_textbox(RECT_AXA_GMM_NOMBRE_ASEGURADO4))
    a.nombre_asegurado5= quitar_espacios(page.get_textbox(RECT_AXA_GMM_NOMBRE_ASEGURADO5))
    
    a.fecha_nacimiento_asegurado1 = quitar_espacios(page.get_textbox(RECT_AXA_FECHA_NACIMIENTO_ASEGURADO1))
    a.fecha_nacimiento_asegurado2 = quitar_espacios(page.get_textbox(RECT_AXA_FECHA_NACIMIENTO_ASEGURADO2))
    a.fecha_nacimiento_asegurado3 = quitar_espacios(page.get_textbox(RECT_AXA_FECHA_NACIMIENTO_ASEGURADO3))
    a.fecha_nacimiento_asegurado4 = quitar_espacios(page.get_textbox(RECT_AXA_FECHA_NACIMIENTO_ASEGURADO4))
    a.fecha_nacimiento_asegurado5 = quitar_espacios(page.get_textbox(RECT_AXA_FECHA_NACIMIENTO_ASEGURADO5))

    a.parentesco_asegurado1 = quitar_espacios(page.get_textbox(RECT_AXA_GMM_PARENTESCO_ASEGURADO1))
    a.parentesco_asegurado1 = quitar_espacios(page.get_textbox(RECT_AXA_GMM_PARENTESCO_ASEGURADO2))
    a.parentesco_asegurado1 = quitar_espacios(page.get_textbox(RECT_AXA_GMM_PARENTESCO_ASEGURADO3))
    a.parentesco_asegurado1 = quitar_espacios(page.get_textbox(RECT_AXA_GMM_PARENTESCO_ASEGURADO4))
    a.parentesco_asegurado1 = quitar_espacios(page.get_textbox(RECT_AXA_GMM_PARENTESCO_ASEGURADO5))

    return p
        
        
        
    
    
    
    
    