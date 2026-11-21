# Software FJ - Sistema integral de clientes, servicios y reservas

Curso Programación (213023) - UNAD - Fase 4 (manejo de excepciones).

## Cómo ejecutarlo
    python main.py
Solo usa la biblioteca estándar de Python 3.8+. No requiere base de datos.
Los errores y eventos quedan en `logs/software_fj.log`.

## Estructura
| Archivo | Contenido |
|---|---|
| `excepciones.py` | Excepciones personalizadas (jerarquía desde `ErrorSoftwareFJ`) |
| `registro.py` | Configuración del archivo de logs |
| `entidades.py` | `EntidadBase` (abstracta) y `Cliente` (encapsulación y validación) |
| `servicios.py` | `Servicio` (abstracta), `ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada` |
| `reservas.py` | `Reserva`: confirmar, cancelar y procesar (try/except/else/finally y `raise ... from`) |
| `gestor.py` | `GestorFJ`: listas internas y operaciones "seguras" que registran el error y continúan |
| `main.py` | Simulación de 17 operaciones válidas e inválidas |

## Conceptos aplicados
- **Abstracción:** `EntidadBase` y `Servicio` son clases abstractas (`ABC`).
- **Herencia y polimorfismo:** tres servicios sobrescriben `calcular_costo`, `validar_parametros` y `describir`.
- **Encapsulación:** atributos privados con propiedades que validan en `Cliente`.
- **Sobrecarga simulada:** `calcular_costo_total(horas, impuesto=None, descuento=0.0)` con parámetros opcionales.
- **Excepciones:** personalizadas, `try/except`, `try/except/else`, `try/except/finally` y encadenamiento.
