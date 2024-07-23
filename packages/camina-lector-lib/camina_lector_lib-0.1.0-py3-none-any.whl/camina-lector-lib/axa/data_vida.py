import fitz

from axa.constants import (
    RECT_AXA_VIDA_CONTRATANTE, RECT_AXA_VIDA_DOMICILIO, RECT_AXA_VIDA_FORMA_PAGO, RECT_AXA_VIDA_MONEDA, RECT_AXA_VIDA_PERIODO_PAGO, SEARCH_AXA_VIDA_SA,
    RECT_AXA_VIDA_PLAZO_PAGO, RECT_AXA_VIDA_POLIZA, RECT_AXA_VIDA_PRIMA_ANUAL_ADICIONAL, RECT_AXA_VIDA_PRIMA_ANUAL_TOTAL,
    RECT_AXA_VIDA_PRIMA_ANUAL_TOTAL_FRACCIONADO, RECT_AXA_VIDA_PRIMA_FRACCIONADO_TOTAL, RECT_AXA_VIDA_PROGRAMA, RECT_AXA_VIDA_RFC,
    RECT_AXA_VIDA_TELEFONO, RECT_AXA_VIDA_TITULAR_FNAC, RECT_AXA_VIDA_TITULAR_NOMBRE, RECT_AXA_VIDA_VIGENCIA_FIN, RECT_AXA_VIDA_VIGENCIA_INI
)
 
from model.poliza import Poliza
from utils.constants import ASEGURADORA_AXA, PERIDO_PAGO_ANUAL, RAMO_VIDA
from utils.fechas_utils import calcular_ultimo_pago
from utils.string_utils import get_dia_cobro, homologa_fecha_nacimiento, homologa_fecha_vigencia, homologa_forma_pago, homologa_moneda, homologa_periodo_pago
from utils.string_utils import homologa_plazo_pago, homologa_programa_axa, quitar_espacios, str_to_float, invertir_nombre

def get_data_vida_axa(doc: fitz.Document) -> Poliza:
    page = doc[0] # pagina 1

      #init class poliza
    p = Poliza()
    p.aseguradora = ASEGURADORA_AXA
    p.ramo = RAMO_VIDA
   
    p.poliza = page.get_textbox(RECT_AXA_VIDA_POLIZA).strip()
   
    p.contrante_nombre = invertir_nombre(quitar_espacios(page.get_textbox(RECT_AXA_VIDA_CONTRATANTE)))
    p.contratante_domicilio = quitar_espacios(page.get_textbox(RECT_AXA_VIDA_DOMICILIO))
    p.contratante_rfc = page.get_textbox(RECT_AXA_VIDA_RFC).strip()
    p.contratante_telefono = page.get_textbox(RECT_AXA_VIDA_TELEFONO).strip()
   
    p.titular_nombre = invertir_nombre(page.get_textbox(RECT_AXA_VIDA_TITULAR_NOMBRE).strip())
    p.titular_fecha_nacimiento = homologa_fecha_nacimiento(page.get_textbox(RECT_AXA_VIDA_TITULAR_FNAC))
  
    p.fecha_inicio_vigencia = homologa_fecha_vigencia(page.get_textbox(RECT_AXA_VIDA_VIGENCIA_INI))
    p.fecha_fin_vigencia = homologa_fecha_vigencia(page.get_textbox(RECT_AXA_VIDA_VIGENCIA_FIN))
    p.id_moneda = homologa_moneda(page.get_textbox(RECT_AXA_VIDA_MONEDA))
    plazo_pago = homologa_plazo_pago(page.get_textbox(RECT_AXA_VIDA_PLAZO_PAGO))
    p.id_pago = homologa_forma_pago(page.get_textbox(RECT_AXA_VIDA_FORMA_PAGO))
    p.id_periodo = homologa_periodo_pago(page.get_textbox(RECT_AXA_VIDA_PERIODO_PAGO))

    p.programa = homologa_programa_axa(programa=page.get_textbox(RECT_AXA_VIDA_PROGRAMA), plazo=plazo_pago)

    rectSA = page.search_for(SEARCH_AXA_VIDA_SA)
    if rectSA!=[] and len(rectSA)>1:
        rectSA[2].y0 = rectSA[2].y1 + 5
        rectSA[2].y1 = rectSA[2].y1 + 13
        p.suma_asegurada = page.get_textbox(rectSA[2]).strip()
        

    #calcular fecha ultimo pago
    if plazo_pago>0:
        p.fecha_ultimo_pago = calcular_ultimo_pago(fecha_vigencia=p.fecha_inicio_vigencia, plazo_pago= plazo_pago, periodo=p.id_periodo)
   
    if p.fecha_inicio_vigencia:
        p.dia_cobro = get_dia_cobro(p.fecha_inicio_vigencia)

    if p.id_periodo == PERIDO_PAGO_ANUAL:
        prima_adicional = str_to_float(page.get_textbox(RECT_AXA_VIDA_PRIMA_ANUAL_ADICIONAL))
        p.prima_total = str_to_float(page.get_textbox(RECT_AXA_VIDA_PRIMA_ANUAL_TOTAL))
        p.prima_inicial = p.prima_total + prima_adicional
        p.prima_subsecuente = p.prima_inicial
    else: 
        p.prima_total = str_to_float(page.get_textbox(RECT_AXA_VIDA_PRIMA_ANUAL_TOTAL_FRACCIONADO))
        p.prima_inicial = str_to_float(page.get_textbox(RECT_AXA_VIDA_PRIMA_FRACCIONADO_TOTAL)) 
        p.prima_subsecuente = p.prima_inicial  

    return p
    