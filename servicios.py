# -*- coding: utf-8 -*-
"""
Servicio (clase abstracta) y tres servicios especializados.

Polimorfismo: la reserva solo conoce "un Servicio" y le pide calcular el
costo, describirse o validar parámetros; cada hijo responde a su manera.
"""

from abc import abstractmethod

from entidades import EntidadBase
from excepciones import (CalculoInconsistenteError, ServicioInvalidoError)

IVA_POR_DEFECTO = 0.19   # 19 % de IVA en Colombia


class Servicio(EntidadBase):
    """Clase abstracta de la que heredan todos los servicios de la empresa."""

    _FAMILIA = "servicio"

    def __init__(self, nombre, tarifa_hora, disponible=True):
        super().__init__()
        if not isinstance(nombre, str) or not nombre.strip():
            raise ServicioInvalidoError("El servicio necesita un nombre")
        if not isinstance(tarifa_hora, (int, float)) or isinstance(tarifa_hora, bool) \
                or tarifa_hora <= 0:
            raise ServicioInvalidoError("La tarifa por hora debe ser un número mayor que cero")
        self.nombre = nombre.strip()
        self._tarifa_hora = float(tarifa_hora)
        self._disponible = bool(disponible)

    @property
    def tarifa_hora(self):
        return self._tarifa_hora

    @property
    def disponible(self):
        return self._disponible

    def cambiar_disponibilidad(self, valor):
        self._disponible = bool(valor)

    # --- métodos que cada hijo DEBE sobrescribir -----------------------------
    @abstractmethod
    def calcular_costo(self, horas):
        """Costo base (sin impuestos ni descuentos) para esa duración."""

    @abstractmethod
    def validar_parametros(self, horas, **opciones):
        """Lanza ServicioInvalidoError si la duración u opciones no sirven."""

    # --- sobrecarga simulada -------------------------------------------------
    def calcular_costo_total(self, horas, impuesto=None, descuento=0.0):
        """
        Un solo nombre, varias formas de llamarlo (Python no tiene sobrecarga
        clásica, así que se simula con parámetros opcionales):

            s.calcular_costo_total(3)                      -> costo + IVA 19 %
            s.calcular_costo_total(3, descuento=0.10)      -> con 10 % de descuento
            s.calcular_costo_total(3, impuesto=0.0)        -> sin impuesto
            s.calcular_costo_total(3, 0.05, 0.10)          -> impuesto 5 %, descuento 10 %
        """
        if impuesto is None:
            impuesto = IVA_POR_DEFECTO
        if not 0 <= impuesto <= 1:
            raise CalculoInconsistenteError(f"Impuesto fuera de rango (0 a 1): {impuesto}")
        if not 0 <= descuento < 1:
            raise CalculoInconsistenteError(f"Descuento fuera de rango (0 a 0.99): {descuento}")
        base = self.calcular_costo(horas)
        total = base * (1 - descuento) * (1 + impuesto)
        if total <= 0:
            raise CalculoInconsistenteError("El costo total resultó menor o igual a cero")
        return round(total, 2)


class ReservaSala(Servicio):
    """Reserva de salas: el costo depende de las horas y hay límite de aforo."""

    def __init__(self, nombre, tarifa_hora, capacidad, disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        if not isinstance(capacidad, int) or capacidad < 1:
            raise ServicioInvalidoError("La capacidad de la sala debe ser un entero positivo")
        self.capacidad = capacidad

    def calcular_costo(self, horas):
        return self.tarifa_hora * horas

    def validar_parametros(self, horas, **opciones):
        if not 1 <= horas <= 8:
            raise ServicioInvalidoError("Una sala se reserva entre 1 y 8 horas")
        asistentes = opciones.get("asistentes", 1)
        if asistentes > self.capacidad:
            raise ServicioInvalidoError(
                f"{asistentes} asistentes superan la capacidad ({self.capacidad})")

    def describir(self):
        return f"Sala '{self.nombre}' (capacidad {self.capacidad}) - ${self.tarifa_hora:,.0f}/hora"


class AlquilerEquipo(Servicio):
    """Alquiler de equipos: tarifa por hora más un seguro fijo por equipo."""

    def __init__(self, nombre, tarifa_hora, seguro, disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        if not isinstance(seguro, (int, float)) or seguro < 0:
            raise ServicioInvalidoError("El seguro debe ser un número no negativo")
        self.seguro = float(seguro)

    def calcular_costo(self, horas):
        return self.tarifa_hora * horas + self.seguro

    def validar_parametros(self, horas, **opciones):
        if not 1 <= horas <= 72:
            raise ServicioInvalidoError("Un equipo se alquila entre 1 y 72 horas")

    def describir(self):
        return (f"Equipo '{self.nombre}' - ${self.tarifa_hora:,.0f}/hora "
                f"+ seguro ${self.seguro:,.0f}")


class AsesoriaEspecializada(Servicio):
    """Asesorías: la tarifa se multiplica según el nivel del asesor."""

    FACTORES = {"junior": 1.0, "senior": 1.5, "experto": 2.0}

    def __init__(self, nombre, tarifa_hora, nivel, disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        if nivel not in self.FACTORES:
            raise ServicioInvalidoError(
                f"Nivel '{nivel}' no válido; use: {', '.join(self.FACTORES)}")
        self.nivel = nivel

    def calcular_costo(self, horas):
        return self.tarifa_hora * self.FACTORES[self.nivel] * horas

    def validar_parametros(self, horas, **opciones):
        if not 1 <= horas <= 6:
            raise ServicioInvalidoError("Una asesoría dura entre 1 y 6 horas")

    def describir(self):
        return f"Asesoría '{self.nombre}' nivel {self.nivel} - ${self.tarifa_hora:,.0f}/hora base"
