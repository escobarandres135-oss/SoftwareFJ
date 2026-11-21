"""
Módulo: excepciones.py
Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ

Autor: Andres Felipe Escobar Yusunguaira
Programa: Ingeniería de Sistemas - UNAD
Curso: Programación (213023) - Fase 4

Jerarquía de excepciones personalizadas del sistema. Todas heredan de
SoftwareFJError, lo que permite capturarlas de forma general o específica.
"""


class SoftwareFJError(Exception):
    """Excepción base de todo el sistema Software FJ."""

    def __init__(self, mensaje, codigo="SFJ-000"):
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.codigo = codigo

    def __str__(self):
        return f"[{self.codigo}] {self.mensaje}"


# ---------------------- Errores de datos / validación ----------------------
class ValidacionError(SoftwareFJError):
    """Se lanza cuando un dato no cumple las reglas de validación."""

    def __init__(self, campo, mensaje):
        super().__init__(f"Campo '{campo}': {mensaje}", "SFJ-100")
        self.campo = campo


class ParametroFaltanteError(ValidacionError):
    """Se lanza cuando falta un parámetro obligatorio."""

    def __init__(self, campo):
        super().__init__(campo, "es obligatorio y no fue suministrado")
        self.codigo = "SFJ-101"


# ---------------------------- Errores de clientes ---------------------------
class ClienteError(SoftwareFJError):
    """Errores relacionados con la gestión de clientes."""

    def __init__(self, mensaje):
        super().__init__(mensaje, "SFJ-200")


class ClienteDuplicadoError(ClienteError):
    def __init__(self, documento):
        super().__init__(f"Ya existe un cliente con documento {documento}")
        self.codigo = "SFJ-201"


class ClienteNoEncontradoError(ClienteError):
    def __init__(self, documento):
        super().__init__(f"No existe un cliente con documento {documento}")
        self.codigo = "SFJ-202"


# --------------------------- Errores de servicios ---------------------------
class ServicioError(SoftwareFJError):
    """Errores relacionados con servicios."""

    def __init__(self, mensaje):
        super().__init__(mensaje, "SFJ-300")


class ServicioNoDisponibleError(ServicioError):
    def __init__(self, nombre):
        super().__init__(f"El servicio '{nombre}' no está disponible")
        self.codigo = "SFJ-301"


class CalculoInconsistenteError(ServicioError):
    """Se lanza cuando un cálculo de costos produce un valor ilógico."""

    def __init__(self, detalle):
        super().__init__(f"Cálculo inconsistente: {detalle}")
        self.codigo = "SFJ-302"


# ---------------------------- Errores de reservas ---------------------------
class ReservaError(SoftwareFJError):
    """Errores relacionados con reservas."""

    def __init__(self, mensaje):
        super().__init__(mensaje, "SFJ-400")


class OperacionNoPermitidaError(ReservaError):
    """Se lanza al intentar una transición de estado inválida."""

    def __init__(self, operacion, estado_actual):
        super().__init__(
            f"No se puede '{operacion}' una reserva en estado '{estado_actual}'"
        )
        self.codigo = "SFJ-401"


class ReservaNoEncontradaError(ReservaError):
    def __init__(self, id_reserva):
        super().__init__(f"No existe la reserva con id {id_reserva}")
        self.codigo = "SFJ-402"
