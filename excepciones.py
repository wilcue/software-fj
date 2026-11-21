# -*- coding: utf-8 -*-
"""
Excepciones personalizadas de Software FJ.

Todas heredan de ErrorSoftwareFJ. Así, en cualquier parte del sistema se
puede atrapar "cualquier error propio de la aplicación" con un solo
except ErrorSoftwareFJ, o ser más específico con cada subclase.
"""


class ErrorSoftwareFJ(Exception):
    """Excepción base de la aplicación."""


class ClienteInvalidoError(ErrorSoftwareFJ):
    """Datos del cliente inválidos (nombre, documento, correo, teléfono...)."""


class ServicioInvalidoError(ErrorSoftwareFJ):
    """Datos o parámetros inválidos al crear o usar un servicio."""


class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """El servicio existe, pero en este momento no se puede reservar."""


class ReservaInvalidaError(ErrorSoftwareFJ):
    """La reserva no se puede crear o procesar con los datos recibidos."""


class OperacionNoPermitidaError(ErrorSoftwareFJ):
    """Se intentó una acción que el estado actual no permite."""


class CalculoInconsistenteError(ErrorSoftwareFJ):
    """Un cálculo de costos dio un resultado o recibió valores incoherentes."""


class ParametroFaltanteError(ErrorSoftwareFJ):
    """Faltan datos obligatorios para completar una operación."""
