# -*- coding: utf-8 -*-
"""
Configuración del archivo de logs.

El enunciado permite usar archivos SOLO para registrar eventos y errores,
por eso este es el único lugar donde el programa escribe en disco.
"""

import logging
import os

RUTA_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "software_fj.log")


def configurar_logger():
    """Crea (o reutiliza) el logger de la aplicación y devuelve la instancia."""
    os.makedirs(os.path.dirname(RUTA_LOG), exist_ok=True)
    logger = logging.getLogger("software_fj")
    if logger.handlers:            # evita duplicar mensajes si se llama dos veces
        return logger
    logger.setLevel(logging.INFO)
    manejador = logging.FileHandler(RUTA_LOG, encoding="utf-8")
    manejador.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s", "%Y-%m-%d %H:%M:%S"))
    logger.addHandler(manejador)
    return logger


log = configurar_logger()
