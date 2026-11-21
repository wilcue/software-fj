# -*- coding: utf-8 -*-
"""
Clase abstracta base del sistema y clase Cliente.

EntidadBase representa "cualquier cosa con identidad propia" (clientes,
servicios y reservas). Obliga a que cada hija sepa describirse.
"""

import re
from abc import ABC, abstractmethod
from itertools import count

from excepciones import ClienteInvalidoError


class EntidadBase(ABC):
    """Clase abstracta: no se puede instanciar directamente."""

    _contadores = {}               # un contador independiente por familia
    _FAMILIA = "entidad"           # las hijas lo sobrescriben (cliente, servicio...)

    def __init__(self):
        # Encapsulación: el id se guarda "privado" y solo se lee por propiedad.
        contador = EntidadBase._contadores.setdefault(self._FAMILIA, count(1))
        self._id = next(contador)

    @property
    def id(self):
        return self._id

    @abstractmethod
    def describir(self):
        """Cada entidad devuelve un texto que la describe."""

    def __str__(self):
        return self.describir()


class Cliente(EntidadBase):
    """Cliente de Software FJ con datos personales encapsulados y validados."""

    _FAMILIA = "cliente"
    _PATRON_CORREO = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")

    def __init__(self, nombre, documento, correo, telefono):
        super().__init__()
        # Cada asignación pasa por su setter, que valida antes de guardar.
        self.nombre = nombre
        self.documento = documento
        self.correo = correo
        self.telefono = telefono

    # --- nombre ------------------------------------------------------------
    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ClienteInvalidoError("El nombre debe ser texto de al menos 3 caracteres")
        if any(ch.isdigit() for ch in valor):
            raise ClienteInvalidoError("El nombre no puede contener números")
        self.__nombre = valor.strip().title()

    # --- documento ---------------------------------------------------------
    @property
    def documento(self):
        return self.__documento

    @documento.setter
    def documento(self, valor):
        texto = str(valor).strip() if valor is not None else ""
        if not texto.isdigit() or not (6 <= len(texto) <= 12):
            raise ClienteInvalidoError("El documento debe tener entre 6 y 12 dígitos")
        self.__documento = texto

    # --- correo ------------------------------------------------------------
    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        if not isinstance(valor, str) or not self._PATRON_CORREO.match(valor.strip()):
            raise ClienteInvalidoError(f"Correo electrónico inválido: {valor!r}")
        self.__correo = valor.strip().lower()

    # --- teléfono ----------------------------------------------------------
    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        texto = str(valor).strip() if valor is not None else ""
        if not texto.isdigit() or len(texto) != 10:
            raise ClienteInvalidoError("El teléfono debe tener exactamente 10 dígitos")
        self.__telefono = texto

    def describir(self):
        return f"Cliente #{self.id}: {self.nombre} (doc. {self.documento}, {self.correo})"
