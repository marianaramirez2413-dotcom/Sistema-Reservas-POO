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

# EXCEPCIONES ADICIONALES Y ENCADENAMIENTO
# =========================
class ErrorReserva(Exception):
    pass

class ErrorDisponibilidad(Exception):
    pass

# =========================
# CLASE ABSTRACTA ENTIDAD GENERAL
# =========================
# Se crea para cumplir el requisito de "entidad general" sin modificar Cliente/Servicio
class EntidadGeneral(ABC):
    @abstractmethod
    def obtener_identificador(self):
        pass

# =========================
# CLASE RESERVA
# =========================
class Reserva(EntidadGeneral):
    def __init__(self, cliente, servicio, duracion):
        if not cliente or not servicio:
            raise ErrorReserva("Cliente y servicio son obligatorios")
        
        # Simulación de error para mostrar encadenamiento (raise ... from ...)
        try:
            self.duracion = int(duracion)
            if self.duracion <= 0:
                raise ValueError("La duración debe ser mayor a 0")
        except ValueError as e:
            raise ErrorReserva("Error crítico al asignar la duración") from e

        self.cliente = cliente
        self.servicio = servicio
        self.estado = "Pendiente"

    def obtener_identificador(self):
        # Accedemos al atributo privado del cliente usando name mangling para no modificar la clase original
        return f"Reserva de {self.cliente._Cliente__nombre} para {self.servicio.nombre}"

    def confirmar(self):
        if self.estado == "Cancelada":
            raise ErrorDisponibilidad("No se puede confirmar una reserva que ya fue cancelada")
        self.estado = "Confirmada"

    def cancelar(self):
        self.estado = "Cancelada"

    # Simulación de método sobrecargado usando parámetros opcionales
    def calcular_total(self, impuesto=0.0, descuento=0.0):
        costo_base = self.servicio.calcular_costo() * self.duracion
        costo_con_descuento = costo_base - (costo_base * descuento)
        total = costo_con_descuento + (costo_con_descuento * impuesto)
        return total

# =========================
# SIMULACIÓN DE 10 OPERACIONES (Gestión con Listas)
# =========================
if __name__ == "__main__":
    # Manejo de listas internas
    lista_clientes = []
    lista_servicios = []
    lista_reservas = []

    print("\n--- INICIANDO SIMULACIÓN DEL SISTEMA (10 OPERACIONES) ---")

    # Operación 1: Registro válido de cliente
    try:
        c_valido = Cliente("Ana", "ana@mail.com")
        lista_clientes.append(c_valido)
        print("Op 1: Cliente Ana registrado correctamente.")
    except Exception as e:
        registrar_log(f"Op 1 Error: {e}")

    # Operación 2: Registro inválido de cliente (falla)
    try:
        c_invalido = Cliente("", "correo_malo")
        lista_clientes.append(c_invalido)
    except ErrorValidacion as e:
        registrar_log(f"Op 2 Error de validación: {e}")
        print("Op 2: Error al registrar cliente atrapado. El sistema sigue.")

    # Operación 3: Creación de servicio 1
    s_sala_nueva = ServicioSala("Sala A")
    lista_servicios.append(s_sala_nueva)
    print("Op 3: Servicio de Sala creado.")

    # Operación 4: Creación de servicio 2
    s_equipo_nuevo = ServicioEquipo("Proyector")
    lista_servicios.append(s_equipo_nuevo)
    print("Op 4: Servicio de Equipo creado.")

    # Operación 5: Reserva exitosa (Uso de try/except/else/finally)
    try:
        r_exitosa = Reserva(lista_clientes[0], lista_servicios[0], 2)
    except ErrorReserva as e:
        registrar_log(f"Op 5 Error: {e}")
    else:
        lista_reservas.append(r_exitosa)
        print("Op 5 (Else): Reserva exitosa creada y añadida a la lista.")
    finally:
        print("Op 5 (Finally): Bloque de intento de reserva 1 finalizado.")

    # Operación 6: Reserva fallida por datos inválidos (Demuestra encadenamiento)
    try:
        r_fallida_1 = Reserva(lista_clientes[0], lista_servicios[1], "letras")
    except ErrorReserva as e:
        registrar_log(f"Op 6 Error encadenado: {e} - Causa original: {e.__cause__}")
        print("Op 6: Reserva fallida por duración en formato de letras.")

    # Operación 7: Reserva fallida por cliente faltante
    try:
        r_fallida_2 = Reserva(None, lista_servicios[0], 1)
    except ErrorReserva as e:
        registrar_log(f"Op 7 Error: {e}")
        print("Op 7: Reserva fallida por falta de cliente.")

    # Operación 8: Cálculo de costos (Método sobrecargado sin parámetros extra)
    if lista_reservas:
        total_base = lista_reservas[0].calcular_total()
        print(f"Op 8: Total reserva calculado (Costo base): ${total_base}")

    # Operación 9: Cálculo de costos (Método sobrecargado con impuestos y descuentos)
    if lista_reservas:
        total_modificado = lista_reservas[0].calcular_total(impuesto=0.19, descuento=0.10)
        print(f"Op 9: Total reserva calculado (Con variaciones): ${total_modificado}")

    # Operación 10: Intento de confirmación incorrecto
    if lista_reservas:
        try:
            reserva_actual = lista_reservas[0]
            reserva_actual.cancelar()
            reserva_actual.confirmar() # Esto forzará el ErrorDisponibilidad
        except ErrorDisponibilidad as e:
            registrar_log(f"Op 10 Error de disponibilidad: {e}")
            print("Op 10: Error controlado al intentar confirmar una reserva cancelada.")
            
    print("--- SIMULACIÓN FINALIZADA SIN INTERRUPCIONES ---")
