import vpython as vp
'''
La clase Astro es la encarga de crear las instacias que representan un cuerpo celeste en el espacio
'''
class Astro:
    #Costructor
    def __init__(self, masa, radio, color, brillo, posicion, velocidad, aceleracion, objetoVisual, rastro):
        self.masa = masa
        self.radio = radio
        self.color = color
        self.brillo = brillo
        self.posicion = posicion
        self.velocidad = velocidad
        self.aceleracion = aceleracion
        self.objetoVisual = objetoVisual
        self.rastro = rastro
    #Metodos
    