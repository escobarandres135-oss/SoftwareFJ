"""
Módulo: sistema.py
Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ

Autor: Andres Felipe Escobar Yusunguaira
Programa: Ingeniería de Sistemas - UNAD
Curso: Programación (213023) - Fase 4

Gestor central. Toda la información vive en LISTAS INTERNAS de objetos
(no se usa ninguna base de datos).
"""

from .cliente import Cliente
from .reserva import Reserva
from .excepciones import (ClienteDuplicadoError, ClienteNoEncontradoError,
                          ReservaNoEncontradaError, ValidacionError)
from .logger import registrar_evento


class SistemaSoftwareFJ:

    def __init__(self):
        self.__clientes = []
        self.__servicios = []
        self.__reservas = []
        registrar_evento("===== Sistema Software FJ iniciado =====")

    # -------------------------------- clientes -----------------------------
    def registrar_cliente(self, documento, nombre, correo, telefono):
        if any(c.documento == str(documento).strip() for c in self.__clientes):
            raise ClienteDuplicadoError(documento)
        cliente = Cliente(documento, nombre, correo, telefono)
        self.__clientes.append(cliente)
        registrar_evento(f"Cliente registrado: {cliente.describir()}")
        return cliente

    def buscar_cliente(self, documento):
        for c in self.__clientes:
            if c.documento == str(documento):
                return c
        raise ClienteNoEncontradoError(documento)

    # ------------------------------- servicios -----------------------------
    def agregar_servicio(self, servicio):
        self.__servicios.append(servicio)
        registrar_evento(f"Servicio creado: {servicio.describir()}")
        return servicio

    def buscar_servicio(self, nombre):
        for s in self.__servicios:
            if s.nombre.lower() == nombre.lower():
                return s
        raise ValidacionError("servicio", f"no existe el servicio '{nombre}'")

    # -------------------------------- reservas -----------------------------
    def crear_reserva(self, documento, nombre_servicio, duracion, descuento=None):
        cliente = self.buscar_cliente(documento)
        servicio = self.buscar_servicio(nombre_servicio)
        reserva = Reserva(cliente, servicio, duracion, descuento)
        self.__reservas.append(reserva)
        registrar_evento(f"Reserva creada: {reserva.describir()}")
        return reserva

    def buscar_reserva(self, id_reserva):
        for r in self.__reservas:
            if r.id == id_reserva:
                return r
        raise ReservaNoEncontradaError(id_reserva)

    # --------------------------------- reportes ----------------------------
    @property
    def clientes(self):
        return list(self.__clientes)      # copia: protege la lista interna

    @property
    def servicios(self):
        return list(self.__servicios)

    @property
    def reservas(self):
        return list(self.__reservas)

    def total_facturado(self):
        return sum(r.costo_total for r in self.__reservas
                   if r.estado == Reserva.PROCESADA)
