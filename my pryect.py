# =========================
# IMPORTS
# =========================
from abc import ABC, abstractmethod
from datetime import datetime

# =========================
# LOGS
# =========================
def registrar_log(mensaje):
    with open("log.txt", "a") as archivo:
        archivo.write(f"{datetime.now()} - {mensaje}\n")

# =========================
# EXCEPCIÓN PERSONALIZADA
# =========================
class ErrorValidacion(Exception):
    pass

# =========================
# CLASE CLIENTE
# =========================
class Cliente:
    def __init__(self, nombre, correo):
        if not nombre:
            raise ErrorValidacion("Nombre vacío")
        if "@" not in correo:
            raise ErrorValidacion("Correo inválido")

        self.__nombre = nombre
        self.__correo = correo

    def mostrar_info(self):
        return f"Cliente: {self.__nombre} - {self.__correo}"


# PRUEBA
if __name__ == "__main__":
    try:
        c1 = Cliente("Juan", "juan@mail.com")
        print(c1.mostrar_info())

        c2 = Cliente("", "malcorreo")  # error
    except Exception as e:
        print("Error:", e)
        registrar_log(e)

        # =========================
# CLASE ABSTRACTA SERVICIO
# =========================
class Servicio(ABC):
    def __init__(self, nombre):
        self.nombre = nombre

    @abstractmethod
    def calcular_costo(self):
        pass


    # =========================
# SERVICIOS
# =========================
class ServicioSala(Servicio):
    def calcular_costo(self):
        return 50000

class ServicioEquipo(Servicio):
    def calcular_costo(self):
        return 30000

class ServicioAsesoria(Servicio):
    def calcular_costo(self):
        return 80000


# PRUEBA
if __name__ == "__main__":
    s1 = ServicioSala("Sala")
    print("Costo sala:", s1.calcular_costo())