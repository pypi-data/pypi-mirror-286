from calendar import isleap
from datetime import datetime
from dateutil.relativedelta import relativedelta

from utils.constants import PERIDO_PAGO_ANUAL, PERIDO_PAGO_BIMESTRAL, PERIDO_PAGO_CONTADO, PERIDO_PAGO_MENSUAL, PERIDO_PAGO_SEMESTRAL, PERIDO_PAGO_TRIMESTRAL

def calcular_ultimo_pago(fecha_vigencia: str, plazo_pago: int, periodo: int) -> str:
   meses = 0
   
   if periodo ==  PERIDO_PAGO_MENSUAL:
       meses = 1

   if periodo ==  PERIDO_PAGO_BIMESTRAL:
       meses =  2

   if periodo ==  PERIDO_PAGO_TRIMESTRAL:
       meses = 3

   if periodo ==  PERIDO_PAGO_SEMESTRAL:
       meses = 6

   if periodo ==  PERIDO_PAGO_ANUAL or periodo == PERIDO_PAGO_CONTADO:
       meses = 12    

   plazo = plazo_pago * 12 - meses 
   fv = datetime.strptime(fecha_vigencia, '%d/%m/%Y').date()
    
   return (fv + relativedelta(months=plazo)).strftime('%d/%m/%Y')
 


   

