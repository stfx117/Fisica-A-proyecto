import vpython as vp
'''
La clase CalculadorFisico es el encargado de los claculos matematicos que definen el comportamiento de los astros
'''
class CalculadorFisico:
    #Constructor
    def __init__(self, metodoIntegracion):
        self.metodoIntegracion = metodoIntegracion
    #Metodos