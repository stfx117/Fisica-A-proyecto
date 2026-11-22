import vpython as vp
'''
La clase Astro es la encarga de crear las instacias que representan un cuerpo celeste en el espacio
'''
#Constantes de configuracion
MASA_ESTRELLA = 6e12      # masa mínima para que el astro brille
MASA_REFERENCIA = 1e12    # masa a la que corresponde RADIO_BASE
RADIO_BASE = 0.5
RADIO_MIN = 0.2
RADIO_MAX = 1.5

class Astro:
    #Costructor
    def __init__(self, masa, color, posicion, velocidad):
        self.masa = masa
        self.color = color
        self.posicion = posicion
        self.velocidad = velocidad
        self.aceleracion = vp.vector(0, 0, 0)
        
        self.radio = RADIO_MIN
        self.brillo = False
        self.luz = None
        self.objetoVisual = vp.sphere(pos=posicion, radius=self.radio, color=color, make_trail=False)
        
        self.modificar_masa
        
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
        if self.masa >= MASA_ESTRELLA:
            self.brillo = True
            if self.luz is None:
                self.luz = vp.local_light(pos=self.posicion, color=vp.color.white)
        else:
            self.brillo = False
            if self.luz is not None:
                self.luz.visible = False
                self.luz = None
        #se ajusta el tamaño del astro 
        radio = RADIO_BASE*(self.masa/MASA_REFERENCIA)**0.5
        self.radio = max(RADIO_MIN, min(RADIO_MAX, radio))
        self.actualizar_visual()