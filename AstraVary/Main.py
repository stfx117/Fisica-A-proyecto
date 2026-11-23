import sys
from pathlib import Path

import vpython as vp

PROJECT_DIRECTORY = Path(__file__).resolve().parent
MODEL_DIRECTORY = PROJECT_DIRECTORY / "ModeloFisicoMatematico"
for directory in (PROJECT_DIRECTORY, MODEL_DIRECTORY):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))

from ModeloFisicoMatematico.Astro import Astro
from ModeloFisicoMatematico.CalculadorFisico import CalculadorFisico
from ModeloFisicoMatematico.GraficadorOrbital import GraficadorOrbital
from ModeloFisicoMatematico.SistemaEstelar import SistemaEstelar
from GUI.InterfazUsuario import InterfasUsuario


G_FISICA = 6.67430e-11
MASA_INICIAL = 1e12
ESCALA_LONGITUD = 1e7
ESCALA_TIEMPO = (
    ESCALA_LONGITUD ** 3 / (G_FISICA * MASA_INICIAL)
) ** 0.5
G = G_FISICA * ESCALA_TIEMPO ** 2 / ESCALA_LONGITUD ** 3
PASO_TIEMPO = 1e8 / ESCALA_TIEMPO
SUAVIZADO = 1e-2 / ESCALA_LONGITUD
RADIO_ORBITAL = 8e7 / ESCALA_LONGITUD
COLORES_INICIALES = [vp.color.yellow, vp.color.cyan, vp.color.magenta]
MOSTRAR_TABLA_MAGNITUDES = False
ANCHO_CONTROLES = 360
ANCHO_VISUALIZACION = 720
ALTO_VISUALIZACION = 600
ANCHO_INTERFAZ = ANCHO_CONTROLES + ANCHO_VISUALIZACION


def crear_astro(escena, masa, posicion, velocidad, color):
    escena.select()
    astro = Astro(masa, color, posicion, velocidad)
    astro.modificar_masa(masa)
    astro.objetoVisual.make_trail = True
    astro.objetoVisual.retain = 500
    astro.objetoVisual.trail_radius = 0.02
    return astro


def crear_sistema():
    tabla_panel = None
    if MOSTRAR_TABLA_MAGNITUDES:
        tabla_panel = vp.canvas(
            title="AstraVary | Magnitudes del sistema",
            width=ANCHO_INTERFAZ,
            height=1,
            background=vp.vector(0.055, 0.07, 0.11),
            align="left",
        )
    panel = vp.canvas(
        title="",
        width=ANCHO_CONTROLES,
        height=1,
        background=vp.vector(0.91, 0.95, 1.0),
        align="left",
    )
    escena = vp.canvas(
        title="Visualizacion del problema de los tres cuerpos",
        width=ANCHO_VISUALIZACION,
        height=ALTO_VISUALIZACION,
        background=vp.vector(0.015, 0.025, 0.06),
        align="right",
        center=vp.vector(0, 0, 0),
        range=20,
    )
    grafica = vp.graph(
        title="Evolucion orbital",
        xtitle="Tiempo normalizado",
        ytitle="Distancia normalizada",
        width=ANCHO_INTERFAZ,
        height=300,
        align="left",
    )

    calculador = CalculadorFisico(G, PASO_TIEMPO, SUAVIZADO)
    graficador = GraficadorOrbital(grafica, [])
    sistema = SistemaEstelar(calculador, graficador)

    def restablecer_modelo(tipo_plantilla="Lagrange"):
        velocidad_angular = (
            G * MASA_INICIAL / (3 * RADIO_ORBITAL ** 3)
        ) ** 0.5
        for indice, color_astro in enumerate(COLORES_INICIALES):
            angulo = 2 * vp.pi * indice / 3
            posicion = vp.vector(
                RADIO_ORBITAL * vp.cos(angulo),
                RADIO_ORBITAL * vp.sin(angulo),
                0,
            )
            if tipo_plantilla == "Lagrange":
                velocidad = vp.vector(
                    -posicion.y * velocidad_angular,
                    posicion.x * velocidad_angular,
                    0,
                )
            else:
                velocidad = vp.vector(0, 0, 0)
            sistema.agregar_astro(
                crear_astro(
                    escena,
                    MASA_INICIAL,
                    posicion,
                    velocidad,
                    color_astro,
                )
            )
        graficador.inicializar_curvas(sistema.astros)

    restablecer_modelo()
    interfaz = InterfasUsuario(
        ventana=panel,
        sistema=sistema,
        visualizacion=escena,
        graficador=graficador,
        crear_astro=lambda masa, posicion, velocidad, color: crear_astro(
            escena, masa, posicion, velocidad, color
        ),
        restablecer_modelo=restablecer_modelo,
        escala_longitud=ESCALA_LONGITUD,
        escala_tiempo=ESCALA_TIEMPO,
        G_fisica=G_FISICA,
        ventana_tabla=tabla_panel,
        mostrar_tabla=MOSTRAR_TABLA_MAGNITUDES,
    )
    interfaz.crear_menu_inicial()
    interfaz.crear_controles_simulacion()
    return escena, sistema, interfaz


def main():
    _, sistema, interfaz = crear_sistema()
    ejecutando = {"valor": False}
    pausada = {"valor": False}

    def iniciar():
        ejecutando["valor"] = True

    def cambiar_pausa(estado):
        pausada["valor"] = estado

    interfaz.on_iniciar = iniciar
    interfaz.on_pausa = cambiar_pausa
    interfaz.on_salir = lambda: sys.exit(0)

    while True:
        vp.rate(240)
        if ejecutando["valor"] and not pausada["valor"]:
            sistema.actualizar_simulacion()
            interfaz.actualizar_vectores()
            interfaz.actualizar_tabla_medidas()


if __name__ == "__main__":
    main()
