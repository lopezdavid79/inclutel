
import json
import os
import sys
from module.Socio import Socio

class GestionSocio:
    def __init__(self, nombre_archivo='Socios.json'):
        self.nombre_archivo = nombre_archivo
        self.socios = self.cargar_datos()
        if not isinstance(self.socios, list):
            self.socios = []

    def _obtener_ruta_completa(self):
        """Obtiene la ruta completa al archivo JSON."""
        if getattr(sys, 'frozen', False):
            ruta_base = sys._MEIPASS
        else:
            ruta_base = os.path.abspath('.')
        return os.path.join(ruta_base, 'data', self.nombre_archivo)

    def cargar_datos(self):
        """Carga los socios desde el archivo JSON."""
        ruta_completa = self._obtener_ruta_completa()
        if os.path.exists(ruta_completa):
            with open(ruta_completa, 'r', encoding='utf-8') as archivo:
                try:
                    socios_lista = json.load(archivo)
                    return socios_lista
                except json.JSONDecodeError:
                    print("❌ Error al leer JSON, inicializando una lista vacía.")
                    return []
        else:
            return []

    def guardar_datos(self):
        """Guarda la lista de socios en el archivo JSON."""
        ruta_completa = self._obtener_ruta_completa()
        for socio in self.socios:
            if isinstance(socio, dict):
                print(list(socio.keys()))
            else:
                print("Un elemento en self.socios no es un diccionario")
        with open(ruta_completa, 'w', encoding='utf-8') as archivo:
            json.dump(self.socios, archivo, indent=4, ensure_ascii=False)

    def registrar_socio(self, nombre, domicilio, telefono, n_socio):
        nuevo_id = len(self.socios) + 1
        """Registra un nuevo socio y lo guarda en la base de datos."""
        nuevo_socio = Socio(nuevo_id,nombre, domicilio, telefono, n_socio)
        socio_dict = nuevo_socio.a_diccionario()
        self.socios.append(socio_dict)
        self.guardar_datos()
        print(f"Socio registrado: {socio_dict}")
        return nuevo_socio

    def editar_socio(self, id_socio, nombre=None, domicilio=None, telefono=None, n_socio=None):
        """Edita un socio existente."""
        try:
            id_socio = int(id_socio)
        except ValueError:
            print(f"❌ Error: ID {id_socio} no es un número válido")
            return

        socio = next((s for s in self.socios if s["id"] == id_socio), None)

        if not socio:
            print(f"❌ Error: Socio con ID {id_socio} no encontrado")
            return

        if nombre:
            socio["nombre"] = nombre
        if domicilio:
            socio["domicilio"] = domicilio
        if telefono:
            socio["telefono"] = telefono
        if n_socio:
            socio["n_socio"] = n_socio

        self.guardar_datos()
        print(f"✅ Socio {id_socio} actualizado: {socio}")

    def obtener_todos(self):
        """Devuelve todos los socios como un diccionario indexado."""
        return {str(socio["id"]): socio for socio in self.socios}

    def buscar_socio(self, id_socio):
        """Busca un socio por su ID y devuelve su información."""
        for socio in self.socios:
            if socio["id"] == id_socio:
                return socio
        return None

    def eliminar_socio(self, id_socio):
        """Elimina un socio por su ID."""
        try:
            id_socio = int(id_socio)
        except ValueError:
            print(f"❌ Error: ID {id_socio} no es un número válido")
            return False

        socio = next((s for s in self.socios if s["id"] == id_socio), None)

        if socio:
            self.socios.remove(socio)
            self.guardar_datos()
            print(f"Socio con ID {id_socio} eliminado.")
            return True

        print(f"Socio con ID {id_socio} no encontrado.")
        return False
