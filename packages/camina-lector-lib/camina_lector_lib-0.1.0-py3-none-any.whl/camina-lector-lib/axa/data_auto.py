import fitz

from axa.constants import (
    RECT_AXA_AUTO_CONTRATANTE, RECT_AXA_AUTO_DOMICILIO, RECT_AXA_AUTO_ENDOSO, RECT_AXA_AUTO_FORMA_PAGO, RECT_AXA_AUTO_MODELO, SEARCH_AXA_AUTO_COBERTURAS,
    RECT_AXA_AUTO_MONEDA, RECT_AXA_AUTO_MOTOR, RECT_AXA_AUTO_PLACAS, RECT_AXA_AUTO_POLIZA, RECT_AXA_AUTO_RFC, RECT_AXA_AUTO_SERIE,
    RECT_AXA_AUTO_SERVICIO, RECT_AXA_AUTO_TELEFONO, RECT_AXA_AUTO_USO, RECT_AXA_AUTO_VEHICULO, RECT_AXA_AUTO_VIGENCIA_FIN,
    RECT_AXA_AUTO_VIGENCIA_INI, SEARCH_AXA_AUTO_GASTOS, SEARCH_AXA_AUTO_PRIMA_NETA, SEARCH_AXA_AUTO_TASA, SEARCH_AXA_AUTO_TOTAL
) 
from model.poliza import Poliza
from utils.constants import ASEGURADORA_AXA, PERIDO_PAGO_ANUAL, PERIDO_PAGO_CONTADO, RAMO_AUTOS
from utils.string_utils import get_dia_cobro, homologa_endoso, homologa_fecha_vigencia, homologa_forma_pago, homologa_moneda, homologa_periodo_pago, homologa_plan_auto 
from utils.string_utils import quitar_espacios, str_to_float
from utils.utils import pagos_periodos, truncate

def get_data_auto_axa(doc: fitz.Document) -> Poliza:
    page = doc[0] # pagina 1

     #init class poliza
    p = Poliza()
    p.aseguradora = ASEGURADORA_AXA
    p.ramo = RAMO_AUTOS

    p.poliza = page.get_textbox(RECT_AXA_AUTO_POLIZA).strip()

    p.contrante_nombre = quitar_espacios(page.get_textbox(RECT_AXA_AUTO_CONTRATANTE))
    p.contratante_domicilio = quitar_espacios(page.get_textbox(RECT_AXA_AUTO_DOMICILIO))
    p.contratante_rfc = page.get_textbox(RECT_AXA_AUTO_RFC).strip()
    p.contratante_telefono = page.get_textbox(RECT_AXA_AUTO_TELEFONO).strip()
   
    p.fecha_inicio_vigencia = homologa_fecha_vigencia(page.get_textbox(RECT_AXA_AUTO_VIGENCIA_INI))
    p.fecha_fin_vigencia = homologa_fecha_vigencia(page.get_textbox(RECT_AXA_AUTO_VIGENCIA_FIN))
    p.id_moneda = homologa_moneda(page.get_textbox(RECT_AXA_AUTO_MONEDA))
    p.id_pago = homologa_forma_pago(page.get_textbox(RECT_AXA_AUTO_FORMA_PAGO))
    p.id_periodo = homologa_periodo_pago(page.get_textbox(RECT_AXA_AUTO_FORMA_PAGO))
   
    if p.fecha_inicio_vigencia:
        p.dia_cobro = get_dia_cobro(p.fecha_inicio_vigencia)

    p.vehiculo_descripcion = quitar_espacios(page.get_textbox(RECT_AXA_AUTO_VEHICULO))
    p.vehiculo_modelo = page.get_textbox(RECT_AXA_AUTO_MODELO).strip() 
    p.vehiculo_endoso = homologa_endoso(page.get_textbox(RECT_AXA_AUTO_ENDOSO)) 
    p.vehiculo_serie = page.get_textbox(RECT_AXA_AUTO_SERIE).strip()
    p.vehiculo_placas = page.get_textbox(RECT_AXA_AUTO_PLACAS).strip()
    p.vehiculo_uso = page.get_textbox(RECT_AXA_AUTO_USO).strip()
    p.vehiculo_servicio = page.get_textbox(RECT_AXA_AUTO_SERVICIO).strip()
    p.vehiculo_motor = page.get_textbox(RECT_AXA_AUTO_MOTOR).strip()

    coberturasRect = page.search_for(SEARCH_AXA_AUTO_COBERTURAS)
    if(coberturasRect!=[]):
        coberturasRect[0].x0 = 20
        coberturasRect[0].x1 = coberturasRect[0].x1 + 70
        coberturasRect[0].y0 = coberturasRect[0].y0 + 20
        coberturasRect[0].y1 = coberturasRect[0].y1 + 120
        coberturas = quitar_espacios(page.get_textbox(coberturasRect[0]))
        p.vehiculo_plan = homologa_plan_auto(coberturas)
   
    prima_neta_rect = page.search_for(SEARCH_AXA_AUTO_PRIMA_NETA)
    if(prima_neta_rect!=[]):
        prima_neta_rect[0].x0 = prima_neta_rect[0].x0 + 123;
        prima_neta_rect[0].x1 = prima_neta_rect[0].x1 + 164; 
        p.prima_neta = str_to_float(page.get_textbox(prima_neta_rect[0]))

    total_rect = page.search_for(SEARCH_AXA_AUTO_TOTAL)
    if(total_rect!=[]):
        total_rect[0].x0 = total_rect[0].x0 + 123;
        total_rect[0].x1 = total_rect[0].x1 + 164; 
        p.prima_total = str_to_float(page.get_textbox(total_rect[0]))   

    p.prima_inicial = p.prima_total
    p.prima_subsecuente = p.prima_total

     #calcular pago inicial y subsecuente dependiendo del periodo    
    if p.id_periodo != PERIDO_PAGO_ANUAL and p.id_periodo!= PERIDO_PAGO_CONTADO :

        pagos = pagos_periodos(p.id_periodo)
        prima_neta_periodo = truncate(p.prima_neta / pagos)
        
        tasa_financiamiento_rect = page.search_for(SEARCH_AXA_AUTO_TASA)
        tasa_financimiento = 0.0
        if(tasa_financiamiento_rect!=[]):
            tasa_financiamiento_rect[0].x0 = tasa_financiamiento_rect[0].x0 + 123;
            tasa_financiamiento_rect[0].x1 = tasa_financiamiento_rect[0].x1 + 164; 
            tasa_financimiento = str_to_float(page.get_textbox(tasa_financiamiento_rect[0]))

        tasa_financiamiento_periodo =  truncate(tasa_financimiento / pagos)   

        gastos_expedicion_rect = page.search_for(SEARCH_AXA_AUTO_GASTOS)
        gastos_expedicion = 0.0
        if(gastos_expedicion_rect!=[]):
            gastos_expedicion_rect[0].x0 = gastos_expedicion_rect[0].x0 + 123;
            gastos_expedicion_rect[0].x1 = gastos_expedicion_rect[0].x1 + 164; 
            gastos_expedicion =  str_to_float(page.get_textbox(gastos_expedicion_rect[0]))    

        prima_inicial = (prima_neta_periodo + tasa_financiamiento_periodo + gastos_expedicion) * 1.16
        p.prima_inicial = truncate(prima_inicial)
        p.prima_subsecuente = truncate(p.prima_total - p.prima_inicial)

    return p     