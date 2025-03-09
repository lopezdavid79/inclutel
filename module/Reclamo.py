import datetime

class Reclamo:
    contador_id = 0

    def __init__(self, fecha,tipo, detalle, socio, estado):
        Reclamo.contador_id += 1
        self.id = Reclamo.contador_id
        self.fecha =fecha 
        self.tipo = tipo
        self.detalle = detalle
        self.socio = socio
        estados_validos = ["Pendiente", "En progreso", "Resuelto", "Cancelado"]
        if estado not in estados_validos:
            raise ValueError(f"Estado inválido: {estado}. Debe ser uno de {estados_validos}")
        self.estado = estado

    def __str__(self):
        return f"ID: {self.id}, Fecha: {self.fecha}, Tipo: {self.tipo}, socio: {self.socio}, Detalle: {self.detalle}, Estado: {self.estado}"

    def a_diccionario(self):
        if isinstance(self.fecha, str):
            fecha_datetime = datetime.datetime.fromisoformat(self.fecha)
            return {
                "id": self.id,
                "fecha": fecha_datetime.isoformat(),
                "tipo": self.tipo,
                "socio": self.socio,
                "detalle": self.detalle,
                "estado": self.estado
            }
        else:
            return {
                "id": self.id,
                "fecha": self.fecha.isoformat(),
                "tipo": self.tipo,
                "socio": self.socio,   
                "detalle": self.detalle,
                "estado": self.estado
        }