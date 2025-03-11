
import urllib.parse
import webbrowser


import datetime
import os
import re
import sys
import wx
import wx.lib.mixins.listctrl as listmix
from module.ReproductorSonido import ReproductorSonido
from views.fr_ListSocio import ListSocio,AgregarSocioDialog
from module.GestionReclamo import GestionReclamo
from module.GestionSocio import GestionSocio
gestion_reclamo = GestionReclamo()
gestion_socio = GestionSocio()
class ListReclamo(wx.Frame, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, id=None, title="Gestión de Reclamos", *args, **kwds):
        super().__init__(parent, id=wx.ID_ANY, title=title, *args, **kwds)

        panel = wx.Panel(self)
        self.nombre_archivo_productos = 'data/productos.json'
        # Botón desplegable 
        self.btn_menu = wx.Button(panel, label="&Menú", pos=(10, 260))  # Ajusta la posición según sea necesario
        self.btn_menu.Bind(wx.EVT_BUTTON, self.on_mostrar_menu)
        # Lista de reclamos
        self.list_ctrl = wx.ListCtrl(panel, style=wx.LC_REPORT | wx.BORDER_SUNKEN, pos=(10, 10), size=(600, 250))
        self.list_ctrl.InsertColumn(0, 'ID', width=50)
        self.list_ctrl.InsertColumn(1, 'Fecha', width=100)
        self.list_ctrl.InsertColumn(2, 'Socio', width=150)
        self.list_ctrl.InsertColumn(3, 'Detalle', width=200)
        self.list_ctrl.InsertColumn(4, 'Estado', width=100)
        self.cargar_reclamos()
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.mostrar_detalle_reclamo)

        # Botones
        btn_nuevo = wx.Button(panel, label="Nuevo Reclamo", pos=(50, 300))
        btn_nuevo.Bind(wx.EVT_BUTTON, self.abrir_dialogo_nuevo)
        btn_cerrar = wx.Button(panel, label="Cerrar", pos=(300, 300))
        btn_cerrar.Bind(wx.EVT_BUTTON, self.cerrar_ventana)
        btn_actualizar = wx.Button(panel, label="Actualizar", pos=(175, 300))
        btn_actualizar.Bind(wx.EVT_BUTTON, self.actualizar_lista)

        self.Show()

    def actualizar_lista(self, event):
        self.cargar_reclamos()
        print("Lista actualizada en la interfaz")
        sys.stdout.flush()
        ReproductorSonido.reproducir("refresh.wav")

    def cargar_reclamos(self):
        self.list_ctrl.DeleteAllItems()
        reclamos = gestion_reclamo.obtener_todos()
        for id_reclamo, datos in reclamos.items():
            index = self.list_ctrl.InsertItem(self.list_ctrl.GetItemCount(), str(id_reclamo))
            self.list_ctrl.SetItem(index, 1, datos["fecha"])
            self.list_ctrl.SetItem(index, 2, datos["socio"])
            self.list_ctrl.SetItem(index, 3, datos["detalle"])
            self.list_ctrl.SetItem(index, 4, datos["estado"])

    def mostrar_detalle_reclamo(self, event):
        index = event.GetIndex()
        id_reclamo = self.list_ctrl.GetItemText(index)

        reclamos = gestion_reclamo.obtener_todos()
        if id_reclamo in reclamos:
            datos = reclamos[id_reclamo]
            dialogo = DetalleReclamoDialog(self, id_reclamo, datos)
            dialogo.ShowModal()
            dialogo.Destroy()
            self.cargar_reclamos()

    def abrir_dialogo_nuevo(self, event):
        ReproductorSonido.reproducir("screenCurtainOn.wav")
        dialogo = AgregarReclamoDialog(self)
        if dialogo.ShowModal() == wx.ID_OK:
            self.cargar_reclamos()
        dialogo.Destroy()

    def cerrar_ventana(self, event):
        ReproductorSonido.reproducir("screenCurtainOff.wav")
        self.Close()

    def on_mostrar_menu(self, event):
        menu = wx.Menu()
        ver_socio_item = menu.Append(wx.ID_ANY, "Ver Socios")
        self.Bind(wx.EVT_MENU, self.on_ver_socios, ver_socio_item)
        add_socio_item = menu.Append(wx.ID_ANY, "Agregar Socios")
        self.Bind(wx.EVT_MENU, self.on_add_socios, add_socio_item)
        exit_socio_item = menu.Append(wx.ID_ANY, "Salir")
        self.Bind(wx.EVT_MENU, self.cerrar_ventana, exit_socio_item)
        self.PopupMenu(menu, self.btn_menu.GetPosition())
        menu.Destroy()

    def on_ver_socios(self, event):
        frame_socios = ListSocio(self) # Crea una instancia de fr_listSocio
        frame_socios.Show()
        
    def on_add_socios(self, event):
        add_socios = AgregarSocioDialog(self) # Crea una instancia de fr_listSocio
        add_socios.Show()
        


class DetalleReclamoDialog(wx.Dialog):
    def __init__(self, parent, id_reclamo, datos):
        super().__init__(parent, title="Detalle del Reclamo", size=(300, 250))
        self.id_reclamo = id_reclamo

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        vbox.Add(wx.StaticText(panel, label=f"ID: {id_reclamo}"), flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add(wx.StaticText(panel, label=f"Fecha: {datos['fecha']}"), flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add(wx.StaticText(panel, label=f"socio: {datos['socio']}"), flag=wx.LEFT | wx.TOP, border=10)
        
        vbox.Add(wx.StaticText(panel, label=f"Detalle: {datos['detalle']}"), flag=wx.LEFT | wx.TOP, border=10)
        vbox.Add(wx.StaticText(panel, label=f"Estado: {datos['estado']}"), flag=wx.LEFT | wx.TOP, border=10)

        btn_editar = wx.Button(panel, label="Editar")
        btn_editar.Bind(wx.EVT_BUTTON, self.editar_reclamo)
        btn_delete = wx.Button(panel, label="Eliminar")
        btn_delete.Bind(wx.EVT_BUTTON, self.eliminar_reclamo)
        btn_cerrar = wx.Button(panel, wx.ID_CANCEL, "Cerrar")

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(btn_editar, flag=wx.RIGHT, border=10)
        hbox.Add(btn_delete, flag=wx.RIGHT, border=10)
        hbox.Add(btn_cerrar)

        vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)
        panel.SetSizer(vbox)

    def editar_reclamo(self, event):
        dialogo = EditarReclamoDialog(self, self.id_reclamo)
        if dialogo.ShowModal() == wx.ID_OK:
            self.EndModal(wx.ID_OK)
        dialogo.Destroy()

    def eliminar_reclamo(self, event):
        dialogo = EliminarReclamoDialog(self, self.id_reclamo, gestion_reclamo)
        if dialogo.ShowModal() == wx.ID_OK:
            self.EndModal(wx.ID_OK)
        dialogo.Destroy()

class EditarReclamoDialog(wx.Dialog):
    def __init__(self, parent, id_reclamo):
        super().__init__(parent, title="Editar Reclamo", size=(300, 250))
        self.id_reclamo = id_reclamo

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        reclamos = gestion_reclamo.obtener_todos()
        datos = reclamos.get(id_reclamo, {})

        vbox.Add(wx.StaticText(panel, label="Fecha:"), flag=wx.LEFT | wx.TOP, border=10)
        self.txt_fecha = wx.TextCtrl(panel, value=datos.get("fecha", ""))
        vbox.Add(self.txt_fecha, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        vbox.Add(wx.StaticText(panel, label="socio:"), flag=wx.LEFT | wx.TOP, border=10)
        self.txt_socio = wx.TextCtrl(panel, value=datos.get("socio", ""))
        vbox.Add(self.txt_socio, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        vbox.Add(wx.StaticText(panel, label="Detalle:"), flag=wx.LEFT | wx.TOP, border=10)
        self.txt_detalle = wx.TextCtrl(panel, value=datos.get("detalle", ""), style=wx.TE_MULTILINE)
        vbox.Add(self.txt_detalle, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        vbox.Add(wx.StaticText(panel, label="Estado:"), flag=wx.LEFT | wx.TOP, border=10)
        self.combo_estado = wx.ComboBox(panel, choices=["Pendiente", "Realizado", "En Proceso", "Cancelado", "Finalizado"], style=wx.CB_READONLY)
        self.combo_estado.SetValue(datos.get("estado", ""))
        vbox.Add(self.combo_estado, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=10)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        btn_ok = wx.Button(panel, wx.ID_OK, "Guardar")
        btn_cancel = wx.Button(panel, wx.ID_CANCEL, "Cancelar")
        hbox.Add(btn_ok, flag=wx.RIGHT, border=10)
        hbox.Add(btn_cancel)

        vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)
        panel.SetSizer(vbox)

        self.Bind(wx.EVT_BUTTON, self.guardar_cambios, btn_ok)

    def guardar_cambios(self, event):
        fecha = self.txt_fecha.GetValue().strip()
        socio = self.txt_socio.GetValue().strip()
        detalle = self.txt_detalle.GetValue().strip()
        estado = self.combo_estado.GetValue().strip()

        if not fecha or not socio or not detalle or not estado:
            wx.MessageBox("Todos los campos son obligatorios", "Error", wx.OK | wx.ICON_ERROR)
            return

        try:
            gestion_reclamo.editar_reclamo(self.id_reclamo, fecha, socio, detalle, estado)
            wx.MessageBox("Reclamo actualizado con éxito", "Éxito", wx.OK | wx.ICON_INFORMATION)
            self.EndModal(wx.ID_OK)
        except Exception as e:
            wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_ERROR)

class EliminarReclamoDialog(wx.Dialog):
    def __init__(self, parent, id_reclamo, gestion_reclamo):
        super().__init__(parent, title="Eliminar Reclamo", size=(300, 150))
        self.id_reclamo = id_reclamo
        self.parent = parent
        self.gestion_reclamo = gestion_reclamo

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        reclamos = self.gestion_reclamo.obtener_todos()
        reclamo = reclamos.get(str(id_reclamo))

        if reclamo:
            mensaje = f"¿Estás seguro de que deseas eliminar el reclamo con ID '{reclamo['id']}'?"
            vbox.Add(wx.StaticText(panel, label=mensaje), flag=wx.ALL, border=10)

            hbox = wx.BoxSizer(wx.HORIZONTAL)
            btn_ok = wx.Button(panel, wx.ID_OK, "Eliminar")
            btn_cancel = wx.Button(panel, wx.ID_CANCEL, "Cancelar")
            hbox.Add(btn_ok, flag=wx.RIGHT, border=10)
            hbox.Add(btn_cancel)

            vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)
            panel.SetSizer(vbox)

            self.Bind(wx.EVT_BUTTON, self.eliminar_reclamo, btn_ok)
        else:
            wx.MessageBox(f"No se encontró el reclamo con ID {id_reclamo}", "Error", wx.OK | wx.ICON_ERROR)
            self.EndModal(wx.ID_CANCEL)

    def eliminar_reclamo(self, event):
        try:
            self.gestion_reclamo.eliminar_reclamo(self.id_reclamo)
            wx.MessageBox("Reclamo eliminado con éxito", "Éxito", wx.OK | wx.ICON_INFORMATION)
            self.EndModal(wx.ID_OK)
            if hasattr(self.parent, "cargar_reclamos"):
                self.parent.cargar_reclamos()
        except Exception as e:
            wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_ERROR)






class AgregarReclamoDialog(wx.Dialog):
    def __init__(self, parent, id=None, title="Nuevo Reclamo"):
        super().__init__(parent, id=wx.ID_ANY, title=title)
        #self.cargar_socios()
        
        self.id = id
        self.SetTitle(title)

        vbox = wx.BoxSizer(wx.VERTICAL)
        panel = wx.Panel(self)
        grid = wx.GridBagSizer(5, 5)

        # servicio de Reclamo (combo box)
        grid.Add(wx.StaticText(panel, label="servicio de Reclamo:"), pos=(0, 0), flag=wx.ALL, border=5)
        self.combo_servicio = wx.ComboBox(panel, choices=["Luz", "Agua", "Internet", "Cable"], style=wx.CB_READONLY)
        grid.Add(self.combo_servicio, pos=(0, 1), flag=wx.EXPAND | wx.ALL, border=5)

        # Detalle (multilínea)
        grid.Add(wx.StaticText(panel, label="Detalle:"), pos=(1, 0), flag=wx.ALL, border=5)
        self.txt_detalle = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        grid.Add(self.txt_detalle, pos=(1, 1), flag=wx.EXPAND | wx.ALL, border=5)

                # socio
        grid.Add(wx.StaticText(panel, label="socio:"), pos=(2, 0), flag=wx.ALL, border=5)
        self.txt_socio = wx.TextCtrl(panel)
        grid.Add(self.txt_socio, pos=(2, 1), flag=wx.EXPAND | wx.ALL, border=5)

        # Lista desplegable para mostrar los socios encontrados
        self.list_socios = wx.ListBox(panel, style=wx.LB_SINGLE)
        grid.Add(self.list_socios, pos=(3, 1), flag=wx.EXPAND | wx.ALL, border=5)
        self.list_socios.Hide() # Ocultar la lista al inicio

        # Cargar el JSON de socios
        self.cargar_socios()

        # Bindear el evento de cambio de texto
        self.txt_socio.Bind(wx.EVT_TEXT, self.buscar_socio)
        self.list_socios.Bind(wx.EVT_LISTBOX, self.seleccionar_socio)
# Estado (combo box)
        grid.Add(wx.StaticText(panel, label="Estado:"), pos=(3, 0), flag=wx.ALL, border=5)
        self.combo_estado = wx.ComboBox(panel, choices=["Pendiente", "Realizado", "En Proceso", "Cancelado", "Finalizado"], style=wx.CB_READONLY)
        grid.Add(self.combo_estado, pos=(4, 0), flag=wx.EXPAND | wx.ALL, border=5)

        # Botones
        btn_ok = wx.Button(panel, label="Guardar")
        btn_cancel = wx.Button(panel, wx.ID_CANCEL, "Cancelar")
        btn_ok.Bind(wx.EVT_BUTTON, self.guardar_reclamo)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(btn_ok, flag=wx.RIGHT, border=10)
        hbox.Add(btn_cancel)
        self.socios_dict=self.cargar_socios()
        vbox.Add(grid, proportion=1, flag=wx.ALL | wx.EXPAND, border=10)
        vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.ALL, border=10)
        panel.SetSizer(vbox)
        self.Bind(wx.EVT_CHAR_HOOK, self.on_key_down)
        self.Centre()



    def cargar_socios(self):
        self.list_socios.Clear()
        socios = gestion_socio.obtener_todos()  # Suponiendo que devuelve el diccionario JSON
        print("Datos obtenidos de gestion_socio.obtener_todos():")
        print(socios)
        print("servicio de 'socios':", type(socios))  
        socios_dict = {}  # Se crea un diccionario vacío.
        
        if socios:
            for socio in socios.values():  # Iteramos sobre los valores del diccionario
                item_text = f"Código: {socio['id']} - {socio['nombre']} - Domicilio: {socio['domicilio']} - Teléfono: {socio['telefono']}"
                self.list_socios.Append(item_text)
                socios_dict[socio['id']] = socio# Usamos el ID como clave
        
        return socios_dict# Se retorna el diccionario.
    

    def buscar_socio(self, event):
        texto_busqueda = self.txt_socio.GetValue().lower()
        socios_encontrados = []

        if hasattr(self, 'socios_dict'): #verificamos que exista socios_dict
            self.list_socios.Clear() # Limpiamos la lista antes de agregar nuevos resultados
            for socio in self.socios_dict.values(): #iteramos sobre self.socios_dict.values()
                if texto_busqueda in socio["nombre"].lower():
                    item_text = f"{socio['nombre']} - Domicilio: {socio['domicilio']} - Teléfono: {socio['telefono']}"
                    self.list_socios.Append(item_text)
                    socios_encontrados.append(socio["nombre"])

            if socios_encontrados:
                self.list_socios.Show()
            else:
                self.list_socios.Hide()
        else:
            print("Advertencia: self.socios_dict no está inicializado.")
    
    def seleccionar_socio(self, event):
        seleccion = self.list_socios.GetStringSelection()
        self.txt_socio.SetValue(seleccion)
        self.list_socios.Hide()
    def on_key_down(self, event):
        key_code = event.GetKeyCode()
        control_presionado = event.ControlDown()

        if control_presionado and key_code == ord("G"):
            self.guardar_reclamo(None)
        elif control_presionado and key_code == ord("C"):
            self.Close()
        event.Skip()

    def guardar_reclamo(self, event):

        servicio = self.combo_servicio.GetValue().strip()
        detalle = self.txt_detalle.GetValue().strip()
        socio = self.txt_socio.GetValue().strip()
        estado = self.combo_estado.GetValue().strip()

        if not servicio or not detalle or not socio or not estado:
            self.mostrar_mensaje("Error: Todos los campos son obligatorios.", wx.ICON_ERROR)
            return

        try:
            gestion_reclamo.registrar_reclamo(None,servicio, detalle, socio, estado)
            print(f"Reclamo guardado: servicio={servicio}, socio={socio}, Detalle={detalle}, Estado={estado}")
            self.mostrar_mensaje("Reclamo guardado con éxito.", wx.ICON_INFORMATION)

            # Enviar reclamo por WhatsApp
            self.enviar_reclamo_whatsapp(servicio, detalle, socio)

            # Limpiar los campos después de guardar
            self.combo_servicio.SetSelection(0)
            self.txt_detalle.SetValue("")
            self.txt_socio.SetValue("")
            self.combo_estado.SetSelection(0)
        except Exception as e:
            self.mostrar_mensaje(f"Error al guardar el reclamo: {e}", wx.ICON_ERROR)

    def enviar_reclamo_whatsapp(self, servicio, detalle, socio):
        """Envía el reclamo por WhatsApp a un número fijo."""

        numero_telefono = "5493534294632" # Reemplaza con el número fijo.
        mensaje = f"Nuevo reclamo:\nServicio: {servicio}\n- {detalle}\nSocio: {socio}"
        mensaje_codificado = urllib.parse.quote(mensaje)
        url = f"https://wa.me/{numero_telefono}?text={mensaje_codificado}"
        webbrowser.open_new_tab(url)


    def mostrar_mensaje(self, mensaje, servicio=wx.ICON_ERROR):
        wx.MessageBox(mensaje, "Información", style=servicio)