# -*- coding: utf-8 -*-
"""
GestorFJ: guarda clientes, servicios y reservas en listas internas (sin base
de datos) y ofrece operaciones "seguras": si algo falla, se registra en el
log y el programa sigue funcionando.
"""

from entidades import Cliente
from excepciones import (ClienteInvalidoError, ErrorSoftwareFJ,
                         ParametroFaltanteError, ServicioInvalidoError)
from registro import log
from reservas import Reserva
from servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala


class GestorFJ:
    TIPOS_SERVICIO = {
        "sala": ReservaSala,
        "equipo": AlquilerEquipo,
        "asesoria": AsesoriaEspecializada,
    }

    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    # ------------------------------------------------------------------
    def registrar_cliente(self, nombre, documento, correo, telefono):
        try:
            cliente = Cliente(nombre, documento, correo, telefono)
            if any(c.documento == cliente.documento for c in self.clientes):
                raise ClienteInvalidoError(
                    f"Ya existe un cliente con documento {cliente.documento}")
        except ErrorSoftwareFJ as error:
            log.error("Registro de cliente fallido: %s", error)
            print(f"   [ERROR] {error}")
            return None
        self.clientes.append(cliente)
        log.info("Cliente registrado: %s", cliente.describir())
        print(f"   [OK] {cliente}")
        return cliente

    def crear_servicio(self, tipo, **datos):
        try:
            clase = self.TIPOS_SERVICIO.get(tipo)
            if clase is None:
                raise ServicioInvalidoError(f"Tipo de servicio desconocido: '{tipo}'")
            try:
                servicio = clase(**datos)
            except TypeError as error:   # faltan o sobran argumentos
                raise ParametroFaltanteError(
                    f"Parámetros incompletos para '{tipo}': {error}") from error
        except ErrorSoftwareFJ as error:
            log.error("Creación de servicio fallida: %s", error)
            print(f"   [ERROR] {error}")
            return None
        self.servicios.append(servicio)
        log.info("Servicio creado: %s", servicio.describir())
        print(f"   [OK] {servicio.describir()}")
        return servicio

    def crear_reserva(self, cliente, servicio, horas, **opciones):
        try:
            reserva = Reserva(cliente, servicio, horas, **opciones)
        except ErrorSoftwareFJ as error:
            causa = f" (causa: {error.__cause__})" if error.__cause__ else ""
            log.error("Creación de reserva fallida: %s%s", error, causa)
            print(f"   [ERROR] {error}{causa}")
            return None
        self.reservas.append(reserva)
        log.info("Reserva creada: %s", reserva.describir())
        print(f"   [OK] {reserva}")
        return reserva

    def ejecutar(self, descripcion, accion, *args, **kwargs):
        """Ejecuta confirmar/cancelar/procesar capturando cualquier error propio."""
        try:
            resultado = accion(*args, **kwargs)
        except ErrorSoftwareFJ as error:
            causa = f" (causa: {error.__cause__})" if error.__cause__ else ""
            log.error("%s: %s%s", descripcion, error, causa)
            print(f"   [ERROR] {descripcion}: {error}{causa}")
            return None
        print(f"   [OK] {descripcion}")
        return resultado
