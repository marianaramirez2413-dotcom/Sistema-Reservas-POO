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

# =========================
# NUEVAS EXCEPCIONES PERSONALIZADAS
# =========================
class ClienteNoEncontradoError(Exception):
    pass

class ServicioNoDisponibleError(Exception):
    pass

class ReservaInvalidaError(Exception):
    pass

class OperacionNoPermitidaError(Exception):
    pass

# =========================
# CLASE RESERVA (con sobrecarga de métodos)
# =========================
class Reserva:
    def __init__(self, id_reserva, cliente, servicio, duracion):
        self._id = id_reserva
        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion  # en horas, o días según servicio
        self._estado = "PENDIENTE"  # valores: PENDIENTE, CONFIRMADA, CANCELADA, COMPLETADA

    # Métodos principales
    def confirmar(self):
        if self._estado != "PENDIENTE":
            raise OperacionNoPermitidaError(f"No se puede confirmar reserva en estado {self._estado}")
        # Simular que el servicio siempre está disponible (porque no tienen atributo disponible)
        self._estado = "CONFIRMADA"
        registrar_log(f"Reserva {self._id} confirmada")

    def cancelar(self):
        if self._estado in ["CANCELADA", "COMPLETADA"]:
            raise OperacionNoPermitidaError(f"No se puede cancelar reserva en estado {self._estado}")
        self._estado = "CANCELADA"
        registrar_log(f"Reserva {self._id} cancelada")

    def procesar(self):
        if self._estado != "CONFIRMADA":
            raise ReservaInvalidaError("Solo se pueden procesar reservas confirmadas")
        # Simulación de procesamiento exitoso
        self._estado = "COMPLETADA"
        registrar_log(f"Reserva {self._id} procesada exitosamente")

    # Sobrecarga de calcular_costo_total (usando parámetros opcionales)
    def calcular_costo_total(self, impuesto=0.0, descuento=0.0):
        """
        Uso:
        - costo_base = reserva.calcular_costo_total()
        - con impuesto: reserva.calcular_costo_total(impuesto=21)
        - con impuesto y descuento: reserva.calcular_costo_total(impuesto=21, descuento=10)
        """
        costo_base = self._servicio.calcular_costo()  # usa el costo fijo del servicio
        total = costo_base * (1 + impuesto / 100)
        total = total * (1 - descuento / 100)
        return total

    # Otra "sobrecarga": método con nombre diferente (simulando sobrecarga por tipo)
    def calcular_costo_con_iva(self):
        return self.calcular_costo_total(impuesto=21)

    def mostrar_info(self):
        return f"Reserva {self._id}: {self._cliente.mostrar_info()} - Servicio: {self._servicio.nombre} - Estado: {self._estado}"

# =========================
# CLASE SISTEMA (gestiona listas y operaciones)
# =========================
class SistemaGestion:
    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []
        self._contador_clientes = 1
        self._contador_reservas = 1

    def registrar_cliente(self, nombre, correo):
        """Intenta registrar un cliente. Retorna el cliente o None si falla."""
        try:
            cliente = Cliente(nombre, correo)
            # Le asignamos un ID interno (no está en la clase Cliente, lo manejamos aparte)
            cliente.id = self._contador_clientes  # agregamos atributo dinámicamente
            self.clientes.append(cliente)
            self._contador_clientes += 1
            registrar_log(f"Cliente registrado: {cliente.mostrar_info()}")
            return cliente
        except ErrorValidacion as e:
            registrar_log(f"Error al registrar cliente: {str(e)}")
            print(f"[ERROR] {e}")
            return None

    def agregar_servicio(self, servicio):
        self.servicios.append(servicio)
        registrar_log(f"Servicio agregado: {servicio.nombre} - Costo base: {servicio.calcular_costo()}")

    def buscar_cliente_por_id(self, id_cliente):
        for c in self.clientes:
            if hasattr(c, 'id') and c.id == id_cliente:
                return c
        raise ClienteNoEncontradoError(f"Cliente con ID {id_cliente} no existe")

    def buscar_servicio_por_nombre(self, nombre):
        for s in self.servicios:
            if s.nombre == nombre:
                return s
        raise ServicioNoDisponibleError(f"Servicio {nombre} no encontrado")

    def crear_reserva(self, id_cliente, nombre_servicio, duracion):
        try:
            cliente = self.buscar_cliente_por_id(id_cliente)
            servicio = self.buscar_servicio_por_nombre(nombre_servicio)
            # Crear reserva
            id_reserva = self._contador_reservas
            reserva = Reserva(id_reserva, cliente, servicio, duracion)
            self.reservas.append(reserva)
            self._contador_reservas += 1
            registrar_log(f"Reserva creada: {reserva.mostrar_info()}")
            return reserva
        except (ClienteNoEncontradoError, ServicioNoDisponibleError) as e:
            registrar_log(f"Error al crear reserva: {str(e)}")
            print(f"[ERROR] {e}")
            return None
        except Exception as e:
            registrar_log(f"Error inesperado al crear reserva: {str(e)}")
            print(f"[ERROR] Inesperado: {e}")
            return None

    def confirmar_reserva(self, id_reserva):
        reserva = self._buscar_reserva_por_id(id_reserva)
        if reserva:
            try:
                reserva.confirmar()
                print(f"Reserva {id_reserva} confirmada")
            except OperacionNoPermitidaError as e:
                registrar_log(str(e))
                print(f"[ERROR] {e}")

    def cancelar_reserva(self, id_reserva):
        reserva = self._buscar_reserva_por_id(id_reserva)
        if reserva:
            try:
                reserva.cancelar()
                print(f"Reserva {id_reserva} cancelada")
            except OperacionNoPermitidaError as e:
                registrar_log(str(e))
                print(f"[ERROR] {e}")

    def procesar_reserva(self, id_reserva):
        reserva = self._buscar_reserva_por_id(id_reserva)
        if reserva:
            try:
                reserva.procesar()
                print(f"Reserva {id_reserva} procesada")
            except ReservaInvalidaError as e:
                registrar_log(str(e))
                print(f"[ERROR] {e}")

    def _buscar_reserva_por_id(self, id_reserva):
        for r in self.reservas:
            if r._id == id_reserva:
                return r
        registrar_log(f"Intento de buscar reserva inexistente: {id_reserva}")
        print(f"[ERROR] Reserva {id_reserva} no existe")
        return None

# =========================
# SIMULACIÓN DE 10 OPERACIONES (válidas e inválidas)
# =========================
def simulacion():
    print("=== INICIO DE SIMULACIÓN DE 10 OPERACIONES ===\n")
    sistema = SistemaGestion()

    # 1. Registrar cliente válido
    print("1. Registrar cliente válido (Ana López, ana@mail.com)")
    cliente1 = sistema.registrar_cliente("Ana López", "ana@mail.com")

    # 2. Registrar cliente con correo inválido (debe fallar)
    print("\n2. Registrar cliente con correo inválido (juan, sin @)")
    cliente2 = sistema.registrar_cliente("Juan", "juansinarroba")

    # 3. Registrar cliente válido (Carlos)
    print("\n3. Registrar cliente válido (Carlos, carlos@mail.com)")
    cliente3 = sistema.registrar_cliente("Carlos", "carlos@mail.com")

    # 4. Agregar servicios
    print("\n4. Agregar servicios: Sala, Equipo, Asesoría")
    sistema.agregar_servicio(ServicioSala("Sala"))
    sistema.agregar_servicio(ServicioEquipo("Equipo"))
    sistema.agregar_servicio(ServicioAsesoria("Asesoria"))

    # 5. Crear reserva válida (cliente1 con Sala, duración 2)
    print("\n5. Crear reserva (Cliente Ana, servicio Sala, duración 2)")
    reserva1 = sistema.crear_reserva(id_cliente=1, nombre_servicio="Sala", duracion=2)
    if reserva1:
        print(f"   Costo base: {reserva1.calcular_costo_total():.2f}")
        print(f"   Con 21% IVA: {reserva1.calcular_costo_total(impuesto=21):.2f}")
        print(f"   Con descuento 10%: {reserva1.calcular_costo_total(descuento=10):.2f}")
        print(f"   Con IVA + descuento: {reserva1.calcular_costo_total(impuesto=21, descuento=10):.2f}")

    # 6. Crear reserva con cliente inexistente (ID 99) -> debe fallar
    print("\n6. Crear reserva con cliente ID 99 (inexistente)")
    reserva_invalida1 = sistema.crear_reserva(99, "Sala", 1)

    # 7. Crear reserva con servicio inexistente -> debe fallar
    print("\n7. Crear reserva con servicio 'Fotocopiadora' (inexistente)")
    reserva_invalida2 = sistema.crear_reserva(1, "Fotocopiadora", 1)

    # 8. Confirmar reserva1
    print("\n8. Confirmar reserva1")
    sistema.confirmar_reserva(reserva1._id)

    # 9. Cancelar reserva1 (ahora está confirmada, se puede cancelar)
    print("\n9. Cancelar reserva1")
    sistema.cancelar_reserva(reserva1._id)

    # 10. Intentar procesar reserva1 (está cancelada, debe fallar)
    print("\n10. Intentar procesar reserva1 (ya cancelada)")
    sistema.procesar_reserva(reserva1._id)

    # Operación extra para mostrar manejo de finally (demostración)
    print("\n--- Demostración de try/except/finally ---")
    try:
        archivo = open("demo.txt", "w")
        archivo.write("Prueba de finally")
    except Exception as e:
        registrar_log(f"Error en demo: {e}")
    finally:
        if 'archivo' in locals() and not archivo.closed:
            archivo.close()
            print("Archivo cerrado correctamente (finally)")

    print("\n=== SIMULACIÓN FINALIZADA ===")
    print("Revise el archivo 'log.txt' para ver todos los eventos y errores.")

# Ejecutar simulación
if __name__ == "__main__":
    simulacion()
