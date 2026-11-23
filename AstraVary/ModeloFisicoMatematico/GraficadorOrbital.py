import vpython as vp

'''
La clase GraficadorOrbital representa en una grafica la distancia
al origen de cada astro a medida que avanza la simulacion.
'''
class GraficadorOrbital:
    #Constructor
    def __init__(self, ventanaGrafica, curvas):
        self.ventanaGrafica = ventanaGrafica
        self.curvas = curvas

    #Metodos
    def inicializar_curvas(self, astros):
        """Crea una curva para cada astro, conservando su color."""
        #Evita acumular las curvas de una simulacion anterior.
        self.limpiar_graficas()

        #Crea la ventana solo si no se recibio una previamente.
        if self.ventanaGrafica is None:
            self.ventanaGrafica = vp.graph(
                title="Distancia de los astros al origen",
                xtitle="Tiempo",
                ytitle="Distancia al origen"
            )

        for indice, astro in enumerate(astros, start=1):
            curva = vp.gcurve(
                graph=self.ventanaGrafica,
                color=astro.color,
                label=f"Astro {indice}"
            )
            self.curvas.append(curva)

    def actualizar_graficas(self, astros, tiempoActual):
        """Agrega a cada curva la distancia del astro al origen."""
        if self.curvas is None or len(self.curvas) != len(astros):
            raise ValueError(
                "Inicializa las curvas con inicializar_curvas(astros) "
                "antes de actualizar las graficas."
            )

        for i in range(len(astros)):
            astro = astros[i]
            curva = self.curvas[i]

            distancia = vp.mag(astro.posicion)
            curva.plot(tiempoActual, distancia)

    def limpiar_graficas(self):
        """Elimina las curvas, sin borrar la ventana grafica."""
        if self.curvas is None:
            self.curvas = []
            return

        for curva in self.curvas:
            curva.delete()
        self.curvas.clear()