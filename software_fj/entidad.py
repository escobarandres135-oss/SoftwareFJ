"""
Módulo: entidad.py
Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ

Autor: Andres Felipe Escobar Yusunguaira
Programa: Ingeniería de Sistemas - UNAD
Curso: Programación (213023) - Fase 4

Clase abstracta que representa cualquier entidad general del sistema
(Cliente, Servicio, Reserva). Aplica el principio de ABSTRACCIÓN.
"""

from abc import ABC, abstractmethod
from datetime import datetime
import itertools


class EntidadBase(ABC):
    """Entidad general: todas tienen un id único y una fecha de creación."""

    # Un contador independiente por categoría (Cliente, Servicio, Reserva)
    _contadores = {}

    def __init__(self):
        categoria = self._categoria()
        if categoria not in EntidadBase._contadores:
            EntidadBase._contadores[categoria] = itertools.count(1)
        self._id = next(EntidadBase._contadores[categoria])
        self._fecha_creacion = datetime.now()

    @classmethod
    def _categoria(cls):
        """Clase hija directa de EntidadBase (Cliente, Servicio o Reserva)."""
        for clase in cls.__mro__:
            if EntidadBase in clase.__bases__:
                return clase.__name__
        return cls.__name__

    @property
    def id(self):
        return self._id

    @property
    def fecha_creacion(self):
        return self._fecha_creacion

    @abstractmethod
    def validar(self):
        """Cada entidad define sus propias reglas de validación."""

    @abstractmethod
    def describir(self):
        """Cada entidad sabe describirse a sí misma."""

    def __str__(self):
        return self.describir()
