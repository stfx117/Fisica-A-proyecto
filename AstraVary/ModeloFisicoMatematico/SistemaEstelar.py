import vpython as vp
from CalculadorFisico import CalculadorFisico
from GraficadorOrbital import GraficadorOrbital

'''
La clase SistemaEstelar es el espacio simulado donde van a interactuar los astros 
'''
class SistemaEstelar:
    #Constructor
    def __init__(self, calculador, graficador):
        self.astros = []
        self.tiempoActual = 0.0
        self.ejecutando = False
        self.calculador = calculador
        self.graficador = graficador
    #Metodos
    def agregar_astro(self, astro):
        """_summary_

        Args:
            Astro (_type_): _description_
        """
        self.astros.append(astro)
        
    def actualizar_simulacion(self):
        """_summary_
        """
        self.calculador.actualizar_movimiento(self.astros)
        self.tiempoActual += self.calculador.dt
        for astro in self.astros:
            astro.actualizar_visual()
        self.graficador.actualizar_graficas(self.astros, self.tiempoActual)
    
    def reiniciar_sistema(self):
        """_summary_
        """
        for astro in self.astros:
            astro.eliminar_visual()
        self.astros.clear()
        self.tiempoActual = 0.0
        self.graficador.limpiar_graficas()
    
    def cambiar_masa_astro(self, indice, nueva_masa):
        """_summary_

        Args:
            indice (_type_): _description_
            nueva_masa (_type_): _description_
        """
        self.astros[indice].modificar_masa(nueva_masa)
    