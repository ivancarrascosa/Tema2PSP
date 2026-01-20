from multiprocessing import Pipe, Process
import os


def leer_numeros(conn, fichero):
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
                    conn.send(numero)
                    print(f"[Lector {pid}] Añadido a la cola: {numero}")
    except FileNotFoundError:
        print(f"[Lector {pid}] ERROR: No se encontró el fichero '{fichero}'")
    except ValueError as e:
        print(f"[Lector {pid}] ERROR: Valor no válido en el fichero: {e}")

    # Señal de finalización
    conn.send(None)
    print(f"[Lector {pid}] Lectura completada. Enviado None para finalizar.")

def sumar_numeros(conn):
    suma = 0
    numero = 0

    numero = conn.recv()
    while numero != None:
        suma += numero
        numero = conn.recv()
    print(f"La suma total es {suma}")
    conn.close()

if __name__ == '__main__':
    left, right = Pipe()
    p1 = Process(target=leer_numeros, args=(left, "Parte1/numeros.txt"))
    p2 = Process(target=sumar_numeros, args=(right,))

    p1.start()
    p2.start()

    p1.join()
    p2.join()


