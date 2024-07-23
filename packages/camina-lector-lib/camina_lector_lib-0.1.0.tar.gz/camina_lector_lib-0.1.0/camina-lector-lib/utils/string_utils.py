from utils.constants import MEDIO_COBRO_AGE, MEDIO_COBRO_MD, MEDIO_COBRO_TDC, MEDIO_COBRO_TDD, MONEDA_PESO, MONEDA_UDI, MONEDA_USD, PERIDO_PAGO_ANUAL, PERIDO_PAGO_BIMESTRAL, PERIDO_PAGO_CONTADO, PERIDO_PAGO_MENSUAL, PERIDO_PAGO_SEMESTRAL, PERIDO_PAGO_TRIMESTRAL


MES_CORTO = ["ENE", "FEB", "MAR", "ABR", "MAY", "JUN", "JUL", "AGO", "SEP", "OCT", "NOV", "DIC"]
MES_LARGO = ["ENERO", "FEBRERO", "MARZO", "ABRIL", "MAYO", "JUNIO", "JULIO", "AGOSTO", "SEPTIEMBRE", "OCTUBRE", "NOVIEMBRE", "DICIEMBRE"]

"""
    se envia la fecha en formato ejemplo '01/ENE/2024'
    regresa la fecha en formato '01/01/2024'
"""
def homologa_fecha_vigencia(fecha: str) -> str:
    fecha = fecha.strip().upper() # quitar espacios izq y derecha y convertir a mayusculas
    afecha = fecha.split("/")
    
    if len(afecha) < 3:
        return ""
    
    mes = MES_CORTO.index(afecha[1]) + 1

    if mes < 10:
        mes = "0" + str(mes)

    return afecha[0] + "/" + str(mes) + "/" + afecha[2]

"""
    se envia la fecha en formato ejemplo '21 DE MARZO DE 2024' 
    regresa la fecha en formato '21/03/2024'
"""
def homologa_fecha_nacimiento(fecha: str) -> str:
    fecha = fecha.strip().upper().replace("DE ", "") # quitar espacios izq y derecha y convertir a mayusculas y replace DE
    afecha = fecha.split(" ")
    
    if len(afecha) < 3:
        return ""
    
    mes = MES_LARGO.index(afecha[1]) + 1

    if mes < 10:
        mes = "0" + str(mes)

    return afecha[0] + "/" + str(mes) + "/" + afecha[2]

"""
    se envia la moneda como String ejemplo PESOS 
    regresa un entero identificador de la moneda como esta en la base de datos
    PESOS = 1, USD = 2, UDI = 3
"""
def homologa_moneda(moneda: str) -> int:
    moneda = moneda.strip().upper() # quitar espacios izq y derecha y convertir a mayusculas
    
    if 'PESO' in moneda or 'NACIONAL' in moneda or 'MXN' in moneda:
        return MONEDA_PESO
    
    if 'DOLAR' in moneda or 'USD' in moneda:
        return MONEDA_USD

    if 'UDI' in moneda:
        return MONEDA_UDI
   
"""
    se envia el periodo como string ejemplo 'MENSUAL' 
    regresa un entero identificador del periodo como esta en la base de datos
    MENSUAL = 1, TRIMESTRAL = 2, SEMESTRAL = 3, ANUAL = 4, CONTADO = 5, BIMESTRAL = 6
"""    
def homologa_periodo_pago(periodo: str) -> int:
    periodo = periodo.strip().upper() # quitar espacios izq y derecha y convertir a mayusculas
    
    if "MENSUAL" in periodo:
        return PERIDO_PAGO_MENSUAL

    if "TRIMESTRAL" in periodo:
        return PERIDO_PAGO_TRIMESTRAL
    
    if "SEMESTRAL" in periodo:
        return PERIDO_PAGO_SEMESTRAL
    
    if "ANUAL" in periodo:
        return PERIDO_PAGO_ANUAL
    
    if "CONTADO" in periodo:
        return PERIDO_PAGO_CONTADO
    
    if "BIMESTRAL" in periodo:
        return PERIDO_PAGO_BIMESTRAL

    return  0   

"""
    se envia el pago como string ejemplo 'MASTERCARD' 
    regresa un entero identificador del pago como esta en la base de datos
    TDC = 1, TDD = 2, AGE = 3, MD = 4, NOM = 5, SIN = 6
"""   
def homologa_forma_pago(pago:str) -> int:
    pago = pago.strip().upper()
    
    if "AMEX" in pago or "MASTERCARD" or "CREDITO" in pago:
        return MEDIO_COBRO_TDC
    
    if "DÉBITO" in pago or "DEBITO" in pago:
        return MEDIO_COBRO_TDD
    
    if "EFECTIVO" in pago:
        return MEDIO_COBRO_MD
    
    if "AGENTE" in pago or "CARGO" in pago:
        return MEDIO_COBRO_AGE

    return 0

def homologa_endoso(endoso: str) ->str:
    endoso = endoso.strip().upper()
    if "APLICA" in endoso:
        return "0001"
    
    return endoso
"""
    se envia un plazo de pago como string ejemplo 10 años
    regresa numero de años del plazo ejemplo 10
"""
def homologa_plazo_pago(plazo: str) -> int:
    anios = 0
    plazo = plazo.strip().upper().replace("AÑOS", "")
    try:
        anios = int(plazo)
    except:
        anios = 0
        
    return anios

def homologa_programa_axa(programa: str, plazo: int) -> str:
    programa = programa.strip().upper()

    if "PROTGT" in programa:
        programa = "VPL "
        if plazo>0:
            programa = programa + str(plazo) + " AÑOS" 
    
    return programa

"""
    se quitan los espacios y saltos de linea de una cadena
""" 
def quitar_espacios(cadena : str) -> str:
    cadena = cadena.replace("\n", " ").strip()
    return " ".join(cadena.split())

"""
    se envia una fecha como string ejemplo '05/06/2024' 
    regresa la primera posicion de la fecha 05 como dia de cobro
""" 

def get_dia_cobro(fecha: str) -> int:
    afecha = fecha.split("/")
    
    if len(afecha) < 3:
        return ""
    
    return int(afecha[0])
"""
    se envia una cadena y la convierte a numero flotante
"""
def str_to_float(cadena:str) -> float:
    cadena = cadena.replace(",", "").replace("$", "").replace("M.N", "").replace("M.N.", "").strip()
    if cadena:
        return float(cadena)
    else:
        return 0.0
    
"""
    se envia una cadena y en base a las coberturas devuelve el plan
"""    
def homologa_plan_auto(coberturas: str) -> str:
    plan = "NO"
    RT = False
    DM = False
    coberturas = coberturas.upper()

    if "ROBO TOTAL" in coberturas:
        RT = True
    if "DAÑOS MATERIALES" in coberturas:
        DM = True

    if RT and DM:
        plan = "AMPLIA"

    if RT and not DM:
        plan = "LIMITADA"

    if not RT and not DM:
        plan = "RC"

    return plan
        

""""
    se envia una cadena y le quita simbolos de pesos a la suma asegurada
"""
def homologa_sa(cadena:str) -> str:
    return  cadena.replace("M.N", "").replace("$", "").replace("M.N.", "").strip()
    
"""
    se envia el nombre completo y regresa si es persona fisica o moral
"""
def tipo_persona(nombre_completo: str) -> int:
    persona = False
    nombre_completo = nombre_completo.upper()
    sociedades =  [" S. ", " S "," C.S."," C.S"," CS"," C."," C "," R.L."," R.L"," RL"," S.A."," S.A"," SA "," S.C.", " S.C", " SC ",
            " S.A.S.", " S.A.S", " S.AS", " SAS ", " S.R.L.", " S.R.L", " S.RL", " SRL ", " S.A.B.", " S.AB", " SAB ", " AC ", " AC ", "A.C.", " A.C "]
    c = 0
    while c < len(sociedades) and not persona: 
        if sociedades[c] in nombre_completo:
            persona= True

        c+=1    
    
    return 2 if persona else 1
"""
    se envia un nombre completo con una coma si es persona fisica quita la coma e inverierte el nombre
    regresa la cadena con el nombre correcto
"""
def invertir_nombre(nombre: str) -> str:
    if tipo_persona(nombre_completo=nombre) == 1:
        nombres = nombre.split(",")
        if len(nombres)>1:
            nombre = nombres[1] + " " + nombres[0]

    return nombre        

"""
    se envia un nombre completo sea fisica o moral y separa por nombre y apellido 
"""	
def separar_nombre_completo(nombre_completo: str):
    articulos = ["A","Y","DEL","LAS","LOS","DE","LA","DA","DO","DOS","SAN","SANTA","I","VAN","VON", "O", "MAC", "DI", "D"]
    separate = nombre_completo.upper().split(" ")
    nombres = "" 
    apellidos = ""
    names = []

    prev = "";
    c = 0;
    len_separate = len(separate)

    for token in separate:
        
        if token == "Y" and len(names)>=3:
            union = ""
            x = range(c, len_separate) 
            for d in x:
                union += separate[d] + " " 
        
        if token in articulos:
            prev += token + " "
        else:
            names.append(prev + token)
            prev = ""    

        c+=1
	
    len_names = len(names)
    if len_names == 1: 
        nombres = names[0]
        apellidos = "" 
    elif len_names ==2:
        nombres = names[0]
        apellidos = names[1]        
    elif len_names == 3:
        nombres = names[0] + " " + names[1]
        apellidos = names[2]        
    else:    
        apellidos = names[len_names-2] + " " + names[len_names-1]
        names.pop()
        names.pop()
        nombres = ' '.join(names)
        

    return nombres, apellidos