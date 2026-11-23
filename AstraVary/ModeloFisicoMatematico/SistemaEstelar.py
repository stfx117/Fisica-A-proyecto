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
        """
        Agrega un objeto de la clase astro a la lista de oastros e el sistema

        Args:
            astro (Astro): una instancia de la clase astro
        """
        self.astros.append(astro)
        
    def actualizar_simulacion(self):
        """
        Actualiza el movimiento, las graficas y la representacion visual de los astros dentor de la simulacion
        """
        self.calculador.actualizar_movimiento(self.astros)
        self.tiempoActual += self.calculador.dt     #avansa dt unidades de tiempo
        for astro in self.astros:
            astro.actualizar_visual()
        self.graficador.actualizar_graficas(self.astros, self.tiempoActual)
    
    def reiniciar_sistema(self):
        """
        Vuelve al estado original de la simulacion
        """
        for astro in self.astros:
            astro.eliminar_visual()
        self.astros.clear()
        self.tiempoActual = 0.0
        self.graficador.limpiar_graficas()
    
    def cambiar_masa_astro(self, indice, nueva_masa):
        """
        Cambia la masa del astro
        
        Args:
            indice (int): posicion del astro dentro de la lista
            nueva_masa (float): masa nueva del astro
        """
        self.astros[indice].modificar_masa(nueva_masa)
    