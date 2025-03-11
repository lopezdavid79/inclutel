import json
import os
import sys

from module.Reclamo import Reclamo  # Importa la clase Reclamo

class GestionReclamo:
    def __init__(self, nombre_archivo='Reclamos.json'):
        self.nombre_archivo = nombre_archivo
        self.reclamos = self.cargar_datos()
        if not isinstance(self.reclamos, list):
            self.reclamos = []

    def _obtener_ruta_completa(self):
        """Obtiene la ruta completa al archivo JSON."""
        if getattr(sys, 'frozen', False):
            ruta_base = sys._MEIPASS
        else:
            ruta_base = os.path.abspath('.')
        return os.path.join(ruta_base, 'data', self.nombre_archivo)

    def cargar_datos(self):
        """Carga los reclamos desde el archivo JSON."""
        ruta_completa = self._obtener_ruta_completa()
        if os.path.exists(ruta_completa):
            with open(ruta_completa, 'r', encoding='utf-8') as archivo:
                try:
                    reclamos_lista = json.load(archivo)
                    return reclamos_lista
                except json.JSONDecodeError:
                    print("❌ Error al leer JSON, inicializando una lista vacía.")
                    return []
        else:
            return []

    def guardar_datos(self):
        """Guarda la lista de reclamos en el archivo JSON."""
        ruta_completa = self._obtener_ruta_completa()
        for reclamo in self.reclamos:
            if isinstance(reclamo, dict): # nos aseguramos que es un diccionario
                print(list(reclamo.keys())) # Imprime la lista de claves
            else:
                print("Un elemento en self.reclamos no es un diccionario")
                #print (reclamo) # imprime el elemento para ver que es.
        with open(ruta_completa, 'w', encoding='utf-8') as archivo:
            json.dump(self.reclamos, archivo, indent=4, ensure_ascii=False)

    def registrar_reclamo(self, fecha, servicio, detalle, socio, estado):
        """Registra un nuevo reclamo y lo guarda en la base de datos."""
        nuevo_id = len(self.reclamos) + 1
        nuevo_reclamo = Reclamo(nuevo_id, servicio, detalle, socio, estado) 
        reclamo_dict = nuevo_reclamo.a_diccionario()  # Usamos el método a_diccionario
        #print("Diccionario antes de guardar:", reclamo_dict) # Agregamos esta línea
        self.reclamos.append(reclamo_dict)
        self.guardar_datos()
        print(f"Reclamo registrado: {reclamo_dict}")
        return nuevo_reclamo
    def editar_reclamo(self, id_reclamo, fecha=None, socio=None, detalle=None, estado=None):
        """Edita un reclamo existente."""
        try:
            id_reclamo = int(id_reclamo)
        except ValueError:
            print(f"❌ Error: ID {id_reclamo} no es un número válido")
            return

        reclamo = next((r for r in self.reclamos if r["id"] == id_reclamo), None)

        if not reclamo:
            print(f"❌ Error: Reclamo con ID {id_reclamo} no encontrado")
            return

        if fecha:
            reclamo["fecha"] = fecha
        if socio:
            reclamo["socio"] = socio
        if detalle:
            reclamo["detalle"] = detalle
        if estado:
            reclamo["estado"] = estado

        self.guardar_datos()
        print(f"✅ Reclamo {id_reclamo} actualizado: {reclamo}")

    def obtener_todos(self):
        """Devuelve todos los reclamos como un diccionario indexado."""
        return {str(reclamo["id"]): reclamo for reclamo in self.reclamos}

    def buscar_reclamo(self, id_reclamo):
        """Busca un reclamo por su ID y devuelve su información."""
        for reclamo in self.reclamos:
            if reclamo["id"] == id_reclamo:
                return reclamo
        return None

    def eliminar_reclamo(self, id_reclamo):
        """Elimina un reclamo por su ID."""
        try:
            id_reclamo = int(id_reclamo)
        except ValueError:
            print(f"❌ Error: ID {id_reclamo} no es un número válido")
            return False

        reclamo = next((r for r in self.reclamos if r["id"] == id_reclamo), None)

        if reclamo:
            self.reclamos.remove(reclamo)
            self.guardar_datos()
            print(f"Reclamo con ID {id_reclamo} eliminado.")
            return True

        print(f"Reclamo con ID {id_reclamo} no encontrado.")
        return False