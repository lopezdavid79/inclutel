import datetime

class Reclamo:
    def __init__(self, id, servicio, detalle, socio, estado):
        self.id = id
        self.fecha = datetime.date.today()  # Establece la fecha actual
        self.servicio = servicio
        self.detalle = detalle
        self.socio = socio
        estados_validos = ["Pendiente", "En progreso", "Resuelto", "Cancelado"]
        if estado not in estados_validos:
            raise ValueError(f"Estado inválido: {estado}. Debe ser uno de {estados_validos}")
        self.estado = estado

    def __str__(self):
        return f"ID: {self.id}, Fecha: {self.fecha.strftime('%d-%m-%Y')}, servicio: {self.servicio}, socio: {self.socio}, Detalle: {self.detalle}, Estado: {self.estado}"

    def a_diccionario(self):
        return {
            "id": self.id,
            "fecha": self.fecha.strftime('%d-%m-%Y'),  # Ahora se guarda en formato día-mes-año
            "servicio": self.servicio,
            "socio": self.socio,
            "detalle": self.detalle,
            "estado": self.estado
        }
