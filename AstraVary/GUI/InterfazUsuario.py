import vpython as vp


class InterfasUsuario:
    def __init__(
        self,
        ventana,
        sistema,
        visualizacion,
        graficador,
        crear_astro,
        restablecer_modelo,
        escala_longitud,
        escala_tiempo,
        G_fisica,
        on_iniciar=None,
        on_salir=None,
        ventana_tabla=None,
        mostrar_tabla=True,
    ):
        self.ventana = ventana
        self.ventana_tabla = (
            ventana if ventana_tabla is None else ventana_tabla
        )
        self.sistema = sistema
        self.visualizacion = visualizacion
        self.graficador = graficador
        self.crear_astro = crear_astro
        self.restablecer_modelo = restablecer_modelo
        self.escala_longitud = escala_longitud
        self.escala_tiempo = escala_tiempo
        self.G_fisica = G_fisica
        self.mostrar_tabla = mostrar_tabla
        self.escala_masa = (
            escala_longitud ** 3 / (G_fisica * escala_tiempo ** 2)
        )
        self.on_iniciar = on_iniciar
        self.on_salir = on_salir
        self.on_pausa = None
        self.mostrarVectores = False
        self.mostrarOrbitas = True
        self.pausada = False
        self.masa_sliders = []
        self.etiquetas_masa = []
        self.vectores_velocidad = []
        self.tabla_medidas = None
        self._contador_actualizaciones_tabla = 0

    def crear_menu_inicial(self):
        if self.mostrar_tabla:
            self.ventana_tabla.select()
            self.ventana_tabla.append_to_caption(
                "<style>"
                "button { width: 154px !important; height: 38px !important; "
                "border-radius: 9px !important; font-size: 13px !important; "
                "font-weight: 600 !important; margin: 3px !important; "
                "box-sizing: border-box !important; }"
                "input[type=range] { accent-color: #38bdf8; }"
                "</style>"
                "<div style='font-family:sans-serif; color:#e8edf5; "
                "padding:12px 16px; background:#111827; "
                "border-bottom:1px solid #334155;'>"
                "<span style='font-size:20px; font-weight:700; "
                "letter-spacing:1px;'>ASTRAVARY</span>"
                "<span style='margin-left:14px; color:#94a3b8; "
                "font-size:12px;'>Simulador de tres cuerpos</span></div>"
                "<div style='padding:10px 14px 2px; color:#7dd3fc; "
                "font:600 11px sans-serif; letter-spacing:1px;'>"
                "MAGNITUDES Y ESCALAS</div>"
            )
            self.tabla_medidas = vp.wtext(
                text="",
                pos=self.ventana_tabla.caption_anchor,
            )
        self.ventana.select()
        self.ventana.append_to_title(
                "<style>"
                "div:has(> #astravary-controls-marker) { "
                "background:#e8f2ff !important; color:#1e3a5f !important; "
                "width:360px; padding:10px; box-sizing:border-box; "
                "border-radius:12px; }"
                "button { width:154px !important; height:38px !important; "
            "border-radius:9px !important; font-size:13px !important; "
            "font-weight:600 !important; margin:3px !important; "
                "box-sizing:border-box !important; }"
                "input[type=range] { accent-color:#0284c7; }"
                "select { background:#f8fbff; color:#1e293b; "
                "border:1px solid #93c5fd; border-radius:6px; }"
                "</style>"
                "<span id='astravary-controls-marker' style='display:none;'></span>"
                "<div style='margin:4px; padding:8px; background:#dbeafe; "
                "border:1px solid #93c5fd; border-radius:9px;'>"
                "<div style='padding:11px 8px 5px; color:#1e3a5f; "
            "font:600 11px sans-serif; letter-spacing:1px;'>"
            "CONTROLES DE SIMULACION</div>"
        )
        self.ventana.append_to_title(
                "<div style='padding:5px 8px 2px; color:#1e3a5f; "
            "font:600 13px sans-serif;'>"
            "ACCIONES</div>"
        )
        self.boton_iniciar = vp.button(
            text="Iniciar",
            bind=self.iniciar_simulacion,
            background=vp.vector(0.12, 0.48, 0.42),
            pos=self.ventana.title_anchor,
            canvas=self.ventana,
        )
        self.boton_pausa = vp.button(
            text="Pausar",
            bind=self.alternar_pausa,
            disabled=True,
            pos=self.ventana.title_anchor,
            canvas=self.ventana,
        )
        self.ventana.append_to_title("<br>")
        self.boton_reiniciar = vp.button(
            text="Reiniciar",
            bind=lambda _evento: self.reiniciar(),
            pos=self.ventana.title_anchor,
            canvas=self.ventana,
        )
        self.boton_salir = vp.button(
            text="Salir",
            bind=self.salir_programa,
            background=vp.vector(0.58, 0.20, 0.27),
            pos=self.ventana.title_anchor,
            canvas=self.ventana,
        )
        self.ventana.append_to_title("</div>")

    def crear_controles_simulacion(self):
        self.ventana.select()
        self.ventana.append_to_title(
            "<div style='margin:4px; padding:8px; background:#dbeafe; "
            "border:1px solid #93c5fd; border-radius:9px;'>"
            "<div style='padding:6px 8px; color:#1e3a5f; "
            "font:600 11px sans-serif; letter-spacing:1px;'>"
            "PARAMETROS DEL MODELO</div>"
            "<div style='padding:3px 8px; color:#1e3a5f; "
            "font:600 13px sans-serif;'>Masas de los cuerpos</div>"
            f"<div style='padding:0 8px; color:#475569; font:10px sans-serif;'>"
            f"Escala: 1 uM = {self.escala_masa:.2e} kg</div>"
        )
        for indice, astro in enumerate(self.sistema.astros):
            self._crear_control_masa(indice, astro)

        self.ventana.append_to_title(
            "<br><div style='padding: 6px 8px; color: #1e3a5f; "
            "font: 600 13px sans-serif;'>Plantilla inicial</div>"
        )
        self.selector_plantilla = vp.menu(
            choices=["Lagrange", "Triangulo en reposo"],
            index=0,
            bind=self.cambiar_plantilla,
            pos=self.ventana.title_anchor,
            canvas=self.ventana,
        )
        self.ventana.append_to_title(
            "<br><div style='padding: 8px 8px 3px; color: #1e3a5f; "
            "font: 600 13px sans-serif;'>Visualizacion</div>"
        )
        self.checkbox_vectores = vp.checkbox(
            text="Vectores de velocidad",
            checked=self.mostrarVectores,
            bind=self.alternar_vectores,
            pos=self.ventana.title_anchor,
            canvas=self.ventana,
        )
        self.ventana.append_to_title("<br>")
        self.checkbox_orbitas = vp.checkbox(
            text="Orbitas",
            checked=self.mostrarOrbitas,
            bind=self.alternar_orbitas,
            pos=self.ventana.title_anchor,
            canvas=self.ventana,
        )
        self.ventana.append_to_title("<br><br>")
        self.boton_agregar_astro = vp.button(
            text="Agregar astro",
            bind=self.agregar_astro,
            pos=self.ventana.title_anchor,
            canvas=self.ventana,
        )
        self.ventana.append_to_title("</div>")
        self.actualizar_tabla_medidas(forzar=True)

    def _crear_control_masa(self, indice, astro):
        self.ventana.select()
        self.ventana.append_to_title(
            "<div style='margin:5px 8px; padding:7px 10px; "
            "background:#f1f7ff; border:1px solid #bfdbfe; "
            "border-radius:8px;'>"
        )
        etiqueta = vp.wtext(
            text=(
                f"<br><b style='color:#1e3a5f;'>Cuerpo {indice + 1}</b>"
                f"<br><span style='color:#0369a1;'>"
                f"{astro.masa:.2e} kg "
                f"({astro.masa / self.escala_masa:.2f} uM)</span><br>"
            ),
            pos=self.ventana.title_anchor,
        )
        slider = vp.slider(
            min=1e11,
            max=8e12,
            value=astro.masa,
            step=1e11,
            length=180,
            bind=lambda evento, i=indice: self.evento_cambiar_masa(evento, i),
            pos=self.ventana.title_anchor,
            canvas=self.ventana,
        )
        self.ventana.append_to_title(
            "<br><span style='color:#475569; font:10px sans-serif;'>"
            "Rango: 1.00e+11 - 8.00e+12 kg "
            "(0.10 - 8.00 uM)</span></div>"
        )
        self.etiquetas_masa.append(etiqueta)
        self.masa_sliders.append(slider)

    def evento_cambiar_masa(self, slider, indice):
        if indice >= len(self.sistema.astros):
            return
        self.sistema.cambiar_masa_astro(indice, slider.value)
        self.etiquetas_masa[indice].text = (
            f"<br><b style='color:#1e3a5f;'>Cuerpo {indice + 1}</b>"
            f"<br><span style='color:#0369a1;'>"
            f"{slider.value:.2e} kg "
            f"({slider.value / self.escala_masa:.2f} uM)</span><br>"
        )
        self.actualizar_tabla_medidas(forzar=True)

    def actualizar_tabla_medidas(self, forzar=False):
        if not self.mostrar_tabla or self.tabla_medidas is None:
            return
        self._contador_actualizaciones_tabla += 1
        if not forzar and self._contador_actualizaciones_tabla % 12:
            return

        tarjetas = []
        factor_velocidad = self.escala_longitud / self.escala_tiempo
        for indice, astro in enumerate(self.sistema.astros, start=1):
            x_real = astro.posicion.x * self.escala_longitud
            y_real = astro.posicion.y * self.escala_longitud
            radio_real = vp.mag(astro.posicion) * self.escala_longitud
            rapidez_real = vp.mag(astro.velocidad) * factor_velocidad
            tarjetas.append(
                "<td style='width:33.33%; padding:5px; vertical-align:top;'>"
                "<div style='padding:9px 11px; background:#ffffff; "
                "border:1px solid #bfdbfe; border-radius:8px;'>"
                f"<div style='padding-bottom:5px; color:#0369a1; "
                f"font-weight:700; border-bottom:1px solid #dbeafe;'>"
                f"ASTRO {indice}</div>"
                "<div style='padding-top:5px;'>"
                f"Masa: {astro.masa / self.escala_masa:.2f} uM "
                f"({astro.masa:.3e} kg)<br>"
                f"x: {astro.posicion.x:.2f} uL ({x_real:.3e} m) "
                f"&nbsp; y: {astro.posicion.y:.2f} uL "
                f"({y_real:.3e} m)<br>"
                f"r: {vp.mag(astro.posicion):.2f} uL "
                f"({radio_real:.3e} m)<br>"
                f"|v|: {vp.mag(astro.velocidad):.3e} uL/uT "
                f"({rapidez_real:.3e} m/s)<br>"
                f"Radio visual: {astro.radio:.2f} uL"
                "</div></div></td>"
            )
        filas_tarjetas = [
            "<tr>" + "".join(tarjetas[inicio:inicio + 3]) + "</tr>"
            for inicio in range(0, len(tarjetas), 3)
        ]

        tiempo_real = self.sistema.tiempoActual * self.escala_tiempo
        dt_real = self.sistema.calculador.dt * self.escala_tiempo
        g_modelo = (
            self.G_fisica * self.escala_tiempo ** 2
            / self.escala_longitud ** 3
        )
        self.tabla_medidas.text = (
            "<div style='margin:4px 12px 10px; padding:8px; "
            "background:#e8f2ff; border:1px solid #93c5fd; "
            "border-radius:9px; font:11px/1.5 sans-serif; color:#1e293b;'>"
            "<table style='width:100%; border-collapse:collapse; "
            "table-layout:fixed;'><tr>"
            "<td style='width:33.33%; padding:5px 10px; "
            "border-right:1px solid #bfdbfe;'>"
            "<span style='color:#0369a1; font-weight:700;'>ESCALAS</span><br>"
            f"1 uL = {self.escala_longitud:.2e} m<br>"
            f"1 uT = {self.escala_tiempo:.2e} s<br>"
            f"1 uM = {self.escala_masa:.2e} kg</td>"
            "<td style='width:33.33%; padding:5px 10px; "
            "border-right:1px solid #bfdbfe;'>"
            "<span style='color:#0369a1; font-weight:700;'>GRAVEDAD</span><br>"
            f"G fisica = {self.G_fisica:.3e} m^3/(kg s^2)<br>"
            f"G modelo = {g_modelo:.3e} uL^3/(kg uT^2)<br>"
            f"G normalizada = {g_modelo * self.escala_masa:.3f} "
            "uL^3/(uM uT^2)</td>"
            "<td style='width:33.33%; padding:5px 10px;'>"
            "<span style='color:#0369a1; font-weight:700;'>TIEMPO</span><br>"
            f"dt = {self.sistema.calculador.dt:.4f} uT "
            f"({dt_real:.2e} s)<br>"
            f"Actual = {self.sistema.tiempoActual:.4f} uT "
            f"({tiempo_real:.2e} s)</td>"
            "</tr></table><hr style='border:0; "
            "border-top:1px solid #bfdbfe;'>"
            "<table style='width:100%; border-collapse:collapse; "
            "table-layout:fixed;'><tbody>"
            f"{''.join(filas_tarjetas)}</tbody></table></div>"
        )

    def alternar_vectores(self, checkbox):
        self.mostrarVectores = checkbox.checked
        self.actualizar_vectores()

    def alternar_orbitas(self, checkbox):
        self.mostrarOrbitas = checkbox.checked
        for astro in self.sistema.astros:
            astro.objetoVisual.clear_trail()
            astro.objetoVisual.make_trail = self.mostrarOrbitas

    def cambiar_plantilla(self, menu):
        self.reiniciar(menu.selected)

    def reiniciar(self, tipo_plantilla="Lagrange"):
        self.sistema.reiniciar_sistema()
        self._limpiar_vectores()
        self._eliminar_controles_adicionales()
        self.restablecer_modelo(tipo_plantilla)

        for indice, (slider, etiqueta, astro) in enumerate(
            zip(self.masa_sliders, self.etiquetas_masa, self.sistema.astros)
        ):
            slider.value = astro.masa
            etiqueta.text = (
                f"<br><b style='color:#1e3a5f;'>Cuerpo {indice + 1}</b>"
                f"<br><span style='color:#0369a1;'>"
                f"{astro.masa:.2e} kg "
                f"({astro.masa / self.escala_masa:.2f} uM)</span><br>"
            )
        self.actualizar_tabla_medidas(forzar=True)

        if self.pausada:
            self.pausada = False
            self.boton_pausa.text = "Pausar"
            if self.on_pausa is not None:
                self.on_pausa(False)

    def _eliminar_controles_adicionales(self):
        for etiqueta in self.etiquetas_masa[3:]:
            etiqueta.delete()
        for slider in self.masa_sliders[3:]:
            slider.delete()
        self.etiquetas_masa = self.etiquetas_masa[:3]
        self.masa_sliders = self.masa_sliders[:3]

    def _limpiar_vectores(self):
        for vector_velocidad in self.vectores_velocidad:
            vector_velocidad.visible = False
        self.vectores_velocidad = []

    def actualizar_vectores(self):
        if not self.mostrarVectores:
            for vector_velocidad in self.vectores_velocidad:
                vector_velocidad.visible = False
            return

        while len(self.vectores_velocidad) < len(self.sistema.astros):
            astro = self.sistema.astros[len(self.vectores_velocidad)]
            self.visualizacion.select()
            self.vectores_velocidad.append(
                vp.arrow(
                    pos=astro.posicion,
                    axis=astro.velocidad * 3,
                    color=vp.color.orange,
                    canvas=self.visualizacion,
                )
            )

        for astro, vector_velocidad in zip(
            self.sistema.astros, self.vectores_velocidad
        ):
            vector_velocidad.pos = astro.posicion
            vector_velocidad.axis = astro.velocidad * 3
            vector_velocidad.visible = True

    def agregar_astro(self, _boton=None):
        indice = len(self.sistema.astros)
        angulo = 2 * vp.pi * indice / 5
        radio = 14 + max(0, indice - 3) * 2
        self.visualizacion.range = max(self.visualizacion.range, radio + 4)
        posicion = vp.vector(
            radio * vp.cos(angulo),
            radio * vp.sin(angulo),
            0,
        )
        masa_central = sum(astro.masa for astro in self.sistema.astros)
        rapidez = (
            self.sistema.calculador.G * masa_central / radio
        ) ** 0.5
        velocidad = vp.vector(
            -vp.sin(angulo) * rapidez,
            vp.cos(angulo) * rapidez,
            0,
        )
        colores = [
            vp.color.red,
            vp.color.green,
            vp.color.blue,
            vp.color.orange,
            vp.color.magenta,
        ]
        nuevo = self.crear_astro(
            2e11,
            posicion,
            velocidad,
            colores[indice % len(colores)],
        )
        nuevo.objetoVisual.make_trail = self.mostrarOrbitas
        self.sistema.agregar_astro(nuevo)
        self._crear_control_masa(indice, nuevo)
        self.graficador.inicializar_curvas(self.sistema.astros)
        self.actualizar_tabla_medidas(forzar=True)

    def iniciar_simulacion(self, _boton=None):
        if self.on_iniciar is not None:
            self.on_iniciar()
        self.boton_pausa.disabled = False

    def alternar_pausa(self, _boton=None):
        self.pausada = not self.pausada
        self.boton_pausa.text = "Reanudar" if self.pausada else "Pausar"
        if self.on_pausa is not None:
            self.on_pausa(self.pausada)

    def salir_programa(self, _boton=None):
        if self.on_salir is not None:
            self.on_salir()
