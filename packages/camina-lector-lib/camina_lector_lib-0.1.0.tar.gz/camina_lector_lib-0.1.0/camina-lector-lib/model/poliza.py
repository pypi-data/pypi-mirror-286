from utils.constants import RAMO_AUTOS, RAMO_GMM, RAMO_VIDA


class Poliza:
    aseguradora: int
    ramo: int
    poliza: str
    programa: str
    
    contrante_nombre: str
    contratante_domicilio: str
    contratante_rfc: str
    contratante_telefono: str
    contratante_correo: str
    

    titular_nombre: str
    titular_fecha_nacimiento: str
   
    fecha_inicio_vigencia: str
    fecha_fin_vigencia: str
    fecha_emision: str
    fecha_ultimo_pago: str

    id_moneda: int
    id_pago: int #conducto de cobro TDC, TDD, Agente
    id_periodo: int #forma de pago, mensual, trimestral
    dia_cobro: int

    prima_neta: float
    prima_total: float
    prima_inicial: float
    prima_subsecuente: float
   
    #solo auto
    vehiculo_descripcion: str
    vehiculo_modelo: str
    vehiculo_endoso: str
    vehiculo_serie: str
    vehiculo_placas: str
    vehiculo_uso: str
    vehiculo_servicio: str
    vehiculo_motor: str
    vehiculo_plan: str

    #Solo GMM
    coberturas: str
    suma_asegurada: str
    deducible: float
    coaseguro: str
    coaseguro_tope: str
    
    
    def __init__(self):
        self.aseguradora = 0
        self.ramo = 0
        self.poliza = ""
        self.programa = ""
        self.contrante_nombre = ""
        self.contratante_domicilio = ""
        self.contratante_rfc = ""
        self.contratante_telefono = ""
        self.contratante_correo = ""
        self.titular_nombre = ""
        self.titular_fecha_nacimiento = ""
        self.fecha_inicio_vigencia = ""
        self.fecha_fin_vigencia = ""
        self.fecha_emision = ""
        self.fecha_ultimo_pago = ""
        self.id_moneda = 0
        self.id_pago = 0
        self.id_periodo = 0
        self.dia_cobro = 0
        self.prima_neta = 0.0
        self.prima_total = 0.0
        self.prima_inicial = 0.0
        self.prima_subsecuente = 0.0
        self.vehiculo_descripcion = ""
        self.vehiculo_modelo = ""
        self.vehiculo_endoso = ""
        self.vehiculo_serie = ""
        self.vehiculo_placas = ""
        self.vehiculo_uso = ""
        self.vehiculo_servicio = ""
        self.vehiculo_motor = ""
        self.vehiculo_plan = ""
        self.coberturas = ""
        self.suma_asegurada = ""
        self.deducible = ""
        self.coaseguro = ""
        self.coaseguro_tope = ""
        

    def __str__(self):
        poliza = f"aseguradora = {self.aseguradora}, ramo={self.ramo}, poliza={self.poliza}, programa={self.programa}"
        poliza += f"\nContratante[nombre={self.contrante_nombre}, domicilio={self.contratante_domicilio}, rfc={self.contratante_rfc}, telefono={self.contratante_telefono}, correo={self.contratante_correo}]"
        
        if self.titular_nombre:
            poliza += f"\nTilular[nombre={self.titular_nombre}, fecha_nacimiento={self.titular_fecha_nacimiento}]"
        
        poliza += f"\nfecha_inicio_vigencia={self.fecha_inicio_vigencia}, fecha_fin_vigencia={self.fecha_fin_vigencia}, moneda={self.id_moneda}, pago={self.id_pago}, periodo={self.id_periodo}, dia_cobro={self.dia_cobro}" 
        
        if self.fecha_emision:
            poliza+=f"\nfecha_emision={self.fecha_emision}"
        
        if self.fecha_ultimo_pago:
            poliza+=f"\nfecha_ultimo_pago={self.fecha_ultimo_pago}"

        poliza += f"\nprima_neta={self.prima_neta}, prima_inicial={self.prima_inicial}, prima_subsecuente={self.prima_subsecuente}, prima_total={self.prima_total}"
        
        if self.ramo == RAMO_AUTOS:
            poliza += f"\nVehiculo[descripcion={self.vehiculo_descripcion}, modelo={self.vehiculo_modelo}, endoso={self.vehiculo_endoso}, serie={self.vehiculo_serie}, "
            poliza += f"placas={self.vehiculo_placas}, uso={self.vehiculo_uso}, servicio={self.vehiculo_servicio}, motor={self.vehiculo_motor}, plan = {self.vehiculo_plan}]" 

        if self.coberturas:
            poliza += f"\n[coberturas={self.coberturas}]"
        
        if self.ramo == RAMO_VIDA or self.ramo == RAMO_GMM:
            poliza += f"\nsuma_asegurada={self.suma_asegurada}, deducible={self.deducible}, coaseguro={self.coaseguro}, coaseguro_tope={self.coaseguro_tope}"
        
        return poliza
    