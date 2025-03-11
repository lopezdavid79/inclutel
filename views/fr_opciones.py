import wx
import pickle

DATA_FILE = "data.pkl"
telefono_global = ""  # Variable global para almacenar el número

def save_phone_number(phone_number):
    """Guarda el número de teléfono en el archivo y actualiza la variable global."""
    global telefono_global  # Indica que se usará la variable global
    telefono_global = phone_number
    with open(DATA_FILE, "wb") as file:
        pickle.dump({"phone_number": phone_number}, file)

def load_phone_number():
    """Carga el número de teléfono del archivo y lo almacena en la variable global."""
    global telefono_global  # Indica que se usará la variable global
    try:
        with open(DATA_FILE, "rb") as file:
            data = pickle.load(file)
            telefono_global = data.get("phone_number", "")
            return telefono_global
    except (FileNotFoundError, EOFError):
        telefono_global = ""
        return ""

class Opciones(wx.Frame):
    def __init__(self, parent=None):
        super().__init__(parent, title="Guardar Número de Teléfono", size=(350, 200))
        panel = wx.Panel(self)

        vbox = wx.BoxSizer(wx.VERTICAL)

        self.label = wx.StaticText(panel, label="Ingrese su número de teléfono:")
        vbox.Add(self.label, flag=wx.ALL, border=10)

        self.phone_text = wx.TextCtrl(panel)
        self.phone_text.SetValue(load_phone_number())  # Carga el valor inicial

        vbox.Add(self.phone_text, flag=wx.EXPAND | wx.ALL, border=10)

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.save_button = wx.Button(panel, label="Guardar")
        self.save_button.Bind(wx.EVT_BUTTON, self.on_save)
        hbox.Add(self.save_button, flag=wx.RIGHT, border=10)

        self.cancel_button = wx.Button(panel, label="Cancelar")
        self.cancel_button.Bind(wx.EVT_BUTTON, self.on_cancel)
        hbox.Add(self.cancel_button, flag=wx.LEFT, border=10)

        vbox.Add(hbox, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

        panel.SetSizer(vbox)

        self.Show()

    def on_save(self, event):
        phone_number = self.phone_text.GetValue()
        save_phone_number(phone_number)
        wx.MessageBox("Número guardado exitosamente", "Éxito", wx.OK | wx.ICON_INFORMATION)

    def on_cancel(self, event):
        self.Close()

# Clase de gestión de reclamos (ejemplo)
class GestionReclamos:
    def __init__(self):
        self.numero_telefono = telefono_global  # Accede a la variable global

    def mostrar_telefono(self):
        print(f"Número de teléfono para reclamos: {self.numero_telefono}")


    
