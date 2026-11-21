"""
Módulo: reserva.py
Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ

Autor: Andres Felipe Escobar Yusunguaira
Programa: Ingeniería de Sistemas - UNAD
Curso: Programación (213023) - Fase 4

Clase Reserva: integra cliente, servicio, duración y estado.
Ciclo de vida:  PENDIENTE -> CONFIRMADA -> PROCESADA
                PENDIENTE / CONFIRMADA -> CANCELADA
"""

from .entidad import EntidadBase
from .cliente import Cliente
from .servicios import Servicio, IVA
from .excepciones import (ValidacionError, OperacionNoPermitidaError,
                          ReservaError, SoftwareFJError)
from .logger import registrar_evento, registrar_error


class Reserva(EntidadBase):
    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    CANCELADA = "CANCELADA"
    PROCESADA = "PROCESADA"

    def __init__(self, cliente, servicio, duracion, descuento=None):
        super().__init__()
        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._descuento = descuento
        self._estado = Reserva.PENDIENTE
        self._costo_total = None
        self.validar()

    # ------------------------------ propiedades ----------------------------
    @property
    def cliente(self):
        return self._cliente

    @property
    def servicio(self):
        return self._servicio

    @property
    def estado(self):
        return self._estado

    @property
    def costo_total(self):
        return self._costo_total

    # ------------------------------- validación ----------------------------
    def validar(self):
        if not isinstance(self._cliente, Cliente):
            raise ValidacionError("cliente", "debe ser un objeto Cliente válido")
        if not isinstance(self._servicio, Servicio):
            raise ValidacionError("servicio", "debe ser un objeto Servicio válido")
        # Delega la validación de la duración al servicio (polimorfismo)
        self._servicio.validar_parametros(self._duracion)
        return True

    # ------------------------------ operaciones ----------------------------
    def confirmar(self):
        """Confirma la reserva y calcula su costo (try / except / else)."""
        if self._estado != Reserva.PENDIENTE:
            raise OperacionNoPermitidaError("confirmar", self._estado)
        try:
            costo = self._servicio.calcular_costo(self._duracion, IVA, self._descuento)
        except SoftwareFJError as e:
            # Encadenamiento: el error de cálculo se envuelve en un ReservaError
            raise ReservaError(
                f"No se pudo confirmar la reserva #{self.id}") from e
        else:
            # Solo se ejecuta si el cálculo fue exitoso
            self._costo_total = costo
            self._estado = Reserva.CONFIRMADA
            registrar_evento(f"Reserva #{self.id} CONFIRMADA - total ${costo:,.2f}")
            return costo

    def cancelar(self, motivo="Sin motivo"):
        if self._estado in (Reserva.CANCELADA, Reserva.PROCESADA):
            raise OperacionNoPermitidaError("cancelar", self._estado)
        self._estado = Reserva.CANCELADA
        registrar_evento(f"Reserva #{self.id} CANCELADA - motivo: {motivo}")

    def procesar(self):
        """Procesa (cobra) la reserva (try / except / finally)."""
        registrar_evento(f"Inicio de procesamiento de la reserva #{self.id}")
        try:
            if self._estado != Reserva.CONFIRMADA:
                raise OperacionNoPermitidaError("procesar", self._estado)
            if not self._servicio.disponible:
                raise ReservaError(
                    f"El servicio '{self._servicio.nombre}' dejó de estar disponible")
            self._estado = Reserva.PROCESADA
            registrar_evento(f"Reserva #{self.id} PROCESADA correctamente")
            return True
        except SoftwareFJError as e:
            registrar_error(e, f"Procesando reserva #{self.id}")
            raise
        finally:
            # Se ejecuta siempre, haya error o no
            registrar_evento(
                f"Fin de procesamiento de la reserva #{self.id} (estado: {self._estado})")

    def describir(self):
        costo = f"${self._costo_total:,.2f}" if self._costo_total else "sin calcular"
        return (f"Reserva #{self.id} [{self._estado}] - {self._cliente.nombre} | "
                f"{self._servicio.nombre} x {self._duracion} {self._servicio.unidad}(s) | "
                f"Total: {costo}")
