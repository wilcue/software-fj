# -*- coding: utf-8 -*-
"""
Clase Reserva: une cliente + servicio + duración + estado.

Aquí se ven los tres esquemas de bloques pedidos:
  try/except          -> en el constructor
  try/except/else     -> en confirmar()
  try/except/finally  -> en procesar()
y el encadenamiento de excepciones con "raise ... from ...".
"""

from entidades import Cliente, EntidadBase
from excepciones import (CalculoInconsistenteError, ErrorSoftwareFJ,
                         OperacionNoPermitidaError, ReservaInvalidaError,
                         ServicioInvalidoError, ServicioNoDisponibleError)
from registro import log
from servicios import Servicio


class Reserva(EntidadBase):
    _FAMILIA = "reserva"
    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    CANCELADA = "CANCELADA"
    PROCESADA = "PROCESADA"

    def __init__(self, cliente, servicio, horas, **opciones):
        super().__init__()
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva necesita un cliente válido")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva necesita un servicio válido")
        if not isinstance(horas, (int, float)) or isinstance(horas, bool):
            raise ReservaInvalidaError("La duración debe ser numérica")

        # try/except con encadenamiento: el error original queda como "causa".
        try:
            servicio.validar_parametros(horas, **opciones)
        except ServicioInvalidoError as error:
            raise ReservaInvalidaError("Los parámetros no cumplen las reglas del servicio") from error

        self._cliente = cliente
        self._servicio = servicio
        self._horas = horas
        self._opciones = opciones
        self._estado = Reserva.PENDIENTE
        self._costo = None

    @property
    def estado(self):
        return self._estado

    @property
    def costo(self):
        return self._costo

    def confirmar(self):
        """try/except/else: el bloque else solo corre si NO hubo error."""
        try:
            if self._estado != Reserva.PENDIENTE:
                raise OperacionNoPermitidaError(
                    f"Solo se confirma una reserva PENDIENTE (actual: {self._estado})")
            if not self._servicio.disponible:
                raise ServicioNoDisponibleError(
                    f"El servicio '{self._servicio.nombre}' no está disponible")
        except ErrorSoftwareFJ as error:
            log.error("Confirmación fallida en reserva #%s: %s", self.id, error)
            raise
        else:
            self._estado = Reserva.CONFIRMADA
            log.info("Reserva #%s confirmada", self.id)

    def cancelar(self):
        if self._estado in (Reserva.CANCELADA, Reserva.PROCESADA):
            error = OperacionNoPermitidaError(
                f"No se puede cancelar una reserva {self._estado}")
            log.error("Cancelación fallida en reserva #%s: %s", self.id, error)
            raise error
        self._estado = Reserva.CANCELADA
        log.info("Reserva #%s cancelada", self.id)

    def procesar(self, impuesto=None, descuento=0.0):
        """try/except/finally: el finally deja huella aunque algo falle."""
        try:
            if self._estado != Reserva.CONFIRMADA:
                raise OperacionNoPermitidaError(
                    f"Solo se procesa una reserva CONFIRMADA (actual: {self._estado})")
            self._costo = self._servicio.calcular_costo_total(
                self._horas, impuesto, descuento)
        except CalculoInconsistenteError as error:
            # Se cambia de tipo de error pero se conserva el original (from).
            raise ReservaInvalidaError(
                f"No se pudo procesar la reserva #{self.id}") from error
        else:
            self._estado = Reserva.PROCESADA
            log.info("Reserva #%s procesada. Total: $%s", self.id, f"{self._costo:,.2f}")
            return self._costo
        finally:
            log.info("Intento de procesamiento terminado (reserva #%s)", self.id)

    def describir(self):
        total = f"${self._costo:,.2f}" if self._costo is not None else "sin calcular"
        return (f"Reserva #{self.id} [{self._estado}] {self._cliente.nombre} -> "
                f"{self._servicio.nombre}, {self._horas} h, total {total}")
