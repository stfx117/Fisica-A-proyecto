import vpython as vp
'''
La clase Astro es la encarga de crear las instacias que representan un cuerpo celeste en el espacio
'''
class Astro:
    #Costructor
    def __init__(self, masa, radio, color, brillo, luz, posicion, velocidad, aceleracion, objetoVisual):
        self.masa = masa
        self.radio = radio
        self.color = color
        self.brillo = brillo
        self.luz = luz
        self.posicion = posicion
        self.velocidad = velocidad
        self.aceleracion = aceleracion
        self.objetoVisual = objetoVisual
        
    #Metodos
    def actualizar_visual(self):
        """_summary_
        """
        #se actualizan los valores para actualisar el visual
        self.objetoVisual.pos = self.posicion
        self.objetoVisual.radius = self.radio
        self.objetoVisual.emissive = self.brillo
        #actualisa la posicion de la luz
        if self.luz is not None:
            self.luz.pos = self.posicion
        
    def modificar_masa(self, nueva_masa):
        """_summary_

        Args:
            nueva_masa (_type_): _description_
        """
        self.masa = nueva_masa
        #se crea un objeto local_ligth
        if self.masa >= 60:
            self.brillo = True
            if self.luz is None:
                self.luz = vp.local_light(pos=self.posicion, color=vp.color.white)
        else:
            self.brillo = False
            if self.luz is not None:
                self.luz.visible = False
                self.luz = None
        #se ajusta el tamaño del astro 
        nuevo_radio = 0.5*(self.masa/10)**0.5
        if nuevo_radio < 0.2:
            nuevo_radio = 0.2
        elif nuevo_radio > 1.5:
            nuevo_radio = 1.5
        #se actualiza el visual del astro
        self.radio = nuevo_radio
        self.actualizar_visual()