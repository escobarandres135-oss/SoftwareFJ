"""
Programa principal - Sistema Integral de Gestión de Clientes, Servicios y Reservas
Empresa: Software FJ

Universidad Nacional Abierta y a Distancia - UNAD
Escuela de Ciencias Básicas, Tecnología e Ingeniería - ECBTI
Programa: Ingeniería de Sistemas
Curso: Programación (213023) - Fase 4

Autor: Andres Felipe Escobar Yusunguaira - Estudiante de Ingeniería de Sistemas

Ejecutar con:   python main.py
Simula 14 operaciones completas (válidas e inválidas). Ningún error detiene
el programa: todos se capturan, se muestran en pantalla y se guardan en
logs/software_fj.log
"""

from software_fj.sistema import SistemaSoftwareFJ
from software_fj.servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from software_fj.excepciones import SoftwareFJError
from software_fj.logger import registrar_error, registrar_evento, RUTA_LOG

sistema = SistemaSoftwareFJ()
resultados = {"exitosas": 0, "fallidas": 0}


def ejecutar(numero, descripcion, operacion):
    """
    Ejecuta una operación de forma segura. Ningún error detiene el sistema.
    Usa try / except / else / finally.
    """
    print(f"\n[{numero:02d}] {descripcion}")
    try:
        resultado = operacion()
    except SoftwareFJError as e:
        resultados["fallidas"] += 1
        print(f"     ✗ ERROR CONTROLADO -> {e}")
        if e.__cause__:
            print(f"       Causa original: {type(e.__cause__).__name__}: {e.__cause__}")
        registrar_error(e, f"Operación {numero:02d} ({descripcion})")
    except Exception as e:  # Errores inesperados: también se controlan
        resultados["fallidas"] += 1
        print(f"     ✗ ERROR INESPERADO -> {type(e).__name__}: {e}")
        registrar_error(e, f"Operación {numero:02d} - error inesperado")
    else:
        resultados["exitosas"] += 1
        print(f"     ✓ OK -> {resultado}")
    finally:
        registrar_evento(f"Operación {numero:02d} finalizada")


def main():
    print("=" * 72)
    print("  SOFTWARE FJ - Sistema de Gestión de Clientes, Servicios y Reservas")
    print("  Autor: Andres Felipe Escobar Yusunguaira - Ing. de Sistemas UNAD")
    print("=" * 72)

    # ------------------------------ CLIENTES -------------------------------
    ejecutar(1, "Registrar cliente válido (Laura Gómez)",
             lambda: sistema.registrar_cliente("1023456789", "laura gómez",
                                               "laura.gomez@mail.com", "3104567890").describir())
    ejecutar(2, "Registrar cliente válido (Carlos Ruiz)",
             lambda: sistema.registrar_cliente("80123456", "Carlos Ruiz",
                                               "cruiz@empresa.co", "3209876543").describir())
    ejecutar(3, "Registrar cliente con correo inválido",
             lambda: sistema.registrar_cliente("52987654", "Ana Torres",
                                               "ana.torres@", "3001112233"))
    ejecutar(4, "Registrar cliente sin nombre (parámetro faltante)",
             lambda: sistema.registrar_cliente("1111222233", None,
                                               "x@mail.com", "3001112233"))
    ejecutar(5, "Registrar cliente con documento duplicado",
             lambda: sistema.registrar_cliente("80123456", "Pedro Díaz",
                                               "pdiaz@mail.com", "3150001122"))

    # ------------------------------ SERVICIOS ------------------------------
    ejecutar(6, "Crear servicio: Sala de juntas",
             lambda: sistema.agregar_servicio(
                 ReservaSala("Sala Ejecutiva", 50000, capacidad=12)).describir())
    ejecutar(7, "Crear servicio: Alquiler de portátiles",
             lambda: sistema.agregar_servicio(
                 AlquilerEquipo("Portátiles", 35000, "Laptop Core i7", cantidad=5)).describir())
    ejecutar(8, "Crear servicio: Asesoría en ciberseguridad",
             lambda: sistema.agregar_servicio(
                 AsesoriaEspecializada("Ciberseguridad", 120000, "Seguridad informática",
                                       nivel="senior")).describir())
    ejecutar(9, "Crear servicio con tarifa no numérica (encadenamiento)",
             lambda: sistema.agregar_servicio(
                 ReservaSala("Sala Norte", "cincuenta mil", capacidad=10)))
    ejecutar(10, "Crear asesoría con nivel inexistente",
             lambda: sistema.agregar_servicio(
                 AsesoriaEspecializada("Cloud", 90000, "Nube", nivel="maestro")))

    # ------------------------------ RESERVAS -------------------------------
    def reserva_exitosa():
        r = sistema.crear_reserva("1023456789", "Sala Ejecutiva", 4)
        r.confirmar()
        r.procesar()
        return r.describir()
    ejecutar(11, "Reserva completa: crear, confirmar y procesar sala (4 h)", reserva_exitosa)

    def reserva_con_descuento():
        r = sistema.crear_reserva("80123456", "Portátiles", 7, descuento=0.10)
        r.confirmar()
        r.procesar()
        return r.describir()
    ejecutar(12, "Reserva de portátiles por 7 días con 10 % de descuento",
             reserva_con_descuento)

    ejecutar(13, "Reserva con duración excesiva (sala por 20 h)",
             lambda: sistema.crear_reserva("1023456789", "Sala Ejecutiva", 20))
    ejecutar(14, "Reserva para cliente inexistente",
             lambda: sistema.crear_reserva("99999999", "Ciberseguridad", 2))

    def servicio_no_disponible():
        servicio = sistema.buscar_servicio("Ciberseguridad")
        servicio.cambiar_disponibilidad(False)
        try:
            return sistema.crear_reserva("80123456", "Ciberseguridad", 3)
        finally:
            servicio.cambiar_disponibilidad(True)   # se restaura siempre
    ejecutar(15, "Reserva sobre servicio temporalmente no disponible",
             servicio_no_disponible)

    def cancelar_y_procesar():
        r = sistema.crear_reserva("80123456", "Ciberseguridad", 3)
        r.cancelar("El cliente reprogramó")
        r.procesar()                  # no permitido: ya está cancelada
    ejecutar(16, "Cancelar reserva y luego intentar procesarla", cancelar_y_procesar)

    def descuento_invalido():
        r = sistema.crear_reserva("1023456789", "Ciberseguridad", 2, descuento=1.5)
        r.confirmar()                 # ReservaError encadenado a ValidacionError
    ejecutar(17, "Confirmar reserva con descuento inválido (150 %)", descuento_invalido)

    def doble_confirmacion():
        r = sistema.crear_reserva("1023456789", "Ciberseguridad", 2)
        r.confirmar()
        r.confirmar()
    ejecutar(18, "Confirmar dos veces la misma reserva", doble_confirmacion)

    # --------------------------- SOBRECARGA ---------------------------------
    def demostrar_sobrecarga():
        s = sistema.buscar_servicio("Ciberseguridad")
        return (f"base=${s.calcular_costo(2):,.0f} | "
                f"con IVA=${s.calcular_costo(2, 0.19):,.0f} | "
                f"IVA+desc 10%=${s.calcular_costo(2, 0.19, 0.10):,.0f} | "
                f"cotizar(2)=${s.cotizar(2):,.0f} | "
                f"cotizar(dict)=${s.cotizar({'duracion': 2, 'descuento': 0.2}):,.0f}")
    ejecutar(19, "Métodos sobrecargados de cálculo de costos", demostrar_sobrecarga)

    ejecutar(20, "Cotizar con un tipo no soportado (texto)",
             lambda: sistema.buscar_servicio("Sala Ejecutiva").cotizar("cuatro horas"))

    # ------------------------------ RESUMEN --------------------------------
    print("\n" + "=" * 72)
    print("  RESUMEN")
    print("=" * 72)
    print(f"  Operaciones exitosas: {resultados['exitosas']}")
    print(f"  Operaciones con error controlado: {resultados['fallidas']}")
    print(f"  Clientes registrados: {len(sistema.clientes)}")
    for c in sistema.clientes:
        print(f"    - {c}")
    print(f"  Servicios activos: {len(sistema.servicios)}")
    for s in sistema.servicios:
        print(f"    - {s}")   # polimorfismo: cada servicio se describe distinto
    print(f"  Reservas: {len(sistema.reservas)}")
    for r in sistema.reservas:
        print(f"    - {r}")
    print(f"  Total facturado (reservas procesadas): ${sistema.total_facturado():,.2f}")
    print(f"\n  Log de eventos y errores: {RUTA_LOG}")
    print("  El sistema finalizó sin interrupciones.")
    registrar_evento("===== Sistema Software FJ finalizado correctamente =====")


if __name__ == "__main__":
    main()
