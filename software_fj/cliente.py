"""
Módulo: cliente.py
Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ

Autor: Andres Felipe Escobar Yusunguaira
Programa: Ingeniería de Sistemas - UNAD
Curso: Programación (213023) - Fase 4

Clase Cliente con ENCAPSULACIÓN de datos personales (atributos privados
y propiedades con validación en cada asignación).
"""

import re

from .entidad import EntidadBase
from .excepciones import ValidacionError, ParametroFaltanteError

PATRON_CORREO = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")


class Cliente(EntidadBase):
    """Cliente de Software FJ."""

    def __init__(self, documento=None, nombre=None, correo=None, telefono=None):
        super().__init__()
        # Los setters validan cada dato; si algo falla se lanza excepción
        # y el objeto nunca queda en un estado inválido.
        self.documento = documento
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        self.validar()

    # ------------------------------ documento ------------------------------
    @property
    def documento(self):
        return self.__documento

    @documento.setter
    def documento(self, valor):
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError("documento")
        valor = str(valor).strip()
        if not valor.isdigit() or not 6 <= len(valor) <= 10:
            raise ValidacionError("documento",
                                  "debe ser numérico y tener entre 6 y 10 dígitos")
        self.__documento = valor

    # -------------------------------- nombre -------------------------------
    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError("nombre")
        valor = " ".join(str(valor).split())
        if len(valor) < 3 or not all(c.isalpha() or c == " " for c in valor):
            raise ValidacionError("nombre",
                                  "solo admite letras y mínimo 3 caracteres")
        self.__nombre = valor.title()

    # -------------------------------- correo -------------------------------
    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError("correo")
        valor = str(valor).strip().lower()
        if not PATRON_CORREO.match(valor):
            raise ValidacionError("correo", f"'{valor}' no tiene formato válido")
        self.__correo = valor

    # ------------------------------- teléfono ------------------------------
    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        if valor is None or str(valor).strip() == "":
            raise ParametroFaltanteError("telefono")
        valor = str(valor).strip()
        if not valor.isdigit() or len(valor) != 10:
            raise ValidacionError("telefono", "debe tener exactamente 10 dígitos")
        self.__telefono = valor

    # ------------------------- métodos de la entidad -----------------------
    def validar(self):
        # Las validaciones individuales ya se hicieron en los setters; aquí se
        # verifica la coherencia del objeto completo.
        return all([self.__documento, self.__nombre, self.__correo, self.__telefono])

    def describir(self):
        # Se enmascara el documento para proteger el dato personal
        doc_oculto = "*" * (len(self.__documento) - 4) + self.__documento[-4:]
        return f"Cliente #{self.id}: {self.__nombre} (doc {doc_oculto}, {self.__correo})"
