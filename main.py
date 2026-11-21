# -*- coding: utf-8 -*-
"""
Software FJ - Sistema integral de clientes, servicios y reservas.
Curso Programación (213023) - Fase 4.

Ejecutar:  python main.py
Simula 17 operaciones (válidas e inválidas) sin base de datos. Todo error se
registra en logs/software_fj.log y el programa continúa hasta el final.
"""

from gestor import GestorFJ
from registro import RUTA_LOG, log


def titulo(n, texto):
    print(f"\n{n:>2}. {texto}")


def simulacion():
    fj = GestorFJ()
    log.info("===== INICIO DE LA SIMULACIÓN =====")

    # ---- CLIENTES -------------------------------------------------------
    titulo(1, "Cliente válido (Ana)")
    ana = fj.registrar_cliente("ana maría torres", "1020304050", "ana.torres@correo.com", "3101234567")
    titulo(2, "Cliente válido (Luis)")
    luis = fj.registrar_cliente("Luis Pérez", "79456123", "luis.perez@correo.com", "3209876543")
    titulo(3, "Cliente inválido: correo mal escrito")
    fj.registrar_cliente("Carlos Ruiz", "52123456", "carlos-sin-arroba.com", "3001112233")
    titulo(4, "Cliente inválido: documento con letras")
    fj.registrar_cliente("Marta Díaz", "12AB56", "marta@correo.com", "3004445566")
    titulo(5, "Cliente inválido: documento duplicado")
    fj.registrar_cliente("Ana Torres Bis", "1020304050", "otra@correo.com", "3105556677")

    # ---- SERVICIOS ------------------------------------------------------
    titulo(6, "Servicio válido: sala de juntas")
    sala = fj.crear_servicio("sala", nombre="Sala Andes", tarifa_hora=60000, capacidad=10)
    titulo(7, "Servicio válido: alquiler de portátil")
    equipo = fj.crear_servicio("equipo", nombre="Portátil Pro", tarifa_hora=8000, seguro=15000)
    titulo(8, "Servicio válido: asesoría senior")
    asesoria = fj.crear_servicio("asesoria", nombre="Arquitectura de software",
                                 tarifa_hora=90000, nivel="senior")
    titulo(9, "Servicio inválido: tarifa negativa")
    fj.crear_servicio("equipo", nombre="Proyector", tarifa_hora=-500, seguro=0)
    titulo(10, "Servicio inválido: parámetro faltante (sin capacidad)")
    fj.crear_servicio("sala", nombre="Sala Fantasma", tarifa_hora=50000)

    # ---- RESERVAS -------------------------------------------------------
    titulo(11, "Reserva exitosa: Ana reserva la sala 3 h (confirmar + procesar)")
    r1 = fj.crear_reserva(ana, sala, 3, asistentes=6)
    fj.ejecutar("Confirmar reserva", r1.confirmar)
    fj.ejecutar("Procesar con IVA y 10 % de descuento", r1.procesar, descuento=0.10)

    titulo(12, "Reserva fallida: 15 asistentes en una sala para 10")
    fj.crear_reserva(luis, sala, 2, asistentes=15)

    titulo(13, "Reserva fallida: servicio no disponible")
    asesoria.cambiar_disponibilidad(False)
    r3 = fj.crear_reserva(luis, asesoria, 2)
    fj.ejecutar("Confirmar reserva", r3.confirmar)
    asesoria.cambiar_disponibilidad(True)

    titulo(14, "Reserva cancelada correctamente")
    r4 = fj.crear_reserva(luis, equipo, 24)
    fj.ejecutar("Cancelar reserva", r4.cancelar)

    titulo(15, "Operación no permitida: cancelar una reserva ya procesada")
    fj.ejecutar("Cancelar reserva procesada", r1.cancelar)

    titulo(16, "Cálculo inconsistente: descuento del 150 %")
    r5 = fj.crear_reserva(ana, asesoria, 2)
    fj.ejecutar("Confirmar reserva", r5.confirmar)
    fj.ejecutar("Procesar con descuento 150 %", r5.procesar, descuento=1.5)

    titulo(17, "Reserva fallida: cliente inexistente (None)")
    fj.crear_reserva(None, sala, 1)

    # ---- RESUMEN --------------------------------------------------------
    print("\n" + "=" * 60)
    print(f"Clientes registrados: {len(fj.clientes)} | Servicios: {len(fj.servicios)} "
          f"| Reservas: {len(fj.reservas)}")
    for reserva in fj.reservas:
        print("  -", reserva)
    print("\nPolimorfismo: el mismo método calcular_costo_total() con 2 h:")
    for servicio in fj.servicios:
        print(f"  - {servicio.nombre:<26} -> ${servicio.calcular_costo_total(2):>12,.2f}")
    print("=" * 60)
    print(f"El programa terminó sin interrupciones. Revise el log en:\n{RUTA_LOG}")
    log.info("===== FIN DE LA SIMULACIÓN =====")


if __name__ == "__main__":
    simulacion()
