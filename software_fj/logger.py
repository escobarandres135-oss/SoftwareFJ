"""
Módulo: logger.py
Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ

Autor: Andres Felipe Escobar Yusunguaira
Programa: Ingeniería de Sistemas - UNAD
Curso: Programación (213023) - Fase 4

Registro de eventos y errores en un archivo de texto (logs). Es el único
uso de archivos del sistema: no se usa ninguna base de datos.
"""

import logging
import os

RUTA_LOG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "logs", "software_fj.log")


def configurar_logger(ruta=RUTA_LOG):
    """Crea (una sola vez) el logger del sistema que escribe en archivo."""
    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    logger = logging.getLogger("SoftwareFJ")
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        manejador = logging.FileHandler(ruta, encoding="utf-8")
        formato = logging.Formatter(
            "%(asctime)s | %(levelname)-8s | %(message)s", "%Y-%m-%d %H:%M:%S"
        )
        manejador.setFormatter(formato)
        logger.addHandler(manejador)
    return logger


log = configurar_logger()


def registrar_evento(mensaje):
    log.info(mensaje)


def registrar_advertencia(mensaje):
    log.warning(mensaje)


def registrar_error(error, contexto=""):
    """Registra un error incluyendo, si existe, la causa encadenada."""
    texto = f"{contexto} -> {type(error).__name__}: {error}" if contexto else \
        f"{type(error).__name__}: {error}"
    causa = error.__cause__
    if causa is not None:
        texto += f" | Causa original: {type(causa).__name__}: {causa}"
    log.error(texto)
