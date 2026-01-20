"""
EJERCICIO 3: COMUNICACIÓN ENTRE PROCESOS CON QUEUE
===================================================
- Un proceso lee números de un fichero y los pone en una Queue
- Otro proceso lee de la Queue y calcula la suma
- Se usa None como señal de finalización
"""

import multiprocessing
import os


def leer_numeros(cola, fichero):
    """
    Lee números de un fichero (uno por línea) y los añade a la cola.
    Al terminar, añade None para indicar que no hay más números.
    """
    pid = os.getpid()
    print(f"[Lector {pid}] Iniciando lectura del fichero '{fichero}'...")

    try:
        with open(fichero, 'r') as f:
            for linea in f:
                linea = linea.strip()
                if linea:
                    numero = int(linea)
                    cola.put(numero)
                    print(f"[Lector {pid}] Añadido a la cola: {numero}")
    except FileNotFoundError:
        print(f"[Lector {pid}] ERROR: No se encontró el fichero '{fichero}'")
    except ValueError as e:
        print(f"[Lector {pid}] ERROR: Valor no válido en el fichero: {e}")

    # Señal de finalización
    cola.put(None)
    print(f"[Lector {pid}] Lectura completada. Enviado None para finalizar.")


def sumar_numeros(cola):
    """
    Lee números de la cola y los suma hasta recibir None.
    """
    pid = os.getpid()
    print(f"[Sumador {pid}] Esperando números de la cola...")

    suma = 0
    contador = 0

    while True:
        numero = cola.get()

        if numero is None:
            print(f"[Sumador {pid}] Recibido None. Finalizando suma.")
            break

        suma += numero
        contador += 1
        print(f"[Sumador {pid}] Recibido: {numero} | Suma parcial: {suma}")

    print(f"[Sumador {pid}] RESULTADO FINAL: Suma de {contador} números = {suma}")


def main():
    print("=" * 60)
    print("COMUNICACIÓN ENTRE PROCESOS CON QUEUE")
    print("=" * 60)

    # Crear la cola para comunicación entre procesos
    cola = multiprocessing.Queue()

    # Ruta del fichero de números
    fichero = "Parte1/numeros.txt"

    # Crear los dos procesos
    proceso_lector = multiprocessing.Process(
        target=leer_numeros,
        args=(cola, fichero)
    )
    proceso_sumador = multiprocessing.Process(
        target=sumar_numeros,
        args=(cola,)
    )

    print(f"\nProceso principal PID: {os.getpid()}")
    print("Iniciando procesos...\n")

    # Iniciar ambos procesos
    proceso_lector.start()
    proceso_sumador.start()

    # Esperar a que terminen
    proceso_lector.join()
    proceso_sumador.join()

    print("\n" + "=" * 60)
    print("Ambos procesos han terminado.")
    print("=" * 60)


if __name__ == "__main__":
    main()
