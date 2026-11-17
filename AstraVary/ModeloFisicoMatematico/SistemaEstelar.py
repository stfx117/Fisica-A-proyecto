'''
La clase SistemaEstelar es el espacio simulado donde van a interactuar los astros 
'''
class SistemaEstelar:
    #Constructor
    def __init__(self, astros, G, dt, tiempoActual):
        self.astros = astros
        self.G = G
        self.dt = dt
        self.tiempoActual = tiempoActual
    #Metodos