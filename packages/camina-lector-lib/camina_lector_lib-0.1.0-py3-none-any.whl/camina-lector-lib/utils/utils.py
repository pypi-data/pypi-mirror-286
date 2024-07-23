import math

from utils.constants import PERIDO_PAGO_BIMESTRAL, PERIDO_PAGO_MENSUAL, PERIDO_PAGO_SEMESTRAL, PERIDO_PAGO_TRIMESTRAL

"""
    se envia un periodo como entero y regresa el numero de pagos
    ejemplo 1 mensual regresa 12 pagos
"""

def pagos_periodos(periodo: int) -> int:
    if periodo ==  PERIDO_PAGO_MENSUAL:
        return 12

    if periodo ==  PERIDO_PAGO_TRIMESTRAL:
        return 4

    if periodo ==  PERIDO_PAGO_SEMESTRAL:
        return 2

    if periodo ==  PERIDO_PAGO_BIMESTRAL:
        return 6

    return 1   
"""
    trunca dos digitos de un numero flotante
"""
def truncate(numero: float, digits: int = 2) -> float:
    nbDecimals = len(str(numero).split('.')[1]) 
    if nbDecimals <= digits:
        return numero
    stepper = 10.0 ** digits
    return math.trunc(stepper * numero) / stepper