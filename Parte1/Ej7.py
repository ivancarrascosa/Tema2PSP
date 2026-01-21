import multiprocessing

SENAL_FIN = None


def leerNumeros(fichero, cola):
    """Lee pares de números de un fichero y los pone en la cola."""
    with open(fichero, 'r') as f:
        for linea in f:
            partes = linea.strip().split()
            if len(partes) == 2:
                num1, num2 = int(partes[0]), int(partes[1])
                cola.put((num1, num2))
    cola.put(SENAL_FIN)


def sumarNumeros(cola, cola_resultados):
    """Recibe pares de números de la cola y calcula la suma del rango."""
    datos = cola.get()
    while datos is not SENAL_FIN:
        num1, num2 = datos
        inicio, fin = min(num1, num2), max(num1, num2)
        suma = sum(range(inicio, fin + 1))
        cola_resultados.put(f"Rango ({num1}, {num2}): La suma total es {suma}")
        datos = cola.get()
    cola_resultados.put(SENAL_FIN)


if __name__ == '__main__':
    cola_numeros = multiprocessing.Queue()
    cola_resultados = multiprocessing.Queue()

    proceso_lector = multiprocessing.Process(target=leerNumeros, args=('Parte1/numeros.txt', cola_numeros))
    proceso_sumador = multiprocessing.Process(target=sumarNumeros, args=(cola_numeros, cola_resultados))

    proceso_lector.start()
    proceso_sumador.start()

    proceso_lector.join()
    proceso_sumador.join()

    resultado = cola_resultados.get()
    while resultado is not SENAL_FIN:
        print(resultado)
        resultado = cola_resultados.get()
