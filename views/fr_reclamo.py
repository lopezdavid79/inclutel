import wx
import webbrowser
import urllib.parse
import json
import os
from datetime import datetime

class ReclamoFrame(wx.Frame):
    def __init__(self, parent, title):
        super(ReclamoFrame, self).__init__(parent, title=title, size=(400, 400))  # Aumentamos el tamaño

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Campos para el reclamo con etiquetas descriptivas (orden modificado)
        wx.StaticText(panel, label="Seleccione el servicio:", name="lblServicio").SetHelpText("Seleccione el tipo de servicio para el reclamo.")
        self.servicio_choice = wx.Choice(panel, choices=["Luz", "Internet", "Telefonía", "Cable"], name="servicioChoice")
        vbox.Add(self.servicio_choice, 0, wx.ALL | wx.EXPAND, 5)

        wx.StaticText(panel, label="Ingrese la descripción del reclamo:", name="lblDescripcion").SetHelpText("Ingrese una descripción detallada del reclamo.")
        self.descripcion_tc = wx.TextCtrl(panel, style=wx.TE_MULTILINE, name="descripcionTC")
        vbox.Add(self.descripcion_tc, 1, wx.ALL | wx.EXPAND, 5)

        wx.StaticText(panel, label="Ingrese su nombre:", name="lblNombre").SetHelpText("Ingrese su nombre completo.")
        self.nombre_tc = wx.TextCtrl(panel, name="nombreTC")
        vbox.Add(self.nombre_tc, 0, wx.ALL | wx.EXPAND, 5)

        wx.StaticText(panel, label="Ingrese su domicilio:", name="lblDomicilio").SetHelpText("Ingrese su domicilio completo.")
        self.domicilio_tc = wx.TextCtrl(panel, name="domicilioTC")
        vbox.Add(self.domicilio_tc, 0, wx.ALL | wx.EXPAND, 5)

        wx.StaticText(panel, label="Ingrese su teléfono:", name="lblTelefono").SetHelpText("Ingrese su número de teléfono.")
        self.telefono_tc = wx.TextCtrl(panel, name="telefonoTC")
        vbox.Add(self.telefono_tc, 0, wx.ALL | wx.EXPAND, 5)

        # Botones
        hbox = wx.BoxSizer(wx.HORIZONTAL)  # Creamos un sizer horizontal para los botones

        enviar_btn = wx.Button(panel, label="Enviar por WhatsApp", name="btnEnviar")
        enviar_btn.Bind(wx.EVT_BUTTON, self.enviar_reclamo)
        hbox.Add(enviar_btn, 0, wx.ALL | wx.CENTER, 5)

        cerrar_btn = wx.Button(panel, label="Cerrar", name="btnCerrar")
        cerrar_btn.Bind(wx.EVT_BUTTON, self.cerrar_aplicacion)
        hbox.Add(cerrar_btn, 0, wx.ALL | wx.CENTER, 5)

        vbox.Add(hbox, 0, wx.ALL | wx.CENTER, 10)  # Agregamos el sizer horizontal al sizer vertical

        panel.SetSizer(vbox)
        self.Centre()

    def enviar_reclamo(self, event):
        servicio = self.servicio_choice.GetStringSelection()
        nombre = self.nombre_tc.GetValue()
        descripcion = self.descripcion_tc.GetValue()
        domicilio = self.domicilio_tc.GetValue()
        telefono = self.telefono_tc.GetValue()

        mensaje = f"Reclamo de {servicio}:\nNombre: {nombre}\nDomicilio: {domicilio}\nTeléfono: {telefono}\nDescripción: {descripcion}"
        mensaje_codificado = urllib.parse.quote(mensaje)
        numero_telefono = "5493534294632"  # Reemplaza con el número

        url = f"https://wa.me/{numero_telefono}?text={mensaje_codificado}"
        webbrowser.open_new_tab(url)

        # Guardar en JSON
        self.guardar_reclamo_json(servicio, nombre, descripcion, domicilio, telefono)

    def guardar_reclamo_json(self, servicio, nombre, descripcion, domicilio, telefono):
        reclamo = {
            "servicio": servicio,
            "nombre": nombre,
            "descripcion": descripcion,
            "domicilio": domicilio,
            "telefono": telefono,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        archivo_json = "reclamos.json"
        reclamos_existentes = []

        if os.path.exists(archivo_json):
            with open(archivo_json, "r") as f:
                try:
                    reclamos_existentes = json.load(f)
                except json.JSONDecodeError:
                    reclamos_existentes = []

        reclamos_existentes.append(reclamo)

        with open(archivo_json, "w") as f:
            json.dump(reclamos_existentes, f, indent=4)

    def cerrar_aplicacion(self, event):
        self.Close()
