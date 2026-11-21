# Software FJ – Sistema Integral de Gestión de Clientes, Servicios y Reservas

**Universidad Nacional Abierta y a Distancia – UNAD**
Escuela de Ciencias Básicas, Tecnología e Ingeniería (ECBTI)
Programa: Ingeniería de Sistemas
Curso: Programación – Código 213023 – Fase 4

**Autor:** Andres Felipe Escobar Yusunguaira – Estudiante de Ingeniería de Sistemas

---

## Descripción

Aplicación orientada a objetos en Python que gestiona clientes, servicios
(reserva de salas, alquiler de equipos y asesorías especializadas) y reservas
para la empresa Software FJ. **No usa bases de datos**: toda la información se
maneja con objetos y listas internas; el único archivo que se escribe es el
log de eventos y errores (`logs/software_fj.log`).

## Cómo ejecutar

Requiere Python 3.8 o superior, sin librerías externas.

```bash
python main.py
```

El programa simula 20 operaciones (válidas e inválidas), muestra el resultado
de cada una en consola y termina con un resumen. Ningún error detiene la
ejecución.

## Estructura del proyecto

```
SoftwareFJ/
├── main.py                  # Programa principal: simulación de 20 operaciones
├── README.md
├── logs/software_fj.log     # Se genera al ejecutar
└── software_fj/
    ├── entidad.py           # Clase abstracta EntidadBase
    ├── cliente.py           # Clase Cliente (encapsulación y validaciones)
    ├── servicios.py         # Clase abstracta Servicio + 3 servicios derivados
    ├── reserva.py           # Clase Reserva (confirmar, cancelar, procesar)
    ├── sistema.py           # Gestor con listas internas
    ├── excepciones.py       # Excepciones personalizadas
    └── logger.py            # Registro de eventos y errores en archivo
```

## Cumplimiento de los requisitos

| Requisito | Dónde se aplica |
|---|---|
| Clase abstracta de entidades generales | `EntidadBase` (ABC) con `validar()` y `describir()` abstractos |
| Cliente con validaciones y encapsulación | `Cliente`: atributos privados (`__documento`, `__correo`…) con propiedades que validan cada dato; el documento se muestra enmascarado |
| Clase abstracta Servicio + 3 servicios | `Servicio` → `ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada` |
| Polimorfismo / métodos sobrescritos | Cada servicio sobrescribe `costo_base()`, `describir()`, `validar()` y `validar_parametros()` |
| Clase Reserva | Integra cliente, servicio, duración y estado; métodos `confirmar()`, `cancelar()`, `procesar()` |
| Métodos sobrecargados | `calcular_costo(d)`, `calcular_costo(d, iva)`, `calcular_costo(d, iva, descuento)` con `@typing.overload`; y `cotizar()` con `@singledispatchmethod` (acepta `int`, `float` o `dict`) |
| Excepciones personalizadas | Jerarquía en `excepciones.py` con base `SoftwareFJError` y códigos `SFJ-xxx` |
| try / except | `main.ejecutar()` y todos los flujos |
| try / except / else | `Reserva.confirmar()` y `main.ejecutar()` |
| try / except / finally | `Reserva.procesar()` y `main.ejecutar()` |
| Encadenamiento (`raise … from …`) | Tarifa no numérica (`ValueError` → `ValidacionError`) y confirmación fallida (`ValidacionError` → `ReservaError`) |
| Archivo de logs | `logger.py` → `logs/software_fj.log` (incluye la causa original de errores encadenados) |
| Sin base de datos | Listas privadas `__clientes`, `__servicios`, `__reservas` en `SistemaSoftwareFJ` |
| Mínimo 10 operaciones simuladas | 20 operaciones: 8 exitosas y 12 fallidas controladas |

## Operaciones simuladas

| # | Operación | Resultado esperado |
|---|---|---|
| 01–02 | Registro de clientes válidos | ✓ |
| 03 | Cliente con correo inválido | ✗ `ValidacionError` |
| 04 | Cliente sin nombre | ✗ `ParametroFaltanteError` |
| 05 | Documento duplicado | ✗ `ClienteDuplicadoError` |
| 06–08 | Creación de los tres servicios | ✓ |
| 09 | Tarifa no numérica | ✗ `ValidacionError` encadenado a `ValueError` |
| 10 | Asesoría con nivel inexistente | ✗ `ValidacionError` |
| 11 | Reserva de sala creada, confirmada y procesada | ✓ |
| 12 | Alquiler de portátiles con 10 % de descuento | ✓ |
| 13 | Sala por 20 horas (máximo 12) | ✗ `ValidacionError` |
| 14 | Cliente inexistente | ✗ `ClienteNoEncontradoError` |
| 15 | Servicio no disponible | ✗ `ServicioNoDisponibleError` |
| 16 | Procesar una reserva cancelada | ✗ `OperacionNoPermitidaError` |
| 17 | Descuento del 150 % | ✗ `ReservaError` encadenado a `ValidacionError` |
| 18 | Confirmar dos veces | ✗ `OperacionNoPermitidaError` |
| 19 | Demostración de métodos sobrecargados | ✓ |
| 20 | Cotizar con un texto | ✗ `ValidacionError` |

## Reglas de negocio

- **Sala:** tarifa por hora, máximo 12 horas, recargo del 10 % si supera 8 horas; capacidad entre 1 y 200.
- **Equipos:** tarifa por día y por unidad, solo días completos, máximo 30 días, 5 % de descuento desde 7 días.
- **Asesoría:** tarifa por hora con multiplicador según nivel (junior ×1.0, senior ×1.5, experto ×2.0), entre 1 y 40 horas.
- Al confirmar una reserva se aplica IVA del 19 % y el descuento opcional.
