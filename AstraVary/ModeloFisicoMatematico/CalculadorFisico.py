import vpython as vp
'''
La clase CalculadorFisico es el encargado de los claculos matematicos que definen el comportamiento de los astros
'''
class CalculadorFisico:
    #Constructor
    def __init__(self, G, dt, suavizado=1e-2):
        self.G = G                      #constante gravitacional universal aprox 6.674x10^-11 N(m^2)/(kg^2) 
        self.dt = dt                    #delta de tiempo
        self.suavizado = suavizado      #distancia artificial para evitar romper la simulacion cuando los astros se acercan mucho 
    #Metodos
    def calcular_aceleraciones(self, astros):
        """
        Aplica la ley de gravitacion universal de Newton para sumar las que los tres cuerpos ejersen

        Args:
            astros (List): lista con los astros de la simulacion
        """
        for astro in astros:
            astro.aceleracion = vp.vector(0, 0, 0)

        for i, astro_i in enumerate(astros):
            for j, astro_j in enumerate(astros):
                if i == j:
                    continue
                r_vec = astro_j.posicion - astro_i.posicion
                denom = (vp.mag2(r_vec) + self.suavizado**2) ** 1.5
                astro_i.aceleracion += self.G * astro_j.masa * r_vec / denom
    
    def actualizar_movimiento(self, astros):
        """
        Aplica el algoritmo euler-cromer usando el paso de tiempo dt para obtener la velocidad y posicion
        
        Args:
            astros(List): listo cpn los astros de la simulacion 
        """ 
        self.calcular_aceleraciones(astros)
        for astro in astros:
            astro.velocidad = astro.velocidad + astro.aceleracion * self.dt   # velocidad
            astro.posicion = astro.posicion + astro.velocidad * self.dt       # posicion
    
    def calcular_centro_de_masas(astros):
        """
        Calcula la posisicon y velocidad global del sistema 

        Args:
            astros (List): listo cpn los astros de la simulacion 

        Returns:
            vector: vectores con la posicion y velocidad
        """
        masa_total = sum(a.masa for a in astros)
        pos_cm = sum((a.masa * a.posicion for a in astros), vp.vector(0, 0, 0)) / masa_total
        vel_cm = sum((a.masa * a.velocidad for a in astros), vp.vector(0, 0, 0)) / masa_total
        return pos_cm, vel_cm