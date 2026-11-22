import vpython as vp
'''
La clase InterfasUsuario es la encargada de poder interactuar directamente con el usuario
'''
class InterfazUsuario:
    #Constructor
    def __init__(self,ventana, sliderMasa, botones, mostrarVectores, mostrarOrbitas):
        self.ventana = ventana
        self.sliderMasa = sliderMasa
        self.botones = botones 
        self.mostrarVectores = mostrarVectores
        self.mostrarOrbitas = mostrarOrbitas
    #Metodos
    