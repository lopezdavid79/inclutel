import json

class Socio:
    contador_id = 0

    def __init__(self, nombre, domicilio, telefono, n_socio):
        Socio.contador_id += 1
        self.id = Socio.contador_id
        self.nombre = nombre
        self.domicilio = domicilio
        self.telefono = telefono
        self.n_socio = n_socio

    def __str__(self):
        return f"ID: {self.id}, Nombre: {self.nombre}, Domicilio: {self.domicilio}, Teléfono: {self.telefono}, N° Socio: {self.n_socio}"

    def a_diccionario(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "domicilio": self.domicilio,
            "telefono": self.telefono,
            "n_socio": self.n_socio
        }
