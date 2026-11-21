"""
Módulo: servicios.py
Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ

Autor: Andres Felipe Escobar Yusunguaira
Programa: Ingeniería de Sistemas - UNAD
Curso: Programación (213023) - Fase 4

Clase abstracta Servicio y tres servicios especializados:
    - ReservaSala
    - AlquilerEquipo
    - AsesoriaEspecializada

Se aplican HERENCIA (cada servicio hereda de Servicio), POLIMORFISMO
(cada uno sobrescribe costo_base, describir y validar_parametros) y
SOBRECARGA de métodos (calcular_costo admite varias firmas).

Nota sobre sobrecarga en Python: Python no permite definir dos métodos con
el mismo nombre (el segundo reemplaza al primero). La sobrecarga se
implementa de dos formas idiomáticas:
    1. @typing.overload + parámetros opcionales -> calcular_costo(...)
    2. functools.singledispatchmethod (despacho según el tipo del argumento)
       -> cotizar(...)
"""

from abc import abstractmethod
from functools import singledispatchmethod
from typing import overload

from .entidad import EntidadBase
from .excepciones import (ValidacionError, ParametroFaltanteError,
                          ServicioNoDisponibleError, CalculoInconsistenteError)

IVA = 0.19


class Servicio(EntidadBase):
    """Clase abstracta para todos los servicios de Software FJ."""

    unidad = "unidad"          # unidad de la duración (hora, día...)
    duracion_maxima = 1

    def __init__(self, nombre, tarifa, disponible=True):
        super().__init__()
        if not nombre or not str(nombre).strip():
            raise ParametroFaltanteError("nombre del servicio")
        self._nombre = str(nombre).strip()
        try:
            self._tarifa = float(tarifa)
        except (TypeError, ValueError) as e:
            # Encadenamiento de excepciones: se conserva la causa original
            raise ValidacionError("tarifa", f"'{tarifa}' no es un número") from e
        self._disponible = bool(disponible)
        self.validar()

    # ------------------------------ propiedades ----------------------------
    @property
    def nombre(self):
        return self._nombre

    @property
    def tarifa(self):
        return self._tarifa

    @property
    def disponible(self):
        return self._disponible

    def cambiar_disponibilidad(self, disponible):
        self._disponible = bool(disponible)

    # ---------------------------- abstracción ------------------------------
    def validar(self):
        if self._tarifa <= 0:
            raise ValidacionError("tarifa", "debe ser mayor que cero")
        return True

    @abstractmethod
    def costo_base(self, duracion):
        """Costo sin impuestos ni descuentos (polimórfico)."""

    @abstractmethod
    def describir(self):
        """Descripción del servicio (polimórfico)."""

    def validar_parametros(self, duracion):
        """Validación común; las subclases la extienden con super()."""
        if not self._disponible:
            raise ServicioNoDisponibleError(self._nombre)
        if duracion is None:
            raise ParametroFaltanteError("duracion")
        if not isinstance(duracion, (int, float)) or isinstance(duracion, bool):
            raise ValidacionError("duracion", "debe ser numérica")
        if duracion <= 0:
            raise ValidacionError("duracion", "debe ser mayor que cero")
        if duracion > self.duracion_maxima:
            raise ValidacionError(
                "duracion",
                f"máximo {self.duracion_maxima} {self.unidad}(s) para {self._nombre}")
        return True

    # ------------------- SOBRECARGA 1: @overload --------------------------
    @overload
    def calcular_costo(self, duracion: float) -> float: ...

    @overload
    def calcular_costo(self, duracion: float, impuesto: float) -> float: ...

    @overload
    def calcular_costo(self, duracion: float, impuesto: float,
                       descuento: float) -> float: ...

    def calcular_costo(self, duracion, impuesto=None, descuento=None):
        """
        Variantes:
            calcular_costo(d)            -> costo base
            calcular_costo(d, iva)       -> costo base + impuesto
            calcular_costo(d, iva, desc) -> (base - descuento) + impuesto
        """
        self.validar_parametros(duracion)
        costo = self.costo_base(duracion)

        if descuento is not None:
            if not 0 <= descuento < 1:
                raise ValidacionError("descuento", "debe estar entre 0 y 0.99")
            costo *= (1 - descuento)

        if impuesto is not None:
            if not 0 <= impuesto <= 1:
                raise ValidacionError("impuesto", "debe estar entre 0 y 1")
            costo *= (1 + impuesto)

        if costo <= 0 or costo != costo:  # costo != costo detecta NaN
            raise CalculoInconsistenteError(
                f"costo {costo} para {self._nombre} con duración {duracion}")
        return round(costo, 2)

    # --------------- SOBRECARGA 2: singledispatchmethod -------------------
    @singledispatchmethod
    def cotizar(self, argumento):
        raise ValidacionError("cotizar", f"tipo no soportado: {type(argumento).__name__}")

    @cotizar.register
    def _(self, argumento: int):
        """cotizar(3) -> costo con IVA por defecto."""
        return self.calcular_costo(argumento, IVA)

    @cotizar.register
    def _(self, argumento: float):
        return self.calcular_costo(argumento, IVA)

    @cotizar.register
    def _(self, argumento: dict):
        """cotizar({'duracion': 3, 'descuento': 0.1}) -> costo personalizado."""
        if "duracion" not in argumento:
            raise ParametroFaltanteError("duracion")
        return self.calcular_costo(argumento["duracion"],
                                   argumento.get("impuesto", IVA),
                                   argumento.get("descuento"))


# ============================ SERVICIOS DERIVADOS ===========================
class ReservaSala(Servicio):
    """Reserva de salas por horas."""

    unidad = "hora"
    duracion_maxima = 12

    def __init__(self, nombre, tarifa_hora, capacidad, disponible=True):
        self._capacidad = capacidad
        super().__init__(nombre, tarifa_hora, disponible)

    def validar(self):
        super().validar()
        if not isinstance(self._capacidad, int) or not 1 <= self._capacidad <= 200:
            raise ValidacionError("capacidad", "debe ser un entero entre 1 y 200")
        return True

    def costo_base(self, duracion):
        costo = self._tarifa * duracion
        # Recargo del 10 % por uso extendido (más de 8 horas)
        if duracion > 8:
            costo *= 1.10
        return costo

    def describir(self):
        return (f"Sala '{self._nombre}' para {self._capacidad} personas - "
                f"${self._tarifa:,.0f}/hora")


class AlquilerEquipo(Servicio):
    """Alquiler de equipos por días y cantidad de unidades."""

    unidad = "día"
    duracion_maxima = 30

    def __init__(self, nombre, tarifa_dia, tipo_equipo, cantidad=1, disponible=True):
        self._tipo_equipo = tipo_equipo
        self._cantidad = cantidad
        super().__init__(nombre, tarifa_dia, disponible)

    def validar(self):
        super().validar()
        if not self._tipo_equipo:
            raise ParametroFaltanteError("tipo_equipo")
        if not isinstance(self._cantidad, int) or self._cantidad < 1:
            raise ValidacionError("cantidad", "debe ser un entero mayor o igual a 1")
        return True

    def validar_parametros(self, duracion):
        super().validar_parametros(duracion)
        if duracion != int(duracion):
            raise ValidacionError("duracion", "el alquiler se cobra por días completos")
        return True

    def costo_base(self, duracion):
        costo = self._tarifa * duracion * self._cantidad
        # Descuento por volumen: 5 % desde 7 días
        if duracion >= 7:
            costo *= 0.95
        return costo

    def describir(self):
        return (f"Alquiler '{self._nombre}' ({self._tipo_equipo} x{self._cantidad}) - "
                f"${self._tarifa:,.0f}/día por unidad")


class AsesoriaEspecializada(Servicio):
    """Asesorías por horas, con recargo según el nivel del asesor."""

    unidad = "hora"
    duracion_maxima = 40
    NIVELES = {"junior": 1.0, "senior": 1.5, "experto": 2.0}

    def __init__(self, nombre, tarifa_hora, area, nivel="junior", disponible=True):
        self._area = area
        self._nivel = str(nivel).lower() if nivel else nivel
        super().__init__(nombre, tarifa_hora, disponible)

    def validar(self):
        super().validar()
        if not self._area:
            raise ParametroFaltanteError("area")
        if self._nivel not in self.NIVELES:
            raise ValidacionError("nivel", f"debe ser uno de {list(self.NIVELES)}")
        return True

    def validar_parametros(self, duracion):
        super().validar_parametros(duracion)
        if duracion < 1:
            raise ValidacionError("duracion", "la asesoría mínima es de 1 hora")
        return True

    def costo_base(self, duracion):
        return self._tarifa * duracion * self.NIVELES[self._nivel]

    def describir(self):
        return (f"Asesoría '{self._nombre}' en {self._area} (nivel {self._nivel}) - "
                f"${self._tarifa:,.0f}/hora base")
