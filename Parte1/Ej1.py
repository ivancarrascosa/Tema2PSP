"""
EJERCICIO DE MULTIPROCESSING CON POOL
======================================
Comparación entre usar una lista de procesos vs Pool

Un Pool es un "grupo de trabajadores" que gestiona automáticamente
la creación, asignación y reutilización de procesos.
"""

import multiprocessing
import time
import os


def sumar_numeros(n):
    """
    Función que suma todos los números desde 1 hasta n (inclusive).
    Ahora retorna el resultado en lugar de solo imprimirlo.
    """
    pid = os.getpid()
    print(f"[Worker {pid}] Calculando suma hasta {n:,}...")
    
    resultado = 0
    for i in range(1, n + 1):
        resultado += i
    
    print(f"[Worker {pid}] Suma hasta {n:,} = {resultado:,}")
    return resultado  # ¡Importante! Con Pool podemos retornar valores


def metodo_lista_procesos(valores):
    """
    MÉTODO 1: Lista de procesos (como lo tenías antes)
    """
    print("\n" + "=" * 60)
    print("MÉTODO 1: LISTA DE PROCESOS")
    print("=" * 60)
    
    tiempo_inicio = time.time()
    
    # Crear procesos manualmente
    procesos = []
    for valor in valores:
        p = multiprocessing.Process(target=sumar_numeros, args=(valor,))
        procesos.append(p)
    
    # Iniciar todos
    for p in procesos:
        p.start()
    
    # Esperar a todos
    for p in procesos:
        p.join()
    
    tiempo_total = time.time() - tiempo_inicio
    
    print(f"\n⏱  Tiempo: {tiempo_total:.4f} segundos")
    print("❌ LIMITACIÓN: No podemos obtener los valores de retorno fácilmente")
    
    return tiempo_total


def metodo_pool(valores):
    """
    MÉTODO 2: Pool de procesos (RECOMENDADO)
    """
    print("\n" + "=" * 60)
    print("MÉTODO 2: POOL DE PROCESOS")
    print("=" * 60)
    
    tiempo_inicio = time.time()
    
    # Crear un Pool con tantos workers como CPUs disponibles
    # El Pool gestiona automáticamente los procesos
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        
        # map() distribuye los valores entre los workers automáticamente
        # y RETORNA los resultados en orden
        resultados = pool.map(sumar_numeros, valores)
    
    tiempo_total = time.time() - tiempo_inicio
    
    print(f"\n⏱  Tiempo: {tiempo_total:.4f} segundos")
    print(f"✅ Resultados obtenidos: {resultados}")
    
    return tiempo_total, resultados


def metodo_pool_con_muchas_tareas(num_tareas=20):
    """
    MÉTODO 3: Pool con MUCHAS tareas pequeñas
    Aquí es donde Pool realmente brilla - reutiliza workers
    """
    print("\n" + "=" * 60)
    print(f"MÉTODO 3: POOL CON {num_tareas} TAREAS (reutilización de workers)")
    print("=" * 60)
    
    # Muchas tareas pequeñas
    valores = [1_000_000] * num_tareas
    
    tiempo_inicio = time.time()
    
    with multiprocessing.Pool(processes=4) as pool:
        resultados = pool.map(sumar_numeros, valores)
    
    tiempo_total = time.time() - tiempo_inicio
    
    print(f"\n⏱  Tiempo con Pool: {tiempo_total:.4f} segundos")
    print(f"📊 {num_tareas} tareas ejecutadas por solo 4 workers")
    print("✅ Los workers se REUTILIZAN - no se crean 20 procesos")
    
    return tiempo_total


def demostrar_metodos_pool():
    """
    Demostración de los diferentes métodos de Pool
    """
    print("\n" + "=" * 60)
    print("DIFERENTES MÉTODOS DE POOL")
    print("=" * 60)
    
    valores = [5_000_000, 10_000_000, 7_500_000, 12_000_000]
    
    with multiprocessing.Pool(processes=4) as pool:
        
        # ----------------------------------------
        # 1. map() - El más simple y común
        # ----------------------------------------
        print("\n📌 pool.map() - Bloquea hasta tener todos los resultados")
        resultados_map = pool.map(sumar_numeros, valores)
        print(f"   Resultados: {resultados_map}")
        
        # ----------------------------------------
        # 2. map_async() - No bloqueante
        # ----------------------------------------
        print("\n📌 pool.map_async() - No bloquea, devuelve AsyncResult")
        async_result = pool.map_async(sumar_numeros, valores)
        print("   Podemos hacer otras cosas mientras se calculan...")
        resultados_async = async_result.get()  # Aquí sí esperamos
        print(f"   Resultados: {resultados_async}")
        
        # ----------------------------------------
        # 3. apply_async() - Para tareas individuales
        # ----------------------------------------
        print("\n📌 pool.apply_async() - Para enviar tareas una a una")
        tareas = []
        for v in valores:
            tarea = pool.apply_async(sumar_numeros, (v,))
            tareas.append(tarea)
        
        resultados_apply = [t.get() for t in tareas]
        print(f"   Resultados: {resultados_apply}")


def main():
    print("=" * 60)
    print("COMPARACIÓN: LISTA DE PROCESOS vs POOL")
    print("=" * 60)
    print(f"CPUs disponibles: {multiprocessing.cpu_count()}")
    
    valores = [10_000_000, 20_000_000, 15_000_000, 25_000_000]
    
    # Ejecutar ambos métodos
    tiempo_lista = metodo_lista_procesos(valores)
    tiempo_pool, resultados = metodo_pool(valores)
    
    # Demostrar reutilización de workers
    metodo_pool_con_muchas_tareas(20)
    
    # Resumen comparativo
    print("\n" + "=" * 60)
    print("RESUMEN: ¿POR QUÉ POOL ES MEJOR?")
    print("=" * 60)
    
    print("""
┌─────────────────────────────────────────────────────────────────┐
│                    LISTA DE PROCESOS                            │
├─────────────────────────────────────────────────────────────────┤
│ ❌ Crear proceso nuevo para CADA tarea                          │
│ ❌ No retorna valores fácilmente                                │
│ ❌ Gestión manual de start() y join()                           │
│ ❌ Si hay 100 tareas → 100 procesos (¡sobrecarga!)              │
│ ❌ Más código, más propenso a errores                           │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                         POOL                                    │
├─────────────────────────────────────────────────────────────────┤
│ ✅ Número FIJO de workers (reutilizables)                       │
│ ✅ Retorna valores directamente                                 │
│ ✅ Gestión automática (with statement)                          │
│ ✅ Si hay 100 tareas → solo N workers las procesan              │
│ ✅ Código más limpio y pythónico                                │
│ ✅ Métodos útiles: map, map_async, apply_async, starmap         │
└─────────────────────────────────────────────────────────────────┘
""")
    
    print("ANALOGÍA PARA ENTENDER LA DIFERENCIA:")
    print("-" * 60)
    print("""
🏭 LISTA DE PROCESOS = Contratar un empleado nuevo para cada tarea
   - Llega cliente 1 → Contratas empleado 1
   - Llega cliente 2 → Contratas empleado 2
   - ...
   - Llega cliente 100 → Contratas empleado 100
   → ¡Muy costoso! Cada contratación lleva tiempo.

🏭 POOL = Tener un equipo fijo de empleados
   - Tienes 4 empleados fijos
   - Llega cliente 1 → Empleado 1 lo atiende
   - Llega cliente 2 → Empleado 2 lo atiende
   - Empleado 1 termina → Atiende al cliente 5
   - ...
   → ¡Eficiente! Los empleados se reutilizan.
""")
    
    print("\n" + "=" * 60)
    print("CUÁNDO USAR CADA UNO")
    print("=" * 60)
    print("""
📌 USA POOL CUANDO:
   • Tienes muchas tareas similares
   • Necesitas los valores de retorno
   • Quieres código limpio y mantenible
   • La cantidad de tareas puede variar

📌 USA LISTA DE PROCESOS CUANDO:
   • Necesitas control muy específico de cada proceso
   • Los procesos deben ejecutar funciones diferentes
   • Necesitas comunicación compleja entre procesos
   • Solo tienes 2-3 procesos puntuales
""")


if __name__ == "__main__":
    main()